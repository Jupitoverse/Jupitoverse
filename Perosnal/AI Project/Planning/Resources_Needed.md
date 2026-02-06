# Resources Needed

Tools, environments, and assets required to implement and run the Data Annotation Platform (both approaches). No code deliverables — planning only.

---

## 1. Development Environment

| Resource | Purpose | Notes |
|----------|---------|-------|
| **IDE** | Cursor (primary), VS Code | Cursor for implementation and prompts. |
| **Python** | 3.11+ | Backend and scripts. |
| **Node.js** (optional) | If using React/Vite for frontend | LTS version. |
| **Git** | Version control | GitHub assumed (PRD). |
| **Docker Desktop** | Local containers for app, Postgres, Redis | Eases local dev and alignment with prod. |
| **DB client** | pgAdmin, DBeaver, or VS Code extension | Inspect Postgres. |
| **API client** | Postman, Insomnia, or curl | Test REST APIs and OpenAPI. |

---

## 2. Infrastructure (Dev / Staging / Prod)

| Resource | Purpose | Who provides (typical) |
|----------|---------|-------------------------|
| **Compute** | Run API, workers, frontend (or static host) | Azure App Service / Container Apps or AWS ECS/EC2 |
| **PostgreSQL** | Primary DB | Azure Database for PostgreSQL or AWS RDS |
| **Blob/Object storage** | Task assets, uploads, export artifacts | Azure Blob or S3 |
| **Redis** (optional) | Claim lock, cache, Celery broker | Azure Cache for Redis or ElastiCache |
| **Secrets** | API keys, DB URLs, Okta client secret | Azure Key Vault or AWS Secrets Manager |
| **DNS / SSL** | Hostnames, HTTPS | Azure/AWS or existing IT |

*PRD states “- Data provides standardized AWS environments”; if so, use provided AWS accounts and conform to their stack (Postgres, S3, etc.).*

---

## 3. Third-Party / Integrations

| Resource | Purpose | Phase |
|----------|---------|--------|
| **Okta** | SSO (OAuth2) — AUTH-02 | Phase 2 |
| **Datadog** (or equivalent) | Logs, metrics, alerts — PRD | Phase 2 |
| **GitHub** | Repo, Issues, Actions (CI/CD) | Phase 1 |

---

## 4. Data & Test Assets

| Resource | Purpose |
|----------|---------|
| **Sample workspace/project/batch** | Realistic hierarchy for dev and demos |
| **Sample tasks** | Mix of text, image, audio/video URLs (or small files) |
| **Sample response schemas** | Single-select, multi-select, free-text, mixed |
| **Golden/benchmark tasks** | Pre-labeled tasks for Phase 2 benchmark flow |
| **Rater/Reviewer/Ops test accounts** | Per role for UAT and staging demo |

---

## 5. Documentation & Specs

| Resource | Location / Owner |
|----------|-------------------|
| PRD Addendum v2.0 | `Data_Annotation_Platform_PRD_Addendum_v2.0 - Copy.pdf` |
| Appendix A (requirements) | In same PRD |
| This planning set | `Planning/` (README, approaches, plan, strategy, tech stack, etc.) |
| API spec (later) | OpenAPI YAML/JSON in repo |
| Runbooks | To be added in implementation (env setup, deploy, rollback) |

---

## 6. Approach B Only — LLM

| Resource | Purpose |
|----------|---------|
| **OpenAI account** (or Azure OpenAI) | API access for GPT 4.1 (or chosen model) |
| **API key** | Stored in secrets; never in repo |
| **Prompt templates** | Stored in `Planning/Prompts/` and versioned |
| **Usage/cost tracking** | Per-project or global caps; logs for token count and cost |

See **Subscriptions_Needed.md** for billing and quotas.

---

## 7. Summary Checklist

- [ ] Dev machine: Python, Docker, Git, Cursor
- [ ] Repo: GitHub (or designated)
- [ ] Infra: Postgres, Blob/S3, optional Redis; compute for API + workers
- [ ] Auth: Okta tenant (or - Data–provided)
- [ ] Observability: Datadog or Azure App Insights
- [ ] (Approach B) OpenAI or Azure OpenAI account and key
- [ ] Sample data and test accounts for UAT and staging demo

All of the above are planning references; no implementation is implied in this document.
