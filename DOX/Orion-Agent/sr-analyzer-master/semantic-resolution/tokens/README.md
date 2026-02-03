# 🔑 Tokens Module

> **API Token Storage**

Stores API tokens for the LLM service.

---

## 📁 Structure

```
tokens/
├── README.md
└── Tokens.xlsx    # API tokens (required)
```

---

## 📋 Tokens.xlsx Format

| Email | Token |
|-------|-------|
| user1@amdocs.com | api-token-1 |
| user2@amdocs.com | api-token-2 |
| user3@amdocs.com | api-token-3 |

> ⚠️ **Required**: System will not start without valid tokens.

---

## 🔄 Token Rotation

The `TokenManager` class in `RAG/pipeline/multi_model_rag_pipeline_chatgpt.py` handles:

1. **Loading** tokens from Excel
2. **Rotation** when quota exhausted ($4/day limit)
3. **Status tracking** (available/exhausted)

### Usage

```python
from RAG.pipeline.multi_model_rag_pipeline_chatgpt import TokenManager

manager = TokenManager("tokens/Tokens.xlsx")

# Get current token
token = manager.get_current_token()

# Mark exhausted (rotate to next)
manager.mark_exhausted()

# Check status
print(manager.get_status())  # "Tokens: 3/5 available"
```

---

## 💡 Best Practices

1. **Multiple Tokens**: Add 3-5 tokens for redundancy
2. **Daily Limits**: Each token has $4/day limit
3. **Security**: Don't commit `Tokens.xlsx` to version control
4. **Backup**: Keep backup of valid tokens

---

## 🔗 Related

- [RAG/pipeline/README.md](../RAG/pipeline/README.md) - TokenManager

---

*Part of SR-Analyzer Tokens Module*
