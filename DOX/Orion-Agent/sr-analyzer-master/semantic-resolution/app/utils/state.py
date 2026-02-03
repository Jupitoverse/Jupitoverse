#!/usr/bin/env python3
"""
Shared Application State
Manages shared state across blueprints
"""

import os
import sys
from pathlib import Path

# Project paths
FLASK_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(FLASK_APP_DIR)

# Add to path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Directory paths
DATABASE_DIR = os.path.join(PROJECT_ROOT, 'data', 'database')
VECTORSTORE_DIR = os.path.join(PROJECT_ROOT, 'data', 'vectorstore')
VECTOR_STORE_DIR = VECTORSTORE_DIR  # ChromaDB and vectorstore files
CHROMADB_PATH = os.path.join(VECTORSTORE_DIR, 'chromadb_store')  # ChromaDB store path
TOKENS_DIR = os.path.join(PROJECT_ROOT, 'tokens')
INPUT_DIR = os.path.join(PROJECT_ROOT, 'input')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')
REPORTS_DIR = os.path.join(OUTPUT_DIR, 'reports')
UPLOADS_DIR = INPUT_DIR
BASE_DIR = PROJECT_ROOT

# Session data storage
session_data = {
    'uploaded_file': None,
    'analyzed_data': None,
    'original_df': None
}

# Initialize managers lazily
_feedback_manager = None
_analyzer = None
_age_calculator = None
_feedback_storage = None


def get_feedback_manager():
    """Get or initialize feedback manager"""
    global _feedback_manager
    if _feedback_manager is None:
        try:
            from user.feedback.user_feedback_manager import UserFeedbackManager
            _feedback_manager = UserFeedbackManager()
        except Exception as e:
            print(f"[WARN] Could not initialize feedback manager: {e}")
    return _feedback_manager


def get_analyzer():
    """Get or initialize SR analyzer"""
    global _analyzer
    if _analyzer is None:
        try:
            from analyzers.comprehensive_sr_analyzer import ComprehensiveSRAnalyzer
            _analyzer = ComprehensiveSRAnalyzer()
        except Exception as e:
            print(f"[WARN] Could not initialize analyzer: {e}")
    return _analyzer


def get_age_calculator():
    """Get or initialize age calculator"""
    global _age_calculator
    if _age_calculator is None:
        try:
            from assignment.priority_age_calculator import PriorityAgeCalculator
            _age_calculator = PriorityAgeCalculator()
            print("[OK] Priority age calculator initialized")
        except Exception as e:
            print(f"[WARN] Priority age calculator not available: {e}")
    return _age_calculator


def get_feedback_storage():
    """Get or initialize feedback storage"""
    global _feedback_storage
    if _feedback_storage is None:
        try:
            from RAG.utils.feedback_storage import WorkaroundFeedbackStorage
            _feedback_storage = WorkaroundFeedbackStorage()
            print("[OK] Workaround feedback storage initialized")
        except Exception as e:
            print(f"[WARN] Could not initialize feedback storage: {e}")
    return _feedback_storage


