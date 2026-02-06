# Data Annotation Platform — Presentation & Stakeholder Brief

**Document purpose:** Shareable presentation covering approach, technical resources, timeline, and discovery questions to deliver the project in the best possible way with minimum effort.

---

## 1. Approach (Technical Summary)

We propose **two implementation approaches**; the same core platform supports both. Recommendation: start with **Approach A** (no LLM) to reach a working MVP faster, then add **Approach B** (LLM-assisted) only where it adds clear value.

### Approach A — No AI/LLM (Deterministic)

| Aspect | Technical detail |
|--------|------------------|
| **Architecture** | REST API (FastAPI) + PostgreSQL + optional Redis for claim locking; schema-driven task UI. |
| **Data model** | Workspace → Project → Batch → Task → Annotation hierarchy; pipeline stages (L1, Review, Done, Hold, Archive) and status state machine. |
| **Queue & assignment** | FIFO by task upload time; deterministic claim locking (DB or Redis) to prevent double-claim; manual and rule-based assignment (by rater level, project). |
| **Quality** | Programmatic linters (regex, schema validation, thresholds); benchmark tasks (gold comparison); consensus via N annotations per task with rule-based aggregation (e.g. majority vote). |
| **Integrations** | No external AI/LLM APIs; optional Okta (OAuth2) for SSO; Datadog (or equivalent) for logs/metrics. |
| **Benefit** | Lower complexity, no per-token cost, full PRD compliance, faster path to production. |

### Approach B — With LLM (Assistive Only)

| Aspect | Technical detail |
|--------|------------------|
| **Adds on top of A** | Same core platform; LLM used only for **assistive** features (suggested labels, instruction generation, optional consistency lint, benchmark gold proposals, export summaries). |
| **Integration** | OpenAI API (e.g. GPT 4.1) or Azure OpenAI; versioned prompt templates in repo; feature flags per project; fallback to non-LLM path when API unavailable. |
| **Safety** | LLM never drives critical path (claim, assignment, pipeline transitions, export); all outputs validated against schema; usage and cost logged. |
| **Benefit** | Better rater experience and Ops efficiency where assistive AI is justified; incremental rollout. |

**Why this minimizes effort:** One codebase, one data model, one deployment. Approach B is a set of optional features on top of A, not a second system.

---

## 2. Resources Needed (Technical Terms)

### 2.1 Development

| Resource | Technical specification |
|----------|-------------------------|
| **Runtime** | Python 3.11+ (FastAPI), Node.js LTS if React frontend |
| **Database** | PostgreSQL 14+ (transactional data, JSONB for flexible response schemas) |
| **Cache / lock** | Redis (optional): claim locking, rate limiting, Celery broker for async jobs |
| **Object storage** | S3 or Azure Blob: task assets, uploads, export artifacts; signed URLs for access |
| **Version control & CI/CD** | Git, GitHub; GitHub Actions for build, test, deploy |
| **Secrets** | Azure Key Vault or AWS Secrets Manager (DB URL, API keys, Okta client secret) |

### 2.2 Infrastructure (Dev / Staging / Prod)

| Resource | Technical specification |
|----------|-------------------------|
| **Compute** | Containerized API + workers (Docker); Azure App Service / Container Apps or AWS ECS/EC2 |
| **Database** | Managed PostgreSQL (Azure Database for PostgreSQL or AWS RDS); backups and HA per env |
| **Observability** | Structured JSON logging; Datadog (or Azure Monitor / App Insights): logs, metrics, alerts |
| **Auth** | Okta SSO (OAuth2) for Phase 2; JWT or session for Phase 1 |

### 2.3 Third-Party / APIs (Outbound from this application)

| System | Purpose | Direction |
|--------|---------|-----------|
| **Okta** | SSO (OAuth2) | Auth: validate tokens, user provisioning |
| **Datadog (or equivalent)** | Logs, metrics, traces | Outbound: send logs/metrics |
| **OpenAI / Azure OpenAI** (Approach B only) | Assistive features | Outbound: prompt → response; no data written back to external system |
| **Customer / internal systems** | Data in and out | See “Discovery questions” below |

### 2.4 Deliverables from this team

- REST APIs (OpenAPI/Swagger), CRUD for all core entities, queue and pipeline endpoints  
- Ops portal, Rater portal, Reviewer portal, Customer dashboard (per PRD)  
- DB migrations, runbooks, developer setup and API documentation  

---

## 3. Timeline — 5–6 Months (3–4 people)

Assumption: **3–4 people** (e.g. 1 backend, 1 frontend, 1 DevOps/QA, 1 tech lead or product/BA). Calendar time **5–6 months** to a production-ready platform (Phase 1 + Phase 2 complete, Phase 3 only if in scope).

| Phase | Duration (approx.) | Outcome |
|-------|--------------------|--------|
| **Phase 1 — MVP** | 8–10 weeks | End-to-end flow: workspace/project/batch/task CRUD, FIFO queue, claim lock, annotate → review → done; Ops/Rater/Reviewer UIs; baseline auth and logging. |
| **Phase 2 — Operational** | 8–10 weeks | Consensus, benchmarks, linters, Ops tooling (bulk upload, export, reset/archive, tagging), time tracking, full audit, Okta SSO, multi-project isolation, Customer dashboard. |
| **Phase 3 — Optional** | Per SOW | Autosave, advanced assignment, pre/post-processing, prelabels (Approach B), etc. |
| **Buffer & UAT** | 2–4 weeks | Integration, performance, security review, UAT, go-live prep. |

**Total:** ~5–6 months for Phase 1 + Phase 2 + buffer with 3–4 people. Phase 3 adds time only if included in SOW.

---

## 4. Discovery Questions — To Deliver Best Outcome with Minimum Effort

These questions clarify scope, integrations, and constraints so we can design once and avoid rework.

### 4.1 User interaction and roles

1. **What user interactions are required in each portal (Ops, Rater, Reviewer, Customer)?**  
   - *Why:* So we build the right screens and workflows once (e.g. bulk actions, filters, export options) and avoid “we also need X” later.

2. **Who creates workspaces, projects, and batches today? Is it only internal Ops, or do customers need self-serve project creation (even if limited)?**  
   - *Why:* PRD says customers do *not* create projects; confirming this keeps scope clear and effort minimal.

3. **How do raters and reviewers get access today (invite link, SSO, -Works routing)? Do we need rater impersonation for support from day one?**  
   - *Why:* Drives auth and Phase 2 vs Phase 3 scope (e.g. OPS-04 impersonation).

4. **What “task content” types must we support in the first release (text only, image, audio, video, HTML)? Any file size or format limits?**  
   - *Why:* Defines storage, signed URLs, and UI components; avoids overbuilding or missing a key type.

### 4.2 Third-party APIs and integrations

5. **Which third-party systems must READ data FROM this application?**  
   - Examples: BI/reporting tools, customer dashboards, data warehouses, internal ticketing.  
   - *Why:* We expose the right APIs (REST, webhooks, or export formats) once, with correct auth and rate limits.

6. **Which third-party systems must WRITE or UPDATE data INTO this application?**  
   - Examples: customer submitting tasks via API, HR system pushing user list, -Works sending assignments.  
   - *Why:* We design ingestion APIs, idempotency, and validation so integrations are simple and safe.

7. **Is there an existing identity provider (Okta or other) we must integrate with? Any constraints (SCIM, Just-in-Time provisioning)?**  
   - *Why:* Aligns Phase 2 auth with your IdP and avoids rework.

8. **Where should completed annotations and exports go? (Same platform only, S3/Blob path, customer API callback, webhook?) Any required format or SLA for delivery?**  
   - *Why:* Defines export and optional outbound integrations; keeps effort focused.

### 4.3 Process and quality

9. **What is the expected daily task volume and peak concurrent raters? (Order of magnitude is enough.)**  
   - *Why:* Confirms we size queue, DB, and locking (and optional Redis) correctly without over-engineering.

10. **Are there existing golden/benchmark datasets or quality rules we must support from day one?**  
    - *Why:* If yes, we build benchmark and linter support early; if no, we can keep Phase 2 quality features as designed.

11. **Who defines the “response schema” (labels, options, free-text) per project—Ops only, or also customers/templates?**  
    - *Why:* Decides whether we need a UI schema builder in Phase 2 and any customer-facing config.

### 4.4 Environment and compliance

12. **Which cloud and region are mandated (e.g. AWS us-east-1, Azure EU)? Any data residency or compliance (GDPR, PII) we must satisfy?**  
    - *Why:* Drives Azure vs AWS, Azure OpenAI vs OpenAI, and retention/audit design.

13. **Is there an existing CI/CD or deployment pipeline we must plug into? (e.g. GitHub Actions, Jenkins, ArgoCD)**  
    - *Why:* We align with your pipeline from the start and avoid duplicate tooling.

---

## 5. Why This Plan Minimizes Effort vs Alternatives

| Factor | How we minimize effort |
|--------|-------------------------|
| **Single codebase** | One platform for both approaches; LLM is optional features, not a second stack. |
| **Phased delivery** | Phase 1 proves end-to-end flow and value; Phase 2 adds production hardening; Phase 3 only if contracted. |
| **Clear boundaries** | PRD’s “Customer vs Internal” and “In scope / Out of scope” followed strictly; no scope creep without change control. |
| **Reuse and standards** | REST + OpenAPI, standard Postgres and S3/Blob patterns; no custom protocols. |
| **Discovery first** | Questions above reduce rework by aligning on integrations, users, and constraints before build. |
| **Proven stack** | Python/FastAPI, PostgreSQL, Redis, Docker; team can move fast and maintain long term. |

---

## 6. Next Steps

1. **Align on approach:** Approach A only, or A then B with a defined set of LLM features.  
2. **Answer discovery questions** (Sections 4.1–4.4) and document any “must have” integrations and SLAs.  
3. **Confirm timeline and team:** 5–6 months, 3–4 people, Phase 1 + Phase 2; Phase 3 only if in SOW.  
4. **Kick off Phase 1** with a single repo, shared backlog, and regular demos.

---

*This document can be shared as a presentation or handout. The live v3 demo (in the `v3` folder) shows the core flow: Ops dashboard, Rater queue and annotation, Reviewer queue and approval.*
