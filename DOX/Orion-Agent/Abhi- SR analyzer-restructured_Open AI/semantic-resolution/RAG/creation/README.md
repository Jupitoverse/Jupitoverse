# 🔨 RAG Creation Module

> **Database and Vectorstore Creation Scripts**

This folder contains scripts for creating and initializing the various databases and vectorstores used by the RAG pipeline.

---

## 📁 Structure

```
creation/
├── README.md
├── create_chromadb_store.py     # Main ChromaDB creation
├── create_java_mapping.py       # Java mapping database
├── create_abbreviations_db.py   # Abbreviations lookup
└── create_comcast_code_db.py    # Backend code vectorstore
```

---

## 📦 Scripts

### `create_chromadb_store.py`
Creates the main ChromaDB vectorstore from historical SR data.

```python
# Usage
python creation/create_chromadb_store.py

# Creates:
# - data/vectorstore/chromadb_store/
# - Collection: clean_history_data
```

**Process:**
1. Load Excel/CSV historical data
2. Generate embeddings with all-MiniLM-L6-v2
3. Store in ChromaDB with metadata

### `create_java_mapping.py`
Creates the Java class mapping database.

```python
# Usage
python creation/create_java_mapping.py

# Creates:
# - data/database/javaMapping.db (SQLite)
# - ChromaDB collection: java_mapping
```

**Process:**
1. Scan Java source files
2. Extract class names, methods, packages
3. Create SQLite lookup + vector embeddings

### `create_abbreviations_db.py`
Creates the abbreviations lookup database.

```python
# Usage
python creation/create_abbreviations_db.py

# Creates:
# - data/database/abbreviations.db (SQLite)
```

**Process:**
1. Load abbreviation mappings
2. Create full-text search index
3. Store in SQLite with FTS5

### `create_comcast_code_db.py`
Creates the backend code vectorstore for semantic search.

```python
# Usage
python creation/create_comcast_code_db.py

# Creates:
# - ChromaDB collection: comcast_code
```

**Process:**
1. Parse Java/backend code files
2. Chunk code into semantic units
3. Generate embeddings and store

---

## 🔧 Running All Scripts

```bash
# From semantic-resolution directory
python creation/create_chromadb_store.py
python creation/create_java_mapping.py
python creation/create_abbreviations_db.py
python creation/create_comcast_code_db.py
```

---

## ⚠️ Prerequisites

- Source data files in correct locations
- Sufficient disk space (~2GB for full vectorstore)
- sentence-transformers package installed

---

*Part of SR-Analyzer RAG Module*
