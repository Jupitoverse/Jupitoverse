"""RAG Recipe - FastAPI app. Run from repo root: cd "RAG Recipe" && uvicorn backend.app:app --reload"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

try:
    from backend.routes.options import router as options_router
    from backend.routes.chunking_routes import router as chunking_router
    from backend.routes.projects import router as projects_router
except ImportError:
    from routes.options import router as options_router
    from routes.chunking_routes import router as chunking_router
    from routes.projects import router as projects_router

app = FastAPI(title="RAG Recipe", version="0.1.0")

# Static and templates (relative to RAG Recipe root)
static_path = ROOT / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
templates = Jinja2Templates(directory=str(ROOT / "templates"))

app.include_router(options_router)
app.include_router(chunking_router)
app.include_router(projects_router)

# RAG routes loaded in background so server starts fast (chromadb/pandas can be slow)
import threading
_rag_loaded = False
def _load_rag_routes():
    global _rag_loaded
    if _rag_loaded:
        return
    try:
        from backend.routes.chat import router as chat_router
        from backend.routes.documents import router as documents_router
        from backend.routes.excel_routes import router as excel_router
    except ImportError:
        from routes.chat import router as chat_router
        from routes.documents import router as documents_router
        from routes.excel_routes import router as excel_router
    app.include_router(chat_router)
    app.include_router(documents_router)
    app.include_router(excel_router)
    _rag_loaded = True

@app.on_event("startup")
def startup():
    threading.Thread(target=_load_rag_routes, daemon=True).start()


@app.get("/health")
def health():
    """Health check - returns 200 if app is running."""
    return {"status": "ok", "app": "RAG Recipe"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"request": request})


@app.get("/rag-recipe", response_class=HTMLResponse)
def rag_recipe(request: Request):
    return templates.TemplateResponse(request, "rag_recipe.html", {"request": request})


@app.get("/add-project", response_class=HTMLResponse)
def add_project(request: Request):
    return templates.TemplateResponse(request, "add_project.html", {"request": request})


@app.get("/project/{project_id}", response_class=HTMLResponse)
def project_detail(request: Request, project_id: str):
    return templates.TemplateResponse(request, "project_detail.html", {"request": request, "project_id": project_id})
