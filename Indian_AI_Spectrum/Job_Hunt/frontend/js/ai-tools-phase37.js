// AI Tools Database - Phase 37: Database & Data Engineering
// 150+ Database and data tools

const AI_TOOLS_PHASE37 = [
    // ==================== RELATIONAL DATABASES ====================
    {name: "PostgreSQL", category: "Database", subcategory: "Relational", desc: "Advanced open source DB", url: "postgresql.org", pricing: "Free", rating: 4.8, tags: ["open-source", "sql", "reliable"], featured: true},
    {name: "MySQL", category: "Database", subcategory: "Relational", desc: "Popular open source DB", url: "mysql.com", pricing: "Free", rating: 4.6, tags: ["open-source", "sql", "widely-used"]},
    {name: "MariaDB", category: "Database", subcategory: "Relational", desc: "MySQL fork", url: "mariadb.org", pricing: "Free", rating: 4.5, tags: ["open-source", "mysql-compatible", "fork"]},
    {name: "Microsoft SQL Server", category: "Database", subcategory: "Enterprise", desc: "Microsoft database", url: "microsoft.com/sql-server", pricing: "Freemium", rating: 4.5, tags: ["microsoft", "enterprise", "analytics"]},
    {name: "Oracle Database", category: "Database", subcategory: "Enterprise", desc: "Enterprise database", url: "oracle.com/database", pricing: "Paid", rating: 4.4, tags: ["enterprise", "oracle", "mission-critical"]},
    {name: "CockroachDB", category: "Database", subcategory: "Distributed", desc: "Distributed SQL", url: "cockroachlabs.com", pricing: "Freemium", rating: 4.4, tags: ["distributed", "resilient", "scale"]},
    {name: "TiDB", category: "Database", subcategory: "Distributed", desc: "Distributed MySQL", url: "pingcap.com", pricing: "Freemium", rating: 4.3, tags: ["distributed", "mysql-compatible", "htap"]},
    {name: "YugabyteDB", category: "Database", subcategory: "Distributed", desc: "Distributed PostgreSQL", url: "yugabyte.com", pricing: "Freemium", rating: 4.3, tags: ["distributed", "postgres-compatible", "geo"]},
    {name: "PlanetScale", category: "Database", subcategory: "Serverless", desc: "Serverless MySQL", url: "planetscale.com", pricing: "Freemium", rating: 4.5, tags: ["serverless", "mysql", "branching"]},
    {name: "Neon", category: "Database", subcategory: "Serverless", desc: "Serverless Postgres", url: "neon.tech", pricing: "Freemium", rating: 4.4, tags: ["serverless", "postgres", "branching"]},
    {name: "Supabase", category: "Database", subcategory: "BaaS", desc: "Open source Firebase", url: "supabase.com", pricing: "Freemium", rating: 4.6, tags: ["baas", "postgres", "realtime"]},
    {name: "Xata", category: "Database", subcategory: "Serverless", desc: "Serverless database", url: "xata.io", pricing: "Freemium", rating: 4.2, tags: ["serverless", "search", "branches"]},
    {name: "Turso", category: "Database", subcategory: "Edge", desc: "Edge SQLite", url: "turso.tech", pricing: "Freemium", rating: 4.3, tags: ["edge", "sqlite", "libsql"]},
    
    // ==================== NOSQL DATABASES ====================
    {name: "MongoDB", category: "Database", subcategory: "Document", desc: "Document database", url: "mongodb.com", pricing: "Freemium", rating: 4.5, tags: ["document", "nosql", "flexible"], featured: true},
    {name: "Redis", category: "Database", subcategory: "Cache", desc: "In-memory data store", url: "redis.io", pricing: "Freemium", rating: 4.7, tags: ["cache", "fast", "versatile"]},
    {name: "Cassandra", category: "Database", subcategory: "Wide-Column", desc: "Distributed wide-column", url: "cassandra.apache.org", pricing: "Free", rating: 4.3, tags: ["distributed", "scalable", "apache"]},
    {name: "ScyllaDB", category: "Database", subcategory: "Wide-Column", desc: "High-performance Cassandra", url: "scylladb.com", pricing: "Freemium", rating: 4.4, tags: ["performance", "cassandra-compatible", "c++"]},
    {name: "DynamoDB", category: "Database", subcategory: "Key-Value", desc: "AWS NoSQL", url: "aws.amazon.com/dynamodb", pricing: "Pay-per-use", rating: 4.4, tags: ["aws", "serverless", "scalable"]},
    {name: "Couchbase", category: "Database", subcategory: "Document", desc: "Document database", url: "couchbase.com", pricing: "Freemium", rating: 4.2, tags: ["document", "mobile", "sync"]},
    {name: "Firebase Firestore", category: "Database", subcategory: "Document", desc: "Google document DB", url: "firebase.google.com/firestore", pricing: "Freemium", rating: 4.5, tags: ["firebase", "realtime", "mobile"]},
    {name: "CouchDB", category: "Database", subcategory: "Document", desc: "Apache document DB", url: "couchdb.apache.org", pricing: "Free", rating: 4.1, tags: ["apache", "sync", "offline-first"]},
    {name: "Fauna", category: "Database", subcategory: "Serverless", desc: "Serverless document DB", url: "fauna.com", pricing: "Freemium", rating: 4.2, tags: ["serverless", "graphql", "acid"]},
    {name: "RavenDB", category: "Database", subcategory: "Document", desc: "ACID document DB", url: "ravendb.net", pricing: "Freemium", rating: 4.1, tags: ["document", "acid", "dotnet"]},
    {name: "KeyDB", category: "Database", subcategory: "Cache", desc: "Multi-threaded Redis", url: "keydb.dev", pricing: "Free", rating: 4.2, tags: ["redis-compatible", "multi-threaded", "fast"]},
    {name: "Dragonfly", category: "Database", subcategory: "Cache", desc: "Redis alternative", url: "dragonflydb.io", pricing: "Free", rating: 4.3, tags: ["redis-compatible", "fast", "memory-efficient"]},
    
    // ==================== DATA WAREHOUSES ====================
    {name: "Snowflake", category: "Data Warehouse", subcategory: "Cloud", desc: "Cloud data platform", url: "snowflake.com", pricing: "Pay-per-use", rating: 4.6, tags: ["cloud", "scalable", "data-sharing"], featured: true},
    {name: "BigQuery", category: "Data Warehouse", subcategory: "Google", desc: "Google data warehouse", url: "cloud.google.com/bigquery", pricing: "Pay-per-use", rating: 4.6, tags: ["google", "serverless", "ml"]},
    {name: "Amazon Redshift", category: "Data Warehouse", subcategory: "AWS", desc: "AWS data warehouse", url: "aws.amazon.com/redshift", pricing: "Pay-per-use", rating: 4.4, tags: ["aws", "columnar", "scalable"]},
    {name: "Azure Synapse", category: "Data Warehouse", subcategory: "Microsoft", desc: "Microsoft analytics", url: "azure.microsoft.com/synapse-analytics", pricing: "Pay-per-use", rating: 4.3, tags: ["microsoft", "analytics", "spark"]},
    {name: "Databricks", category: "Data Warehouse", subcategory: "Lakehouse", desc: "Unified analytics", url: "databricks.com", pricing: "Pay-per-use", rating: 4.6, tags: ["lakehouse", "spark", "ml"]},
    {name: "ClickHouse", category: "Data Warehouse", subcategory: "OLAP", desc: "Fast OLAP database", url: "clickhouse.com", pricing: "Freemium", rating: 4.5, tags: ["olap", "fast", "columnar"]},
    {name: "Apache Druid", category: "Data Warehouse", subcategory: "OLAP", desc: "Real-time analytics", url: "druid.apache.org", pricing: "Free", rating: 4.3, tags: ["real-time", "olap", "streaming"]},
    {name: "Firebolt", category: "Data Warehouse", subcategory: "Cloud", desc: "Cloud data warehouse", url: "firebolt.io", pricing: "Paid", rating: 4.3, tags: ["cloud", "fast", "sql"]},
    {name: "Apache Pinot", category: "Data Warehouse", subcategory: "OLAP", desc: "Real-time OLAP", url: "pinot.apache.org", pricing: "Free", rating: 4.2, tags: ["real-time", "olap", "linkedin"]},
    {name: "StarRocks", category: "Data Warehouse", subcategory: "OLAP", desc: "MPP database", url: "starrocks.io", pricing: "Free", rating: 4.2, tags: ["olap", "mpp", "mysql-compatible"]},
    
    // ==================== DATA ENGINEERING ====================
    {name: "Apache Spark", category: "Data Engineering", subcategory: "Processing", desc: "Unified analytics engine", url: "spark.apache.org", pricing: "Free", rating: 4.7, tags: ["processing", "ml", "streaming"], featured: true},
    {name: "Apache Kafka", category: "Data Engineering", subcategory: "Streaming", desc: "Event streaming", url: "kafka.apache.org", pricing: "Free", rating: 4.7, tags: ["streaming", "messaging", "events"]},
    {name: "Apache Flink", category: "Data Engineering", subcategory: "Streaming", desc: "Stream processing", url: "flink.apache.org", pricing: "Free", rating: 4.5, tags: ["streaming", "stateful", "real-time"]},
    {name: "Apache Airflow", category: "Data Engineering", subcategory: "Orchestration", desc: "Workflow automation", url: "airflow.apache.org", pricing: "Free", rating: 4.5, tags: ["orchestration", "dag", "scheduling"]},
    {name: "Prefect", category: "Data Engineering", subcategory: "Orchestration", desc: "Modern orchestration", url: "prefect.io", pricing: "Freemium", rating: 4.4, tags: ["orchestration", "python", "modern"]},
    {name: "Dagster", category: "Data Engineering", subcategory: "Orchestration", desc: "Data orchestrator", url: "dagster.io", pricing: "Freemium", rating: 4.4, tags: ["orchestration", "assets", "software-defined"]},
    {name: "dbt", category: "Data Engineering", subcategory: "Transform", desc: "Data transformation", url: "getdbt.com", pricing: "Freemium", rating: 4.6, tags: ["transformation", "sql", "elt"]},
    {name: "Fivetran", category: "Data Engineering", subcategory: "ETL", desc: "Automated data movement", url: "fivetran.com", pricing: "Paid", rating: 4.5, tags: ["etl", "connectors", "automated"]},
    {name: "Airbyte", category: "Data Engineering", subcategory: "ELT", desc: "Open source ELT", url: "airbyte.com", pricing: "Freemium", rating: 4.4, tags: ["elt", "open-source", "connectors"]},
    {name: "Stitch", category: "Data Engineering", subcategory: "ETL", desc: "ETL service", url: "stitchdata.com", pricing: "Freemium", rating: 4.2, tags: ["etl", "simple", "talend"]},
    {name: "Meltano", category: "Data Engineering", subcategory: "ELT", desc: "DataOps platform", url: "meltano.com", pricing: "Free", rating: 4.2, tags: ["elt", "open-source", "singer"]},
];

// Export
if (typeof window !== 'undefined') {
    window.AI_TOOLS_PHASE37 = AI_TOOLS_PHASE37;
}


