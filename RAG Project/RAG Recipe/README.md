# RAG Recipe

UI-based RAG project with FastAPI. Configure LLM (Ollama Qwen or OpenAI with multi-key loop), embedding model, and chunking; create projects; chat over your documents; upload Excel for row-by-row RAG; monitor usage.

## How to run

**Option 1 – Double-click (recommended)**  
1. Open File Explorer and go to: `C:\Users\abhisha3\Desktop\Projects\RAG Project\RAG Recipe`  
2. Double-click **RUN_SERVER.bat**  
3. A console window will open; wait until you see something like: `Uvicorn running on http://127.0.0.1:8000`  
4. In your browser open: **http://127.0.0.1:8000**

**Option 2 – From a terminal**  
1. Open Command Prompt or PowerShell.  
2. Run:
```cmd
cd "C:\Users\abhisha3\Desktop\Projects\RAG Project\RAG Recipe"
set PYTHONPATH=%CD%
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```
3. In your browser open: **http://127.0.0.1:8000**

**Option 3 – Using main.py**  
```cmd
cd "C:\Users\abhisha3\Desktop\Projects\RAG Project\RAG Recipe"
python main.py
```
Then open: **http://127.0.0.1:8000**

If the app does not load: install dependencies with `pip install -r requirements.txt` and try again. The first start can take a few seconds while RAG routes load in the background.

## What’s included

- **Home** (`/`) – Entry page with links.
- **RAG Recipe** (`/rag-recipe`) – List projects; link to **Add Project**.
- **Add Project** (`/add-project`) – Sliding steps:
  1. **LLM** – Ollama Qwen (local) or OpenAI (multiple API keys with tag; rotation when credit exhausts).
  2. **Embedding** – SentenceTransformer (all-MiniLM, paraphrase-MiniLM) or OpenAI (text-embedding-3-small, ada-002).
  3. **Chunking** – Splitter (Character, Recursive, Sentence), chunk size/overlap, live metrics and color-coded preview.
  4. **Create** – Set project name and create the RAG project.

- **Project detail** (`/project/{project_id}`) – Tabs:
  - **Chatbot** – RAG chat (query → vector store → LLM).
  - **Documents** – Upload PDF, DOCX, TXT; chunk and ingest into Chroma.
  - **Excel** – Upload Excel; each row is cleaned and run through RAG; click a row to see result; feedback and regeneration.
  - **Monitoring** – Total/today/last call: tokens, cost (USD).

- **Data** – Per-project under `project_data/<project_id>/` (config, chroma, documents, excel_history, monitoring.json). Removing a project archives it; archived projects are permanently deleted after 10 days.

## Requirements

```bash
pip install -r requirements.txt
```

Heavy optional deps: `sentence-transformers`, `chromadb`, `openai` (for cloud options). For local-only: Ollama running and `sentence-transformers` + `chromadb` are enough for the pipeline.
