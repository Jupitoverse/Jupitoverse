from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = ""
    role: str


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = ""
    role: str = "rater"


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class WorkspaceBase(BaseModel):
    name: str
    description: Optional[str] = ""


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceResponse(WorkspaceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = ""
    pipeline_stages: List[str] = ["L1", "Review", "Done"]
    response_schema: Optional[dict] = None


class ProjectCreate(ProjectBase):
    workspace_id: int


class ProjectResponse(ProjectBase):
    id: int
    workspace_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class BatchBase(BaseModel):
    name: str


class BatchCreate(BatchBase):
    project_id: int


class BatchResponse(BatchBase):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    content: dict


class TaskCreate(TaskBase):
    batch_id: int


class BulkTasksRequest(BaseModel):
    batch_id: int
    tasks: List[dict]


class TaskResponse(BaseModel):
    id: int
    batch_id: int
    workflow_id: Optional[int] = None
    status: str
    pipeline_stage: str
    content: dict
    claimed_by_id: Optional[int] = None
    claimed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AnnotationCreate(BaseModel):
    response: dict


class AnnotationResponse(BaseModel):
    id: int
    task_id: int
    user_id: int
    response: dict
    pipeline_stage: str
    created_at: datetime

    class Config:
        from_attributes = True


# --- Workflow ---
class WorkflowBase(BaseModel):
    name: str
    description: Optional[str] = ""


class WorkflowCreate(WorkflowBase):
    pass


class WorkflowResponse(WorkflowBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class WorkflowNodeBase(BaseModel):
    node_type: str  # form, review, api_call, db_update, manual
    name: str
    config: Optional[dict] = None


class WorkflowNodeCreate(WorkflowNodeBase):
    workflow_id: int


class WorkflowNodeResponse(WorkflowNodeBase):
    id: int
    workflow_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class WorkflowEdgeCreate(BaseModel):
    workflow_id: int
    from_node_id: int
    to_node_id: int


class WorkflowEdgeResponse(BaseModel):
    id: int
    workflow_id: int
    from_node_id: int
    to_node_id: int
    created_at: datetime

    class Config:
        from_attributes = True
