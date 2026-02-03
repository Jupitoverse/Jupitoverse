# 3. Backend, DevOps & Cloud – Interview Guide

Skills covered: Python, Flask, Docker, Kubernetes (K9s), Azure Data Factory, Azure AI Foundry, AWS CloudWatch

---

## 📋 Quick Reference

| Area | Key Points |
|------|------------|
| Flask | WSGI app, routes, blueprints, app factory, CORS, REST |
| Docker | Image, container, Dockerfile, compose, layers, volumes |
| Kubernetes | Pods, Deployments, Services, K9s for CLI management |
| Azure Data Factory | ETL/ELT, pipelines, activities, linked services, data flows |
| Azure AI Foundry | Azure AI studio: models, RAG, agents, deployment |
| AWS CloudWatch | Logs, metrics, alarms, dashboards, log insights |

---

## 🔑 Core Concepts

### 1. Python (Backend Context)

- WSGI: Web Server Gateway Interface; Flask is WSGI-compatible (Gunicorn, uWSGI).
- Async: For I/O-bound concurrency; Flask is sync by default; FastAPI/Starlette are async-native.
- Best practices: Virtual envs, type hints, env vars for config, structured logging.

### 2. Flask

- Application factory: `def create_app():` → create `Flask(__name__)`, load config, register blueprints, return app. Enables testing and multiple instances.
- Blueprints: Modular routes and views; `Blueprint('name', __name__)`; `app.register_blueprint(bp, url_prefix='/api/...')`.
- REST: Resource-based URLs, HTTP methods (GET/POST/PUT/DELETE), JSON request/response, status codes.

```python
# Application factory
def create_app(config=None):
    app = Flask(__name__)
    app.config.from_object(config or DefaultConfig)
    app.register_blueprint(api_bp, url_prefix='/api')
    return app
```

### 3. Docker

- Image: Read-only template (layers); built from Dockerfile.
- Container: Running instance of an image; isolated process + filesystem.
- Dockerfile: FROM, RUN, COPY, ADD, ENV, EXPOSE, CMD/ENTRYPOINT.
- Compose: Multi-container app via `docker-compose.yml` (services, networks, volumes).

### 4. Kubernetes (K8s) & K9s

- Pod: Smallest deployable unit; one or more containers sharing network/storage.
- Deployment: Declarative updates for Pods (replicas, rolling update).
- Service: Stable network access to Pods (ClusterIP, NodePort, LoadBalancer).
- K9s: Terminal UI to view/edit Pods, Deployments, Services, logs, exec into containers.

### 5. Azure Data Factory (ADF)

- Purpose: Serverless ETL/ELT; orchestrate data movement and transformation.
- Concepts: Pipeline (workflow), Activity (copy, transform, etc.), Linked Service (connection to store), Dataset (data structure).
- Use case: Ingest from blob/SQL/API → transform (e.g. Data Flow or Databricks) → load to warehouse/lake.

### 6. Azure AI Foundry (Azure AI Studio)

- Purpose: Build and deploy AI apps: models, RAG, agents, safety, deployment.
- Features: Model catalog, prompt flow, RAG with vector store, evaluation, deployment to endpoints.
- Relevance: Gen AI apps, RAG, and agents on Azure.

### 7. AWS CloudWatch

- Logs: Log groups/streams; retention; Logs Insights for querying.
- Metrics: Namespace, metric name, dimensions; custom metrics via API/SDK.
- Alarms: Thresholds on metrics → SNS (email, etc.) or auto-scaling actions.

---

## 💡 Top 15 Interview Q&A – Backend / DevOps / Cloud

Q1: What is the Flask application factory and why use it?
> "It’s a function that creates and configures the Flask app (e.g. `create_app()`). Benefits: multiple instances for testing, avoid circular imports, lazy init, and config flexibility."

Q2: What are Flask Blueprints?
> "Blueprints modularize the app: each has its own routes and optional static/templates. We register them with a URL prefix. Good for separating auth, API, admin, etc."

Q3: How do you run Flask in production?
> "Use a production WSGI server like Gunicorn or uWSGI behind a reverse proxy (e.g. Nginx). Don’t use the built-in dev server. Set workers, timeouts, and env (e.g. FLASK_ENV=production)."

Q4: What is CORS and how do you handle it in Flask?
> "Cross-Origin Resource Sharing – browsers block cross-origin requests unless the server allows. In Flask we use Flask-CORS: allow specific origins, methods, and headers. In prod we restrict to known front-end origins."

Q5: Docker image vs container?
> "Image is the read-only template (layers); container is a running instance with a writable layer. Multiple containers can run from the same image."

Q6: How do you reduce Docker image size?
> "Use a slim base (e.g. alpine, python-slim); multi-stage builds (build in one stage, copy artifact to a minimal final stage); minimize layers and avoid caching unnecessary files."

Q7: What is the difference between CMD and ENTRYPOINT?
> "CMD is the default command/args; ENTRYPOINT is the executable that runs. If both are set, CMD is passed as args to ENTRYPOINT. ENTRYPOINT is good for 'image as binary' usage."

Q8: What is a Kubernetes Pod?
> "The smallest deployable unit: one or more containers that share network and storage. Usually one main container per Pod; sidecars for logging, proxy, etc."

Q9: Deployment vs Service?
> "Deployment manages desired state of Pods (replicas, image, rollout). Service gives a stable network endpoint (cluster IP/DNS) to reach those Pods for load balancing."

Q10: What is K9s?
> "A terminal UI for Kubernetes: browse Pods, Deployments, Services, view logs, exec into containers, and perform basic operations without typing long kubectl commands."

Q11: What is Azure Data Factory used for?
> "Orchestrating ETL/ELT: copy data between stores, run transformations (e.g. Data Flows, Databricks), schedule and monitor pipelines. Linked services connect to sources and sinks; activities define steps."

Q12: What is Azure AI Foundry / AI Studio?
> "A platform to build and deploy AI solutions: choose models, build RAG and agents, evaluate, and deploy to endpoints. Relevant for Gen AI and RAG on Azure."

Q13: How do you monitor an app on AWS?
> "Use CloudWatch: send logs to Log Groups, emit metrics (e.g. latency, errors), set Alarms on thresholds (e.g. 5xx rate), and use Dashboards for visibility. Optionally use X-Ray for tracing."

Q14: How do you secure API keys and secrets?
> "Never commit them. Use env vars or a secrets manager (e.g. Azure Key Vault, AWS Secrets Manager). In K8s, use Secrets and mount as env or files. In Docker, pass via env at runtime, not in Dockerfile."

Q15: How would you scale a Flask app?
> "Horizontal: run multiple Gunicorn workers or replicas behind a load balancer. Use a shared session store (e.g. Redis) if needed. Database connection pooling; cache (Redis) for frequent reads; stateless app design."

---

## 📊 Key Talking Points

- Flask: App factory, blueprints, REST, CORS, production WSGI server.
- Docker: Image layers, multi-stage builds, compose for local multi-service.
- K8s: Pods, Deployments, Services; K9s for day-to-day ops.
- Azure: ADF for data pipelines; AI Foundry for Gen AI/RAG/agents.
- AWS: CloudWatch for logs, metrics, alarms, and dashboards.

---

## 📁 See Also

- [1_Core_GenAI_RAG_LLM.md](1_Core_GenAI_RAG_LLM.md) – RAG/LLM  
- [4_Data_Analytics_Python_DS.md](4_Data_Analytics_Python_DS.md) – Data stack  
- [0_GEN_AI_MASTER_INDEX.md](0_GEN_AI_MASTER_INDEX.md) – Master index  
