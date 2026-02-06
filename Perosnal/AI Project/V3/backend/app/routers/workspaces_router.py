from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user, require_ops

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.get("", response_model=list[schemas.WorkspaceResponse])
def list_workspaces(
    db: Session = Depends(get_db),
    user: models.User = Depends(require_ops),
):
    return db.query(models.Workspace).all()


@router.post("", response_model=schemas.WorkspaceResponse)
def create_workspace(
    body: schemas.WorkspaceCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_ops),
):
    w = models.Workspace(name=body.name, description=body.description or "")
    db.add(w)
    db.commit()
    db.refresh(w)
    return w


@router.get("/{workspace_id}", response_model=schemas.WorkspaceResponse)
def get_workspace(
    workspace_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    w = db.query(models.Workspace).filter(models.Workspace.id == workspace_id).first()
    if not w:
        raise HTTPException(404, "Workspace not found")
    return w
