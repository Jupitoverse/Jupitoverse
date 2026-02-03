# 🔐 Admin Module

> **Admin Portal Functionality: Email Integration & Upload Processing**

This module handles the administrative workflow for SR processing, including:
- Fetching daily reports from Outlook email
- Processing Excel uploads through the RAG pipeline
- Merging results to the historical database

---

## 🐧 Platform Compatibility

| Feature | Windows | Linux/Mac |
|---------|---------|-----------|
| Admin Portal (Web UI) | ✅ | ✅ |
| Excel Upload Processing | ✅ | ✅ |
| RAG Pipeline | ✅ | ✅ |
| ChromaDB Merge | ✅ | ✅ |
| **Outlook Email Fetcher** | ✅ | ❌ |

> ⚠️ **Linux/Mac Users**: The email fetcher requires Windows COM (`win32com`). Use the admin portal to manually upload Excel files instead of automatic email fetching.

---

## 📁 Structure

```
admin/
├── __init__.py
├── README.md
├── email/                        # Email integration
│   ├── __init__.py
│   ├── email_fetcher.py          # Outlook COM interface
│   ├── email_to_rag_processor.py # Email → RAG pipeline
│   ├── downloads/                # Downloaded attachments
│   └── README.md
└── upload/                       # File upload handling
    ├── __init__.py
    ├── admin_upload_and_merge_with_rag.py  # Main upload flow
    ├── admin_upload_and_merge.py           # Legacy (no RAG)
    └── README.md
```

---

## 🔄 Complete Admin Workflow

The admin upload process follows this 6-step workflow:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ADMIN UPLOAD WORKFLOW                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 1: ANALYZE                                                 │
│  ├── Read Excel file                                            │
│  ├── Clean data (remove blank rows, date footers)               │
│  ├── Standardize column names                                   │
│  └── Run semantic analysis (ComprehensiveSRAnalyzer)            │
│                                                                  │
│  Step 2: SAVE SEMANTIC RESULTS                                  │
│  └── Save to output/reports/Admin_Upload_TIMESTAMP.xlsx         │
│                                                                  │
│  Step 3: PREPARE RAG INPUT                                      │
│  ├── Merge semantic workarounds with original file              │
│  ├── Add Resolution Category and Status Reason                  │
│  └── Save to RAG/input/ folder                                  │
│                                                                  │
│  Step 4: RUN RAG PIPELINE                                       │
│  ├── Initialize MultiModelSRPipeline                            │
│  ├── Process all SRs through 5-LLM calls                        │
│  ├── Track LLM usage statistics                                 │
│  └── Save to RAG/llm output/ folder                             │
│                                                                  │
│  Step 5: MERGE TO CHROMADB                                      │
│  ├── Load RAG results (AI Workaround + Assigned To)             │
│  ├── For existing SRs: UPDATE (preserve user feedback)          │
│  ├── For new SRs: ADD to vectorstore                            │
│  └── Generate new embeddings                                    │
│                                                                  │
│  Step 5.5: INJECT TO VECTORSTORE                                │
│  └── Only inject NEW SRs (skip existing)                        │
│                                                                  │
│  Step 5.6: CLEANUP                                              │
│  └── Delete temporary files from RAG/input, RAG/output          │
│                                                                  │
│  Step 6: SUMMARY                                                │
│  ├── Display statistics                                         │
│  └── Show assignment distribution                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📧 Email Integration (Windows Only)

### `email_fetcher.py`

Fetches daily SR reports from Outlook using Windows COM interface.

> ⚠️ **Windows Only**: This feature uses `win32com` and requires:
> - Windows OS
> - Microsoft Outlook desktop app installed
> - User logged into Outlook

**Key Features:**
- No authentication needed (uses logged-in Outlook session)
- Auto-detects user email address
- Filters by sender and subject pattern
- Saves attachments to `downloads/email_reports/`

**Configuration:**
```python
SENDER_EMAIL = "GSSUTSMail@amdocs.com"
SUBJECT_PATTERN = "Scheduled Report - Mukul"
ATTACHMENT_PATTERN = "mukul"
```

**Usage:**
```python
from admin.email.email_fetcher import OutlookEmailFetcher

fetcher = OutlookEmailFetcher()
file_path, email_date = fetcher.fetch_latest_report(days_back=2)
```

**CLI Usage:**
```bash
# Fetch latest report
python email_fetcher.py

# Search last 5 days
python email_fetcher.py --days-back 5

# List recent emails (debug)
python email_fetcher.py --list
```

---

## 📤 Upload Processing

### `admin_upload_and_merge_with_rag.py`

Main function that orchestrates the complete admin workflow.

**Function Signature:**
```python
def upload_and_merge_with_rag(
    excel_path: str,
    progress_callback: Callable[[int, str], None] = None
) -> Tuple[bool, str, List]:
```

**Parameters:**
- `excel_path`: Path to the uploaded Excel file
- `progress_callback`: Optional callback for progress updates (percent, message)

**Returns:**
- `success`: Boolean indicating success/failure
- `output_path`: Path to saved analysis file
- `errors`: List of any errors encountered

**Key Functions:**

| Function | Description |
|----------|-------------|
| `clean_excel_data()` | Removes blank rows and date footer rows |
| `log()` | Logs message and calls progress callback |
| Semantic analysis | Uses `ComprehensiveSRAnalyzer` |
| RAG pipeline | Uses `MultiModelSRPipeline` |
| ChromaDB merge | Uses `HistoryDatabaseManager` |

---

## 🔧 Column Standardization

The upload process standardizes various column names:

```python
column_mapping = {
    'Call ID': ['SR ID', 'call id', 'sr id', 'Inc Call ID'],
    'Description': ['description', 'Issue Description', 'Inc Description'],
    'Notes': ['notes', 'Additional Notes', 'Resolution', 'Inc Resolution'],
    'Customer Priority': ['Priority', 'priority', 'UTS Priority'],
    'STATUS': ['Status', 'status', 'Inc Current EIR - Status'],
    'Assigned Group': ['Application', 'Assignee Support Group'],
    'Submit Date': ['Created Date', 'Inc Created Date'],
    'SLA Resolution Categorization T1': [...],
    'SLA Resolution Category': [...],
    'Resolution Categorization': [...]
}
```

---

## 📊 LLM Usage Tracking

The admin upload tracks and saves LLM usage statistics:

```json
{
  "last_updated": "2026-01-07T10:30:00",
  "last_run": {
    "total_calls": 25,
    "input_tokens": 50000,
    "output_tokens": 15000,
    "cost": 0.1234,
    "srs_processed": 5
  },
  "cumulative": {
    "total_cost": 12.34,
    "total_tokens": 500000,
    "total_calls": 250
  }
}
```

Saved to: `data/database/llm_usage_stats.json`

---

## ⚠️ Error Handling

The admin module includes robust error handling:

- **Excel cleaning**: Removes invalid rows without failing
- **RAG fallback**: Continues without AI workarounds if RAG fails
- **ChromaDB errors**: Logs and continues processing
- **File cleanup**: Gracefully handles file-in-use errors

---

## 🔗 Related Modules

- [RAG Pipeline](../RAG/README.md) - Multi-model LLM processing
- [Analyzers](../analyzers/README.md) - Semantic analysis
- [Data](../data/README.md) - ChromaDB and databases

---

*Part of SR-Analyzer Admin Module*
