"""
Path Configuration
Central location for all path constants used across the application
"""

import os
from pathlib import Path

# Base directory (semantic-resolution folder)
BASE_DIR = Path(__file__).parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
DB_DIR = DATA_DIR / "db"
VECTORSTORE_DIR = DATA_DIR / "vectorstore"
UPLOADS_DIR = DATA_DIR / "uploads"
OUTPUT_DIR = DATA_DIR / "output"
REPORTS_DIR = OUTPUT_DIR / "reports"
EXPORTS_DIR = OUTPUT_DIR / "exports"
DAILY_ASSIGNMENTS_DIR = OUTPUT_DIR / "daily_assignments"
BACKUP_DIR = DATA_DIR / "backup"

# Database files
CLEAN_HISTORY_DB = DB_DIR / "clean_history_data.db"
JAVA_MAPPING_DB = DB_DIR / "javaMapping.db"
PEOPLE_SKILLS_DB = DB_DIR / "people_skills.db"
SR_TRACKING_DB = DB_DIR / "sr_tracking.db"
ABBREVIATION_DB = DB_DIR / "abbreviation.db"
WORKAROUND_FEEDBACK_DB = DB_DIR / "workaround_feedback.db"
LLM_USAGE_STATS = DB_DIR / "llm_usage_stats.json"

# Vectorstore paths
CHROMADB_STORE = VECTORSTORE_DIR / "chromadb_store"
COMCAST_CODE_DB = VECTORSTORE_DIR / "comcast_code.db"

# Other paths
TOKENS_DIR = BASE_DIR / "tokens"
TOKENS_FILE = TOKENS_DIR / "Tokens.xlsx"
MODELS_DIR = BASE_DIR / "models"
TEMPLATES_DIR = BASE_DIR / "templates"

# RAG paths
RAG_DIR = BASE_DIR / "rag"
RAG_INPUT_DIR = BASE_DIR / "RAG" / "input"
RAG_OUTPUT_DIR = BASE_DIR / "RAG" / "llm output"


def ensure_directories():
    """Create all required directories if they don't exist"""
    dirs = [
        DATA_DIR, DB_DIR, VECTORSTORE_DIR, UPLOADS_DIR, 
        OUTPUT_DIR, REPORTS_DIR, EXPORTS_DIR, DAILY_ASSIGNMENTS_DIR,
        BACKUP_DIR, TOKENS_DIR, RAG_INPUT_DIR, RAG_OUTPUT_DIR
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


# String versions for backward compatibility
def get_path_str(path: Path) -> str:
    """Convert Path to string"""
    return str(path)

