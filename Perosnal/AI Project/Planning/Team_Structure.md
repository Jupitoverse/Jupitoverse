# Team Structure & Roles

Proposed roles and responsibilities for building and operating the Data Annotation Platform. Can be scaled from solo (e.g., you + Cursor) to a small team.

---

## 1. Approach A (No-LLM) — Minimal Team

| Role | Responsibility | Can be same person? |
|------|----------------|---------------------|
| **Product / Requirements** | PRD alignment, prioritization, acceptance criteria | Yes (solo) |
| **Backend / API** | FastAPI/Flask, data model, queueing, pipeline, auth, storage (Postgres, S3/Blob) | Yes |
| **Frontend** | Ops Portal, Rater Portal, Reviewer Portal, Customer Dashboard (HTML/CSS/JS or React) | Yes |
| **DevOps / Infra** | Docker, Azure (or AWS), CI/CD, env config, secrets | Yes (part-time) |
| **QA** | Manual flows, test cases, regression; optional automation (pytest, Playwright) | Yes (you or part-time) |

**Solo with Cursor:** One person can cover all roles; Cursor assists with backend, frontend, tests, and config. Use the Implementation_Plan phases to slice work into small deliverables.

---

## 2. Approach B (With-LLM) — Additional Focus

Same as above, plus:

| Role | Responsibility | Notes |
|------|----------------|-------|
| **LLM / Prompt engineering** | Prompt design, versioning, safety, fallbacks; token/cost awareness | Can be same as Backend; prompts in repo (Prompts/) |
| **Integration** | OpenAI/Azure OpenAI client, retries, rate limits, logging | Backend owner typically |

No separate “AI team” required; one developer can own LLM integration and prompt library with Cursor support.

---

## 3. Optional Scaling (Larger Team)

If you add people later:

- **Backend developer:** APIs, queue, pipeline, DB, linters.
- **Frontend developer:** All portals and task UI.
- **DevOps:** Azure/AWS, Docker, CI/CD, monitoring.
- **QA:** Test automation and UAT.

For Phase 3 (optional features), add only if SOW includes preprocessing, custom graders, or heavy LLM usage.

---

## 4. Responsibilities Matrix (PRD-Aligned)

| PRD Area | Owner (minimal) | Deliverable |
|----------|------------------|-------------|
| Data model & CRUD APIs | Backend | DATA-01, DATA-02, DATA-03 |
| Pipeline & status | Backend | PIPE-01, PIPE-02, PIPE-03, PIPE-04, PIPE-05 |
| Queue & assignment | Backend | QUEUE-01–05 |
| Task UI | Frontend | UI-01–06 |
| Ops tools | Frontend + Backend | OPS-01–07 |
| Rater/Reviewer portals | Frontend | RATER-01, RATER-02 |
| Auth & RBAC | Backend | AUTH-01, AUTH-02, AUTH-03 |
| Quality (linters, benchmarks, time) | Backend | QUAL-01, QUAL-02, QUAL-03 |
| Customer portal | Frontend + Backend | CUST-01, CUST-02, CUST-03 |
| Logging & audit | Backend | LOG-01 |
| LLM features (Approach B) | Backend + Prompts | Per Approach_B_With_LLM |

---

## 5. Cursor-Centric Workflow

- **You:** Product decisions, architecture choices, code review, deployment, testing.
- **Cursor:** Implementation from specs (APIs, UI, DB migrations, prompts), refactors, test drafts, docs.
- **Artifacts:** Planning docs in this folder; prompts in `Prompts/`; code in repo with clear module boundaries so Cursor can work file-by-file.

This structure supports presenting both approaches and scaling when needed.
