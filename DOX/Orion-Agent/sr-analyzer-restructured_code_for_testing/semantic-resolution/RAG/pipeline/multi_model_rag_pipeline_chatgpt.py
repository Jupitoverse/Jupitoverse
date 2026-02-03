"""
Multi-Model SR Analysis RAG Pipeline with ChatGPT
Intelligent Service Request Analysis using 5 LLM Calls + Keywords Extraction

Architecture:
- LLM CALL 1: Find Semantic Workaround (fallback if none from search)
- LLM CALL 2: Java Error Detection (5-Source Voting)
- LLM CALL 3a: Extract Activity Keywords (for fuzzy search)
- LLM CALL 3b: Extract Activity Names (from available classes)
- LLM CALL 4a/4b: Java or General Resolution
- LLM CALL 5: Skill-Based SR Assignment

Context Sources:
1. javaMapping.db - Java class metadata (fuzzy search for activity names)
2. comcast_code (ChromaDB) - Backend code semantic search  
3. clean_history_data (ChromaDB) - Historical SR semantic search
4. PostgreSQL (via activity_name_finder) - Activity implementation lookup
5. people_skills.db - Team skills and availability

API: https://ai-framework1:8085/api/v1/call_llm
Token File: sr-analyzer/semantic-resolution/tokens/Tokens.xlsx
"""

import os
import sys
import json
import re
import sqlite3
import pickle
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
import urllib3
import concurrent.futures

import pandas as pd
import requests
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set NO_PROXY for local proxy connection
os.environ["NO_PROXY"] = os.environ["no_proxy"] = "ai-framework1"

# LangChain imports
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun

# Import existing components
try:
    # Add current directory to path for activity_name_finder (already in pipeline folder)
    sys.path.insert(0, str(Path(__file__).parent))
    from activity_name_finder import ActivityFinder, find_activity
    ACTIVITY_FINDER_AVAILABLE = True
except ImportError as e:
    ACTIVITY_FINDER_AVAILABLE = False
    print(f"[WARN] ActivityFinder not available - activity validation will be skipped ({e})")

try:
    sys.path.append(str(Path(__file__).parent.parent.parent / 'analyzers'))
    from sr_text_preprocessor import SRTextPreprocessor
    PREPROCESSOR_AVAILABLE = True
except ImportError:
    PREPROCESSOR_AVAILABLE = False
    print("[WARN] SRTextPreprocessor not available")


# ============================================================================
# PROMPTS
# ============================================================================

PROMPT_FIND_SEMANTIC_WORKAROUND = """You are a semantic workaround retrieval assistant for Service Request (SR) analysis.

=== CURRENT SERVICE REQUEST ===
SR ID: {sr_id}
Description: {description}
Notes: {notes}
Resolution Category: {resolution_category}

=== HISTORICAL MATCHES FROM DATABASE ===
(These are SRs with similarity scores, may contain low-quality workarounds)

{historical_matches}

=== YOUR TASK ===
1. Analyze the current SR's core issue (symptoms, systems involved, error type)
2. Find the BEST matching workaround from historical matches
3. Ignore garbage workarounds: "NA", "N/A", "escalated", "closed", empty, too generic
4. If multiple good matches exist, COMBINE the best steps from each
5. If NO useful workaround exists, return "NO_MATCH"

=== OUTPUT FORMAT (JSON only, no explanation) ===
{{
    "matched_sr_id": "<best matching SR ID or null>",
    "similarity_reason": "<brief explanation why this matches>",
    "semantic_workaround": "<extracted or combined workaround text>",
    "quality_score": 0.0-1.0
}}

If no useful match found:
{{
    "matched_sr_id": null,
    "similarity_reason": "No relevant workaround found in historical data",
    "semantic_workaround": "NO_MATCH",
    "quality_score": 0.0
}}
"""

PROMPT_JAVA_DETECTION_VOTING = """You are a Java error detection system using 5-SOURCE VOTING mechanism.

=== CURRENT SERVICE REQUEST ===
SR ID: {sr_id}
Priority: {priority}
Description: {description}
Notes: {notes}

=== SOURCE 1: RESOLUTION CATEGORIES ===
Current SR Category: {resolution_category}
Similar SRs Categories:
{similar_categories}

Java-indicating categories: code, backend, application error, system error, service failure, application
Non-Java categories: data, interface, configuration, network, frontend, user error, UI, CRM, web

=== SOURCE 2: SEMANTIC WORKAROUND ===
{semantic_workaround}

Look for Java indicators:
- Java classes: *Service, *Controller, *Repository, *Manager, *Handler, *Impl, *Processor
- Exceptions: NullPointerException, SQLException, IOException, ClassNotFoundException, RuntimeException
- Java packages: com.amdocs.*, com.comcast.*, org.amdocs.*, org.*
- Stack traces: "at com.", "at org.", "at java."
- Java files: *.java
- Java commands: mvn, systemctl restart, jstack, jmap, catalina
- Backend terms: tomcat, jboss, wildfly

=== SOURCE 3: AI WORKAROUNDS FROM SIMILAR SRs ===
{ai_workarounds}

Count Java indicators in each AI-generated workaround (marked with "AI Generated:").

=== SOURCE 4: USER WORKAROUNDS FROM SIMILAR SRs ===
{user_workarounds}

Count Java indicators in each user workaround (marked with "Workaround:" or "User Corrected:").

=== SOURCE 5: CURRENT SR CONTENT ===
Analyze description and notes for direct Java indicators:
- Stack traces with exception names
- Java class/package references
- Backend service error messages
- .java file mentions

=== VOTING RULES ===
For each source, vote:
- "JAVA" if ≥3 Java indicators found OR strong Java evidence (stack trace, exception)
- "NON_JAVA" if non-Java keywords dominate OR customer/third-party issue indicator
- "UNKNOWN" if insufficient evidence

Final decision: is_java_error = (java_votes > non_java_votes)

Confidence calculation:
- HIGH: ≥80% agreement with ≥3 meaningful votes (java + non_java)
- MEDIUM: ≥67% agreement with ≥3 meaningful votes
- LOW: ≥60% agreement OR ≥50% with ≥4 meaningful voters
- VERY_LOW: <60% agreement

=== OUTPUT FORMAT (JSON only, no other text) ===
{{
    "votes": {{
        "category": "JAVA|NON_JAVA|UNKNOWN",
        "semantic": "JAVA|NON_JAVA|UNKNOWN",
        "ai_workarounds": "JAVA|NON_JAVA|UNKNOWN",
        "user_workarounds": "JAVA|NON_JAVA|UNKNOWN",
        "current_sr": "JAVA|NON_JAVA|UNKNOWN"
    }},
    "vote_evidence": {{
        "category": "<why this vote>",
        "semantic": "<why this vote>",
        "ai_workarounds": "<why this vote>",
        "user_workarounds": "<why this vote>",
        "current_sr": "<why this vote>"
    }},
    "java_votes": <count of JAVA votes>,
    "non_java_votes": <count of NON_JAVA votes>,
    "unknown_votes": <count of UNKNOWN votes>,
    "is_java_error": true|false,
    "confidence": "HIGH|MEDIUM|LOW|VERY_LOW",
    "issue_type": "Java/Code|Data|Configuration|Network|Interface|Unknown",
    "evidence": ["<quoted evidence 1>", "<quoted evidence 2>"]
}}
"""

# ============================================================================
# LLM CALL 3a: EXTRACT ACTIVITY KEYWORDS (for fuzzy search)
# ============================================================================

PROMPT_EXTRACT_ACTIVITY_KEYWORDS = """You are analyzing a Service Request to identify potential Java activity/class name keywords.

=== SERVICE REQUEST ===
Description: {description}
Notes: {notes}

=== TASK ===
Extract KEYWORDS that might be part of Java class/activity names mentioned in this SR.

Look for:
1. CamelCase fragments: "Validate", "Address", "Create", "Order", "Process"
2. Technical terms from errors: "decompose", "sync", "transform", "execute"
3. Domain keywords: "Payment", "Customer", "Account", "Billing", "Inventory"
4. Class name hints: Any capitalized words that look like Java classes
5. Error mentions: Words near "error", "failed", "exception", "activity"

=== OUTPUT FORMAT (JSON only) ===
{{
    "keywords": ["keyword1", "keyword2", "keyword3", ...],
    "explicit_class_names": ["AnyFullClassNameMentioned", ...]
}}

RULES:
- Extract 5-15 most relevant keywords
- Include both partial words and full class names if mentioned
- Keywords should be 3+ characters
- Include variations if unsure (e.g., "validate", "Validate", "Validation")
"""

# ============================================================================
# LLM CALL 3b: EXTRACT ACTIVITIES FROM AVAILABLE LIST
# ============================================================================

PROMPT_EXTRACT_ACTIVITIES = """You are an activity name extractor for Java backend systems.

=== CURRENT SERVICE REQUEST ===
Description: {description}
Notes: {notes}

=== SEMANTIC WORKAROUND ===
{semantic_workaround}

=== HISTORICAL WORKAROUNDS (Top 3 Similar) ===
{historical_workarounds}

=== AVAILABLE JAVA CLASSES (from codebase - SELECT ONLY FROM THIS LIST) ===
{available_class_names}

=== JAVA CODE CONTEXT ===
{java_code_context}

{retry_context}

=== TASK ===
From the AVAILABLE JAVA CLASSES list above, identify which classes are related to the error/issue in this SR.

=== MATCHING RULES ===
1. ONLY return class names that appear in the AVAILABLE JAVA CLASSES list
2. Match partial mentions: e.g., "decompose error" → select all decomposeXXX classes
3. Include related Impl classes when the base activity is mentioned
4. Match quoted names: "ValidateAddress" → select ValidateAddress and ValidateAddressImpl
5. Look for error patterns: "error in X", "X failed" → select X and related classes

=== OUTPUT FORMAT (JSON only, no other text) ===
{{
    "activity_names": [
        {{
            "name": "<EXACT class name from AVAILABLE list>",
            "evidence": "<quoted text where this was found>",
            "confidence": "high|medium|low"
        }}
    ]
}}

If no matching classes found in the available list:
{{
    "activity_names": []
}}
"""

PROMPT_RETRY_ACTIVITIES = """
=== PREVIOUS ATTEMPT - ACTIVITIES NOT FOUND ===
The following activity names were NOT FOUND in the database:
{failed_activities}

Please provide ALTERNATIVE activity names. Consider:
- Different spelling or casing (e.g., ValidateAddress vs validateAddress)
- Parent/child activity relationships
- Service name instead of activity name (e.g., AddressService instead of ValidateAddress)
- Looking at the Java code context for actual class names used
- Similar activities that might handle this functionality
"""

# ============================================================================
# LLM CALL 5: SKILL-BASED ASSIGNMENT PROMPT
# ============================================================================

PROMPT_SKILL_BASED_ASSIGNMENT = """You are an intelligent SR assignment system. Your job is to assign ONE person to handle this Service Request.

=== SERVICE REQUEST DETAILS ===
SR ID: {sr_id}
Priority: {priority}
Description: {description}
Application: {application}
Complexity Score: {complexity_score}/10
Is Java Error: {is_java_error}
Issue Type: {issue_type}

=== AVAILABLE TEAM MEMBERS ===
{team_members_context}

=== CURRENT WORKLOAD STATUS ===
{workload_status}

=== ASSIGNMENT RULES (MUST FOLLOW) ===

1. **AVAILABILITY CHECK (CRITICAL)**
   - If availability = 0% → DO NOT assign (skip this person completely)
   - If availability < 100% → Effective load = max_load × (availability/100)
   - Example: max_load=10, availability=50% → can only take 5 SRs

2. **LOAD CHECK (CRITICAL)**
   - current_load >= effective_max_load → DO NOT assign (person is full)
   - If everyone is full, select person with lowest (current_load / effective_max_load) ratio

3. **SKILL MATCHING**
   - P1/P2 SRs → Prefer skill_level >= 4.0 (experienced)
   - P3/P4 SRs → Any skill level is acceptable
   - High complexity (>7) → Require skill_level >= 4.0
   - Low complexity (<4) → Prefer lower skill level (save experts for hard SRs)

4. **EQUAL DISTRIBUTION**
   - Everyone should get at least one SR before someone gets a second
   - If multiple candidates, prefer the one with lower current_load

5. **SPECIALIZATION MATCH**
   - Match application to person's specializations when possible
   - Java errors → Prefer people with "java" in specializations

6. **TIE-BREAKER ORDER**
   If multiple candidates are equal:
   a) Lowest current_load
   b) Highest skill_level match for complexity
   c) Best specialization match

=== OUTPUT FORMAT ===
Return ONLY the name of the assigned person. Nothing else.
Use the EXACT name as shown in the AVAILABLE TEAM MEMBERS list (with spaces, not underscores).
No explanation, no reasoning, no punctuation.

Example outputs:
Praveer
John Smith
Aditya Sahore

If absolutely no one is available, return:
UNASSIGNED
"""

PROMPT_JAVA_RESOLUTION = """You are a Java backend expert generating precise fix instructions for a Service Request.

=== SERVICE REQUEST ===
SR ID: {sr_id}
Priority: {priority}
Description: {description}
Notes: {notes}

=== JAVA ERROR DETECTION RESULT ===
Is Java Error: Yes
Confidence: {detection_confidence}
Vote breakdown: {java_votes} Java, {non_java_votes} Non-Java, {unknown_votes} Unknown
Evidence:
{detection_evidence}

=== IDENTIFIED ACTIVITIES (VALIDATED) ===
{activities_with_details}

=== IMPLEMENTATION CLASSES ===
{impl_classes}

=== ACTUAL JAVA CODE (from codebase) ===
{java_code_snippets}

=== JAVA METADATA (available classes) ===
{java_metadata}

=== SEMANTIC WORKAROUND (from similar SRs) ===
{semantic_workaround}

=== HISTORICAL PATTERNS ===
{historical_patterns}

{abbreviation_context}

=== ANTI-HALLUCINATION RULES (CRITICAL) ===
1. Use ONLY file paths that appear EXACTLY in IMPLEMENTATION CLASSES or JAVA CODE sections
2. Use ONLY class names from IDENTIFIED ACTIVITIES or JAVA METADATA sections
3. If a path/class is NOT in the provided context, write: "[NEEDS INVESTIGATION - not in context]"
4. Quote exact error text from the SR description/notes using "quotes"
5. For uncertain steps, use "Investigate X" NOT "Fix X"
6. If no historical pattern matches, state: "No similar pattern found - following standard troubleshooting"
7. NEVER invent server names, IP addresses, database names, or paths not provided
8. Reference the source of each step (e.g., "Based on similar SR CAS123..." or "From code context...")

=== YOUR TASK ===
1. Confirm the Java error type with exact evidence quoted from the SR
2. Map it to the exact implementation class and file from the provided context
3. Generate a comprehensive AI WORKAROUND grounded in the provided context
4. Mark anything not found in context as "[NEEDS INVESTIGATION]"
5. Adapt historical workaround patterns to this specific SR's data

=== OUTPUT FORMAT ===

**AI WORKAROUND:**
1. [Investigation] Access the application server and check logs
   - Look for: "[exact error quoted from SR]"
   - Log location: [path from context OR "investigate standard log paths"]
2. [Investigation] Identify the failing component
   - Class: [class name from IDENTIFIED ACTIVITIES]
   - Path: [path from IMPLEMENTATION CLASSES OR "[NEEDS INVESTIGATION]"]
3. [Analysis] Determine root cause based on error pattern
   - Error type: [from detection evidence]
   - Based on: [historical pattern reference OR "requires investigation"]
4. [Resolution] Apply the fix
   - [Specific action grounded in historical pattern or code context]
5. [Resolution] Additional configuration/data updates if needed
6. [Verification] Restart affected service and verify
7. [Verification] Test the affected functionality
8. [Escalation] If unresolved after above steps, escalate to [team] with [specific info to include]
... (8-12 steps, each grounded in provided context)

=== SELF-CHECK BEFORE OUTPUT ===
- All file paths must be from provided context (not invented)
- All class names must match validated activities or metadata
- Uncertain items are marked as [NEEDS INVESTIGATION]
- Steps reference their evidence source
"""

PROMPT_GENERAL_RESOLUTION = """You are an SR resolution expert generating fix instructions for a NON-Java issue.

=== SERVICE REQUEST ===
SR ID: {sr_id}
Priority: {priority}
Resolution Category: {resolution_category}
Status Reason: {status_reason}
Description: {description}
Notes: {notes}

=== ISSUE CLASSIFICATION ===
Is Java Error: No
Issue Type: {issue_type}
Confidence: {confidence}
Vote breakdown: {java_votes} Java, {non_java_votes} Non-Java, {unknown_votes} Unknown

=== SEMANTIC WORKAROUND (from similar SRs) ===
{semantic_workaround}

=== HISTORICAL SOLUTIONS ===
{historical_solutions}

{abbreviation_context}

=== ANTI-HALLUCINATION RULES (CRITICAL) ===
1. Use ONLY information from the SR description, notes, and provided context
2. Quote exact text from the SR using "quotes" when referencing specific data
3. If specific IDs, names, or systems are mentioned in SR, use THOSE exact values
4. If information is NOT in the SR or context, write: "[NEEDS INVESTIGATION - not provided]"
5. For uncertain steps, use "Investigate X" NOT "Fix X"
6. Reference the source of each step (e.g., "Based on similar SR CAS123..." or "From SR notes...")
7. NEVER invent customer names, IDs, system names, or data not in the SR
8. If no historical pattern matches well, state: "No exact pattern found - adapting general approach"

=== YOUR TASK ===
1. Identify the core issue using exact quotes from description/notes
2. Extract the BEST pattern from semantic/historical workarounds
3. Adapt steps to THIS SR's specific data (use actual IDs, names from SR)
4. Mark anything not in SR as "[NEEDS INVESTIGATION]"

=== OUTPUT FORMAT ===

**AI WORKAROUND:**
1. [Investigation] Identify the specific issue from SR
   - Issue: "[quote exact problem from SR description]"
   - Affected: [specific data/system from SR OR "[NEEDS INVESTIGATION]"]
2. [Investigation] Check relevant systems/logs
   - Based on: [historical pattern reference OR "standard troubleshooting"]
3. [Analysis] Identify root cause
   - Symptoms match: [similar SR pattern OR "requires investigation"]
4. [Resolution] Apply fix adapted from historical workaround
   - Action: [specific step from semantic workaround, adapted with THIS SR's data]
   - Using: [actual IDs/names from SR]
5. [Resolution] Additional updates if needed
6. [Verification] Confirm resolution
   - Test: [specific to the issue type]
7. [Verification] Validate with requestor if needed
8. [Escalation] If unresolved, escalate to [team based on issue type] with [specific info]
... (8-12 steps, each grounded in SR data or historical patterns)

=== SELF-CHECK BEFORE OUTPUT ===
- All specific data (IDs, names) must be from the SR (not invented)
- Steps reference their evidence source (SR or historical pattern)
- Uncertain items are marked as [NEEDS INVESTIGATION]
- Historical patterns are adapted with THIS SR's specific data
"""


# ============================================================================
# TOKEN MANAGER
# ============================================================================

class TokenManager:
    """Manages API tokens with automatic rotation on quota exhaustion"""
    
    def __init__(self, tokens_file: Path = None):
        if tokens_file is None:
            # Tokens are now in tokens/ folder
            tokens_file = Path(__file__).parent.parent.parent / "tokens" / "Tokens.xlsx"
        
        self.tokens_file = tokens_file
        self.tokens: List[Dict[str, str]] = []
        self.current_index = 0
        self.exhausted_tokens: set = set()
        self._load_tokens()
    
    def _load_tokens(self):
        """Load tokens from Excel file"""
        if not self.tokens_file.exists():
            raise FileNotFoundError(f"Tokens file not found: {self.tokens_file}")
        
        try:
            df = pd.read_excel(self.tokens_file)
            
            email_col = None
            for col in df.columns:
                if col.strip().lower() in ['email', 'name']:
                    email_col = col
                    break
            
            token_col = None
            for col in df.columns:
                if col.lower() == 'token':
                    token_col = col
                    break
            
            if email_col and token_col:
                for _, row in df.iterrows():
                    email = str(row[email_col]).strip() if pd.notna(row[email_col]) else ""
                    token = str(row[token_col]).strip() if pd.notna(row[token_col]) else ""
                    if email and token:
                        self.tokens.append({'email': email, 'token': token})
            elif token_col:
                for _, row in df.iterrows():
                    token = str(row[token_col]).strip() if pd.notna(row[token_col]) else ""
                    if token:
                        self.tokens.append({'email': 'sr_rag_pipeline@amdocs.com', 'token': token})
            else:
                raise ValueError("Excel must have 'Token' column!")
            
            if not self.tokens:
                raise ValueError("No valid tokens found!")
            
            print(f"[TOKEN] ✅ Loaded {len(self.tokens)} API tokens")
            
        except Exception as e:
            raise ValueError(f"Error loading tokens: {e}")
    
    def get_current_token(self) -> Optional[str]:
        available = [i for i in range(len(self.tokens)) if i not in self.exhausted_tokens]
        if not available:
            return None
        while self.current_index in self.exhausted_tokens:
            self.current_index = (self.current_index + 1) % len(self.tokens)
        return self.tokens[self.current_index]['token']
    
    def get_current_email(self) -> Optional[str]:
        if not self.tokens or self.current_index >= len(self.tokens):
            return None
        return self.tokens[self.current_index]['email']
    
    def mark_exhausted(self) -> bool:
        self.exhausted_tokens.add(self.current_index)
        print(f"[TOKEN] ⚠️ Token #{self.current_index + 1} exhausted")
        for i in range(len(self.tokens)):
            next_idx = (self.current_index + 1 + i) % len(self.tokens)
            if next_idx not in self.exhausted_tokens:
                self.current_index = next_idx
                print(f"[TOKEN] ✅ Rotated to token #{self.current_index + 1}")
                return True
        return False
    
    def get_status(self) -> str:
        available = len(self.tokens) - len(self.exhausted_tokens)
        return f"Tokens: {available}/{len(self.tokens)} available"


# ============================================================================
# LLM WRAPPER
# ============================================================================

class MultiModelLLM:
    """LLM wrapper for multi-model pipeline with JSON parsing"""
    
    def __init__(self, token_manager: TokenManager, model_name: str = "gpt-4.1"):
        self.token_manager = token_manager
        self.model_name = model_name
        self.api_url = "https://ai-framework1:8085/api/v1/call_llm"
        
        # Usage tracking
        self.total_calls = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.call_history = []
    
    def call(self, prompt: str, call_name: str = "unknown", temperature: float = 0.2) -> str:
        """Make LLM call with automatic token rotation"""
        
        max_retries = len(self.token_manager.tokens)
        
        for attempt in range(max_retries):
            token = self.token_manager.get_current_token()
            if not token:
                return json.dumps({"error": "All API tokens exhausted"})
            
            try:
                payload = {
                    "llm_model": self.model_name,
                    "messages": [
                        {
                            "content": "You are an expert SR analysis system. Always respond with valid JSON only, no markdown or explanation outside JSON.",
                            "role": "system"
                        },
                        {"content": prompt, "role": "user"}
                    ],
                    "max_tokens": 4000  # Ensure full response for workarounds
                }
                
                headers = {
                    "Content-Type": "application/json",
                    "accept": "application/json",
                    "API-Key": token,
                    "X-Effective-Caller": self.token_manager.get_current_email() or "sr_rag_pipeline@amdocs.com"
                }
                
                response = requests.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                    timeout=300,
                    verify=False
                )
                
                if response.status_code == 429:
                    if self.token_manager.mark_exhausted():
                        continue
                    return json.dumps({"error": "All tokens exhausted"})
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Track usage
                    self.total_calls += 1
                    self.total_input_tokens += data.get('input_tokens', 0)
                    self.total_output_tokens += data.get('output_tokens', 0)
                    self.total_cost += data.get('cost', 0)
                    self.call_history.append({
                        'call_name': call_name,
                        'input_tokens': data.get('input_tokens', 0),
                        'output_tokens': data.get('output_tokens', 0),
                        'cost': data.get('cost', 0)
                    })
                    
                    return data.get('message', '').strip()
                else:
                    print(f"[LLM] Error: {response.status_code}")
                    return json.dumps({"error": f"API error {response.status_code}"})
                    
            except requests.exceptions.Timeout:
                print(f"[LLM] Timeout on {call_name}, retrying...")
                continue
            except Exception as e:
                print(f"[LLM] Error: {e}")
                return json.dumps({"error": str(e)})
        
        return json.dumps({"error": "Failed after all retries"})
    
    def parse_json_response(self, response: str) -> Dict:
        """Parse JSON from LLM response, handling markdown code blocks"""
        try:
            # Try direct parse
            return json.loads(response)
        except json.JSONDecodeError:
            pass
        
        # Try extracting from markdown code block
        json_match = re.search(r'```(?:json)?\s*([\s\S]*?)```', response)
        if json_match:
            try:
                return json.loads(json_match.group(1).strip())
            except json.JSONDecodeError:
                pass
        
        # Try finding JSON object in response
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        return {"error": "Failed to parse JSON", "raw_response": response[:500]}
    
    def get_usage_summary(self) -> Dict:
        return {
            'total_calls': self.total_calls,
            'total_input_tokens': self.total_input_tokens,
            'total_output_tokens': self.total_output_tokens,
            'total_cost': self.total_cost,
            'call_breakdown': self.call_history,
            'tokens_status': self.token_manager.get_status()
        }


# ============================================================================
# VECTORSTORE HANDLER (reused logic)
# ============================================================================

class VectorstoreHandler:
    """Handle all vectorstore queries - ChromaDB only"""
    
    def __init__(self, java_db_path: Path = None, comcast_code_db_path: Path = None, history_db_path: Path = None):
        # ChromaDB path - all vectorstores are now in ChromaDB
        self.chromadb_path = Path(__file__).parent.parent.parent / "data" / "vectorstore" / "chromadb_store"
        
        print("[*] Loading Sentence Transformer model...")
        # Load model with device='cpu' to avoid meta tensor error
        import os
        os.environ['ACCELERATE_TORCH_DEVICE'] = 'cpu'
        self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        print("[OK] Model loaded")
        
        self.preprocessor = SRTextPreprocessor() if PREPROCESSOR_AVAILABLE else None
        
        # Initialize ChromaDB
        self.chromadb_client = None
        self.use_chromadb = False
        self.history_collection = None
        self.java_mapping_collection = None
        self.comcast_code_collection = None
        self._init_chromadb()
    
    def _init_chromadb(self):
        """Initialize ChromaDB client and collections"""
        try:
            import chromadb
            
            if self.chromadb_path.exists():
                # Use basic PersistentClient without Settings to avoid "different settings" error
                self.chromadb_client = chromadb.PersistentClient(path=str(self.chromadb_path))
                collections = [c.name for c in self.chromadb_client.list_collections()]
                
                # Load collections
                if 'clean_history_data' in collections:
                    self.history_collection = self.chromadb_client.get_collection('clean_history_data')
                if 'java_mapping' in collections:
                    self.java_mapping_collection = self.chromadb_client.get_collection('java_mapping')
                if 'comcast_code' in collections:
                    self.comcast_code_collection = self.chromadb_client.get_collection('comcast_code')
                
                self.use_chromadb = True
                print(f"[OK] ChromaDB initialized ({len(collections)} collections)")
                print(f"     - History: {self.history_collection.count() if self.history_collection else 0} records")
                print(f"     - Java Mapping: {self.java_mapping_collection.count() if self.java_mapping_collection else 0} records")
                print(f"     - Code Search: {self.comcast_code_collection.count() if self.comcast_code_collection else 0} records")
            else:
                print(f"[ERROR] ChromaDB not found at {self.chromadb_path}")
        except ImportError:
            print("[ERROR] ChromaDB not installed - pip install chromadb")
        except Exception as e:
            print(f"[ERROR] ChromaDB init error: {e}")
    
    def _load_comcast_code_db(self):
        try:
            print(f"[*] Loading comcast_code.db...")
            self.comcast_code_data = {
                'embeddings': np.load(self.comcast_code_db_path / "embeddings.npy"),
                'documents': pickle.load(open(self.comcast_code_db_path / "documents.pkl", 'rb')),
                'metadatas': pickle.load(open(self.comcast_code_db_path / "metadatas.pkl", 'rb')),
                'config': json.load(open(self.comcast_code_db_path / "config.json", 'r'))
            }
            print(f"[OK] comcast_code.db loaded ({self.comcast_code_data['config']['total_chunks']} chunks)")
        except Exception as e:
            print(f"[WARN] Error loading comcast_code.db: {e}")
    
    def _load_history_db(self):
        try:
            print(f"[*] Loading history_data.db...")
            with open(self.history_db_path, 'rb') as f:
                self.history_data = pickle.load(f)
            print(f"[OK] history_data.db loaded ({self.history_data.get('total_records', 0)} records)")
        except Exception as e:
            print(f"[WARN] Error loading history_data.db: {e}")
    
    def _load_abbreviation_db_legacy(self, abbreviation_db_path):
        """Load abbreviation.db vectorstore (legacy pickle)"""
        try:
            print(f"[*] Loading abbreviation.db (legacy)...")
            with open(abbreviation_db_path, 'rb') as f:
                self.abbreviation_data = pickle.load(f)
            print(f"[OK] abbreviation.db loaded ({self.abbreviation_data.get('total_records', 0)} abbreviations)")
        except Exception as e:
            print(f"[WARN] Error loading abbreviation.db: {e}")
            self.abbreviation_data = None
    
    def search_abbreviations(self, query_text: str, top_k: int = 15) -> str:
        """
        Search abbreviation database for relevant terms in the SR text.
        Uses SQLite database for fast text-based lookup.
        Returns formatted context string for LLM prompt.
        """
        abbreviation_db_path = Path(__file__).parent.parent.parent / "database" / "stores" / "abbreviation.db"
        
        if not abbreviation_db_path.exists():
            return ""
        
        try:
            # Extract potential abbreviations from query (uppercase words 2-6 chars)
            import re
            words = set(re.findall(r'\b[A-Z]{2,6}\b', query_text.upper()))
            
            # Also search for context matches
            search_terms = query_text.lower().split()[:10]
            
            conn = sqlite3.connect(abbreviation_db_path)
            cursor = conn.cursor()
            
            abbreviations = []
            seen = set()
            
            # 1. Direct abbreviation matches
            for word in words:
                cursor.execute("""
                    SELECT short_form, full_form, context FROM abbreviations 
                    WHERE short_form = ? LIMIT 1
                """, (word,))
                row = cursor.fetchone()
                if row and row[0] not in seen:
                    seen.add(row[0])
                    entry = f"{row[0]} = {row[1]}"
                    if row[2]:
                        entry += f" (Context: {row[2][:100]})"
                    abbreviations.append(entry)
            
            # 2. Context/full form relevance search (if room for more)
            if len(abbreviations) < top_k:
                remaining = top_k - len(abbreviations)
                placeholders = " OR ".join(["full_form LIKE ? OR context LIKE ?"] * min(5, len(search_terms)))
                if placeholders:
                    params = []
                    for term in search_terms[:5]:
                        params.extend([f'%{term}%', f'%{term}%'])
                    
                    cursor.execute(f"""
                        SELECT short_form, full_form, context FROM abbreviations 
                        WHERE {placeholders} LIMIT ?
                    """, (*params, remaining))
                    
                    for row in cursor.fetchall():
                        if row[0] not in seen:
                            seen.add(row[0])
                            entry = f"{row[0]} = {row[1]}"
                            if row[2]:
                                entry += f" (Context: {row[2][:100]})"
                            abbreviations.append(entry)
            
            conn.close()
            
            if not abbreviations:
                return ""
            
            # Format as context section
            result = "=== ABBREVIATION REFERENCE ===\n"
            result += "Use these abbreviations when they appear in the SR:\n"
            for abbr in abbreviations[:12]:
                result += f"  - {abbr}\n"
            
            return result
            
        except Exception as e:
            print(f"[WARN] Error searching abbreviations: {e}")
            return ""
    
    def get_java_metadata_context(self, limit: int = 50) -> str:
        """Get Java class metadata - now from ChromaDB java_mapping collection"""
        # Try ChromaDB first
        if self.use_chromadb and self.chromadb_client:
            try:
                collection = self.chromadb_client.get_collection('java_mapping')
                # Get sample of classes
                results = collection.get(limit=limit, include=['metadatas'])
                
                context = "Available Java Classes:\n"
                if results and results['ids']:
                    for i, id_ in enumerate(results['ids']):
                        meta = results['metadatas'][i] if results['metadatas'] else {}
                        class_name = meta.get('class_name', 'Unknown')
                        class_type = meta.get('class_type', '')
                        package = meta.get('package', '')
                        file_path = meta.get('file_path', '')
                        
                        context += f"  - {class_name} ({class_type}) - {package}\n"
                        if file_path:
                            context += f"    Path: {file_path}\n"
                return context
            except Exception as e:
                print(f"[WARN] ChromaDB java_mapping error: {e}")
        
        # Fallback to SQLite if exists
        try:
            conn = sqlite3.connect(self.java_db_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT class_name, package, file_path, class_type, annotations
                FROM java_classes ORDER BY class_name LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            conn.close()
            
            context = "Available Java Classes:\n"
            for row in rows:
                class_name, package, file_path, class_type, annotations = row
                context += f"  - {class_name} ({class_type}) - {package}\n"
                if file_path:
                    context += f"    Path: {file_path}\n"
            return context
        except Exception as e:
            return f"Java metadata not accessible: {e}"
    
    def search_java_mapping_semantically(self, query_text: str, top_k: int = 10) -> List[Dict]:
        """Search Java class mappings semantically using ChromaDB"""
        if self.use_chromadb and self.chromadb_client:
            try:
                collection = self.chromadb_client.get_collection('java_mapping')
                query_embedding = self.semantic_model.encode([query_text])[0].tolist()
                
                results_raw = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    include=["documents", "metadatas", "distances"]
                )
                
                results = []
                if results_raw and results_raw['ids'] and len(results_raw['ids']) > 0:
                    for i, id_ in enumerate(results_raw['ids'][0]):
                        distance = results_raw['distances'][0][i] if results_raw['distances'] else 1.0
                        similarity = 1 - distance
                        if similarity < 0.4:
                            continue
                        results.append({
                            'similarity': similarity,
                            'class_name': results_raw['metadatas'][0][i].get('class_name', '') if results_raw['metadatas'] else '',
                            'package': results_raw['metadatas'][0][i].get('package', '') if results_raw['metadatas'] else '',
                            'class_type': results_raw['metadatas'][0][i].get('class_type', '') if results_raw['metadatas'] else '',
                            'file_path': results_raw['metadatas'][0][i].get('file_path', '') if results_raw['metadatas'] else '',
                            'fqn': results_raw['metadatas'][0][i].get('full_qualified_name', '') if results_raw['metadatas'] else ''
                        })
                return results
            except Exception as e:
                print(f"[WARN] ChromaDB java_mapping search error: {e}")
        return []
    
    def search_java_classes_fuzzy(self, keywords: List[str], max_results: int = 100) -> List[str]:
        """
        Fuzzy search Java class names using keywords.
        Searches ChromaDB java_mapping collection using substring matching on class names.
        
        Args:
            keywords: List of keywords to search for (e.g., ["decompose", "XYZ", "validate"])
            max_results: Maximum number of class names to return
            
        Returns:
            List of matching class names from the database
        """
        if not keywords:
            return []
        
        matching_classes = set()
        
        # Method 1: Use ChromaDB metadata filtering if available
        if self.use_chromadb and self.chromadb_client:
            try:
                collection = self.chromadb_client.get_collection('java_mapping')
                
                # Get all class metadata (ChromaDB doesn't support LIKE queries, so we fetch and filter)
                # For efficiency, we use semantic search with each keyword
                for keyword in keywords[:10]:  # Limit keywords to prevent too many queries
                    if len(keyword) < 3:
                        continue
                    
                    # Semantic search for classes related to this keyword
                    query_embedding = self.semantic_model.encode([keyword])[0].tolist()
                    results_raw = collection.query(
                        query_embeddings=[query_embedding],
                        n_results=30,
                        include=["metadatas"]
                    )
                    
                    if results_raw and results_raw['metadatas'] and len(results_raw['metadatas']) > 0:
                        for metadata in results_raw['metadatas'][0]:
                            class_name = metadata.get('class_name', '')
                            if class_name:
                                # Also do substring check for better matching
                                if keyword.lower() in class_name.lower():
                                    matching_classes.add(class_name)
                                else:
                                    # Still add if semantic match found
                                    matching_classes.add(class_name)
                
                print(f"   [FUZZY] Found {len(matching_classes)} matching classes from {len(keywords)} keywords")
                return list(matching_classes)[:max_results]
                
            except Exception as e:
                print(f"[WARN] ChromaDB fuzzy search error: {e}")
        
        # Method 2: Fallback to SQLite javaMapping.db if ChromaDB not available
        sqlite_db_path = Path(__file__).parent.parent.parent / "data" / "backup" / "javaMapping.db"
        if sqlite_db_path.exists():
            try:
                conn = sqlite3.connect(str(sqlite_db_path))
                cursor = conn.cursor()
                
                for keyword in keywords[:15]:
                    if len(keyword) < 3:
                        continue
                    # Fuzzy substring search
                    cursor.execute(
                        "SELECT DISTINCT class_name FROM java_classes WHERE class_name LIKE ? LIMIT 30",
                        (f'%{keyword}%',)
                    )
                    for row in cursor.fetchall():
                        if row[0]:
                            matching_classes.add(row[0])
                
                conn.close()
                print(f"   [FUZZY-SQLite] Found {len(matching_classes)} matching classes")
                return list(matching_classes)[:max_results]
                
            except Exception as e:
                print(f"[WARN] SQLite fuzzy search error: {e}")
        
        return list(matching_classes)[:max_results]
    
    def get_all_class_names_sample(self, sample_size: int = 200) -> List[str]:
        """
        Get a sample of class names from the database for LLM context.
        Useful when no specific keywords are available.
        """
        class_names = []
        
        if self.use_chromadb and self.chromadb_client:
            try:
                collection = self.chromadb_client.get_collection('java_mapping')
                # Get random sample using a generic query
                results = collection.get(
                    limit=sample_size,
                    include=["metadatas"]
                )
                if results and results['metadatas']:
                    for metadata in results['metadatas']:
                        class_name = metadata.get('class_name', '')
                        if class_name:
                            class_names.append(class_name)
            except Exception as e:
                print(f"[WARN] Error getting class names sample: {e}")
        
        return class_names
    
    def search_java_code_semantically(self, query_text: str, top_k: int = 5) -> List[Dict]:
        # Use ChromaDB if available
        if self.use_chromadb and self.chromadb_client:
            try:
                collection = self.chromadb_client.get_collection('comcast_code')
                query_embedding = self.semantic_model.encode([query_text])[0].tolist()
                
                results_raw = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    include=["documents", "metadatas", "distances"]
                )
                
                results = []
                if results_raw and results_raw['ids'] and len(results_raw['ids']) > 0:
                    for i, id_ in enumerate(results_raw['ids'][0]):
                        distance = results_raw['distances'][0][i] if results_raw['distances'] else 1.0
                        similarity = 1 - distance
                        if similarity < 0.45:
                            continue
                        results.append({
                            'similarity': similarity,
                            'code': results_raw['documents'][0][i] if results_raw['documents'] else '',
                            'metadata': results_raw['metadatas'][0][i] if results_raw['metadatas'] else {}
                        })
                return results
                
            except Exception as e:
                print(f"[WARN] ChromaDB code search error: {e}")
        
        # Fallback if no data loaded
        if not self.comcast_code_data:
            return []
        
        try:
            query_embedding = self.semantic_model.encode([query_text])[0]
            similarities = cosine_similarity([query_embedding], self.comcast_code_data['embeddings'])[0]
            top_indices = similarities.argsort()[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                similarity = float(similarities[idx])
                if similarity < 0.45:
                    continue
                results.append({
                    'similarity': similarity,
                    'code': self.comcast_code_data['documents'][idx],
                    'metadata': self.comcast_code_data['metadatas'][idx]
                })
            return results
        except Exception as e:
            print(f"[WARN] Java code search error: {e}")
            return []
    
    def search_historical_srs(self, query_text: str, top_k: int = 10, timeout: int = 15) -> List[Dict]:
        # Use ChromaDB if available
        if self.use_chromadb and self.chromadb_client:
            try:
                collection = self.chromadb_client.get_collection('clean_history_data')
                
                # Preprocess query if available
                search_query = query_text
                if self.preprocessor:
                    search_query = self.preprocessor.clean_for_semantic_search(query_text)
                
                query_embedding = self.semantic_model.encode([search_query])[0].tolist()
                
                results_raw = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    include=["documents", "metadatas", "distances"]
                )
                
                results = []
                if results_raw and results_raw['ids'] and len(results_raw['ids']) > 0:
                    for i, id_ in enumerate(results_raw['ids'][0]):
                        distance = results_raw['distances'][0][i] if results_raw['distances'] else 1.0
                        similarity = 1 - distance
                        if similarity < 0.55:
                            continue
                        
                        meta = results_raw['metadatas'][0][i] if results_raw['metadatas'] else {}
                        
                        # Build workaround text
                        workaround_parts = []
                        if meta.get('workaround'):
                            workaround_parts.append(f"Workaround: {meta['workaround']}")
                        if meta.get('ai_generated_workaround') and meta.get('ai_generated_workaround') != 'NA':
                            workaround_parts.append(f"AI Generated: {meta['ai_generated_workaround']}")
                        if meta.get('user_corrected_workaround'):
                            workaround_parts.append(f"User Corrected: {meta['user_corrected_workaround']}")
                        
                        results.append({
                            'similarity': similarity,
                            'sr_id': meta.get('call_id', 'Unknown'),
                            'description': meta.get('description', ''),
                            # 'summary' removed - was redundant
                            'resolution_category': meta.get('resolution_categorization', meta.get('sla_resolution_category', '')),
                            'workaround': '\n'.join(workaround_parts) if workaround_parts else '',
                            'metadata': meta
                        })
                
                # DEBUG: Log search results
                raw_count = len(results_raw['ids'][0]) if results_raw and results_raw['ids'] else 0
                print(f"   [DEBUG] ChromaDB raw results: {raw_count}")
                print(f"   [DEBUG] After 0.55 threshold filter: {len(results)} matches")
                if results:
                    print(f"   [DEBUG] Top match similarity: {results[0]['similarity']:.1%}")
                    wa_preview = results[0]['workaround'][:100].replace('\n', ' ')
                    print(f"   [DEBUG] Top match workaround: {wa_preview}...")
                
                return results
                
            except Exception as e:
                print(f"[WARN] ChromaDB historical search error: {e}")
        
        # Fallback to legacy pickle
        if not self.history_data:
            return []
        
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
                future = executor.submit(self._perform_semantic_search, query_text, top_k)
                return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            print(f"[TIMEOUT] Semantic search exceeded {timeout}s")
            return []
        except Exception as e:
            print(f"[WARN] Historical search error: {e}")
            return []
    
    def _perform_semantic_search(self, query_text: str, top_k: int = 10) -> List[Dict]:
        try:
            if self.history_data.get('preprocessed', False) and self.preprocessor:
                query_text = self.preprocessor.clean_for_semantic_search(query_text)
            
            query_embedding = self.semantic_model.encode([query_text])[0]
            similarities = cosine_similarity([query_embedding], self.history_data['embeddings'])[0]
            top_indices = similarities.argsort()[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                similarity = float(similarities[idx])
                if similarity < 0.30:  # Lower threshold to get more candidates for LLM
                    continue
                
                metadata = self.history_data['metadata'][idx]
                
                # Build workaround text from available fields
                workaround_parts = []
                if metadata.get('workaround'):
                    workaround_parts.append(f"Workaround: {metadata['workaround']}")
                if metadata.get('ai_generated_workaround') and str(metadata['ai_generated_workaround']).lower() not in ['na', 'nan', 'none', '']:
                    workaround_parts.append(f"AI Generated: {metadata['ai_generated_workaround']}")
                if metadata.get('user_corrected_workaround') and str(metadata['user_corrected_workaround']).lower() not in ['na', 'nan', 'none', '']:
                    workaround_parts.append(f"User Corrected: {metadata['user_corrected_workaround']}")
                
                results.append({
                    'similarity': similarity,
                    'sr_id': metadata.get('call_id', 'Unknown'),
                    'workaround': "\n".join(workaround_parts) if workaround_parts else "Not available",
                    'resolution_category': metadata.get('resolution_categorization', 'Unknown'),
                    'status_reason': metadata.get('status_reason', 'Unknown'),
                    'description': metadata.get('description', '')[:300]
                })
            
            return results
        except Exception as e:
            print(f"[WARN] Semantic search error: {e}")
            return []


# ============================================================================
# MULTI-MODEL PIPELINE
# ============================================================================

class MultiModelSRPipeline:
    """Multi-model SR Analysis Pipeline with 5 LLM Calls"""
    
    def __init__(self, tokens_file: Path = None, model_name: str = "gpt-4.1"):
        self.base_dir = Path(__file__).parent.parent
        self.input_dir = self.base_dir / "input"
        self.output_dir = self.base_dir / "llm output"
        
        if tokens_file is None:
            # Tokens are now in tokens/ folder
            tokens_file = Path(__file__).parent.parent.parent / "tokens" / "Tokens.xlsx"
        
        # ChromaDB path - all vectorstores now in ChromaDB
        self.chromadb_path = Path(__file__).parent.parent.parent / "data" / "vectorstore" / "chromadb_store"
        
        # Initialize components
        print(f"\n{'='*60}")
        print("Multi-Model SR Analysis Pipeline (ChatGPT)")
        print(f"{'='*60}")
        
        self.token_manager = TokenManager(tokens_file)
        self.llm = MultiModelLLM(self.token_manager, model_name)
        self.vectorstore = VectorstoreHandler()  # Uses ChromaDB internally
        
        # Activity finder
        self.activity_finder = None
        if ACTIVITY_FINDER_AVAILABLE:
            try:
                self.activity_finder = ActivityFinder()
                print("[OK] ActivityFinder connected")
            except Exception as e:
                print(f"[WARN] ActivityFinder not available: {e}")
        
        # Garbage workaround patterns
        self.garbage_patterns = [
            r'^n/?a$', r'^na$', r'^none$', r'^null$', r'^-$', r'^\.$',
            r'^not\s*(available|applicable)$', r'^escalated$', r'^closed$',
            r'^no\s*action', r'^resolved$', r'^fixed$'
        ]
        
        self.results = []
        
        # 🆕 LLM CALL 5: Daily load tracking for skill-based assignment
        self.daily_loads = {}  # Track daily assignments: {name: count}
        self.daily_date = None
        
        # Create directories
        self.input_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"[OK] Pipeline initialized (5 LLM Calls)")
        print(f"{'='*60}\n")
    
    def _is_garbage_workaround(self, text: str) -> bool:
        """Check if workaround is garbage/useless"""
        if not text or len(text.strip()) < 15:
            return True
        
        text_lower = text.strip().lower()
        for pattern in self.garbage_patterns:
            if re.match(pattern, text_lower, re.IGNORECASE):
                return True
        
        return False
    
    def _filter_workarounds(self, historical_matches: List[Dict]) -> List[Dict]:
        """Filter out garbage workarounds"""
        valid = []
        garbage_count = 0
        for match in historical_matches:
            workaround = match.get('workaround', '')
            if not self._is_garbage_workaround(workaround):
                valid.append(match)
            else:
                garbage_count += 1
                wa_preview = workaround[:50].replace('\n', ' ') if workaround else '(empty)'
                print(f"   [DEBUG] Garbage filtered: '{wa_preview}'")
        print(f"   [DEBUG] Filtered {garbage_count} garbage workarounds out of {len(historical_matches)}")
        return valid
    
    # ========================================================================
    # LLM CALL 1: Find Semantic Workaround
    # ========================================================================
    
    def _llm_find_workaround(self, sr_data: Dict, historical_matches: List[Dict]) -> str:
        """LLM CALL 1: Find best semantic workaround from history"""
        print("   [LLM 1] Finding semantic workaround...")
        
        # Build historical matches context
        hist_context = ""
        for i, match in enumerate(historical_matches[:10], 1):
            hist_context += f"\n--- Historical SR #{i} (Similarity: {match['similarity']:.1%}) ---\n"
            hist_context += f"SR ID: {match['sr_id']}\n"
            hist_context += f"Category: {match['resolution_category']}\n"
            hist_context += f"Workaround:\n{match['workaround'][:800]}\n"
        
        # DEBUG: Log context being sent to LLM
        print(f"   [DEBUG] hist_context length: {len(hist_context)} chars")
        print(f"   [DEBUG] Number of matches passed to LLM: {len(historical_matches)}")
        if not hist_context.strip():
            print("   [DEBUG] ⚠️ EMPTY CONTEXT - LLM will likely return NO_MATCH!")
        
        prompt = PROMPT_FIND_SEMANTIC_WORKAROUND.format(
            sr_id=sr_data.get('SR ID', 'Unknown'),
            description=sr_data.get('Description', '')[:1500],
            notes=sr_data.get('Notes', '')[:1500],
            resolution_category=sr_data.get('Resolution Category', 'Unknown'),
            historical_matches=hist_context if hist_context else "No historical matches available."
        )
        
        response = self.llm.call(prompt, call_name="find_workaround", temperature=0.1)
        result = self.llm.parse_json_response(response)
        
        if result.get('semantic_workaround') and result['semantic_workaround'] != "NO_MATCH":
            print(f"   [LLM 1] ✅ Found workaround (quality: {result.get('quality_score', 'N/A')})")
            return result['semantic_workaround']
        else:
            print("   [LLM 1] ⚠️ No suitable workaround found")
            return ""
    
    # ========================================================================
    # LLM CALL 2: Java Detection with Voting
    # ========================================================================
    
    def _llm_detect_java_with_voting(self, sr_data: Dict, semantic_workaround: str, 
                                      historical_matches: List[Dict]) -> Dict:
        """LLM CALL 2: Detect Java error using 5-source voting"""
        print("   [LLM 2] Running Java detection with 5-source voting...")
        
        # Build context for each source
        similar_categories = "\n".join([
            f"  • SR {m['sr_id']}: {m['resolution_category']}" 
            for m in historical_matches[:5]
        ]) or "No similar SR categories available"
        
        ai_workarounds = ""
        user_workarounds = ""
        for match in historical_matches[:5]:
            wa = match.get('workaround', '')
            if 'AI Generated:' in wa:
                ai_workarounds += f"\n--- SR {match['sr_id']} ---\n{wa[:500]}\n"
            if 'Workaround:' in wa or 'User Corrected:' in wa:
                user_workarounds += f"\n--- SR {match['sr_id']} ---\n{wa[:500]}\n"
        
        prompt = PROMPT_JAVA_DETECTION_VOTING.format(
            sr_id=sr_data.get('SR ID', 'Unknown'),
            priority=sr_data.get('Priority', sr_data.get('Customer Priority', 'Medium')),
            description=sr_data.get('Description', '')[:2000],
            notes=sr_data.get('Notes', '')[:2000],
            resolution_category=sr_data.get('Resolution Category', 'Unknown'),
            similar_categories=similar_categories,
            semantic_workaround=semantic_workaround[:2000] if semantic_workaround else "Not available",
            ai_workarounds=ai_workarounds[:2000] if ai_workarounds else "No AI workarounds in similar SRs",
            user_workarounds=user_workarounds[:2000] if user_workarounds else "No user workarounds in similar SRs"
        )
        
        response = self.llm.call(prompt, call_name="java_detection", temperature=0.1)
        result = self.llm.parse_json_response(response)
        
        # Default result if parsing fails
        if 'error' in result:
            print(f"   [LLM 2] ⚠️ Parse error, defaulting to non-Java")
            return {
                'is_java_error': False,
                'confidence': 'VERY_LOW',
                'java_votes': 0,
                'non_java_votes': 0,
                'unknown_votes': 5,
                'evidence': [],
                'issue_type': 'Unknown',
                'votes': {}
            }
        
        is_java = result.get('is_java_error', False)
        confidence = result.get('confidence', 'LOW')
        print(f"   [LLM 2] {'✅ Java Error' if is_java else '❌ Not Java'} (Confidence: {confidence})")
        print(f"   [LLM 2] Votes: {result.get('java_votes', 0)} Java, {result.get('non_java_votes', 0)} Non-Java, {result.get('unknown_votes', 0)} Unknown")
        
        return result
    
    # ========================================================================
    # LLM CALL 3: Extract Activity Names with Retry
    # ========================================================================
    
    def _llm_extract_activity_keywords(self, sr_data: Dict) -> Tuple[List[str], List[str]]:
        """
        LLM CALL 3a: Extract keywords from SR for fuzzy class name search.
        Returns: (keywords, explicit_class_names)
        """
        print("   [LLM 3a] Extracting activity keywords...")
        
        prompt = PROMPT_EXTRACT_ACTIVITY_KEYWORDS.format(
            description=sr_data.get('Description', '')[:2000],
            notes=sr_data.get('Notes', '')[:2000]
        )
        
        response = self.llm.call(prompt, call_name="extract_keywords", temperature=0.1)
        result = self.llm.parse_json_response(response)
        
        keywords = result.get('keywords', [])
        explicit_names = result.get('explicit_class_names', [])
        
        # Ensure we have lists
        if not isinstance(keywords, list):
            keywords = []
        if not isinstance(explicit_names, list):
            explicit_names = []
        
        print(f"   [LLM 3a] Found {len(keywords)} keywords, {len(explicit_names)} explicit class names")
        return keywords, explicit_names
    
    def _llm_extract_activities(self, sr_data: Dict, semantic_workaround: str,
                                 historical_matches: List[Dict], retry_context: str = "",
                                 available_classes: List[str] = None) -> List[Dict]:
        """
        LLM CALL 3b: Extract activity names from AVAILABLE classes list.
        Now uses two-step approach: keywords → fuzzy search → selection from real classes.
        """
        
        # Get Java code context
        query = f"{sr_data.get('Description', '')} {sr_data.get('Notes', '')}"
        java_code_matches = self.vectorstore.search_java_code_semantically(query, top_k=5)
        
        java_code_context = ""
        for i, match in enumerate(java_code_matches, 1):
            meta = match.get('metadata', {})
            java_code_context += f"\n--- Code Match #{i} ({match['similarity']:.1%}) ---\n"
            java_code_context += f"File: {meta.get('file_path', 'Unknown')}\n"
            java_code_context += f"Code:\n{match['code'][:600]}\n"
        
        # Historical workarounds
        hist_workarounds = ""
        for match in historical_matches[:3]:
            hist_workarounds += f"\n--- SR {match['sr_id']} ({match['similarity']:.1%}) ---\n"
            hist_workarounds += f"{match['workaround'][:500]}\n"
        
        # Format available classes for prompt
        if available_classes:
            available_classes_str = "\n".join([f"  - {name}" for name in available_classes[:100]])
        else:
            available_classes_str = "(No specific classes found - extract based on patterns)"
        
        prompt = PROMPT_EXTRACT_ACTIVITIES.format(
            description=sr_data.get('Description', '')[:2000],
            notes=sr_data.get('Notes', '')[:2000],
            semantic_workaround=semantic_workaround[:1500] if semantic_workaround else "Not available",
            historical_workarounds=hist_workarounds if hist_workarounds else "No historical workarounds available",
            available_class_names=available_classes_str,
            java_code_context=java_code_context if java_code_context else "No Java code context available",
            retry_context=retry_context
        )
        
        response = self.llm.call(prompt, call_name="extract_activities", temperature=0.1)
        result = self.llm.parse_json_response(response)
        
        activities = result.get('activity_names', [])
        if isinstance(activities, list):
            return activities
        return []
    
    def _extract_and_validate_activities(self, sr_data: Dict, semantic_workaround: str,
                                          historical_matches: List[Dict], max_retries: int = 2) -> List[Dict]:
        """
        Extract activities using two-step approach with javaMapping.db context.
        
        Flow:
        1. LLM Call 3a: Extract keywords from SR
        2. Fuzzy search javaMapping.db with those keywords
        3. LLM Call 3b: Select from available classes
        4. Validate selected classes against activity_finder
        5. Retry with failed activities if needed
        """
        print("   [LLM 3] Extracting activity names (two-step approach)...")
        
        # ====================================================================
        # STEP 1: Extract keywords from SR (LLM Call 3a)
        # ====================================================================
        keywords, explicit_names = self._llm_extract_activity_keywords(sr_data)
        
        # ====================================================================
        # STEP 2: Fuzzy search javaMapping.db with keywords
        # ====================================================================
        all_keywords = keywords + explicit_names
        if all_keywords:
            available_classes = self.vectorstore.search_java_classes_fuzzy(all_keywords, max_results=100)
            print(f"   [FUZZY] Found {len(available_classes)} matching classes from javaMapping.db")
        else:
            # Fallback: get sample of class names
            available_classes = self.vectorstore.get_all_class_names_sample(sample_size=50)
            print(f"   [FUZZY] No keywords, using {len(available_classes)} sample classes")
        
        # ====================================================================
        # STEP 3: LLM Call 3b - Select from available classes
        # ====================================================================
        validated = []
        retry_count = 0
        retry_context = ""
        
        while retry_count <= max_retries:
            # Call LLM with available classes context
            activities = self._llm_extract_activities(
                sr_data, semantic_workaround, 
                historical_matches, retry_context,
                available_classes=available_classes
            )
            
            if not activities:
                print(f"   [LLM 3b] No activities found")
                break
            
            print(f"   [LLM 3b] Found {len(activities)} activity candidates")
            
            # ====================================================================
            # STEP 4: Validate each against activity_finder database
            # ====================================================================
            failed_activities = []
            for activity in activities:
                name = activity.get('name', '') if isinstance(activity, dict) else str(activity)
                
                if not name:
                    continue
                
                if self.activity_finder:
                    result = self.activity_finder.find_activity_implementation(name)
                    
                    if result.get('success'):
                        print(f"   [VALIDATE] ✅ {name} → {result['class_name']}")
                        validated.append({
                            'activity_name': name,
                            'impl_class': result.get('class_name'),
                            'impl_path': result.get('impl_path'),
                            'class_path': result.get('class_path'),
                            'profile_name': result.get('profile_name', 'Unknown')
                        })
                    else:
                        print(f"   [VALIDATE] ❌ {name} not found in activity_finder DB")
                        failed_activities.append(name)
                else:
                    # No activity finder, accept if class exists in our fuzzy search results
                    if name in available_classes or f"{name}Impl" in available_classes:
                        print(f"   [VALIDATE] ✅ {name} (in javaMapping.db)")
                        validated.append({
                            'activity_name': name,
                            'impl_class': f"{name}Impl" if not name.endswith('Impl') else name,
                            'impl_path': f"customization/src/main/java/.../{name}.java",
                            'class_path': f"com.amdocs.{name.lower()}.{name}"
                        })
                    else:
                        print(f"   [VALIDATE] ❌ {name} not in available classes")
                        failed_activities.append(name)
            
            # If all validated or no retries left, break
            if not failed_activities or retry_count >= max_retries:
                break
            
            # ====================================================================
            # STEP 5: Retry with failed activities
            # ====================================================================
            retry_context = PROMPT_RETRY_ACTIVITIES.format(
                failed_activities=", ".join(failed_activities)
            )
            retry_count += 1
            print(f"   [LLM 3b] Retrying with {len(failed_activities)} failed activities (attempt {retry_count}/{max_retries})")
        
        print(f"   [LLM 3] ✅ Final validated: {len(validated)} activities")
        return validated
    
    # ========================================================================
    # LLM CALL 4a: Java Resolution
    # ========================================================================
    
    def _llm_java_resolution(self, sr_data: Dict, java_result: Dict, 
                             validated_activities: List[Dict], semantic_workaround: str,
                             historical_matches: List[Dict]) -> str:
        """LLM CALL 4a: Generate Java-specific resolution"""
        print("   [LLM 4a] Generating Java resolution...")
        
        # Build activities context
        activities_context = ""
        impl_classes_context = ""
        for act in validated_activities:
            activities_context += f"  • {act['activity_name']} (confidence: validated)\n"
            impl_classes_context += f"  • Class: {act.get('impl_class', 'Unknown')}\n"
            impl_classes_context += f"    Path: {act.get('impl_path', 'Unknown')}\n"
        
        if not activities_context:
            activities_context = "No validated activities found"
            impl_classes_context = "No implementation classes found"
        
        # Get Java code for validated activities
        java_code_context = ""
        for act in validated_activities[:3]:
            impl_class = act.get('impl_class', act['activity_name'])
            code_matches = self.vectorstore.search_java_code_semantically(impl_class, top_k=2)
            for match in code_matches:
                meta = match.get('metadata', {})
                java_code_context += f"\n--- {impl_class} ({match['similarity']:.1%}) ---\n"
                java_code_context += f"File: {meta.get('file_path', 'Unknown')}\n"
                java_code_context += f"Code:\n{match['code'][:800]}\n"
        
        if not java_code_context:
            java_code_context = "No Java code found for validated activities"
        
        # Java metadata
        java_metadata = self.vectorstore.get_java_metadata_context(limit=30)
        
        # Historical patterns
        hist_patterns = ""
        for match in historical_matches[:3]:
            hist_patterns += f"\n--- SR {match['sr_id']} ({match['similarity']:.1%}) ---\n"
            hist_patterns += f"Category: {match['resolution_category']}\n"
            hist_patterns += f"Workaround:\n{match['workaround'][:600]}\n"
        
        # Get abbreviation context before LLM call
        sr_text = f"{sr_data.get('Description', '')} {sr_data.get('Notes', '')}"
        abbreviation_context = self.vectorstore.search_abbreviations(sr_text, top_k=15)
        
        prompt = PROMPT_JAVA_RESOLUTION.format(
            sr_id=sr_data.get('SR ID', 'Unknown'),
            priority=sr_data.get('Priority', sr_data.get('Customer Priority', 'Medium')),
            description=sr_data.get('Description', '')[:2000],
            notes=sr_data.get('Notes', '')[:2000],
            detection_confidence=java_result.get('confidence', 'Unknown'),
            java_votes=java_result.get('java_votes', 0),
            non_java_votes=java_result.get('non_java_votes', 0),
            unknown_votes=java_result.get('unknown_votes', 0),
            detection_evidence="\n".join(java_result.get('evidence', [])[:5]),
            activities_with_details=activities_context,
            impl_classes=impl_classes_context,
            java_code_snippets=java_code_context[:3000],
            java_metadata=java_metadata[:2000],
            semantic_workaround=semantic_workaround[:1500] if semantic_workaround else "Not available",
            historical_patterns=hist_patterns[:2000] if hist_patterns else "No historical patterns available",
            abbreviation_context=abbreviation_context
        )
        
        response = self.llm.call(prompt, call_name="java_resolution", temperature=0.2)
        print("   [LLM 4a] ✅ Java resolution generated")
        return response
    
    # ========================================================================
    # LLM CALL 4b: General Resolution
    # ========================================================================
    
    def _llm_general_resolution(self, sr_data: Dict, java_result: Dict,
                                semantic_workaround: str, historical_matches: List[Dict]) -> str:
        """LLM CALL 4b: Generate general (non-Java) resolution"""
        print("   [LLM 4b] Generating general resolution...")
        
        # Historical solutions
        hist_solutions = ""
        for match in historical_matches[:5]:
            hist_solutions += f"\n--- SR {match['sr_id']} ({match['similarity']:.1%}) ---\n"
            hist_solutions += f"Category: {match['resolution_category']}\n"
            hist_solutions += f"Status Reason: {match.get('status_reason', 'Unknown')}\n"
            hist_solutions += f"Workaround:\n{match['workaround'][:600]}\n"
        
        # Get abbreviation context before LLM call
        sr_text = f"{sr_data.get('Description', '')} {sr_data.get('Notes', '')}"
        abbreviation_context = self.vectorstore.search_abbreviations(sr_text, top_k=15)
        
        prompt = PROMPT_GENERAL_RESOLUTION.format(
            sr_id=sr_data.get('SR ID', 'Unknown'),
            priority=sr_data.get('Priority', sr_data.get('Customer Priority', 'Medium')),
            resolution_category=sr_data.get('Resolution Category', 'Unknown'),
            status_reason=sr_data.get('Status Reason', 'Unknown'),
            description=sr_data.get('Description', '')[:2000],
            notes=sr_data.get('Notes', '')[:2000],
            issue_type=java_result.get('issue_type', 'Unknown'),
            confidence=java_result.get('confidence', 'Unknown'),
            java_votes=java_result.get('java_votes', 0),
            non_java_votes=java_result.get('non_java_votes', 0),
            unknown_votes=java_result.get('unknown_votes', 0),
            semantic_workaround=semantic_workaround[:2000] if semantic_workaround else "Not available",
            historical_solutions=hist_solutions[:3000] if hist_solutions else "No historical solutions available",
            abbreviation_context=abbreviation_context
        )
        
        response = self.llm.call(prompt, call_name="general_resolution", temperature=0.2)
        print("   [LLM 4b] ✅ General resolution generated")
        return response
    
    # ========================================================================
    # LLM CALL 5: Skill-Based Assignment
    # ========================================================================
    
    def _reset_daily_loads_if_needed(self):
        """Reset daily load tracking if date changed and load actual counts from ChromaDB"""
        from datetime import date, datetime
        today = date.today()
        if self.daily_date != today:
            self.daily_loads = {}
            self.daily_date = today
            print(f"   [LLM 5] Daily loads reset for {today}")
            
            # 🆕 Load ACTUAL daily loads from ChromaDB
            try:
                import chromadb
                if self.chromadb_path.exists():
                    client = chromadb.PersistentClient(path=str(self.chromadb_path))
                    collection = client.get_collection('clean_history_data')
                    today_str = datetime.now().strftime('%Y-%m-%d')
                    all_records = collection.get(include=['metadatas'])
                    for metadata in all_records.get('metadatas', []):
                        if metadata:
                            sr_date = metadata.get('added_date', '') or metadata.get('opened_date', '')
                            if today_str in str(sr_date):
                                assigned_to = metadata.get('assigned_to', '')
                                if assigned_to:
                                    # Normalize name (handle underscores vs spaces)
                                    normalized_name = assigned_to.replace('_', ' ')
                                    self.daily_loads[normalized_name] = self.daily_loads.get(normalized_name, 0) + 1
                    if self.daily_loads:
                        print(f"   [LLM 5] Loaded actual loads from ChromaDB: {dict(sorted(self.daily_loads.items(), key=lambda x: -x[1]))}")
            except Exception as e:
                print(f"   [LLM 5] Could not load loads from ChromaDB: {e}")
    
    def _get_team_members_context(self) -> str:
        """Get all team members with skills, load, and availability from people_skills.db"""
        db_path = Path(__file__).parent.parent.parent / 'data' / 'database' / 'people_skills.db'
        
        if not db_path.exists():
            return "No team members database found."
        
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        context = ""
        
        try:
            cursor.execute("""
                SELECT 
                    tm.name,
                    tm.status,
                    s.application,
                    s.skill_level,
                    s.max_load,
                    s.min_load,
                    s.specializations,
                    COALESCE(ah.availability_percent, 100) as availability
                FROM team_members tm
                LEFT JOIN skills s ON tm.id = s.member_id
                LEFT JOIN (
                    SELECT member_id, availability_percent
                    FROM availability_history
                    WHERE (end_date IS NULL OR end_date >= datetime('now'))
                    GROUP BY member_id
                    HAVING id = MAX(id)
                ) ah ON tm.id = ah.member_id
                WHERE tm.status = 'active'
                ORDER BY tm.name, s.application
            """)
            
            rows = cursor.fetchall()
            
            # Group by member
            members = {}
            for row in rows:
                name = row[0]
                if name not in members:
                    members[name] = {
                        'availability': row[7] if row[7] is not None else 100,
                        'skills': []
                    }
                if row[2]:  # Has application skill
                    members[name]['skills'].append({
                        'application': row[2],
                        'skill_level': row[3] or 3.0,
                        'max_load': row[4] or 10,
                        'specializations': row[6] or ''
                    })
            
            # Format context
            for name, data in members.items():
                availability = data['availability']
                current_load = self.daily_loads.get(name, 0)
                
                context += f"\n--- {name} ---\n"
                context += f"Availability: {availability}%\n"
                context += f"Current Load Today: {current_load} SRs\n"
                
                if availability == 0:
                    context += "⛔ UNAVAILABLE - DO NOT ASSIGN\n"
                    continue
                
                for skill in data['skills']:
                    max_load = skill['max_load']
                    effective_load = int(max_load * (availability / 100))
                    context += f"  • {skill['application']}: Skill {skill['skill_level']}/5, "
                    context += f"Max Load: {effective_load} (base: {max_load})\n"
                    if skill['specializations']:
                        context += f"    Specializations: {skill['specializations']}\n"
            
        except Exception as e:
            context = f"Error loading team data: {e}"
        finally:
            conn.close()
        
        return context if context else "No team members found in database."
    
    def _get_workload_status(self) -> str:
        """Get current workload status for all members"""
        self._reset_daily_loads_if_needed()
        
        if not self.daily_loads:
            return "No SRs assigned yet today. Everyone has 0 current load."
        
        status = "Current assignments today:\n"
        for name, count in sorted(self.daily_loads.items(), key=lambda x: -x[1]):
            status += f"  • {name}: {count} SRs assigned\n"
        
        return status
    
    def _calculate_complexity(self, sr_data: Dict, is_java_error: bool) -> float:
        """Calculate complexity score (0-10) based on SR data"""
        score = 5.0  # Base
        
        priority = sr_data.get('Priority', sr_data.get('Customer Priority', 'P3'))
        if priority == 'P1':
            score += 2.5
        elif priority == 'P2':
            score += 1.5
        elif priority == 'P4':
            score -= 1.0
        
        if is_java_error:
            score += 1.5
        
        desc = sr_data.get('Description', '')
        if len(desc) > 1000:
            score += 1.0
        elif len(desc) < 200:
            score -= 0.5
        
        return min(max(score, 1.0), 10.0)
    
    def _validate_assignment_name(self, name: str) -> bool:
        """Check if name exists in database (with underscore/space normalization)"""
        db_path = Path(__file__).parent.parent.parent / 'data' / 'database' / 'people_skills.db'
        try:
            # Normalize: replace underscores with spaces
            normalized_name = name.replace('_', ' ').strip()
            
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            
            # Try exact match first
            cursor.execute("SELECT name FROM team_members WHERE name = ? AND status = 'active'", (normalized_name,))
            result = cursor.fetchone()
            
            if result:
                conn.close()
                return True
            
            # Try case-insensitive match as fallback
            cursor.execute("SELECT name FROM team_members WHERE LOWER(name) = LOWER(?) AND status = 'active'", (normalized_name,))
            result = cursor.fetchone()
            conn.close()
            
            return result is not None
        except:
            return False
    
    def _fallback_assignment(self) -> str:
        """Fallback: Get person with lowest load"""
        db_path = Path(__file__).parent.parent.parent / 'data' / 'database' / 'people_skills.db'
        try:
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("""
                SELECT tm.name
                FROM team_members tm
                LEFT JOIN (
                    SELECT member_id, availability_percent
                    FROM availability_history
                    WHERE (end_date IS NULL OR end_date >= datetime('now'))
                    GROUP BY member_id
                    HAVING id = MAX(id)
                ) ah ON tm.id = ah.member_id
                WHERE tm.status = 'active'
                AND COALESCE(ah.availability_percent, 100) > 0
                ORDER BY tm.name
            """)
            members = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            if not members:
                return "Not Assigned"
            
            # Find member with lowest daily load
            member_loads = [(m, self.daily_loads.get(m, 0)) for m in members]
            member_loads.sort(key=lambda x: x[1])
            
            selected = member_loads[0][0]
            self.daily_loads[selected] = self.daily_loads.get(selected, 0) + 1
            print(f"   [LLM 5] Fallback assignment: {selected}")
            return selected
            
        except Exception as e:
            print(f"   [LLM 5] ❌ Fallback failed: {e}")
            return "Not Assigned"
    
    def _llm_skill_assignment(self, sr_data: Dict, is_java_error: bool, 
                               issue_type: str) -> str:
        """LLM CALL 5: Skill-based SR assignment"""
        print("   [LLM 5] Running skill-based assignment...")
        
        self._reset_daily_loads_if_needed()
        
        sr_id = sr_data.get('SR ID', sr_data.get('Call ID', 'Unknown'))
        priority = sr_data.get('Priority', sr_data.get('Customer Priority', 'P3'))
        description = sr_data.get('Description', '')[:1000]
        application = sr_data.get('Application', sr_data.get('application', 'Unknown'))
        
        complexity = self._calculate_complexity(sr_data, is_java_error)
        
        # Get context
        team_context = self._get_team_members_context()
        workload_status = self._get_workload_status()
        
        # Build prompt
        prompt = PROMPT_SKILL_BASED_ASSIGNMENT.format(
            sr_id=sr_id,
            priority=priority,
            description=description,
            application=application,
            complexity_score=f"{complexity:.1f}",
            is_java_error="Yes" if is_java_error else "No",
            issue_type=issue_type,
            team_members_context=team_context,
            workload_status=workload_status
        )
        
        # Call LLM with very low temperature for deterministic output
        response = self.llm.call(prompt, call_name="skill_assignment", temperature=0.1)
        
        # Clean up response - should be just a name
        assigned_name = response.strip().split('\n')[0].strip()
        # Remove any punctuation
        assigned_name = re.sub(r'[^\w\s_-]', '', assigned_name).strip()
        # Normalize underscores to spaces (LLM sometimes uses underscores)
        assigned_name = assigned_name.replace('_', ' ').strip()
        
        # Validate
        if assigned_name and assigned_name.upper() != 'UNASSIGNED':
            if self._validate_assignment_name(assigned_name):
                # Increment daily load
                self.daily_loads[assigned_name] = self.daily_loads.get(assigned_name, 0) + 1
                print(f"   [LLM 5] ✅ Assigned → {assigned_name} (load: {self.daily_loads[assigned_name]})")
                return assigned_name
            else:
                print(f"   [LLM 5] ⚠️ Name '{assigned_name}' not found in DB, using fallback")
                return self._fallback_assignment()
        
        print(f"   [LLM 5] ⚠️ No valid assignment, using fallback")
        return self._fallback_assignment()
    
    # ========================================================================
    # MAIN ANALYSIS ORCHESTRATION
    # ========================================================================
    
    def analyze_single_sr(self, sr_data: Dict) -> Dict:
        """Main orchestration - analyze single SR with 4 LLM calls"""
        
        sr_id = sr_data.get('SR ID', sr_data.get('Call ID', 'Unknown'))
        priority = sr_data.get('Priority', sr_data.get('Customer Priority', 'Medium'))
        description = str(sr_data.get('Description', ''))
        notes = str(sr_data.get('Notes', ''))
        
        print(f"\n{'='*60}")
        print(f"[*] Analyzing SR: {sr_id} (Priority: {priority})")
        print(f"{'='*60}")
        
        # STEP 1-2: Semantic Search
        print("   [SEARCH] Searching historical SRs...")
        query_text = f"{description} {notes}".strip()
        historical_matches = self.vectorstore.search_historical_srs(query_text, top_k=10)
        print(f"   [SEARCH] Found {len(historical_matches)} matches")
        
        # STEP 3: Filter garbage workarounds
        valid_workarounds = self._filter_workarounds(historical_matches)
        print(f"   [FILTER] {len(valid_workarounds)} valid workarounds after filtering")
        
        # DEBUG: Log workaround selection decision
        print(f"   [DEBUG] Historical matches count: {len(historical_matches)}")
        print(f"   [DEBUG] Valid workarounds count: {len(valid_workarounds)}")
        if valid_workarounds:
            print(f"   [DEBUG] Top valid similarity: {valid_workarounds[0]['similarity']:.1%}")
            print(f"   [DEBUG] Meets 0.5 threshold: {valid_workarounds[0]['similarity'] >= 0.5}")
        else:
            print(f"   [DEBUG] ⚠️ No valid workarounds after filtering!")
        
        # STEP 4-5: Get semantic workaround
        if valid_workarounds and valid_workarounds[0]['similarity'] >= 0.5:
            semantic_workaround = valid_workarounds[0]['workaround']
            print(f"   [WORKAROUND] Using top match ({valid_workarounds[0]['similarity']:.1%} similarity)")
        else:
            reason = 'no valid workarounds' if not valid_workarounds else f"similarity {valid_workarounds[0]['similarity']:.1%} < 0.5"
            print(f"   [DEBUG] Calling LLM 1 because: {reason}")
            # LLM CALL 1: Find workaround
            semantic_workaround = self._llm_find_workaround(sr_data, historical_matches)
        
        # STEP 6: LLM CALL 2 - Java Detection with Voting
        java_result = self._llm_detect_java_with_voting(sr_data, semantic_workaround, historical_matches)
        is_java_error = java_result.get('is_java_error', False)
        
        # STEP 7-8: Activity extraction with retry (if Java)
        validated_activities = []
        if is_java_error:
            validated_activities = self._extract_and_validate_activities(
                sr_data, semantic_workaround, historical_matches, max_retries=2
            )
        
        # STEP 9-10: Generate final resolution
        if is_java_error:
            ai_response = self._llm_java_resolution(
                sr_data, java_result, validated_activities, 
                semantic_workaround, historical_matches
            )
        else:
            ai_response = self._llm_general_resolution(
                sr_data, java_result, semantic_workaround, historical_matches
            )
        
        # Extract AI workaround from response
        ai_workaround = self._extract_ai_workaround(ai_response)
        
        # 🆕 LLM CALL 5: Skill-based assignment (replaces old logic)
        assigned_to = self._llm_skill_assignment(
            sr_data, 
            is_java_error, 
            java_result.get('issue_type', 'Unknown')
        )
        
        result = {
            'SR ID': sr_id,
            'Priority': priority,
            'Is Java Error': 'Yes' if is_java_error else 'No',
            'Confidence': java_result.get('confidence', 'Unknown'),
            'Issue Type': java_result.get('issue_type', 'Unknown'),
            'Java Votes': java_result.get('java_votes', 0),
            'Non-Java Votes': java_result.get('non_java_votes', 0),
            'Activity Names': ", ".join([a['activity_name'] for a in validated_activities]) if validated_activities else 'N/A',
            'Implementation Classes': ", ".join([a.get('impl_class', 'Unknown') for a in validated_activities]) if validated_activities else 'N/A',
            'AI Workaround': ai_workaround,
            'Full Response': ai_response,
            'Semantic Workaround Used': semantic_workaround[:500] if semantic_workaround else 'None',
            'Assigned To': assigned_to  # 🆕 From LLM CALL 5
        }
        
        print(f"   [OK] ✅ Analysis complete for {sr_id} (Assigned: {assigned_to})")
        return result
    
    def _extract_ai_workaround(self, response: str) -> str:
        """Extract AI workaround section from response"""
        if not response or len(response.strip()) < 20:
            return "[Analysis failed]"
        
        # Check if response is JSON format and convert to text
        try:
            json_data = json.loads(response.strip())
            
            # If it's a dict with AI WORKAROUND key
            if isinstance(json_data, dict):
                wa_data = json_data.get('AI WORKAROUND') or json_data.get('AI_WORKAROUND') or json_data.get('workaround')
                if wa_data:
                    return self._json_workaround_to_text(wa_data)
        except json.JSONDecodeError:
            pass  # Not JSON, continue with text extraction
        
        # Look for AI WORKAROUND marker
        markers = ["**AI WORKAROUND:**", "AI WORKAROUND:", "**WORKAROUND:**", "WORKAROUND:"]
        for marker in markers:
            start_idx = response.find(marker)
            if start_idx != -1:
                # Extract from marker to end (no more separate sections)
                # Remove any trailing NOTE: lines
                content = response[start_idx:].strip()
                
                # Remove trailing NOTE section if present
                note_idx = content.find("\nNOTE:")
                if note_idx != -1:
                    content = content[:note_idx].strip()
                
                return content
        
        # If no marker found, return the whole response (cleaned)
        return response.strip()[:3000]
    
    def _json_workaround_to_text(self, wa_data) -> str:
        """Convert JSON workaround structure to readable text"""
        lines = ["**AI WORKAROUND:**"]
        
        if isinstance(wa_data, list):
            for item in wa_data:
                if isinstance(item, dict):
                    step = item.get('step', '')
                    step_type = item.get('type', '')
                    desc = item.get('description', '')
                    details = item.get('details', {})
                    based_on = item.get('based_on', '')
                    
                    line = f"{step}. [{step_type}] {desc}" if step else f"- [{step_type}] {desc}"
                    lines.append(line)
                    
                    if isinstance(details, dict):
                        for k, v in details.items():
                            lines.append(f"   - {k}: {v}")
                    elif details:
                        lines.append(f"   - {details}")
                    
                    if based_on:
                        lines.append(f"   Based on: {based_on}")
                else:
                    lines.append(f"- {item}")
        elif isinstance(wa_data, str):
            lines.append(wa_data)
        
        return "\n".join(lines)
    
    # ========================================================================
    # FILE I/O
    # ========================================================================
    
    def find_input_excel(self) -> Optional[Path]:
        """Find Excel file in input directory"""
        excel_files = list(self.input_dir.glob("*.xlsx")) + list(self.input_dir.glob("*.xls"))
        
        if not excel_files:
            print(f"[ERROR] No Excel files found in: {self.input_dir}")
            return None
        
        excel_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        
        if len(excel_files) > 1:
            print(f"[INFO] Found {len(excel_files)} Excel files. Using LATEST: {excel_files[0].name}")
        
        return excel_files[0]
    
    def read_excel_input(self, file_path: Path) -> Optional[pd.DataFrame]:
        """Read input Excel file"""
        try:
            df = pd.read_excel(file_path)
            print(f"[OK] Read {len(df)} service requests from: {file_path.name}")
            return df
        except Exception as e:
            print(f"[ERROR] Error reading Excel: {e}")
            return None
    
    def process_all_srs(self, df: pd.DataFrame):
        """Process all SRs"""
        total_srs = len(df)
        print(f"\n[START] Processing {total_srs} SRs with Multi-Model Pipeline")
        print(f"[INFO] {self.token_manager.get_status()}")
        
        for idx, row in tqdm(df.iterrows(), total=total_srs, desc="Processing SRs"):
            try:
                sr_data = row.to_dict()
                result = self.analyze_single_sr(sr_data)
                self.results.append(result)
            except Exception as e:
                print(f"\n[ERROR] Error processing SR {row.get('SR ID', idx)}: {e}")
                self.results.append({
                    'SR ID': row.get('SR ID', f'SR_{idx}'),
                    'AI Workaround': f'Error: {str(e)}',
                    'Is Java Error': 'Error'
                })
        
        print(f"\n[OK] Processed {len(self.results)} service requests")
    
    def save_results(self, input_filename: str) -> Optional[Path]:
        """Save results to Excel"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{Path(input_filename).stem}_multimodel_{timestamp}.xlsx"
            output_path = self.output_dir / output_filename
            
            results_df = pd.DataFrame(self.results)
            results_df.to_excel(output_path, index=False, engine='openpyxl')
            
            # Print usage summary
            usage = self.llm.get_usage_summary()
            
            print(f"\n{'='*60}")
            print(f"[SUCCESS] Analysis complete")
            print(f"{'='*60}")
            print(f"[OUTPUT] File: {output_path}")
            print(f"[STATS] SRs analyzed: {len(self.results)}")
            print(f"[USAGE] Total LLM calls: {usage['total_calls']}")
            print(f"[USAGE] Total tokens: {usage['total_input_tokens']} in / {usage['total_output_tokens']} out")
            print(f"[USAGE] Total cost: ${usage['total_cost']:.4f}")
            print(f"[USAGE] {usage['tokens_status']}")
            
            # Print call breakdown
            if usage['call_breakdown']:
                print(f"\n[CALL BREAKDOWN]")
                call_counts = {}
                for call in usage['call_breakdown']:
                    name = call['call_name']
                    call_counts[name] = call_counts.get(name, 0) + 1
                for name, count in call_counts.items():
                    print(f"  • {name}: {count} calls")
            
            print(f"{'='*60}")
            
            return output_path
            
        except Exception as e:
            print(f"[ERROR] Error saving results: {e}")
            return None
    
    def run(self):
        """Main pipeline execution"""
        print("\n" + "="*70)
        print("Multi-Model SR Analysis RAG Pipeline (ChatGPT + 4 LLM Calls)")
        print("="*70)
        
        # Find input
        input_file = self.find_input_excel()
        if not input_file:
            print(f"\nPlease place an Excel file in: {self.input_dir}")
            return False
        
        # Read input
        df = self.read_excel_input(input_file)
        if df is None:
            return False
        
        # Process all SRs
        self.process_all_srs(df)
        
        # Save results
        output_path = self.save_results(input_file.name)
        
        return output_path is not None


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Multi-Model SR Analysis Pipeline")
    parser.add_argument('--tokens', type=str, default=None, help='Path to Tokens.xlsx')
    parser.add_argument('--model', type=str, default='gpt-4.1', help='Model name')
    
    args = parser.parse_args()
    
    try:
        tokens_file = Path(args.tokens) if args.tokens else None
        pipeline = MultiModelSRPipeline(tokens_file=tokens_file, model_name=args.model)
        success = pipeline.run()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\nPipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nFatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

