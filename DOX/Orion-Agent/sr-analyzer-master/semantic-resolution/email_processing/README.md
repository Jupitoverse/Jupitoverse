# 📧 Email Processing Scripts

> **Standalone Email Processing Tools (Windows Only)**

---

## ⚠️ Windows Only

These scripts use Windows PowerShell and COM interfaces.

| Feature | Windows | Linux/Mac |
|---------|:-------:|:---------:|
| Email Scripts | ✅ | ❌ |

---

## 📁 Structure

```
email_processing/
├── README.md
├── fetch_outlook_attachments.ps1   # PowerShell script
└── fetch_outlook_emails.bat        # Batch wrapper
```

---

## 📄 Scripts

### `fetch_outlook_emails.bat`

Batch wrapper to run PowerShell script:

```cmd
fetch_outlook_emails.bat
```

### `fetch_outlook_attachments.ps1`

PowerShell script to:
- Connect to Outlook via COM
- Search for SR report emails
- Download Excel attachments

---

## 🔧 Usage

```cmd
cd email_processing
fetch_outlook_emails.bat
```

---

## ⚠️ Requirements

- Windows OS
- Outlook desktop app installed
- User logged into Outlook
- PowerShell execution policy allows scripts

---

## 🔗 Related

- [admin/email/README.md](../admin/email/README.md) - Python email fetcher

---

*Part of SR-Analyzer Project*
