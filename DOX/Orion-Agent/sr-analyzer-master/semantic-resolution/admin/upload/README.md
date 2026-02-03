# 📤 Upload Module

> **Excel Upload Processing with RAG Integration**

Handles Excel file uploads through the complete RAG pipeline.

---

## 📁 Structure

```
upload/
├── README.md
├── __init__.py
├── admin_upload_and_merge_with_rag.py  # Main upload flow
└── admin_upload_and_merge.py           # Legacy (no RAG)
```

---

## 📦 `admin_upload_and_merge_with_rag.py`

### Main Function

```python
from admin.upload.admin_upload_and_merge_with_rag import upload_and_merge_with_rag

success, output_path, errors = upload_and_merge_with_rag(
    excel_path="input/report.xlsx",
    progress_callback=lambda pct, msg: print(f"{pct}%: {msg}")
)
```

### Workflow

```
Step 1: Read & Clean Excel
├── Remove blank rows
├── Remove date footer rows
└── Standardize column names

Step 2: Semantic Analysis
├── Run ComprehensiveSRAnalyzer
└── Find similar historical SRs

Step 3: Save Semantic Results
└── output/reports/Admin_Upload_TIMESTAMP.xlsx

Step 4: RAG Pipeline
├── Run MultiModelSRPipeline
├── 5 LLM calls per SR
└── Generate AI workarounds

Step 5: Merge to ChromaDB
├── Update existing SRs
├── Add new SRs
└── Preserve user feedback

Step 6: Cleanup
└── Delete temporary files
```

### Column Mapping

| Standard | Alternatives |
|----------|--------------|
| Call ID | SR ID, call id, Inc Call ID |
| Description | description, Issue Description |
| Notes | notes, Resolution, Inc Resolution |
| Priority | Customer Priority, UTS Priority |

---

## 🔗 Related

- [admin/README.md](../README.md) - Admin module
- [RAG/README.md](../../RAG/README.md) - RAG pipeline

---

*Part of SR-Analyzer Admin Module*
