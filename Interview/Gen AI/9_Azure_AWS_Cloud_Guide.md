# 9. Azure & AWS Cloud – Interview Guide

Skills covered: Azure basics; Azure Monitor (CloudWatch-like); Azure Data Factory; data ingestion; Azure AI Foundry; Azure Synapse; AWS basics (EC2, CloudWatch, health checks); Kafka lag; Elasticsearch.

---

## Quick Reference

| Area | Key Points |
|------|------------|
| Azure basics | Subscriptions, resource groups, regions; IAM (Azure AD, RBAC) |
| Azure Monitor | Logs, metrics, alerts, dashboards; Log Analytics, Application Insights |
| Azure Data Factory | ETL/ELT; pipelines, activities, linked services, datasets; triggers |
| Data ingestion | ADF copy activity; event-based (Event Grid); streaming (Event Hubs) |
| Azure AI Foundry | AI Studio: models, RAG, agents; deployment, safety |
| Azure Synapse | Analytics: SQL pool, Spark, pipeline; lake + warehouse |
| AWS EC2 | Virtual servers; instance types, AMI, security groups, key pairs |
| AWS CloudWatch | Logs, metrics, alarms; dashboards; Logs Insights |
| Health checks | ALB/NLB health checks; EC2 status; auto-scaling based on health |
| Kafka lag | Consumer lag = messages not yet consumed; monitor and scale consumers |
| Elasticsearch | Search engine; full-text, aggregations; dense_vector for RAG hybrid |

---

## Azure Basics

- Subscription: Billing and access boundary; one or more per org.
- Resource group: Logical container for resources in a subscription; lifecycle and RBAC.
- Region: Geographic location (e.g. East US); some services are regional or global.
- IAM: Azure AD for identity; RBAC (role-based access) on subscription/resource group/resource.
- Common services: Compute (VMs, App Service, AKS), Storage (Blob, ADLS), DB (Cosmos, SQL DB), Networking (VNet, Load Balancer).

---

## Azure Monitor (vs “Azure CloudWatch”)

Azure’s equivalent to AWS CloudWatch for observability:

- Logs: Send to Log Analytics workspace; query with KQL (Kusto Query Language); retention and alerts.
- Metrics: Platform and custom metrics; dimensions; chart in workbooks/dashboards.
- Alerts: Rule on metric or log query; action groups (email, webhook, runbook, etc.).
- Application Insights: APM for apps (requests, dependencies, exceptions, performance).
- Use: Centralize logs from ADF, AI, apps; set alerts on failure or latency; dashboards for pipelines and APIs.

---

## Azure Data Factory (ADF)

- Purpose: Serverless ETL/ELT; orchestrate data movement and transformation.
- Pipeline: Workflow containing activities (copy, transform, control).
- Activity: Copy (source → sink), Data Flow (transform in Spark), Execute Pipeline, etc.
- Linked service: Connection to store (Blob, SQL, HTTP, etc.); credentials in Key Vault.
- Dataset: Schema/structure of data at a location.
- Trigger: Schedule, event, or manual; runs pipeline.
- Data Flow: In-memory Spark; mapping data flows for ETL without code (or code for complex logic).
- Use: Ingest from Blob/SQL/API → transform (Data Flow or Databricks) → load to warehouse/lake (Synapse, ADLS).

---

## Data Ingestion (Azure)

- Batch: ADF copy activity; schedule or event-driven; from files, DBs, APIs to Blob/ADLS/Synapse.
- Event-driven: Event Grid (event routing) or Event Hubs (streaming ingestion); trigger ADF or downstream.
- Streaming: Event Hubs or IoT Hub; process with Stream Analytics, Spark, or custom consumers.
- Best practices: Incremental loads (watermark, change tracking); idempotency; error handling and retries; store raw then transform (medallion).

---

## Azure AI Foundry (AI Studio)

- Purpose: Build and deploy Gen AI apps on Azure.
- Features: Model catalog (OpenAI, OSS); prompt flow; RAG (vector store, index); agents; safety (content filter); deployment to endpoints.
- Use: Deploy RAG or agents; use Azure OpenAI; evaluate and monitor; integrate with ADF or Synapse for data.

---

## Azure Synapse

- Purpose: Unified analytics: data lake + data warehouse + pipelines + Spark.
- SQL pool: Dedicated or serverless SQL for querying lake (Parquet, etc.) or warehouse.
- Spark pool: For transformation, ML, streaming.
- Pipelines: Same as ADF; orchestrate ingest and transform.
- Use: Lakehouse pattern; one place for raw/curated/serving; SQL and Spark in same workspace.

---

## AWS Basics – EC2

- EC2: Virtual server in AWS; choose AMI (OS/image), instance type (vCPU, memory), region, AZ.
- Security group: Firewall (inbound/outbound rules); attach to instance(s).
- Key pair: SSH key for Linux login; store private key securely.
- Storage: EBS (volume attached to instance); instance store (ephemeral).
- Use: Run apps when you need full control; alternatively use Lambda, ECS, or managed services.

---

## AWS CloudWatch

- Logs: Log groups and streams; send from EC2, Lambda, apps; retention; CloudWatch Logs Insights for querying.
- Metrics: Namespace, metric name, dimensions; default (CPU, etc.) and custom (put from app).
- Alarms: Threshold on metric (e.g. CPU > 80%); trigger SNS, auto-scaling, or other actions.
- Dashboards: Visualize metrics and logs.
- Use: Centralize logs and metrics; alert on errors or latency; drive auto-scaling.

---

## Health Checks (AWS)

- ALB/NLB: Target group health check (HTTP path, interval, healthy/unhealthy threshold); traffic only to healthy targets.
- EC2: Instance status checks (system, instance); optional detailed monitoring.
- Auto Scaling: Use health check to replace unhealthy instances; combine with ALB for rolling updates.
- Use: Ensure traffic goes only to healthy instances; auto-heal by replacing bad instances.

---

## Kafka Lag

- Consumer lag: Difference between latest offset in partition and current consumer offset; messages not yet consumed.
- Why it matters: High lag = consumer can’t keep up; delay and backlog.
- Monitor: Kafka metrics (consumer lag per group/topic/partition); CloudWatch or Datadog if using Amazon MSK.
- Mitigation: Scale consumers (more instances or partitions); optimize consumer logic; increase parallelism; fix slow downstream (DB, API).
- Use: Set alerts on lag; tune partition count and consumer count; debug slow pipelines.

---

## Elasticsearch (Basics)

- Purpose: Search and analytics engine; full-text search, aggregations, structured queries.
- Index: Like a “table”; documents (JSON); mapping = schema (field types).
- Query: Match, term, bool, range; aggregations (sum, avg, terms bucket).
- dense_vector: Field type for vector similarity (cosine, dot product); use for hybrid (keyword + vector) RAG.
- Use: Log search, product search, dashboards (Kibana); hybrid RAG when you already use ES.
- vs Vector DB: ES is general search + vector; dedicated vector DBs are tuned for ANN at very large scale.

---

## Top 15 Interview Q&A – Azure & AWS

Q1: What is Azure Data Factory used for?
> "Serverless ETL/ELT: copy data between stores (Blob, SQL, API), run transformations (Data Flow, Databricks), schedule and monitor. Linked services for connections; activities in pipelines; triggers to run."

Q2: How do you ingest data in Azure?
> "Batch: ADF copy activity on schedule or event. Streaming: Event Hubs. Event-driven: Event Grid to trigger ADF or functions. I use incremental loads (watermark) and store raw then transform."

Q3: What is Azure AI Foundry / AI Studio?
> "Platform to build and deploy Gen AI: model catalog, prompt flow, RAG with vector store, agents, safety, deployment to endpoints. Use for RAG and agents on Azure."

Q4: What is Azure Synapse?
> "Unified analytics: data lake + warehouse + pipelines + Spark. SQL pool (dedicated or serverless) and Spark pool; same pipelines as ADF. Lakehouse in one workspace."

Q5: What is Azure Monitor?
> "Azure’s observability: logs (Log Analytics, KQL), metrics, alerts, dashboards, Application Insights. Use for centralizing logs and metrics from ADF, apps, and AI services; set alerts on failure or latency."

Q6: What is EC2 and when do you use it?
> "AWS virtual server: choose AMI, instance type, region. Use when you need full control of OS and app. Otherwise consider Lambda, ECS, or RDS for less ops."

Q7: How do you monitor an app on AWS?
> "CloudWatch: send logs to Log Groups, put metrics (latency, errors), create Alarms on thresholds, use Dashboards. Optionally X-Ray for tracing. Alert on 5xx or high latency."

Q8: How do health checks work for EC2 behind a load balancer?
> "ALB target group has a health check (path, interval, healthy/unhealthy threshold). ALB sends traffic only to healthy targets. Unhealthy instances are replaced by ASG if configured."

Q9: What is Kafka consumer lag?
> "Lag = latest offset in partition minus consumer’s current offset; messages not yet consumed. High lag means consumer is behind. I monitor it and scale consumers or partitions; fix slow processing or downstream."

Q10: When do you use Elasticsearch?
> "Full-text search, log search, aggregations, dashboards. For RAG, use dense_vector for hybrid (keyword + vector) when we already have ES. Dedicated vector DB for very large ANN-only workloads."

Q11: What is the difference between Azure Monitor and AWS CloudWatch?
> "Same idea: logs, metrics, alerts, dashboards. Azure Monitor uses Log Analytics and KQL; CloudWatch uses Log Groups and Logs Insights. Both integrate with respective ecosystems."

Q12: What is a linked service in ADF?
> "Connection to external store (Blob, SQL DB, HTTP, etc.). Holds connection info; credentials in Key Vault. Datasets reference linked service to define data location and shape."

Q13: How do you secure secrets in Azure and AWS?
> "Azure: Key Vault; reference in ADF or app. AWS: Secrets Manager or Parameter Store; IAM for access. Never put secrets in code or config in repo."

Q14: What is the difference between Event Hubs and Event Grid?
> "Event Hubs: high-throughput streaming ingestion; process with Stream Analytics or consumers. Event Grid: event routing (pub/sub); trigger functions, ADF, etc. Use Event Hubs for streams; Event Grid for discrete events."

Q15: How does Gen AI fit with Azure data services?
> "ADF ingests and prepares data; Synapse for lake/warehouse. AI Foundry uses that data for RAG (index in vector store) or training. End-to-end: ingest → curate → index → RAG/agents in AI Foundry."

---

## Key Talking Points

- Azure: Resource groups, ADF for ETL, Monitor for observability, AI Foundry for Gen AI, Synapse for analytics.
- AWS: EC2, CloudWatch (logs, metrics, alarms), health checks for ALB/ASG.
- Data: ADF copy and Data Flow; incremental and event-driven ingestion.
- Kafka lag: monitor and scale consumers; fix slow processing.
- Elasticsearch: search and analytics; dense_vector for hybrid RAG when already using ES.

---

## See Also

- [3_Backend_DevOps_Cloud.md](3_Backend_DevOps_Cloud.md) – Docker, K8s, ADF, AI Foundry, CloudWatch
- [1_Core_GenAI_RAG_LLM.md](1_Core_GenAI_RAG_LLM.md) – RAG, vector DBs
- [0_GEN_AI_MASTER_INDEX.md](0_GEN_AI_MASTER_INDEX.md) – Master index
