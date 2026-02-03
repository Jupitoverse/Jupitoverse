# 🌐 App Module

> **Flask Web Application for SR Feedback System**

This module provides the web interface for both admin and user portals.

---

## 🚀 Quick Start

> **See [USER_ADMIN_GUIDE.md](../USER_ADMIN_GUIDE.md) for complete usage instructions**

```bash
# Start application
python app/sr_feedback_app.py
```

**Access Points:**
| Portal | URL | Credentials |
|--------|-----|-------------|
| User Portal | http://localhost:5000/user | None / Azure AD |
| Admin Portal | http://localhost:5000/admin | `admin` / `admin123` |
| Team Skills | http://localhost:5000/team/skill | Admin only |

---

## 📁 Structure

```
app/
├── __init__.py              # Flask app factory
├── sr_feedback_app.py       # Entry point
├── sqlite_fix.py            # SQLite compatibility
├── routes/                  # URL route handlers
│   ├── __init__.py          # Blueprint registration
│   ├── auth.py              # Authentication (368 lines)
│   ├── user.py              # User portal (1064 lines)
│   ├── admin.py             # Admin portal (605 lines)
│   ├── team.py              # Team management (760 lines)
│   └── api.py               # REST API (361 lines)
└── utils/                   # Helper functions
    ├── helpers.py           # Utility functions
    ├── decorators.py        # Route decorators
    ├── state.py             # Shared state
    ├── summarize_semantic_wa.py
    └── known_workaround_service.py
```

---

## 📋 Routes Overview

### Authentication (`/`)

| Route | Description |
|-------|-------------|
| `/` | Login selection page |
| `/admin/login` | Admin login |
| `/user/login` | User login |
| `/azure/login` | Azure AD SSO |

### User Portal (`/user`)

| Route | Description |
|-------|-------------|
| `/user` | Main feedback page |
| `/user/my_srs` | User's assigned SRs |
| `/user/search/<sr_id>` | Search SR |
| `/user/feedback` | Submit correction |

### Admin Portal (`/admin`)

| Route | Description |
|-------|-------------|
| `/admin` | Dashboard |
| `/admin/upload` | Upload Excel |
| `/admin/stats` | Statistics |
| `/admin/download/<file>` | Download report |

### Team Management (`/team`)

| Route | Description |
|-------|-------------|
| `/team/skill` | Skills matrix |
| `/team/people` | Team JSON |
| `/team/people/<name>/availability` | Set availability |

### REST API (`/api`)

| Route | Description |
|-------|-------------|
| `/api/vote/upvote` | Upvote workaround |
| `/api/vote/downvote` | Downvote workaround |
| `/api/regenerate` | Regenerate AI WA |

---

## 🏭 App Factory

```python
# app/__init__.py
from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'sr_feedback_secret_key'
    app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
    
    # Register blueprints
    from app.routes import register_blueprints
    register_blueprints(app)
    
    return app
```

---

## 🔐 Authentication

**Supported Methods:**
- Local admin login (`admin` / `admin123`)
- Local user login
- Azure AD SSO (if configured)

**Decorators:**
```python
@login_required          # Any authenticated user
@admin_required          # Admin only
@user_login_required     # User portal access
```

**Admin Emails:**
Configure via `ADMIN_EMAILS` environment variable or in `auth.py`.

---

## 📂 Key Files

### `sr_feedback_app.py`

Application entry point:
```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### `utils/state.py`

Shared application state:
```python
BASE_DIR = Path(__file__).parent.parent.parent
CHROMADB_PATH = BASE_DIR / "data/vectorstore/chromadb_store"
DATABASE_DIR = BASE_DIR / "data/database"
```

---

## 🔗 Related

- [routes/README.md](routes/README.md) - Route handlers
- [utils/README.md](utils/README.md) - Utilities
- [templates/README.md](../templates/README.md) - HTML templates

---

*Part of SR-Analyzer App Module*
