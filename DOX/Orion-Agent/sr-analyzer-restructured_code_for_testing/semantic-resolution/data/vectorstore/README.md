# 🗃️ Vectorstore Module

> **ChromaDB Vector Database for Semantic Search**

This folder contains the ChromaDB vector store and tools for managing vector embeddings.

---

## 📁 Structure

```
vectorstore/
├── README.md
├── chromadb_store/                    # Main ChromaDB database
│   ├── chroma.sqlite3                 # SQLite metadata
│   └── [collection-ids]/              # Collection data directories
│       ├── data_level0.bin            # Vector data
│       ├── header.bin                 # Index header
│       ├── index_metadata.pickle      # Index metadata
│       ├── length.bin                 # Vector lengths
│       └── link_lists.bin             # HNSW graph links
├── historical data injector/          # Data injection tools
│   ├── push_historical_data.py
│   └── README.txt
└── vectorstore_creation/              # Creation scripts
    ├── create_vectorstore.py
    └── historical data excel/
```

---

## 📊 ChromaDB Collections

### `clean_history_data`
**Purpose**: Historical SR data for semantic search

| Field | Type | Description |
|-------|------|-------------|
| call_id | string | SR ID (uppercase) |
| description | string | SR description |
| wl_summary | string | Notes/summary |
| workaround | string | Original workaround |
| ai_generated_workaround | string | RAG-generated workaround |
| user_corrected_workaround | string | JSON array of user corrections |
| resolution_categorization | string | Resolution category |
| application | string | Application area |
| priority | string | P1-P4 |
| assigned_to | string | Team member |

**Stats**: ~1,180,000 records

### `java_mapping`
**Purpose**: Java class metadata for code lookup

| Field | Type | Description |
|-------|------|-------------|
| class_name | string | Java class name |
| package | string | Package path |
| file_path | string | Source file location |
| class_type | string | Service, Activity, etc. |
| methods | string | Key method names |

### `comcast_code`
**Purpose**: Backend code for semantic code search

| Field | Type | Description |
|-------|------|-------------|
| code_chunk | string | Code snippet |
| file_path | string | Source file path |
| class_name | string | Class containing code |
| method_name | string | Method name |

---

## 🔧 Usage

### Connect to ChromaDB

```python
import chromadb
from chromadb.config import Settings

client = chromadb.PersistentClient(
    path="data/vectorstore/chromadb_store",
    settings=Settings(anonymized_telemetry=False)
)

# Get collection
collection = client.get_collection("clean_history_data")
print(f"Records: {collection.count()}")
```

### Semantic Search

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
query_embedding = model.encode("network connectivity issue")

results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=10,
    include=["documents", "metadatas", "distances"]
)
```

### Add New Record

```python
collection.add(
    ids=["CAS123456"],
    documents=["Network timeout in provisioning"],
    metadatas=[{
        "call_id": "CAS123456",
        "priority": "P2",
        "ai_generated_workaround": "1. Check connectivity..."
    }]
)
```

---

## 📦 Creation Scripts

### `vectorstore_creation/create_vectorstore.py`

Creates the vectorstore from historical Excel data.

```python
python vectorstore_creation/create_vectorstore.py

# Steps:
# 1. Load Excel files from historical data excel/
# 2. Clean and preprocess text
# 3. Generate embeddings with all-MiniLM-L6-v2
# 4. Insert into ChromaDB
```

### `historical data injector/push_historical_data.py`

Injects new historical data into existing vectorstore.

```python
python "historical data injector/push_historical_data.py"

# Incremental update - doesn't recreate entire store
```

---

## 📊 Storage Details

| Component | Size (Approx) |
|-----------|---------------|
| chroma.sqlite3 | ~500 MB |
| Collection directories | ~1.5 GB |
| Total | ~2 GB |

**Note**: Size varies with number of records and embedding dimensions (384 for all-MiniLM-L6-v2).

---

## ⚠️ Backup & Recovery

### Create Backup

```python
import shutil
shutil.copytree(
    "data/vectorstore/chromadb_store",
    "data/backup/chromadb_store_backup"
)
```

### Restore from Backup

```python
shutil.rmtree("data/vectorstore/chromadb_store")
shutil.copytree(
    "data/backup/chromadb_store_backup",
    "data/vectorstore/chromadb_store"
)
```

---

## 🔗 Related

- [Data/README.md](../README.md) - Data module overview
- [RAG/utils/README.md](../../RAG/utils/README.md) - History database manager

---

*Part of SR-Analyzer Data Module*
