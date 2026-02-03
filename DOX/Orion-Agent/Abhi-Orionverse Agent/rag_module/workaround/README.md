# 🔧 Workaround Module

> **Workaround Extraction and Resolution Mapping Tools**

This module provides tools for extracting, analyzing, and retrieving workarounds from various sources including historical data and resolution mappings.

---

## 📁 Structure

```
workaround/
├── __init__.py
├── README.md
├── resolution_mapping_retriever.py     # ChromaDB search for resolutions
├── add_suggested_workaround_column.py  # Add workaround column to Excel
├── analyze_workaround_mapping.py       # Analyze workaround patterns
├── create_llm_workaround_mapping.py    # Create LLM-based mappings
├── extract_final_workarounds.py        # Extract final workarounds
└── extract_workarounds_by_category.py  # Category-based extraction
```

---

## 📦 Key Components

### 1. `resolution_mapping_retriever.py` - ResolutionMappingRetriever

Primary class for searching resolution mappings using ChromaDB.

```python
from workaround.resolution_mapping_retriever import ResolutionMappingRetriever

retriever = ResolutionMappingRetriever(vectorstore_dir="data/vectorstore")

# Search for similar resolutions
results = retriever.search("network connectivity issue", top_k=5)

# Get formatted context for RAG
context = retriever.search_with_context("database error", top_k=3)
```

**Key Methods:**

| Method | Description |
|--------|-------------|
| `search(query, top_k, similarity_threshold)` | Search vectorstore |
| `search_with_context(query, top_k)` | Get RAG-formatted context |
| `get_by_index(index)` | Get specific record |
| `get_all_data()` | Get entire dataset |
| `get_stats()` | Get vectorstore statistics |

**Search Result Format:**
```python
[
    {
        'index': 0,
        'similarity': 0.85,
        'data': {
            'category': 'Network',
            'resolution': 'Check connectivity...',
            'workaround': 'Restart service...'
        }
    }
]
```

**Context Format for RAG:**
```
Found 3 relevant resolution mappings:

1. (Similarity: 0.85)
   category: Network
   resolution: Check connectivity settings
   workaround: Restart the affected service

2. (Similarity: 0.72)
   ...
```

**Storage Backends:**
- **Primary**: ChromaDB (`resolution_mapping` collection)
- **Fallback**: Pickle file (`resolution_mapping.db`)

---

### 2. `add_suggested_workaround_column.py`

Adds a "Suggested Workaround" column to Excel files based on semantic search.

```python
# Usage
python add_suggested_workaround_column.py input.xlsx output.xlsx
```

**Process:**
1. Load input Excel
2. For each SR, search historical database
3. Find best matching workaround
4. Add as new column
5. Save to output file

---

### 3. `analyze_workaround_mapping.py`

Analyzes workaround patterns across the database.

```python
# Usage
python analyze_workaround_mapping.py
```

**Output:**
- Common workaround patterns
- Category distribution
- Quality metrics
- Missing workaround analysis

---

### 4. `create_llm_workaround_mapping.py`

Creates LLM-generated workaround mappings for categories without good historical data.

```python
# Usage
python create_llm_workaround_mapping.py
```

**Process:**
1. Identify categories with poor workaround coverage
2. Generate template workarounds using LLM
3. Store as resolution mappings

---

### 5. `extract_final_workarounds.py`

Extracts finalized workarounds from processed SR data.

```python
# Usage
python extract_final_workarounds.py input.xlsx
```

**Features:**
- Combines AI and user workarounds
- Applies quality filtering
- Outputs clean workaround list

---

### 6. `extract_workarounds_by_category.py`

Extracts workarounds grouped by resolution category.

```python
# Usage
python extract_workarounds_by_category.py
```

**Output Format:**
```json
{
    "Network": [
        {"sr_id": "CAS123", "workaround": "..."},
        {"sr_id": "CAS456", "workaround": "..."}
    ],
    "Application": [
        ...
    ]
}
```

---

## 🔍 ResolutionMappingRetriever Deep Dive

### Initialization
```python
def __init__(self, vectorstore_dir: str = "data/vectorstore"):
    """
    Initialize the retriever.
    
    Attempts:
    1. Load from ChromaDB (primary)
    2. Fall back to pickle file (legacy)
    
    Also loads SentenceTransformer model for queries.
    """
```

### Search Implementation
```python
def search(self, query: str, top_k: int = 5, 
           similarity_threshold: float = 0.0) -> List[Dict]:
    """
    Search the vectorstore for similar resolutions.
    
    ChromaDB mode:
    1. Encode query with SentenceTransformer
    2. Query ChromaDB with embedding
    3. Filter by similarity threshold
    4. Return formatted results
    
    Pickle fallback:
    1. Encode query
    2. Normalize embeddings
    3. Compute cosine similarities
    4. Return top-k results
    """
```

### Statistics
```python
def get_stats(self) -> Dict[str, Any]:
    """
    Get vectorstore statistics.
    
    Returns:
    {
        'num_records': 5000,
        'embedding_dimension': 384,
        'storage_format': 'ChromaDB',
        'metadata': {...}
    }
    """
```

---

## 📊 Workaround Quality Filtering

The module applies quality filters to workarounds:

**Garbage Patterns (Rejected):**
```python
garbage_patterns = [
    r'^n/?a$',              # "NA", "N/A"
    r'^none$',              # "none"
    r'^null$',              # "null"
    r'^-$',                 # "-"
    r'^not\s*available$',   # "not available"
    r'^escalated$',         # "escalated"
    r'^closed$',            # "closed"
    r'^no\s*action',        # "no action"
    r'^resolved$',          # "resolved" (too vague)
    r'^fixed$'              # "fixed" (too vague)
]
```

**Quality Criteria:**
- Minimum length: 15 characters
- Contains actionable steps
- Not just status updates
- Not customer-specific info

---

## 🔧 Usage Examples

### Basic Search
```python
from workaround.resolution_mapping_retriever import ResolutionMappingRetriever

retriever = ResolutionMappingRetriever()

# Search for resolutions
results = retriever.search(
    query="network timeout connecting to database",
    top_k=5,
    similarity_threshold=0.5
)

for r in results:
    print(f"Similarity: {r['similarity']:.2f}")
    print(f"Resolution: {r['data'].get('resolution', 'N/A')}")
    print()
```

### RAG Integration
```python
# Get context for LLM prompt
context = retriever.search_with_context(
    "Java NullPointerException in ValidateAddress",
    top_k=3
)

prompt = f"""
Based on these historical resolutions:
{context}

Provide a workaround for the current issue...
"""
```

### Statistics
```python
stats = retriever.get_stats()
print(f"Total resolutions: {stats['num_records']}")
print(f"Storage: {stats['storage_format']}")
```

---

## 🔗 Related Modules

- [RAG Pipeline](../RAG/README.md) - Uses workaround search
- [Analyzers](../analyzers/README.md) - Semantic analysis
- [Data](../data/README.md) - Vectorstore storage

---

*Part of SR-Analyzer Workaround Module*
