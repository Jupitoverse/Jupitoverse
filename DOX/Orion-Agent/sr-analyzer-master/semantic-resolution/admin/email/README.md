# 📧 Email Module

> **Outlook Email Integration (Windows Only)**

Fetches daily SR reports from Outlook using Windows COM.

---

## ⚠️ Windows Only

This module uses Windows COM interface (`win32com`).

| Feature | Windows | Linux/Mac |
|---------|:-------:|:---------:|
| Email Fetcher | ✅ | ❌ |

**Linux/Mac**: Use manual Excel upload in admin portal.

---

## 📁 Structure

```
email/
├── README.md
├── __init__.py
├── email_fetcher.py          # Outlook COM interface
└── email_to_rag_processor.py # Email → RAG pipeline
```

---

## 📦 `email_fetcher.py`

### Class: `OutlookEmailFetcher`

Connects to Outlook and downloads attachments.

```python
from admin.email.email_fetcher import OutlookEmailFetcher

fetcher = OutlookEmailFetcher()
file_path, email_date = fetcher.fetch_latest_report(days_back=2)
```

### Configuration

```python
SENDER_EMAIL = "GSSUTSMail@amdocs.com"
SUBJECT_PATTERN = "Scheduled Report - Mukul"
ATTACHMENT_PATTERN = "mukul"
```

### Requirements

- Windows OS
- Outlook desktop app installed
- User logged into Outlook

### CLI Usage

```bash
# Fetch latest report
python email_fetcher.py

# Search last 5 days
python email_fetcher.py --days-back 5

# List recent emails
python email_fetcher.py --list
```

---

## 🔗 Related

- [admin/README.md](../README.md) - Admin module
- [upload/README.md](../upload/README.md) - Upload processing

---

*Part of SR-Analyzer Admin Module*
