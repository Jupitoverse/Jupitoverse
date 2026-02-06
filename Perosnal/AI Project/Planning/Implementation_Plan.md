# Implementation Plan

Phased delivery plan aligned with PRD Phase 1 (MVP), Phase 2 (Operational), and Phase 3 (Optional). Applicable to both Approach A and Approach B; Approach B adds LLM features as optional layers.

---

## Phase 1 — MVP (4–6 weeks target)

**Goal:** End-to-end internal labeling platform: create workspace/project/batch → upload tasks → assign → annotate → review → basic export. No LLM in Phase 1 for either approach.

### 1.1 Core Data & API

| # | Deliverable | Requirements | Notes |
|---|-------------|--------------|-------|
| 1.1 | Workspace, Project, Batch, Task, Annotation models + CRUD APIs | DATA-01, DATA-02 | Postgres; OpenAPI docs |
| 1.2 | Response schema support (versioned, per project/batch) | DATA-03 | JSONB or Mongo; UI schema derived from this |
| 1.3 | Pipeline model (stages: L1, L2, Review, Hold, Archive) + status enum | PIPE-01, PIPE-02 | Configurable per project |
| 1.4 | Ops controls API: advance, hold, archive | PIPE-03 | Authorized Ops only |

### 1.2 Queue & Assignment

| # | Deliverable | Requirements | Notes |
|---|-------------|--------------|-------|
| 1.5 | FIFO queue (by upload time); claim with deterministic locking | QUEUE-01 | DB or Redis lock; no double-claim |
| 1.6 | Manual and automatic assignment APIs | QUEUE-02 | Assign task(s) to rater(s) |

### 1.3 Auth & Access

| # | Deliverable | Requirements | Notes |
|---|-------------|--------------|-------|
| 1.7 | Login, profile, internal vs external separation | AUTH-01, AUTH-03 | Roles: Ops, Rater, Reviewer, Admin |
| 1.8 | (Phase 2 in PRD; can defer) Okta SSO | AUTH-02 | Or simple auth first, Okta in Phase 2 |

### 1.4 Task UI & Portals

| # | Deliverable | Requirements | Notes |
|---|-------------|--------------|-------|
| 1.9 | Task UI: media (text, image, audio, video, HTML/markdown) | UI-01 | Signed URLs for assets |
| 1.10 | Response components: single/multi-select, free-text | UI-02 | Schema-driven |
| 1.11 | Dynamic UI per task; different UI per pipeline level (review vs L1) | UI-03, UI-04 | |
| 1.12 | Rater portal: queue, claim, submit, status | RATER-01 | |
| 1.13 | Reviewer portal: review queue, approve/edit, submit | — | Implied by pipeline |
| 1.14 | Ops portal (minimal): project/batch/task list, pipeline controls | — | Full Ops tooling in Phase 2 |

### 1.5 Storage & Observability

| # | Deliverable | Requirements | Notes |
|---|-------------|--------------|-------|
| 1.15 | Blob storage (Azure Blob or S3) for uploads; signed URLs | INT-02 | |
| 1.16 | Baseline logging (claims, submissions, status changes) | — | Structured logs |

### Phase 1 Definition of Done

- [ ] End-to-end flow in staging: create project → upload batch → assign → rater annotates → reviewer reviews → status advances.
- [ ] No double-claim; FIFO ordering and claim lock verified.
- [ ] OpenAPI published; developer setup doc.
- [ ] All Phase 1 P0 requirements from PRD covered.

---

## Phase 2 — Operational Expansion (4–6 weeks after Phase 1)

**Goal:** Production-ready operations: consensus, benchmarks, Ops tooling (upload/export/reset/tagging), linters, time tracking, audit, multi-project isolation.

### 2.1 Quality & Pipeline

| # | Deliverable | Requirements | Notes |
|---|-------------|--------------|-------|
| 2.1 | Consensus: N annotations per task; aggregation | PIPE-04 | |
| 2.2 | Benchmarks: gate or interleaved; golden tasks | PIPE-05 | |
| 2.3 | Linter framework: configurable, blocking/warning, store results | QUAL-01 | Programmatic rules (Approach A); optional LLM lint (Approach B) |
| 2.4 | Time tracking (active time per task) | QUAL-03 | |

### 2.2 Ops Tooling

| # | Deliverable | Requirements | Notes |
|---|-------------|--------------|-------|
| 2.5 | Task/batch upload UI with validation and progress | OPS-01 | |
| 2.6 | Batch export: CSV/JSON + assets/signed URLs | OPS-02 | |
| 2.7 | Reset / archive / ignore controls | OPS-03 | |
| 2.8 | Rater/Reviewer impersonation (Product Admin) | OPS-04 | Audit logged |
| 2.9 | Tag management: bulk add/remove for tasks and raters | OPS-06 | |
| 2.10 | Ops UI builder (GUI for response schema) | UI-05 | |

### 2.3 Assignment & Rater

| # | Deliverable | Requirements | Notes |
|---|-------------|--------------|-------|
| 2.11 | Mass assignment by rater level; project-level assignment | QUEUE-03, QUEUE-04 | |
| 2.12 | Rater levels/qualifications management | RATER-02 | |

### 2.4 Customer & Auth

| # | Deliverable | Requirements | Notes |
|---|-------------|--------------|-------|
| 2.13 | Customer dashboard: subscription, seats, API key view | CUST-01 | |
| 2.14 | Okta SSO (OAuth2) | AUTH-02 | |
| 2.15 | Logging & audit: searchable, retention; key events | LOG-01 | |
| 2.16 | Multi-project/batch concurrency; isolation | INT-03 | |

### Phase 2 Definition of Done

- [ ] All P1 requirements demonstrated in staging.
- [ ] Consensus, benchmarks, linters, export, impersonation, tags, time tracking working.
- [ ] Documentation updated; tests and performance checks pass.

---

## Phase 3 — Optional (SOW-Dependent)

Only items contracted in SOW. Examples:

| # | Deliverable | Requirements | Notes |
|---|-------------|--------------|-------|
| 3.1 | Drafts/autosave | UI-06 | |
| 3.2 | Advanced assignment (random, LIFO, weighted) | QUEUE-05 | |
| 3.3 | Ops dashboard (counts, drill-down) | OPS-05 | |
| 3.4 | Advanced task filtering | OPS-07 | |
| 3.5 | Pre/post-processing hooks (e.g., Lambda/n8n) | PROC-01 | |
| 3.6 | Prelabels/predictions (Approach B: LLM prelabels) | PROC-02 | |
| 3.7 | Instruction page in task UI; notification center | MISC-03, MISC-04 | |
| 3.8 | Customer upload/download datasets | CUST-03 | |
| 3.9 | Customer usage/annotation volume metrics | CUST-02 | |

---

## Approach B — Where LLM Fits In

- **Phase 1:** No LLM; same as Approach A.
- **Phase 2:** Optional: LLM-assisted linter (consistency check), or post-Phase 2.
- **Phase 3 (or earlier):** Suggested labels in task UI, instruction generation, benchmark gold creation, export summaries, prelabels. Add one feature at a time; use `Planning/Prompts/` and feature flags.

---

## Cursor-Friendly Slicing

- Each deliverable above can be implemented as a focused set of files (e.g., “queue service”, “task UI components”, “export job”). Describe the slice in a short spec or ticket and implement with Cursor.
- Keep backend (FastAPI), frontend (HTML/JS or React), and prompts (Approach B) in separate modules so Cursor can work on one area at a time.
- Run tests and API checks after each slice to avoid regressions.

This plan supports presenting both approaches and executing implementation using Cursor and the chosen tech stack.
