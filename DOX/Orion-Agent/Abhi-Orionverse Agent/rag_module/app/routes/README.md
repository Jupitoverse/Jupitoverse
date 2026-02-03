# 🌐 Flask Routes Module

> **API Endpoints and Web Routes**

This folder contains Flask Blueprint route handlers for the web application.

---

## 📁 Structure

```
routes/
├── README.md
├── __init__.py             # Blueprint exports
├── auth.py                 # Authentication routes
├── user.py                 # User-facing routes
├── admin.py                # Admin routes
├── team.py                 # Team management routes
└── api.py                  # REST API endpoints
```

---

## 📦 Route Files

### `auth.py` - Authentication Blueprint

Handles user login, logout, and session management.

```python
# Routes
POST /auth/login      # User login
POST /auth/logout     # User logout
GET  /auth/status     # Check session status
```

### `user.py` - User Blueprint

User-facing routes for feedback and workaround viewing.

```python
# Routes
GET  /user/                   # User dashboard
GET  /user/search             # Search SRs
POST /user/feedback/<sr_id>   # Submit workaround feedback
GET  /user/history            # View submitted feedback
GET  /user/sr/<sr_id>         # View SR details
```

### `admin.py` - Admin Blueprint

Admin routes for uploading, processing, and management.

```python
# Routes
GET  /admin/                  # Admin dashboard
POST /admin/upload            # Upload Excel file
GET  /admin/status            # Processing status
POST /admin/reprocess/<sr_id> # Reprocess single SR
GET  /admin/statistics        # Database statistics
GET  /admin/export            # Export data
POST /admin/rebuild-index     # Rebuild vector index
```

### `team.py` - Team Blueprint

Team management routes.

```python
# Routes
GET  /team/                   # Team overview
GET  /team/members            # List members
POST /team/update             # Update team config
GET  /team/workload           # View workload
GET  /team/assignments        # Daily assignments
```

### `api.py` - REST API Blueprint

Programmatic API endpoints.

```python
# Routes
GET  /api/v1/search           # Semantic search
POST /api/v1/analyze          # Analyze single SR
GET  /api/v1/sr/<sr_id>       # Get SR details
PUT  /api/v1/workaround       # Update workaround
GET  /api/v1/team/skills      # Get team skills
POST /api/v1/assignment       # Generate assignment
```

---

## 🔧 Blueprint Registration

In `app/__init__.py`:

```python
from flask import Flask
from app.routes.auth import auth_bp
from app.routes.user import user_bp
from app.routes.admin import admin_bp
from app.routes.team import team_bp
from app.routes.api import api_bp

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(team_bp, url_prefix='/team')
    app.register_blueprint(api_bp, url_prefix='/api/v1')
    
    return app
```

---

## 📋 Admin Upload Endpoint

The main upload endpoint in `admin.py`:

```python
@admin_bp.route('/upload', methods=['POST'])
def upload_excel():
    """
    Handle Excel file upload and trigger RAG processing.
    
    Form Data:
        file: Excel file (.xls, .xlsx)
        
    Returns:
        JSON with processing status and results
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    # Validate file
    if not file.filename.endswith(('.xls', '.xlsx')):
        return jsonify({'error': 'Invalid file format'}), 400
    
    # Save and process
    filepath = save_upload(file)
    result = upload_and_merge_with_rag(filepath)
    
    return jsonify(result)
```

---

## 📋 User Feedback Endpoint

In `user.py`:

```python
@user_bp.route('/feedback/<sr_id>', methods=['POST'])
def submit_feedback(sr_id):
    """
    Submit user workaround feedback.
    
    Form Data:
        workaround: User's corrected workaround text
        
    Updates ChromaDB with user feedback.
    """
    data = request.form
    workaround = data.get('workaround', '').strip()
    
    if not workaround:
        return jsonify({'error': 'Workaround required'}), 400
    
    # Add to history
    manager = HistoryDatabaseManager()
    manager.add_user_feedback_entry(
        sr_id=sr_id,
        user_corrected_workaround=workaround,
        corrected_by=session.get('user_email')
    )
    
    return jsonify({'success': True})
```

---

## 🔐 Authentication

Routes are protected using decorators:

```python
from functools import wraps
from flask import session, redirect

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return redirect('/auth/login')
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            return jsonify({'error': 'Admin required'}), 403
        return f(*args, **kwargs)
    return decorated
```

---

## 📊 API Response Format

Standard JSON response format:

```json
{
    "success": true,
    "data": {...},
    "message": "Operation completed",
    "timestamp": "2026-01-07T10:30:00Z"
}
```

Error response:

```json
{
    "success": false,
    "error": "Error message",
    "code": "ERROR_CODE"
}
```

---

*Part of SR-Analyzer Flask App Module*
