# 🛠️ RAG/utils Module

> **Utility Scripts for RAG Pipeline**

This folder contains utility classes and functions that support the main RAG pipeline.

---

## 📁 Structure

```
utils/
├── README.md
└── history_db_manager.py     # ChromaDB management
```

---

## 📦 Main File: `history_db_manager.py`

### Class: `HistoryDatabaseManager`

Manages ChromaDB vectorstore for SR history data with support for:
- Semantic search using sentence transformers
- Adding/updating SR entries
- User feedback integration
- Duplicate prevention

```python
from RAG.utils.history_db_manager import HistoryDatabaseManager

manager = HistoryDatabaseManager(chromadb_path="data/vectorstore/chromadb_store")

# Search historical SRs
results = manager.search_semantic("network connectivity issue", top_k=5)

# Add new SR entry
manager.add_user_feedback_entry(
    sr_id="CAS123456",
    description="Network timeout...",
    ai_generated_workaround="Check connectivity..."
)

# Update existing SR
manager.update_sr_from_admin(
    sr_id="CAS123456",
    ai_generated_workaround="Updated workaround...",
    preserve_user_feedback=True
)
```

---

## 🔧 Key Methods

### Initialization
```python
def __init__(self, db_path=None, chromadb_path=None):
    """
    Initialize the manager.
    
    Args:
        db_path: Legacy parameter (ignored)
        chromadb_path: Path to ChromaDB store
        
    Connects to ChromaDB and loads sentence transformer model.
    """
```

### Adding/Updating Entries
```python
def add_user_feedback_entry(
    self,
    sr_id: str,
    description: str = "",
    notes: str = "",
    user_corrected_workaround: str = "",
    ai_generated_workaround: str = "NA",
    priority: str = "User Feedback",
    **additional_fields
) -> bool:
    """
    Add or update an entry in the history database.
    
    BEHAVIOR:
    - If SR exists: UPDATE (prevents duplicates)
    - If SR doesn't exist: ADD new record
    - User workarounds stored as JSON array (supports multiple)
    """
```

```python
def update_sr_from_admin(
    self,
    sr_id: str,
    ai_generated_workaround: str = None,
    description: str = None,
    notes: str = None,
    preserve_user_feedback: bool = True,
    **additional_fields
) -> bool:
    """
    Update existing SR with new data from admin upload.
    
    IMPORTANT: Preserves user_corrected_workaround if preserve_user_feedback=True
    """
```

### Updating Workarounds
```python
def update_workaround(self, sr_id: str, user_corrected_workaround: str) -> bool:
    """Update user_corrected_workaround for an existing entry."""

def update_ai_workaround(self, sr_id: str, new_ai_workaround: str) -> bool:
    """Update ai_generated_workaround when user approves regenerated workaround."""
```

### Querying
```python
def get_all_user_feedback_for_sr(self, sr_id: str) -> List[Dict]:
    """
    Get ALL user feedback entries for a specific SR.
    Parses JSON user_corrected_workaround field.
    Returns list sorted by date (newest first).
    """

def get_statistics(self) -> Dict[str, Any]:
    """
    Get database statistics.
    
    Returns:
        {
            'total_records': 1180000,
            'user_feedback_count': 500,
            'columns': [...],
            'model_name': 'all-MiniLM-L6-v2',
            'storage': 'ChromaDB'
        }
    """
```

---

## 📊 User Workaround JSON Format

User workarounds are stored as JSON array to support multiple corrections:

```json
[
    {
        "user": "user1@company.com",
        "wa": "1. Check logs\n2. Restart service...",
        "date": "2026-01-07T10:30:00"
    },
    {
        "user": "user2@company.com",
        "wa": "Additional step: Clear cache...",
        "date": "2026-01-08T14:15:00"
    }
]
```

### Appending New Workaround
```python
def _append_user_workaround(self, existing_wa_json: str, new_wa: str, user: str) -> str:
    """
    Append new user workaround to JSON history array.
    Handles both JSON format and legacy plain text.
    """
```

### Getting Latest Workaround
```python
def _get_latest_user_workaround(self, wa_json: str) -> Dict[str, str]:
    """
    Get the latest user workaround from JSON array.
    Returns: {'user': '...', 'wa': '...', 'date': '...'}
    """
```

---

## 🔍 ChromaDB Integration

### Collection: `clean_history_data`

Metadata fields stored:

| Field | Description |
|-------|-------------|
| call_id | SR ID (uppercase) |
| description | SR description |
| wl_summary | Notes/summary |
| workaround | Original workaround |
| ai_generated_workaround | RAG-generated |
| user_corrected_workaround | JSON array |
| resolution_categorization | Category |
| application | App area |
| assigned_to | Team member |
| priority | P1-P4 |
| source | admin_upload or user_feedback |

### Embedding Model
- Model: `all-MiniLM-L6-v2`
- Dimensions: 384
- Device: CPU (to avoid GPU errors)

---

## 🔧 Usage Example

```python
from RAG.utils.history_db_manager import HistoryDatabaseManager

# Initialize
manager = HistoryDatabaseManager()

# Check statistics
stats = manager.get_statistics()
print(f"Total records: {stats['total_records']}")

# Add new SR from admin upload
manager.add_user_feedback_entry(
    sr_id="CAS123456",
    description="Network connectivity issue",
    notes="Customer reports timeout",
    ai_generated_workaround="1. Check network settings...",
    priority="P2",
    application="SOM_MM",
    assigned_to="John Smith"
)

# Add user feedback
manager.add_user_feedback_entry(
    sr_id="CAS123456",
    user_corrected_workaround="Add step: Verify firewall rules",
    corrected_by="user@company.com"
)

# Get all feedback for SR
feedback_list = manager.get_all_user_feedback_for_sr("CAS123456")
for fb in feedback_list:
    print(f"By: {fb['corrected_by']}")
    print(f"Correction: {fb['user_corrected_workaround'][:100]}")
```

---

## 🔗 Related

- [RAG/README.md](../README.md) - RAG module overview
- [Data/README.md](../../data/README.md) - Data storage

---

*Part of SR-Analyzer RAG Utils Module*
