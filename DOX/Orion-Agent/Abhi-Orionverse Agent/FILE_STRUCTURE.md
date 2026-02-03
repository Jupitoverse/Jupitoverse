# 📁 File Structure - Orionverse Agent

> Complete file structure documentation for the combined project

---

## 🏠 Root Directory

```
Abhi-Orionverse Agent/
│
├── 📄 index.html                    # Main SPA entry point
├── 📄 README.md                     # Project documentation
├── 📄 FILE_STRUCTURE.md             # This file
├── 📄 requirements.txt              # Base Python dependencies
├── 📄 START_APP.bat                 # Windows startup script
│
├── 📂 backend/                      # Flask backend (Port 5001)
├── 📂 static/                       # Frontend CSS/JS assets
├── 📂 templates/                    # HTML page templates
├── 📂 rag_module/                   # RAG/AI module
├── 📂 docs/                         # Additional documentation
└── 📂 scripts/                      # Utility scripts
```

---

## 🖥️ Backend (`backend/`)

Flask API server handling all data operations.

```
backend/
├── 📄 app.py                        # Main Flask application factory
├── 📄 database.py                   # PostgreSQL connection handler
├── 📄 debug_search.py               # Search debugging utilities
├── 📄 test_backend_live.py          # API test suite
├── 📄 schema_workarounds_enhanced.sql  # Database schema
│
├── 📂 data/                         # JSON data files
│   ├── sr_data.json                 # 32,730+ Service Requests
│   ├── defect_data.json             # 2,979+ Defects
│   ├── outage_report_data.json      # Outage reports
│   └── ultron_data.json             # Ultron system data
│
├── 📂 routes/                       # API route blueprints
│   ├── __init__.py                  # Blueprint registration
│   ├── auth.py                      # /api/auth/* - Authentication
│   ├── search.py                    # /api/search/* - Search API
│   ├── workarounds.py               # /api/workarounds/* - Basic WA
│   ├── workarounds_enhanced.py      # Enhanced workaround features
│   ├── bulk_handling.py             # /api/bulk-handling/* - B1-B6 ops
│   ├── billing.py                   # /api/billing/* - Billing reports
│   ├── billing_csv.py               # CSV billing exports
│   ├── excel_loader.py              # /api/excel/* - Excel uploads
│   └── smart_sr.py                  # /api/smart-sr/* - RAG integration
│
└── 📂 __pycache__/                  # Python bytecode (auto-generated)
```

### Route Endpoints

| Blueprint | Prefix | File | Key Functions |
|-----------|--------|------|---------------|
| auth_bp | /api/auth | auth.py | login, logout, verify |
| search_bp | /api/search | search.py | all, filter |
| workarounds_bp | /api/workarounds | workarounds.py | CRUD operations |
| bulk_handling_bp | /api/bulk-handling | bulk_handling.py | B1-B6 operations |
| billing_bp | /api/billing | billing.py | Reports, revenue |
| smart_sr_bp | /api/smart-sr | smart_sr.py | AI analysis, semantic search |

---

## 🎨 Static Assets (`static/`)

Frontend CSS and JavaScript files.

```
static/
├── 📂 css/
│   └── style.css                    # Main stylesheet (all styles)
│
└── 📂 js/
    ├── main.js                      # App initialization, routing
    ├── api.js                       # API client wrapper
    ├── auth.js                      # Authentication handling
    ├── search.js                    # Search Anything module
    ├── bulk_handling.js             # Bulk operations module
    ├── bulk_handling_tabs.js        # Tab switching for bulk ops
    ├── abbreviations.js             # Abbreviation database
    └── smart_sr.js                  # Smart SR Assignment module
```

### JavaScript Modules

| Module | Global Object | Purpose |
|--------|---------------|---------|
| main.js | - | App bootstrap, navigation |
| api.js | API | HTTP request wrapper |
| auth.js | Auth | Login/logout, session |
| search.js | SearchAnything | Search functionality |
| bulk_handling.js | BulkHandling | B1-B6 operations |
| smart_sr.js | SmartSR | RAG/AI analysis |

---

## 📄 Templates (`templates/`)

HTML page templates loaded dynamically via SPA routing.

```
templates/
├── home.html                        # Home dashboard
├── smart_sr_assignment.html         # 🆕 AI Analysis page
├── search_anything.html             # Search across all data
├── bulk_handling.html               # Bulk operations interface
├── dashboard.html                   # Analytics dashboard
├── billing.html                     # Billing reports
├── workarounds.html                 # (if exists)
├── stuck_activities.html            # Stuck activity tracker
├── top_offender.html                # Top offender analysis
├── sr_handling.html                 # SR management
├── training.html                    # Training materials
├── welcome-kit.html                 # New joiner resources
├── links.html                       # Important links
├── release.html                     # Release information
├── events.html                      # Team events
├── assignments.html                 # Team assignments
├── database.html                    # Database viewer
├── imp-links.html                   # Important links (alt)
└── abbreviation.html                # Abbreviation lookup
```

---

## 🤖 RAG Module (`rag_module/`)

AI-powered SR analysis using RAG (Retrieval-Augmented Generation).

```
rag_module/
├── 📄 README.md                     # RAG module documentation
├── 📄 requirements.txt              # RAG-specific dependencies
├── 📄 TECHNICAL_SPECIFICATIONS.md   # Technical details
├── 📄 First_time_MultiModel.bat     # First-time setup (Windows)
├── 📄 First_time_MultiModel.sh      # First-time setup (Linux/Mac)
├── 📄 START_MULTIMODEL_RAG.bat      # Regular startup (Windows)
├── 📄 START_MULTIMODEL_RAG.sh       # Regular startup (Linux/Mac)
│
├── 📂 RAG/                          # Core RAG pipeline
│   ├── __init__.py
│   ├── extract_semantic_workarounds.py  # Semantic extraction
│   ├── 📂 pipeline/
│   │   ├── __init__.py
│   │   ├── multi_model_rag_pipeline_chatgpt.py  # Main pipeline
│   │   └── activity_name_finder.py              # Activity extraction
│   ├── 📂 creation/                 # Vectorstore creation scripts
│   │   ├── create_history_vectorstore.py
│   │   ├── create_abbreviation_vectorstore.py
│   │   └── ...
│   ├── 📂 utils/                    # Utility functions
│   │   ├── token_manager.py         # API token rotation
│   │   ├── llm_caller.py            # LLM API wrapper
│   │   └── ...
│   └── 📂 rag/
│       ├── README.md
│       └── LLM_FLOW_DOCUMENTATION.md
│
├── 📂 app/                          # Original RAG Flask app
│   ├── __init__.py                  # App factory
│   ├── sr_feedback_app.py           # Entry point
│   ├── 📂 routes/                   # Original routes
│   │   ├── admin.py
│   │   ├── api.py
│   │   ├── auth.py
│   │   ├── team.py
│   │   └── user.py
│   └── 📂 utils/
│       ├── helpers.py
│       ├── decorators.py
│       └── state.py
│
├── 📂 data/                         # Data storage
│   ├── 📂 vectorstore/
│   │   └── 📂 chromadb_store/       # ChromaDB vector database
│   │       ├── chroma.sqlite3       # ChromaDB metadata
│   │       └── *.bin, *.pickle      # Vector embeddings
│   ├── 📂 database/
│   │   ├── abbreviation.db          # Abbreviation lookup
│   │   ├── people_skills.db         # Team skills
│   │   ├── sr_tracking.db           # SR tracking
│   │   ├── workaround_feedback.db   # User feedback
│   │   └── llm_usage_stats.json     # LLM usage tracking
│   └── 📂 backup/                   # Database backups
│
├── 📂 models/                       # ML models
│   └── 📂 sentence-transformers_all-MiniLM-L6-v2/
│       ├── config.json
│       ├── pytorch_model.bin        # Model weights
│       └── ...
│
├── 📂 tokens/                       # API tokens
│   ├── README.md
│   └── Tokens.xlsx                  # API token storage
│
├── 📂 templates/                    # Original RAG templates
│   ├── 📂 admin/
│   ├── 📂 auth/
│   ├── 📂 feedback/
│   ├── 📂 team/
│   └── 📂 user/
│
├── 📂 analyzers/                    # SR analysis components
│   ├── batch_sr_analyser.py
│   ├── comprehensive_sr_analyzer.py
│   └── sr_text_preprocessor.py
│
├── 📂 team/                         # Team management
│   └── people_skills_database.py
│
├── 📂 assignment/                   # Assignment logic
│   ├── daily_data_manager.py
│   └── priority_age_calculator.py
│
├── 📂 workaround/                   # Workaround utilities
│   ├── resolution_mapping_retriever.py
│   └── ...
│
├── 📂 admin/                        # Admin functions
│   ├── 📂 email/                    # Outlook integration
│   └── 📂 upload/                   # File upload handlers
│
├── 📂 user/                         # User feedback
│   └── 📂 feedback/
│
├── 📂 config/                       # Configuration
│   ├── settings.py
│   └── paths.py
│
├── 📂 input/                        # Input file staging
│   └── *.xls, *.xlsx
│
└── 📂 output/                       # Generated outputs
    ├── 📂 daily_assignments/
    ├── 📂 exports/
    └── 📂 reports/
```

---

## 📚 Documentation (`docs/`)

Additional documentation files.

```
docs/
├── ARCHITECTURE.md                  # System architecture
├── DEVELOPER_GUIDE.md               # Developer documentation
├── QUICK_START.md                   # Quick start guide
├── DEPLOYMENT_CHECKLIST.md          # Deployment checklist
├── BULK_HANDLING_GUIDE.md           # Bulk operations guide
├── SEARCH_ENGINE_GUIDE.md           # Search functionality
├── WORKAROUND_FEATURES_SUMMARY.md   # Workaround features
└── ... (other docs)
```

---

## 🛠️ Scripts (`scripts/`)

Utility and startup scripts.

```
scripts/
├── convert_excel.py                 # Excel to JSON converter
├── setup_avd.ps1                    # AVD setup (PowerShell)
├── START_BACKEND.bat                # Backend startup
├── START_NETWORK_BACKEND.bat        # Network deployment
├── test_api.html                    # API testing page
└── test_network_access.ps1          # Network test
```

---

## 📊 Data Flow

```
┌────────────────────────────────────────────────────────────────────┐
│                           USER REQUEST                              │
└─────────────────────────────┬──────────────────────────────────────┘
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                    FRONTEND (index.html)                            │
│    ┌─────────┐   ┌──────────────┐   ┌─────────────────────┐       │
│    │ main.js │ → │ smart_sr.js  │ → │ API.js              │       │
│    └─────────┘   └──────────────┘   └──────────┬──────────┘       │
└─────────────────────────────────────────────────┼──────────────────┘
                                                  │ HTTP
                                                  ▼
┌────────────────────────────────────────────────────────────────────┐
│                    BACKEND (Flask - Port 5001)                      │
│    ┌───────────────────────────────────────────────────────────┐   │
│    │                      app.py (Router)                       │   │
│    ├───────────┬───────────┬───────────┬───────────┬───────────┤   │
│    │ search.py │ smart_sr  │ workaround│ bulk_ops  │   auth    │   │
│    └─────┬─────┴─────┬─────┴─────┬─────┴─────┬─────┴─────┬─────┘   │
│          │           │           │           │           │         │
└──────────┼───────────┼───────────┼───────────┼───────────┼─────────┘
           │           │           │           │           │
           ▼           ▼           ▼           ▼           ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
    │ sr_data  │ │ RAG      │ │ Postgres │ │ Postgres │ │ Session  │
    │ .json    │ │ Module   │ │ DB       │ │ DB       │ │ Store    │
    └──────────┘ └────┬─────┘ └──────────┘ └──────────┘ └──────────┘
                      │
                      ▼
              ┌──────────────┐
              │  ChromaDB    │
              │  Vectorstore │
              │  (1.18M+)    │
              └──────────────┘
```

---

## 🔑 Key Files Quick Reference

| File | Purpose | Edit When |
|------|---------|-----------|
| `backend/app.py` | Flask app creation | Adding new routes |
| `backend/routes/smart_sr.py` | RAG integration | AI functionality |
| `static/js/main.js` | Navigation config | Adding new pages |
| `static/js/smart_sr.js` | AI UI logic | Smart SR features |
| `templates/smart_sr_assignment.html` | AI page template | UI changes |
| `rag_module/RAG/pipeline/*.py` | RAG pipeline | AI logic |
| `rag_module/config/settings.py` | RAG config | Configuration |

---

*Last updated: 2026-01-12*
