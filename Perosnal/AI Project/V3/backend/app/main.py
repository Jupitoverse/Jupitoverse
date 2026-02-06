from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .database import engine, Base, SessionLocal
from .models import User, Workspace, Project, Batch, Task, Workflow, WorkflowNode, WorkflowEdge
from .auth import get_password_hash
from .routers import auth_router, workspaces_router, projects_router, batches_router, tasks_router, queue_router, workflows_router


def seed_db():
    db = SessionLocal()
    try:
        # Always ensure admin abhi@demo.com exists and password is admin123 (fixes existing DBs)
        admin = db.query(User).filter(User.email == "abhi@demo.com").first()
        if not admin:
            admin = User(
                email="abhi@demo.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Abhi",
                role="admin",
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
        else:
            admin.hashed_password = get_password_hash("admin123")
            admin.role = "admin"
            admin.full_name = "Abhi"
            db.commit()

        # Seed demo workflow if none exist (for new DB or after adding workflow tables)
        if db.query(Workflow).count() == 0:
            w = Workflow(name="Annotation pipeline", description="Upload → Form → Review → Done")
            db.add(w)
            db.commit()
            db.refresh(w)
            n1 = WorkflowNode(workflow_id=w.id, node_type="form", name="Add attributes")
            n2 = WorkflowNode(workflow_id=w.id, node_type="review", name="Review")
            db.add_all([n1, n2])
            db.commit()
            db.refresh(n1)
            db.refresh(n2)
            e = WorkflowEdge(workflow_id=w.id, from_node_id=n1.id, to_node_id=n2.id)
            db.add(e)
            db.commit()

        if db.query(User).count() > 1:
            # Already have users (e.g. ops, rater, reviewer) — only admin was ensured above
            return
        users = [
            User(email="ops@demo.com", hashed_password=get_password_hash("demo"), full_name="Ops User", role="ops"),
            User(email="rater@demo.com", hashed_password=get_password_hash("demo"), full_name="Rater One", role="rater"),
            User(email="reviewer@demo.com", hashed_password=get_password_hash("demo"), full_name="Reviewer One", role="reviewer"),
        ]
        for u in users:
            db.add(u)
        db.commit()
        ws = Workspace(name="Demo Workspace", description="Demo for annotation platform")
        db.add(ws)
        db.commit()
        db.refresh(ws)
        proj = Project(
            workspace_id=ws.id,
            name="Sentiment Labeling",
            description="Label sentiment of customer messages",
            pipeline_stages=["L1", "Review", "Done"],
            response_schema={"sentiment": "single_select", "notes": "free_text"},
        )
        db.add(proj)
        db.commit()
        db.refresh(proj)
        batch = Batch(project_id=proj.id, name="Batch 1")
        db.add(batch)
        db.commit()
        db.refresh(batch)
        for i in range(1, 6):
            t = Task(
                batch_id=batch.id,
                content={"text": f"Sample message {i}: The product arrived on time and quality was great."},
            )
            db.add(t)
        db.commit()
    finally:
        db.close()


def ensure_workflow_id_column():
    """Add workflow_id to tasks table if missing (for existing DBs)."""
    from sqlalchemy import text
    with engine.connect() as conn:
        if "sqlite" in str(engine.url):
            r = conn.execute(text("PRAGMA table_info(tasks)"))
            cols = [row[1] for row in r]
            if "workflow_id" not in cols:
                conn.execute(text("ALTER TABLE tasks ADD COLUMN workflow_id INTEGER"))
                conn.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    ensure_workflow_id_column()
    seed_db()
    yield


app = FastAPI(title="Data Annotation Platform", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(workspaces_router.router)
app.include_router(projects_router.router)
app.include_router(batches_router.router)
app.include_router(tasks_router.router)
app.include_router(workflows_router.router)
app.include_router(queue_router.router)

# frontend is sibling of backend (v3/frontend, v3/backend)
frontend_path = Path(__file__).resolve().parent.parent.parent / "frontend"


@app.get("/")
def serve_app():
    index = frontend_path / "index.html"
    if index.exists():
        return FileResponse(str(index))
    return {"message": "Data Annotation Platform API", "docs": "/docs"}


if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=str(frontend_path / "static")), name="static")
