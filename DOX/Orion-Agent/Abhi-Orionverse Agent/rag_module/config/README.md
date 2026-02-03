# ⚙️ Config Module

> **Configuration Settings and Path Constants**

This module centralizes all configuration settings and path constants used throughout the SR-Analyzer application.

---

## 📁 Structure

```
config/
├── __init__.py
├── README.md
├── settings.py          # Application settings
└── paths.py             # Path constants
```

---

## 📦 Files

### `settings.py` - Application Settings

Contains Flask and application configuration:

```python
# Flask Settings
FLASK_DEBUG = True
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
SECRET_KEY = 'sr-feedback-secret-key'

# Session Settings
SESSION_TYPE = 'filesystem'
PERMANENT_SESSION_LIFETIME = timedelta(hours=8)

# Upload Settings
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

# Model Settings
SENTENCE_TRANSFORMER_MODEL = 'all-MiniLM-L6-v2'

# LLM API Settings
LLM_API_URL = 'https://ai-framework1:8085/api/v1/call_llm'
LLM_MODEL_NAME = 'gpt-4.1'
LLM_TEMPERATURE = 0.2

# Search Settings
SEMANTIC_SEARCH_TOP_K = 10
SIMILARITY_THRESHOLD = 0.55
```

**Usage:**
```python
from config.settings import FLASK_PORT, SECRET_KEY, LLM_API_URL

app.config['SECRET_KEY'] = SECRET_KEY
```

---

### `paths.py` - Path Constants

Centralized path definitions for all data files:

```python
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
```

**Usage:**
```python
from config.paths import CHROMADB_STORE, PEOPLE_SKILLS_DB

# Use paths
client = chromadb.PersistentClient(path=str(CHROMADB_STORE))
conn = sqlite3.connect(str(PEOPLE_SKILLS_DB))
```

**Helper Functions:**
```python
def ensure_directories():
    """Create all required directories if they don't exist"""
    dirs = [
        DATA_DIR, DB_DIR, VECTORSTORE_DIR, UPLOADS_DIR,
        OUTPUT_DIR, REPORTS_DIR, EXPORTS_DIR, DAILY_ASSIGNMENTS_DIR,
        BACKUP_DIR, TOKENS_DIR, RAG_INPUT_DIR, RAG_OUTPUT_DIR
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

def get_path_str(path: Path) -> str:
    """Convert Path to string for backward compatibility"""
    return str(path)
```

---

## 📊 Directory Layout

```
semantic-resolution/
├── config/
│   ├── settings.py
│   └── paths.py
├── data/
│   ├── db/                    → DB_DIR
│   │   ├── *.db               → Database files
│   │   └── *.json             → JSON configs
│   ├── vectorstore/           → VECTORSTORE_DIR
│   │   └── chromadb_store/    → CHROMADB_STORE
│   ├── uploads/               → UPLOADS_DIR
│   ├── output/                → OUTPUT_DIR
│   │   ├── reports/           → REPORTS_DIR
│   │   ├── exports/           → EXPORTS_DIR
│   │   └── daily_assignments/ → DAILY_ASSIGNMENTS_DIR
│   └── backup/                → BACKUP_DIR
├── tokens/                    → TOKENS_DIR
│   └── Tokens.xlsx            → TOKENS_FILE
├── models/                    → MODELS_DIR
├── templates/                 → TEMPLATES_DIR
└── RAG/
    ├── input/                 → RAG_INPUT_DIR
    └── llm output/            → RAG_OUTPUT_DIR
```

---

## 🔧 Configuration Patterns

### Loading Configuration
```python
# In application initialization
from config.settings import *
from config.paths import ensure_directories

ensure_directories()

app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
```

### Environment Overrides
```python
import os
from config.settings import FLASK_PORT

# Allow environment override
port = int(os.environ.get('SR_PORT', FLASK_PORT))
```

### Path Usage
```python
from config.paths import PEOPLE_SKILLS_DB, CHROMADB_STORE

# Always use Path objects for cross-platform compatibility
db_path = PEOPLE_SKILLS_DB  # Path object
db_path_str = str(PEOPLE_SKILLS_DB)  # String for sqlite3.connect()
```

---

## 🔗 Related Modules

- [App](../app/README.md) - Uses Flask settings
- [RAG](../RAG/README.md) - Uses LLM settings
- [Data](../data/README.md) - Uses path constants

---

*Part of SR-Analyzer Config Module*
