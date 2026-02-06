# Consistency Linter — Optional LLM Lint

**Feature:** Optional semantic consistency check for free-text (or mixed) annotations.  
**Model:** GPT 4.1 or similar.  
**When:** After rater submits or in review; only if “LLM consistency lint” is enabled for project.

---

## System prompt (optional)

You are a quality checker for annotations. Compare the task content with the rater’s free-text response. Decide if the response is semantically consistent with the task (e.g., no contradiction, plausible interpretation). Output only: CONSISTENT or INCONSISTENT, then one short reason (one line). Do not output anything else.

---

## User prompt (template)

```
Task content:
{{task_content}}

Rater's response (free-text or selected labels):
{{annotation_response}}

Is this response semantically consistent with the task? Answer with:
CONSISTENT / INCONSISTENT
Reason: <one short line>
```

---

## Placeholders

| Placeholder | Description |
|-------------|-------------|
| `{{task_content}}` | Task text/media description (truncate if needed) |
| `{{annotation_response}}` | The rater’s submitted response (relevant fields only) |

---

## Response handling

- Parse first line for CONSISTENT vs INCONSISTENT; store result and reason as lint result.
- If parse fails, store as “lint error” (e.g., unknown); do not block submission unless configured as blocking.
- This lint is optional and additive to programmatic linters (Approach A).
