#!/usr/bin/env python3
"""
Helper Utilities for SR Feedback Application
Common utility functions used across routes
"""

import re
import os
import pandas as pd
from typing import Dict, Optional
from datetime import datetime
from pathlib import Path


def safe_get(d: Dict, keys, default='NA') -> str:
    """
    Safely get values from dict and handle NaN/None values
    
    Args:
        d: Dictionary to search
        keys: Key or list of keys to try
        default: Default value if not found
    
    Returns:
        Value from dict or default
    """
    if isinstance(keys, str):
        keys = [keys]
    for key in keys:
        val = d.get(key, default)
        if pd.isna(val) or val is None or str(val).strip() == '':
            continue
        return str(val)
    return default


def sanitize_for_json(value, default='') -> str:
    """
    Clean value for JSON serialization - handles NaN, None, and control characters
    """
    if value is None:
        return default
    
    try:
        if pd.isna(value):
            return default
    except (TypeError, ValueError):
        pass
    
    val_str = str(value)
    
    if val_str.lower() in ['nan', 'none', 'null', 'nat']:
        return default
    
    val_str = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', val_str)
    return val_str


def concatenate_categorization_fields(sr_dict: Dict, source: str = 'excel_temp') -> str:
    """Concatenate SLA categorization fields into a single display string"""
    fields = []
    
    # Try both naming conventions since ChromaDB may use either
    field_name_variants = [
        # (snake_case, Title Case, ChromaDB specific)
        ['resolution_categorization', 'Resolution Categorization', 'Resolution Categorization T2'],
        ['resolution_categorization_tier3', 'Resolution Categorization Tier 3', 'Resolution Category Tier 3'],
        ['sla_resolution_categorization_t1', 'SLA Resolution Categorization T1'],
        ['sla_resolution_category', 'SLA Resolution Category'],
    ]
    
    for variants in field_name_variants:
        value = safe_get(sr_dict, variants, '')
        if value and str(value).strip() and str(value).strip().lower() not in ['nan', 'none', 'n/a', 'na', '']:
            fields.append(str(value).strip())
            break  # Only take first matching variant to avoid duplicates
    
    return ' > '.join(fields) if fields else 'N/A'


def classify_sr_ticket(
    description: str,
    notes: str = "",
    priority: str = "P3",
    workaround_text: str = "",
    interface_likelihood: float = 0.0,
    similar_tickets_count: int = 0,
    direct_to_interface_count: int = 0,
    resolved_with_wa_count: int = 0,
    wa_then_interface_count: int = 0
) -> dict:
    """Classify an SR ticket as Easy Win, Moderate, or Tough based on various factors."""
    combined_text = f"{description} {notes} {workaround_text}".lower()
    
    easy_keywords = [
        'password reset', 'login issue', 'access denied', 'unlock account',
        'refresh data', 'clear cache', 'restart', 'reboot', 'timeout',
        'missing permission', 'sync issue', 'configuration update',
        'user setup', 'enable feature', 'disable feature'
    ]
    
    moderate_keywords = [
        'data mismatch', 'incorrect value', 'calculation error', 'report issue',
        'integration failure', 'api error', 'workflow stuck', 'validation error',
        'batch job failed', 'schedule issue', 'notification missing'
    ]
    
    tough_keywords = [
        'system crash', 'database corruption', 'data loss', 'security breach',
        'performance degradation', 'memory leak', 'deadlock', 'infinite loop',
        'null pointer', 'stack overflow', 'critical failure', 'production down',
        'interface development', 'custom development', 'enhancement', 'new feature'
    ]
    
    easy_matches = sum(1 for kw in easy_keywords if kw in combined_text)
    moderate_matches = sum(1 for kw in moderate_keywords if kw in combined_text)
    tough_matches = sum(1 for kw in tough_keywords if kw in combined_text)
    
    java_failure = 'java' in combined_text and ('exception' in combined_text or 'error' in combined_text or 'failure' in combined_text)
    if java_failure:
        tough_matches += 2
    
    if interface_likelihood > 0.7:
        tough_matches += 2
    elif interface_likelihood > 0.4:
        moderate_matches += 1
    
    if similar_tickets_count > 0:
        if direct_to_interface_count / similar_tickets_count > 0.6:
            tough_matches += 2
        elif resolved_with_wa_count / similar_tickets_count > 0.6:
            easy_matches += 2
    
    total_matches = easy_matches + moderate_matches + tough_matches
    
    if total_matches == 0:
        classification = "Moderate"
        difficulty_score = 3.0
    elif tough_matches >= moderate_matches and tough_matches >= easy_matches:
        classification = "Tough"
        difficulty_score = 4.5 if tough_matches > 3 else 4.0
    elif easy_matches >= moderate_matches:
        classification = "Easy Win"
        difficulty_score = 1.5 if easy_matches > 3 else 2.0
    else:
        classification = "Moderate"
        difficulty_score = 3.0
    
    return {
        'classification': classification,
        'difficulty_score': difficulty_score,
        'easy_matches': easy_matches,
        'moderate_matches': moderate_matches,
        'tough_matches': tough_matches,
        'java_failure_detected': java_failure
    }


def calculate_skill_difficulty_match(skill_level: float, difficulty_score: float) -> float:
    """Calculate a score bonus/penalty based on how well skill level matches SR difficulty."""
    if difficulty_score <= 2.0:
        ideal_skill = 2.0
    elif difficulty_score <= 3.5:
        ideal_skill = 3.0
    else:
        ideal_skill = 4.5
    
    skill_diff = abs(skill_level - ideal_skill)
    
    if skill_diff <= 0.5:
        return 3.0
    elif skill_diff <= 1.0:
        return 1.5
    elif skill_diff <= 1.5:
        return 0.0
    elif skill_diff <= 2.0:
        return -1.5
    else:
        return -3.0


def get_project_root() -> str:
    """Get the project root directory"""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_database_dir() -> str:
    """Get the database directory"""
    return os.path.join(get_project_root(), 'data', 'database')


def get_vectorstore_dir() -> str:
    """Get the vectorstore directory"""
    return os.path.join(get_project_root(), 'data', 'vectorstore')
