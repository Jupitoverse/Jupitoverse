# 🚀 SR-Analyzer

> **AI-Powered Service Request Analysis System**

An intelligent SR triage and resolution system using a 5-LLM RAG pipeline, semantic search across 1.18M+ historical records, and skill-based team assignment.

---

## 🎯 What It Does

| Feature | Description |
|---------|-------------|
| 🔍 **Semantic Search** | Finds similar SRs from 1.18M+ records using AI embeddings |
| 🤖 **5-LLM Pipeline** | Generates intelligent workarounds using GPT-4.1 |
| ☕ **Java Detection** | 5-source voting to detect backend/Java errors |
| 👥 **Smart Assignment** | Assigns SRs based on team skills and availability |
| 📝 **Learning System** | Improves from user feedback and corrections |

---

## 🚀 Quick Start

### First Time Setup

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

### Regular Startup

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

### Access Points

| Portal | URL | Credentials |
|--------|-----|-------------|
| **User Portal** | http://localhost:5000 | None required |
| **Admin Portal** | http://localhost:5000/admin | `admin` / `admin123` |

---

## 🐧 Platform Compatibility

| Feature | Windows | Linux/Mac |
|---------|:-------:|:---------:|
| Web Application | ✅ | ✅ |
| RAG Pipeline | ✅ | ✅ |
| Semantic Search | ✅ | ✅ |
| Java Detection | ✅ | ✅ |
| Team Assignment | ✅ | ✅ |
| User Feedback | ✅ | ✅ |
| **Outlook Email Fetch** | ✅ | ❌ |

> ⚠️ **Linux Note**: Email fetching requires Windows Outlook. Use manual Excel upload instead.

---

## 📁 Project Structure

```
sr-analyzer/
└── semantic-resolution/          # Main application
    ├── app/                      # Flask web application
    ├── admin/                    # Admin portal & email
    ├── RAG/                      # 5-LLM RAG pipeline
    │   └── pipeline/             # Core pipeline files
    ├── analyzers/                # SR analysis engine
    ├── team/                     # Team skills database
    ├── data/                     # Databases & vectorstores
    ├── templates/                # HTML templates
    ├── tokens/                   # API tokens
    ├── First_time_MultiModel.bat # First-time setup (Win)
    └── START_MULTIMODEL_RAG.bat  # Regular startup (Win)
```

---

## 🔧 Requirements

- **Python**: 3.10, 3.11, or 3.12
- **API Tokens**: `tokens/Tokens.xlsx`
- **Network**: Access to `ai-framework1:8085`

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [USER_ADMIN_GUIDE.md](semantic-resolution/USER_ADMIN_GUIDE.md) | Complete user and admin guide |
| [TECHNICAL_SPECIFICATIONS.md](semantic-resolution/TECHNICAL_SPECIFICATIONS.md) | Technical architecture details |
| [semantic-resolution/README.md](semantic-resolution/README.md) | Module documentation |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    5-LLM RAG PIPELINE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Excel Upload → Semantic Search → 5 LLM Calls → Assignment     │
│                                                                  │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌───────┐ ┌──────┐       │
│   │ LLM 1   │ │ LLM 2   │ │ LLM 3   │ │LLM 4  │ │LLM 5 │       │
│   │Workaround│ │Java Vote│ │Activity │ │Resolve│ │Assign│       │
│   └─────────┘ └─────────┘ └─────────┘ └───────┘ └──────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 👥 Contributors

- **Praveer Dubey** - Lead Developer

---

*Last Updated: January 2026*
