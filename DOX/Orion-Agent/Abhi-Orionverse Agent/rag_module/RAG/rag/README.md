# 🧠 RAG/rag Module

> **Core Multi-Model RAG Pipeline Implementation**

This folder contains the main RAG pipeline that orchestrates 5 LLM calls for comprehensive SR analysis.

---

## 📁 Structure

```
rag/
├── README.md
├── multi_model_rag_pipeline_chatgpt.py    # Main pipeline (2000+ lines)
└── LLM_FLOW_DOCUMENTATION.md              # Detailed flow documentation
```

---

## 📦 Main File: `multi_model_rag_pipeline_chatgpt.py`

### Overview

A comprehensive 5-LLM pipeline for SR analysis with:
- Intelligent semantic search
- 5-source voting for Java detection
- Activity extraction with PostgreSQL validation
- Anti-hallucination prompts
- Skill-based team assignment

### Key Classes

#### `TokenManager`
Manages API tokens with automatic rotation.

```python
class TokenManager:
    def __init__(self, tokens_file: Path = None)
    def get_current_token(self) -> Optional[str]
    def get_current_email(self) -> Optional[str]
    def mark_exhausted(self) -> bool
    def get_status(self) -> str
```

#### `MultiModelLLM`
LLM wrapper for API calls with JSON parsing.

```python
class MultiModelLLM:
    def __init__(self, token_manager, model_name="gpt-4.1")
    def call(self, prompt: str, call_name: str, temperature: float) -> str
    def parse_json_response(self, response: str) -> Dict
    def get_usage_summary(self) -> Dict
```

#### `VectorstoreHandler`
Handles all vector database queries.

```python
class VectorstoreHandler:
    def __init__(self)
    def search_historical_srs(self, query: str, top_k: int) -> List[Dict]
    def search_java_code_semantically(self, query: str, top_k: int) -> List[Dict]
    def search_java_mapping_semantically(self, query: str, top_k: int) -> List[Dict]
    def get_java_metadata_context(self, limit: int) -> str
    def search_abbreviations(self, query: str, top_k: int) -> str
```

#### `MultiModelSRPipeline`
Main orchestrator for the 5-LLM pipeline.

```python
class MultiModelSRPipeline:
    def __init__(self, tokens_file=None, model_name="gpt-4.1")
    
    # LLM Call Methods
    def _llm_find_workaround(self, sr_data, historical_matches) -> str
    def _llm_detect_java_with_voting(self, sr_data, semantic_workaround, historical_matches) -> Dict
    def _llm_extract_activities(self, sr_data, semantic_workaround, historical_matches, retry_context) -> List[Dict]
    def _extract_and_validate_activities(self, sr_data, semantic_workaround, historical_matches, max_retries) -> List[Dict]
    def _llm_java_resolution(self, sr_data, java_result, validated_activities, semantic_workaround, historical_matches) -> str
    def _llm_general_resolution(self, sr_data, java_result, semantic_workaround, historical_matches) -> str
    def _llm_skill_assignment(self, sr_data, is_java_error, issue_type) -> str
    
    # Orchestration
    def analyze_single_sr(self, sr_data: Dict) -> Dict
    def process_all_srs(self, df: pd.DataFrame)
    def run(self)
```

---

## 🔄 Pipeline Flow

```
┌────────────────────────────────────────────────────────────┐
│                    analyze_single_sr()                      │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  1. Semantic Search                                         │
│     └── search_historical_srs(query, top_k=10)             │
│                                                             │
│  2. Filter Garbage Workarounds                              │
│     └── _filter_workarounds(historical_matches)            │
│                                                             │
│  3. Get Semantic Workaround                                 │
│     ├── If similarity ≥ 50%: Use top match                 │
│     └── Else: LLM #1 - _llm_find_workaround()              │
│                                                             │
│  4. Java Detection                                          │
│     └── LLM #2 - _llm_detect_java_with_voting()            │
│                                                             │
│  5. Activity Extraction (if Java)                           │
│     └── LLM #3 - _extract_and_validate_activities()        │
│         └── Retry loop with PostgreSQL validation           │
│                                                             │
│  6. Generate Resolution                                     │
│     ├── If Java: LLM #4a - _llm_java_resolution()          │
│     └── Else:    LLM #4b - _llm_general_resolution()       │
│                                                             │
│  7. Skill-Based Assignment                                  │
│     └── LLM #5 - _llm_skill_assignment()                   │
│                                                             │
│  8. Return Result Dictionary                                │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

## 📜 LLM Prompts

### PROMPT_FIND_SEMANTIC_WORKAROUND (LLM #1)
- **Purpose**: Find best workaround from historical matches
- **Input**: Current SR + historical matches
- **Output**: JSON with matched_sr_id, semantic_workaround, quality_score

### PROMPT_JAVA_DETECTION_VOTING (LLM #2)
- **Purpose**: Determine if Java error using 5-source voting
- **Input**: 5 context sources
- **Output**: JSON with votes, is_java_error, confidence

### PROMPT_EXTRACT_ACTIVITIES (LLM #3)
- **Purpose**: Extract Java activity names
- **Input**: SR data + Java code context
- **Output**: JSON with activity_names array

### PROMPT_JAVA_RESOLUTION (LLM #4a)
- **Purpose**: Generate Java-specific resolution
- **Input**: Validated activities + code snippets
- **Output**: Structured AI WORKAROUND text

### PROMPT_GENERAL_RESOLUTION (LLM #4b)
- **Purpose**: Generate non-Java resolution
- **Input**: Historical patterns + SR data
- **Output**: Structured AI WORKAROUND text

### PROMPT_SKILL_BASED_ASSIGNMENT (LLM #5)
- **Purpose**: Select team member for SR
- **Input**: SR details + team context + workload
- **Output**: Single team member name

---

## 🔧 Configuration

### API Settings
```python
API_URL = "https://ai-framework1:8085/api/v1/call_llm"
MODEL_NAME = "gpt-4.1"
TEMPERATURE = 0.2  # Low for deterministic outputs
```

### Directories
```python
self.input_dir = self.base_dir / "input"
self.output_dir = self.base_dir / "llm output"
```

### Garbage Patterns
```python
self.garbage_patterns = [
    r'^n/?a$', r'^na$', r'^none$', r'^null$',
    r'^not\s*(available|applicable)$',
    r'^escalated$', r'^closed$',
    r'^no\s*action', r'^resolved$', r'^fixed$'
]
```

---

## 📊 Output Fields

| Field | Type | Description |
|-------|------|-------------|
| SR ID | str | Service Request ID |
| Priority | str | P1-P4 |
| Is Java Error | str | "Yes" or "No" |
| Confidence | str | HIGH/MEDIUM/LOW/VERY_LOW |
| Issue Type | str | Java/Code, Data, Config, etc. |
| Java Votes | int | Count of JAVA votes |
| Non-Java Votes | int | Count of NON_JAVA votes |
| Activity Names | str | Comma-separated activities |
| Implementation Classes | str | Java class paths |
| AI Workaround | str | Generated resolution |
| Full Response | str | Complete LLM response |
| Semantic Workaround Used | str | Source workaround |
| Assigned To | str | Team member name |

---

## 📈 Usage Statistics

The pipeline tracks:
- Total LLM calls
- Input/output tokens
- Cost
- Call breakdown by type

```python
usage = pipeline.llm.get_usage_summary()
print(f"Total calls: {usage['total_calls']}")
print(f"Total cost: ${usage['total_cost']:.4f}")
```

---

## 🚀 Usage

### Batch Processing
```python
from RAG.rag.multi_model_rag_pipeline_chatgpt import MultiModelSRPipeline

pipeline = MultiModelSRPipeline()
pipeline.run()  # Processes Excel in RAG/input
```

### Single SR Analysis
```python
pipeline = MultiModelSRPipeline()
result = pipeline.analyze_single_sr({
    'SR ID': 'CAS123456',
    'Description': 'Network timeout...',
    'Notes': 'Error in logs...',
    'Priority': 'P2'
})
```

---

## 🔗 Related

- [LLM_FLOW_DOCUMENTATION.md](LLM_FLOW_DOCUMENTATION.md) - Detailed flow docs
- [RAG/README.md](../README.md) - Module overview

---

*Part of SR-Analyzer RAG Module*
