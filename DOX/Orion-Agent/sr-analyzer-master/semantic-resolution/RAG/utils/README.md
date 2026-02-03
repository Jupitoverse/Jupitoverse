# 🛠️ RAG Utils Module

> **Utility Scripts for RAG Pipeline**

---

## 📁 Structure

```
utils/
├── README.md
├── __init__.py
├── history_db_manager.py     # ChromaDB management (main)
├── chromadb_manager.py       # ChromaDB utilities
└── feedback_storage.py       # Feedback persistence
```

---

## 📦 `history_db_manager.py`

### Class: `HistoryDatabaseManager`

Manages ChromaDB vectorstore for SR history data.

```python
from RAG.utils.history_db_manager import HistoryDatabaseManager

manager = HistoryDatabaseManager(chromadb_path="data/vectorstore/chromadb_store")

# Search
results = manager.search_semantic("network issue", top_k=5)

# Add/Update SR
manager.add_user_feedback_entry(
    sr_id="CAS123456",
    description="Network timeout...",
    ai_generated_workaround="Check connectivity..."
)

# Get statistics
stats = manager.get_statistics()
print(f"Records: {stats['total_records']}")
```

### Key Methods

| Method | Description |
|--------|-------------|
| `add_user_feedback_entry()` | Add or update SR entry |
| `update_sr_from_admin()` | Update from admin upload |
| `get_all_user_feedback_for_sr()` | Get feedback for SR |
| `get_statistics()` | Get database stats |

### User Workaround JSON Format

User workarounds are stored as JSON array:

```json
[
  {
    "user": "user@company.com",
    "wa": "1. Check logs...",
    "date": "2026-01-07T10:30:00"
  }
]
```

---

## 📦 `chromadb_manager.py`

ChromaDB connection and collection utilities.

---

## 📦 `feedback_storage.py`

Feedback persistence utilities.

---

## 🔗 Related

- [RAG/README.md](../README.md) - RAG module overview
- [data/README.md](../../data/README.md) - Data storage

---

*Part of SR-Analyzer RAG Module*
