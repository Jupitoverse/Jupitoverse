# Suggested Labels — Task UI Pre-fill

**Feature:** Return suggested annotation values for a task so the rater can accept or edit.  
**Model:** GPT 4.1 or similar.  
**When:** Optional; when rater opens a task and feature is enabled for project.

---

## System prompt (optional)

You are an annotation assistant. Given task content and the expected response schema, suggest valid annotation values. Output only valid options or text that fit the schema. Do not explain; output in the requested format.

---

## User prompt (template)

```
Task content (for context):
{{task_content}}

Response schema (field id, type, allowed values if any):
{{schema}}

Allowed values for single/multi-select (if any): {{allowed_values}}

Return a JSON object with one key per schema field id and the suggested value(s). Use this exact structure:
{{schema_example}}

For free-text fields, suggest a concise answer. For single-select, choose one option. For multi-select, choose all that apply. If uncertain, prefer leaving a field as null.
```

---

## Placeholders

| Placeholder | Description |
|-------------|-------------|
| `{{task_content}}` | Text/media description or transcript (truncate if very long) |
| `{{schema}}` | Response schema (field ids, types, options) |
| `{{allowed_values}}` | List of allowed options for select fields |
| `{{schema_example}}` | Example JSON shape, e.g. `{"sentiment": "positive", "notes": null}` |

---

## Response handling

- Parse JSON from model output; validate against schema.
- If parse fails or validation fails, return no suggestions (fallback: empty).
- Do not display raw model output without validation.
