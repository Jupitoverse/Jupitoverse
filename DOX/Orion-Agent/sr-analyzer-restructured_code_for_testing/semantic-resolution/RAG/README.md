# 🤖 RAG Module

> **Multi-Model Retrieval-Augmented Generation Pipeline**

The heart of the SR-Analyzer system - a sophisticated 5-LLM pipeline that analyzes Service Requests using semantic search, Java detection, activity extraction, and intelligent resolution generation.

---

## 📁 Structure

```
RAG/
├── __init__.py
├── README.md
├── SR_Analysis_Flow_Diagram.png
├── extract_semantic_workarounds.py    # Extract workarounds from analysis
│
├── rag/                               # Core pipeline
│   ├── multi_model_rag_pipeline_chatgpt.py  # Main 5-LLM pipeline
│   ├── LLM_FLOW_DOCUMENTATION.md            # Detailed LLM flow docs
│   └── README.md
│
├── pipeline/                          # Pipeline utilities
│   ├── activity_name_finder.py        # PostgreSQL activity lookup
│   └── README.md
│
├── utils/                             # Utility scripts
│   ├── history_db_manager.py          # ChromaDB management
│   └── README.md
│
├── creation/                          # Vectorstore creation
│   ├── create_history_vectorstore.py  # Build ChromaDB from Excel
│   ├── create_java_mapping.py         # Parse Java source files
│   └── README.md
│
├── input/                             # Input files (temporary)
└── llm output/                        # Generated analysis results
```

---

## 🔗 5-LLM Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         MULTI-MODEL RAG PIPELINE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   INPUT: SR Data (Description, Notes, Priority)                             │
│                     │                                                        │
│                     ▼                                                        │
│   ┌─────────────────────────────────────────┐                               │
│   │         SEMANTIC SEARCH                  │                               │
│   │  Query ChromaDB for similar SRs          │                               │
│   │  Similarity threshold: 0.55              │                               │
│   └────────────────┬────────────────────────┘                               │
│                    │                                                         │
│         ┌─────────┴─────────┐                                               │
│         │  Similarity ≥ 50%? │                                               │
│         └─────────┬─────────┘                                               │
│              NO   │   YES                                                    │
│         ┌────────┴────────┐                                                 │
│         ▼                 ▼                                                 │
│   ┌──────────┐     ┌──────────────┐                                         │
│   │ LLM #1   │     │ Use Top      │                                         │
│   │ Find     │     │ Match        │                                         │
│   │Workaround│     │ Directly     │                                         │
│   └────┬─────┘     └──────┬───────┘                                         │
│        └─────────┬────────┘                                                 │
│                  ▼                                                          │
│   ┌────────────────────────────────────────┐                                │
│   │              LLM #2                     │                                │
│   │     JAVA DETECTION (5-Source Voting)    │                                │
│   │  ┌───────┐ ┌───────┐ ┌───────┐         │                                │
│   │  │Cat.   │ │Semantic│ │AI WA  │         │                                │
│   │  │ Vote  │ │ Vote   │ │ Vote  │         │                                │
│   │  └───────┘ └───────┘ └───────┘         │                                │
│   │  ┌───────┐ ┌───────┐                   │                                │
│   │  │User WA│ │Current│                   │                                │
│   │  │ Vote  │ │SR Vote│                   │                                │
│   │  └───────┘ └───────┘                   │                                │
│   └────────────────┬───────────────────────┘                                │
│                    │                                                         │
│         ┌─────────┴─────────┐                                               │
│         │   is_java_error?   │                                               │
│         └─────────┬─────────┘                                               │
│              YES  │   NO                                                     │
│         ┌────────┴────────┐                                                 │
│         ▼                 │                                                 │
│   ┌──────────┐            │                                                 │
│   │ LLM #3   │            │                                                 │
│   │ Extract  │            │                                                 │
│   │Activities│            │                                                 │
│   │+ Validate│            │                                                 │
│   │PostgreSQL│            │                                                 │
│   └────┬─────┘            │                                                 │
│        │                  │                                                 │
│        ▼                  ▼                                                 │
│   ┌──────────┐     ┌──────────┐                                             │
│   │ LLM #4a  │     │ LLM #4b  │                                             │
│   │   JAVA   │     │ GENERAL  │                                             │
│   │RESOLUTION│     │RESOLUTION│                                             │
│   └────┬─────┘     └────┬─────┘                                             │
│        └─────────┬──────┘                                                   │
│                  ▼                                                          │
│   ┌────────────────────────────────────────┐                                │
│   │              LLM #5                     │                                │
│   │     SKILL-BASED ASSIGNMENT              │                                │
│   │  • Check availability                   │                                │
│   │  • Match skill to complexity            │                                │
│   │  • Balance workload                     │                                │
│   └────────────────┬───────────────────────┘                                │
│                    ▼                                                         │
│   OUTPUT: AI Workaround + Assigned Team Member                              │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📜 LLM Prompts Overview

### LLM #1: Find Semantic Workaround
**Purpose**: Extract best workaround when semantic search similarity < 50%

```
Input:
- Current SR details
- Historical matches (even low similarity)

Output (JSON):
{
    "matched_sr_id": "CAS123456",
    "similarity_reason": "Similar network issue pattern",
    "semantic_workaround": "Check connectivity...",
    "quality_score": 0.75
}
```

### LLM #2: Java Error Detection (5-Source Voting)
**Purpose**: Determine if SR is a Java/backend error

**Vote Sources**:
1. **Category Vote**: Current SR's resolution category
2. **Semantic Vote**: Java indicators in workaround
3. **AI Workaround Vote**: Java patterns in AI suggestions
4. **User Workaround Vote**: Java patterns in user corrections
5. **Current SR Vote**: Direct analysis of description/notes

**Java Indicators**:
- Java classes: `*Service`, `*Controller`, `*Repository`
- Exceptions: `NullPointerException`, `SQLException`
- Packages: `com.amdocs.*`, `com.comcast.*`
- Stack traces: `at com.`, `at org.`

```
Output (JSON):
{
    "votes": {
        "category": "JAVA",
        "semantic": "NON_JAVA",
        "ai_workarounds": "UNKNOWN",
        "user_workarounds": "JAVA",
        "current_sr": "JAVA"
    },
    "java_votes": 3,
    "non_java_votes": 1,
    "is_java_error": true,
    "confidence": "MEDIUM"
}
```

### LLM #3: Extract Activity Names
**Purpose**: Identify Java activity names for backend issues

**Activity Patterns**:
- CamelCase with action verbs: `Validate*`, `Create*`, `Update*`
- Domain keywords: `*Address`, `*Order`, `*Customer`
- Impl suffix handling: `ValidateAddressImpl` → `ValidateAddress`

**Validation Loop**:
1. Extract activities from LLM
2. Query PostgreSQL for implementation
3. If not found, retry with alternative names (max 2 retries)

### LLM #4a: Java Resolution
**Purpose**: Generate comprehensive Java-specific workaround

**Anti-Hallucination Rules**:
- Use ONLY file paths from provided context
- Use ONLY class names from validated activities
- Mark unknown items as `[NEEDS INVESTIGATION]`
- Reference source for each step

### LLM #4b: General Resolution
**Purpose**: Generate workaround for non-Java issues

**Grounding Requirements**:
- Quote exact text from SR
- Use specific IDs/names from SR
- Adapt historical patterns to current SR

### LLM #5: Skill-Based Assignment
**Purpose**: Select optimal team member for the SR

**Assignment Rules**:
1. Skip members with 0% availability
2. Check workload capacity
3. Match skill level to SR complexity
4. P1/P2 SRs → Prefer experts (skill ≥ 4.0)
5. Low complexity → Prefer junior members (save experts)

---

## 🔧 Key Classes

### `MultiModelSRPipeline`
Main orchestrator for the 5-LLM pipeline.

```python
from RAG.rag.multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline

pipeline = MultiModelSRPipeline(
    tokens_file="tokens/Tokens.xlsx",
    model_name="gpt-4.1"
)

# Analyze single SR
result = pipeline.analyze_single_sr(sr_data)

# Process Excel file
pipeline.run()  # Reads from RAG/input, outputs to RAG/llm output
```

### `TokenManager`
Manages API tokens with automatic rotation.

```python
class TokenManager:
    def get_current_token() -> str
    def mark_exhausted() -> bool  # Rotate to next token
    def get_status() -> str       # "Tokens: 3/5 available"
```

### `MultiModelLLM`
LLM wrapper with JSON parsing and usage tracking.

```python
class MultiModelLLM:
    def call(prompt, call_name, temperature) -> str
    def parse_json_response(response) -> dict
    def get_usage_summary() -> dict
```

### `VectorstoreHandler`
Handles queries to ChromaDB collections.

```python
class VectorstoreHandler:
    def search_historical_srs(query, top_k) -> List[Dict]
    def search_java_code_semantically(query, top_k) -> List[Dict]
    def get_java_metadata_context(limit) -> str
    def search_abbreviations(query, top_k) -> str
```

---

## 📊 Output Format

Each analyzed SR produces:

| Field | Description |
|-------|-------------|
| `SR ID` | Service Request identifier |
| `Priority` | P1, P2, P3, P4 |
| `Is Java Error` | Yes/No |
| `Confidence` | HIGH/MEDIUM/LOW/VERY_LOW |
| `Issue Type` | Java/Code, Data, Configuration, etc. |
| `Java Votes` | Count of JAVA votes |
| `Non-Java Votes` | Count of NON_JAVA votes |
| `Activity Names` | Validated Java activities |
| `Implementation Classes` | Java class paths |
| `AI Workaround` | Generated resolution steps |
| `Semantic Workaround Used` | Source workaround |
| `Assigned To` | Team member name |

---

## ⚙️ Configuration

### API Endpoint
```python
API_URL = "https://ai-framework1:8085/api/v1/call_llm"
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
2. `comcast_code` (ChromaDB) - Backend code semantic search
3. `clean_history_data` (ChromaDB) - Historical SR semantic search
4. PostgreSQL - Activity implementation lookup
5. `people_skills.db` - Team skills and availability

---

## 📁 Subfolders

### `rag/`
Core pipeline implementation:
- `multi_model_rag_pipeline_chatgpt.py` - Main 5-LLM pipeline (2000+ lines)

### `pipeline/`
Pipeline utilities:
- `activity_name_finder.py` - PostgreSQL lookup for Java activities

### `utils/`
Utility scripts:
- `history_db_manager.py` - ChromaDB CRUD operations

### `creation/`
Vectorstore creation scripts:
- `create_history_vectorstore.py` - Build ChromaDB from Excel
- `create_java_mapping.py` - Parse Java source files

---

## 🚀 Usage

### Run Full Pipeline
```bash
# Place Excel in RAG/input/
cd semantic-resolution
python -c "from RAG.rag.multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline; MultiModelSRPipeline().run()"
```

### Programmatic Usage
```python
from RAG.rag.multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline

pipeline = MultiModelSRPipeline()

# Single SR analysis
sr_data = {
    'SR ID': 'CAS123456',
    'Description': 'Network timeout when calling ValidateAddress...',
    'Notes': 'NullPointerException in logs...',
    'Priority': 'P2'
}
result = pipeline.analyze_single_sr(sr_data)

print(f"Is Java: {result['Is Java Error']}")
print(f"Assigned: {result['Assigned To']}")
print(f"Workaround: {result['AI Workaround'][:200]}...")
```

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| LLM Calls per SR | 3-5 (adaptive) |
| Average Time per SR | ~15 seconds |
| Token Usage (typical) | 3000-5000 per SR |
| API Model | gpt-4.1 |

---

## 🔗 Related Modules

- [Analyzers](../analyzers/README.md) - Semantic analysis
- [Data](../data/README.md) - ChromaDB storage
- [Team](../team/README.md) - Skills database

---

*Part of SR-Analyzer RAG Module*
