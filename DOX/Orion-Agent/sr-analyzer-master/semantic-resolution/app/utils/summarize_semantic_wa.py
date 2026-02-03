#!/usr/bin/env python3
"""
Semantic Workaround Summarization Module
Summarizes workarounds from similar SRs into actionable steps using LLM

This module is separate from the main RAG pipeline to:
1. Keep summarization logic isolated
2. Allow easy updates to summarization prompts
3. Enable caching and performance optimizations
4. Make UI-triggered summarization independent
"""

import os
import sys
import json
import logging
import re
from typing import List, Dict, Optional

# Setup paths
UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(UTILS_DIR)
PROJECT_ROOT = os.path.dirname(APP_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Setup logging
logger = logging.getLogger(__name__)

# ============================================================================
# PROMPT
# ============================================================================

PROMPT_SUMMARIZE_SEMANTIC_WA = """You are a workaround summarization expert for Service Request analysis. Your goal is to synthesize multiple historical workarounds into clear, actionable steps.

=== CURRENT SERVICE REQUEST ===
SR ID: {sr_id}
Description: {description}
Priority: {priority}

=== SIMILAR SR WORKAROUNDS ===
The following workarounds were used to solve similar issues:

{semantic_workarounds}

{abbreviation_context}

=== YOUR TASK ===
Analyze all the workarounds above and create a UNIFIED, ACTIONABLE summary of the best resolution steps.

=== SUMMARIZATION RULES ===
1. Combine similar steps from different workarounds into single comprehensive steps
2. Remove duplicates and redundant information
3. Prioritize steps that appear in multiple workarounds (proven solutions)
4. Keep only actionable, specific steps (no vague advice like "check system")
5. Order steps logically: Investigation → Root Cause → Action → Verification
6. If workarounds conflict, prefer the one with higher similarity score
7. Remove garbage: "NA", "escalated", "pending", generic statements, empty content
8. Include specific commands, paths, or identifiers where mentioned
9. Maximum 6-10 concise, clear steps
10. For P1/P2: Prioritize quick resolution steps first
11. For P3/P4: Include thorough investigation steps

=== GOOD OUTPUT EXAMPLE ===
Input workarounds from 3 similar SRs:
- SR1 (85%): "Checked logs, found NPE in OrderService. Restarted service. Issue resolved."
- SR2 (78%): "Customer data was missing address. Updated customer record. Retried order."
- SR3 (72%): "Order timeout. Increased timeout to 60s in config. Worked after retry."

Good summarized output:
1. Check application logs for NullPointerException or timeout errors in OrderService
2. Verify customer data completeness, especially address fields
3. If data missing, update customer record with correct information
4. Check and increase timeout configuration if needed (recommend 60s)
5. Restart the OrderService to apply changes
6. Retry the failed order and confirm successful completion

=== BAD OUTPUT EXAMPLE (AVOID) ===
1. Check logs
2. []
3. Fix the issue
4. [NEEDS INVESTIGATION]
5. Restart something
6. Contact team

Problems: Too vague, empty brackets, no specific actions

=== CONFLICT RESOLUTION ===
If workarounds provide conflicting advice:
- Prefer higher similarity score workaround
- Prefer more recent SR resolution
- Note the alternative: "Alternative approach from SR XXX: ..."

=== OUTPUT FORMAT ===
Return ONLY numbered steps with specific details. No headers, no explanations, no markdown, no brackets:

1. Check the application logs at the specified path for the error pattern
2. Verify customer data in database using the customer ID from the SR
3. Restart the affected service if needed
4. Update the configuration or data as specified in historical workarounds
5. Confirm the fix by testing the affected functionality
...

CRITICAL: Do NOT use placeholder brackets like [] or (). Write actual content or skip the step.

If no useful workarounds found, return exactly:
No actionable workarounds found from similar SRs. Manual investigation recommended.
"""


# ============================================================================
# LLM HANDLER (With Token Rotation - same as main pipeline)
# ============================================================================

class SummarizationLLM:
    """LLM handler for summarization with automatic token rotation on quota exhaustion"""
    
    def __init__(self):
        self.tokens = []  # List of all available tokens
        self.current_index = 0
        self.exhausted_tokens = set()  # Track exhausted token indices
        self.model = "gpt-4.1"
        self.base_url = "https://ai-framework1:8085/api/v1/call_llm"
        
        # Usage tracking
        self.total_calls = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        
        self._load_all_tokens()
    
    def _load_all_tokens(self):
        """Load ALL API tokens from Tokens.xlsx for rotation"""
        tokens_file = os.path.join(PROJECT_ROOT, 'tokens', 'Tokens.xlsx')
        
        if os.path.exists(tokens_file):
            try:
                import pandas as pd
                df = pd.read_excel(tokens_file)
                
                # Find token column
                token_col = None
                for col in df.columns:
                    if 'token' in col.lower() or 'api' in col.lower() or 'key' in col.lower():
                        token_col = col
                        break
                
                if token_col:
                    # Load ALL valid tokens
                    for _, row in df.iterrows():
                        token = str(row[token_col]).strip()
                        if token and token != 'nan' and len(token) > 10:
                            self.tokens.append(token)
                    
                    if self.tokens:
                        logger.info(f"[SummarizationLLM] Loaded {len(self.tokens)} API tokens for rotation")
                        return
            except Exception as e:
                logger.warning(f"[SummarizationLLM] Failed to load Tokens.xlsx: {e}")
        
        # Fallback to environment variable
        env_token = os.environ.get('OPENAI_API_KEY', '')
        if env_token:
            self.tokens.append(env_token)
            logger.info("[SummarizationLLM] Loaded 1 token from environment")
        else:
            logger.warning("[SummarizationLLM] No API tokens found - summarization will be skipped")
    
    def get_current_token(self) -> str:
        """Get current active token"""
        if not self.tokens:
            return ""
        return self.tokens[self.current_index]
    
    def rotate_token(self) -> bool:
        """Rotate to next available token. Returns True if rotation successful."""
        if not self.tokens:
            return False
        
        self.exhausted_tokens.add(self.current_index)
        logger.info(f"[SummarizationLLM] ⚠️ Token #{self.current_index + 1} exhausted")
        
        # Find next non-exhausted token
        for i in range(len(self.tokens)):
            next_idx = (self.current_index + 1 + i) % len(self.tokens)
            if next_idx not in self.exhausted_tokens:
                self.current_index = next_idx
                logger.info(f"[SummarizationLLM] ✅ Rotated to token #{self.current_index + 1}")
                return True
        
        logger.error("[SummarizationLLM] ❌ All tokens exhausted!")
        return False
    
    def _update_usage_stats(self, call_result: dict):
        """Update LLM usage stats file with summarization costs"""
        try:
            from datetime import datetime
            usage_file = os.path.join(PROJECT_ROOT, 'data', 'database', 'llm_usage_stats.json')
            
            # Load existing stats
            existing_data = {}
            if os.path.exists(usage_file):
                with open(usage_file, 'r') as f:
                    existing_data = json.load(f)
            
            # Update summarization-specific stats
            summarization_stats = existing_data.get('summarization', {
                'total_calls': 0,
                'total_input_tokens': 0,
                'total_output_tokens': 0,
                'total_cost': 0.0
            })
            
            summarization_stats['total_calls'] += 1
            summarization_stats['total_input_tokens'] += call_result.get('input_tokens', 0)
            summarization_stats['total_output_tokens'] += call_result.get('output_tokens', 0)
            summarization_stats['total_cost'] += call_result.get('cost', 0)
            summarization_stats['last_updated'] = datetime.now().isoformat()
            
            existing_data['summarization'] = summarization_stats
            
            # Write back
            with open(usage_file, 'w') as f:
                json.dump(existing_data, f, indent=2)
                
        except Exception as e:
            logger.warning(f"[SummarizationLLM] Failed to update usage stats: {e}")
    
    def get_usage_stats(self) -> dict:
        """Get current usage statistics"""
        return {
            'total_calls': self.total_calls,
            'total_input_tokens': self.total_input_tokens,
            'total_output_tokens': self.total_output_tokens,
            'total_cost': self.total_cost
        }
    
    def call(self, prompt: str, temperature: float = 0.2) -> str:
        """Make LLM call with automatic token rotation on quota exhaustion"""
        if not self.tokens:
            logger.error("[SummarizationLLM] No API tokens available")
            return ""
        
        import requests
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Set NO_PROXY for internal API
        os.environ["NO_PROXY"] = os.environ.get("no_proxy", "") + ",ai-framework1"
        
        # Try with token rotation
        max_retries = len(self.tokens)
        
        for attempt in range(max_retries):
            current_token = self.get_current_token()
            if not current_token:
                return ""
            
            try:
                headers = {
                    "Content-Type": "application/json",
                    "accept": "application/json",
                    "API-Key": current_token,
                    "X-Effective-Caller": "sr_summarization@amdocs.com"
                }
                
                payload = {
                    "llm_model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert at summarizing technical workarounds into clear, actionable steps."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
                
                response = requests.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                    timeout=60,
                    verify=False
                )
                
                if response.status_code == 200:
                    result = response.json()
                    message = result.get('message', '').strip()
                    
                    # Track usage
                    self.total_calls += 1
                    self.total_input_tokens += result.get('input_tokens', 0)
                    self.total_output_tokens += result.get('output_tokens', 0)
                    self.total_cost += result.get('cost', 0)
                    
                    # Update the usage stats file
                    self._update_usage_stats(result)
                    
                    if message:
                        logger.info(f"[SummarizationLLM] ✅ Call successful (token #{self.current_index + 1}, cost: ${result.get('cost', 0):.4f})")
                    return message
                
                elif response.status_code == 429 or 'quota' in response.text.lower() or 'limit' in response.text.lower():
                    # Token exhausted - rotate and retry
                    logger.warning(f"[SummarizationLLM] Token #{self.current_index + 1} quota exceeded, rotating...")
                    if not self.rotate_token():
                        return ""  # All tokens exhausted
                    continue
                
                else:
                    logger.error(f"[SummarizationLLM] API error: {response.status_code} - {response.text[:200]}")
                    return ""
                    
            except Exception as e:
                logger.error(f"[SummarizationLLM] Call failed: {e}")
                return ""
        
        return ""


# ============================================================================
# MAIN SUMMARIZATION CLASS
# ============================================================================

class SemanticWASummarizer:
    """
    Summarizes semantic workarounds from similar SRs into actionable steps.
    
    Usage:
        summarizer = SemanticWASummarizer()
        summary = summarizer.summarize(sr_id, description, priority, similar_srs)
    """
    
    def __init__(self):
        self.llm = SummarizationLLM()
        self._cache = {}  # Simple in-memory cache
        self.abbreviation_context = self._load_abbreviations()
        logger.info("[SemanticWASummarizer] Initialized")
    
    def _load_abbreviations(self) -> str:
        """Load abbreviation context from abbreviation.db"""
        try:
            import sqlite3
            abbrev_db_path = os.path.join(PROJECT_ROOT, 'vectorstores', 'abbreviation.db')
            
            if not os.path.exists(abbrev_db_path):
                logger.debug("[SemanticWASummarizer] abbreviation.db not found")
                return ""
            
            conn = sqlite3.connect(abbrev_db_path)
            cursor = conn.cursor()
            
            # Get table name
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            if not tables:
                conn.close()
                return ""
            
            table_name = tables[0][0]
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 50")
            rows = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            conn.close()
            
            if not rows:
                return ""
            
            # Build context string
            abbrev_list = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                short = row_dict.get('short_form', row_dict.get('abbreviation', ''))
                full = row_dict.get('full_form', row_dict.get('meaning', row_dict.get('description', '')))
                if short and full:
                    abbrev_list.append(f"- {short}: {full}")
            
            if abbrev_list:
                return "=== ABBREVIATION REFERENCE ===\n" + "\n".join(abbrev_list[:30])
            return ""
            
        except Exception as e:
            logger.debug(f"[SemanticWASummarizer] Could not load abbreviations: {e}")
            return ""
    
    def _build_workarounds_context(self, similar_srs: List[Dict]) -> str:
        """Build context string from similar SRs"""
        context = ""
        valid_count = 0
        
        for i, sr in enumerate(similar_srs[:5], 1):  # Top 5 only
            similarity = sr.get('similarity', 0)
            
            # Get workaround from various possible field names
            workaround = (
                sr.get('workaround') or 
                sr.get('ai_workaround') or 
                sr.get('ai_generated_workaround') or
                sr.get('semantic_workaround') or
                ''
            )
            
            # Get resolution category
            resolution = (
                sr.get('resolution_category') or 
                sr.get('sla_resolution') or
                sr.get('category') or
                'Unknown'
            )
            
            # Get CAS ID from various possible field names (prioritize call_id)
            cas_id = sr.get('call_id', '') or sr.get('sr_id', '') or sr.get('cas_id', '') or f'Unknown#{i}'
            
            # Skip garbage workarounds
            workaround_lower = workaround.lower().strip() if workaround else ''
            if not workaround or workaround_lower in [
                'na', 'n/a', 'none', 'pending', 'escalated', '', 
                'not available', 'no workaround', 'null', 'undefined'
            ]:
                continue
            
            # Skip very short workarounds (likely garbage)
            if len(workaround.strip()) < 20:
                continue
            
            # Enhanced check: Skip workarounds that are just headers with empty content
            # (e.g., "**AI WORKAROUND:**\n- []\n- []")
            cleaned_wa = workaround
            for pattern in ['**AI WORKAROUND:**', '**AI WORKAROUND**', 'AI WORKAROUND:', 'AI WORKAROUND']:
                cleaned_wa = cleaned_wa.replace(pattern, '')
            # Remove empty brackets and empty bullet/numbered lines
            cleaned_wa = re.sub(r'\[\s*\]', '', cleaned_wa)  # Remove []
            cleaned_wa = re.sub(r'^\s*[-*•]\s*$', '', cleaned_wa, flags=re.MULTILINE)  # Empty bullets
            cleaned_wa = re.sub(r'^\s*\d+\.\s*$', '', cleaned_wa, flags=re.MULTILINE)  # Empty numbers
            cleaned_wa = re.sub(r'\n+', '\n', cleaned_wa).strip()  # Collapse newlines
            
            if len(cleaned_wa) < 15:
                logger.debug(f"Skipping empty/header-only workaround for {cas_id}")
                continue
            
            valid_count += 1
            
            # Format percentage correctly
            if isinstance(similarity, float) and similarity <= 1:
                sim_display = f"{similarity:.0%}"
            else:
                sim_display = f"{similarity}%"
            
            # CAS ID as the FIRST line, prominently displayed
            context += f"\n=== CAS ID: {cas_id} ===\n"
            context += f"Similarity: {sim_display}\n"
            context += f"Resolution Category: {resolution}\n"
            context += f"Workaround:\n{workaround[:800]}\n"
        
        return context
    
    def summarize(self, sr_id: str, description: str, priority: str, 
                  similar_srs: List[Dict]) -> Dict:
        """
        Summarize semantic workarounds into actionable steps.
        
        Args:
            sr_id: Current SR ID
            description: SR description
            priority: SR priority
            similar_srs: List of similar SRs with workarounds
            
        Returns:
            Dict with 'success', 'summary', 'similar_count', and 'cas_ids'
        """
        
        # Quick validation
        if not similar_srs:
            return {
                'success': False,
                'summary': "No similar SRs found.",
                'similar_count': 0,
                'cas_ids': []
            }
        
        # Check cache (simple key based on SR ID)
        cache_key = f"{sr_id}_{len(similar_srs)}"
        if cache_key in self._cache:
            logger.info(f"[SemanticWASummarizer] Cache hit for {sr_id}")
            return self._cache[cache_key]
        
        # Extract all CAS IDs first (for header display)
        cas_ids = []
        for sr in similar_srs[:5]:  # Top 5 only
            cas_id = sr.get('call_id', '') or sr.get('sr_id', '') or sr.get('cas_id', '')
            if cas_id and cas_id not in cas_ids:
                cas_ids.append(cas_id)
        
        # Build workarounds context
        workarounds_context = self._build_workarounds_context(similar_srs)
        
        if not workarounds_context.strip():
            # Return success=True with a clear message so frontend uses this instead of showing individual cards
            cas_ids_header = "Similar SRs Found:\n" + "\n".join([f"  • {cid}" for cid in cas_ids]) if cas_ids else ""
            no_wa_message = f"""{cas_ids_header}

⚠️ No workarounds were recorded by users for these similar SRs.

The similar tickets found had their issues resolved, but the resolution steps were not documented by users.
Manual investigation is recommended based on the SR descriptions."""

            result = {
                'success': True,  # Return True so frontend uses this message
                'summary': no_wa_message.strip(),
                'similar_count': len(similar_srs),
                'cas_ids': cas_ids,
                'no_recorded_workarounds': True  # Flag to indicate no WA recorded
            }
            # Cache this result too
            self._cache[cache_key] = result
            logger.info(f"[SemanticWASummarizer] ⚠️ No workarounds recorded for similar SRs of {sr_id}")
            return result
        
        # Build prompt
        prompt = PROMPT_SUMMARIZE_SEMANTIC_WA.format(
            sr_id=sr_id,
            description=description[:1500] if description else "Not provided",
            priority=priority or "Medium",
            semantic_workarounds=workarounds_context,
            abbreviation_context=self.abbreviation_context
        )
        
        # Call LLM
        logger.info(f"[SemanticWASummarizer] Summarizing workarounds for SR {sr_id}...")
        response = self.llm.call(prompt, temperature=0.1)
        
        if response:
            # Build final summary with CAS IDs header first
            cas_ids_header = "Similar SRs Referenced:\n" + "\n".join([f"  • {cid}" for cid in cas_ids]) if cas_ids else ""
            full_summary = f"{cas_ids_header}\n\n--- Summarized Workaround ---\n\n{response}" if cas_ids_header else response
            
            result = {
                'success': True,
                'summary': full_summary,
                'similar_count': len(similar_srs),
                'cas_ids': cas_ids
            }
            # Cache the result
            self._cache[cache_key] = result
            logger.info(f"[SemanticWASummarizer] ✅ Successfully summarized for {sr_id}")
            return result
        else:
            return {
                'success': False,
                'summary': "Unable to generate summary. Please try again.",
                'similar_count': len(similar_srs),
                'cas_ids': cas_ids
            }
    
    def clear_cache(self):
        """Clear the summarization cache"""
        self._cache = {}
        logger.info("[SemanticWASummarizer] Cache cleared")


# ============================================================================
# SINGLETON INSTANCE
# ============================================================================

_summarizer_instance = None

def get_summarizer() -> SemanticWASummarizer:
    """Get or create the singleton summarizer instance"""
    global _summarizer_instance
    if _summarizer_instance is None:
        _summarizer_instance = SemanticWASummarizer()
    return _summarizer_instance


def summarize_semantic_workarounds(sr_id: str, description: str, priority: str,
                                    similar_srs: List[Dict]) -> Dict:
    """
    Convenience function to summarize workarounds.
    
    Args:
        sr_id: Current SR ID
        description: SR description  
        priority: SR priority
        similar_srs: List of similar SRs with workarounds
        
    Returns:
        Dict with 'success', 'summary', 'similar_count'
    """
    summarizer = get_summarizer()
    return summarizer.summarize(sr_id, description, priority, similar_srs)

