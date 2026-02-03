# 📥 Input Module

> **Input File Staging Area**

This folder serves as a staging area for uploaded Excel files before they are processed by the RAG pipeline.

---

## 📁 Structure

```
input/
├── README.md
└── *.xls, *.xlsx          # Uploaded Excel files
```

---

## 🔄 File Lifecycle

```
1. Admin uploads Excel → saved to input/
2. Pipeline processes file
3. Results saved to RAG/llm output/
4. Original file renamed with timestamp
5. Cleanup removes old files
```

---

## 📋 Expected File Format

Uploaded Excel files should contain these columns:

| Column | Required | Description |
|--------|----------|-------------|
| Call ID / SR ID | ✅ | Service Request identifier |
| Description | ✅ | SR description text |
| Notes | Optional | Additional notes/resolution |
| Priority | Optional | P1, P2, P3, P4 |
| Status | Optional | Current status |
| Application | Optional | Application area |
| Submit Date | Optional | Creation date |

---

## 🔧 File Naming Convention

Files are renamed after upload with timestamps:

```
upload_YYYYMMDD_HHMMSS_originalname.xlsx

Example:
upload_20260107_103000_Daily_Report.xlsx
```

---

## 🧹 Cleanup

Old files are automatically cleaned during admin upload:

```python
# Files older than processing are deleted
for excel_file in input_dir.glob("*.xlsx"):
    if is_processed(excel_file):
        excel_file.unlink()
```

---

## ⚠️ Notes

- Files are processed in order of modification time (newest first)
- Only one file is processed per run
- Large files (>16MB) are rejected by the web interface
- Supported formats: `.xls`, `.xlsx`

---

*Part of SR-Analyzer Input Module*
