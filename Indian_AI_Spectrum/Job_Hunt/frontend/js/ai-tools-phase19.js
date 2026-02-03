// AI Tools Database - Phase 19: Data Science, ML & AI Development
// 200+ Tools for AI/ML development and data science

const AI_TOOLS_PHASE19 = [
    // ==================== AI/ML PLATFORMS ====================
    {name: "OpenAI", category: "AI Platform", subcategory: "LLM", desc: "Leading AI research company", url: "openai.com", pricing: "Freemium", rating: 4.8, tags: ["gpt", "chatgpt", "dalle"], featured: true},
    {name: "Anthropic", category: "AI Platform", subcategory: "LLM", desc: "AI safety company", url: "anthropic.com", pricing: "Paid", rating: 4.7, tags: ["claude", "safety", "constitutional"], featured: true},
    {name: "Google AI", category: "AI Platform", subcategory: "LLM", desc: "Google's AI platform", url: "ai.google", pricing: "Freemium", rating: 4.6, tags: ["gemini", "google", "multimodal"]},
    {name: "Cohere", category: "AI Platform", subcategory: "NLP", desc: "Enterprise NLP platform", url: "cohere.com", pricing: "Freemium", rating: 4.4, tags: ["nlp", "enterprise", "embeddings"]},
    {name: "AI21 Labs", category: "AI Platform", subcategory: "LLM", desc: "Language models", url: "ai21.com", pricing: "Freemium", rating: 4.3, tags: ["jurassic", "nlp", "writing"]},
    {name: "Hugging Face", category: "AI Platform", subcategory: "Hub", desc: "ML model hub", url: "huggingface.co", pricing: "Freemium", rating: 4.7, tags: ["hub", "transformers", "community"], featured: true},
    {name: "Replicate", category: "AI Platform", subcategory: "Inference", desc: "Run ML models in cloud", url: "replicate.com", pricing: "Pay-per-use", rating: 4.5, tags: ["inference", "api", "open-source"]},
    {name: "Together AI", category: "AI Platform", subcategory: "Inference", desc: "Open source AI cloud", url: "together.ai", pricing: "Pay-per-use", rating: 4.4, tags: ["inference", "fine-tuning", "open-source"]},
    {name: "Fireworks AI", category: "AI Platform", subcategory: "Inference", desc: "Fast model inference", url: "fireworks.ai", pricing: "Pay-per-use", rating: 4.4, tags: ["fast", "inference", "fine-tuning"]},
    {name: "Groq", category: "AI Platform", subcategory: "Hardware", desc: "LPU inference engine", url: "groq.com", pricing: "Freemium", rating: 4.5, tags: ["fast", "hardware", "lpu"]},
    {name: "Anyscale", category: "AI Platform", subcategory: "Compute", desc: "AI compute platform", url: "anyscale.com", pricing: "Paid", rating: 4.3, tags: ["ray", "distributed", "training"]},
    {name: "Modal", category: "AI Platform", subcategory: "Serverless", desc: "Serverless AI compute", url: "modal.com", pricing: "Pay-per-use", rating: 4.5, tags: ["serverless", "gpu", "python"]},
    {name: "Banana", category: "AI Platform", subcategory: "Serverless", desc: "Serverless ML hosting", url: "banana.dev", pricing: "Pay-per-use", rating: 4.2, tags: ["serverless", "gpu", "inference"]},
    {name: "RunPod", category: "AI Platform", subcategory: "GPU", desc: "GPU cloud for AI", url: "runpod.io", pricing: "Pay-per-use", rating: 4.4, tags: ["gpu", "affordable", "serverless"]},
    {name: "Lambda Labs", category: "AI Platform", subcategory: "GPU", desc: "GPU cloud for ML", url: "lambdalabs.com", pricing: "Paid", rating: 4.4, tags: ["gpu", "cloud", "workstations"]},
    
    // ==================== ML OPS ====================
    {name: "Weights & Biases", category: "MLOps", subcategory: "Experiment", desc: "ML experiment tracking", url: "wandb.ai", pricing: "Freemium", rating: 4.7, tags: ["experiment", "tracking", "visualization"], featured: true},
    {name: "MLflow", category: "MLOps", subcategory: "Platform", desc: "Open source ML platform", url: "mlflow.org", pricing: "Free", rating: 4.5, tags: ["open-source", "tracking", "deployment"]},
    {name: "Comet ML", category: "MLOps", subcategory: "Experiment", desc: "ML experiment management", url: "comet.com", pricing: "Freemium", rating: 4.4, tags: ["experiment", "tracking", "llm"]},
    {name: "Neptune.ai", category: "MLOps", subcategory: "Experiment", desc: "ML metadata store", url: "neptune.ai", pricing: "Freemium", rating: 4.4, tags: ["experiment", "metadata", "tracking"]},
    {name: "DVC", category: "MLOps", subcategory: "Data", desc: "Data version control", url: "dvc.org", pricing: "Free", rating: 4.4, tags: ["versioning", "data", "open-source"]},
    {name: "Kubeflow", category: "MLOps", subcategory: "Kubernetes", desc: "ML toolkit for Kubernetes", url: "kubeflow.org", pricing: "Free", rating: 4.2, tags: ["kubernetes", "pipelines", "open-source"]},
    {name: "Seldon", category: "MLOps", subcategory: "Deployment", desc: "ML deployment platform", url: "seldon.io", pricing: "Freemium", rating: 4.2, tags: ["deployment", "kubernetes", "enterprise"]},
    {name: "BentoML", category: "MLOps", subcategory: "Serving", desc: "ML model serving", url: "bentoml.com", pricing: "Freemium", rating: 4.4, tags: ["serving", "packaging", "open-source"]},
    {name: "Metaflow", category: "MLOps", subcategory: "Framework", desc: "ML framework by Netflix", url: "metaflow.org", pricing: "Free", rating: 4.4, tags: ["framework", "netflix", "data-science"]},
    {name: "Prefect", category: "MLOps", subcategory: "Orchestration", desc: "Data workflow orchestration", url: "prefect.io", pricing: "Freemium", rating: 4.5, tags: ["orchestration", "workflow", "python"]},
    {name: "Dagster", category: "MLOps", subcategory: "Orchestration", desc: "Data orchestration platform", url: "dagster.io", pricing: "Freemium", rating: 4.4, tags: ["orchestration", "data", "assets"]},
    {name: "Airflow", category: "MLOps", subcategory: "Orchestration", desc: "Workflow automation", url: "airflow.apache.org", pricing: "Free", rating: 4.3, tags: ["orchestration", "apache", "dags"]},
    {name: "ZenML", category: "MLOps", subcategory: "Framework", desc: "MLOps framework", url: "zenml.io", pricing: "Freemium", rating: 4.3, tags: ["framework", "pipelines", "portable"]},
    {name: "ClearML", category: "MLOps", subcategory: "Platform", desc: "End-to-end MLOps", url: "clear.ml", pricing: "Freemium", rating: 4.4, tags: ["experiment", "pipeline", "serving"]},
    {name: "Valohai", category: "MLOps", subcategory: "Platform", desc: "MLOps platform", url: "valohai.com", pricing: "Paid", rating: 4.2, tags: ["platform", "automation", "enterprise"]},
    
    // ==================== DATA SCIENCE ====================
    {name: "Jupyter", category: "Data Science", subcategory: "Notebooks", desc: "Interactive notebooks", url: "jupyter.org", pricing: "Free", rating: 4.7, tags: ["notebooks", "python", "open-source"], featured: true},
    {name: "Google Colab", category: "Data Science", subcategory: "Notebooks", desc: "Free cloud notebooks", url: "colab.research.google.com", pricing: "Freemium", rating: 4.6, tags: ["notebooks", "free-gpu", "google"]},
    {name: "Kaggle", category: "Data Science", subcategory: "Platform", desc: "Data science community", url: "kaggle.com", pricing: "Free", rating: 4.6, tags: ["competitions", "datasets", "notebooks"]},
    {name: "Databricks", category: "Data Science", subcategory: "Platform", desc: "Unified analytics platform", url: "databricks.com", pricing: "Paid", rating: 4.5, tags: ["spark", "lakehouse", "enterprise"]},
    {name: "Deepnote", category: "Data Science", subcategory: "Notebooks", desc: "Data science notebooks", url: "deepnote.com", pricing: "Freemium", rating: 4.5, tags: ["collaborative", "notebooks", "sql"]},
    {name: "Hex", category: "Data Science", subcategory: "Analytics", desc: "Data workspace", url: "hex.tech", pricing: "Freemium", rating: 4.5, tags: ["notebooks", "sql", "apps"]},
    {name: "Observable", category: "Data Science", subcategory: "Visualization", desc: "Data exploration notebooks", url: "observablehq.com", pricing: "Freemium", rating: 4.4, tags: ["javascript", "d3", "reactive"]},
    {name: "Saturn Cloud", category: "Data Science", subcategory: "Cloud", desc: "Data science cloud", url: "saturncloud.io", pricing: "Freemium", rating: 4.3, tags: ["cloud", "dask", "gpu"]},
    {name: "Paperspace", category: "Data Science", subcategory: "GPU", desc: "GPU cloud platform", url: "paperspace.com", pricing: "Pay-per-use", rating: 4.3, tags: ["gpu", "notebooks", "gradient"]},
    {name: "Lightning AI", category: "Data Science", subcategory: "Platform", desc: "AI development platform", url: "lightning.ai", pricing: "Freemium", rating: 4.4, tags: ["pytorch", "studios", "apps"]},
    {name: "Streamlit", category: "Data Science", subcategory: "Apps", desc: "Data app framework", url: "streamlit.io", pricing: "Freemium", rating: 4.6, tags: ["apps", "python", "dashboards"]},
    {name: "Gradio", category: "Data Science", subcategory: "Demos", desc: "ML demo builder", url: "gradio.app", pricing: "Free", rating: 4.5, tags: ["demos", "interfaces", "huggingface"]},
    {name: "Dash", category: "Data Science", subcategory: "Dashboards", desc: "Python dashboards", url: "plotly.com/dash", pricing: "Freemium", rating: 4.3, tags: ["dashboards", "plotly", "python"]},
    {name: "Panel", category: "Data Science", subcategory: "Dashboards", desc: "Python dashboards", url: "panel.holoviz.org", pricing: "Free", rating: 4.2, tags: ["dashboards", "holoviz", "widgets"]},
    {name: "Voila", category: "Data Science", subcategory: "Notebooks", desc: "Notebooks to web apps", url: "voila.readthedocs.io", pricing: "Free", rating: 4.1, tags: ["jupyter", "apps", "widgets"]},
    
    // ==================== VECTOR DATABASES ====================
    {name: "Pinecone", category: "Vector DB", subcategory: "Managed", desc: "Vector database for AI", url: "pinecone.io", pricing: "Freemium", rating: 4.6, tags: ["vector", "managed", "similarity"], featured: true},
    {name: "Weaviate", category: "Vector DB", subcategory: "Open Source", desc: "Open source vector DB", url: "weaviate.io", pricing: "Freemium", rating: 4.5, tags: ["vector", "open-source", "hybrid"]},
    {name: "Milvus", category: "Vector DB", subcategory: "Open Source", desc: "Vector database", url: "milvus.io", pricing: "Free", rating: 4.4, tags: ["vector", "open-source", "scalable"]},
    {name: "Qdrant", category: "Vector DB", subcategory: "Open Source", desc: "Vector similarity engine", url: "qdrant.tech", pricing: "Freemium", rating: 4.5, tags: ["vector", "rust", "fast"]},
    {name: "Chroma", category: "Vector DB", subcategory: "Open Source", desc: "AI-native vector DB", url: "trychroma.com", pricing: "Free", rating: 4.4, tags: ["vector", "embeddings", "simple"]},
    {name: "LanceDB", category: "Vector DB", subcategory: "Serverless", desc: "Serverless vector DB", url: "lancedb.com", pricing: "Freemium", rating: 4.3, tags: ["vector", "serverless", "multimodal"]},
    {name: "Vespa", category: "Vector DB", subcategory: "Search", desc: "Big data serving engine", url: "vespa.ai", pricing: "Freemium", rating: 4.3, tags: ["search", "vector", "yahoo"]},
    {name: "Zilliz", category: "Vector DB", subcategory: "Cloud", desc: "Milvus cloud service", url: "zilliz.com", pricing: "Freemium", rating: 4.3, tags: ["milvus", "cloud", "enterprise"]},
    {name: "Supabase Vector", category: "Vector DB", subcategory: "Postgres", desc: "pgvector in Supabase", url: "supabase.com/vector", pricing: "Freemium", rating: 4.3, tags: ["postgres", "pgvector", "supabase"]},
    {name: "SingleStore", category: "Vector DB", subcategory: "Database", desc: "Unified database with vectors", url: "singlestore.com", pricing: "Freemium", rating: 4.2, tags: ["database", "real-time", "vector"]},
    
    // ==================== LLM TOOLS ====================
    {name: "LangChain", category: "LLM Tools", subcategory: "Framework", desc: "LLM application framework", url: "langchain.com", pricing: "Free", rating: 4.5, tags: ["framework", "chains", "agents"], featured: true},
    {name: "LlamaIndex", category: "LLM Tools", subcategory: "Framework", desc: "Data framework for LLMs", url: "llamaindex.ai", pricing: "Free", rating: 4.5, tags: ["rag", "data", "framework"]},
    {name: "Haystack", category: "LLM Tools", subcategory: "Framework", desc: "NLP framework", url: "haystack.deepset.ai", pricing: "Free", rating: 4.3, tags: ["rag", "search", "open-source"]},
    {name: "Semantic Kernel", category: "LLM Tools", subcategory: "Framework", desc: "Microsoft LLM SDK", url: "github.com/microsoft/semantic-kernel", pricing: "Free", rating: 4.2, tags: ["microsoft", "sdk", "c-sharp"]},
    {name: "Promptfoo", category: "LLM Tools", subcategory: "Testing", desc: "LLM testing framework", url: "promptfoo.dev", pricing: "Freemium", rating: 4.4, tags: ["testing", "evaluation", "open-source"]},
    {name: "Helicone", category: "LLM Tools", subcategory: "Monitoring", desc: "LLM observability", url: "helicone.ai", pricing: "Freemium", rating: 4.4, tags: ["monitoring", "logging", "observability"]},
    {name: "LangSmith", category: "LLM Tools", subcategory: "Monitoring", desc: "LangChain debugging", url: "smith.langchain.com", pricing: "Freemium", rating: 4.4, tags: ["debugging", "langchain", "tracing"]},
    {name: "Portkey", category: "LLM Tools", subcategory: "Gateway", desc: "LLM gateway", url: "portkey.ai", pricing: "Freemium", rating: 4.3, tags: ["gateway", "observability", "routing"]},
    {name: "Literal AI", category: "LLM Tools", subcategory: "Monitoring", desc: "LLM monitoring platform", url: "literalai.com", pricing: "Freemium", rating: 4.2, tags: ["monitoring", "evaluation", "chainlit"]},
    {name: "Instructor", category: "LLM Tools", subcategory: "Structured", desc: "Structured LLM outputs", url: "useinstructor.com", pricing: "Free", rating: 4.4, tags: ["structured", "pydantic", "typing"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE19 = AI_TOOLS_PHASE19;
}


