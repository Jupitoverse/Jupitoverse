# 🌐 App Module

> **Flask Web Application for SR Feedback System**

This module provides the web interface for both admin and user portals, enabling SR analysis, feedback collection, and team management.

---

## 📁 Structure

```
app/
├── __init__.py                    # Flask app factory (create_app)
├── README.md
├── sr_feedback_app.py             # Application entry point
│
├── routes/                        # URL route handlers (Blueprints)
│   ├── __init__.py
│   ├── admin.py                   # Admin portal routes
│   ├── user.py                    # User portal routes
│   ├── team.py                    # Team management routes
│   ├── api.py                     # REST API endpoints
│   ├── auth.py                    # Authentication routes
│   └── README.md
│
└── utils/                         # Helper functions
    ├── __init__.py
    ├── helpers.py                 # Utility functions
    ├── decorators.py              # Route decorators
    ├── state.py                   # Shared application state
    ├── summarize_semantic_wa.py   # Workaround summarization
    └── README.md
```

---

## 🚀 Quick Start

```bash
cd semantic-resolution
python app/sr_feedback_app.py

# Access:
# User Portal:  http://localhost:5000
# Admin Portal: http://localhost:5000/admin
```

---

## 📋 Route Overview

### User Portal (`/`)
| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page with SR search |
| `/feedback/<sr_id>` | GET | View SR details and workaround |
| `/feedback/<sr_id>` | POST | Submit workaround correction |
| `/search` | GET | Search SRs by ID or keywords |

### Admin Portal (`/admin`)
| Route | Method | Description |
|-------|--------|-------------|
| `/admin` | GET | Admin dashboard |
| `/admin/upload` | GET/POST | Upload Excel file |
| `/admin/reports` | GET | View generated reports |
| `/admin/team` | GET | Team management |
| `/admin/settings` | GET | System settings |

### Team Management (`/team`)
| Route | Method | Description |
|-------|--------|-------------|
| `/team/skills` | GET | View team skills matrix |
| `/team/availability` | GET/POST | Manage availability |
| `/team/assignments` | GET | View current assignments |

### API Endpoints (`/api`)
| Route | Method | Description |
|-------|--------|-------------|
| `/api/analyze` | POST | Analyze single SR (JSON) |
| `/api/search` | GET | Search SRs (JSON response) |
| `/api/feedback` | POST | Submit feedback (JSON) |
| `/api/team/status` | GET | Team status (JSON) |
| `/api/regenerate` | POST | Regenerate AI workaround |

### Authentication (`/auth`)
| Route | Method | Description |
|-------|--------|-------------|
| `/auth/login` | GET/POST | Login page |
| `/auth/logout` | GET | Logout |
| `/auth/session` | GET | Session info |

---

## 🏭 Flask App Factory

The application uses the Flask app factory pattern in `__init__.py`:

```python
def create_app() -> Flask:
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
    
    # Register Blueprints
    from .routes.auth import auth_bp
    from .routes.user import user_bp
    from .routes.admin import admin_bp
    from .routes.team import team_bp
    from .routes.api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(team_bp, url_prefix='/team')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
```

---

## 📦 Routes Module

### `admin.py` - Admin Blueprint

Handles all admin portal functionality:

```python
@admin_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handle Excel file upload"""
    if request.method == 'POST':
        file = request.files['file']
        # Save file and trigger processing
        from admin.upload.admin_upload_and_merge_with_rag import upload_and_merge_with_rag
        success, output_path, errors = upload_and_merge_with_rag(file_path)
        return redirect(url_for('admin.reports'))
    return render_template('admin/upload.html')
```

### `user.py` - User Blueprint

Handles user feedback collection:

```python
@user_bp.route('/feedback/<sr_id>', methods=['GET', 'POST'])
def feedback(sr_id):
    """View SR and submit feedback"""
    if request.method == 'POST':
        user_workaround = request.form['workaround']
        # Save feedback to ChromaDB
        manager.add_user_feedback_entry(
            sr_id=sr_id,
            user_corrected_workaround=user_workaround
        )
        flash('Feedback submitted successfully!')
    
    sr_data = get_sr_by_id(sr_id)
    return render_template('user/feedback_main.html', sr=sr_data)
```

### `api.py` - API Blueprint

RESTful API endpoints:

```python
@api_bp.route('/analyze', methods=['POST'])
def analyze():
    """Analyze SR via API"""
    data = request.get_json()
    
    pipeline = MultiModelSRPipeline()
    result = pipeline.analyze_single_sr(data)
    
    return jsonify(result)
```

---

## 🛠️ Utils Module

### `helpers.py`

Common utility functions:

```python
def get_sr_by_id(sr_id: str) -> Optional[Dict]:
    """Retrieve SR from ChromaDB by ID"""
    
def format_workaround(text: str) -> str:
    """Format workaround for display"""
    
def validate_excel_file(file) -> Tuple[bool, str]:
    """Validate uploaded Excel file"""
    
def sanitize_input(text: str) -> str:
    """Sanitize user input"""
```

### `decorators.py`

Route decorators:

```python
def login_required(f):
    """Require login for route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Require admin role for route"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function
```

### `state.py`

Shared application state:

```python
# Global state accessible across routes
app_state = {
    'analyzer': None,          # ComprehensiveSRAnalyzer instance
    'pipeline': None,          # MultiModelSRPipeline instance
    'history_manager': None,   # HistoryDatabaseManager instance
    'processing': False,       # Is processing in progress?
    'last_upload': None        # Last upload timestamp
}
```

### `summarize_semantic_wa.py`

Workaround summarization utilities:

```python
def summarize_workaround(text: str, max_length: int = 500) -> str:
    """Create a summary of long workaround text"""
    
def extract_key_steps(workaround: str) -> List[str]:
    """Extract numbered steps from workaround"""
```

---

## 🎨 Templates

The app uses Jinja2 templates located in `templates/`:

```
templates/
├── admin/
│   ├── dashboard.html
│   ├── upload.html
│   └── reports.html
├── auth/
│   ├── login.html
│   └── logout.html
├── feedback/
│   ├── base.html
│   ├── search.html
│   └── detail.html
├── team/
│   └── skill_view.html
└── user/
    └── feedback_main.html
```

---

## ⚙️ Configuration

### Flask Settings (in `__init__.py`)
```python
app.config.update(
    SECRET_KEY='sr-feedback-secret-key',
    MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16MB max upload
    UPLOAD_FOLDER='input/',
    ALLOWED_EXTENSIONS={'xls', 'xlsx'}
)
```

### Session Configuration
```python
app.config.update(
    SESSION_TYPE='filesystem',
    PERMANENT_SESSION_LIFETIME=timedelta(hours=8)
)
```

---

## 🔒 Security

- **CSRF Protection**: Flask-WTF for forms
- **File Validation**: Check extensions and size
- **Input Sanitization**: Clean user inputs
- **Session Security**: Secure cookie configuration

---

## 📊 API Response Format

All API endpoints return JSON:

```json
{
    "success": true,
    "data": {
        "sr_id": "CAS123456",
        "ai_workaround": "...",
        "assigned_to": "John Smith"
    },
    "message": "Analysis complete",
    "timestamp": "2026-01-07T10:30:00"
}
```

Error responses:
```json
{
    "success": false,
    "error": "Invalid SR ID format",
    "code": 400
}
```

---

## 🔗 Related Modules

- [Admin](../admin/README.md) - Upload processing
- [Analyzers](../analyzers/README.md) - SR analysis
- [RAG](../RAG/README.md) - LLM pipeline

---

*Part of SR-Analyzer App Module*
