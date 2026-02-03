# 🚀 Orionverse Agent

> **Combined Web Portal + AI-Powered SR Analysis**

A unified platform that integrates the **Orionverse Hub** (web portal) with **Smart SR Assignment** (RAG-based AI analysis) for comprehensive service request management.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## 🌟 Overview

**Orionverse Agent** combines two powerful systems:

| Component | Description |
|-----------|-------------|
| **Orionverse Hub** | Web portal for SR search, bulk handling, billing, workarounds |
| **Smart SR Assignment** | RAG pipeline for AI-powered SR analysis and team assignment |

### Key Capabilities

- 🔍 **Search Anything**: Search across 32K+ SRs and 3K+ defects
- 🤖 **AI Analysis**: RAG-based workaround suggestions and resolution
- 👥 **Team Assignment**: Intelligent SR routing based on skills
- 📊 **Bulk Handling**: Process multiple SRs efficiently
- 📝 **Workaround Database**: Community-driven knowledge base

---

## ✨ Features

### Web Portal (Orionverse Hub)
- **Home Dashboard** - Quick access to all features
- **Search Anything** - Full-text search across SR/Defect databases
- **Bulk Handling** - B1-B6 bulk operations for SR management
- **Billing** - Revenue and rebilling reports
- **Workarounds** - Create, edit, and share solutions
- **Team Management** - Skills tracking and assignments

### AI Module (Smart SR Assignment)
- **Single SR Analysis** - Analyze individual SRs with RAG pipeline
- **Semantic Search** - Find similar historical SRs using vector similarity
- **Java Error Detection** - Automatic classification of Java vs non-Java issues
- **Activity Extraction** - Extract activity names from SR descriptions
- **Workaround Suggestions** - AI-generated resolution recommendations
- **Batch Processing** - Analyze multiple SRs at once

---

## 📁 Project Structure

```
Abhi-Orionverse Agent/
├── 📄 index.html                 # Main entry point (SPA)
├── 📄 README.md                  # This file
├── 📄 requirements.txt           # Python dependencies
│
├── 📂 backend/                   # Flask backend server
│   ├── app.py                    # Main Flask application
│   ├── database.py               # Database connections
│   ├── 📂 data/                  # JSON data files
│   │   ├── sr_data.json          # 32K+ SR records
│   │   └── defect_data.json      # 3K+ defect records
│   └── 📂 routes/                # API route blueprints
│       ├── auth.py               # Authentication
│       ├── search.py             # Search API
│       ├── workarounds.py        # Workaround CRUD
│       ├── bulk_handling.py      # Bulk operations
│       ├── billing.py            # Billing reports
│       └── smart_sr.py           # 🆕 RAG integration
│
├── 📂 static/                    # Frontend assets
│   ├── 📂 css/
│   │   └── style.css             # Main stylesheet
│   └── 📂 js/
│       ├── main.js               # App initialization
│       ├── api.js                # API client
│       ├── auth.js               # Authentication
│       ├── search.js             # Search functionality
│       ├── bulk_handling.js      # Bulk operations
│       └── smart_sr.js           # 🆕 Smart SR module
│
├── 📂 templates/                 # HTML page templates
│   ├── home.html
│   ├── search_anything.html
│   ├── bulk_handling.html
│   ├── smart_sr_assignment.html  # 🆕 AI Analysis page
│   └── ... (other pages)
│
├── 📂 rag_module/                # 🆕 RAG Pipeline Module
│   ├── 📂 RAG/
│   │   └── 📂 pipeline/
│   │       └── multi_model_rag_pipeline_chatgpt.py
│   ├── 📂 data/
│   │   ├── 📂 vectorstore/       # ChromaDB vector store
│   │   └── 📂 database/          # SQLite databases
│   ├── 📂 models/                # Sentence transformers
│   ├── 📂 tokens/                # API tokens
│   └── README.md                 # RAG module documentation
│
└── 📂 docs/                      # Additional documentation
    ├── ARCHITECTURE.md
    ├── DEVELOPER_GUIDE.md
    └── ...
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 - 3.12
- pip (Python package manager)
- Chrome/Edge browser (recommended)

### Installation

1. **Clone/Navigate to project directory**
   ```bash
   cd "C:\Users\abhisha3\Desktop\Projects\DOX\Orion-Agent\Abhi-Orionverse Agent"
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install flask flask-cors langchain chromadb sentence-transformers
   ```

3. **Start the backend server**
   ```bash
   cd backend
   python app.py
   ```

4. **Start the frontend server** (in a new terminal)
   ```bash
   cd "C:\Users\abhisha3\Desktop\Projects\DOX\Orion-Agent\Abhi-Orionverse Agent"
   python -m http.server 8080
   ```

5. **Open in browser**
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:5001

### Quick Start Scripts

**Windows:**
```batch
@echo off
start cmd /k "cd backend && python app.py"
start cmd /k "python -m http.server 8080"
timeout /t 3
start http://localhost:8080
```

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        ORIONVERSE AGENT                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐         ┌─────────────────────────────┐   │
│  │    Frontend     │         │         Backend             │   │
│  │  (Port 8080)    │ ◀─────▶ │      (Port 5001)           │   │
│  │                 │  HTTP    │                             │   │
│  │  ├─ index.html  │         │  ├─ Flask App               │   │
│  │  ├─ static/js/  │         │  │   ├─ search.py           │   │
│  │  └─ templates/  │         │  │   ├─ workarounds.py      │   │
│  │                 │         │  │   ├─ bulk_handling.py    │   │
│  └─────────────────┘         │  │   └─ smart_sr.py ────────┼───┤
│                              │  │                          │   │
│                              │  └─ data/                   │   │
│                              │      ├─ sr_data.json        │   │
│                              │      └─ defect_data.json    │   │
│                              └─────────────────────────────┘   │
│                                           │                     │
│                                           │ RAG Integration     │
│                                           ▼                     │
│                              ┌─────────────────────────────┐   │
│                              │       RAG Module            │   │
│                              │      (rag_module/)          │   │
│                              │                             │   │
│                              │  ├─ Multi-Model Pipeline    │   │
│                              │  │   └─ 5 LLM Calls         │   │
│                              │  ├─ ChromaDB Vectorstore    │   │
│                              │  │   └─ 1.18M+ records      │   │
│                              │  ├─ Sentence Transformers   │   │
│                              │  └─ Team Skills DB          │   │
│                              └─────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### RAG Pipeline Flow

```
SR Input → Semantic Search → Java Detection → Activity Extraction → Resolution → Assignment
    │            │                 │                │                  │           │
    └────────────┴─────────────────┴────────────────┴──────────────────┴───────────┘
                              5 Focused LLM Calls
```

---

## 📡 API Reference

### Orionverse Hub APIs

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/search/all` | GET | Get initial data (5 SRs, 5 Defects) |
| `/api/search/filter` | POST | Search with filters |
| `/api/workarounds` | GET/POST | CRUD workarounds |
| `/api/bulk-handling/*` | POST | Bulk operations (B1-B6) |
| `/api/auth/login` | POST | User authentication |

### Smart SR APIs (NEW)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/smart-sr/status` | GET | Check RAG system status |
| `/api/smart-sr/stats` | GET | Get system statistics |
| `/api/smart-sr/analyze` | POST | Analyze single SR |
| `/api/smart-sr/batch-analyze` | POST | Batch SR analysis |
| `/api/smart-sr/semantic-search` | POST | Semantic similarity search |
| `/api/smart-sr/workaround-suggestions` | POST | Get AI suggestions |
| `/api/smart-sr/team-assignment` | POST | Get team assignment |

### Example: Analyze SR

```javascript
fetch('/api/smart-sr/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        sr_id: 'SR-12345',
        description: 'Customer unable to place order...',
        category: 'Order Management',
        customer_id: 'CUST001'
    })
})
.then(res => res.json())
.then(result => {
    console.log(result.analysis.semantic_workaround);
    console.log(result.analysis.assigned_to);
});
```

---

## ⚙️ Configuration

### Backend Configuration (backend/app.py)

```python
app.run(
    host='0.0.0.0',    # Listen on all interfaces
    port=5001,         # Backend port
    debug=True,        # Development mode
    threaded=True      # Multi-threaded
)
```

### RAG Module Configuration (rag_module/config/settings.py)

- **Vectorstore**: ChromaDB at `rag_module/data/vectorstore/chromadb_store`
- **Database**: SQLite at `rag_module/data/database/`
- **Models**: Sentence transformers at `rag_module/models/`
- **Tokens**: API tokens at `rag_module/tokens/Tokens.xlsx`

### Environment Variables

```bash
# Database connection (for PostgreSQL activity lookup)
DB_HOST=inoscmm2181
DB_PORT=30432
DB_NAME=paasdb
DB_USER=ossdb01ref
DB_PASSWORD=ossdb01ref
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Backend won't start
```bash
# Check if port is in use
netstat -ano | findstr :5001

# Kill process if needed
taskkill /PID <pid> /F
```

#### 2. RAG module not loading
```bash
# Verify vectorstore exists
dir rag_module\data\vectorstore\chromadb_store

# Check API status
curl http://localhost:5001/api/smart-sr/status
```

#### 3. Unicode errors on Windows
The app includes encoding fixes, but if you see errors:
```python
# Already in app.py, but can add to other files:
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
```

#### 4. Module not found errors
```bash
# Ensure all dependencies installed
pip install -r requirements.txt
pip install -r rag_module/requirements.txt
```

---

## 📊 Data Sources

| Source | Records | Location |
|--------|---------|----------|
| SR Data | 32,730+ | `backend/data/sr_data.json` |
| Defect Data | 2,979+ | `backend/data/defect_data.json` |
| Historical SRs | 1.18M+ | `rag_module/data/vectorstore/` |
| Java Classes | 11,795+ | `rag_module/data/vectorstore/` |
| Team Skills | Dynamic | `rag_module/data/database/people_skills.db` |

---

## 👥 Team

- **Orionverse Hub**: Amdocs Orion Team
- **RAG Module**: SR-Analyzer Team

---

## 📝 Changelog

### v5.0.0 (2026-01-12)
- 🆕 Integrated Smart SR Assignment with RAG pipeline
- 🆕 Added AI-powered SR analysis
- 🆕 Added semantic search functionality
- 🔧 Combined Orionverse Hub + RAG module
- 📚 Comprehensive documentation

### v4.0.0
- Search Anything with 32K+ SRs
- Bulk Handling (B1-B6)
- Workaround database

---

## 📄 License

Internal use only - Amdocs

---

*Built with ❤️ by the Orion Team*
