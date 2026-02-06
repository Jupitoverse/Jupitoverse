# Gamma.app Prompt: Data Annotation Platform Phase 1 Deck

**Copy the text below into Gamma (gamma.app) when creating a new AI presentation. Paste the entire block into the prompt field so Gamma generates a matching deck.**

---

```
Create a professional, stakeholder-facing presentation with this exact structure and content.

**Title:** Data Annotation Platform — Phase 1: Architecture, Data Model & Delivery Confidence

**Audience:** Technical and business stakeholders. Tone: clear, confident, proposal-style.

**Slides to create (12 slides):**

1. **Title slide**
   - Title: "Data Annotation Platform"
   - Subtitle: "Phase 1 — Architecture, Data Model & Delivery Confidence"
   - One line: "Technical proposal for stakeholder alignment"

2. **Phase 1 — What We Deliver (8–10 weeks)**
   - Bullet list:
     - End-to-end flow: Workspace → Project → Batch → Task → Annotation
     - REST APIs (OpenAPI): CRUD for all entities, queue, pipeline controls
     - FIFO queue with deterministic claim locking (no double-claim)
     - Multi-stage pipeline: L1 → Review → Done (configurable)
     - Three portals: Ops (dashboard, controls), Rater (queue, annotate), Reviewer (review, approve)
     - Auth & RBAC: Login, roles (Ops, Rater, Reviewer, Admin), internal vs external separation
     - Task UI: Schema-driven; text, image, audio, video; single/multi-select, free-text
     - Storage: PostgreSQL (transactional), S3/Azure Blob (assets), signed URLs
     - Baseline logging: claims, submissions, status transitions (structured JSON)

3. **High-Level Architecture**
   - Client: Browser — Ops Portal, Rater Portal, Reviewer Portal (HTTPS)
   - API layer: FastAPI — REST, OpenAPI, JWT auth, RBAC. Routes: /auth, /workspaces, /projects, /batches, /tasks, /queue
   - Data layer: PostgreSQL (users, workspaces, projects, batches, tasks, annotations, pipeline state); S3/Azure Blob (task assets, signed URLs); Redis (optional) for claim locking, cache, Celery
   - Deployment: Containerized API (Docker); cloud compute (Azure/AWS); secrets from vault

4. **Data Model — Core Entities**
   - Workspace (1) ───< (N) Project — Top-level isolation; name, description
   - Project (1) ───< (N) Batch — pipeline_stages[], response_schema (JSON)
   - Batch (1) ───< (N) Task — FIFO order by created_at
   - Task (1) ───< (N) Annotation — status, pipeline_stage, content (JSON), claimed_by_id
   - User (1) ───< (N) Task (claimed), (N) Annotation — email, role, hashed_password
   - Key design: Response schema is JSON (flexible); UI derived from schema. Pipeline stages configurable per project (e.g. L1, Review, Hold, Done).

5. **Pipeline & Status Flow**
   - Task statuses: pending → claimed → in_review → done (or hold, archived)
   - Pipeline stages (e.g.): L1 → Review → Done. Ops can advance, hold, or archive.
   - Flow: Rater claims task (FIFO) → submits annotation → task moves to Review. Reviewer opens task → approves or edits → task moves to Done.
   - Claim locking: Single source of truth (DB or Redis); no task claimed by two raters. All state transitions logged for audit.

6. **Workflow & Data Visibility (PRD-Aligned)**
   - Workflows: Configurable graphs of nodes (form, review, API, DB, manual) and edges; unique node ID and instance ID per run.
   - Annotation flow: Upload file → form node (add attributes) → submit → review node → task enters work queue.
   - Work queue: Manual/review nodes assign tasks to queues; users see only tasks in their queue (by role or hierarchy).
   - Task tab: One view with filters and sorting (status, workflow, date, assignee); data scoped by visibility.
   - Data visibility: Admin sees all; other users see only tasks assigned to them or in their queue.
   - Child workflows: A node can start a sub-workflow; completion is sequential (child completes then parent continues).

7. **Infrastructure (Phase 1)**
   - Compute: API containerized (Docker); Azure App Service / Container Apps or AWS ECS; optional Celery + Redis for async
   - Database: PostgreSQL 14+ (managed); JSONB for flexible fields
   - Storage: S3 or Azure Blob — task assets, uploads, exports; signed URLs; no public bucket
   - Secrets: Azure Key Vault / AWS Secrets Manager (DB URL, API keys, JWT secret)
   - Environments: Dev, Staging, Prod with isolated DB and storage per env

8. **Deployment & CI/CD**
   - Version control: Git, GitHub; branch strategy (main + feature branches)
   - CI: GitHub Actions — on push/PR: build, run tests, lint
   - Build: Docker image for API; multi-stage build for smaller image
   - Deploy: Push image to registry (ACR/ECR); deploy with rolling update
   - Database: Migrations (e.g. Alembic) run as part of release; backward-compatible
   - Secrets: Injected via environment or cloud secret store; never in image or repo
   - Rollback: Previous image tag; migrations forward/backward compatible where possible

9. **Monitoring, Logging & Insights**
   - Logging: Structured JSON logs (request id, user, action, duration, status); stdout → aggregator
   - Events logged: login, task claim, submit, status change, Ops actions; no PII in logs
   - Metrics: API latency (p50/p95), error rate, queue depth, tasks per status (Prometheus or cloud native)
   - Dashboards: Operational view (tasks by status, throughput, errors); Datadog / Azure Monitor / CloudWatch
   - Alerts: Error rate spike, latency SLO breach, queue backlog; PagerDuty/email/Slack
   - Audit: Key actions (who, what, when) stored and searchable; retention per policy (e.g. 90 days)

10. **Security & Compliance (Phase 1)**
    - Authentication: Login + JWT for API; optional Okta SSO in Phase 2
    - Authorization: RBAC — Ops, Rater, Reviewer, Admin; internal vs external; server-side enforcement
    - Data in transit: HTTPS only; TLS 1.2+
    - Data at rest: DB and blob encrypted (cloud default or customer-managed keys)
    - Secrets: In vault; rotated per policy; not in code or repo
    - Audit: Sensitive actions logged; logs retained for compliance

11. **Why We Can Deliver — Confidence**
    - Proven stack: Python/FastAPI, PostgreSQL, Redis, S3/Blob — widely used and maintainable
    - Clear scope: Phase 1 bounded by PRD; we deliver MVP flow and foundations first
    - Working demo: V3 demo shows end-to-end flow (Ops, Rater, Reviewer); we extend and harden it
    - Single codebase: One platform for all personas; no fragmented systems
    - Phased delivery: Working software in 8–10 weeks; we iterate with your feedback
    - Discovery first: Align on users, load, and integrations before build to avoid rework
    - Workflow & visibility: Graph-based workflows and Admin vs user-wise data designed per PRD (see Developer Guide).

12. **Next Steps**
    - 1. Align on Phase 1 scope and timeline (8–10 weeks, 3–4 people)
    - 2. Confirm infrastructure: cloud, region, and any existing CI/CD we plug into
    - 3. Answer discovery questions (users, load, integrations, data constraints)
    - 4. Kick off: repo, backlog, first sprint; regular demos to stakeholders

Use a clean, professional theme (e.g. dark header with green/teal accent). Keep each slide readable with clear headings and bullet points; avoid crowding.
```

---

**How to use:** In Gamma, start a new presentation with “Generate with AI” and paste the entire content between the triple backticks (including the slide titles and bullet points). Adjust theme or visuals in Gamma after generation if needed.
