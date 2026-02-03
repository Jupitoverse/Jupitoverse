# 📁 Semantic-Resolution

> **Core Application Directory for SR-Analyzer**

This is the main working directory containing all source code, configurations, and data for the SR Analysis system.

---

## 📋 Directory Overview

| Folder | Purpose | Key Files |
|--------|---------|-----------|
| `admin/` | Admin portal & email integration | `admin_upload_and_merge_with_rag.py` |
| `analyzers/` | SR text analysis & preprocessing | `batch_sr_analyser.py` |
| `app/` | Flask web application | `sr_feedback_app.py` |
| `assignment/` | SR assignment logic | `priority_age_calculator.py` |
| `config/` | Configuration settings | `settings.py`, `paths.py` |
| `data/` | Databases & vector stores | ChromaDB, SQLite files |
| `RAG/` | Multi-model RAG pipeline | `multi_model_rag_pipeline_chatgpt.py` |
| `team/` | Team skills management | `people_skills_database.py` |
| `user/` | User feedback system | `user_feedback_manager.py` |
| `workaround/` | Workaround extraction tools | `resolution_mapping_retriever.py` |
| `templates/` | HTML templates | Jinja2 templates |
| `tokens/` | API token storage | `Tokens.xlsx` |
| `models/` | ML models | sentence-transformers |
| `input/` | Input file staging | Uploaded Excel files |
| `output/` | Generated reports | Analysis results |

---

## 🚀 Quick Start

### 🆕 First Time Setup

Run the first-time setup script to install all dependencies and start the application:

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
1. Checks Python 3.10-3.12 installation
2. Installs all pip dependencies (LangChain, ChromaDB, etc.)
3. Verifies `tokens/Tokens.xlsx` exists
4. Checks vector stores and databases
5. Sets PostgreSQL configuration
6. Starts the Flask application

---

### 🔄 Regular Startup (After First Time)

**Windows:**
```cmd
START_MULTIMODEL_RAG.bat
```

**Linux/Mac:**
```bash
./START_MULTIMODEL_RAG.sh
```

---

### 📝 Manual Setup Steps

```bash
# 1. Install dependencies
pip install -r requirements.txt
pip install langchain langchain-core langchain-community chromadb

# 2. Set PostgreSQL environment variables
# Windows:
set DB_HOST=inoscmm2181 && set DB_PORT=30432 && set DB_NAME=paasdb

# Linux/Mac:
export DB_HOST=inoscmm2181 DB_PORT=30432 DB_NAME=paasdb

# 3. Verify tokens file exists
# Create tokens/Tokens.xlsx with columns: Email, Token

# 4. Start application
python app/sr_feedback_app.py
```

---

### 🔗 Access Points

| Portal | URL | Credentials |
|--------|-----|-------------|
| User Portal | http://localhost:5000 | No login required |
| Admin Portal | http://localhost:5000/admin | admin / admin123 |

---

### 🐧 Linux/Mac Compatibility

| Feature | Windows | Linux/Mac |
|---------|---------|-----------|
| Flask Web App | ✅ | ✅ |
| RAG Pipeline (5 LLM Calls) | ✅ | ✅ |
| ChromaDB Vector Store | ✅ | ✅ |
| Semantic Search | ✅ | ✅ |
| PostgreSQL Activity Lookup | ✅ | ✅ |
| Team Skills Management | ✅ | ✅ |
| User Feedback System | ✅ | ✅ |
| **Outlook Email Fetcher** | ✅ | ❌ |

> ⚠️ **Linux Limitation**: The Outlook email fetcher (`admin/email/email_fetcher.py`) uses Windows COM (`win32com`) and **does NOT work on Linux/Mac**. Use manual Excel upload via admin portal instead.

---

### 🔧 Optional: Initialize from Scratch

```bash
# Create vectorstores (if needed)
python RAG/creation/create_history_vectorstore.py

# Load team configuration from People.xlsx
python -c "from team.people_skills_database import PeopleSkillsDatabase; PeopleSkillsDatabase().load_people_from_excel()"
```

---

## 📊 Data Flow

```
┌──────────────────────────────────────────────────────────────┐
│                      DATA FLOW DIAGRAM                        │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│   ┌─────────────┐          ┌─────────────┐                   │
│   │ Outlook     │ ──────▶  │ admin/email │                   │
│   │ Daily Email │          │ fetcher     │                   │
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
│                          │     RAG/rag/    │                 │
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

## 🔧 Key Components

### 1. Admin Module (`admin/`)
- **Email Fetcher**: Connects to Outlook via Windows COM to fetch daily SR reports
- **Upload Handler**: Processes Excel uploads through complete RAG pipeline
- **6-Step Workflow**: Analyze → Save → Prepare → RAG → Merge → Cleanup

### 2. Analyzers (`analyzers/`)
- **AIEnhancedServiceRequestAnalyzer**: Main analysis engine with semantic search
- **SRTextPreprocessor**: Cleans SR text for better embedding quality
- **ComprehensiveSRAnalyzer**: Legacy compatibility wrapper

### 3. RAG Pipeline (`RAG/`)
- **5 LLM Calls**: Workaround finder, Java detection, activity extraction, resolution, assignment
- **Token Management**: Automatic rotation on quota exhaustion
- **Anti-Hallucination**: Strict grounding rules prevent fabricated information

### 4. Data Layer (`data/`)
- **ChromaDB**: Vector store for semantic search (1.18M+ records)
- **SQLite**: Team skills, SR tracking, abbreviations
- **Collections**: clean_history_data, java_mapping, comcast_code

### 5. Web Application (`app/`)
- **Flask Blueprints**: Modular route organization
- **User Portal**: Feedback submission and workaround viewing
- **Admin Portal**: Upload, team management, reports

---

## 📝 Configuration Files

| File | Purpose |
|------|---------|
| `config/settings.py` | Flask settings, model configs |
| `config/paths.py` | All path constants |
| `tokens/Tokens.xlsx` | API tokens for LLM calls |
| `People.xlsx` | Team member configurations |
| `requirements.txt` | Python dependencies |

---

## 🗄️ Database Schema

### ChromaDB Collections

**clean_history_data**
```
- call_id: SR ID
- description: SR description
- workaround: Original workaround
- ai_generated_workaround: RAG-generated workaround
- user_corrected_workaround: JSON array of user corrections
- resolution_categorization: Category
- application: Application area
- assigned_to: Assigned team member
```

**java_mapping**
```
- class_name: Java class name
- package: Package path
- file_path: Source file location
- class_type: Service, Controller, etc.
```

### SQLite Tables

**people_skills.db**
```sql
- team_members (id, name, status, employee_id)
- skills (member_id, application, skill_level, max_load, specializations)
- assignment_history (member_id, sr_id, complexity_score, success_rate)
- availability_history (member_id, availability_percent, reason)
```

---

## 🔒 Security Notes

- API tokens stored in `tokens/Tokens.xlsx` (not in version control)
- ChromaDB files contain sensitive SR data
- Flask session uses secure cookie with `SECRET_KEY`
- No external authentication required (internal network)

---

## 📚 See Also

- [Main README](../README.md) - Project overview
- [RAG/README.md](RAG/README.md) - RAG pipeline details
- [admin/README.md](admin/README.md) - Admin functionality
- [analyzers/README.md](analyzers/README.md) - Analysis components

---

*Part of SR-Analyzer Project*
