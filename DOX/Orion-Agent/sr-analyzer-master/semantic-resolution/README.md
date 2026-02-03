# 📁 Semantic-Resolution

> **Core Application Directory for SR-Analyzer**

This is the main working directory containing all source code, configurations, and data for the SR Analysis system.

---

## 🚀 Quick Start

### First Time Setup

**Windows:**
```cmd
First_time_MultiModel.bat
```

**Linux/Mac:**
```bash
chmod +x First_time_MultiModel.sh
./First_time_MultiModel.sh
```

**What it does:**
1. ✅ Checks Python 3.10-3.12
2. ✅ Creates virtual environment
3. ✅ Installs dependencies (Flask, LangChain, ChromaDB, etc.)
4. ✅ Verifies `tokens/Tokens.xlsx`
5. ✅ Checks databases and vector stores
6. ✅ Starts the Flask application

### Regular Startup

**Windows:**
```cmd
START_MULTIMODEL_RAG.bat
```

**Linux/Mac:**
```bash
./START_MULTIMODEL_RAG.sh
```

### Manual Setup

```bash
# 1. Create and activate virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt
pip install langchain langchain-core langchain-community chromadb

# 3. Set PostgreSQL environment (for activity lookup)
export DB_HOST=inoscmm2181 DB_PORT=30432 DB_NAME=paasdb

# 4. Start application
python app/sr_feedback_app.py
```

### Access Points

| Portal | URL | Credentials |
|--------|-----|-------------|
| User Portal | http://localhost:5000 | None / Azure AD |
| Admin Portal | http://localhost:5000/admin | `admin` / `admin123` |

---

## 🐧 Platform Compatibility

| Feature | Windows | Linux/Mac |
|---------|:-------:|:---------:|
| Flask Web App | ✅ | ✅ |
| RAG Pipeline (5 LLM Calls) | ✅ | ✅ |
| ChromaDB Vector Store | ✅ | ✅ |
| Semantic Search | ✅ | ✅ |
| PostgreSQL Activity Lookup | ✅ | ✅ |
| Team Skills Management | ✅ | ✅ |
| User Feedback System | ✅ | ✅ |
| Azure AD SSO | ✅ | ✅ |
| **Outlook Email Fetcher** | ✅ | ❌ |

> ⚠️ **Linux Limitation**: The Outlook email fetcher uses Windows COM (`win32com`) and **does NOT work on Linux/Mac**. Use manual Excel upload via admin portal instead.

---

## 📁 Directory Structure

```
semantic-resolution/
│
├── 📂 app/                       # Flask Web Application
│   ├── __init__.py               # App factory (create_app)
│   ├── sr_feedback_app.py        # Entry point
│   ├── routes/                   # URL route handlers (5 blueprints)
│   │   ├── auth.py               # Authentication (368 lines)
│   │   ├── user.py               # User portal (1064 lines)
│   │   ├── admin.py              # Admin portal (605 lines)
│   │   ├── team.py               # Team management (760 lines)
│   │   └── api.py                # REST API (361 lines)
│   └── utils/                    # Helper functions
│
├── 📂 admin/                     # Admin Functionality
│   ├── email/                    # Outlook email fetching (Windows only)
│   └── upload/                   # Excel upload processing
│
├── 📂 RAG/                       # RAG Pipeline
│   ├── pipeline/                 # Core 5-LLM pipeline
│   │   ├── multi_model_rag_pipeline_chatgpt.py  # Main (2681 lines)
│   │   └── activity_name_finder.py
│   ├── utils/                    # ChromaDB management
│   ├── creation/                 # Vectorstore creation scripts
│   ├── input/                    # Pipeline input staging
│   └── llm output/               # Generated results
│
├── 📂 analyzers/                 # SR Analysis Engine
│   ├── batch_sr_analyser.py      # AIEnhancedServiceRequestAnalyzer
│   ├── comprehensive_sr_analyzer.py
│   └── sr_text_preprocessor.py   # Text cleaning
│
├── 📂 team/                      # Team Management
│   └── people_skills_database.py # Skills DB (1948 lines)
│
├── 📂 user/                      # User Feedback
│   └── feedback/                 # Feedback manager
│
├── 📂 data/                      # Data Storage
│   ├── database/                 # SQLite databases
│   │   ├── people_skills.db      # Team skills
│   │   ├── abbreviation.db       # Abbreviations
│   │   └── sr_tracking.db        # SR tracking
│   ├── vectorstore/              # Vector embeddings
│   │   └── chromadb_store/       # ChromaDB (1.18M+ records)
│   └── backup/                   # Backup files
│
├── 📂 templates/                 # HTML Templates (Jinja2)
│   ├── admin/                    # Admin portal (3 templates)
│   ├── auth/                     # Authentication (4 templates)
│   ├── user/                     # User portal (2 templates)
│   ├── team/                     # Team management (1 template)
│   └── json_workaround/          # Known workarounds (2 templates)
│
├── 📂 config/                    # Configuration
│   ├── settings.py               # App settings
│   ├── paths.py                  # Path constants
│   └── azure_ad.py               # Azure AD config
│
├── 📂 tokens/                    # API Token Storage
│   └── Tokens.xlsx               # API tokens (required)
│
├── 📂 models/                    # ML Models
│   └── sentence-transformers_all-MiniLM-L6-v2/
│
├── 📂 input/                     # Input file staging
├── 📂 output/                    # Generated reports
│   ├── reports/                  # Admin upload reports
│   ├── daily_assignments/        # Daily assignment reports
│   └── exports/                  # Data exports
│
├── 📂 workaround/                # Workaround extraction tools
├── 📂 json_workaround/           # Known workaround search
├── 📂 assignment/                # SR assignment logic
├── 📂 email_processing/          # Standalone email scripts (Windows)
│
├── 📄 First_time_MultiModel.bat  # First-time setup (Windows)
├── 📄 First_time_MultiModel.sh   # First-time setup (Linux)
├── 📄 START_MULTIMODEL_RAG.bat   # Regular startup (Windows)
├── 📄 START_MULTIMODEL_RAG.sh    # Regular startup (Linux)
├── 📄 requirements.txt           # Python dependencies
├── 📄 USER_ADMIN_GUIDE.md        # 📚 User & Admin guide
└── 📄 TECHNICAL_SPECIFICATIONS.md # Technical docs
```

---

## 🔄 Data Flow

```
┌──────────────────────────────────────────────────────────────┐
│                      DATA FLOW DIAGRAM                        │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│   ┌─────────────┐          ┌─────────────┐                   │
│   │ Outlook     │ ──────▶  │ admin/email │                   │
│   │ Daily Email │          │ (Win only)  │                   │
│   └─────────────┘          └──────┬──────┘                   │
│                                   │                          │
│   ┌─────────────┐                 │                          │
│   │ Manual      │ ──────▶  ┌──────▼──────┐                   │
│   │ Excel Upload│          │admin/upload │                   │
│   └─────────────┘          └──────┬──────┘                   │
│                                   │                          │
│                          ┌────────▼────────┐                 │
│                          │   analyzers/    │                 │
│                          │ preprocessor &  │                 │
│                          │ semantic search │                 │
│                          └────────┬────────┘                 │
│                                   │                          │
│                          ┌────────▼────────┐                 │
│                          │  RAG/pipeline/  │                 │
│                          │  5-LLM Pipeline │                 │
│                          └────────┬────────┘                 │
│                                   │                          │
│       ┌───────────────────────────┼───────────────────┐      │
│       ▼                           ▼                   ▼      │
│ ┌───────────┐            ┌───────────────┐    ┌───────────┐ │
│ │data/      │            │   output/     │    │  team/    │ │
│ │vectorstore│            │   reports     │    │assignment │ │
│ │(ChromaDB) │            │  (Excel)      │    │ tracking  │ │
│ └───────────┘            └───────────────┘    └───────────┘ │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## 🤖 5-LLM Pipeline

The core AI engine uses 5 specialized LLM calls:

| LLM | Purpose | Trigger |
|-----|---------|---------|
| **#1** | Find Semantic Workaround | Similarity < 50% |
| **#2** | Java Error Detection | Always (5-source voting) |
| **#3** | Extract Activity Names | If Java detected |
| **#4a/4b** | Resolution Generation | Java or General |
| **#5** | Skill-Based Assignment | Always |

---

## 🗄️ Database Schema

### ChromaDB Collection: `clean_history_data`

| Field | Description |
|-------|-------------|
| call_id | SR ID (uppercase) |
| description | SR description |
| workaround | Original workaround |
| ai_generated_workaround | RAG-generated |
| user_corrected_workaround | JSON array of corrections |

### SQLite: `people_skills.db`

| Table | Description |
|-------|-------------|
| team_members | Names, status, emails |
| skills | Application skills, levels |
| assignment_history | Past assignments (ML) |

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [USER_ADMIN_GUIDE.md](USER_ADMIN_GUIDE.md) | Complete user & admin guide |
| [TECHNICAL_SPECIFICATIONS.md](TECHNICAL_SPECIFICATIONS.md) | Technical architecture |
| [RAG/README.md](RAG/README.md) | RAG pipeline details |
| [app/README.md](app/README.md) | Flask application |

---

## 🔐 Security Notes

- API tokens in `tokens/Tokens.xlsx` (not in version control)
- Flask session uses `SECRET_KEY` (change in production)
- Admin emails configurable via `ADMIN_EMAILS` env variable
- Azure AD SSO supported

---

*Part of SR-Analyzer Project*
