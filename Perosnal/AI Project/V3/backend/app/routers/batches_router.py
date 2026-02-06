from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user, require_ops

router = APIRouter(prefix="/batches", tags=["batches"])


@router.get("", response_model=list[schemas.BatchResponse])
def list_batches(
    project_id: int | None = None,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    q = db.query(models.Batch)
    if project_id is not None:
        q = q.filter(models.Batch.project_id == project_id)
    return q.all()


@router.post("", response_model=schemas.BatchResponse)
def create_batch(
    body: schemas.BatchCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_ops),
):
    batch = models.Batch(project_id=body.project_id, name=body.name)
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


@router.get("/{batch_id}", response_model=schemas.BatchResponse)
def get_batch(
    batch_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    b = db.query(models.Batch).filter(models.Batch.id == batch_id).first()
    if not b:
        raise HTTPException(404, "Batch not found")
    return b
