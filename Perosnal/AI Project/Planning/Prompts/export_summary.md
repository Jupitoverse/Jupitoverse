# Export Summary — Batch/Project Report Blurb

**Feature:** Generate a short summary of a batch or project for reports or delivery notes.  
**Model:** GPT 4.1 or similar.  
**When:** Optional; when Ops exports a batch or generates a report and “Include AI summary” is enabled.

---

## System prompt (optional)

You are a report assistant. Given batch/project metadata and high-level stats, write a 2–4 sentence executive summary suitable for a delivery report. Be factual and neutral. Do not invent numbers; use only the provided stats. Output only the summary text.

---

## User prompt (template)

```
Project: {{project_name}}
Batch: {{batch_name}}

Stats:
- Total tasks: {{total_tasks}}
- Completed annotations: {{completed_count}}
- Pipeline stages: {{pipeline_stages}}
- Export date: {{export_date}}

Write a 2–4 sentence executive summary for the delivery report. Use only the above information. Output only the summary, no heading.
```

---

## Placeholders

| Placeholder | Description |
|-------------|-------------|
| `{{project_name}}` | Project name |
| `{{batch_name}}` | Batch name |
| `{{total_tasks}}` | Total task count |
| `{{completed_count}}` | Number of completed annotations |
| `{{pipeline_stages}}` | Comma-separated stage names |
| `{{export_date}}` | Export timestamp or date |

---

## Response handling

- Store as optional field in export metadata or report; do not replace human-written notes.
- If model fails or is disabled, leave summary blank (fallback).
