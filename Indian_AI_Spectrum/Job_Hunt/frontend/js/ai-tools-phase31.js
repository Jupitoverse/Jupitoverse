// AI Tools Database - Phase 31: More AI/ML & Data Tools
// 150+ Additional AI/ML tools

const AI_TOOLS_PHASE31 = [
    // ==================== MACHINE LEARNING PLATFORMS ====================
    {name: "AWS SageMaker", category: "ML Platform", subcategory: "Cloud", desc: "AWS ML platform", url: "aws.amazon.com/sagemaker", pricing: "Pay-per-use", rating: 4.4, tags: ["aws", "enterprise", "full-cycle"], featured: true},
    {name: "Google Vertex AI", category: "ML Platform", subcategory: "Cloud", desc: "Google Cloud ML platform", url: "cloud.google.com/vertex-ai", pricing: "Pay-per-use", rating: 4.5, tags: ["google", "automl", "enterprise"]},
    {name: "Azure Machine Learning", category: "ML Platform", subcategory: "Cloud", desc: "Microsoft ML platform", url: "azure.microsoft.com/machine-learning", pricing: "Pay-per-use", rating: 4.3, tags: ["azure", "enterprise", "mlops"]},
    {name: "IBM Watson Studio", category: "ML Platform", subcategory: "Enterprise", desc: "IBM AI platform", url: "ibm.com/watson/studio", pricing: "Paid", rating: 4.1, tags: ["ibm", "enterprise", "watson"]},
    {name: "H2O.ai", category: "ML Platform", subcategory: "AutoML", desc: "AutoML platform", url: "h2o.ai", pricing: "Freemium", rating: 4.4, tags: ["automl", "open-source", "enterprise"]},
    {name: "DataRobot", category: "ML Platform", subcategory: "AutoML", desc: "Enterprise AI platform", url: "datarobot.com", pricing: "Paid", rating: 4.3, tags: ["automl", "enterprise", "mlops"]},
    {name: "Alteryx", category: "ML Platform", subcategory: "Analytics", desc: "Analytics automation", url: "alteryx.com", pricing: "Paid", rating: 4.3, tags: ["analytics", "automation", "no-code"]},
    {name: "RapidMiner", category: "ML Platform", subcategory: "Data Science", desc: "Data science platform", url: "rapidminer.com", pricing: "Freemium", rating: 4.2, tags: ["data-science", "visual", "enterprise"]},
    {name: "KNIME", category: "ML Platform", subcategory: "Open Source", desc: "Open analytics platform", url: "knime.com", pricing: "Freemium", rating: 4.3, tags: ["open-source", "visual", "workflows"]},
    {name: "Domino Data Lab", category: "ML Platform", subcategory: "Enterprise", desc: "Enterprise MLOps", url: "dominodatalab.com", pricing: "Paid", rating: 4.2, tags: ["enterprise", "mlops", "collaboration"]},
    {name: "Dataiku", category: "ML Platform", subcategory: "Collaborative", desc: "Collaborative data science", url: "dataiku.com", pricing: "Freemium", rating: 4.4, tags: ["collaborative", "visual", "enterprise"]},
    {name: "Anaconda", category: "ML Platform", subcategory: "Python", desc: "Python/R data science", url: "anaconda.com", pricing: "Freemium", rating: 4.5, tags: ["python", "packages", "environments"]},
    {name: "MindsDB", category: "ML Platform", subcategory: "Database", desc: "ML in databases", url: "mindsdb.com", pricing: "Freemium", rating: 4.2, tags: ["database", "sql", "predictions"]},
    {name: "PyCaret", category: "ML Platform", subcategory: "Low-Code", desc: "Low-code ML library", url: "pycaret.org", pricing: "Free", rating: 4.4, tags: ["low-code", "python", "automl"]},
    {name: "AutoKeras", category: "ML Platform", subcategory: "AutoML", desc: "AutoML for Keras", url: "autokeras.com", pricing: "Free", rating: 4.2, tags: ["automl", "keras", "neural"]},
    
    // ==================== DEEP LEARNING ====================
    {name: "TensorFlow", category: "Deep Learning", subcategory: "Framework", desc: "Google's ML framework", url: "tensorflow.org", pricing: "Free", rating: 4.6, tags: ["framework", "google", "production"], featured: true},
    {name: "PyTorch", category: "Deep Learning", subcategory: "Framework", desc: "Meta's ML framework", url: "pytorch.org", pricing: "Free", rating: 4.7, tags: ["framework", "meta", "research"]},
    {name: "Keras", category: "Deep Learning", subcategory: "API", desc: "High-level neural networks", url: "keras.io", pricing: "Free", rating: 4.6, tags: ["high-level", "simple", "tensorflow"]},
    {name: "JAX", category: "Deep Learning", subcategory: "Framework", desc: "Google research framework", url: "jax.readthedocs.io", pricing: "Free", rating: 4.5, tags: ["google", "research", "autograd"]},
    {name: "Flax", category: "Deep Learning", subcategory: "Library", desc: "Neural network library", url: "flax.readthedocs.io", pricing: "Free", rating: 4.3, tags: ["jax", "neural", "google"]},
    {name: "MXNet", category: "Deep Learning", subcategory: "Framework", desc: "Apache deep learning", url: "mxnet.apache.org", pricing: "Free", rating: 4.1, tags: ["apache", "scalable", "aws"]},
    {name: "Caffe", category: "Deep Learning", subcategory: "Framework", desc: "Deep learning framework", url: "caffe.berkeleyvision.org", pricing: "Free", rating: 4.0, tags: ["berkeley", "speed", "legacy"]},
    {name: "Fast.ai", category: "Deep Learning", subcategory: "Library", desc: "Simplified deep learning", url: "fast.ai", pricing: "Free", rating: 4.6, tags: ["simple", "course", "pytorch"]},
    {name: "Detectron2", category: "Deep Learning", subcategory: "Computer Vision", desc: "Object detection by Meta", url: "detectron2.readthedocs.io", pricing: "Free", rating: 4.5, tags: ["detection", "segmentation", "meta"]},
    {name: "YOLO", category: "Deep Learning", subcategory: "Object Detection", desc: "Real-time detection", url: "ultralytics.com", pricing: "Free", rating: 4.6, tags: ["detection", "real-time", "fast"]},
    {name: "OpenCV", category: "Deep Learning", subcategory: "Computer Vision", desc: "Computer vision library", url: "opencv.org", pricing: "Free", rating: 4.6, tags: ["vision", "classic", "comprehensive"]},
    {name: "Albumentations", category: "Deep Learning", subcategory: "Augmentation", desc: "Image augmentation", url: "albumentations.ai", pricing: "Free", rating: 4.5, tags: ["augmentation", "images", "fast"]},
    {name: "Timm", category: "Deep Learning", subcategory: "Models", desc: "PyTorch image models", url: "timm.fast.ai", pricing: "Free", rating: 4.5, tags: ["models", "pretrained", "sota"]},
    {name: "Transformers", category: "Deep Learning", subcategory: "NLP", desc: "Hugging Face transformers", url: "huggingface.co/transformers", pricing: "Free", rating: 4.7, tags: ["nlp", "transformers", "pretrained"]},
    {name: "spaCy", category: "Deep Learning", subcategory: "NLP", desc: "Industrial NLP", url: "spacy.io", pricing: "Free", rating: 4.6, tags: ["nlp", "production", "python"]},
    
    // ==================== DATA ENGINEERING ====================
    {name: "Apache Spark", category: "Data Engineering", subcategory: "Processing", desc: "Unified analytics engine", url: "spark.apache.org", pricing: "Free", rating: 4.6, tags: ["big-data", "processing", "apache"], featured: true},
    {name: "Apache Kafka", category: "Data Engineering", subcategory: "Streaming", desc: "Event streaming platform", url: "kafka.apache.org", pricing: "Free", rating: 4.6, tags: ["streaming", "real-time", "events"]},
    {name: "Apache Flink", category: "Data Engineering", subcategory: "Streaming", desc: "Stream processing", url: "flink.apache.org", pricing: "Free", rating: 4.4, tags: ["streaming", "stateful", "processing"]},
    {name: "dbt", category: "Data Engineering", subcategory: "Transform", desc: "Data transformation", url: "getdbt.com", pricing: "Freemium", rating: 4.6, tags: ["transform", "sql", "analytics"]},
    {name: "Fivetran", category: "Data Engineering", subcategory: "ETL", desc: "Automated data movement", url: "fivetran.com", pricing: "Paid", rating: 4.5, tags: ["etl", "automated", "connectors"]},
    {name: "Airbyte", category: "Data Engineering", subcategory: "ETL", desc: "Open source ETL", url: "airbyte.com", pricing: "Freemium", rating: 4.4, tags: ["etl", "open-source", "connectors"]},
    {name: "Stitch", category: "Data Engineering", subcategory: "ETL", desc: "Simple ETL by Talend", url: "stitchdata.com", pricing: "Freemium", rating: 4.2, tags: ["etl", "simple", "talend"]},
    {name: "Meltano", category: "Data Engineering", subcategory: "ELT", desc: "Open source ELT", url: "meltano.com", pricing: "Free", rating: 4.2, tags: ["elt", "open-source", "singer"]},
    {name: "Great Expectations", category: "Data Engineering", subcategory: "Quality", desc: "Data quality", url: "greatexpectations.io", pricing: "Freemium", rating: 4.4, tags: ["quality", "testing", "validation"]},
    {name: "Monte Carlo", category: "Data Engineering", subcategory: "Observability", desc: "Data observability", url: "montecarlodata.com", pricing: "Paid", rating: 4.3, tags: ["observability", "reliability", "monitoring"]},
    {name: "Atlan", category: "Data Engineering", subcategory: "Catalog", desc: "Active data catalog", url: "atlan.com", pricing: "Paid", rating: 4.4, tags: ["catalog", "governance", "collaboration"]},
    {name: "Alation", category: "Data Engineering", subcategory: "Catalog", desc: "Data intelligence", url: "alation.com", pricing: "Paid", rating: 4.3, tags: ["catalog", "intelligence", "governance"]},
    {name: "Collibra", category: "Data Engineering", subcategory: "Governance", desc: "Data governance", url: "collibra.com", pricing: "Paid", rating: 4.2, tags: ["governance", "catalog", "enterprise"]},
    {name: "Snowflake", category: "Data Engineering", subcategory: "Warehouse", desc: "Cloud data platform", url: "snowflake.com", pricing: "Pay-per-use", rating: 4.6, tags: ["warehouse", "cloud", "sharing"]},
    {name: "Databricks", category: "Data Engineering", subcategory: "Lakehouse", desc: "Lakehouse platform", url: "databricks.com", pricing: "Paid", rating: 4.5, tags: ["lakehouse", "spark", "unified"]},
    
    // ==================== COMPUTER VISION ====================
    {name: "Roboflow", category: "Computer Vision", subcategory: "Platform", desc: "CV developer tools", url: "roboflow.com", pricing: "Freemium", rating: 4.5, tags: ["datasets", "annotation", "deployment"]},
    {name: "V7", category: "Computer Vision", subcategory: "Annotation", desc: "AI data engine", url: "v7labs.com", pricing: "Paid", rating: 4.4, tags: ["annotation", "auto-label", "workflows"]},
    {name: "Labelbox", category: "Computer Vision", subcategory: "Annotation", desc: "Training data platform", url: "labelbox.com", pricing: "Freemium", rating: 4.4, tags: ["annotation", "enterprise", "workflow"]},
    {name: "Scale AI", category: "Computer Vision", subcategory: "Annotation", desc: "Data for AI", url: "scale.com", pricing: "Paid", rating: 4.3, tags: ["annotation", "enterprise", "autonomous"]},
    {name: "Supervisely", category: "Computer Vision", subcategory: "Platform", desc: "CV platform", url: "supervisely.com", pricing: "Freemium", rating: 4.3, tags: ["annotation", "platform", "apps"]},
    {name: "CVAT", category: "Computer Vision", subcategory: "Open Source", desc: "Open annotation tool", url: "cvat.ai", pricing: "Free", rating: 4.3, tags: ["annotation", "open-source", "intel"]},
    {name: "Label Studio", category: "Computer Vision", subcategory: "Open Source", desc: "Data labeling tool", url: "labelstud.io", pricing: "Freemium", rating: 4.4, tags: ["annotation", "open-source", "multi-type"]},
    {name: "Hasty.ai", category: "Computer Vision", subcategory: "Annotation", desc: "AI-assisted labeling", url: "hasty.ai", pricing: "Freemium", rating: 4.2, tags: ["annotation", "ai-assisted", "fast"]},
    {name: "Segments.ai", category: "Computer Vision", subcategory: "Annotation", desc: "Annotation for robotics", url: "segments.ai", pricing: "Freemium", rating: 4.2, tags: ["annotation", "3d", "lidar"]},
    {name: "Clarifai", category: "Computer Vision", subcategory: "Platform", desc: "AI platform", url: "clarifai.com", pricing: "Freemium", rating: 4.2, tags: ["platform", "recognition", "api"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE31 = AI_TOOLS_PHASE31;
}


