# 🔐 Admin Module

> **Admin Portal: Email Integration & Upload Processing**

This module handles the administrative workflow for SR processing.

---

## 🚀 Quick Start

> **See [USER_ADMIN_GUIDE.md](../USER_ADMIN_GUIDE.md) for complete admin instructions**

**Access**: http://localhost:5000/admin  
**Credentials**: `admin` / `admin123`

---

## 🐧 Platform Compatibility

| Feature | Windows | Linux/Mac |
|---------|:-------:|:---------:|
| Admin Portal (Web UI) | ✅ | ✅ |
| Excel Upload Processing | ✅ | ✅ |
| RAG Pipeline | ✅ | ✅ |
| ChromaDB Merge | ✅ | ✅ |
| **Outlook Email Fetcher** | ✅ | ❌ |

> ⚠️ **Linux/Mac**: Email fetcher requires Windows COM. Use manual upload instead.

---

## 📁 Structure

```
admin/
├── __init__.py
├── README.md
├── email/                        # Email integration
│   ├── email_fetcher.py          # Outlook COM interface (Windows)
│   ├── email_to_rag_processor.py # Email → RAG pipeline
│   └── README.md
└── upload/                       # File upload handling
    ├── admin_upload_and_merge_with_rag.py  # Main upload flow
    ├── admin_upload_and_merge.py           # Legacy (no RAG)
    └── README.md
```

---

## 🔄 Admin Upload Workflow

```
Step 1: UPLOAD
├── Admin uploads Excel file via web portal
├── File saved to input/ folder
└── Data cleaned (blank rows, date footers removed)

Step 2: SEMANTIC ANALYSIS
├── Each SR analyzed with ComprehensiveSRAnalyzer
├── Finds similar historical SRs
└── Extracts semantic workarounds

Step 3: SAVE SEMANTIC RESULTS
└── Saved to output/reports/Admin_Upload_TIMESTAMP.xlsx

Step 4: RAG PIPELINE
├── Initialize MultiModelSRPipeline
├── Run 5-LLM calls per SR
└── Generate AI workarounds + assignments

Step 5: MERGE TO CHROMADB
├── Existing SRs: UPDATE (preserve user feedback)
├── New SRs: ADD to vectorstore
└── Regenerate embeddings

Step 6: CLEANUP
└── Delete temporary files
```

---

## 📧 Email Fetcher (Windows Only)

### How It Works

```python
# Uses Windows COM to connect to Outlook
import win32com.client
outlook = win32com.client.Dispatch("Outlook.Application")
```

### Configuration

```python
# In email_fetcher.py
SENDER_EMAIL = "GSSUTSMail@amdocs.com"
SUBJECT_PATTERN = "Scheduled Report - Mukul"
ATTACHMENT_PATTERN = "mukul"
```

### Usage

```python
from admin.email.email_fetcher import OutlookEmailFetcher

fetcher = OutlookEmailFetcher()
file_path, email_date = fetcher.fetch_latest_report(days_back=2)
```

---

## 📤 Upload Processing

### Main Function

```python
from admin.upload.admin_upload_and_merge_with_rag import upload_and_merge_with_rag

success, output_path, errors = upload_and_merge_with_rag(
    excel_path="input/report.xlsx",
    progress_callback=lambda pct, msg: print(f"{pct}%: {msg}")
)
```

### Excel Column Mapping

The system auto-maps various column names:

| Standard | Alternatives |
|----------|--------------|
| Call ID | SR ID, call id, Inc Call ID |
| Description | description, Issue Description |
| Notes | notes, Resolution, Inc Resolution |
| Priority | Customer Priority, UTS Priority |

---

## 📊 LLM Usage Tracking

Saved to `data/database/llm_usage_stats.json`:

```json
{
  "last_run": {
    "total_calls": 25,
    "input_tokens": 50000,
    "output_tokens": 15000,
    "cost": 0.12,
    "srs_processed": 5
  },
  "cumulative": {
    "total_cost": 12.34,
    "total_tokens": 500000
  }
}
```

---

## 🔗 Related

- [email/README.md](email/README.md) - Email fetcher details
- [upload/README.md](upload/README.md) - Upload processing
- [RAG/README.md](../RAG/README.md) - RAG pipeline

---

*Part of SR-Analyzer Admin Module*
