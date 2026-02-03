# Orionverse Agent - Combined Portal with RAG Integration

## 📋 Project Overview

**Project Name:** Orionverse Agent  
**Type:** Integrated Full-Stack Application with RAG Capabilities  
**Tech Stack:** Flask, Python, ChromaDB, SQLite, REST APIs, JavaScript  
**Purpose:** Unified portal combining Orionverse web features with SR Analyzer RAG capabilities

---

## 🎯 Project Description

### Short Description (30 seconds)
"Orionverse Agent is the production deployment that combines our Orionverse web portal with the SR Analyzer RAG pipeline. It provides a unified interface where users can access traditional support tools (search, billing, bulk handling) alongside AI-powered SR analysis features. The architecture uses Flask Blueprints to integrate the RAG module as a subcomponent while maintaining the original Orionverse functionality."

### Detailed Description (2-3 minutes)
"This project represents the integration of two separate systems into a unified platform:

**1. Orionverse Base Features:**
- Universal search across SRs, defects, and workarounds
- SQO and ONI API consoles with automatic token management
- Billing operations and CSV processing
- Bulk handling for batch operations

**2. Integrated RAG Features (Smart SR Assignment):**
- AI-powered SR analysis using the multi-model pipeline
- Semantic workaround retrieval from ChromaDB
- Java error detection with 5-source voting
- Skill-based team assignment
- User feedback collection for model improvement

**Technical Integration Approach:**
- The RAG module is included as a subdirectory (`rag_module/`)
- Flask Blueprints register RAG routes under `/api/smart-sr`
- Shared ChromaDB and SQLite databases
- Unified authentication across all features
- Consistent UI theme using CSS variables

**New Tabs Added:**
1. **My Dashboard:** Personal SR analysis view
2. **Smart SR Assignment:** AI-powered SR analysis
3. **Smart Team:** Team skills and assignment management

The key challenge was integrating two Flask applications with different architectures while maintaining backward compatibility and consistent user experience."

---

## 📁 File Structure

```
Abhi-Orionverse Agent/
├── backend/
│   ├── app.py                           # Main Flask app with all blueprints
│   ├── routes/
│   │   ├── auth.py                      # Authentication
│   │   ├── search.py                    # Universal search
│   │   ├── billing.py                   # Billing operations
│   │   ├── bulk_handling.py             # Batch operations
│   │   ├── sqo_api.py                   # SQO API proxy
│   │   ├── oni_api.py                   # ONI API proxy
│   │   └── smart_sr.py                  # RAG integration routes ⭐
│   └── data/
│       ├── sr_data.json
│       ├── defect_data.json
│       └── ultron_data.json
│
├── rag_module/                          # Integrated RAG system ⭐
│   ├── RAG/
│   │   ├── pipeline/
│   │   │   └── multi_model_rag_pipeline_chatgpt.py
│   │   └── vectorstore/
│   │       └── vectorstore_manager.py
│   ├── app/
│   │   ├── routes/
│   │   │   ├── api.py                   # RAG API endpoints
│   │   │   └── team.py                  # Team management
│   │   └── utils/
│   ├── data/
│   │   ├── vectorstore/
│   │   │   └── chroma_db/               # ChromaDB storage
│   │   ├── people_skills.db             # Team skills
│   │   └── database/
│   │       └── javaMapping.db           # Java mapping
│   ├── analyzers/
│   ├── config/
│   └── templates/
│
├── static/
│   ├── css/
│   │   └── style.css                    # Unified theme
│   └── js/
│       ├── main.js                      # Navigation with new tabs
│       ├── smart_sr.js                  # RAG UI module ⭐
│       ├── api_console.js               # SQO/ONI console
│       └── search.js
│
├── templates/
│   ├── home.html
│   ├── search_anything.html
│   ├── sqo.html
│   ├── oni.html
│   ├── my_dashboard.html                # New: Personal dashboard ⭐
│   ├── smart_sr_assignment.html         # New: AI SR analysis ⭐
│   └── smart_team.html                  # New: Team management ⭐
│
├── index.html                           # SPA entry point
├── START_APP.bat                        # Launch script
├── PROMPT.txt                           # Change history
└── requirements.txt
```

---

## 🛠️ Technologies Used

| Category | Technology | Purpose |
|----------|------------|---------|
| Backend | Flask 2.x | Web framework |
| Backend | Flask-CORS | Cross-origin handling |
| LLM | OpenAI API (Amdocs Gateway) | AI analysis |
| Embeddings | Sentence Transformers | Text vectorization |
| Vector DB | ChromaDB | Semantic search |
| Database | SQLite | Skills & Java mapping |
| Frontend | Vanilla JavaScript | SPA functionality |
| Styling | CSS Variables | Unified theming |
| API | REST | Communication |

---

## 🔧 Key Technical Implementations

### 1. Integrating RAG Module as Blueprint

```python
# backend/app.py
from flask import Flask
from flask_cors import CORS

# Import original blueprints
from routes.auth import auth_bp
from routes.search import search_bp
from routes.sqo_api import sqo_api_bp
from routes.oni_api import oni_api_bp

# Import RAG integration blueprint
from routes.smart_sr import smart_sr_bp  # ⭐ New

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register original blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(sqo_api_bp, url_prefix='/api/sqo')
    app.register_blueprint(oni_api_bp, url_prefix='/api/oni')
    
    # Register RAG blueprint ⭐
    app.register_blueprint(smart_sr_bp, url_prefix='/api/smart-sr')
    
    return app
```

### 2. Smart SR Blueprint (RAG Integration)

```python
# backend/routes/smart_sr.py
import sys
import os
from flask import Blueprint, request, jsonify

# Add rag_module to path
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
RAG_MODULE_PATH = os.path.join(PROJECT_ROOT, 'rag_module')
sys.path.insert(0, RAG_MODULE_PATH)

smart_sr_bp = Blueprint('smart_sr', __name__)

# Lazy load RAG pipeline (heavy initialization)
_rag_pipeline = None

def get_rag_pipeline():
    global _rag_pipeline
    if _rag_pipeline is None:
        from RAG.pipeline.multi_model_rag_pipeline_chatgpt import MultiModelRAGPipeline
        _rag_pipeline = MultiModelRAGPipeline()
    return _rag_pipeline

@smart_sr_bp.route('/analyze', methods=['POST'])
def analyze_sr():
    """Analyze single SR using RAG pipeline"""
    data = request.get_json()
    
    pipeline = get_rag_pipeline()
    result = pipeline.analyze_sr({
        'sr_id': data.get('sr_id'),
        'description': data.get('description'),
        'priority': data.get('priority'),
        'notes': data.get('notes', '')
    })
    
    return jsonify({
        'success': True,
        'analysis': result
    })

@smart_sr_bp.route('/team/members', methods=['GET'])
def get_team_members():
    """Get team members from people_skills.db"""
    import sqlite3
    
    db_path = os.path.join(RAG_MODULE_PATH, 'data', 'people_skills.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM team_members")
    members = cursor.fetchall()
    
    return jsonify({'members': members})

@smart_sr_bp.route('/database-info', methods=['GET'])
def get_database_info():
    """Get ChromaDB statistics"""
    import chromadb
    
    chroma_path = os.path.join(RAG_MODULE_PATH, 'data', 'vectorstore', 'chroma_db')
    client = chromadb.PersistentClient(path=chroma_path)
    
    collections = client.list_collections()
    info = []
    
    for col in collections:
        info.append({
            'name': col.name,
            'count': col.count()
        })
    
    return jsonify({'collections': info})
```

### 3. Navigation with New Tabs

```javascript
// static/js/main.js
const NAV_CONFIG = {
    links: [
        { id: 'home', text: 'Home', file: 'templates/home.html' },
        { id: 'my-dashboard', text: '📊 My Dashboard', file: 'templates/my_dashboard.html' },
        { id: 'smart-sr', text: '🤖 Smart SR Assignment', file: 'templates/smart_sr_assignment.html' },
        { id: 'smart-team', text: '👥 Smart Team', file: 'templates/smart_team.html' },
        { id: 'sqo', text: '⚡ SQO', file: 'templates/sqo.html' },
        { id: 'oni', text: '🔮 ONI', file: 'templates/oni.html' },
        { id: 'search-anything', text: 'Search Anything', file: 'templates/search_anything.html' },
        // ... other tabs
    ]
};
```

### 4. Smart SR JavaScript Module

```javascript
// static/js/smart_sr.js
const SMART_SR_API_BASE = 'http://127.0.0.1:5002/api/smart-sr';

const SmartSR = {
    async analyzeSR(srData) {
        const response = await fetch(`${SMART_SR_API_BASE}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(srData)
        });
        return response.json();
    },
    
    async loadDatabaseInfo() {
        const response = await fetch(`${SMART_SR_API_BASE}/database-info`);
        const data = await response.json();
        this.displayDatabaseInfo(data.collections);
    },
    
    displayDatabaseInfo(collections) {
        const container = document.getElementById('db-info');
        container.innerHTML = collections.map(col => `
            <div class="db-collection">
                <h4>${col.name}</h4>
                <p>${col.count} documents</p>
            </div>
        `).join('');
    }
};

const SmartTeam = {
    async loadTeamData() {
        const response = await fetch(`${SMART_SR_API_BASE}/team/members`);
        const data = await response.json();
        this.renderTeamMembers(data.members);
    },
    
    renderTeamMembers(members) {
        const grid = document.getElementById('team-grid');
        grid.innerHTML = members.map(member => `
            <div class="team-card">
                <h3>${member.name}</h3>
                <p>Skills: ${member.skills}</p>
                <p>Workload: ${member.current_workload}</p>
            </div>
        `).join('');
    }
};
```

### 5. Unified Theme CSS

```css
/* static/css/style.css - Shared variables */
:root {
    --bg-primary: #0a0a12;
    --bg-secondary: #1a1822;
    --border-primary: #2c2a3a;
    --text-primary: #f0f0f5;
    --text-secondary: #a09cb0;
    --accent-primary: #8B5CF6;
    --accent-secondary: #a78bfa;
    --accent-glow: rgba(139, 92, 246, 0.5);
    --success-color: #2dd4bf;
    --error-color: #f43f5e;
}

/* Smart SR specific styles using shared variables */
.smart-sr-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-primary);
    border-radius: 12px;
    padding: 24px;
}

.smart-sr-card:hover {
    border-color: var(--accent-primary);
    box-shadow: 0 0 20px var(--accent-glow);
}
```

---

## 🔄 Integration Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Orionverse Agent                              │
│                 (Unified Portal Architecture)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  Original       │ │  RAG Module     │ │  API Proxies    │
│  Orionverse     │ │  (smart_sr_bp)  │ │  (sqo, oni)     │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ • Search        │ │ • SR Analysis   │ │ • SQO APIs      │
│ • Billing       │ │ • Team Mgmt     │ │ • ONI APIs      │
│ • Bulk Handling │ │ • Feedback      │ │ • Token Mgmt    │
│ • Auth          │ │ • Vector Search │ │                 │
└─────────────────┘ └─────────────────┘ └─────────────────┘
          │                   │                   │
          └───────────────────┼───────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Flask Application                             │
│                    (app.py - Port 5002)                         │
├─────────────────────────────────────────────────────────────────┤
│  Blueprints:                                                    │
│  • /api/auth         - Authentication                           │
│  • /api/search       - Universal search                         │
│  • /api/billing      - Billing operations                       │
│  • /api/sqo          - SQO API proxy                           │
│  • /api/oni          - ONI API proxy                           │
│  • /api/smart-sr     - RAG integration ⭐                       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Frontend (Port 8081)                          │
├─────────────────────────────────────────────────────────────────┤
│  Navigation Tabs:                                               │
│  • Home                                                         │
│  • 📊 My Dashboard     (RAG - personal view)                   │
│  • 🤖 Smart SR         (RAG - analysis)                        │
│  • 👥 Smart Team       (RAG - team mgmt)                       │
│  • ⚡ SQO              (API console)                           │
│  • 🔮 ONI              (API console)                           │
│  • Search Anything     (original)                              │
│  • Billing, etc.       (original)                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 💡 Interview Questions & Answers

### Q1: How did you integrate two separate Flask applications?
**Answer:** "I used Flask Blueprints to modularize both applications. The RAG module was included as a subdirectory, and I created a bridge blueprint (`smart_sr.py`) that:
1. Adds the RAG module path to `sys.path`
2. Lazily imports RAG components to avoid heavy initialization on startup
3. Exposes RAG functionality through REST endpoints
4. Handles path resolution for databases (ChromaDB, SQLite)

This approach maintains separation of concerns while enabling integration."

### Q2: What challenges did you face during integration?
**Answer:** "Several challenges:
1. **Path resolution:** RAG module expected relative paths; had to make them absolute
2. **CORS:** Frontend on port 8081, backend on 5002 required explicit CORS config
3. **Lazy loading:** RAG pipeline is heavy; implemented lazy initialization
4. **Theme consistency:** RAG templates used different colors; unified with CSS variables
5. **Authentication:** Removed RAG's separate auth, used Orionverse's unified login
6. **Port conflicts:** Original projects used same ports; reassigned to 5002/8081"

### Q3: How do you handle the different authentication systems?
**Answer:** "The original RAG project had its own login (admin/admin123). I:
1. Removed RAG's authentication routes
2. Extended Orionverse's auth to cover RAG endpoints
3. Used session-based auth across all blueprints
4. Added `@login_required` decorator to RAG routes
5. Unified user roles (admin can access all, user sees limited features)"

### Q4: How do you ensure consistent UI across integrated features?
**Answer:** "I used CSS variables defined in a single stylesheet:
```css
:root {
    --bg-primary: #0a0a12;
    --accent-primary: #8B5CF6;
    /* ... */
}
```

All templates (original and RAG) reference these variables. When adding new RAG templates, I:
1. Replaced hardcoded colors with variables
2. Used the same card, button, and form styles
3. Maintained consistent spacing and typography
4. Applied the dark theme throughout"

### Q5: How does the frontend know which API base to use?
**Answer:** "I implemented dynamic API URL detection:
```javascript
const SMART_SR_API_BASE = window.location.hostname === 'localhost'
    ? 'http://127.0.0.1:5002/api/smart-sr'
    : `http://${window.location.hostname}:5002/api/smart-sr`;
```

This allows the same code to work locally and on network deployment. The backend port (5002) is configured separately from the frontend (8081)."

### Q6: What's the benefit of this combined architecture?
**Answer:** "Multiple benefits:
1. **Single deployment:** One application to deploy and maintain
2. **Unified UX:** Users don't switch between applications
3. **Shared authentication:** Login once, access everything
4. **Consistent data:** Same SR data available to search and RAG
5. **Reduced infrastructure:** Single server instead of multiple
6. **Easier updates:** Modify one codebase instead of synchronizing two"

---

## 🚀 How to Run

```bash
# Using the batch script
START_APP.bat

# Or manually:

# Terminal 1: Backend (Port 5002)
cd backend
python app.py

# Terminal 2: Frontend (Port 8081)
cd "Abhi-Orionverse Agent"
python -m http.server 8081

# Access
http://localhost:8081
```

---

## 📊 Key Metrics

- **Integrated Blueprints:** 9 (6 original + 3 RAG)
- **New Tabs:** 3 (My Dashboard, Smart SR, Smart Team)
- **API Endpoints:** 25+ combined
- **Shared Databases:** 3 (ChromaDB, people_skills.db, javaMapping.db)
- **Lines of Code:** ~15,000 (combined)
- **Deployment:** Single server, dual ports (5002, 8081)

---

## 🔗 Project Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                    Project Evolution                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐     ┌─────────────────┐
│   Orionverse    │     │  SR Analyzer    │
│   (Web Portal)  │     │  (Ollama/OpenAI)│
└────────┬────────┘     └────────┬────────┘
         │                       │
         │    Integration        │
         └───────────┬───────────┘
                     │
                     ▼
         ┌─────────────────────┐
         │  Orionverse Agent   │
         │  (Combined Portal)  │
         └─────────────────────┘
```

This project represents the culmination of the individual projects, combining web portal functionality with AI-powered SR analysis in a unified, production-ready application.
