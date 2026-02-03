# 📊 LLM Output Folder

> **Generated Analysis Results**

Contains Excel files with RAG pipeline results.

---

## 📁 Structure

```
llm output/
├── README.md
└── RAG_Analysis_TIMESTAMP.xlsx
```

---

## 📋 Output Format

| Column | Description |
|--------|-------------|
| SR ID | Service Request ID |
| Description | Original description |
| Notes | Original notes |
| Priority | P1, P2, P3, P4 |
| Is Java Error | Yes/No |
| Confidence | HIGH/MEDIUM/LOW/VERY_LOW |
| Java Votes | Count of JAVA votes |
| Non-Java Votes | Count of NON_JAVA votes |
| Activity Names | Validated activities |
| Implementation Classes | Java class paths |
| AI Workaround | Generated resolution |
| Semantic Workaround Used | Source workaround |
| Assigned To | Team member |

---

## 🧹 Cleanup

Files are automatically deleted after merging to ChromaDB.

---

## 🔗 Related

- [RAG/README.md](../README.md) - RAG pipeline

---

*Part of SR-Analyzer RAG Module*
