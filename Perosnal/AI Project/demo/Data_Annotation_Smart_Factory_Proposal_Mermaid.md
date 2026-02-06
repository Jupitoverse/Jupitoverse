# Data Annotation Smart Factory Proposal — Mermaid Diagrams

These diagrams correspond to the **Data_Annotation_Smart_Factory_Proposal_Final.pptx** (technical architecture, infra, database, workflow). Use in docs or render in GitHub / Mermaid Live.

---

## 1. High-Level Architecture (Slide 7 — Architecture Blueprint)

```mermaid
flowchart TB
    subgraph Edge["Layer 1 — Edge"]
        CF[CloudFront CDN]
        WAF[AWS WAF]
    end

    subgraph API["Layer 2 — API"]
        APIGW[API Gateway REST]
    end

    subgraph Compute["Layer 3 — Compute"]
        L1[Lambda: Auth]
        L2[Lambda: Queue Consumer]
        L3[Lambda: Linter]
        L4[Lambda: Export]
    end

    subgraph Queue["Queueing"]
        SQS[SQS FIFO]
    end

    subgraph Data["Layer 4 — Data"]
        RDS[(PostgreSQL RDS)]
        MONGO[(MongoDB Atlas)]
        S3[(S3 Buckets)]
    end

    User[Users / Ops / Raters] --> CF
    CF --> WAF --> APIGW
    APIGW --> L1 & L2 & L3 & L4
    L2 --> SQS
    SQS --> L2
    L1 & L2 & L3 & L4 --> RDS & MONGO & S3
```

---

## 2. Technology Stack — Component Map (Slide 6)

```mermaid
flowchart LR
    subgraph Frontend["Frontend"]
        React[React 18 + Tailwind]
        CDN[CloudFront + S3]
    end

    subgraph Security["Security"]
        Okta[Okta OIDC]
        WAF2[AWS WAF]
        SM[Secrets Manager]
    end

    subgraph Backend["Backend"]
        APIGW2[API Gateway]
        Lambda[Lambda Node.js 20]
        SQS2[SQS FIFO]
    end

    subgraph Storage["Storage"]
        PG[(PostgreSQL 15)]
        Mongo[(MongoDB)]
        S32[S3]
    end

    React --> CDN
    CDN --> APIGW2
    Okta --> APIGW2
    WAF2 --> APIGW2
    APIGW2 --> Lambda
    Lambda --> SQS2
    Lambda --> PG & Mongo & S32
    SM --> Lambda
```

---

## 3. End-to-End Workflow (Slides 5, 11 — Smart Factory + How It Works)

```mermaid
flowchart LR
    subgraph Ingest["1. INGEST"]
        A[Ops uploads batch]
        B[Validate files]
        C[Push to SQS Pending]
    end

    subgraph Assign["2. ASSIGNMENT"]
        D[Rater clicks Start]
        E[Pop from Queue]
        F[PostgreSQL: SELECT FOR UPDATE SKIP LOCKED]
        G[Lock task to User A]
    end

    subgraph Execute["3. EXECUTION"]
        H[Rater labels]
        I[Auto-save]
        J[Submit → Linter Lambda]
        K{Valid?}
    end

    subgraph Delivery["4. DELIVERY"]
        L[Move to Done/Review]
        M[Export JSON/CSV]
        N[Signed S3 URLs]
    end

    A --> B --> C
    C --> D --> E --> F --> G
    G --> H --> I --> J --> K
    K -->|Yes| L --> M --> N
    K -->|No| H
```

---

## 4. Task Claim — Sequence (Deterministic Locking)

```mermaid
sequenceDiagram
    participant Rater
    participant API
    participant Lambda
    participant PostgreSQL
    participant SQS

    Rater->>API: POST /queue/next
    API->>Lambda: Invoke (or sync DB)
    Lambda->>PostgreSQL: BEGIN; SELECT id FROM tasks WHERE batch_id=? AND claimed_by_id IS NULL ORDER BY created_at LIMIT 1 FOR UPDATE SKIP LOCKED
    PostgreSQL-->>Lambda: task_id
    Lambda->>PostgreSQL: UPDATE tasks SET claimed_by_id=?, claimed_at=NOW() WHERE id=?
    Lambda->>PostgreSQL: COMMIT
    Lambda-->>API: task payload
    API-->>Rater: 200 + task
```

---

## 5. Database & Data Model (Slide 8 — Conceptual ER)

```mermaid
erDiagram
    users ||--o{ tasks : "claims"
    users ||--o{ annotations : "creates"
    workspaces ||--o{ projects : "contains"
    projects ||--o{ batches : "contains"
    batches ||--o{ tasks : "contains"
    tasks ||--o{ annotations : "has"

    users {
        int id PK
        string email
        string role
    }

    workspaces {
        int id PK
        string name
    }

    projects {
        int id PK
        int workspace_id FK
        json pipeline_stages
        json response_schema
    }

    batches {
        int id PK
        int project_id FK
        string name
    }

    tasks {
        int id PK
        int batch_id FK
        int claimed_by_id FK
        datetime claimed_at
        string status
        string pipeline_stage
    }

    annotations {
        int id PK
        int task_id FK
        int user_id FK
        json response
        string pipeline_stage
    }
```

---

## 6. 8-Week Timeline (Slide 13 — Team & Timeline)

```mermaid
gantt
    title Phase 1 MVP — 8-Week Plan
    dateFormat  YYYY-MM-DD
    section Team
    1x Solution Architect (Serverless & Security) :a1, 2026-02-10, 56d
    2x Senior Full-Stack Engineers (UI + Backend) :a2, 2026-02-10, 56d
    1x UI/UX Designer :a3, 2026-02-10, 56d
    section Phase
    Week 1-2: Infrastructure & Auth (Okta) :p1, 2026-02-10, 14d
    Week 3-6: Traffic Controller Queue & Task UI :p2, 2026-02-24, 28d
    Week 7: E2E Testing (5k user sim) & Ops Tools :p3, 2026-03-24, 7d
    Week 8: UAT & Handoff :p4, 2026-03-31, 7d
```

---

## 7. Security & Access Flow (Internal vs External)

```mermaid
flowchart TB
    subgraph External["External (Raters)"]
        R[Rater Workbench]
    end

    subgraph Internal["Internal (Ops / Managers)"]
        O[Ops Command Center]
    end

    subgraph Okta["Okta"]
        IDP[Identity Provider]
    end

    subgraph API_Gateway["API Gateway"]
        ExtPath[/queue, /tasks/claim, /submit]
        IntPath[/workspaces, /projects, /batches, /export]
    end

    R --> ExtPath
    O --> IntPath
    R & O --> IDP
    IDP --> ExtPath & IntPath
    ExtPath --> Lambda
    IntPath --> Lambda
```

---

## How to Use

- **GitHub**: Paste any code block into a `.md` file; GitHub renders Mermaid automatically.
- **Mermaid Live**: https://mermaid.live — paste and export as PNG/SVG.
- **VS Code**: Install "Mermaid Preview" or "Markdown Preview Mermaid Support" to preview.

All diagrams align with the final proposal deck: architecture layers, tech stack, workflow, DB model, timeline, and security.
