# 🧠 all-MiniLM-L6-v2 Model

> **Pre-trained Sentence Transformer**

---

## 📊 Specifications

| Property | Value |
|----------|-------|
| Model | all-MiniLM-L6-v2 |
| Dimensions | 384 |
| Max Tokens | 256 |
| Size | ~22MB |
| Language | English |

---

## 🔧 Usage

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    'models/sentence-transformers_all-MiniLM-L6-v2'
)

embeddings = model.encode(["Hello world"])
```

---

## 📁 Files

| File | Description |
|------|-------------|
| config.json | Model config |
| pytorch_model.bin | Weights |
| tokenizer_config.json | Tokenizer config |
| vocab.txt | Vocabulary |

---

## ⚠️ Notes

- Do not modify files
- Model downloads automatically if missing

---

*Part of SR-Analyzer Models Module*
