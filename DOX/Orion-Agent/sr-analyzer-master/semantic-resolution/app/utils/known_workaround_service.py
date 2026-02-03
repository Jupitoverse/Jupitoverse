#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Known Workaround Service
Searches JSON knowledge base for known workarounds matching SR descriptions.

This service integrates with the json_workaround module to provide:
- Keyword-based search for known issues
- Match scoring based on description/RCA similarity
- High-priority workarounds for LLM context
"""

import re
import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Stop words for keyword extraction
STOP_WORDS = {
    'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'in', 
    'with', 'to', 'for', 'of', 'as', 'it', 'that', 'this', 'from', 'by', 
    'be', 'are', 'was', 'were', 'been', 'being', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
    'must', 'shall', 'can', 'need', 'dare', 'ought', 'used', 'get', 'got',
    'getting', 'make', 'made', 'making', 'go', 'going', 'went', 'gone',
    'take', 'took', 'taken', 'see', 'saw', 'seen', 'know', 'knew', 'known',
    'think', 'thought', 'want', 'wanted', 'use', 'using', 'find', 'found',
    'give', 'gave', 'given', 'tell', 'told', 'try', 'tried', 'ask', 'asked',
    'seem', 'seemed', 'feel', 'felt', 'become', 'became', 'leave', 'left',
    'put', 'keep', 'kept', 'let', 'begin', 'began', 'begun', 'show', 'showed',
    'shown', 'hear', 'heard', 'play', 'played', 'run', 'ran', 'move', 'moved',
    'like', 'liked', 'live', 'lived', 'believe', 'believed', 'hold', 'held',
    'bring', 'brought', 'happen', 'happened', 'write', 'wrote', 'written',
    'provide', 'provided', 'sit', 'sat', 'stand', 'stood', 'lose', 'lost',
    'pay', 'paid', 'meet', 'met', 'include', 'included', 'continue', 'continued',
    'set', 'learn', 'learned', 'change', 'changed', 'lead', 'led', 'understand',
    'understood', 'watch', 'watched', 'follow', 'followed', 'stop', 'stopped',
    'create', 'created', 'speak', 'spoke', 'spoken', 'read', 'allow', 'allowed',
    'add', 'added', 'spend', 'spent', 'grow', 'grew', 'grown', 'open', 'opened',
    'walk', 'walked', 'win', 'won', 'offer', 'offered', 'remember', 'remembered',
    'love', 'loved', 'consider', 'considered', 'appear', 'appeared', 'buy',
    'bought', 'wait', 'waited', 'serve', 'served', 'die', 'died', 'send', 'sent',
    'expect', 'expected', 'build', 'built', 'stay', 'stayed', 'fall', 'fell',
    'cut', 'reach', 'reached', 'kill', 'killed', 'remain', 'remained', 'customer',
    'issue', 'problem', 'error', 'please', 'help', 'need', 'unable', 'not',
    'working', 'work', 'user', 'users', 'system', 'service', 'request', 'ticket',
    'sr', 'case', 'reported', 'report', 'facing', 'face', 'getting', 'showing',
    'shows', 'display', 'displays', 'see', 'seeing', 'receiving', 'received',
    'when', 'while', 'trying', 'after', 'before', 'during', 'since', 'until'
}


class KnownWorkaroundService:
    """
    Service to find known workarounds from JSON knowledge base.
    
    Provides semantic matching between new SR descriptions and 
    known issues stored in the JSON workaround database.
    """
    
    def __init__(self):
        """Initialize the service with the workaround handler."""
        self.handler = None
        self._init_handler()
    
    def _init_handler(self):
        """Lazily initialize the workaround handler."""
        try:
            from json_workaround.data_handler import get_workaround_handler
            self.handler = get_workaround_handler()
            logger.info(f"Known workaround service initialized with {len(self.handler.data)} records")
        except Exception as e:
            logger.error(f"Failed to initialize known workaround handler: {e}")
            self.handler = None
    
    def find_known_workaround(self, description, rca: str = "", 
                              threshold: float = 0.35) -> Optional[Dict]:
        """
        Find the best matching known workaround for a given issue.
        
        Args:
            description: SR description text (str) OR sr_data dict with 'description' key
            rca: Root cause analysis or resolution category (if available)
            threshold: Minimum match score (0-1), default 0.35 (35%)
            
        Returns:
            Best matching workaround dict with 'match_score' field, or None
        """
        if not self.handler:
            self._init_handler()
            if not self.handler:
                return None
        
        # Handle dict input (sr_data) - extract description field
        if isinstance(description, dict):
            description = str(description.get('description', '') or description.get('Description', ''))
        
        # Ensure string type
        description = str(description) if description else ""
        
        if not description or len(description.strip()) < 10:
            return None
        
        try:
            # Extract meaningful keywords from description
            keywords = self._extract_keywords(description)
            
            if not keywords:
                logger.debug("No meaningful keywords extracted from description")
                return None
            
            # Search JSON workarounds using multiple keyword combinations
            all_matches = []
            
            # Strategy 1: Full keyword search
            full_query = ' '.join(keywords[:8])
            results = self.handler.search_combined(
                description_query=full_query,
                rca_query=rca if rca else "",
                limit=10
            )
            all_matches.extend(results)
            
            # Strategy 2: Individual keyword search (for catching specific terms)
            for keyword in keywords[:5]:
                if len(keyword) >= 4:  # Only meaningful keywords
                    results = self.handler.search_combined(
                        description_query=keyword,
                        rca_query="",
                        limit=3
                    )
                    all_matches.extend(results)
            
            # Strategy 3: Error pattern matching
            error_patterns = self._extract_error_patterns(description)
            for pattern in error_patterns[:3]:
                results = self.handler.search_combined(
                    description_query=pattern,
                    rca_query="",
                    limit=3
                )
                all_matches.extend(results)
            
            if not all_matches:
                return None
            
            # Score and rank all matches
            scored_matches = self._score_matches(all_matches, description, rca)
            
            if scored_matches and scored_matches[0]['match_score'] >= threshold:
                best = scored_matches[0]
                logger.info(f"✅ Found known workaround: SR {best.get('sr_id', 'N/A')} "
                           f"(score: {best['match_score']:.1%})")
                return best
            
            return None
            
        except Exception as e:
            logger.error(f"Known workaround search error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def find_all_matching_workarounds(self, description, rca: str = "",
                                      limit: int = 5, threshold: float = 0.25) -> List[Dict]:
        """
        Find all matching known workarounds above threshold.
        
        Args:
            description: SR description text (str) OR sr_data dict with 'description' key
            rca: Root cause analysis (if available)
            limit: Maximum number of results
            threshold: Minimum match score
            
        Returns:
            List of matching workarounds with 'match_score' field
        """
        if not self.handler:
            self._init_handler()
            if not self.handler:
                return []
        
        # Handle dict input (sr_data) - extract description field
        if isinstance(description, dict):
            description = str(description.get('description', '') or description.get('Description', ''))
        
        # Ensure string type
        description = str(description) if description else ""
        
        if not description or len(description.strip()) < 10:
            return []
        
        try:
            keywords = self._extract_keywords(description)
            if not keywords:
                return []
            
            all_matches = []
            
            # Search with combined keywords
            full_query = ' '.join(keywords[:8])
            results = self.handler.search_combined(
                description_query=full_query,
                rca_query=rca,
                limit=20
            )
            all_matches.extend(results)
            
            # Score and filter
            scored = self._score_matches(all_matches, description, rca)
            filtered = [m for m in scored if m['match_score'] >= threshold]
            
            return filtered[:limit]
            
        except Exception as e:
            logger.error(f"Known workaround search error: {e}")
            return []
    
    def _extract_keywords(self, text: str) -> List[str]:
        """
        Extract meaningful keywords from text for searching.
        
        Args:
            text: Input text to extract keywords from
            
        Returns:
            List of keywords ordered by importance
        """
        if not text:
            return []
        
        # Normalize text
        text_lower = text.lower()
        
        # Extract words, keeping only alphanumeric
        words = re.findall(r'\b[a-z0-9]+\b', text_lower)
        
        # Filter out stop words and short words
        keywords = [w for w in words if len(w) >= 3 and w not in STOP_WORDS]
        
        # Add error patterns (CamelCase, Exception names)
        error_patterns = self._extract_error_patterns(text)
        
        # Combine and deduplicate while preserving order
        seen = set()
        result = []
        
        # Error patterns first (high value)
        for pattern in error_patterns:
            pattern_lower = pattern.lower()
            if pattern_lower not in seen:
                seen.add(pattern_lower)
                result.append(pattern)
        
        # Then regular keywords
        for kw in keywords:
            if kw not in seen:
                seen.add(kw)
                result.append(kw)
        
        return result
    
    def _extract_error_patterns(self, text: str) -> List[str]:
        """
        Extract error-specific patterns from text.
        
        Args:
            text: Input text
            
        Returns:
            List of error patterns found
        """
        patterns = []
        
        # CamelCase words (likely class names)
        camel_case = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b', text)
        patterns.extend(camel_case)
        
        # Exception/Error names
        exceptions = re.findall(r'\b\w+(?:Exception|Error|Failure|Fault)\b', text, re.IGNORECASE)
        patterns.extend(exceptions)
        
        # Activity names (common pattern in this codebase)
        activities = re.findall(r'\b\w+Activity\b', text)
        patterns.extend(activities)
        
        # Java package patterns
        java_packages = re.findall(r'(?:com|org|java)\.[a-z.]+\.[A-Z]\w+', text)
        patterns.extend(java_packages)
        
        # Specific error codes
        error_codes = re.findall(r'\b(?:ERR|ERROR|FAIL|ORA|SQL)[_-]?\d+\b', text, re.IGNORECASE)
        patterns.extend(error_codes)
        
        return list(set(patterns))
    
    def _score_matches(self, matches: List[Dict], description: str, 
                       rca: str) -> List[Dict]:
        """
        Score and rank matches by relevance to the query.
        
        Args:
            matches: List of potential matches from search
            description: Original SR description
            rca: Original RCA/category
            
        Returns:
            List of matches with 'match_score' field, sorted by score
        """
        if not matches:
            return []
        
        seen_ids = set()
        scored = []
        
        desc_lower = description.lower()
        desc_words = set(re.findall(r'\b[a-z0-9]+\b', desc_lower))
        desc_words = desc_words - STOP_WORDS
        
        rca_lower = rca.lower() if rca else ""
        rca_words = set(re.findall(r'\b[a-z0-9]+\b', rca_lower)) if rca_lower else set()
        
        # Extract error patterns from description for bonus scoring
        desc_errors = set(p.lower() for p in self._extract_error_patterns(description))
        
        for match in matches:
            sr_id = match.get('sr_id', '')
            if sr_id in seen_ids:
                continue
            seen_ids.add(sr_id)
            
            # Get match text
            match_desc = (match.get('description', '') or '').lower()
            match_rca = (match.get('rca', '') or '').lower()
            match_wa = (match.get('workaround', '') or '').lower()
            
            match_words = set(re.findall(r'\b[a-z0-9]+\b', match_desc))
            match_words = match_words - STOP_WORDS
            
            # Calculate word overlap score
            if desc_words and match_words:
                overlap = len(desc_words & match_words)
                union = len(desc_words | match_words)
                jaccard_score = overlap / union if union > 0 else 0
            else:
                jaccard_score = 0
            
            # Check for error pattern matches (high value)
            match_errors = set(p.lower() for p in self._extract_error_patterns(
                match.get('description', '') + ' ' + match.get('rca', '')
            ))
            error_overlap = len(desc_errors & match_errors)
            error_bonus = min(error_overlap * 0.15, 0.3)  # Up to 30% bonus
            
            # RCA match bonus
            rca_bonus = 0
            if rca_words and match_rca:
                match_rca_words = set(re.findall(r'\b[a-z0-9]+\b', match_rca))
                rca_overlap = len(rca_words & match_rca_words)
                if rca_overlap > 0:
                    rca_bonus = min(rca_overlap * 0.1, 0.2)  # Up to 20% bonus
            
            # Workaround quality bonus (prefer matches with good workarounds)
            wa_bonus = 0
            if match_wa and len(match_wa) > 50:
                wa_bonus = 0.05  # 5% bonus for having a substantial workaround
            
            # Calculate final score
            final_score = jaccard_score + error_bonus + rca_bonus + wa_bonus
            final_score = min(final_score, 1.0)  # Cap at 100%
            
            match_copy = match.copy()
            match_copy['match_score'] = final_score
            scored.append(match_copy)
        
        # Sort by score descending
        scored.sort(key=lambda x: x['match_score'], reverse=True)
        
        return scored
    
    def get_stats(self) -> Dict:
        """Get statistics about the known workaround database."""
        if not self.handler:
            self._init_handler()
        
        if self.handler:
            return self.handler.get_stats()
        return {'total_records': 0, 'data_loaded': False}
    
    def reload_data(self):
        """Reload the workaround data from JSON file."""
        if self.handler:
            self.handler.reload_data()
            logger.info("Known workaround data reloaded")


# Singleton instance for shared access
_service_instance: Optional[KnownWorkaroundService] = None


def get_known_workaround_service() -> KnownWorkaroundService:
    """Get or create the singleton KnownWorkaroundService instance."""
    global _service_instance
    if _service_instance is None:
        _service_instance = KnownWorkaroundService()
    return _service_instance
