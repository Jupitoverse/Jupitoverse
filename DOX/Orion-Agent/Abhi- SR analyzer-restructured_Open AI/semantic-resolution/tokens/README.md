# 🔑 Tokens Module

> **API Token Storage for LLM Calls**

This folder contains API tokens used for calling the LLM service.

---

## 📁 Structure

```
tokens/
├── README.md
└── Tokens.xlsx          # API token storage
```

---

## 📋 Tokens.xlsx Format

| Column | Description |
|--------|-------------|
| Email | Token owner's email address |
| Token | API token string |

**Example:**
```
| Email               | Token                    |
|---------------------|--------------------------|
| user1@amdocs.com    | sk-abc123...             |
| user2@amdocs.com    | sk-def456...             |
| user3@amdocs.com    | sk-ghi789...             |
```

---

## 🔄 Token Rotation

The `TokenManager` class in `RAG/rag/multi_model_rag_pipeline_chatgpt.py` handles:

1. **Loading**: Reads all tokens from Excel
2. **Current Token**: Returns active token for API calls
3. **Exhaustion Detection**: Detects 429 (rate limit) responses
4. **Rotation**: Switches to next available token
5. **Status Tracking**: Reports available vs exhausted tokens

```python
from RAG.rag.multi_model_rag_pipeline_chatgpt import TokenManager

manager = TokenManager(tokens_file="tokens/Tokens.xlsx")

# Get current token
token = manager.get_current_token()
email = manager.get_current_email()

# Mark as exhausted (on 429 response)
has_more = manager.mark_exhausted()

# Get status
status = manager.get_status()  # "Tokens: 2/3 available"
```

---

## ⚠️ Security Notes

- **DO NOT** commit `Tokens.xlsx` to version control
- Add to `.gitignore`:
  ```
  tokens/Tokens.xlsx
  ```
- Keep backup in secure location
- Rotate tokens periodically

---

## 🔧 Adding New Tokens

1. Open `Tokens.xlsx` in Excel
2. Add new row with Email and Token
3. Save file
4. Tokens will be loaded on next pipeline run

---

## 📊 Usage Statistics

Token usage is tracked in `data/database/llm_usage_stats.json`:

```json
{
    "last_run": {
        "total_calls": 25,
        "input_tokens": 50000,
        "output_tokens": 15000,
        "cost": 0.1234
    }
}
```

---

*Part of SR-Analyzer Tokens Module*
