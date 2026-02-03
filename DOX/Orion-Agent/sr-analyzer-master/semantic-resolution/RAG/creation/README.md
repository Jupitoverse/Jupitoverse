# 🔨 RAG Creation Module

> **Vectorstore Creation Scripts**

Scripts for creating and populating ChromaDB vectorstores.

---

## 📁 Structure

```
creation/
├── __init__.py
├── README.md
├── create_history_vectorstore.py        # Main history store
├── create_clean_history_vectorstore.py  # Clean history store
├── create_abbreviation_vectorstore.py   # Abbreviation embeddings
├── create_workaround_comments_vectorstore.py
└── add_new_training_data.py             # Incremental updates
```

---

## 📦 Scripts

### `create_history_vectorstore.py`

Creates ChromaDB from historical Excel data.

```bash
python create_history_vectorstore.py
```

### `create_clean_history_vectorstore.py`

Creates the `clean_history_data` collection.

```bash
python create_clean_history_vectorstore.py
```

### `create_abbreviation_vectorstore.py`

Creates abbreviation embeddings.

```bash
python create_abbreviation_vectorstore.py
```

### `add_new_training_data.py`

Incrementally adds new data to existing store.

```bash
python add_new_training_data.py --input new_data.xlsx
```

---

## 🔧 Process

```
1. Load Excel/CSV data
2. Clean and preprocess text
3. Generate embeddings (all-MiniLM-L6-v2)
4. Create/update ChromaDB collection
5. Store with metadata
```

---

## ⚠️ Notes

- Full creation takes hours for 1M+ records
- Requires ~2GB disk space
- Use `add_new_training_data.py` for incremental updates

---

## 🔗 Related

- [RAG/README.md](../README.md) - RAG module
- [data/README.md](../../data/README.md) - Data storage

---

*Part of SR-Analyzer RAG Module*
