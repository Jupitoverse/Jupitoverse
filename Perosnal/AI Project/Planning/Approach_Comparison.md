# Approach Comparison: No-LLM vs With-LLM

High-level comparison of the two solution approaches for the Data Annotation Platform.

---

## At a Glance

| Dimension | Approach A — No-LLM | Approach B — With-LLM |
|-----------|----------------------|------------------------|
| **Core platform** | Same (Workspace → Project → Batch → Task → Annotation, pipelines, queueing) | Same |
| **Quality / validation** | Rule-based linters, benchmarks, consensus (no AI) | Same + optional LLM-assisted suggestions and conflict hints |
| **Automation** | Manual Ops workflows; deterministic logic only | Optional LLM assist: instruction generation, label suggestions, review hints |
| **External APIs** | None (no AI/LLM calls) | OpenAI API (e.g., GPT 4.1) for assistive features only |
| **Cost** | No per-token AI cost; infra + labor only | Infra + labor + API usage (configurable caps) |
| **Complexity** | Lower; no model integration or prompt ops | Higher; prompt design, safety, rate limits, fallbacks |
| **Implementable with Cursor** | Yes, fully | Yes, fully |
| **PRD compliance** | Full (Phases 1–2; Phase 3 optional) | Full + optional Phase 3 AI enhancements |

---

## Feature Mapping

| PRD Area | Approach A (No-LLM) | Approach B (With-LLM) |
|----------|----------------------|------------------------|
| **Queueing & assignment** | FIFO, claim locking, manual/auto assignment — rules only | Same |
| **Linters (QUAL-01)** | Programmatic rules (regex, schema, thresholds) | Same + optional “LLM lint” (e.g., consistency check) |
| **Benchmarks** | Pre-labeled gold; compare rater output to gold | Same; optional LLM to generate or refine gold set |
| **Task UI** | Schema-driven; no AI in UI | Same; optional “suggested label” or “pre-fill” from LLM |
| **Ops tooling** | Upload, export, reset/archive, tagging — manual | Same; optional LLM for export summaries or report blurbs |
| **Pre/post-processing (Phase 3)** | Scripts (Lambda/custom); no ML | Optional LLM in pipeline (e.g., normalize text, suggest categories) |
| **Prelabels/predictions (Phase 3)** | Out of scope or manual | LLM-generated prelabels; rater edits/confirms |

---

## When to Choose Which

- **Choose Approach A** when: budget and simplicity matter most; no need for AI-assisted labeling or automation; you want zero dependency on external LLM APIs and no token cost.
- **Choose Approach B** when: you want assistive AI (suggestions, instructions, prelabels) and can manage API cost, prompts, and fallbacks; Phase 3 “predictions/prelabels” or smart tooling is in scope.

Both approaches can be implemented using Cursor and your stack (Python, FastAPI, Azure, Docker, etc.). Approach B is a superset: build Approach A first, then add LLM features on top.
