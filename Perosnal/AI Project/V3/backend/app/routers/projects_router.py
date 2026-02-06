from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user, require_ops

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[schemas.ProjectResponse])
def list_projects(
    workspace_id: int | None = None,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    q = db.query(models.Project)
    if workspace_id is not None:
        q = q.filter(models.Project.workspace_id == workspace_id)
    return q.all()


@router.post("", response_model=schemas.ProjectResponse)
def create_project(
    body: schemas.ProjectCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_ops),
):
    proj = models.Project(
        workspace_id=body.workspace_id,
        name=body.name,
        description=body.description or "",
        pipeline_stages=body.pipeline_stages or ["L1", "Review", "Done"],
        response_schema=body.response_schema or {"sentiment": "single_select", "notes": "free_text"},
    )
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj


@router.get("/{project_id}", response_model=schemas.ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    p = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not p:
        raise HTTPException(404, "Project not found")
    return p
