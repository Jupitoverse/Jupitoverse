# 🔧 RAG Pipeline Module

> **Core 5-LLM Pipeline Implementation**

This folder contains the main RAG pipeline files - the heart of SR-Analyzer.

---

## 📁 Structure

```
pipeline/
├── README.md
├── __init__.py
├── multi_model_rag_pipeline_chatgpt.py  # Main pipeline (2681 lines)
└── activity_name_finder.py              # PostgreSQL activity lookup
```

---

## 📦 `multi_model_rag_pipeline_chatgpt.py`

### Overview

The **core file** of SR-Analyzer implementing the 5-LLM RAG pipeline.

**File Stats:**
- Lines: 2681
- Classes: 4
- LLM Prompts: 6

### Classes

| Class | Lines | Description |
|-------|-------|-------------|
| `TokenManager` | ~100 | API token rotation |
| `MultiModelLLM` | ~150 | LLM wrapper with JSON parsing |
| `VectorstoreHandler` | ~200 | ChromaDB query handler |
| `MultiModelSRPipeline` | ~2000 | Main pipeline orchestrator |

### LLM Prompts

| Prompt | Lines | Purpose |
|--------|-------|---------|
| `PROMPT_FIND_SEMANTIC_WORKAROUND` | 65 | Extract workaround from matches |
| `PROMPT_JAVA_DETECTION_VOTING` | 120 | 5-source Java detection |
| `PROMPT_EXTRACT_ACTIVITIES` | 80 | Extract activity names |
| `PROMPT_JAVA_RESOLUTION` | 100 | Java-specific resolution |
| `PROMPT_GENERAL_RESOLUTION` | 80 | General resolution |
| `PROMPT_SKILL_ASSIGNMENT` | 60 | Team assignment |

### Usage

```python
from RAG.pipeline.multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline

pipeline = MultiModelSRPipeline(tokens_file="tokens/Tokens.xlsx")

result = pipeline.analyze_single_sr({
    'SR ID': 'CAS123456',
    'Description': 'Network timeout error...',
    'Priority': 'P2'
})

print(f"Is Java: {result['Is Java Error']}")
print(f"Confidence: {result['Confidence']}")
print(f"Workaround: {result['AI Workaround']}")
print(f"Assigned: {result['Assigned To']}")
```

### Pipeline Flow

```
INPUT: SR Data
    │
    ▼
SEMANTIC SEARCH (ChromaDB)
    │ Query 1.18M+ historical SRs
    │
    ▼
LLM #1 (if similarity < 50%)
    │ Extract best workaround
    │
    ▼
LLM #2: JAVA DETECTION
    │ 5-source weighted voting
    │ Source 1: Categories (0.5x)
    │ Source 2: Semantic WA (1.5x)
    │ Source 3: AI WAs (1.0x)
    │ Source 4: User WAs (1.0x)
    │ Source 5: Current SR (2.0x)
    │
    ├── JAVA DETECTED
    │   │
    │   ▼
    │   LLM #3: ACTIVITY EXTRACTION
    │   │ Extract CamelCase names
    │   │ Validate against PostgreSQL
    │   │ Retry up to 2 times
    │   │
    │   ▼
    │   LLM #4a: JAVA RESOLUTION
    │
    └── NON-JAVA
        │
        ▼
        LLM #4b: GENERAL RESOLUTION
            │
            ▼
        LLM #5: SKILL ASSIGNMENT
            │ Check availability (skip 0%)
            │ Match skill to complexity
            │
            ▼
        OUTPUT: Result Dict
```

---

## 📦 `activity_name_finder.py`

### Class: `ActivityFinder`

Validates Java activity names against PostgreSQL database.

```python
from RAG.pipeline.activity_name_finder import ActivityFinder

finder = ActivityFinder()
result = finder.find_activity_implementation("ValidateAddress")

if result['found']:
    print(f"Class: {result['class_name']}")
    print(f"Package: {result['package']}")
```

### PostgreSQL Config

```python
DB_HOST = os.getenv('DB_HOST', 'inoscmm2181')
DB_PORT = os.getenv('DB_PORT', '30432')
DB_NAME = os.getenv('DB_NAME', 'paasdb')
DB_USER = os.getenv('DB_USER', 'ossdb01ref')
```

---

## ⚙️ API Configuration

```python
API_URL = "https://ai-framework1:8085/api/v1/call_llm"
DEFAULT_MODEL = "gpt-4.1"
```

---

## 📊 Output Fields

| Field | Type | Description |
|-------|------|-------------|
| SR ID | str | Service Request ID |
| Is Java Error | str | "Yes" / "No" |
| Confidence | str | HIGH/MEDIUM/LOW/VERY_LOW |
| Java Votes | int | Count of JAVA votes |
| Non-Java Votes | int | Count of NON_JAVA votes |
| Activity Names | str | Validated activities |
| Implementation Classes | str | Java class paths |
| AI Workaround | str | Generated resolution |
| Semantic Workaround Used | str | Source workaround |
| Assigned To | str | Team member name |

---

## 🔗 Related

- [RAG/README.md](../README.md) - RAG module overview
- [utils/README.md](../utils/README.md) - Utilities

---

*Part of SR-Analyzer RAG Module*
