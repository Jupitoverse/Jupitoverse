# Data Annotation Platform — v3 Demo

End-to-end demo of the annotation platform with **dark theme** (n8n/Netflix style), **FastAPI** backend, and **PostgreSQL**. Use it to show how the platform looks and behaves.

## Quick start

### Option A — Run locally without Docker (SQLite)

No Docker or PostgreSQL needed. The app uses **SQLite** by default (file: `backend/annotation.db`).

From the **v3** folder:

**Windows (PowerShell):**
```powershell
cd backend
pip install -r requirements.txt
$env:PYTHONPATH = "."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Linux/macOS:**
```bash
cd backend
pip install -r requirements.txt
PYTHONPATH=. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Then open [http://localhost:8000](http://localhost:8000).

### Option B — Run with Docker (PostgreSQL)

From the **v3** folder run `docker-compose up -d`, then create `backend/.env` with:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/annotation_platform
```
Then run the backend as in Option A (same `cd backend` and `uvicorn` commands).

### Open the app

- **App (login + UI):** [http://localhost:8000](http://localhost:8000)
- **API docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

### Demo logins

| Email            | Password  | Role     | Use case |
|------------------|-----------|----------|----------|
| **abhi@demo.com** | **admin123** | **Admin** | Full access: Dashboard, My Queue, Review Queue |
| ops@demo.com     | demo      | Ops      | Dashboard: workspaces, projects, batches, tasks |
| rater@demo.com   | demo      | Rater    | My Queue: get next task, annotate, submit |
| reviewer@demo.com| demo      | Reviewer | Review Queue: review tasks, approve or edit |

*If you already have an existing database (e.g. `annotation.db`), delete it and restart the app to seed the admin user.*

## What’s in this demo

- **Workspace → Project → Batch → Task** hierarchy (seed data included).
- **Ops:** View workspaces, projects, batches, and task counts by status.
- **Rater:** Claim next task (FIFO), annotate (sentiment + notes), submit for review.
- **Reviewer:** See tasks in review, view rater’s annotation, approve or submit with edits.
- **Dark theme:** n8n/Netflix-style (dark gray, green accent).
- **Tech:** FastAPI, PostgreSQL, SQLAlchemy, vanilla JS frontend.

## Project layout

```
v3/
├── backend/
│   ├── app/
│   │   ├── main.py       # FastAPI app, seed, static mount
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── auth.py
│   │   └── routers/       # auth, workspaces, projects, batches, tasks, queue
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── docker-compose.yml
└── README.md
```

## Optional: custom DB URL

Create `backend/.env`:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/annotation_platform
```

Default is the same; change if your Postgres user/password/port differ.

## Flow to demo

1. Log in as **rater@demo.com** → My Queue → **Get next task** → fill sentiment + notes → **Submit for review**.
2. Log in as **reviewer@demo.com** → Review Queue → open task → see rater’s answer → **Approve** or **Submit with edits**.
3. Log in as **ops@demo.com** → Dashboard → see workspaces, projects, batches, task status counts.

This is a **concept demo** for showing the idea; it is not production-hardened (e.g. no Okta, no full RBAC, no export).
