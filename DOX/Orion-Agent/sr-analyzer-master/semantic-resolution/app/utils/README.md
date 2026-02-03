# 🛠️ App Utils Module

> **Helper Functions and Utilities**

Common utilities for the Flask application.

---

## 📁 Structure

```
utils/
├── __init__.py
├── README.md
├── helpers.py           # Utility functions
├── decorators.py        # Route decorators
├── state.py             # Shared application state
├── summarize_semantic_wa.py  # Workaround summarization
└── known_workaround_service.py  # Known WA lookup
```

---

## 📦 `helpers.py`

Utility functions:

```python
def safe_get(dict_obj, key, default=""):
    """Safely get value from dictionary."""

def sanitize_for_json(obj):
    """Sanitize object for JSON serialization."""

def concatenate_categorization_fields(row):
    """Combine categorization fields."""
```

---

## 📦 `decorators.py`

Route decorators:

```python
@login_required
def my_route():
    """Require any login."""

@admin_required
def admin_route():
    """Require admin role."""

@user_login_required
def user_route():
    """Require user login."""
```

---

## 📦 `state.py`

Shared application state:

```python
session_data = {}

BASE_DIR = Path(__file__).parent.parent.parent
CHROMADB_PATH = BASE_DIR / "data/vectorstore/chromadb_store"
DATABASE_DIR = BASE_DIR / "data/database"
OUTPUT_DIR = BASE_DIR / "output"
REPORTS_DIR = OUTPUT_DIR / "reports"

def get_feedback_manager():
    """Get or create UserFeedbackManager."""

def get_analyzer():
    """Get or create ComprehensiveSRAnalyzer."""
```

---

## 📦 `summarize_semantic_wa.py`

Workaround summarization:

```python
def summarize_semantic_workarounds(workarounds, max_length=500):
    """Summarize multiple workarounds into one."""
```

---

## 📦 `known_workaround_service.py`

Known workaround lookup:

```python
from app.utils.known_workaround_service import get_known_workaround_service

service = get_known_workaround_service()
result = service.search("network timeout")
```

---

## 🔗 Related

- [app/README.md](../README.md) - Flask application
- [routes/README.md](../routes/README.md) - Routes

---

*Part of SR-Analyzer App Module*
