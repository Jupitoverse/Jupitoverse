# Data Annotation Platform — Planning

This folder contains all planning artifacts for the **Data Annotation Platform** project, based on the PRD Addendum v2.0. No implementation code lives here; only strategy, approach, and presentation materials.

## Purpose

- Present **two solution approaches**: one without AI/LLM, one with LLM (e.g., OpenAI GPT 4.1).
- Define implementation strategy that can be executed **using Cursor** and your existing stack (Python, FastAPI, Flask, Azure, Docker, etc.).

---

## Document Index

| Document | Description |
|----------|-------------|
| [Approach_Comparison.md](./Approach_Comparison.md) | Side-by-side comparison of Approach A (No-LLM) vs Approach B (With-LLM) |
| [Approach_A_No_LLM.md](./Approach_A_No_LLM.md) | Full approach **without** AI/LLM — rules, workflows, manual ops |
| [Approach_B_With_LLM.md](./Approach_B_With_LLM.md) | Full approach **with** LLM (e.g., OpenAI GPT 4.1) — assistive automation |
| [Team_Structure.md](./Team_Structure.md) | Team structure, roles, and responsibilities for both approaches |
| [Implementation_Plan.md](./Implementation_Plan.md) | Phased plan (Phase 1 MVP → Phase 2 → Phase 3 optional) |
| [Implementation_Strategy.md](./Implementation_Strategy.md) | How to build it (including Cursor-only workflow) |
| [Tech_Stack.md](./Tech_Stack.md) | Recommended technology stack (Python/FastAPI, frontend, DB, infra) |
| [Resources_Needed.md](./Resources_Needed.md) | Tools, infrastructure, and environment needs |
| [Subscriptions_Needed.md](./Subscriptions_Needed.md) | SaaS and API subscriptions (e.g., OpenAI, Azure, etc.) |
| [Presentation_Outline.md](./Presentation_Outline.md) | Presentation outline and slide structure for both approaches |
| [Prompts/](./Prompts/) | Prompt files for LLM-assisted features (Approach B) |

---

## Quick Summary

- **Approach A (No-LLM):** Rule-based quality checks, manual Ops workflows, deterministic queue/assignment. No external AI APIs; implementable entirely with Cursor + your stack.
- **Approach B (With-LLM):** Same core platform plus LLM-assisted features (e.g., suggested labels, conflict resolution, instruction generation). Uses OpenAI API (e.g., GPT 4.1); still implementable with Cursor.

Both approaches target the same PRD scope (Workspace → Project → Batch → Task → Annotation, pipelines, queueing, Ops/Rater/Reviewer/Customer portals) and can be built incrementally.

---

## How to Use This Folder

1. **Presenting:** Use [Presentation_Outline.md](./Presentation_Outline.md) and the approach docs for stakeholder decks.
2. **Estimating:** Use [Implementation_Plan.md](./Implementation_Plan.md), [Resources_Needed.md](./Resources_Needed.md), and [Subscriptions_Needed.md](./Subscriptions_Needed.md).
3. **Building:** Follow [Implementation_Strategy.md](./Implementation_Strategy.md) and [Tech_Stack.md](./Tech_Stack.md); use Cursor for implementation.
4. **LLM features:** Refer to [Approach_B_With_LLM.md](./Approach_B_With_LLM.md) and [Prompts/](./Prompts/) when adding AI-assisted capabilities.

---

*Last updated: Planning phase — no code deliverables in this folder.*
