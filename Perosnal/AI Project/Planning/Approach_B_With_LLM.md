# Approach B: Solution With LLM (e.g., OpenAI GPT 4.1)

Same core platform as Approach A, plus **optional LLM-assisted features** using an external API (e.g., OpenAI GPT 4.1). All core behavior remains deterministic; LLM is additive.

---

## 1. Summary

- **Core platform:** Identical to Approach A (data model, pipeline, queueing, Ops/Rater/Reviewer/Customer portals).
- **LLM role:** Assistive only — suggestions, prelabels, instruction generation, optional conflict hints. No LLM-driven state transitions or mandatory AI decisions.
- **API:** OpenAI API (e.g., GPT 4.1) or Azure OpenAI; LangChain/LangGraph optional for orchestration. Implementable with Cursor.

---

## 2. Where LLM Is Used (Optional Features)

| Area | Use case | How |
|------|----------|-----|
| **Task UI** | Suggested labels / pre-fill | Call LLM with task content + schema; return suggested values; rater can accept or edit. |
| **Instructions** | Project/batch instructions | Generate or refine instruction text from project name + schema description (Ops edits before publish). |
| **Linters** | Optional “consistency” lint | LLM checks semantic consistency of free-text responses (e.g., against task content); result stored as lint result; blocking/warning configurable. |
| **Benchmarks** | Gold set creation | LLM proposes gold labels for a subset of tasks; Ops reviews and marks as golden. |
| **Export / reporting** | Summary blurbs | LLM generates short summary of batch/project for reports (optional). |
| **Pre/post-processing (Phase 3)** | Text normalization / categorization | LLM in pipeline to normalize text or suggest categories before task creation or after export. |
| **Prelabels (Phase 3)** | Pre-annotations | LLM produces prelabels; task UI shows them as editable; export includes original + final. |

---

## 3. Design Principles (Approach B)

- **Fallback:** Every LLM feature must have a non-LLM path (e.g., no suggestion, or rule-based only) so platform works if API is down or disabled.
- **No critical path:** Claim locking, assignment, pipeline transitions, and export logic do not depend on LLM; they stay rule-based.
- **Configurable:** Ops can enable/disable LLM features per project or batch; cost and rate limits are controllable.
- **Audit:** Log LLM calls (project, task, feature, token usage) for cost and compliance.
- **Safety:** Validate and sanitize LLM output against schema; never execute raw model output as code.

---

## 4. Technical Integration

- **Provider:** OpenAI API (GPT 4.1) or Azure OpenAI (same models); keep provider behind an abstraction so you can switch or add others.
- **Orchestration (optional):** LangChain/LangGraph for multi-step flows (e.g., generate → validate → retry); simple REST calls are enough for single-call features.
- **Prompts:** Versioned prompt templates stored in repo (see `Planning/Prompts/`); inject task/schema/project context; few-shot examples where helpful.
- **Rate limits & cost:** Per-project or global caps; queue LLM requests if needed; use smaller/cheaper models for simple tasks where acceptable.

---

## 5. Best Solution Within With-LLM

- **Start as Approach A:** Build and stabilize the full platform without LLM first; add LLM features as optional toggles.
- **One feature at a time:** e.g., “suggested labels” in task UI first; then instruction generation; then optional linter/reporting.
- **Prompt library:** Centralized, versioned prompts (see Prompts folder); easy to tune and A/B test.
- **Config flags:** `project.enable_llm_suggestions`, `project.enable_llm_linter`, etc.; no code deploy to turn features on/off.
- **Observability:** Log model, tokens, latency, errors; optional dashboard for LLM usage and cost per project.

This yields a PRD-compliant platform with optional, safe LLM assistance that you can implement and iterate on using Cursor.
