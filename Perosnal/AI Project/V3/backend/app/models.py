from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from .database import Base


class UserRole(str, enum.Enum):
    ops = "ops"
    rater = "rater"
    reviewer = "reviewer"
    admin = "admin"


class TaskStatus(str, enum.Enum):
    pending = "pending"
    claimed = "claimed"
    in_review = "in_review"
    done = "done"
    archived = "archived"


class PipelineStage(str, enum.Enum):
    l1 = "L1"
    review = "Review"
    done = "Done"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), default="")
    role = Column(String(50), nullable=False, default=UserRole.rater.value)
    created_at = Column(DateTime, default=datetime.utcnow)


class Workspace(Base):
    __tablename__ = "workspaces"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    projects = relationship("Project", back_populates="workspace")


class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    pipeline_stages = Column(JSON, default=["L1", "Review", "Done"])  # ordered stages
    response_schema = Column(JSON, default=dict)  # e.g. {"sentiment": "single_select", "notes": "free_text"}
    created_at = Column(DateTime, default=datetime.utcnow)
    workspace = relationship("Workspace", back_populates="projects")
    batches = relationship("Batch", back_populates="project")


class Batch(Base):
    __tablename__ = "batches"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    project = relationship("Project", back_populates="batches")
    tasks = relationship("Task", back_populates="batch", order_by="Task.created_at")


# --- Workflow (PRD-aligned: graph of nodes and edges) ---
class Workflow(Base):
    __tablename__ = "workflows"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    nodes = relationship("WorkflowNode", back_populates="workflow", foreign_keys="WorkflowNode.workflow_id")
    edges = relationship("WorkflowEdge", back_populates="workflow", foreign_keys="WorkflowEdge.workflow_id")


class WorkflowNode(Base):
    __tablename__ = "workflow_nodes"
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    node_type = Column(String(50), nullable=False)  # form, review, api_call, db_update, manual
    name = Column(String(255), nullable=False)
    config = Column(JSON, default=dict)  # optional node config
    created_at = Column(DateTime, default=datetime.utcnow)
    workflow = relationship("Workflow", back_populates="nodes", foreign_keys=[workflow_id])
    out_edges = relationship("WorkflowEdge", foreign_keys="WorkflowEdge.from_node_id", back_populates="from_node")
    in_edges = relationship("WorkflowEdge", foreign_keys="WorkflowEdge.to_node_id", back_populates="to_node")


class WorkflowEdge(Base):
    __tablename__ = "workflow_edges"
    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    from_node_id = Column(Integer, ForeignKey("workflow_nodes.id"), nullable=False)
    to_node_id = Column(Integer, ForeignKey("workflow_nodes.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    workflow = relationship("Workflow", back_populates="edges", foreign_keys=[workflow_id])
    from_node = relationship("WorkflowNode", foreign_keys=[from_node_id], back_populates="out_edges")
    to_node = relationship("WorkflowNode", foreign_keys=[to_node_id], back_populates="in_edges")


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id"), nullable=False)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=True)  # optional link to workflow
    status = Column(String(50), nullable=False, default=TaskStatus.pending.value)
    pipeline_stage = Column(String(50), nullable=False, default=PipelineStage.l1.value)
    content = Column(JSON, nullable=False)  # e.g. {"text": "...", "media_url": "..."}
    claimed_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    claimed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    batch = relationship("Batch", back_populates="tasks")
    claimed_by = relationship("User", foreign_keys=[claimed_by_id])
    annotations = relationship("Annotation", back_populates="task")
    workflow = relationship("Workflow", foreign_keys=[workflow_id])


class Annotation(Base):
    __tablename__ = "annotations"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    response = Column(JSON, nullable=False)  # e.g. {"sentiment": "positive", "notes": "..."}
    pipeline_stage = Column(String(50), nullable=False)  # L1 or Review
    created_at = Column(DateTime, default=datetime.utcnow)
    task = relationship("Task", back_populates="annotations")
