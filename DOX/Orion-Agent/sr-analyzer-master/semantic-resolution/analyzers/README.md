# 🔍 Analyzers Module

> **SR Text Analysis and Preprocessing**

Core analysis engines for processing Service Requests.

---

## 📁 Structure

```
analyzers/
├── __init__.py
├── README.md
├── batch_sr_analyser.py          # AIEnhancedServiceRequestAnalyzer
├── comprehensive_sr_analyzer.py  # Wrapper for compatibility
└── sr_text_preprocessor.py       # Text cleaning
```

---

## 📦 Key Components

### `batch_sr_analyser.py`

**Class: `AIEnhancedServiceRequestAnalyzer`**

Main analysis engine with semantic search capabilities.

```python
from analyzers.batch_sr_analyser import AIEnhancedServiceRequestAnalyzer

analyzer = AIEnhancedServiceRequestAnalyzer()

result = analyzer.analyze_single_sr({
    'Call ID': 'CAS123456',
    'Description': 'Network connectivity issue...',
    'Notes': 'Customer reports failures...',
    'Priority': 'P2',
    'Application': 'SOM_MM'
})
```

**Features:**
- ChromaDB semantic search
- Java error pattern detection
- Interface detection (DCP, OMW, CAMP, etc.)
- Similarity scoring
- Team assignment

---

### `comprehensive_sr_analyzer.py`

**Class: `ComprehensiveSRAnalyzer`**

Wrapper around `AIEnhancedServiceRequestAnalyzer` for legacy compatibility.

```python
from analyzers.comprehensive_sr_analyzer import ComprehensiveSRAnalyzer

analyzer = ComprehensiveSRAnalyzer()
results = analyzer.analyze_sr_batch(sr_records)
```

---

### `sr_text_preprocessor.py`

**Class: `SRTextPreprocessor`**

Cleans SR text for better semantic search.

```python
from analyzers.sr_text_preprocessor import SRTextPreprocessor

preprocessor = SRTextPreprocessor()
clean_text = preprocessor.clean_for_semantic_search(raw_text)
```

**Removes:**
- Customer names/IDs
- Project names/IDs
- Timestamps/dates
- Email addresses
- Phone numbers
- Metadata labels

**Preserves:**
- Activity names (CW8, CWMA)
- Technical terms (CMFS, CRTE)
- Problem descriptions
- Error messages

---

## 🔍 Java Error Patterns

```python
java_error_patterns = [
    r'java\.lang\.\w*Exception',
    r'NullPointerException',
    r'SQLException',
    r'at\s+[\w\.]+\(',      # Stack trace
    r'Caused by:',
    r'spring framework',
    r'hibernate'
]
```

---

## 🖥️ Interface Detection

```python
interface_keywords = {
    'DCP': ['dcp', 'design center platform', 'quote'],
    'OMW': ['omw', 'order management', 'orchestration'],
    'CAMP': ['camp', 'customer account'],
    'OSO': ['oso', 'order submission'],
    'Billing': ['billing', 'invoice', 'rating'],
    'CRM': ['crm', 'salesforce']
}
```

---

## 📊 Output Fields

| Field | Description |
|-------|-------------|
| SR ID | Service Request ID |
| Suggested Workaround | Best match from history |
| Similar SR IDs | Matching historical SRs |
| Similarity Score | Match percentage (0-1) |
| Java Related | Boolean |
| Interface | Detected interface |
| Assigned To | Team member |

---

## 🔗 Related

- [RAG/README.md](../RAG/README.md) - Uses analyzers
- [data/README.md](../data/README.md) - ChromaDB storage

---

*Part of SR-Analyzer Analyzers Module*
