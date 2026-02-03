# 💾 Data Module

> **Data Storage: Databases, Vector Stores, and Backups**

This module contains all persistent data storage for the SR-Analyzer system, including SQLite databases, ChromaDB vector stores, and backup files.

---

## 📁 Structure

```
data/
├── __init__.py
├── README.md
│
├── database/                      # SQLite databases
│   ├── README.md
│   ├── people_skills.db           # Team skills & availability
│   ├── sr_tracking.db             # SR tracking data
│   ├── abbreviation.db            # Abbreviation mappings
│   ├── workaround_feedback.db     # User feedback storage
│   ├── llm_usage_stats.json       # LLM API usage tracking
│   └── database_creation/         # DB creation scripts
│       └── create_abbreviation_db.py
│
├── vectorstore/                   # Vector embeddings
│   ├── README.md
│   ├── chromadb_store/            # ChromaDB persistent storage
│   │   ├── clean_history_data/    # Historical SR embeddings
│   │   ├── java_mapping/          # Java class metadata
│   │   └── comcast_code/          # Backend code embeddings
│   └── *.py                       # Vectorstore utilities
│
└── backup/                        # Backup files
    ├── chromadb_store/            # ChromaDB backups
    ├── clean_history_data.db      # Pickle backup
    ├── javaMapping.db             # Pickle backup
    ├── comcast_code.db/           # FAISS backup
    └── *.backup_*                 # Timestamped backups
```

---

## 🗄️ Database Files

### `people_skills.db`
**Purpose**: Team member skills, availability, and assignment tracking

| Table | Description |
|-------|-------------|
| `team_members` | Member names, status, IDs |
| `skills` | Application skills, levels, max load |
| `assignment_history` | Past assignments for ML learning |
| `skill_evolution` | Skill level changes over time |
| `availability_history` | Availability tracking |
| `config_changes` | Configuration change log |

### `sr_tracking.db`
**Purpose**: Service Request tracking and status

| Table | Description |
|-------|-------------|
| `srs` | SR records with status |
| `sr_history` | Status change history |
| `assignments` | Current assignments |

### `abbreviation.db`
**Purpose**: Technical abbreviation mappings for context

| Column | Description |
|--------|-------------|
| `short_form` | Abbreviation (e.g., "CMFS") |
| `full_form` | Full text (e.g., "Customer Management Fulfillment System") |
| `context` | Usage context description |

### `workaround_feedback.db`
**Purpose**: User feedback on workarounds

| Table | Description |
|-------|-------------|
| `feedback` | User corrections and ratings |
| `votes` | Thumbs up/down on workarounds |

### `llm_usage_stats.json`
**Purpose**: Track LLM API usage and costs

```json
{
    "last_updated": "2026-01-07T10:30:00",
    "last_run": {
        "total_calls": 25,
        "input_tokens": 50000,
        "output_tokens": 15000,
        "cost": 0.1234,
        "srs_processed": 5
    },
    "cumulative": {
        "total_cost": 12.34,
        "total_tokens": 500000,
        "total_calls": 250
    }
}
```

---

## 🔍 ChromaDB Vector Store

### Location
```
data/vectorstore/chromadb_store/
```

### Collections

#### `clean_history_data`
**Purpose**: Historical SR embeddings for semantic search
**Records**: 1,180,000+

| Metadata Field | Description |
|----------------|-------------|
| `call_id` | SR ID (uppercase) |
| `description` | SR description |
| `wl_summary` | Notes/summary |
| `workaround` | Original workaround |
| `ai_generated_workaround` | RAG-generated workaround |
| `user_corrected_workaround` | JSON array of user corrections |
| `resolution_categorization` | Category |
| `application` | Application area |
| `assigned_to` | Assigned team member |
| `priority` | P1-P4 |
| `status` | Current status |
| `source` | 'admin_upload' or 'user_feedback' |

#### `java_mapping`
**Purpose**: Java class metadata for code reference
**Records**: ~5,000

| Metadata Field | Description |
|----------------|-------------|
| `class_name` | Java class name |
| `package` | Package path |
| `file_path` | Source file location |
| `class_type` | Service, Controller, Repository, etc. |
| `full_qualified_name` | Complete FQN |
| `annotations` | Class annotations |

#### `comcast_code`
**Purpose**: Backend code chunks for semantic search
**Records**: ~20,000

| Metadata Field | Description |
|----------------|-------------|
| `file_path` | Source file path |
| `chunk_type` | Method, class, comment |
| `language` | Programming language |
| `project` | Project name |

---

## 🔧 Embedding Model

All vector stores use:
- **Model**: `all-MiniLM-L6-v2` (Sentence Transformers)
- **Dimensions**: 384
- **Distance**: Cosine similarity

---

## 📊 Querying ChromaDB

```python
import chromadb

# Connect
client = chromadb.PersistentClient(path="data/vectorstore/chromadb_store")

# Get collection
collection = client.get_collection("clean_history_data")

# Count records
count = collection.count()
print(f"Total records: {count}")

# Semantic search
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

query = "network connectivity timeout"
embedding = model.encode([query])[0].tolist()

results = collection.query(
    query_embeddings=[embedding],
    n_results=5,
    include=["documents", "metadatas", "distances"]
)

for i, id_ in enumerate(results['ids'][0]):
    print(f"{id_}: {results['metadatas'][0][i]['call_id']}")
```

---

## 💾 Backup Strategy

### Automatic Backups
- Created before major updates
- Format: `{filename}.backup_{YYYYMMDD_HHMMSS}`

### Manual Backup
```python
import shutil
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copytree(
    "data/vectorstore/chromadb_store",
    f"data/backup/chromadb_store_{timestamp}"
)
```

### Restore from Backup
```python
import shutil

shutil.rmtree("data/vectorstore/chromadb_store")
shutil.copytree(
    "data/backup/chromadb_store_20260107_103000",
    "data/vectorstore/chromadb_store"
)
```

---

## 📁 Subdirectories

### `database/`
Contains SQLite databases and creation scripts:
- `database_creation/` - Scripts to initialize databases

### `vectorstore/`
Contains ChromaDB and related utilities:
- `chromadb_store/` - Persistent ChromaDB data
- Creation and management scripts

### `backup/`
Contains backup files:
- Legacy pickle files
- ChromaDB backups
- Timestamped backups

---

## ⚠️ Important Notes

1. **ChromaDB Path**: Always use `PersistentClient(path=...)` with consistent path
2. **No Settings Mixing**: Avoid changing ChromaDB settings after creation
3. **Backup Before Updates**: Always backup before major vectorstore updates
4. **Disk Space**: ChromaDB can grow large; monitor disk usage
5. **Read-Only Sharing**: ChromaDB files can be copied but not shared while in use

---

## 🔗 Related Modules

- [RAG Utils](../RAG/utils/README.md) - HistoryDatabaseManager
- [Team](../team/README.md) - Uses people_skills.db
- [Analyzers](../analyzers/README.md) - Uses ChromaDB for search

---

*Part of SR-Analyzer Data Module*
