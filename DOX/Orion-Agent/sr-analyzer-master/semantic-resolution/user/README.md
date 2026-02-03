# 👤 User Module

> **User Feedback Collection and Management**

Handles user feedback on AI-generated workarounds.

---

## 📁 Structure

```
user/
├── __init__.py
├── README.md
└── feedback/
    ├── __init__.py
    ├── user_feedback_manager.py    # Feedback management
    └── README.md
```

---

## 🎯 Purpose

1. **Collect Feedback** - Users correct AI workarounds
2. **Improve System** - Corrections improve future suggestions
3. **Track Votes** - Thumbs up/down on usefulness
4. **History Tracking** - All feedback preserved for ML

---

## 📦 `user_feedback_manager.py`

### Class: `UserFeedbackManager`

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

# Vote
manager.vote_workaround("CAS123456", "user@company.com", "up")

# Statistics
stats = manager.get_feedback_stats()
```

---

## 📊 Feedback Storage

### In ChromaDB

User workarounds stored as JSON array in `user_corrected_workaround`:

```json
[
  {
    "user": "user@company.com",
    "wa": "1. Check logs\n2. Restart service...",
    "date": "2026-01-07T10:30:00"
  }
]
```

### In SQLite (`workaround_feedback.db`)

```sql
CREATE TABLE feedback (
    sr_id TEXT,
    user_email TEXT,
    corrected_workaround TEXT,
    rating INTEGER,
    created_at DATETIME
);

CREATE TABLE votes (
    sr_id TEXT,
    user_email TEXT,
    vote TEXT CHECK(vote IN ('up', 'down'))
);
```

---

## 🔄 Feedback Flow

```
User views SR with AI Workaround
         │
         ▼
   Is workaround helpful?
    YES     │     NO
    ▼               ▼
 Vote Up     Submit Correction
 (👍)              │
                    ▼
           UserFeedbackManager
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
   workaround_        ChromaDB
   feedback.db       (history)
                          │
                          ▼
              Future SR Analysis uses
              feedback in 5-source voting
```

---

## 🔗 Related

- [app/README.md](../app/README.md) - Web interface
- [RAG/README.md](../RAG/README.md) - Uses feedback in voting

---

*Part of SR-Analyzer User Module*
