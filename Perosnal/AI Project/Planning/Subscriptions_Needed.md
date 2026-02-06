# Subscriptions Needed

SaaS and API subscriptions required for the Data Annotation Platform. Approach A has no LLM costs; Approach B adds OpenAI (or Azure OpenAI).

---

## 1. Common to Both Approaches

| Service | Purpose | Typical model |
|---------|---------|----------------|
| **GitHub** | Repo, CI/CD (Actions) | Free or Team; check Actions minutes if private repo |
| **Okta** | SSO (OAuth2) — AUTH-02 | Org/developer tier; may be provided by - Data |
| **Azure** or **AWS** | Compute, Postgres, Blob/S3, Redis, Key Vault | Pay-as-you-go or org account; - Data may provide AWS |
| **Datadog** (or Azure Monitor) | Logs, metrics, alerts | Trial or subscription; PRD references Datadog |

*If - Data provides AWS and Okta, only GitHub and observability may be under your direct subscription.*

---

## 2. Approach A Only

No AI/LLM API subscription. Costs are:

- Infrastructure (compute, DB, storage)
- Okta (if not provided)
- Datadog or equivalent (if not provided)
- GitHub (if paid plan)

---

## 3. Approach B — LLM Subscription

| Provider | Product | Use case | Billing |
|----------|---------|----------|--------|
| **OpenAI** | API (e.g., GPT-4.1) | Suggested labels, instructions, linter, prelabels | Per token (input/output); set usage caps in dashboard |
| **Azure OpenAI** | Same models (GPT-4, etc.) | Same as above; use when data must stay in Azure | Per token or commitment; Azure billing |

**Recommendation:** Start with OpenAI API for speed and flexibility; move to Azure OpenAI if compliance or data residency requires it.

**Cost control:**

- Set monthly or per-project limits in OpenAI dashboard.
- Log token usage per project/feature; optionally alert when near threshold.
- Use smaller/cheaper models for simple tasks (e.g., instruction shortening).
- Optional: queue and batch LLM calls to respect rate limits and smooth cost.

---

## 4. Optional / Phase 3

| Service | Purpose | When |
|---------|---------|------|
| **n8n** (self-hosted or cloud) | Pre/post-processing workflows, webhooks | If Phase 3 processing hooks use n8n |
| **SendGrid / Twilio** | Notifications (e.g., rater alerts) | If Phase 3 notification center sends email/SMS |

---

## 5. Summary Table

| Item | Approach A | Approach B |
|------|------------|------------|
| GitHub | Yes | Yes |
| Okta | Yes (or provided) | Yes (or provided) |
| Azure/AWS | Yes (or provided) | Yes (or provided) |
| Datadog / monitoring | Yes (or provided) | Yes (or provided) |
| **OpenAI / Azure OpenAI** | No | **Yes** (pay-per-use or commitment) |

No other subscriptions are strictly required to implement and present both approaches. Add others only if you introduce new services (e.g., email, SMS, BI).
