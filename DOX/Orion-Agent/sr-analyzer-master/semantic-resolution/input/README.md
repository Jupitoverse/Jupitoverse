# 📥 Input Module

> **Input File Staging Area**

Staging area for uploaded Excel files.

---

## 📁 Structure

```
input/
├── README.md
└── *.xlsx    # Uploaded files (temporary)
```

---

## 🔄 Usage

1. **Admin Upload**: Files saved here via web portal
2. **Processing**: Files read by RAG pipeline
3. **Cleanup**: Files deleted after processing

---

## 📋 Expected Format

| Column | Required | Description |
|--------|----------|-------------|
| Call ID | ✅ | SR identifier |
| Description | ✅ | Issue description |
| Notes | Optional | Additional details |
| Priority | Optional | P1, P2, P3, P4 |
| Application | Optional | SOM_MM, SQO_MM |

---

## ⚠️ Notes

- Files are deleted after successful processing
- Only `.xls` and `.xlsx` supported
- Max file size: 50MB

---

## 🔗 Related

- [admin/README.md](../admin/README.md) - Upload handling

---

*Part of SR-Analyzer Input Module*
