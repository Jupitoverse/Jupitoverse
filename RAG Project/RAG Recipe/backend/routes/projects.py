"""API: List/create/update/archive projects."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel
from project_store import (
    list_projects as _list_projects,
    get_project_config,
    create_project as _create_project,
    update_project_config,
    archive_project as _archive_project,
    get_monitoring as _get_monitoring,
    ensure_dirs,
    project_dir,
)

router = APIRouter(prefix="/api/projects", tags=["projects"])


class CreateProjectRequest(BaseModel):
    project_id: str
    name: str
    config: dict = {}


@router.get("")
def list_projects(include_archived: bool = False):
    return {"projects": _list_projects(include_archived=include_archived)}


@router.get("/{project_id}")
def get_project(project_id: str):
    cfg = get_project_config(project_id)
    if not cfg:
        raise HTTPException(status_code=404, detail="Project not found")
    return cfg


@router.post("")
def create_project(req: CreateProjectRequest):
    ensure_dirs()
    root = project_dir(req.project_id)
    if root.exists():
        raise HTTPException(status_code=400, detail="Project ID already exists")
    _create_project(req.project_id, req.name, req.config)
    return {"project_id": req.project_id, "name": req.name}


@router.patch("/{project_id}")
def update_project(project_id: str, updates: dict = Body(default={})):
    if not update_project_config(project_id, updates):
        raise HTTPException(status_code=404, detail="Project not found")
    return {"project_id": project_id, "updated": True}


@router.post("/{project_id}/archive")
def archive_project(project_id: str):
    if not _archive_project(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return {"project_id": project_id, "archived": True}


@router.get("/{project_id}/monitoring")
def get_monitoring(project_id: str):
    m = _get_monitoring(project_id)
    if not m:
        raise HTTPException(status_code=404, detail="Project not found")
    return m
