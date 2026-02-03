// AI Tools Database - Phase 7: Data, Analytics & Finance AI
// 200+ Tools for data professionals and finance

const AI_TOOLS_PHASE7 = [
    // ==================== DATA ANALYSIS ====================
    {name: "Tableau", category: "Data", subcategory: "Visualization", desc: "Business intelligence and analytics", url: "tableau.com", pricing: "Paid", rating: 4.7, tags: ["visualization", "bi", "enterprise"], featured: true},
    {name: "Power BI", category: "Data", subcategory: "Visualization", desc: "Microsoft business analytics", url: "powerbi.microsoft.com", pricing: "Freemium", rating: 4.6, tags: ["microsoft", "bi", "visualization"], featured: true},
    {name: "Looker", category: "Data", subcategory: "BI Platform", desc: "Google Cloud BI platform", url: "looker.com", pricing: "Paid", rating: 4.5, tags: ["google", "bi", "data-modeling"]},
    {name: "Metabase", category: "Data", subcategory: "BI Platform", desc: "Open-source BI tool", url: "metabase.com", pricing: "Freemium", rating: 4.5, tags: ["open-source", "sql", "easy"]},
    {name: "Apache Superset", category: "Data", subcategory: "BI Platform", desc: "Open-source data exploration", url: "superset.apache.org", pricing: "Free", rating: 4.4, tags: ["open-source", "exploration", "dashboards"]},
    {name: "Redash", category: "Data", subcategory: "BI Platform", desc: "Open-source dashboards", url: "redash.io", pricing: "Freemium", rating: 4.3, tags: ["open-source", "sql", "dashboards"]},
    {name: "Mode Analytics", category: "Data", subcategory: "Analytics", desc: "Collaborative data science", url: "mode.com", pricing: "Freemium", rating: 4.4, tags: ["sql", "python", "collaboration"]},
    {name: "Sigma", category: "Data", subcategory: "Cloud BI", desc: "Cloud-native BI platform", url: "sigmacomputing.com", pricing: "Paid", rating: 4.4, tags: ["cloud", "spreadsheet", "bi"]},
    {name: "ThoughtSpot", category: "Data", subcategory: "AI Analytics", desc: "AI-powered analytics", url: "thoughtspot.com", pricing: "Paid", rating: 4.4, tags: ["ai", "search", "insights"]},
    {name: "Sisense", category: "Data", subcategory: "BI Platform", desc: "Embedded analytics platform", url: "sisense.com", pricing: "Paid", rating: 4.3, tags: ["embedded", "analytics", "ai"]},
    {name: "Domo", category: "Data", subcategory: "BI Platform", desc: "Cloud BI and data platform", url: "domo.com", pricing: "Paid", rating: 4.2, tags: ["cloud", "integrations", "mobile"]},
    {name: "Qlik", category: "Data", subcategory: "BI Platform", desc: "Data analytics platform", url: "qlik.com", pricing: "Paid", rating: 4.3, tags: ["associative", "analytics", "enterprise"]},
    {name: "Observable", category: "Data", subcategory: "Data Notebooks", desc: "Collaborative data notebooks", url: "observablehq.com", pricing: "Freemium", rating: 4.5, tags: ["notebooks", "javascript", "visualization"]},
    {name: "Hex", category: "Data", subcategory: "Data Notebooks", desc: "Collaborative data workspace", url: "hex.tech", pricing: "Freemium", rating: 4.5, tags: ["notebooks", "sql", "collaboration"]},
    {name: "Deepnote", category: "Data", subcategory: "Data Notebooks", desc: "Collaborative data science", url: "deepnote.com", pricing: "Freemium", rating: 4.4, tags: ["notebooks", "python", "collaboration"]},
    {name: "Jupyter", category: "Data", subcategory: "Notebooks", desc: "Open-source data notebooks", url: "jupyter.org", pricing: "Free", rating: 4.7, tags: ["open-source", "python", "notebooks"]},
    {name: "Google Colab", category: "Data", subcategory: "Notebooks", desc: "Free Python notebooks with GPU", url: "colab.research.google.com", pricing: "Freemium", rating: 4.6, tags: ["free", "gpu", "google"]},
    {name: "Kaggle", category: "Data", subcategory: "Data Science", desc: "Data science community and competitions", url: "kaggle.com", pricing: "Free", rating: 4.6, tags: ["community", "competitions", "datasets"]},
    {name: "DataRobot", category: "Data", subcategory: "AutoML", desc: "Enterprise AI platform", url: "datarobot.com", pricing: "Paid", rating: 4.4, tags: ["automl", "enterprise", "mlops"]},
    {name: "H2O.ai", category: "Data", subcategory: "AutoML", desc: "Open-source machine learning", url: "h2o.ai", pricing: "Freemium", rating: 4.4, tags: ["automl", "open-source", "enterprise"]},
    
    // ==================== DATA ENGINEERING ====================
    {name: "Snowflake", category: "Data Engineering", subcategory: "Data Warehouse", desc: "Cloud data platform", url: "snowflake.com", pricing: "Paid", rating: 4.7, tags: ["warehouse", "cloud", "scalable"], featured: true},
    {name: "Databricks", category: "Data Engineering", subcategory: "Data Platform", desc: "Unified analytics platform", url: "databricks.com", pricing: "Paid", rating: 4.7, tags: ["spark", "lakehouse", "ml"], featured: true},
    {name: "BigQuery", category: "Data Engineering", subcategory: "Data Warehouse", desc: "Google Cloud data warehouse", url: "cloud.google.com/bigquery", pricing: "Paid", rating: 4.6, tags: ["google", "serverless", "sql"]},
    {name: "Redshift", category: "Data Engineering", subcategory: "Data Warehouse", desc: "AWS data warehouse", url: "aws.amazon.com/redshift", pricing: "Paid", rating: 4.4, tags: ["aws", "warehouse", "enterprise"]},
    {name: "Fivetran", category: "Data Engineering", subcategory: "ETL", desc: "Automated data integration", url: "fivetran.com", pricing: "Paid", rating: 4.6, tags: ["etl", "connectors", "automated"]},
    {name: "Airbyte", category: "Data Engineering", subcategory: "ETL", desc: "Open-source data integration", url: "airbyte.com", pricing: "Freemium", rating: 4.5, tags: ["open-source", "etl", "connectors"]},
    {name: "Stitch", category: "Data Engineering", subcategory: "ETL", desc: "Simple data pipeline", url: "stitchdata.com", pricing: "Freemium", rating: 4.3, tags: ["simple", "etl", "talend"]},
    {name: "dbt", category: "Data Engineering", subcategory: "Transformation", desc: "Data transformation tool", url: "getdbt.com", pricing: "Freemium", rating: 4.7, tags: ["transformation", "sql", "analytics"]},
    {name: "Apache Airflow", category: "Data Engineering", subcategory: "Orchestration", desc: "Workflow orchestration", url: "airflow.apache.org", pricing: "Free", rating: 4.5, tags: ["orchestration", "open-source", "scheduling"]},
    {name: "Prefect", category: "Data Engineering", subcategory: "Orchestration", desc: "Modern data orchestration", url: "prefect.io", pricing: "Freemium", rating: 4.4, tags: ["orchestration", "python", "modern"]},
    {name: "Dagster", category: "Data Engineering", subcategory: "Orchestration", desc: "Data orchestration platform", url: "dagster.io", pricing: "Freemium", rating: 4.4, tags: ["orchestration", "software-defined", "assets"]},
    {name: "Apache Kafka", category: "Data Engineering", subcategory: "Streaming", desc: "Event streaming platform", url: "kafka.apache.org", pricing: "Free", rating: 4.6, tags: ["streaming", "events", "distributed"]},
    {name: "Confluent", category: "Data Engineering", subcategory: "Streaming", desc: "Kafka as a service", url: "confluent.io", pricing: "Freemium", rating: 4.5, tags: ["kafka", "streaming", "managed"]},
    {name: "Apache Spark", category: "Data Engineering", subcategory: "Processing", desc: "Big data processing", url: "spark.apache.org", pricing: "Free", rating: 4.6, tags: ["big-data", "processing", "distributed"]},
    {name: "Trino (Presto)", category: "Data Engineering", subcategory: "Query Engine", desc: "Distributed SQL query engine", url: "trino.io", pricing: "Free", rating: 4.4, tags: ["sql", "distributed", "federated"]},
    
    // ==================== MACHINE LEARNING ====================
    {name: "TensorFlow", category: "ML", subcategory: "Framework", desc: "Open-source ML framework by Google", url: "tensorflow.org", pricing: "Free", rating: 4.6, tags: ["google", "deep-learning", "production"], featured: true},
    {name: "PyTorch", category: "ML", subcategory: "Framework", desc: "Open-source ML framework by Meta", url: "pytorch.org", pricing: "Free", rating: 4.8, tags: ["meta", "research", "dynamic"], featured: true},
    {name: "Hugging Face", category: "ML", subcategory: "Model Hub", desc: "AI model hub and tools", url: "huggingface.co", pricing: "Freemium", rating: 4.8, tags: ["models", "transformers", "community"], featured: true},
    {name: "Weights & Biases", category: "ML", subcategory: "MLOps", desc: "ML experiment tracking", url: "wandb.ai", pricing: "Freemium", rating: 4.7, tags: ["tracking", "experiments", "visualization"]},
    {name: "MLflow", category: "ML", subcategory: "MLOps", desc: "Open-source ML lifecycle", url: "mlflow.org", pricing: "Free", rating: 4.5, tags: ["open-source", "lifecycle", "tracking"]},
    {name: "Neptune.ai", category: "ML", subcategory: "MLOps", desc: "Experiment tracking for ML", url: "neptune.ai", pricing: "Freemium", rating: 4.4, tags: ["tracking", "metadata", "collaboration"]},
    {name: "Comet ML", category: "ML", subcategory: "MLOps", desc: "ML experiment management", url: "comet.ml", pricing: "Freemium", rating: 4.3, tags: ["experiments", "visualization", "comparison"]},
    {name: "DVC", category: "ML", subcategory: "MLOps", desc: "Data version control", url: "dvc.org", pricing: "Free", rating: 4.4, tags: ["versioning", "data", "open-source"]},
    {name: "LangChain", category: "ML", subcategory: "LLM Framework", desc: "Framework for LLM applications", url: "langchain.com", pricing: "Free", rating: 4.6, tags: ["llm", "framework", "agents"]},
    {name: "LlamaIndex", category: "ML", subcategory: "LLM Framework", desc: "Data framework for LLMs", url: "llamaindex.ai", pricing: "Free", rating: 4.5, tags: ["rag", "indexing", "llm"]},
    {name: "Ollama", category: "ML", subcategory: "Local LLM", desc: "Run LLMs locally", url: "ollama.ai", pricing: "Free", rating: 4.6, tags: ["local", "llm", "easy"]},
    {name: "LM Studio", category: "ML", subcategory: "Local LLM", desc: "Desktop app for local LLMs", url: "lmstudio.ai", pricing: "Free", rating: 4.5, tags: ["local", "desktop", "gui"]},
    {name: "Replicate", category: "ML", subcategory: "Model Hosting", desc: "Run ML models in the cloud", url: "replicate.com", pricing: "Pay-per-use", rating: 4.5, tags: ["hosting", "api", "easy"]},
    {name: "Modal", category: "ML", subcategory: "Serverless ML", desc: "Serverless ML infrastructure", url: "modal.com", pricing: "Pay-per-use", rating: 4.5, tags: ["serverless", "python", "gpu"]},
    {name: "Baseten", category: "ML", subcategory: "Model Hosting", desc: "ML model deployment", url: "baseten.co", pricing: "Pay-per-use", rating: 4.3, tags: ["deployment", "hosting", "inference"]},
    
    // ==================== FINANCE & TRADING ====================
    {name: "Bloomberg Terminal", category: "Finance", subcategory: "Financial Data", desc: "Professional financial terminal", url: "bloomberg.com/terminal", pricing: "Paid", rating: 4.8, tags: ["professional", "data", "trading"], featured: true},
    {name: "Refinitiv Eikon", category: "Finance", subcategory: "Financial Data", desc: "Financial analysis platform", url: "refinitiv.com", pricing: "Paid", rating: 4.5, tags: ["data", "analysis", "lseg"]},
    {name: "AlphaSense", category: "Finance", subcategory: "Market Intelligence", desc: "AI market intelligence", url: "alpha-sense.com", pricing: "Paid", rating: 4.5, tags: ["research", "ai", "search"]},
    {name: "Koyfin", category: "Finance", subcategory: "Financial Analysis", desc: "Financial data and analytics", url: "koyfin.com", pricing: "Freemium", rating: 4.4, tags: ["analytics", "affordable", "modern"]},
    {name: "Finviz", category: "Finance", subcategory: "Stock Screener", desc: "Stock screener and visualization", url: "finviz.com", pricing: "Freemium", rating: 4.5, tags: ["screener", "visualization", "free"]},
    {name: "TradingView", category: "Finance", subcategory: "Charting", desc: "Charting and trading platform", url: "tradingview.com", pricing: "Freemium", rating: 4.7, tags: ["charts", "social", "trading"]},
    {name: "Seeking Alpha", category: "Finance", subcategory: "Investment Research", desc: "Investment research platform", url: "seekingalpha.com", pricing: "Freemium", rating: 4.3, tags: ["research", "community", "analysis"]},
    {name: "Benzinga", category: "Finance", subcategory: "News", desc: "Financial news and data", url: "benzinga.com", pricing: "Freemium", rating: 4.2, tags: ["news", "real-time", "data"]},
    {name: "QuantConnect", category: "Finance", subcategory: "Algorithmic Trading", desc: "Algorithmic trading platform", url: "quantconnect.com", pricing: "Freemium", rating: 4.4, tags: ["algo-trading", "backtesting", "cloud"]},
    {name: "Alpaca", category: "Finance", subcategory: "Trading API", desc: "Commission-free trading API", url: "alpaca.markets", pricing: "Free", rating: 4.4, tags: ["api", "trading", "commission-free"]},
    {name: "Polygon.io", category: "Finance", subcategory: "Market Data", desc: "Real-time market data API", url: "polygon.io", pricing: "Freemium", rating: 4.4, tags: ["api", "data", "real-time"]},
    {name: "Plaid", category: "Finance", subcategory: "Banking API", desc: "Connect to bank accounts", url: "plaid.com", pricing: "Paid", rating: 4.5, tags: ["api", "banking", "fintech"]},
    {name: "Stripe", category: "Finance", subcategory: "Payments", desc: "Payment processing platform", url: "stripe.com", pricing: "Pay-per-use", rating: 4.8, tags: ["payments", "developer", "global"]},
    {name: "Wise", category: "Finance", subcategory: "Transfers", desc: "International money transfers", url: "wise.com", pricing: "Pay-per-use", rating: 4.6, tags: ["transfers", "forex", "affordable"]},
    {name: "Mercury", category: "Finance", subcategory: "Banking", desc: "Banking for startups", url: "mercury.com", pricing: "Free", rating: 4.6, tags: ["startup", "banking", "modern"]},
    
    // ==================== ACCOUNTING & TAX ====================
    {name: "QuickBooks", category: "Accounting", subcategory: "Accounting Software", desc: "Small business accounting", url: "quickbooks.intuit.com", pricing: "Paid", rating: 4.4, tags: ["smb", "accounting", "intuit"], featured: true},
    {name: "Xero", category: "Accounting", subcategory: "Accounting Software", desc: "Cloud accounting software", url: "xero.com", pricing: "Paid", rating: 4.5, tags: ["cloud", "accounting", "small-business"]},
    {name: "FreshBooks", category: "Accounting", subcategory: "Accounting Software", desc: "Invoicing and accounting", url: "freshbooks.com", pricing: "Paid", rating: 4.4, tags: ["invoicing", "freelancers", "simple"]},
    {name: "Wave", category: "Accounting", subcategory: "Free Accounting", desc: "Free accounting software", url: "waveapps.com", pricing: "Free", rating: 4.3, tags: ["free", "small-business", "invoicing"]},
    {name: "Zoho Books", category: "Accounting", subcategory: "Accounting Software", desc: "Online accounting software", url: "zoho.com/books", pricing: "Freemium", rating: 4.3, tags: ["zoho", "accounting", "affordable"]},
    {name: "Bench", category: "Accounting", subcategory: "Bookkeeping", desc: "Online bookkeeping service", url: "bench.co", pricing: "Paid", rating: 4.3, tags: ["bookkeeping", "service", "human"]},
    {name: "Pilot", category: "Accounting", subcategory: "Bookkeeping", desc: "Bookkeeping for startups", url: "pilot.com", pricing: "Paid", rating: 4.2, tags: ["startups", "bookkeeping", "cfo"]},
    {name: "TurboTax", category: "Accounting", subcategory: "Tax Software", desc: "Tax preparation software", url: "turbotax.intuit.com", pricing: "Paid", rating: 4.4, tags: ["tax", "personal", "intuit"]},
    {name: "H&R Block", category: "Accounting", subcategory: "Tax Software", desc: "Tax preparation and filing", url: "hrblock.com", pricing: "Freemium", rating: 4.2, tags: ["tax", "preparation", "service"]},
    {name: "TaxJar", category: "Accounting", subcategory: "Sales Tax", desc: "Sales tax automation", url: "taxjar.com", pricing: "Paid", rating: 4.3, tags: ["sales-tax", "automation", "ecommerce"]},
    {name: "Avalara", category: "Accounting", subcategory: "Tax Compliance", desc: "Tax compliance automation", url: "avalara.com", pricing: "Paid", rating: 4.3, tags: ["compliance", "automation", "enterprise"]},
    {name: "Expensify", category: "Accounting", subcategory: "Expense Management", desc: "Expense reporting software", url: "expensify.com", pricing: "Freemium", rating: 4.3, tags: ["expenses", "receipts", "reporting"]},
    {name: "Ramp", category: "Accounting", subcategory: "Corporate Cards", desc: "Corporate cards and spend management", url: "ramp.com", pricing: "Free", rating: 4.6, tags: ["cards", "spend", "automation"]},
    {name: "Brex", category: "Accounting", subcategory: "Corporate Cards", desc: "Corporate cards for startups", url: "brex.com", pricing: "Free", rating: 4.4, tags: ["startups", "cards", "rewards"]},
    {name: "Bill.com", category: "Accounting", subcategory: "AP/AR", desc: "Accounts payable/receivable automation", url: "bill.com", pricing: "Paid", rating: 4.2, tags: ["ap", "ar", "automation"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE7 = AI_TOOLS_PHASE7;
}


