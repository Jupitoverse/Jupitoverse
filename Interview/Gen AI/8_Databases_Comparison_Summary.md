# 8. Databases Comparison & Resume Summary

Skills covered: SQL vs NoSQL, when to use which; comparison of SQL, PostgreSQL, SQLite, MongoDB, Vector DB; pros/cons; quick resume summary.

---

## SQL vs NoSQL – When to Use Which

**SQL (Relational)**  
- Model: Tables, rows, columns; fixed schema.  
- ACID: Strong (transactions, integrity).  
- Scale: Vertical + read replicas; sharding possible.  
- Query: Declarative SQL; joins, aggregates.  
- Use cases: OLTP, reporting, relations, integrity.  
- Examples: PostgreSQL, MySQL, SQL Server, SQLite.

**NoSQL**  
- Model: Document, key-value, wide-column, graph; flexible or schema-less.  
- ACID: Varies (e.g. eventual consistency, tunable).  
- Scale: Horizontal scaling common (partition/shard).  
- Query: API/query lang; often no joins or limited.  
- Use cases: High write throughput, flexible schema, cache, graph, search.  
- Examples: MongoDB, Redis, Cassandra, DynamoDB, Neo4j.

When to use SQL:
- Need strong consistency, transactions, and referential integrity.
- Data is relational (many-to-many, foreign keys).
- Complex queries, joins, and reporting.
- Regulatory or audit requirements.

When to use NoSQL:
- Very high write throughput or horizontal scale.
- Schema changes often or flexible/varying structure.
- Cache, session store, or simple key-value.
- Graph (relationships as first-class) or full-text/vector search as primary need.

---

## Comparison of All Database Types (Pros / Cons)

### Relational (SQL)

**General SQL**  
- Pros: ACID, SQL, joins, reporting, ecosystem.  
- Cons: Schema rigidity, scaling writes can be hard.  
- When to use: OLTP, reporting, when relations matter.

**PostgreSQL**  
- Pros: Rich features, JSON, extensions, open source.  
- Cons: Heavier than SQLite; you run/scale it.  
- When to use: Default choice for apps, analytics, JSON + SQL.

**MySQL**  
- Pros: Fast, widely used, replication.  
- Cons: Fewer advanced features than Postgres.  
- When to use: Web apps, when team knows MySQL.

**SQL Server**  
- Pros: Strong on Windows, enterprise tooling.  
- Cons: Licensing, Windows-centric.  
- When to use: Enterprise on Microsoft stack.

**SQLite**  
- Pros: File-based, no server, zero config, embedded.  
- Cons: Single writer, not for high concurrency.  
- When to use: Local/dev, embedded, small apps, scripts.

### NoSQL

**Document (e.g. MongoDB)**  
- Pros: Flexible schema, JSON, horizontal scale.  
- Cons: No joins, consistency tuning.  
- When to use: Content, catalogs, flexible structure.

**Key-Value (e.g. Redis)**  
- Pros: Very fast, in-memory, simple.  
- Cons: Limited query model, persistence options.  
- When to use: Cache, session, rate limit, pub/sub.

**Wide-Column (e.g. Cassandra)**  
- Pros: Write scale, multi-DC.  
- Cons: No joins, query model limited.  
- When to use: Time-series, events, global write scale.

**Graph (e.g. Neo4j)**  
- Pros: Relationships as first-class.  
- Cons: Different model, smaller ecosystem.  
- When to use: Social, recommendations, fraud.

### Vector DB (for RAG / similarity search)

**Vector DB (ChromaDB, Pinecone, Weaviate, Qdrant, pgvector)**  
- Pros: Built for ANN similarity search, scale.  
- Cons: Another system to run/learn; varies by product.  
- When to use: RAG, recommendations, semantic search. See Core Gen AI doc (1_Core_GenAI_RAG_LLM.md) for detailed comparison.

---

## Quick Resume Summary: SQL, PostgreSQL, SQLite, MongoDB, Vector DB

Use these one-liners and bullets on your resume or in interviews.

### SQL

- Proficient in SQL: complex queries, joins (INNER, LEFT), aggregation (GROUP BY, HAVING), subqueries, window functions (ROW_NUMBER, PARTITION BY), and query optimization (indexes, EXPLAIN).
- Experience with relational design: normalization, primary/foreign keys, transactions (ACID), and stored procedures/views where applicable.

### PostgreSQL

- PostgreSQL: development and production use for application data, reporting, and analytics.
- Features used: JSON/JSONB, indexes (B-tree, composite), transactions, connection pooling; optional: pgvector for vector search, partitioning, replication.

### SQLite

- SQLite: embedded and file-based databases for local tools, scripts, prototyping, and small-to-medium single-user or low-concurrency applications.
- Used for: config storage, local caches, ETL staging, and portable apps without a DB server.

### MongoDB

- MongoDB: document store for flexible-schema data, content, and catalogs.
- Experience: CRUD, aggregation pipeline, indexing, and when to use document model vs relational for a given use case.

### Vector DB

- Vector databases (e.g. ChromaDB, Pinecone, pgvector): storing embeddings and running similarity search for RAG, semantic search, and recommendation pipelines.
- Experience: embedding ingestion, index choice, top-K retrieval, and hybrid setups (vector + relational or keyword).

---

## Side-by-Side Resume Cheat Sheet

- **SQL:** SQL for querying, joins, aggregation, window functions, and optimization.
- **PostgreSQL:** PostgreSQL for application and analytics workloads; JSON, indexing, transactions.
- **SQLite:** SQLite for embedded and file-based storage in tools and prototypes.
- **MongoDB:** MongoDB for document storage and flexible-schema use cases.
- **Vector DB:** Vector DBs (ChromaDB / Pinecone / pgvector) for RAG and semantic search.

---

## When to Use Which – Decision Sketch

- Need strict consistency, relations, and reporting → SQL (PostgreSQL or MySQL).
- Single app, local or low concurrency → SQLite.
- Flexible schema, high write throughput, or document-shaped data → MongoDB or similar.
- Cache or session store → Redis (key-value).
- Similarity search, RAG, embeddings → Vector DB (or pgvector if already on Postgres).
- Already on Postgres and need vectors → pgvector before adding another DB.

---

## See Also

- [7_SQL_DBMS_Interview_Guide.md](7_SQL_DBMS_Interview_Guide.md) – SQL & DBMS Q&A
- [1_Core_GenAI_RAG_LLM.md](1_Core_GenAI_RAG_LLM.md) – Vector DB comparison in RAG
- [0_GEN_AI_MASTER_INDEX.md](0_GEN_AI_MASTER_INDEX.md) – Master index
