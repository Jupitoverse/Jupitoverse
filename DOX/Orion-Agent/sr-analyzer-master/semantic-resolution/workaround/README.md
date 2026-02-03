# 🔧 Workaround Module

> **Workaround Extraction and Resolution Mapping**

Tools for extracting and retrieving workarounds.

---

## 📁 Structure

```
workaround/
├── __init__.py
├── README.md
├── resolution_mapping_retriever.py     # ChromaDB search
├── add_suggested_workaround_column.py  # Add column to Excel
├── analyze_workaround_mapping.py       # Analyze patterns
├── create_llm_workaround_mapping.py    # Create LLM mappings
├── extract_final_workarounds.py        # Extract final WAs
└── extract_workarounds_by_category.py  # Category extraction
```

---

## 📦 `resolution_mapping_retriever.py`

### Class: `ResolutionMappingRetriever`

Searches resolution mappings using ChromaDB.

```python
from workaround.resolution_mapping_retriever import ResolutionMappingRetriever

retriever = ResolutionMappingRetriever()

# Search
results = retriever.search("network timeout", top_k=5, similarity_threshold=0.5)

# RAG context
context = retriever.search_with_context("database error", top_k=3)
```

### Search Result Format

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

---

## 📊 Workaround Quality Filtering

Garbage patterns rejected:

```python
garbage_patterns = [
    r'^n/?a$',              # "NA", "N/A"
    r'^none$',              # "none"
    r'^escalated$',         # "escalated"
    r'^closed$',            # "closed"
    r'^resolved$',          # too vague
    r'^fixed$'              # too vague
]
```

Quality criteria:
- Minimum length: 15 characters
- Contains actionable steps
- Not just status updates

---

## 🔧 Utility Scripts

| Script | Description |
|--------|-------------|
| `add_suggested_workaround_column.py` | Add WA column to Excel |
| `analyze_workaround_mapping.py` | Analyze WA patterns |
| `create_llm_workaround_mapping.py` | Create LLM mappings |
| `extract_final_workarounds.py` | Extract finalized WAs |
| `extract_workarounds_by_category.py` | Category-based extraction |

---

## 🔗 Related

- [RAG/README.md](../RAG/README.md) - Uses workaround search
- [analyzers/README.md](../analyzers/README.md) - Semantic analysis

---

*Part of SR-Analyzer Workaround Module*
