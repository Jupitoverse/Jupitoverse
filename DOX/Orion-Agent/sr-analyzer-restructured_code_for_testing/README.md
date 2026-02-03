# 🚀 SR-Analyzer: Intelligent Service Request Analysis System

> **AI-Powered Multi-Model RAG Pipeline for Automated SR Resolution**

An enterprise-grade Service Request (SR) analysis system that leverages 5 specialized LLM calls, semantic search across 1.18M+ historical records, and intelligent team assignment to automate SR triage and resolution.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [5-LLM Pipeline](#5-llm-pipeline)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Reference](#api-reference)

---

## 🎯 Overview

The SR-Analyzer system transforms how Service Requests are processed by:

1. **Semantic Search**: Finding similar historical SRs from a 1.18M+ record database
2. **Java Detection**: Using 5-source voting to determine if issues are Java/backend errors
3. **Activity Extraction**: Identifying Java activity names and validating against PostgreSQL
4. **AI Resolution**: Generating comprehensive, grounded workarounds
5. **Intelligent Assignment**: Skill-based team member assignment with load balancing

### Key Metrics

| Metric | Value |
|--------|-------|
| Historical Records | 1,180,000+ |
| LLM Calls per SR | 3-5 (adaptive) |
| Semantic Model | all-MiniLM-L6-v2 |
| Vector Store | ChromaDB |
| Average Processing | ~15 seconds/SR |

---

## ✨ Key Features

### 🔍 Semantic Search
- **ChromaDB Vector Store** with sentence-transformer embeddings
- **Text Preprocessing** to remove noise (customer info, timestamps, IDs)
- **Similarity Threshold** filtering for quality matches

### 🗳️ 5-Source Voting System
Determines if an SR is a Java/backend error by voting from:
1. Resolution Categories (current + similar SRs)
2. Semantic Workaround content
3. AI-generated workarounds from similar SRs
4. User-corrected workarounds from history
5. Current SR description/notes content

### 🔄 Activity Extraction with Retry
- Extracts Java activity names from SR content
- Validates against PostgreSQL database
- Up to 2 retry attempts with alternative suggestions

### 🤖 Anti-Hallucination Prompts
- All file paths must come from provided context
- Class names validated against known activities
- Uncertain items marked as `[NEEDS INVESTIGATION]`

### 👥 Skill-Based Assignment
- Matches SR complexity to team member skill levels
- Considers current workload and availability
- Equal distribution with priority handling

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SR-ANALYZER ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐     ┌──────────────┐     ┌─────────────────┐  │
│  │ Excel Upload│ ──▶ │ Preprocessor │ ──▶ │ Semantic Search │  │
│  └─────────────┘     └──────────────┘     └────────┬────────┘  │
│                                                     │           │
│                      ┌──────────────────────────────┘           │
│                      ▼                                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              5-LLM RAG PIPELINE                          │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌───────┐ ┌──────┐ │   │
│  │  │ LLM 1   │ │ LLM 2   │ │ LLM 3   │ │LLM 4a │ │LLM 5 │ │   │
│  │  │Workaround│ │Java Vote│ │Activity │ │  or   │ │Assign│ │   │
│  │  │ Finder  │ │ System  │ │Extract  │ │ LLM 4b│ │ment  │ │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └───────┘ └──────┘ │   │
│  └─────────────────────────────────────────────────────────┘   │
│                      │                                          │
│                      ▼                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ChromaDB Merge│  │Excel Output  │  │Team Assignment Report│  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔗 5-LLM Pipeline

### LLM Call 1: Find Semantic Workaround
**Trigger**: When semantic search similarity < 50%
- Analyzes historical matches to extract best workaround
- Filters garbage workarounds (NA, escalated, closed, etc.)
- Combines multiple workarounds if needed

### LLM Call 2: Java Error Detection
**Always runs** - Uses 5-source voting mechanism:
```
Confidence Levels:
├── HIGH:     ≥80% agreement with ≥3 meaningful votes
├── MEDIUM:   ≥67% agreement with ≥3 meaningful votes
├── LOW:      ≥60% agreement
└── VERY_LOW: <60% agreement
```

### LLM Call 3: Extract Activity Names
**Trigger**: Only if Java error detected
- Extracts CamelCase activity names (ValidateAddress, CreateOrder, etc.)
- Validates against PostgreSQL database
- Retry loop with alternative suggestions if not found

### LLM Call 4a: Java Resolution
**Trigger**: If `is_java_error = true`
- Uses validated activities and implementation classes
- References actual Java code from codebase
- Generates 8-12 step workaround with anti-hallucination rules

### LLM Call 4b: General Resolution
**Trigger**: If `is_java_error = false`
- Adapts historical workaround patterns
- Uses SR-specific data (IDs, names from SR)
- Marks missing info as `[NEEDS INVESTIGATION]`

### LLM Call 5: Skill-Based Assignment
**Always runs** - Intelligent team assignment:
- Checks availability (0% = skip)
- Validates workload capacity
- Matches skill level to SR complexity
- Returns single team member name

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10, 3.11, or 3.12 (required for numpy/pandas compatibility)
- API tokens in `tokens/Tokens.xlsx`

---

### 🆕 First Time Setup

Use the first-time setup script to install all dependencies:

**Windows:**
```cmd
cd semantic-resolution
First_time_MultiModel.bat
```

**Linux/Mac:**
```bash
cd semantic-resolution
chmod +x First_time_MultiModel.sh
./First_time_MultiModel.sh
```

This script will:
1. ✅ Check/verify Python 3.10-3.12
2. ✅ Install all Python dependencies
3. ✅ Verify `tokens/Tokens.xlsx` exists
4. ✅ Check vector stores and databases
5. ✅ Start the Flask application

---

### 🔄 Regular Startup (After First Time)

**Windows:**
```cmd
cd semantic-resolution
START_MULTIMODEL_RAG.bat
```

**Linux/Mac:**
```bash
cd semantic-resolution
./START_MULTIMODEL_RAG.sh
```

---

### 📝 Manual Setup Steps

If you prefer manual setup or the scripts fail:

```bash
# 1. Navigate to project
cd semantic-resolution

# 2. Create virtual environment (optional but recommended)
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install langchain langchain-core langchain-community chromadb

# 4. Verify tokens file exists
# Create tokens/Tokens.xlsx with columns: Email, Token

# 5. Set PostgreSQL environment variables
# Windows:
set DB_HOST=inoscmm2181
set DB_PORT=30432
set DB_NAME=paasdb
set DB_USER=ossdb01ref
set DB_PASSWORD=ossdb01ref

# Linux/Mac:
export DB_HOST=inoscmm2181
export DB_PORT=30432
export DB_NAME=paasdb
export DB_USER=ossdb01ref
export DB_PASSWORD=ossdb01ref

# 6. Start the application
python app/sr_feedback_app.py
```

---

### 🐧 Linux/Mac Compatibility

| Feature | Windows | Linux/Mac |
|---------|---------|-----------|
| Flask Web App | ✅ Works | ✅ Works |
| RAG Pipeline | ✅ Works | ✅ Works |
| ChromaDB | ✅ Works | ✅ Works |
| Semantic Search | ✅ Works | ✅ Works |
| PostgreSQL Activity Lookup | ✅ Works | ✅ Works |
| **Outlook Email Fetcher** | ✅ Works | ❌ Not Supported |
| Team Management | ✅ Works | ✅ Works |

> ⚠️ **Linux Note**: The Outlook email fetcher (`email_fetcher.py`) uses Windows COM interface (`win32com`) and **only works on Windows**. On Linux/Mac, you must manually upload Excel files through the admin portal instead of automatic email fetching.

---

### 🔗 Access Points

After starting the application:

| Portal | URL | Credentials |
|--------|-----|-------------|
| User Portal | http://localhost:5000 | No login required |
| Admin Portal | http://localhost:5000/admin | admin / admin123 |

---

## 📁 Project Structure

```
sr-analyzer/
└── semantic-resolution/           # Main application directory
    ├── admin/                     # Admin portal functionality
    │   ├── email/                 # Outlook email integration
    │   │   ├── email_fetcher.py          # Fetch daily reports from Outlook
    │   │   └── email_to_rag_processor.py # Process email attachments
    │   └── upload/                # File upload processing
    │       ├── admin_upload_and_merge_with_rag.py  # Main upload flow
    │       └── admin_upload_and_merge.py           # Legacy upload
    │
    ├── analyzers/                 # SR Analysis Components
    │   ├── batch_sr_analyser.py          # AIEnhancedServiceRequestAnalyzer
    │   ├── comprehensive_sr_analyzer.py  # Wrapper for legacy compatibility
    │   └── sr_text_preprocessor.py       # Text cleaning for semantic search
    │
    ├── app/                       # Flask Web Application
    │   ├── sr_feedback_app.py     # Application entry point
    │   ├── routes/                # URL route handlers
    │   │   ├── admin.py           # Admin portal routes
    │   │   ├── user.py            # User portal routes
    │   │   ├── team.py            # Team management routes
    │   │   ├── api.py             # REST API endpoints
    │   │   └── auth.py            # Authentication routes
    │   └── utils/                 # Helper functions
    │       ├── helpers.py         # Utility functions
    │       ├── decorators.py      # Route decorators
    │       └── state.py           # Shared application state
    │
    ├── assignment/                # SR Assignment Logic
    │   ├── daily_data_manager.py         # Daily upload management
    │   └── priority_age_calculator.py    # Business day calculations
    │
    ├── config/                    # Configuration
    │   ├── settings.py            # Application settings
    │   └── paths.py               # Path constants
    │
    ├── data/                      # Data Storage
    │   ├── database/              # SQLite databases
    │   │   ├── people_skills.db   # Team skills & availability
    │   │   ├── sr_tracking.db     # SR tracking data
    │   │   └── abbreviation.db    # Abbreviation mappings
    │   └── vectorstore/           # Vector embeddings
    │       └── chromadb_store/    # ChromaDB collections
    │           ├── clean_history_data  # Historical SR embeddings
    │           ├── java_mapping        # Java class metadata
    │           └── comcast_code        # Backend code embeddings
    │
    ├── RAG/                       # RAG Pipeline Components
    │   ├── rag/                   # Core pipeline
    │   │   └── multi_model_rag_pipeline_chatgpt.py  # 5-LLM pipeline
    │   ├── pipeline/              # Pipeline utilities
    │   │   └── activity_name_finder.py  # PostgreSQL activity lookup
    │   ├── utils/                 # RAG utilities
    │   │   └── history_db_manager.py    # ChromaDB management
    │   ├── creation/              # Vectorstore creation scripts
    │   ├── input/                 # Input Excel files
    │   └── llm output/            # Generated results
    │
    ├── team/                      # Team Management
    │   └── people_skills_database.py    # Skills DB with ML learning
    │
    ├── user/                      # User Portal
    │   └── feedback/              # User feedback collection
    │       └── user_feedback_manager.py
    │
    ├── workaround/                # Workaround Tools
    │   ├── resolution_mapping_retriever.py  # Resolution search
    │   └── extract_workarounds_by_category.py
    │
    ├── templates/                 # HTML Templates
    ├── tokens/                    # API Token Storage
    ├── models/                    # ML Models (sentence-transformers)
    ├── input/                     # Input files staging
    └── output/                    # Output files
```

---

## ⚙️ Configuration

### API Tokens (`tokens/Tokens.xlsx`)
```
| Email                  | Token           |
|------------------------|-----------------|
| user1@company.com      | your-api-token1 |
| user2@company.com      | your-api-token2 |
```

### Team Configuration (`People.xlsx`)
```
| Team Member    | App     | Skill Level | Max Load | Specialization      |
|----------------|---------|-------------|----------|---------------------|
| John Smith     | SOM_MM  | 4.5/5       | 12       | Java/Provisioning   |
| Jane Doe       | SQO_MM  | 3.5/5       | 10       | Orders/Billing      |
```

### Environment Variables
```bash
# Optional: Override default paths
export SR_DATA_DIR=/path/to/data
export SR_TOKENS_FILE=/path/to/Tokens.xlsx
```

---

## 📖 Usage

### 1. Admin: Upload Daily SR Report
1. Navigate to `http://localhost:5000/admin`
2. Click "Upload Excel" and select your SR report
3. System automatically:
   - Runs semantic search
   - Executes 5-LLM pipeline
   - Merges to ChromaDB
   - Assigns team members
4. Download results from "Reports" section

### 2. User: Provide Feedback
1. Navigate to `http://localhost:5000`
2. Search for an SR by ID
3. View AI-generated workaround
4. Submit corrections if needed
5. Feedback is stored for ML improvement

### 3. Programmatic Usage
```python
from RAG.rag.multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline

# Initialize pipeline
pipeline = MultiModelSRPipeline(
    tokens_file="tokens/Tokens.xlsx",
    model_name="gpt-4.1"
)

# Analyze single SR
sr_data = {
    'SR ID': 'CAS123456',
    'Description': 'Network connectivity issue...',
    'Notes': 'Customer reports intermittent...',
    'Priority': 'P2'
}
result = pipeline.analyze_single_sr(sr_data)

# Access results
print(f"Is Java Error: {result['Is Java Error']}")
print(f"AI Workaround: {result['AI Workaround']}")
print(f"Assigned To: {result['Assigned To']}")
```

---

## 🔌 API Reference

### REST Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/analyze` | POST | Analyze single SR |
| `/api/search` | GET | Search historical SRs |
| `/api/feedback` | POST | Submit workaround feedback |
| `/api/team/status` | GET | Get team availability |
| `/admin/upload` | POST | Upload Excel file |

### Python API

```python
# Semantic Search
from RAG.utils.history_db_manager import HistoryDatabaseManager
manager = HistoryDatabaseManager()
results = manager.search_semantic("connectivity issue", top_k=5)

# Team Skills
from team.people_skills_database import PeopleSkillsDatabase
db = PeopleSkillsDatabase()
experts = db.get_top_experts("SOM_MM", top_n=3)

# Activity Lookup
from RAG.pipeline.activity_name_finder import ActivityFinder
finder = ActivityFinder()
result = finder.find_activity_implementation("ValidateAddress")
```

---

## 📊 Data Flow

```
1. INPUT: Excel Upload (SR Report)
        ↓
2. PREPROCESSING: Clean text, standardize columns
        ↓
3. SEMANTIC SEARCH: Query ChromaDB for similar SRs
        ↓
4. LLM PIPELINE: 5 specialized LLM calls
        ↓
5. VALIDATION: Activity names validated against PostgreSQL
        ↓
6. ASSIGNMENT: Skill-based team member selection
        ↓
7. OUTPUT: Excel with AI Workarounds + Assignments
        ↓
8. MERGE: Update ChromaDB with new SRs
```

---

## 🛠️ Development

### Adding New Team Members
1. Edit `People.xlsx` with new member details
2. Run: `python -c "from team.people_skills_database import PeopleSkillsDatabase; PeopleSkillsDatabase().load_people_from_excel()"`

### Creating New Vectorstore
```bash
cd semantic-resolution/RAG/creation
python create_history_vectorstore.py
```

### Running Tests
```bash
cd semantic-resolution
python -m pytest tests/
```

---

## 📝 License

Internal Use Only - Amdocs/Comcast Project

---

## 👥 Contributors

- **Praveer Dubey** - Lead Developer
- **Team** - SR Analysis & Support

---

*Last Updated: January 2026*
