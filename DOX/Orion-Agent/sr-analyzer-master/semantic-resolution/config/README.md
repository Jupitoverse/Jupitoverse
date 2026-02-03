# ⚙️ Config Module

> **Configuration Settings and Path Constants**

Centralizes all configuration settings.

---

## 📁 Structure

```
config/
├── __init__.py
├── README.md
├── settings.py          # Application settings
├── paths.py             # Path constants
├── azure_ad.py          # Azure AD config
└── email_config.json    # Email settings
```

---

## 📦 `settings.py`

Application settings:

```python
# Flask
FLASK_DEBUG = True
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000
SECRET_KEY = 'sr-feedback-secret-key'

# Upload
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

# Models
SENTENCE_TRANSFORMER_MODEL = 'all-MiniLM-L6-v2'

# LLM API
LLM_API_URL = 'https://ai-framework1:8085/api/v1/call_llm'
LLM_MODEL_NAME = 'gpt-4.1'

# Search
SEMANTIC_SEARCH_TOP_K = 10
SIMILARITY_THRESHOLD = 0.55
```

---

## 📦 `paths.py`

Path constants:

```python
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# Data
DATA_DIR = BASE_DIR / "data"
DB_DIR = DATA_DIR / "database"
VECTORSTORE_DIR = DATA_DIR / "vectorstore"
CHROMADB_STORE = VECTORSTORE_DIR / "chromadb_store"

# Databases
PEOPLE_SKILLS_DB = DB_DIR / "people_skills.db"
ABBREVIATION_DB = DB_DIR / "abbreviation.db"

# Tokens
TOKENS_FILE = BASE_DIR / "tokens" / "Tokens.xlsx"

# RAG
RAG_INPUT_DIR = BASE_DIR / "RAG" / "input"
RAG_OUTPUT_DIR = BASE_DIR / "RAG" / "llm output"
```

---

## 🔧 Usage

```python
from config.settings import FLASK_PORT, LLM_API_URL
from config.paths import CHROMADB_STORE, PEOPLE_SKILLS_DB

# Flask config
app.config['SECRET_KEY'] = SECRET_KEY

# Database connection
import chromadb
client = chromadb.PersistentClient(path=str(CHROMADB_STORE))
```

---

## 🔗 Related

- [app/README.md](../app/README.md) - Uses Flask settings
- [RAG/README.md](../RAG/README.md) - Uses LLM settings

---

*Part of SR-Analyzer Config Module*
