# Instruction Generation — Project/Batch Instructions

**Feature:** Generate or refine instruction text for annotators/reviewers.  
**Model:** GPT 4.1 or similar.  
**When:** Ops creates or edits project/batch; optional “Generate from schema” action.

---

## System prompt (optional)

You are a technical writer for annotation projects. Generate clear, concise instructions for raters based on project name and response schema. Use neutral language and bullet points where helpful. Do not invent labels or options not present in the schema.

---

## User prompt (template)

```
Project name: {{project_name}}

Batch name (if any): {{batch_name}}

Response schema and field descriptions:
{{schema_with_descriptions}}

Generate short instructions (2–4 paragraphs or bullet list) that explain:
1. What to annotate (high level).
2. How to fill each main field type (single-select, multi-select, free-text).
3. Any special rules (e.g., when to leave blank, format for free-text).

Output only the instruction text, no preamble.
```

---

## Placeholders

| Placeholder | Description |
|-------------|-------------|
| `{{project_name}}` | Project display name |
| `{{batch_name}}` | Batch name or “General” |
| `{{schema_with_descriptions}}` | Schema with field ids, types, and any descriptions |

---

## Response handling

- Use as draft; Ops must review and edit before publishing.
- Store as plain text; support markdown if task UI supports it.
