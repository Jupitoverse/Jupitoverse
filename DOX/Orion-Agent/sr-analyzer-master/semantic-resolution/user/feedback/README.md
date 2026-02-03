# 💬 User Feedback Module

> **Feedback Collection and Storage**

Manages user feedback on AI workarounds.

---

## 📁 Structure

```
feedback/
├── __init__.py
├── README.md
└── user_feedback_manager.py    # UserFeedbackManager class
```

---

## 📦 `user_feedback_manager.py`

### Class: `UserFeedbackManager`

```python
from user.feedback.user_feedback_manager import UserFeedbackManager

manager = UserFeedbackManager()

# Submit correction
manager.submit_feedback(
    sr_id="CAS123456",
    user_email="user@company.com",
    corrected_workaround="1. Check logs\n2. Restart...",
    rating=5
)

# Vote
manager.vote_workaround("CAS123456", "user@company.com", "up")

# Get feedback
feedback = manager.get_feedback_for_sr("CAS123456")

# Statistics
stats = manager.get_feedback_stats()
```

---

## 🔄 Integration

User feedback is used in:

1. **5-Source Voting** - User workarounds as Source 4
2. **Future Searches** - Improved semantic matches
3. **ML Learning** - Pattern recognition

---

## 🔗 Related

- [user/README.md](../README.md) - User module
- [RAG/README.md](../../RAG/README.md) - Uses in voting

---

*Part of SR-Analyzer User Module*
