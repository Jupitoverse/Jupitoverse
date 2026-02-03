# 🧠 Models Module

> **Machine Learning Models for Semantic Search**

This folder contains pre-downloaded ML models used for semantic similarity calculations.

---

## 📁 Structure

```
models/
├── README.md
└── sentence-transformers_all-MiniLM-L6-v2/
    ├── config.json
    ├── modules.json
    ├── tokenizer_config.json
    ├── vocab.txt
    ├── special_tokens_map.json
    ├── tokenizer.json
    ├── sentence_bert_config.json
    ├── pytorch_model.bin          # Model weights (22MB)
    └── config_sentence_transformers.json
```

---

## 🔧 Model: all-MiniLM-L6-v2

### Specifications

| Property | Value |
|----------|-------|
| Model Type | Sentence Transformer |
| Embedding Dimension | 384 |
| Max Sequence Length | 256 tokens |
| Model Size | ~22MB |
| Language | English |
| Use Case | Semantic similarity, clustering |

### Performance

| Metric | Value |
|--------|-------|
| Speed | ~14,000 sentences/sec (GPU) |
| Memory | ~90MB loaded |
| Accuracy | Good for general text |

---

## 📋 Usage

### Auto-Download (Default)
```python
from sentence_transformers import SentenceTransformer

# Downloads automatically if not present
model = SentenceTransformer('all-MiniLM-L6-v2')
```

### Use Local Model
```python
from sentence_transformers import SentenceTransformer

# Use pre-downloaded model
model = SentenceTransformer('models/sentence-transformers_all-MiniLM-L6-v2')
```

### Encoding Text
```python
sentences = [
    "Network connectivity issue with database",
    "Java NullPointerException in service"
]

# Generate embeddings (384-dimensional vectors)
embeddings = model.encode(sentences)
print(embeddings.shape)  # (2, 384)
```

### Computing Similarity
```python
from sklearn.metrics.pairwise import cosine_similarity

query = model.encode(["network timeout"])
docs = model.encode(["network connectivity issue", "java exception"])

similarities = cosine_similarity(query, docs)
print(similarities)  # [[0.85, 0.32]]
```

---

## 🔄 Model Loading in Code

The model is loaded in several places:

### VectorstoreHandler
```python
# RAG/rag/multi_model_rag_pipeline_chatgpt.py
self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
self.semantic_model = self.semantic_model.cpu()
```

### HistoryDatabaseManager
```python
# RAG/utils/history_db_manager.py
self.model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
```

### AIEnhancedServiceRequestAnalyzer
```python
# analyzers/batch_sr_analyser.py
self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
```

---

## ⚠️ CPU vs GPU

The codebase forces CPU usage to avoid GPU-related errors:

```python
import os
os.environ['ACCELERATE_TORCH_DEVICE'] = 'cpu'
os.environ['CUDA_VISIBLE_DEVICES'] = ''

model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
```

This is because:
1. Avoids "meta tensor" errors with accelerate library
2. Works on machines without GPU
3. Memory is more predictable

---

## 📊 Model Files Description

| File | Purpose |
|------|---------|
| `config.json` | Base transformer configuration |
| `pytorch_model.bin` | Trained weights |
| `tokenizer_config.json` | Tokenizer settings |
| `vocab.txt` | Token vocabulary |
| `modules.json` | Model architecture |
| `sentence_bert_config.json` | Sentence-BERT specific config |

---

## 🔄 Updating the Model

To use a different model:

1. Download new model
2. Update path in code
3. Regenerate embeddings in ChromaDB (if dimensions differ)

**Note**: Changing embedding dimensions requires rebuilding the vector store!

---

## 🔗 Related

- [HuggingFace Model Page](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [Sentence Transformers Docs](https://www.sbert.net/)

---

*Part of SR-Analyzer Models Module*
