# Approach A: Solution Without AI/LLM

Complete approach for the Data Annotation Platform **without any AI or LLM calls**. All behavior is deterministic and rule-based.

---

## 1. Summary

- **Scope:** Same as PRD — Workspace → Project → Batch → Task → Annotation, multi-stage pipelines, FIFO queueing, Ops/Rater/Reviewer/Customer portals.
- **Quality & automation:** Linters (programmatic rules), benchmarks (gold comparison), consensus (N annotations per task). No external AI APIs.
- **Implementable with:** Python (FastAPI/Flask), your existing skills, and Cursor. No OpenAI or other LLM subscription required for core platform.

---

## 2. Core Components (No-LLM)

### 2.1 Data Model & APIs

- **Hierarchy:** Workspace → Project → Batch → Task → Annotation (per PRD DATA-01, DATA-02).
- **CRUD:** REST APIs for all core objects; OpenAPI/Swagger docs.
- **Response schemas:** Flexible, versioned; different UI per pipeline level (annotator vs reviewer) — schema-driven only, no LLM.

### 2.2 Pipeline & Status

- **Pipeline:** Configurable stages (e.g., L1 → L2 → Review → Hold → Archive) per project/batch.
- **Statuses:** pending, assigned, claimed, pending-review, done, hold, completed, delivered, archive.
- **Ops controls:** Advance, hold, archive/ignore (manual); no AI-driven transitions.

### 2.3 Queueing & Assignment

- **FIFO:** By task upload time; deterministic claim locking (no double-claim) — QUEUE-01.
- **Assignment:** Manual and automatic (rules: e.g., by rater level, project assignment) — QUEUE-02, QUEUE-03, QUEUE-04.
- **Reclaim/timeout:** Configurable rules; no ML-based assignment.

### 2.4 Task UI (MVP + Phase 2)

- **Media:** Text, image, audio, video, HTML/markdown rendering.
- **Response components:** Single-select, multi-select, free-text, etc.; schema-driven.
- **Level-specific UI:** Reviewer vs L1 UI from schema/config only.

### 2.5 Quality (No-LLM)

- **Linters (QUAL-01):** Programmatic checks (regex, format, required fields, value ranges). Blocking vs warning; results stored per annotation.
- **Benchmarks:** Pre-labeled golden tasks; compare rater output to gold; gate or interleaved serving.
- **Consensus (PIPE-04):** N annotations per task; aggregate by rule (e.g., majority vote), not by LLM.
- **Time tracking (QUAL-03):** Active time per task for payout; no AI.

### 2.6 Ops Tooling

- **Upload (OPS-01):** Bulk task upload with validation and progress.
- **Export (OPS-02):** CSV/JSON + assets/signed URLs.
- **Reset/archive/ignore (OPS-03), tagging (OPS-06), impersonation (OPS-04):** All rule-based and manual.

### 2.7 Auth & Portals

- **Auth:** Login, profile; internal vs external separation (AUTH-01, AUTH-03). Okta SSO in Phase 2 (AUTH-02).
- **Portals:** Ops Portal, Rater Portal, Reviewer Portal, Customer Dashboard (subscription, seats, API key view) — no AI in any portal.

---

## 3. What Is Explicitly Out of Scope (Approach A)

- No LLM calls (OpenAI or otherwise).
- No prelabels/predictions from a model (PROC-02 — Phase 3); if needed, prelabels are uploaded as data.
- No AI-driven pre/post-processing; only scripted transforms (e.g., Lambda) if Phase 3.
- No “suggested labels” or “smart” conflict resolution in UI.

---

## 4. Implementation Readiness

- **Cursor:** All logic can be implemented and refactored in Cursor (backend, APIs, frontend, DB, config).
- **Stack:** Python (FastAPI recommended), PostgreSQL, MongoDB or Postgres-only per choice, S3-compatible storage (e.g., Azure Blob), Docker. Frontend: HTML/CSS/JS or React if preferred.
- **Dependencies:** No OpenAI SDK or LangChain required for Approach A; only standard web stack + DB + storage.

---

## 5. Best Solution Within No-LLM

- **Clear schema-driven UI:** One source of truth (response schema) drives task UI and validation; easy to extend with new field types without codegen.
- **Modular linter framework:** Pluggable linter modules (e.g., format, length, allowed values); Ops selects which linters apply and blocking vs warning.
- **Deterministic queue:** FIFO + claim lock with a single source of truth (DB or Redis) to avoid race conditions.
- **Audit everything:** Log claims, submissions, status changes, Ops actions — required for PRD and operations.
- **Phase 1 first:** Get end-to-end flow (create project → upload → assign → annotate → review → export) working, then add Phase 2 (consensus, benchmarks, export, linters, time tracking).

This gives a production-ready, PRD-compliant platform with no AI/LLM dependency, fully implementable with Cursor.
