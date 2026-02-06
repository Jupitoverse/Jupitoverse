"""Rater: claim next task, submit annotation. Reviewer: list tasks in review, submit review."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user, require_rater, require_reviewer

router = APIRouter(prefix="/queue", tags=["queue"])


@router.get("/next", response_model=schemas.TaskResponse | None)
def get_next_task(
    project_id: int | None = None,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_rater),
):
    """FIFO: next pending task (optionally in project) for this rater to claim."""
    q = (
        db.query(models.Task)
        .filter(models.Task.status == "pending")
        .order_by(models.Task.created_at)
    )
    if project_id is not None:
        q = q.join(models.Batch).filter(models.Batch.project_id == project_id)
    task = q.first()
    if not task:
        return None
    task.status = "claimed"
    task.claimed_by_id = user.id
    task.claimed_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task


@router.get("/my-tasks", response_model=list[schemas.TaskResponse])
def my_claimed_tasks(
    db: Session = Depends(get_db),
    user: models.User = Depends(require_rater),
):
    return (
        db.query(models.Task)
        .filter(models.Task.claimed_by_id == user.id, models.Task.status == "claimed")
        .order_by(models.Task.claimed_at)
        .all()
    )


@router.post("/tasks/{task_id}/submit", response_model=schemas.AnnotationResponse)
def submit_annotation(
    task_id: int,
    body: schemas.AnnotationCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_rater),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    if task.claimed_by_id != user.id:
        raise HTTPException(403, "Not your task")
    ann = models.Annotation(
        task_id=task_id,
        user_id=user.id,
        response=body.response,
        pipeline_stage=task.pipeline_stage or "L1",
    )
    db.add(ann)
    task.status = "in_review"
    task.pipeline_stage = "Review"
    db.commit()
    db.refresh(ann)
    return ann


# --- Reviewer ---

@router.get("/review", response_model=list[schemas.TaskResponse])
def list_tasks_for_review(
    db: Session = Depends(get_db),
    user: models.User = Depends(require_reviewer),
):
    return (
        db.query(models.Task)
        .filter(models.Task.status == "in_review")
        .order_by(models.Task.claimed_at)
        .all()
    )


@router.post("/review/{task_id}/approve")
def approve_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_reviewer),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    task.status = "done"
    task.pipeline_stage = "Done"
    ann = models.Annotation(
        task_id=task_id,
        user_id=user.id,
        response={},
        pipeline_stage="Review",
    )
    db.add(ann)
    db.commit()
    return {"ok": True, "task_id": task_id}


@router.post("/review/{task_id}/submit", response_model=schemas.AnnotationResponse)
def submit_review(
    task_id: int,
    body: schemas.AnnotationCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_reviewer),
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    ann = models.Annotation(
        task_id=task_id,
        user_id=user.id,
        response=body.response,
        pipeline_stage="Review",
    )
    db.add(ann)
    task.status = "done"
    task.pipeline_stage = "Done"
    db.commit()
    db.refresh(ann)
    return ann
