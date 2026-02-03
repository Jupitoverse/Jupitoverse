"""API: Excel upload, row RAG results, feedback/regeneration."""
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List

import pandas as pd

from project_store import get_project_config, project_excel_history_path, project_dir
from rag_pipeline import query_rag, add_documents_to_project
from chunking import chunk_text

router = APIRouter(prefix="/api/projects", tags=["excel"])

EXCEL_RESULTS_FILE = "excel_results.json"


def _clean_row_text(row: pd.Series) -> str:
    parts = [str(v).strip() for v in row if pd.notna(v) and str(v).strip()]
    return " ".join(parts)


@router.post("/{project_id}/excel/upload")
async def upload_excel(project_id: str, file: UploadFile = File(...)):
    cfg = get_project_config(project_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Project not found")
    if not file.filename or not (file.filename.lower().endswith(".xlsx") or file.filename.lower().endswith(".xls")):
        raise HTTPException(status_code=400, detail="Upload .xlsx or .xls file")
    content = await file.read()
    try:
        import io
        df = pd.read_excel(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Excel: {e}")
    excel_dir = project_excel_history_path(project_id)
    excel_dir.mkdir(parents=True, exist_ok=True)
    (excel_dir / file.filename).write_bytes(content)
    chunking = cfg.get("chunking") or {}
    splitter = chunking.get("splitter_id", "character")
    chunk_size = chunking.get("chunk_size", 512)
    chunk_overlap = chunking.get("chunk_overlap", 50)
    results = []
    for idx, row in df.iterrows():
        prompt_text = _clean_row_text(row)
        if not prompt_text:
            results.append({"row_index": int(idx), "prompt": "", "response": "", "context": ""})
            continue
        out = query_rag(project_id, cfg, prompt_text, top_k=4)
        results.append({
            "row_index": int(idx),
            "prompt": prompt_text[:500],
            "response": out.get("response", ""),
            "context": out.get("context", "")[:1000],
            "input_tokens": out.get("input_tokens", 0),
            "output_tokens": out.get("output_tokens", 0),
        })
    results_path = project_dir(project_id) / EXCEL_RESULTS_FILE
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump({"filename": file.filename, "rows": results}, f, indent=2)
    for r in results:
        if r.get("prompt"):
            chunks = chunk_text(r["prompt"], splitter, chunk_size, chunk_overlap)
            if chunks:
                add_documents_to_project(project_id, cfg, chunks, [{"source": "excel", "row": r["row_index"]}])
    return {"rows": len(results), "filename": file.filename, "ok": True}


@router.get("/{project_id}/excel/results")
def get_excel_results(project_id: str):
    cfg = get_project_config(project_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Project not found")
    results_path = project_dir(project_id) / EXCEL_RESULTS_FILE
    if not results_path.exists():
        return {"rows": [], "filename": None}
    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {"rows": data.get("rows", []), "filename": data.get("filename")}


class RowFeedbackRequest(BaseModel):
    row_index: int
    feedback: Optional[str] = None
    regenerate: bool = False


@router.get("/{project_id}/excel/row-result")
def get_row_result(project_id: str, row_index: int):
    cfg = get_project_config(project_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Project not found")
    results_path = project_dir(project_id) / EXCEL_RESULTS_FILE
    if not results_path.exists():
        raise HTTPException(status_code=404, detail="No excel results")
    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    rows = data.get("rows", [])
    for r in rows:
        if r.get("row_index") == row_index:
            return r
    raise HTTPException(status_code=404, detail="Row not found")


@router.post("/{project_id}/excel/feedback")
def submit_feedback(project_id: str, req: RowFeedbackRequest):
    cfg = get_project_config(project_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Project not found")
    results_path = project_dir(project_id) / EXCEL_RESULTS_FILE
    if not results_path.exists():
        raise HTTPException(status_code=404, detail="No excel results")
    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    rows = data.get("rows", [])
    for r in rows:
        if r.get("row_index") == req.row_index:
            if req.feedback:
                r["feedback"] = req.feedback
            if req.regenerate:
                prompt = r.get("prompt", "")
                if prompt:
                    out = query_rag(project_id, cfg, prompt, top_k=4)
                    r["response"] = out.get("response", "")
                    r["context"] = out.get("context", "")[:1000]
            break
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return {"ok": True}
