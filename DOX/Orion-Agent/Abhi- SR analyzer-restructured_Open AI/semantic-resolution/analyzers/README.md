# 🔍 Analyzers Module

> **SR Text Analysis and Preprocessing Components**

This module contains the core analysis engines for processing Service Requests, including semantic search, text preprocessing, and comprehensive SR analysis.

---

## 📁 Structure

```
analyzers/
├── __init__.py
├── README.md
├── batch_sr_analyser.py          # Main: AIEnhancedServiceRequestAnalyzer
├── comprehensive_sr_analyzer.py  # Wrapper for legacy compatibility
└── sr_text_preprocessor.py       # Text cleaning for semantic search
```

---

## 📦 Key Components

### 1. `batch_sr_analyser.py` - AIEnhancedServiceRequestAnalyzer

The main analysis engine that provides comprehensive SR analysis using:
- Java backend mapping (javaMapping.db)
- Historical case intelligence (1.18M+ records)
- Team skills and intelligent assignment
- AI-powered semantic search

**Key Class: `AIEnhancedServiceRequestAnalyzer`**

```python
from analyzers.batch_sr_analyser import AIEnhancedServiceRequestAnalyzer

analyzer = AIEnhancedServiceRequestAnalyzer()

# Analyze single SR
sr_data = {
    'Call ID': 'CAS123456',
    'Description': 'Network connectivity issue...',
    'Notes': 'Customer reports intermittent failures...',
    'Priority': 'P2',
    'Application': 'SOM_MM'
}
result = analyzer.analyze_single_sr(sr_data)
```

**Key Methods:**

| Method | Description |
|--------|-------------|
| `__init__()` | Initializes ChromaDB, models, and databases |
| `analyze_single_sr(sr_data)` | Analyze one SR and return comprehensive results |
| `analyze_sr_batch(sr_list)` | Batch process multiple SRs |
| `calculate_sr_age(submit_date)` | Calculate business day age |
| `connect_database(db_path)` | Connect to SQLite database |

**Initialization Process:**
```
1. Load ChromaDB collections (clean_history_data, java_mapping)
2. Load SentenceTransformer model (all-MiniLM-L6-v2)
3. Initialize text preprocessor
4. Initialize user feedback manager
5. Initialize age calculator
6. Set up Java error patterns and interface keywords
```

**Java Error Patterns:**
```python
java_error_patterns = [
    r'java\.lang\.\w*Exception',
    r'NullPointerException',
    r'SQLException',
    r'ConnectionException',
    r'TimeoutException',
    r'at\s+[\w\.]+\(',      # Stack trace pattern
    r'Caused by:',
    r'Exception in thread',
    r'spring framework',
    r'hibernate'
]
```

**Interface Detection Keywords:**
```python
interface_keywords = {
    'DCP': ['dcp', 'design center platform', 'quote', 'pricing'],
    'OMW': ['omw', 'order management', 'orchestration', 'workflow'],
    'CAMP': ['camp', 'customer account', 'account management'],
    'OSO': ['oso', 'order submission', 'order entry'],
    'Broadsoft': ['broadsoft', 'voice', 'sip', 'telephony'],
    'Billing': ['billing interface', 'invoice system', 'rating'],
    'CRM': ['crm', 'customer relationship', 'salesforce'],
    'Inventory': ['inventory', 'resource management']
}
```

---

### 2. `comprehensive_sr_analyzer.py` - ComprehensiveSRAnalyzer

A thin wrapper around `AIEnhancedServiceRequestAnalyzer` that preserves the historic API expected by legacy tooling.

**Usage:**
```python
from analyzers.comprehensive_sr_analyzer import ComprehensiveSRAnalyzer

analyzer = ComprehensiveSRAnalyzer(vector_store_path="data/database")
results = analyzer.analyze_sr_batch(sr_records)
```

**Key Method: `analyze_sr_batch(sr_records)`**
```python
def analyze_sr_batch(self, sr_records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Analyze a collection of SR dictionaries and return structured results.
    
    Args:
        sr_records: Iterable of SR dictionaries
        
    Returns:
        List of analysis result dictionaries
    """
```

**Path Configuration:**
The wrapper automatically configures paths to databases:
- `data/database/javaMapping.db`
- `data/database/sr_tracking.db`
- `data/database/people_skills.db`
- `data/database/historical_sr_index.pkl` (legacy)

---

### 3. `sr_text_preprocessor.py` - SRTextPreprocessor

Cleans unstructured SR text for optimal semantic search by removing noise while preserving technical content.

**Key Class: `SRTextPreprocessor`**

```python
from analyzers.sr_text_preprocessor import SRTextPreprocessor

preprocessor = SRTextPreprocessor()
clean_text = preprocessor.clean_for_semantic_search(raw_text)
```

**Main Method: `clean_for_semantic_search(text)`**

Applies 16 steps of text cleaning:

| Step | Description |
|------|-------------|
| 1 | Extract and preserve activity name |
| 2 | Remove customer information |
| 3 | Remove project information |
| 4 | Remove plan information |
| 5 | Remove site information |
| 6 | Remove various IDs (keep short codes like CW8) |
| 7 | Remove timestamps and dates |
| 8 | Remove email addresses |
| 9 | Remove phone numbers |
| 10 | Clean metadata field labels |
| 11 | Keep Activity label with value |
| 12 | Normalize whitespace |
| 13 | Clean punctuation |
| 14 | Remove empty brackets |
| 15 | Final cleanup |
| 16 | Quality check (prevent over-aggressive cleaning) |

**Example:**
```python
# Before:
"Customer: ABC Corp - Project: XYZ - Activity: CW8 - CW8 Object completed but the CWM Show is at 0 Obj"

# After:
"Activity CW8 CW8 Object completed but the CWM Show is at 0 Obj"
```

**What Gets Removed:**
- Customer names/IDs
- Project names/IDs
- Plan names/IDs
- Activity IDs (but keeps activity names!)
- Site information
- Timestamps/dates
- Proposal IDs
- Email addresses
- Phone numbers
- Metadata labels (Summary:, Description:, etc.)

**What Gets Preserved:**
- Activity names (CW8, CWMA, CWMB, etc.)
- Technical terms (CMFS, CRTE, CWM, UTI, etc.)
- Problem descriptions
- Error messages
- Status information

**Batch Processing:**
```python
texts = ["text1", "text2", "text3"]
clean_texts = SRTextPreprocessor.preprocess_batch(texts)
```

---

## 📊 Output Format

The analyzer returns a dictionary with these fields:

| Field | Description |
|-------|-------------|
| `SR ID` | Service Request identifier |
| `Original Description` | Raw description text |
| `Original Notes/Summary` | Raw notes text |
| `Priority` | SR priority level |
| `Application` | Application area (SOM_MM, etc.) |
| `Interface` | Detected interface (DCP, OMW, etc.) |
| `Suggested Workaround` | Best matching workaround from history |
| `Similar SR IDs` | List of similar historical SRs |
| `Similarity Score` | Semantic similarity (0-1) |
| `Java Related` | Boolean - is this a Java error? |
| `Assigned To` | Team member assignment |
| `SR Age` | Business days since creation |

---

## 🔧 Configuration

### ChromaDB Path
```python
self.chromadb_path = Path("data/vectorstore/chromadb_store")
```

### Sentence Transformer Model
```python
self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
```

### Similarity Thresholds
- Semantic search minimum: 0.30
- High confidence match: 0.55+

---

## 📈 Statistics Tracking

The analyzer tracks various statistics:

```python
stats = {
    'total_srs': 0,
    'total_processed': 0,
    'java_failures_detected': 0,
    'java_files_identified': 0,
    'historical_matches_found': 0,
    'ai_semantic_searches': 0,
    'workarounds_extracted': 0,
    'interface_detections': 0,
    'skills_based_assignments': 0,
    'high_confidence_analyses': 0,
    'processing_errors': 0
}
```

---

## 🔗 Dependencies

- `sentence-transformers` - Semantic embeddings
- `chromadb` - Vector database
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `sklearn` - Cosine similarity

---

## 🔗 Related Modules

- [RAG Pipeline](../RAG/README.md) - LLM-based analysis
- [Data](../data/README.md) - Database storage
- [Team](../team/README.md) - Skills assignment

---

*Part of SR-Analyzer Analyzers Module*
