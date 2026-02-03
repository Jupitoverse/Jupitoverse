#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Workaround Data Handler
Manages loading and searching of historical workaround JSON data

This module is self-contained to avoid merge conflicts.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

# Get the directory where this file is located
MODULE_DIR = Path(__file__).parent.absolute()
DATA_DIR = MODULE_DIR / 'data'


class WorkaroundDataHandler:
    """
    Handles loading and searching of historical workaround data from JSON files.
    
    Expected JSON structure:
    [
        {
            "description": "...",
            "rca": "...",
            "workaround": "...",
            "sr_id": "...",  # optional
            "category": "...",  # optional
            ... other fields
        },
        ...
    ]
    """
    
    def __init__(self, json_file: Optional[str] = None):
        """
        Initialize the data handler.
        
        Args:
            json_file: Path to JSON file. If None, looks for workarounds.json in data folder.
        """
        self.data: List[Dict[str, Any]] = []
        self.json_file = json_file
        self._load_data()
    
    def _load_data(self) -> None:
        """Load workaround data from JSON file."""
        try:
            # Determine file path
            if self.json_file:
                file_path = Path(self.json_file)
            else:
                file_path = DATA_DIR / 'workarounds.json'
            
            if not file_path.exists():
                logger.warning(f"JSON file not found: {file_path}")
                self.data = []
                return
            
            with open(file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            
            logger.info(f"Loaded {len(self.data)} workaround records from {file_path}")
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON file: {e}")
            self.data = []
        except Exception as e:
            logger.error(f"Error loading workaround data: {e}")
            self.data = []
    
    def reload_data(self, json_file: Optional[str] = None) -> None:
        """Reload data from JSON file."""
        if json_file:
            self.json_file = json_file
        self._load_data()
    
    def get_all_workarounds(self) -> List[Dict[str, Any]]:
        """Get all workaround records."""
        return self.data
    
    def search_by_description(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search workarounds by description (case-insensitive substring match).
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of matching workaround records
        """
        if not query or not query.strip():
            return []
        
        query_lower = query.lower().strip()
        results = []
        
        for record in self.data:
            description = record.get('description', '') or ''
            if query_lower in description.lower():
                results.append(record)
                if len(results) >= limit:
                    break
        
        return results
    
    def search_by_rca(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search workarounds by RCA (Root Cause Analysis) - case-insensitive substring match.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of matching workaround records
        """
        if not query or not query.strip():
            return []
        
        query_lower = query.lower().strip()
        results = []
        
        for record in self.data:
            rca = record.get('rca', '') or ''
            if query_lower in rca.lower():
                results.append(record)
                if len(results) >= limit:
                    break
        
        return results
    
    def search_combined(self, description_query: str = '', rca_query: str = '', 
                       limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search workarounds by both description and RCA.
        Records matching both queries (if both provided) are prioritized.
        
        Args:
            description_query: Description search query
            rca_query: RCA search query
            limit: Maximum number of results to return
            
        Returns:
            List of matching workaround records, sorted by relevance
        """
        desc_query = (description_query or '').lower().strip()
        rca_q = (rca_query or '').lower().strip()
        
        if not desc_query and not rca_q:
            return []
        
        exact_matches = []  # Match both
        partial_matches = []  # Match one
        
        for record in self.data:
            description = (record.get('description', '') or '').lower()
            rca = (record.get('rca', '') or '').lower()
            
            desc_match = desc_query and desc_query in description
            rca_match = rca_q and rca_q in rca
            
            if desc_query and rca_q:
                # Both queries provided
                if desc_match and rca_match:
                    exact_matches.append(record)
                elif desc_match or rca_match:
                    partial_matches.append(record)
            else:
                # Only one query provided
                if desc_match or rca_match:
                    exact_matches.append(record)
        
        # Combine results: exact matches first, then partial matches
        results = exact_matches + partial_matches
        return results[:limit]
    
    def get_by_sr_id(self, sr_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific workaround record by SR ID.
        
        Args:
            sr_id: The SR ID to search for
            
        Returns:
            The matching record or None
        """
        if not sr_id:
            return None
        
        sr_id_lower = sr_id.lower().strip()
        for record in self.data:
            record_sr_id = (record.get('sr_id', '') or '').lower()
            if record_sr_id == sr_id_lower:
                return record
        
        return None
    
    def get_unique_categories(self) -> List[str]:
        """Get list of unique categories from the data."""
        categories = set()
        for record in self.data:
            category = record.get('category', '')
            if category:
                categories.add(category)
        return sorted(list(categories))
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the loaded data."""
        return {
            'total_records': len(self.data),
            'unique_categories': len(self.get_unique_categories()),
            'data_loaded': len(self.data) > 0
        }


# Singleton instance for shared access
_handler_instance: Optional[WorkaroundDataHandler] = None


def get_workaround_handler() -> WorkaroundDataHandler:
    """Get or create the singleton WorkaroundDataHandler instance."""
    global _handler_instance
    if _handler_instance is None:
        _handler_instance = WorkaroundDataHandler()
    return _handler_instance

