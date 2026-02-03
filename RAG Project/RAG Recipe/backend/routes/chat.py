"""API: RAG chat and document ingest."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from project_store import get_project_config, append_monitoring
from rag_pipeline import query_rag, add_documents_to_project
from chunking import chunk_text

router = APIRouter(prefix="/api/projects", tags=["chat"])


class ChatRequest(BaseModel):
    message: str
    top_k: int = 4


@router.post("/{project_id}/chat")
def chat_endpoint(project_id: str, req: ChatRequest):
    cfg = get_project_config(project_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Project not found")
    out = query_rag(project_id, cfg, req.message, top_k=req.top_k)
    if out.get("input_tokens") or out.get("output_tokens"):
        append_monitoring(project_id, input_tokens=out.get("input_tokens", 0), output_tokens=out.get("output_tokens", 0), cost_usd=out.get("cost", 0))
    return out


class IngestRequest(BaseModel):
    texts: List[str]
    metadatas: Optional[List[dict]] = None


@router.post("/{project_id}/ingest")
def ingest_texts(project_id: str, req: IngestRequest):
    cfg = get_project_config(project_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Project not found")
    chunking = cfg.get("chunking") or {}
    splitter = chunking.get("splitter_id", "character")
    chunk_size = chunking.get("chunk_size", 512)
    chunk_overlap = chunking.get("chunk_overlap", 50)
    all_chunks = []
    all_metas = []
    for i, t in enumerate(req.texts):
        chunks = chunk_text(t, splitter, chunk_size, chunk_overlap)
        meta = (req.metadatas or [{}])[i] if (req.metadatas and i < len(req.metadatas)) else {}
        for c in chunks:
            all_chunks.append(c)
            all_metas.append(meta)
    ok = add_documents_to_project(project_id, cfg, all_chunks, all_metas)
    if not ok:
        raise HTTPException(status_code=500, detail="Ingest failed (embed or vector store)")
    return {"ingested": len(all_chunks), "ok": True}
