# 📧 Email Processing Module

> **Automatic Outlook Email Fetching**

This folder contains scripts for automatically fetching daily SR reports from Outlook emails.

---

## ⚠️ Platform Compatibility

| Platform | Status |
|----------|--------|
| **Windows** | ✅ Fully Supported |
| **Linux** | ❌ NOT Supported |
| **Mac** | ❌ NOT Supported |

> **Why Windows Only?** This module uses `win32com` (Windows COM interface) to connect to Microsoft Outlook. This API is only available on Windows. On Linux/Mac, use manual Excel upload via the admin portal instead.

---

## 📁 Structure

```
email/
├── README.md
└── email_processing/
    └── email_fetcher.py     # Main email fetcher
```

---

## 📦 Main File: `email_fetcher.py`

### Class: `OutlookEmailFetcher`

Fetches daily SR reports from Outlook using Windows COM interface.

```python
from email_processing.email_fetcher import OutlookEmailFetcher

fetcher = OutlookEmailFetcher(
    output_dir="data/email_downloads"
)

# Fetch latest report
file_path = fetcher.fetch_latest_report(days_back=7)
if file_path:
    print(f"Downloaded: {file_path}")
```

---

## 🔧 Configuration

Located at top of `email_fetcher.py`:

```python
# Email filtering criteria
SENDER_EMAIL = "report-sender@company.com"
SUBJECT_PATTERN = r"Daily.*SR.*Report"
ATTACHMENT_PATTERN = r".*\.xlsx?$"
```

| Setting | Default | Description |
|---------|---------|-------------|
| SENDER_EMAIL | configured | Expected sender address |
| SUBJECT_PATTERN | regex | Subject line pattern |
| ATTACHMENT_PATTERN | *.xls* | Attachment filename pattern |
| OUTPUT_DIR | data/email_downloads | Download location |

---

## 🔄 Fetch Flow

```
1. Connect to Outlook via COM
2. Access inbox folder
3. Search for emails matching:
   - Sender: SENDER_EMAIL
   - Subject: SUBJECT_PATTERN
   - Date: Within last N days
4. Find attachment matching ATTACHMENT_PATTERN
5. Save attachment to OUTPUT_DIR
6. Return file path
```

---

## 📋 Key Methods

### `__init__(self, output_dir=None)`
Initialize fetcher with output directory.

### `fetch_latest_report(self, days_back=7) -> Optional[str]`
Fetch the most recent matching email attachment.

```python
# Fetch report from last 7 days
file_path = fetcher.fetch_latest_report(days_back=7)
```

### `list_recent_emails(self, days_back=3) -> List[Dict]`
Debug method to list recent emails.

```python
# List emails for debugging
emails = fetcher.list_recent_emails(days_back=3)
for email in emails:
    print(f"From: {email['sender']}")
    print(f"Subject: {email['subject']}")
    print(f"Has Attachments: {email['has_attachments']}")
```

---

## ⚠️ Requirements

- **Windows Only**: Uses win32com for Outlook
- **Outlook Installed**: Desktop Outlook required
- **Logged In**: User must be logged into Outlook
- **Network Access**: Email sync required

### Installation
```bash
pip install pywin32
```

---

## 🔧 Integration with Admin Upload

The email fetcher is used by `admin_upload_and_merge_with_rag.py`:

```python
from email_processing.email_fetcher import OutlookEmailFetcher

# Step 0: Fetch latest email report
fetcher = OutlookEmailFetcher()
report_path = fetcher.fetch_latest_report()

if report_path:
    # Process the downloaded report
    upload_and_merge_with_rag(report_path)
```

---

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| COM Error | Restart Outlook, check permissions |
| No emails found | Verify sender/subject patterns |
| Attachment missing | Check ATTACHMENT_PATTERN regex |
| Permission denied | Run as same user as Outlook |

---

*Part of SR-Analyzer Admin Module*
