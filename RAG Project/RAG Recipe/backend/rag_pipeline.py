"""
RAG pipeline: embed, Chroma, LLM (Ollama or OpenAI with key rotation).
Uses project config for embedding model, chunking, and LLM.
"""
import json
import re
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

# Path for backend imports
_BACKEND = Path(__file__).resolve().parent
import sys
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))

from config import (
    PROJECT_DATA_DIR,
    CHROMA_DIR,
    OLLAMA_BASE_URL,
    OLLAMA_DEFAULT_MODEL,
    OPENAI_DEFAULT_MODEL,
    EMBEDDING_OPTIONS,
)
from chunking import chunk_text

try:
    import requests
except ImportError:
    requests = None

# Lazy load heavy libs
_sentence_model = None
_openai_client = None


def _get_collection(project_id: str, embedding_id: str):
    chroma_path = PROJECT_DATA_DIR / project_id / CHROMA_DIR
    chroma_path.mkdir(parents=True, exist_ok=True)
    try:
        import chromadb
        from chromadb.config import Settings
        client = chromadb.PersistentClient(path=str(chroma_path), settings=Settings(anonymized_telemetry=False))
        coll_name = "docs_" + (embedding_id or "default").replace("-", "_")[:50]
        return client.get_or_create_collection(name=coll_name, metadata={"description": "RAG docs"})
    except Exception:
        return None


def embed_texts_local(model_name: str, texts: List[str]) -> Optional[List[List[float]]]:
    global _sentence_model
    if _sentence_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _sentence_model = SentenceTransformer(model_name)
        except Exception:
            return None
    try:
        return _sentence_model.encode(texts).tolist()
    except Exception:
        return None


def embed_texts_openai(model_name: str, texts: List[str], api_key: str) -> Optional[List[List[float]]]:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        out = client.embeddings.create(model=model_name, input=texts)
        return [d.embedding for d in out.data]
    except Exception:
        return None


def embed_for_project(project_id: str, config: Dict[str, Any], texts: List[str]) -> Optional[List[List[float]]]:
    emb = (config.get("embedding") or "sentence_minilm")
    opts = EMBEDDING_OPTIONS.get(emb, {})
    model = opts.get("model", "all-MiniLM-L6-v2")
    typ = opts.get("type", "local")
    if typ == "openai":
        keys = (config.get("llm") or {}).get("openai_keys") or []
        api_key = keys[0].get("key") if keys else None
        if not api_key:
            return None
        return embed_texts_openai(model, texts, api_key)
    return embed_texts_local(model, texts)


def llm_ollama(prompt: str, model: str = None) -> Dict[str, Any]:
    model = model or OLLAMA_DEFAULT_MODEL
    url = f"{OLLAMA_BASE_URL}/api/generate"
    try:
        r = requests.post(url, json={"model": model, "prompt": prompt, "stream": False}, timeout=120)
        if r.status_code != 200:
            return {"error": f"Ollama {r.status_code}", "response": ""}
        data = r.json()
        return {"response": data.get("response", ""), "input_tokens": 0, "output_tokens": 0, "cost": 0.0}
    except Exception as e:
        return {"error": str(e), "response": ""}


def llm_openai(prompt: str, api_key: str, model: str = None) -> Dict[str, Any]:
    model = model or OPENAI_DEFAULT_MODEL
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        r = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
        )
        usage = r.usage or {}
        return {
            "response": (r.choices[0].message.content or ""),
            "input_tokens": getattr(usage, "prompt_tokens", 0) or 0,
            "output_tokens": getattr(usage, "completion_tokens", 0) or 0,
            "cost": 0.0,
        }
    except Exception as e:
        return {"error": str(e), "response": ""}


def llm_for_project(project_id: str, config: Dict[str, Any], prompt: str) -> Dict[str, Any]:
    llm_cfg = config.get("llm") or {}
    typ = llm_cfg.get("type") or "ollama_qwen"
    if typ == "openai":
        keys = llm_cfg.get("openai_keys") or []
        for k in keys:
            key = k.get("key") or k.get("token")
            if key:
                out = llm_openai(prompt, key, llm_cfg.get("model") or OPENAI_DEFAULT_MODEL)
                if "error" not in out:
                    return out
                if "429" in str(out.get("error", "")) or "quota" in str(out.get("error", "")).lower():
                    continue
                return out
        return {"error": "All API keys exhausted or invalid", "response": ""}
    model = llm_cfg.get("default_model") or OLLAMA_DEFAULT_MODEL
    return llm_ollama(prompt, model)


def add_documents_to_project(project_id: str, config: Dict[str, Any], chunks: List[str], metadatas: List[Dict] = None) -> bool:
    coll = _get_collection(project_id, config.get("embedding") or "sentence_minilm")
    if not coll:
        return False
    embeddings = embed_for_project(project_id, config, chunks)
    if not embeddings or len(embeddings) != len(chunks):
        return False
    metadatas = metadatas or [{}] * len(chunks)
    ids = [f"doc_{i}_{hash(c) % 10**10}" for i, c in enumerate(chunks)]
    try:
        coll.add(ids=ids, embeddings=embeddings, documents=chunks, metadatas=metadatas)
        return True
    except Exception:
        return False


def query_rag(project_id: str, config: Dict[str, Any], query: str, top_k: int = 4) -> Dict[str, Any]:
    coll = _get_collection(project_id, config.get("embedding") or "sentence_minilm")
    if not coll:
        return {"context": "", "sources": [], "response": "Vector store not ready. Add documents first."}
    q_emb = embed_for_project(project_id, config, [query])
    if not q_emb:
        return {"context": "", "sources": [], "response": "Embedding failed."}
    try:
        res = coll.query(query_embeddings=q_emb, n_results=top_k, include=["documents", "metadatas"])
        docs = (res.get("documents") or [[]])[0]
        context = "\n\n".join(docs) if docs else ""
    except Exception:
        context = ""
        docs = []
    prompt = f"""Use the following context to answer the question. If the context does not contain the answer, say so.

Context:
{context}

Question: {query}

Answer:"""
    start = time.perf_counter()
    llm_out = llm_for_project(project_id, config, prompt)
    elapsed = time.perf_counter() - start
    response = llm_out.get("response", "") or llm_out.get("error", "No response.")
    return {
        "context": context,
        "sources": docs,
        "response": response,
        "input_tokens": llm_out.get("input_tokens", 0),
        "output_tokens": llm_out.get("output_tokens", 0),
        "cost": llm_out.get("cost", 0.0),
        "elapsed_seconds": round(elapsed, 2),
    }
