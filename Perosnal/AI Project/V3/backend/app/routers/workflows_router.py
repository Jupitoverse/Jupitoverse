from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas
from ..auth import get_current_user, require_ops

router = APIRouter(prefix="/workflows", tags=["workflows"])


@router.get("", response_model=list[schemas.WorkflowResponse])
def list_workflows(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    return db.query(models.Workflow).order_by(models.Workflow.created_at).all()


@router.post("", response_model=schemas.WorkflowResponse)
def create_workflow(
    body: schemas.WorkflowCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_ops),
):
    w = models.Workflow(name=body.name, description=body.description or "")
    db.add(w)
    db.commit()
    db.refresh(w)
    return w


@router.get("/{workflow_id}", response_model=schemas.WorkflowResponse)
def get_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    w = db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()
    if not w:
        raise HTTPException(404, "Workflow not found")
    return w


@router.get("/{workflow_id}/nodes", response_model=list[schemas.WorkflowNodeResponse])
def list_workflow_nodes(
    workflow_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    w = db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()
    if not w:
        raise HTTPException(404, "Workflow not found")
    return db.query(models.WorkflowNode).filter(models.WorkflowNode.workflow_id == workflow_id).all()


@router.post("/{workflow_id}/nodes", response_model=schemas.WorkflowNodeResponse)
def add_workflow_node(
    workflow_id: int,
    body: schemas.WorkflowNodeBase,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_ops),
):
    w = db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()
    if not w:
        raise HTTPException(404, "Workflow not found")
    node = models.WorkflowNode(
        workflow_id=workflow_id,
        node_type=body.node_type,
        name=body.name,
        config=body.config or {},
    )
    db.add(node)
    db.commit()
    db.refresh(node)
    return node


@router.post("/{workflow_id}/edges", response_model=schemas.WorkflowEdgeResponse)
def add_workflow_edge(
    workflow_id: int,
    body: schemas.WorkflowEdgeCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_ops),
):
    if body.workflow_id != workflow_id:
        raise HTTPException(400, "workflow_id mismatch")
    w = db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()
    if not w:
        raise HTTPException(404, "Workflow not found")
    edge = models.WorkflowEdge(
        workflow_id=workflow_id,
        from_node_id=body.from_node_id,
        to_node_id=body.to_node_id,
    )
    db.add(edge)
    db.commit()
    db.refresh(edge)
    return edge


@router.get("/{workflow_id}/edges", response_model=list[schemas.WorkflowEdgeResponse])
def list_workflow_edges(
    workflow_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    w = db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()
    if not w:
        raise HTTPException(404, "Workflow not found")
    return db.query(models.WorkflowEdge).filter(models.WorkflowEdge.workflow_id == workflow_id).all()


@router.delete("/{workflow_id}")
def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(require_ops),
):
    w = db.query(models.Workflow).filter(models.Workflow.id == workflow_id).first()
    if not w:
        raise HTTPException(404, "Workflow not found")
    db.delete(w)
    db.commit()
    return {"ok": True}
