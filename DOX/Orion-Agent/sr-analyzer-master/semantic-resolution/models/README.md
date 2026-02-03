# 🧠 Models Module

> **Pre-trained ML Models**

Contains pre-downloaded machine learning models.

---

## 📁 Structure

```
models/
├── README.md
└── sentence-transformers_all-MiniLM-L6-v2/
    ├── config.json
    ├── pytorch_model.bin
    ├── tokenizer_config.json
    ├── vocab.txt
    └── ...
```

---

## 📦 all-MiniLM-L6-v2

### Specifications

| Property | Value |
|----------|-------|
| Model Name | all-MiniLM-L6-v2 |
| Embedding Dimension | 384 |
| Max Sequence Length | 256 tokens |
| Model Size | ~22MB |
| Language | English |

### Usage

```python
from sentence_transformers import SentenceTransformer

# Load local model
model = SentenceTransformer(
    'models/sentence-transformers_all-MiniLM-L6-v2'
)

# Encode text
embeddings = model.encode(["Hello world"])
print(embeddings.shape)  # (1, 384)
```

### Where Used

- **Semantic Search**: ChromaDB queries
- **HistoryDatabaseManager**: SR embeddings
- **ResolutionMappingRetriever**: Resolution search

---

## 💡 Notes

- Model downloads automatically if not present
- CPU mode used to avoid GPU issues
- Do not modify model files

---

## 🔗 Related

- [RAG/README.md](../RAG/README.md) - Uses for embeddings
- [data/README.md](../data/README.md) - ChromaDB storage

---

*Part of SR-Analyzer Models Module*
