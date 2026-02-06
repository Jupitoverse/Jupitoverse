# Technology Stack

Recommended stack aligned with your skills (Python, FastAPI, Flask, Azure, Docker, LangChain) and PRD expectations. PRD mentions Node/Express/React; this proposal uses **Python backend** for faster delivery with your expertise while remaining compatible with PRD data and security requirements.

---

## 1. Backend

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Runtime** | Python 3.11+ | Your experience; rich ecosystem. |
| **API framework** | **FastAPI** (primary) or Flask | FastAPI: async, OpenAPI auto, validation. Flask if you prefer simplicity. |
| **API style** | REST; OpenAPI 3.x | PRD requires REST and OpenAPI/Swagger. |
| **Auth** | OAuth2 (Okta); JWT or session | AUTH-02; use `python-jose` or Authlib. |
| **Queue/workers** | Celery + Redis, or FastAPI background tasks | For async jobs (export, bulk assign, LLM calls). Redis for claim locking if needed. |

---

## 2. Data & Storage

| Need | Choice | Rationale |
|------|--------|-----------|
| **Transactional data** | **PostgreSQL** | Workspace, Project, Batch, Task, Annotation, users, audit. PRD expects Postgres. |
| **Schema-flexible / documents** | **PostgreSQL (JSONB)** or MongoDB | PRD allows MongoDB; JSONB in Postgres can cover response schemas and flexible payloads. |
| **File/media storage** | **Azure Blob** or S3 | PRD references S3; Azure Blob is equivalent; signed URLs for asset access (INT-02). |
| **Cache / lock** | **Redis** (optional) | Claim locking, rate limiting, session cache. |
| **ORM / DB access** | SQLAlchemy 2.x, or Django ORM if using Django | Migrations, CRUD, connection pooling. |

---

## 3. Frontend

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Stack** | **HTML + CSS + JavaScript** (vanilla or Alpine.js) **or** React + TypeScript | Your HTML/CSS/JS skills; React if you want component reuse and PRD-style React/TS. |
| **Styling** | Tailwind CSS or plain CSS | PRD mentions Tailwind; quick UI. |
| **Build** | Vite (if React) or minimal (if vanilla) | Fast dev and bundle. |
| **Auth in UI** | Same OAuth2 flow; store token/session | Redirect to Okta; callback to app. |

---

## 4. Infrastructure & DevOps

| Area | Choice | Rationale |
|------|--------|-----------|
| **Cloud** | **Azure** (primary) or AWS | Your Azure experience; PRD assumes AWS — same concepts (compute, blob, DB). |
| **Containers** | **Docker** | App and workers; consistent env. |
| **CI/CD** | **GitHub Actions** | PRD expects GitHub Actions; build, test, deploy. |
| **Secrets** | Azure Key Vault or env vars in CI | API keys, DB URLs, Okta client secret. |
| **Logging / observability** | Structured logs (JSON); optional Datadog/App Insights | PRD references Datadog; Azure Application Insights is an alternative. |

---

## 5. Approach B — LLM

| Need | Choice | Rationale |
|------|--------|-----------|
| **Provider** | **OpenAI API** (e.g., GPT 4.1) or **Azure OpenAI** | Same models; Azure for compliance/data residency if required. |
| **SDK** | `openai` Python package | Official; simple REST wrapper. |
| **Orchestration (optional)** | **LangChain** / **LangGraph** | Your experience; use for multi-step or complex flows; not required for single-call features. |
| **Prompt storage** | Versioned files in repo (`Planning/Prompts/`) | Audit, diff, rollback. |

---

## 6. Summary Table

| Category | Approach A | Approach B (additions) |
|----------|------------|-------------------------|
| Backend | Python, FastAPI, Postgres, Redis (optional), Azure Blob | + OpenAI SDK or LangChain |
| Frontend | HTML/CSS/JS or React/TS, Tailwind | Same |
| Auth | Okta OAuth2, JWT/session | Same |
| Infra | Docker, Azure (or AWS), GitHub Actions | Same |
| LLM | — | OpenAI or Azure OpenAI, Prompts in repo |

---

## 7. PRD Stack Note

PRD specifies Node.js/Express and React/TypeScript. This stack uses **Python/FastAPI** and optional React to leverage your skills and Cursor; functional and security requirements (REST, OpenAPI, Okta, RBAC, S3-style storage, audit) remain unchanged. If contractually required to use Node/React, the same planning and phase breakdown apply; only implementation language and framework change.
