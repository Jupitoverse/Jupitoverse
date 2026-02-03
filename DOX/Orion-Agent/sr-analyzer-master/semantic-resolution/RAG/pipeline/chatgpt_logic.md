# 🔐 ChatGPT API Integration & Token Management

> **How SR-Analyzer connects to ChatGPT via the AI Framework API**

This document explains how the Multi-Model RAG Pipeline authenticates and communicates with ChatGPT for LLM-powered SR analysis.

---

## 📡 API Overview

### Endpoint
```
https://ai-framework1:8085/api/v1/call_llm
```

This is an **internal AI Framework gateway** that proxies requests to OpenAI's ChatGPT models. It handles authentication, rate limiting, and usage tracking.

### Default Model
```
gpt-4.1
```

---

## 🔑 Token Management

### Token Source

Tokens are stored in an Excel file:
```
sr-analyzer/semantic-resolution/tokens/Tokens.xlsx
```

**Required Excel Columns:**
| Column | Description |
|--------|-------------|
| `Email` or `Name` | User identifier for the token |
| `Token` | API authentication token |

### TokenManager Class

The `TokenManager` class (`multi_model_rag_pipeline_chatgpt.py`) handles:

1. **Loading tokens** from Excel on initialization
2. **Automatic rotation** when a token hits rate limits
3. **Tracking exhausted tokens** to avoid retry loops

```python
class TokenManager:
    def __init__(self, tokens_file: Path = None):
        # Default path: tokens/Tokens.xlsx
        self.tokens: List[Dict[str, str]] = []
        self.current_index = 0
        self.exhausted_tokens: set = set()
        self._load_tokens()
    
    def get_current_token(self) -> Optional[str]:
        # Returns active token, auto-rotating if exhausted
        
    def mark_exhausted(self) -> bool:
        # Marks current token as exhausted, rotates to next
        # Returns False if ALL tokens exhausted
```

---

## 📤 API Request Format

### Request Headers

```python
headers = {
    "Content-Type": "application/json",
    "accept": "application/json",
    "API-Key": "<token>",                    # From TokenManager
    "X-Effective-Caller": "<email>"          # User email from Tokens.xlsx
}
```

### Request Payload

```python
payload = {
    "llm_model": "gpt-4.1",
    "messages": [
        {"role": "system", "content": "<system prompt>"},
        {"role": "user", "content": "<user prompt>"}
    ],
    "max_tokens": 8000
}
```

### Example cURL

```bash
curl -X POST "https://ai-framework1:8085/api/v1/call_llm" \
  -H "Content-Type: application/json" \
  -H "API-Key: YOUR_TOKEN_HERE" \
  -H "X-Effective-Caller: user@company.com" \
  -d '{
    "llm_model": "gpt-4.1",
    "messages": [
      {"role": "system", "content": "You are an expert analyst."},
      {"role": "user", "content": "Analyze this issue..."}
    ],
    "max_tokens": 8000
  }'
```

---

## 📥 API Response Format

### Successful Response (200)

```json
{
    "message": "<LLM response text>",
    "input_tokens": 1500,
    "output_tokens": 800,
    "cost": 0.045,
    "finish_reason": "stop"
}
```

### Rate Limited Response (429)

When a token exceeds its quota:
- `TokenManager` marks it as exhausted
- Automatically rotates to the next available token
- Retries the request

---

## 🔄 Token Rotation Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    API Request Flow                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Get token from TokenManager                              │
│         │                                                    │
│         ▼                                                    │
│  2. Make POST request to API                                 │
│         │                                                    │
│         ├── 200 OK ───────► Return response, track usage     │
│         │                                                    │
│         ├── 429 Rate Limit ──► Mark token exhausted          │
│         │         │                                          │
│         │         ▼                                          │
│         │   More tokens available?                           │
│         │         │                                          │
│         │    YES  │   NO                                     │
│         │    ▼    │   ▼                                      │
│         │  Rotate │  Return error                            │
│         │  & retry│  "All tokens exhausted"                  │
│         │         │                                          │
│         └── Other Error ──► Return error response            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Usage Tracking

The `MultiModelLLM` class tracks usage across all calls:

```python
# Tracked metrics
self.total_calls = 0           # Number of LLM calls made
self.total_input_tokens = 0    # Total prompt tokens
self.total_output_tokens = 0   # Total completion tokens
self.total_cost = 0.0          # Total API cost (USD)

# Get usage summary
usage = llm.get_usage()
print(f"Calls: {usage['total_calls']}")
print(f"Tokens: {usage['total_input_tokens']} in / {usage['total_output_tokens']} out")
print(f"Cost: ${usage['total_cost']:.4f}")
print(f"Status: {usage['tokens_status']}")  # e.g., "Tokens: 3/5 available"
```

---

## ⚙️ Configuration

### Environment Variables

```bash
# Proxy bypass for internal API
NO_PROXY=ai-framework1
no_proxy=ai-framework1
```

### Command Line Arguments

```bash
python multi_model_rag_pipeline_chatgpt.py \
    --tokens /path/to/Tokens.xlsx \
    --model gpt-4.1
```

---

## 🛡️ Error Handling

| Status Code | Meaning | Action |
|-------------|---------|--------|
| 200 | Success | Parse response, track usage |
| 429 | Rate Limited | Rotate token, retry |
| 500+ | Server Error | Log error, return failure |
| Timeout | No response in 300s | Return error |

---

## 📁 File Locations

```
sr-analyzer/
└── semantic-resolution/
    ├── tokens/
    │   └── Tokens.xlsx          # API tokens (Email, Token columns)
    └── RAG/
        └── pipeline/
            └── multi_model_rag_pipeline_chatgpt.py  # TokenManager & MultiModelLLM
```

---

## 🔗 Related Components

- **TokenManager**: Token loading & rotation
- **MultiModelLLM**: LLM wrapper with retry logic
- **MultiModelSRPipeline**: Main pipeline using the LLM

---

*Part of SR-Analyzer Multi-Model RAG Pipeline*

