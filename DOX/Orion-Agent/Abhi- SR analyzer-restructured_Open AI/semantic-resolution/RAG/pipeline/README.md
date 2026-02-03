# 🔧 RAG/pipeline Module

> **Pipeline Utilities and Activity Finder**

This folder contains utility classes for the RAG pipeline, including the PostgreSQL activity finder.

---

## 📁 Structure

```
pipeline/
├── README.md
├── __init__.py
├── activity_name_finder.py              # PostgreSQL activity lookup
└── multi_model_rag_pipeline_chatgpt.py  # (duplicate, main is in rag/)
```

---

## 📦 Main File: `activity_name_finder.py`

### Class: `ActivityFinder`

Looks up Java activity implementations in PostgreSQL database to validate extracted activity names.

```python
from RAG.pipeline.activity_name_finder import ActivityFinder

finder = ActivityFinder()

# Find activity implementation
result = finder.find_activity_implementation("ValidateAddress")

if result['found']:
    print(f"Package: {result['package']}")
    print(f"Class: {result['class_name']}")
    print(f"File Path: {result['file_path']}")
else:
    print("Activity not found")
```

---

## 🔧 Key Methods

### `find_activity_implementation(activity_name: str) -> Dict`

Finds the Java implementation of a given activity name.

```python
def find_activity_implementation(self, activity_name: str) -> Dict:
    """
    Look up activity in PostgreSQL database.
    
    Args:
        activity_name: CamelCase activity name (e.g., "ValidateAddress")
        
    Returns:
        {
            'found': True/False,
            'activity_name': 'ValidateAddress',
            'package': 'com.comcast.som.activity',
            'class_name': 'ValidateAddressActivity',
            'file_path': '/path/to/source.java',
            'alternatives': []  # Suggested alternatives if not found
        }
    """
```

### `find_multiple_activities(activity_names: List[str]) -> List[Dict]`

Batch lookup for multiple activities.

```python
def find_multiple_activities(self, activity_names: List[str]) -> List[Dict]:
    """
    Look up multiple activities efficiently.
    Uses single database connection for all lookups.
    """
```

### `get_alternative_suggestions(activity_name: str) -> List[str]`

Get similar activity names when exact match fails.

```python
def get_alternative_suggestions(self, activity_name: str) -> List[str]:
    """
    Get similar activity names using fuzzy matching.
    
    Args:
        activity_name: Activity name that wasn't found
        
    Returns:
        List of up to 5 similar activity names
    """
```

---

## 🔄 Integration with RAG Pipeline

The ActivityFinder is used in LLM Call 3 (Activity Extraction):

```python
# In multi_model_rag_pipeline_chatgpt.py
def _extract_and_validate_activities(self, sr_data, ...):
    activities = self._llm_extract_activities(...)
    
    validated = []
    for activity in activities:
        result = self.activity_finder.find_activity_implementation(activity)
        if result['found']:
            validated.append({
                'name': activity,
                'package': result['package'],
                'class_name': result['class_name']
            })
        else:
            # Retry with alternatives
            alternatives = result['alternatives']
            if alternatives:
                retry_context = f"Try these instead: {alternatives}"
                # LLM retry call...
    
    return validated
```

---

## 🗄️ PostgreSQL Schema

The activity finder queries the following table:

```sql
CREATE TABLE java_activities (
    id SERIAL PRIMARY KEY,
    activity_name VARCHAR(255) NOT NULL,
    package_name VARCHAR(500),
    class_name VARCHAR(255),
    file_path VARCHAR(1000),
    source_code TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_activity_name ON java_activities(activity_name);
```

---

## ⚠️ Configuration

PostgreSQL connection is configured in the class:

```python
class ActivityFinder:
    def __init__(self):
        self.db_config = {
            'host': 'postgresql-server',
            'port': 5432,
            'database': 'sr_analyzer',
            'user': 'app_user',
            'password': '***'
        }
```

---

## 🔗 Related

- [RAG/rag/README.md](../rag/README.md) - Main RAG pipeline
- [RAG/README.md](../README.md) - RAG module overview

---

*Part of SR-Analyzer RAG Module*
