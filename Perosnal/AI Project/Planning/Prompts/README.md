# Prompt Library — Approach B (With-LLM)

This folder holds **versioned prompt templates** for LLM-assisted features in the Data Annotation Platform. Use these with OpenAI API (e.g., GPT 4.1) or Azure OpenAI. No code here — only prompt text and placeholders.

---

## Purpose

- Single place for all LLM prompts; easy to diff, tune, and roll back.
- Placeholders like `{{task_content}}`, `{{schema}}` are replaced at runtime by the backend.
- Keeps prompt engineering separate from application code.

---

## File Index

| File | Feature | When to call |
|------|---------|--------------|
| [suggested_labels.md](./suggested_labels.md) | Suggested labels / pre-fill for task UI | When rater opens a task (optional; feature flag) |
| [instruction_generation.md](./instruction_generation.md) | Generate or refine project/batch instructions | When Ops creates or edits project/batch instructions |
| [consistency_linter.md](./consistency_linter.md) | Optional semantic consistency check (free-text) | After rater submits or in review (optional lint) |
| [benchmark_gold_proposal.md](./benchmark_gold_proposal.md) | Propose gold labels for benchmark tasks | When Ops creates golden set from sample tasks |
| [export_summary.md](./export_summary.md) | Short summary of batch/project for reports | When Ops exports or generates report (optional) |

---

## Usage (Implementation Phase)

1. Backend reads the appropriate prompt file (or cached version).
2. Replace placeholders with actual context (task content, schema, project name, etc.).
3. Call OpenAI (or Azure OpenAI) with the filled prompt; parse response.
4. Validate response against schema/business rules; store or display.
5. Log prompt version, token usage, and errors for audit and cost.

---

## Placeholder Convention

- `{{placeholder}}` — required; replace with string (escape if needed for JSON).
- Optional sections: wrap in `<!-- optional: section_name --> ... <!-- end -->` and include only when relevant.
- Keep prompts under model context limits; truncate long task content if necessary.

---

*No code in this folder; prompts only. Implementation lives in backend LLM service.*
