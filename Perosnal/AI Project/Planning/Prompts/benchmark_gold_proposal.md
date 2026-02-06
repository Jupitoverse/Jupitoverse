# Benchmark Gold Proposal — Gold Set Creation

**Feature:** Propose gold labels for a subset of tasks so Ops can create benchmark (golden) tasks.  
**Model:** GPT 4.1 or similar.  
**When:** Ops selects a set of tasks and runs “Propose gold labels”; Ops reviews and confirms before marking as golden.

---

## System prompt (optional)

You are an expert annotator. Given task content and the response schema, propose the correct annotation (gold label) for this task. Output only valid values that fit the schema. Be consistent and objective. Output in the requested JSON format only.

---

## User prompt (template)

```
Task content:
{{task_content}}

Response schema (field id, type, allowed values):
{{schema}}

Propose the gold annotation as a JSON object with one key per schema field id. Use only allowed values for select fields. For free-text, provide a concise gold answer. Output only the JSON, no explanation.
```

---

## Placeholders

| Placeholder | Description |
|-------------|-------------|
| `{{task_content}}` | Full task content (truncate if very long) |
| `{{schema}}` | Response schema and allowed values |

---

## Response handling

- Parse JSON; validate against schema.
- Store as “proposed gold”; Ops must explicitly approve before task is marked as benchmark.
- Do not auto-apply to production; audit log the proposal and approval.
