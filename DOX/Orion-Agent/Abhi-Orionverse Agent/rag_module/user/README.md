# 👤 User Module

> **User Feedback Collection and Management**

This module handles user feedback on AI-generated workarounds, enabling continuous improvement of the system through user corrections.

---

## 📁 Structure

```
user/
├── __init__.py
├── README.md
└── feedback/
    ├── __init__.py
    ├── user_feedback_manager.py    # Main feedback management
    └── README.md
```

---

## 🎯 Purpose

The user module enables:

1. **Feedback Collection**: Users can correct/improve AI-generated workarounds
2. **Workaround Improvement**: User corrections improve future suggestions
3. **Vote Tracking**: Thumbs up/down on workaround usefulness
4. **History Tracking**: All feedback is preserved for ML learning

---

## 📦 Key Component

### `user_feedback_manager.py` - UserFeedbackManager

Manages user feedback on workarounds with persistence and retrieval.

```python
from user.feedback.user_feedback_manager import UserFeedbackManager

manager = UserFeedbackManager()

# Submit feedback
manager.submit_feedback(
    sr_id="CAS123456",
    user_email="user@company.com",
    corrected_workaround="Updated steps: 1. Check logs...",
    rating=5
)

# Get feedback for SR
feedback_list = manager.get_feedback_for_sr("CAS123456")
```

---

## 🔧 Key Methods

### Submit Feedback
```python
def submit_feedback(
    self,
    sr_id: str,
    user_email: str,
    corrected_workaround: str,
    rating: int = None,
    comments: str = None
) -> bool:
    """
    Submit user feedback on a workaround.
    
    Args:
        sr_id: Service Request ID
        user_email: User's email address
        corrected_workaround: User's corrected workaround text
        rating: Optional rating (1-5 stars)
        comments: Optional additional comments
    
    Returns:
        True if feedback saved successfully
    """
```

### Get Feedback
```python
def get_feedback_for_sr(self, sr_id: str) -> List[Dict]:
    """
    Get all feedback entries for a specific SR.
    
    Returns:
        List of feedback dictionaries sorted by date (newest first)
    """

def get_latest_feedback(self, sr_id: str) -> Optional[Dict]:
    """
    Get the most recent feedback for an SR.
    """
```

### Vote on Workaround
```python
def vote_workaround(
    self,
    sr_id: str,
    user_email: str,
    vote: str  # 'up' or 'down'
) -> bool:
    """
    Record a vote on a workaround.
    """
```

### Statistics
```python
def get_feedback_stats(self) -> Dict[str, Any]:
    """
    Get feedback statistics.
    
    Returns:
        {
            'total_feedback': 150,
            'unique_srs': 100,
            'unique_users': 25,
            'avg_rating': 4.2,
            'vote_ratio': 0.85  # up/(up+down)
        }
    """
```

---

## 📊 Feedback Data Structure

### In ChromaDB
User workarounds are stored as JSON array in `user_corrected_workaround` field:

```json
[
    {
        "user": "user1@company.com",
        "wa": "1. Check the logs for errors\n2. Restart service...",
        "date": "2026-01-07T10:30:00"
    },
    {
        "user": "user2@company.com",
        "wa": "Additional step: Verify database connection...",
        "date": "2026-01-08T14:15:00"
    }
]
```

### In SQLite (workaround_feedback.db)
```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY,
    sr_id TEXT NOT NULL,
    user_email TEXT NOT NULL,
    corrected_workaround TEXT,
    original_workaround TEXT,
    rating INTEGER,
    comments TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE votes (
    id INTEGER PRIMARY KEY,
    sr_id TEXT NOT NULL,
    user_email TEXT NOT NULL,
    vote TEXT CHECK(vote IN ('up', 'down')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔄 Integration with ChromaDB

User feedback is integrated into the historical database via `HistoryDatabaseManager`:

```python
from RAG.utils.history_db_manager import HistoryDatabaseManager

manager = HistoryDatabaseManager()

# Add user feedback (appends to existing)
manager.add_user_feedback_entry(
    sr_id="CAS123456",
    user_corrected_workaround="New workaround steps...",
    corrected_by="user@company.com"
)
```

The feedback is:
1. Appended to JSON array (not replaced)
2. Used in 5-source voting for Java detection
3. Available for future semantic search matches

---

## 📈 Feedback Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    USER FEEDBACK FLOW                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   User views SR with AI Workaround                          │
│                    │                                         │
│                    ▼                                         │
│   ┌────────────────────────────────┐                        │
│   │  Is workaround helpful?        │                        │
│   └────────────────┬───────────────┘                        │
│            YES     │     NO                                  │
│         ┌──────────┴──────────┐                             │
│         ▼                     ▼                             │
│   ┌──────────┐         ┌──────────────┐                     │
│   │ Vote Up  │         │ Submit       │                     │
│   │ (👍)     │         │ Correction   │                     │
│   └──────────┘         └──────┬───────┘                     │
│                               │                              │
│                               ▼                              │
│                    ┌──────────────────┐                     │
│                    │ UserFeedbackMgr  │                     │
│                    │ .submit_feedback │                     │
│                    └────────┬─────────┘                     │
│                             │                               │
│              ┌──────────────┴──────────────┐                │
│              ▼                             ▼                │
│   ┌──────────────────┐         ┌──────────────────┐        │
│   │ workaround_      │         │ ChromaDB         │        │
│   │ feedback.db      │         │ (history)        │        │
│   └──────────────────┘         └──────────────────┘        │
│                                                             │
│   Future SR Analysis uses feedback for:                     │
│   • 5-source voting (user workaround vote)                 │
│   • Improved semantic matches                               │
│   • ML learning                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Usage Example

```python
from user.feedback.user_feedback_manager import UserFeedbackManager

# Initialize
manager = UserFeedbackManager()

# Submit user correction
success = manager.submit_feedback(
    sr_id="CAS123456",
    user_email="john.smith@company.com",
    corrected_workaround="""
    1. Check application logs for NullPointerException
    2. Verify ValidateAddress service is running
    3. Restart the OMS process
    4. Clear cache and retry the operation
    """,
    rating=4,
    comments="AI workaround was close but missed the cache clearing step"
)

if success:
    print("Feedback submitted successfully!")

# Get all feedback for an SR
feedback_list = manager.get_feedback_for_sr("CAS123456")
for fb in feedback_list:
    print(f"By: {fb['user_email']}")
    print(f"Correction: {fb['corrected_workaround'][:100]}...")
    print(f"Date: {fb['created_at']}")
    print()

# Get statistics
stats = manager.get_feedback_stats()
print(f"Total feedback: {stats['total_feedback']}")
print(f"Average rating: {stats['avg_rating']:.1f}/5")
```

---

## 📊 Web Interface

Users access feedback through the web portal:

1. Navigate to `http://localhost:5000`
2. Search for SR by ID
3. View AI-generated workaround
4. Click "Provide Feedback" to submit correction
5. Optionally rate the workaround (1-5 stars)
6. Submit feedback

---

## 🔗 Related Modules

- [App](../app/README.md) - Web interface for feedback
- [RAG](../RAG/README.md) - Uses feedback in voting
- [Data](../data/README.md) - Feedback storage

---

*Part of SR-Analyzer User Module*
