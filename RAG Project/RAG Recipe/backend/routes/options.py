"""API: LLM, Embedding, Chunking options (for dropdowns + pros/cons)."""
from fastapi import APIRouter

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from config import LLM_OPTIONS_META, EMBEDDING_OPTIONS, CHUNKING_OPTIONS

router = APIRouter(prefix="/api/options", tags=["options"])


@router.get("/llm")
def get_llm_options():
    """Return LLM choices with pros/cons for UI."""
    return {"options": list(LLM_OPTIONS_META.values())}


@router.get("/embedding")
def get_embedding_options():
    """Return embedding choices with pros/cons for UI."""
    return {"options": list(EMBEDDING_OPTIONS.values())}


@router.get("/chunking")
def get_chunking_options():
    """Return chunking/splitter choices with pros/cons and min/max for UI."""
    return {"options": list(CHUNKING_OPTIONS.values())}
