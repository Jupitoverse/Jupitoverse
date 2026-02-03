"""API: Document upload (PDF, DOCX, TXT), store-only, ingest, and file download."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from fastapi.responses import FileResponse
from typing import List

from project_store import get_project_config, project_documents_path
from rag_pipeline import add_documents_to_project
from chunking import chunk_text

router = APIRouter(prefix="/api/projects", tags=["documents"])


def _read_txt(content: bytes) -> str:
    return content.decode("utf-8", errors="replace")


def _read_pdf(content: bytes) -> str:
    try:
        from PyPDF2 import PdfReader
        import io
        reader = PdfReader(io.BytesIO(content))
        return "\n".join(p.extract_text() or "" for p in reader.pages)
    except Exception:
        return ""


def _read_docx(content: bytes) -> str:
    try:
        import io
        from docx import Document
        doc = Document(io.BytesIO(content))
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception:
        return ""


@router.post("/{project_id}/documents/upload")
async def upload_documents(
    project_id: str,
    files: List[UploadFile] = File(default=[]),
    ingest: bool = Query(True, description="If false, only store files; call /documents/ingest later"),
):
    cfg = get_project_config(project_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Project not found")
    doc_dir = project_documents_path(project_id)
    doc_dir.mkdir(parents=True, exist_ok=True)
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    stored = []
    for f in files:
        content = await f.read()
        name = f.filename or "file"
        (doc_dir / name).write_bytes(content)
        stored.append(name)
    if not ingest:
        return {"stored": len(stored), "files": stored, "ok": True}
    chunking = cfg.get("chunking") or {}
    splitter = chunking.get("splitter_id", "character")
    chunk_size = chunking.get("chunk_size", 512)
    chunk_overlap = chunking.get("chunk_overlap", 50)
    all_chunks = []
    all_metas = []
    for name in stored:
        path = doc_dir / name
        content = path.read_bytes()
        if name.lower().endswith(".pdf"):
            text = _read_pdf(content)
        elif name.lower().endswith(".docx"):
            text = _read_docx(content)
        else:
            text = _read_txt(content)
        if not text.strip():
            continue
        chunks = chunk_text(text, splitter, chunk_size, chunk_overlap)
        for c in chunks:
            all_chunks.append(c)
            all_metas.append({"source": name})
    if not all_chunks:
        return {"stored": len(stored), "files": stored, "ingested": 0, "ok": True}
    ok = add_documents_to_project(project_id, cfg, all_chunks, all_metas)
    if not ok:
        raise HTTPException(status_code=500, detail="Ingest failed")
    return {"ingested": len(all_chunks), "files": stored, "ok": True}


@router.post("/{project_id}/documents/ingest")
def ingest_documents(project_id: str):
    """Chunk and ingest all files in project documents folder into vector store."""
    cfg = get_project_config(project_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Project not found")
    doc_dir = project_documents_path(project_id)
    if not doc_dir.exists():
        return {"ingested": 0, "ok": True}
    chunking = cfg.get("chunking") or {}
    splitter = chunking.get("splitter_id", "character")
    chunk_size = chunking.get("chunk_size", 512)
    chunk_overlap = chunking.get("chunk_overlap", 50)
    all_chunks = []
    all_metas = []
    for path in doc_dir.iterdir():
        if not path.is_file():
            continue
        name = path.name
        content = path.read_bytes()
        if name.lower().endswith(".pdf"):
            text = _read_pdf(content)
        elif name.lower().endswith(".docx"):
            text = _read_docx(content)
        else:
            text = _read_txt(content)
        if not text.strip():
            continue
        chunks = chunk_text(text, splitter, chunk_size, chunk_overlap)
        for c in chunks:
            all_chunks.append(c)
            all_metas.append({"source": name})
    if not all_chunks:
        return {"ingested": 0, "ok": True}
    ok = add_documents_to_project(project_id, cfg, all_chunks, all_metas)
    if not ok:
        raise HTTPException(status_code=500, detail="Ingest failed")
    return {"ingested": len(all_chunks), "ok": True}


@router.get("/{project_id}/documents/list")
def list_documents(project_id: str):
    cfg = get_project_config(project_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Project not found")
    doc_dir = project_documents_path(project_id)
    if not doc_dir.exists():
        return {"files": []}
    files = [p.name for p in doc_dir.iterdir() if p.is_file()]
    return {"files": files}


@router.get("/{project_id}/documents/file/{filename:path}")
def get_document_file(project_id: str, filename: str):
    """Download or view a document file. Easy access from UI."""
    cfg = get_project_config(project_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Project not found")
    doc_dir = project_documents_path(project_id).resolve()
    path = (doc_dir / filename).resolve()
    try:
        path.relative_to(doc_dir)
    except ValueError:
        raise HTTPException(status_code=404, detail="File not found")
    if not path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, filename=path.name)
