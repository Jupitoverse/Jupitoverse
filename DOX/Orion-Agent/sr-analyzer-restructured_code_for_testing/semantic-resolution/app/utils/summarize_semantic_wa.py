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

PROMPT_SUMMARIZE_SEMANTIC_WA = """You are a workaround summarization expert for Service Request analysis.

=== CURRENT SERVICE REQUEST ===
SR ID: {sr_id}
Description: {description}
Priority: {priority}

=== SIMILAR SR WORKAROUNDS ===
The following workarounds were used to solve similar issues:

{semantic_workarounds}

=== YOUR TASK ===
Analyze all the workarounds above and create a UNIFIED, ACTIONABLE summary of the best resolution steps.

RULES:
1. Combine similar steps from different workarounds into single comprehensive steps
2. Remove duplicates and redundant information
3. Prioritize steps that appear in multiple workarounds (proven solutions)
4. Keep only actionable, specific steps (no vague advice like "check system")
5. Order steps logically: Investigation → Root Cause → Action → Verification
6. If workarounds conflict, prefer the one with higher similarity score
7. Remove garbage: "NA", "escalated", "pending", generic statements, empty content
8. Include specific commands, paths, or identifiers where mentioned
9. Maximum 6-10 concise, clear steps

=== OUTPUT FORMAT ===
Return ONLY numbered steps. No headers, no explanations, no markdown:

1. [First action step with specific details]
2. [Second action step]
3. [Third action step]
...

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
                    if message:
                        logger.info(f"[SummarizationLLM] ✅ Call successful (token #{self.current_index + 1})")
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
        logger.info("[SemanticWASummarizer] Initialized")
    
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
            Dict with 'success', 'summary', and 'similar_count'
        """
        
        # Quick validation
        if not similar_srs:
            return {
                'success': False,
                'summary': "No similar SRs found.",
                'similar_count': 0
            }
        
        # Check cache (simple key based on SR ID)
        cache_key = f"{sr_id}_{len(similar_srs)}"
        if cache_key in self._cache:
            logger.info(f"[SemanticWASummarizer] Cache hit for {sr_id}")
            return self._cache[cache_key]
        
        # Build workarounds context
        workarounds_context = self._build_workarounds_context(similar_srs)
        
        if not workarounds_context.strip():
            return {
                'success': False,
                'summary': "No actionable workarounds found in similar SRs.",
                'similar_count': len(similar_srs)
            }
        
        # Build prompt
        prompt = PROMPT_SUMMARIZE_SEMANTIC_WA.format(
            sr_id=sr_id,
            description=description[:1500] if description else "Not provided",
            priority=priority or "Medium",
            semantic_workarounds=workarounds_context
        )
        
        # Call LLM
        logger.info(f"[SemanticWASummarizer] Summarizing workarounds for SR {sr_id}...")
        response = self.llm.call(prompt, temperature=0.2)
        
        if response:
            result = {
                'success': True,
                'summary': response,
                'similar_count': len(similar_srs)
            }
            # Cache the result
            self._cache[cache_key] = result
            logger.info(f"[SemanticWASummarizer] ✅ Successfully summarized for {sr_id}")
            return result
        else:
            return {
                'success': False,
                'summary': "Unable to generate summary. Please try again.",
                'similar_count': len(similar_srs)
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

