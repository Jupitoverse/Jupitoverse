"""API: Chunking preview (metrics + spans for color-coded UI)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fastapi import APIRouter
from pydantic import BaseModel
from chunking import chunk_preview

router = APIRouter(prefix="/api/chunking", tags=["chunking"])


class ChunkPreviewRequest(BaseModel):
    text: str = "This is the text I would like to chunk up. It is the example text for this exercise."
    splitter_id: str = "character"
    chunk_size: int = 35
    chunk_overlap: int = 4


@router.post("/preview")
def preview_chunking(req: ChunkPreviewRequest):
    """Return chunks, metrics, and spans for UI (splitter dropdown + sliders + color preview)."""
    result = chunk_preview(
        text=req.text,
        splitter_id=req.splitter_id,
        chunk_size=req.chunk_size,
        chunk_overlap=req.chunk_overlap,
    )
    return result
