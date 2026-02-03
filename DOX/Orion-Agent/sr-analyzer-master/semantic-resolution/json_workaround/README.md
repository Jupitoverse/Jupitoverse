# 📚 JSON Workaround Module

> **Known Workaround Search from JSON Data**

Loads and searches historical workaround data from JSON files.

---

## 📁 Structure

```
json_workaround/
├── __init__.py
├── README.md
├── data_handler.py          # WorkaroundDataHandler class
├── routes.py                # Flask routes
└── data/
    ├── workarounds.json     # Main workaround data
    └── sample_workarounds.json
```

---

## 📦 `data_handler.py`

### Class: `WorkaroundDataHandler`

```python
from json_workaround.data_handler import get_workaround_handler

handler = get_workaround_handler()

# Search by description
results = handler.search_by_description("network timeout", top_k=5)

# Search by RCA
results = handler.search_by_rca("connection pool", top_k=5)

# Get all data
all_workarounds = handler.get_all_data()
```

### JSON Schema

```json
[
  {
    "description": "Network timeout when connecting to database",
    "rca": "Connection pool exhausted",
    "workaround": "1. Increase pool size\n2. Restart service",
    "sr_id": "CAS123456",
    "category": "Network"
  }
]
```

---

## 🌐 Web Interface

Access at: `http://localhost:5000/workaround`

Features:
- Search by description
- Search by RCA
- View detailed workarounds
- Copy to clipboard

---

## 🔧 Adding Data

1. Edit `data/workarounds.json`
2. Follow the JSON schema
3. Reload via `/workaround/api/reload`

---

## 🔗 Related

- [templates/json_workaround/README.md](../templates/json_workaround/README.md) - HTML templates
- [app/README.md](../app/README.md) - Flask application

---

*Part of SR-Analyzer JSON Workaround Module*
