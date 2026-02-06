# Implementation Strategy

How to build the Data Annotation Platform so it is **presentable** (two approaches) and **implementable with Cursor** and your stack (Python, FastAPI, Azure, Docker, etc.). No code in this doc — strategy only.

---

## 1. Principles

1. **Build Approach A first.** Get the full platform (data model, pipeline, queue, Ops/Rater/Reviewer/Customer portals) working without any LLM. Then add LLM features as optional toggles (Approach B).
2. **One phase at a time.** Phase 1 → demo and stabilize → Phase 2 → then Phase 3 only if in SOW.
3. **Cursor as primary implementation tool.** Use Planning docs and this strategy as context; implement in small, testable slices so Cursor can generate and refactor code file-by-file.
4. **Single codebase, two modes.** Same repo supports both approaches; LLM features are behind config (e.g., `enable_llm_suggestions`). No separate “Approach B repo.”

---

## 2. Repository & Module Layout (Recommended)

When you start implementation, a structure like this keeps planning and code clear:

```
AI Project/
├── Data_Annotation_Platform_PRD_Addendum_v2.0 - Copy.pdf
├── Planning/                    # This folder — no code
│   ├── README.md
│   ├── Approach_*.md, Team_Structure.md, ...
│   └── Prompts/
├── backend/                     # FastAPI (or Flask) app
│   ├── app/
│   │   ├── api/
│   │   ├── core/                # config, auth, db
│   │   ├── models/
│   │   ├── services/            # queue, pipeline, export, llm (if B)
│   │   └── schemas/
│   ├── tests/
│   └── requirements.txt
├── frontend/                    # Ops / Rater / Reviewer / Customer UIs
│   └── ...
├── docker-compose.yml          # app, postgres, redis (optional)
└── README.md                   # How to run, env vars, links to Planning
```

- **Planning/** stays documentation-only. **Prompts/** under Planning holds versioned prompt templates for Approach B.
- Backend and frontend are separate so Cursor can work on one layer at a time with clear context.

---

## 3. Cursor-Only Workflow

1. **Start from Planning.** Open `Planning/README.md`, `Approach_A_No_LLM.md`, `Implementation_Plan.md`, and `Tech_Stack.md` so Cursor has full context.
2. **Slice work.** Pick one deliverable (e.g., “FIFO queue + claim lock”). Describe in a short prompt: “Implement FIFO queue by upload time and claim locking so a task cannot be claimed by two raters; use Postgres (or Redis).”
3. **Implement in order.** Follow Phase 1 order: data model + CRUD → pipeline → queue → auth → task UI → rater/reviewer portals → Ops minimal → storage + logging. Run and test after each slice.
4. **Tests.** Ask Cursor to add pytest tests for API endpoints and critical logic (claim lock, status transitions). Run in CI (e.g., GitHub Actions).
5. **Approach B later.** After Phase 1 (or Phase 2) is stable, add one LLM feature at a time. For each, add a prompt under `Planning/Prompts/`, a small service in `backend/app/services/llm/`, and a feature flag. Always keep a non-LLM fallback.

---

## 4. Presentation Strategy

- **Deck 1 — Problem & PRD:** Short recap of PRD (hierarchy, pipelines, queueing, personas, phases). Reference `Data_Annotation_Platform_PRD_Addendum_v2.0 - Copy.pdf` and `Planning/Approach_Comparison.md`.
- **Deck 2 — Approach A:** “Solution without AI/LLM.” Walk through `Approach_A_No_LLM.md`, `Tech_Stack.md`, and Phase 1–2 from `Implementation_Plan.md`. Emphasize: rule-based quality, no external API cost, full PRD compliance, implementable with Cursor.
- **Deck 3 — Approach B:** “Solution with LLM (e.g., GPT 4.1).” Walk through `Approach_B_With_LLM.md`, where LLM is used (table), design principles (fallback, configurable, audit). Show same core platform + optional assistive AI; reference `Prompts/` for prompt strategy.
- **Deck 4 — Plan & resources:** Timeline (Phase 1 → 2 → 3), team structure (`Team_Structure.md`), resources (`Resources_Needed.md`), subscriptions (`Subscriptions_Needed.md`), and implementation strategy (this doc).

Use `Presentation_Outline.md` for slide-by-slide outline.

---

## 5. Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Scope creep | Stick to PRD phases; Phase 3 only if in SOW. |
| Claim/concurrency bugs | Single source of truth for “claimed by”; tests that simulate concurrent claims. |
| LLM cost/capacity (Approach B) | Feature flags, per-project caps, usage logging, fallback to no-LLM. |
| PRD expects Node/React | This strategy uses Python/FastAPI; if contract requires Node/React, reuse same planning and phases, swap stack (see Tech_Stack.md). |

---

## 6. Definition of Done (Per Phase)

- **Phase 1:** End-to-end flow in staging; OpenAPI and setup docs; tests passing; no P0 gaps.
- **Phase 2:** All P1 requirements in staging; audit and logging in place; documentation and tests updated.
- **Phase 3:** Only contracted P2/P3 items; each with acceptance criteria and docs.

You can present both approaches with the Planning folder and this strategy, then implement incrementally with Cursor using the same plan and repo layout.
