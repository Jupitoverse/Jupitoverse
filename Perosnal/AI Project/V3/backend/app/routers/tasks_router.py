from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user, require_ops

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[schemas.TaskResponse])
def list_tasks(
    batch_id: int | None = None,
    workflow_id: int | None = None,
    status: str | None = None,
    sort: str | None = None,  # created_at, status, id
    order: str | None = "asc",  # asc | desc
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    q = db.query(models.Task)
    if batch_id is not None:
        q = q.filter(models.Task.batch_id == batch_id)
    if workflow_id is not None:
        q = q.filter(models.Task.workflow_id == workflow_id)
    if status is not None:
        q = q.filter(models.Task.status == status)
    # Admin/Ops see all; others see only their claimed tasks (visibility)
    if user.role not in ("admin", "ops"):
        q = q.filter(models.Task.claimed_by_id == user.id)
    order_col = models.Task.created_at
    if sort == "status":
        order_col = models.Task.status
    elif sort == "id":
        order_col = models.Task.id
    if order == "desc":
        q = q.order_by(order_col.desc())
    else:
        q = q.order_by(order_col)
    return q.all()


@router.post("", response_model=schemas.TaskResponse)
def create_task(
    body: schemas.TaskCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_ops),
):
    task = models.Task(batch_id=body.batch_id, content=body.content)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.post("/bulk", response_model=list[schemas.TaskResponse])
def create_tasks_bulk(
    body: schemas.BulkTasksRequest,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_ops),
):
    created = []
    for t in body.tasks:
        task = models.Task(batch_id=body.batch_id, content=t.get("content", t))
        db.add(task)
        db.flush()
        created.append(task)
    db.commit()
    for t in created:
        db.refresh(t)
    return created


@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    t = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not t:
        raise HTTPException(404, "Task not found")
    return t


@router.get("/{task_id}/annotations", response_model=list[schemas.AnnotationResponse])
def get_task_annotations(
    task_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    t = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not t:
        raise HTTPException(404, "Task not found")
    return db.query(models.Annotation).filter(models.Annotation.task_id == task_id).all()


@router.patch("/{task_id}/stage")
def set_task_stage(
    task_id: int,
    stage: str,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_ops),
):
    t = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not t:
        raise HTTPException(404, "Task not found")
    t.pipeline_stage = stage
    t.status = "in_review" if stage == "Review" else ("done" if stage == "Done" else t.status)
    db.commit()
    return {"ok": True, "task_id": task_id, "pipeline_stage": stage}
