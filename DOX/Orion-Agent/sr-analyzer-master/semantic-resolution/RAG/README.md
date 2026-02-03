# 🤖 RAG Module

> **Multi-Model Retrieval-Augmented Generation Pipeline**

The core AI engine of SR-Analyzer - a 5-LLM pipeline for analyzing Service Requests.

---

## 🚀 Quick Start

> **See [USER_ADMIN_GUIDE.md](../USER_ADMIN_GUIDE.md) for usage instructions**

```python
from RAG.pipeline.multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline

pipeline = MultiModelSRPipeline(tokens_file="tokens/Tokens.xlsx")

result = pipeline.analyze_single_sr({
    'SR ID': 'CAS123456',
    'Description': 'Network timeout error...',
    'Notes': 'Customer reports failures...',
    'Priority': 'P2'
})

print(f"Is Java: {result['Is Java Error']}")
print(f"Workaround: {result['AI Workaround']}")
print(f"Assigned: {result['Assigned To']}")
```

---

## 📁 Structure

```
RAG/
├── __init__.py
├── README.md
├── pipeline/                          # Core pipeline
│   ├── multi_model_rag_pipeline_chatgpt.py  # 5-LLM pipeline
│   ├── activity_name_finder.py        # PostgreSQL lookup
│   └── README.md
├── utils/                             # Utilities
│   ├── history_db_manager.py          # ChromaDB management
│   ├── chromadb_manager.py            # ChromaDB utilities
│   └── README.md
├── creation/                          # Vectorstore creation
│   ├── create_history_vectorstore.py
│   ├── create_clean_history_vectorstore.py
│   └── README.md
├── input/                             # Input staging
└── llm output/                        # Generated results
```

---

## 🔗 5-LLM Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      5-LLM RAG PIPELINE                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   INPUT: SR Data (Description, Notes, Priority)                     │
│                     │                                                │
│                     ▼                                                │
│   ┌─────────────────────────────────────────┐                       │
│   │         SEMANTIC SEARCH                  │                       │
│   │  Query ChromaDB (1.18M+ records)         │                       │
│   │  Similarity threshold: 0.55              │                       │
│   └────────────────┬────────────────────────┘                       │
│                    │                                                 │
│         ┌─────────┴─────────┐                                       │
│         │  Similarity < 50%? │                                       │
│         └─────────┬─────────┘                                       │
│              YES  │                                                  │
│         ┌────────┴────────┐                                         │
│         ▼                                                            │
│   ┌──────────┐                                                      │
│   │ LLM #1   │ ← Find best workaround from matches                  │
│   │Workaround│                                                      │
│   └────┬─────┘                                                      │
│        │                                                             │
│        ▼                                                             │
│   ┌────────────────────────────────────────┐                        │
│   │              LLM #2                     │                        │
│   │     JAVA DETECTION (5-Source Voting)    │                        │
│   │                                         │                        │
│   │  Source 1: Resolution Categories (0.5x) │                        │
│   │  Source 2: Semantic Workaround (1.5x)   │                        │
│   │  Source 3: AI Workarounds (1.0x)        │                        │
│   │  Source 4: User Workarounds (1.0x)      │                        │
│   │  Source 5: Current SR Content (2.0x) ← │                        │
│   └────────────────┬───────────────────────┘                        │
│                    │                                                 │
│         ┌─────────┴─────────┐                                       │
│         │   is_java_error?   │                                       │
│         └─────────┬─────────┘                                       │
│              YES  │   NO                                             │
│         ┌────────┴────────┐                                         │
│         ▼                 │                                         │
│   ┌──────────┐            │                                         │
│   │ LLM #3   │            │ ← Extract activity names                │
│   │Activities│            │   Validate against PostgreSQL           │
│   │+ Validate│            │   Retry up to 2 times                   │
│   └────┬─────┘            │                                         │
│        │                  │                                         │
│        ▼                  ▼                                         │
│   ┌──────────┐     ┌──────────┐                                     │
│   │ LLM #4a  │     │ LLM #4b  │                                     │
│   │   JAVA   │     │ GENERAL  │ ← Generate resolution               │
│   │RESOLUTION│     │RESOLUTION│   Anti-hallucination rules          │
│   └────┬─────┘     └────┬─────┘                                     │
│        └─────────┬──────┘                                           │
│                  ▼                                                   │
│   ┌────────────────────────────────────────┐                        │
│   │              LLM #5                     │                        │
│   │     SKILL-BASED ASSIGNMENT              │ ← Assign to team      │
│   │  • Check availability (skip 0%)         │   member based on     │
│   │  • Match skill to complexity            │   skills              │
│   │  • Balance workload                     │                        │
│   └────────────────┬───────────────────────┘                        │
│                    ▼                                                 │
│   OUTPUT: AI Workaround + Assigned Team Member                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Key Classes

### `MultiModelSRPipeline`

Main orchestrator for the 5-LLM pipeline.

```python
class MultiModelSRPipeline:
    def analyze_single_sr(sr_data: dict) -> dict
    def run() -> None  # Process Excel from input folder
    def get_usage_summary() -> dict
```

### `TokenManager`

Manages API tokens with automatic rotation.

```python
class TokenManager:
    def get_current_token() -> str
    def mark_exhausted() -> bool  # Rotate to next
    def get_status() -> str       # "Tokens: 3/5 available"
```

### `VectorstoreHandler`

Handles ChromaDB queries.

```python
class VectorstoreHandler:
    def search_historical_srs(query, top_k=10) -> List[Dict]
    def search_java_code_semantically(query, top_k=5) -> List[Dict]
```

---

## 📊 Output Fields

| Field | Description |
|-------|-------------|
| SR ID | Service Request identifier |
| Is Java Error | Yes/No |
| Confidence | HIGH/MEDIUM/LOW/VERY_LOW |
| Java Votes | Count of JAVA votes |
| Activity Names | Validated Java activities |
| AI Workaround | Generated resolution steps |
| Assigned To | Team member name |

---

## ⚙️ Configuration

### API Settings

```python
API_URL = "https://ai-framework1:8085/api/v1/call_llm"
DEFAULT_MODEL = "gpt-4.1"
```

### Token File

```
tokens/Tokens.xlsx
| Email           | Token     |
|-----------------|-----------|
| user@amdocs.com | api-token |
```

### Context Sources

1. `javaMapping.db` - Java class metadata
2. `comcast_code` (ChromaDB) - Backend code search
3. `clean_history_data` (ChromaDB) - Historical SRs
4. PostgreSQL - Activity implementation lookup
5. `people_skills.db` - Team skills

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| LLM Calls per SR | 3-5 (adaptive) |
| Average Time | ~15-30 seconds/SR |
| Token Usage | 3000-5000 per SR |

---

## 🔗 Related

- [pipeline/README.md](pipeline/README.md) - Core pipeline
- [utils/README.md](utils/README.md) - Utilities
- [creation/README.md](creation/README.md) - Vectorstore creation

---

*Part of SR-Analyzer RAG Module*
