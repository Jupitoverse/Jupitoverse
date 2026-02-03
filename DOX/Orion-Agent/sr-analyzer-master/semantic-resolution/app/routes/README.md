# 🛣️ Routes Module

> **Flask Blueprint Route Handlers**

URL route handlers organized as Flask Blueprints.

---

## 📁 Structure

```
routes/
├── __init__.py      # Blueprint registration
├── README.md
├── auth.py          # Authentication (368 lines)
├── user.py          # User portal (1064 lines)
├── admin.py         # Admin portal (605 lines)
├── team.py          # Team management (760 lines)
└── api.py           # REST API (361 lines)
```

---

## 📦 Blueprints

### `auth.py` - Authentication Blueprint

**Routes:**

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Login selection page |
| `/login` | GET | Redirect to login |
| `/logout` | GET | Logout user |
| `/admin/login` | GET/POST | Admin login |
| `/user/login` | GET/POST | User login |
| `/azure/login` | GET | Azure AD SSO start |
| `/azure/callback` | GET | Azure AD callback |

**Features:**
- Azure AD SSO integration
- Local fallback authentication
- Login attempt tracking
- Admin: `admin` / `admin123`
- Rate limiting protection

### `user.py` - User Portal Blueprint

**Routes:**

| Route | Method | Description |
|-------|--------|-------------|
| `/user` | GET | Main user portal |
| `/user/my_srs` | GET | User's assigned SRs |
| `/user/search/<sr_id>` | GET | Search SR |
| `/user/get_sr_details` | POST | Get SR details |
| `/user/feedback` | POST | Submit correction |
| `/user/my_availability` | GET/POST | User availability |
| `/user/get_known_workaround` | POST | Get known workaround |

**Features:**
- SR search with semantic matching
- AI workaround display
- Feedback submission
- Known workaround integration
- User availability management

### `admin.py` - Admin Portal Blueprint

**Routes:**

| Route | Method | Description |
|-------|--------|-------------|
| `/admin` | GET | Admin dashboard |
| `/admin/upload` | POST | Upload Excel |
| `/admin/process_file` | POST | Process uploaded file |
| `/admin/stats` | GET | System statistics |
| `/admin/download/<filename>` | GET | Download report |
| `/admin/get_reports` | GET | List reports |

**Features:**
- Excel file upload
- RAG pipeline processing
- Statistics display
- Report download

### `team.py` - Team Management Blueprint

**Routes:**

| Route | Method | Description |
|-------|--------|-------------|
| `/team/skill` | GET | Skills matrix page |
| `/team/people` | GET | Team members JSON |
| `/team/people/<name>/availability` | POST | Set availability |
| `/team/people/<name>/skills` | GET/POST | Member skills |
| `/team/assignments/history` | GET | Assignment history |

**Features:**
- Skills matrix view
- Availability management
- Workload tracking
- Assignment history

### `api.py` - REST API Blueprint

**Routes:**

| Route | Method | Description |
|-------|--------|-------------|
| `/api/vote/upvote` | POST | Upvote workaround |
| `/api/vote/downvote` | POST | Downvote workaround |
| `/api/vote/get_votes` | POST | Get vote counts |
| `/api/feedback/submit` | POST | Submit feedback |
| `/api/regenerate` | POST | Regenerate AI workaround |
| `/api/known_workaround/search` | POST | Search known WAs |

**Features:**
- Voting system
- Feedback API
- AI regeneration
- Known workaround search

---

## 🔧 Blueprint Registration

```python
# routes/__init__.py
def register_blueprints(app):
    from .auth import auth_bp
    from .user import user_bp
    from .admin import admin_bp
    from .team import team_bp
    from .api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(team_bp, url_prefix='/team')
    app.register_blueprint(api_bp, url_prefix='/api')
```

---

## 🔒 Security

**Authentication Decorators:**
```python
@login_required          # Any authenticated user
@admin_required          # Admin users only
@user_login_required     # User portal access
```

**Rate Limiting:**
- Max 5 login attempts
- 15 minute lockout

---

## 🔗 Related

- [app/README.md](../README.md) - Flask application
- [utils/README.md](../utils/README.md) - Utilities

---

*Part of SR-Analyzer App Module*
