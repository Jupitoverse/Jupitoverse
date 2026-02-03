# 🛠️ Flask Utils Module

> **Utility Functions for Web Application**

This folder contains utility functions used by the Flask web application.

---

## 📁 Structure

```
utils/
├── README.md
├── __init__.py
├── file_handler.py       # File upload handling
├── response_helper.py    # JSON response formatting
├── validators.py         # Input validation
└── session_manager.py    # Session utilities
```

---

## 📦 Utility Files

### `file_handler.py`

Handles file upload validation and storage.

```python
from app.utils.file_handler import save_upload, validate_excel

# Validate Excel file
is_valid, error = validate_excel(file)
if not is_valid:
    return error

# Save upload with unique name
filepath = save_upload(file, upload_dir="input/")
```

**Functions:**

```python
def validate_excel(file) -> Tuple[bool, Optional[str]]:
    """Validate uploaded Excel file."""
    
def save_upload(file, upload_dir: str) -> str:
    """Save uploaded file with timestamp."""
    
def cleanup_old_uploads(upload_dir: str, max_age_days: int = 7):
    """Remove old upload files."""
```

### `response_helper.py`

Standardizes JSON responses.

```python
from app.utils.response_helper import success_response, error_response

# Success response
return success_response(
    data={'sr_id': 'CAS123'},
    message='SR processed successfully'
)

# Error response
return error_response(
    error='Invalid file format',
    code='INVALID_FORMAT',
    status=400
)
```

**Functions:**

```python
def success_response(data=None, message=None) -> Response:
    """Create standardized success response."""
    
def error_response(error: str, code: str = None, status: int = 400) -> Response:
    """Create standardized error response."""
    
def paginated_response(data: list, page: int, per_page: int, total: int) -> Response:
    """Create paginated response."""
```

### `validators.py`

Input validation utilities.

```python
from app.utils.validators import validate_sr_id, validate_workaround

# Validate SR ID format
if not validate_sr_id(sr_id):
    return error_response('Invalid SR ID format')

# Validate workaround text
is_valid, cleaned = validate_workaround(workaround_text)
```

**Functions:**

```python
def validate_sr_id(sr_id: str) -> bool:
    """Validate SR ID format (e.g., CAS123456)."""
    
def validate_workaround(text: str) -> Tuple[bool, str]:
    """Validate and clean workaround text."""
    
def validate_priority(priority: str) -> bool:
    """Validate priority format (P1-P4)."""
    
def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent XSS."""
```

### `session_manager.py`

Session management utilities.

```python
from app.utils.session_manager import get_current_user, is_admin

# Get current user
user = get_current_user()
print(user['email'], user['role'])

# Check admin status
if is_admin():
    # Show admin features
    pass
```

**Functions:**

```python
def get_current_user() -> Optional[Dict]:
    """Get current user from session."""
    
def is_admin() -> bool:
    """Check if current user is admin."""
    
def set_user_session(user_data: Dict):
    """Set user data in session."""
    
def clear_session():
    """Clear user session."""
```

---

## 🔧 Usage in Routes

```python
from flask import Blueprint
from app.utils.file_handler import save_upload, validate_excel
from app.utils.response_helper import success_response, error_response
from app.utils.validators import validate_sr_id

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    
    # Validate
    is_valid, error = validate_excel(file)
    if not is_valid:
        return error_response(error)
    
    # Save
    filepath = save_upload(file)
    
    # Process
    result = process_file(filepath)
    
    return success_response(data=result)
```

---

*Part of SR-Analyzer Flask App Module*
