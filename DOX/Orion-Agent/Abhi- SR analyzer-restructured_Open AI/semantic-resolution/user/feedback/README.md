# 💬 User Feedback Module

> **User Workaround Correction System**

This folder contains the feedback management system that allows users to correct AI-generated workarounds.

---

## 📁 Structure

```
feedback/
├── README.md
└── user_feedback_manager.py     # Main feedback manager
```

---

## 📦 Main File: `user_feedback_manager.py`

### Class: `UserFeedbackManager`

Manages user workaround corrections and feedback history.

```python
from user.feedback.user_feedback_manager import UserFeedbackManager

manager = UserFeedbackManager()

# Submit user feedback
manager.submit_feedback(
    sr_id="CAS123456",
    user_workaround="1. Check logs\n2. Restart service...",
    user_email="user@company.com"
)

# Get feedback for SR
feedback_list = manager.get_feedback_for_sr("CAS123456")

# Get user's feedback history
history = manager.get_user_history("user@company.com")
```

---

## 🔧 Key Methods

### Submit Feedback

```python
def submit_feedback(
    self,
    sr_id: str,
    user_workaround: str,
    user_email: str,
    additional_notes: str = None
) -> bool:
    """
    Submit user's workaround correction.
    
    Args:
        sr_id: Service Request ID
        user_workaround: Corrected workaround text
        user_email: User's email address
        additional_notes: Optional notes
        
    Returns:
        True if successful
        
    Updates ChromaDB with user feedback.
    Supports multiple corrections per SR.
    """
```

### Get Feedback for SR

```python
def get_feedback_for_sr(self, sr_id: str) -> List[Dict]:
    """
    Get all user feedback for a specific SR.
    
    Returns list of:
    {
        'user': 'user@company.com',
        'workaround': '1. Check logs...',
        'date': '2026-01-07T10:30:00',
        'notes': 'Additional context'
    }
    """
```

### Get User History

```python
def get_user_history(
    self,
    user_email: str,
    limit: int = 50
) -> List[Dict]:
    """
    Get feedback history for a specific user.
    
    Returns list of:
    {
        'sr_id': 'CAS123456',
        'workaround': '...',
        'date': '...',
        'status': 'applied'  # or 'pending'
    }
    """
```

### Approve AI Regeneration

```python
def approve_regenerated_workaround(
    self,
    sr_id: str,
    user_email: str
) -> bool:
    """
    Approve a regenerated AI workaround.
    Updates ai_generated_workaround field.
    """
```

---

## 📊 Feedback Storage

Feedback is stored in ChromaDB as JSON array:

```json
{
    "user_corrected_workaround": [
        {
            "user": "user1@company.com",
            "wa": "1. Check database connection\n2. Restart service",
            "date": "2026-01-07T10:30:00"
        },
        {
            "user": "user2@company.com",
            "wa": "Add step: Clear cache first",
            "date": "2026-01-08T14:15:00"
        }
    ]
}
```

---

## 🔄 Feedback Flow

```
1. User views AI workaround
2. User submits correction
3. Correction stored in ChromaDB
4. Next RAG run considers user feedback
5. Improved workarounds generated
```

---

## 📋 Integration

### With ChromaDB

```python
from RAG.utils.history_db_manager import HistoryDatabaseManager

class UserFeedbackManager:
    def __init__(self):
        self.history_db = HistoryDatabaseManager()
    
    def submit_feedback(self, sr_id, user_workaround, user_email):
        return self.history_db.add_user_feedback_entry(
            sr_id=sr_id,
            user_corrected_workaround=user_workaround,
            corrected_by=user_email
        )
```

### With Flask Routes

```python
@user_bp.route('/feedback/<sr_id>', methods=['POST'])
def submit_feedback(sr_id):
    manager = UserFeedbackManager()
    manager.submit_feedback(
        sr_id=sr_id,
        user_workaround=request.form['workaround'],
        user_email=session['user_email']
    )
    return jsonify({'success': True})
```

---

## 🔗 Related

- [User/README.md](../README.md) - User module overview
- [RAG/utils/README.md](../../RAG/utils/README.md) - History database

---

*Part of SR-Analyzer User Module*
