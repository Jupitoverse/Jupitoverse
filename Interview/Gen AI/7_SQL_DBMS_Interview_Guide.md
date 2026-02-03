# 7. SQL & DBMS – Interview Guide

Skills covered: SQL queries, joins, aggregation, indexing, transactions, normalization, DBMS concepts.

---

## Quick Reference

| Area | Key Points |
|------|------------|
| DML | SELECT, INSERT, UPDATE, DELETE; WHERE, ORDER BY, LIMIT |
| Joins | INNER, LEFT, RIGHT, FULL; ON condition |
| Aggregation | GROUP BY, HAVING, COUNT, SUM, AVG, MIN, MAX |
| Subqueries | In WHERE, FROM, SELECT; EXISTS, IN, ANY, ALL |
| Indexes | B-tree, composite index; when they help (filter, join, sort) |
| Transactions | ACID, BEGIN, COMMIT, ROLLBACK; isolation levels |
| Normalization | 1NF, 2NF, 3NF; reduce redundancy, avoid anomalies |

---

## Core Concepts

### 1. SELECT and Filtering

- SELECT columns FROM table WHERE condition ORDER BY col LIMIT n.
- DISTINCT for unique rows; AS for aliases.
- Operators: =, <>, <, >, BETWEEN, IN, LIKE (% _), IS NULL.
- AND, OR, NOT; parentheses for precedence.

### 2. Joins

- INNER JOIN: Only matching rows from both tables.
- LEFT JOIN: All from left, match from right; NULL where no match.
- RIGHT JOIN: All from right, match from left.
- FULL OUTER JOIN: All from both; NULL where no match.
- Self-join: Join table to itself (e.g. employee → manager).
- Cross join: Cartesian product (rarely needed).

### 3. Aggregation and GROUP BY

- Aggregate functions: COUNT(*), COUNT(col), SUM, AVG, MIN, MAX.
- GROUP BY column(s): one row per group; non-aggregated columns must be in GROUP BY.
- HAVING: filter groups (after aggregation); WHERE filters rows before aggregation.

### 4. Subqueries

- In WHERE: e.g. WHERE col IN (SELECT col FROM t2), EXISTS (SELECT 1 FROM t2 WHERE ...).
- In FROM: SELECT * FROM (SELECT ...) AS sub.
- In SELECT: scalar subquery (single value); correlated subquery references outer query.

### 5. Indexes

- B-tree index: speeds up WHERE, JOIN, ORDER BY on indexed columns.
- Composite index: (a, b) helps WHERE a=? AND b=? or ORDER BY a, b; order of columns matters.
- Trade-off: faster reads, slower writes and more storage.
- Avoid indexing very low-cardinality columns; consider partial/conditional indexes.

### 6. Transactions

- ACID: Atomicity, Consistency, Isolation, Durability.
- BEGIN; ... statements ...; COMMIT; or ROLLBACK on error.
- Isolation levels: Read Uncommitted, Read Committed, Repeatable Read, Serializable; affect visibility of other transactions' changes.

### 7. Normalization

- 1NF: Atomic values, no repeating groups.
- 2NF: 1NF + no partial dependency (non-key attributes depend on full primary key).
- 3NF: 2NF + no transitive dependency (non-key attributes depend only on primary key).
- Denormalization: sometimes add redundancy for read performance (e.g. reporting).

---

## Common SQL Patterns

```sql
-- Top N per group (e.g. latest order per customer)
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
  FROM orders
) t WHERE rn = 1;

-- Running total
SELECT date, amount, SUM(amount) OVER (ORDER BY date) AS running_total FROM sales;

-- Find duplicates
SELECT col, COUNT(*) FROM t GROUP BY col HAVING COUNT(*) > 1;

-- Exists vs IN (often EXISTS more efficient for large subqueries)
SELECT * FROM a WHERE EXISTS (SELECT 1 FROM b WHERE b.a_id = a.id);
```

---

## Top 20 Interview Q&A – SQL & DBMS

Q1: What is the difference between WHERE and HAVING?
> "WHERE filters rows before aggregation; HAVING filters groups after GROUP BY. Use HAVING for conditions on aggregates (e.g. HAVING COUNT(*) > 1)."

Q2: INNER JOIN vs LEFT JOIN?
> "INNER JOIN returns only rows with matches in both tables. LEFT JOIN returns all rows from the left table and matching rows from the right; NULL where no match. Use LEFT when you want to keep all left rows (e.g. customers with or without orders)."

Q3: What is an index and when do you use one?
> "Index is a structure (e.g. B-tree) that speeds up lookups and sorts on indexed columns. Use on columns in WHERE, JOIN ON, and ORDER BY. Trade-off: faster reads, slower writes, more storage. Don't over-index small or very low-cardinality columns."

Q4: What is a primary key vs unique key?
> "Primary key: unique, not NULL, one per table, often used for clustering. Unique key: unique, can have NULL (depending on DB), can have multiple per table. Both can support foreign key references."

Q5: What is ACID?
> "Atomicity: transaction is all-or-nothing. Consistency: constraints hold after transaction. Isolation: concurrent transactions don't see each other's uncommitted state in bad ways. Durability: committed data survives crashes."

Q6: What is normalization and why use it?
> "Organizing schema to reduce redundancy and update anomalies. 1NF: atomic values. 2NF: no partial dependency on key. 3NF: no transitive dependency. Trade-off: more tables and joins; sometimes denormalize for read performance."

Q7: How do you find the second highest value?
> "ORDER BY col DESC LIMIT 1 OFFSET 1 (or subquery: WHERE col < (SELECT MAX(col) FROM t)). Or use window: ROW_NUMBER() OVER (ORDER BY col DESC) and filter rn=2."

Q8: What is the difference between UNION and UNION ALL?
> "UNION combines result sets and removes duplicates; UNION ALL keeps duplicates. UNION ALL is faster when you know duplicates are OK or don't exist."

Q9: What is a correlated subquery?
> "Subquery that references a column from the outer query. Executed once per outer row. Can often be rewritten as JOIN or window function for better performance."

Q10: What are window functions?
> "Functions over a 'window' of rows (partition, order). Examples: ROW_NUMBER(), RANK(), DENSE_RANK(), SUM() OVER (PARTITION BY ... ORDER BY ...). Don't collapse rows; add computed columns."

Q11: What is a foreign key?
> "Column(s) that reference primary key (or unique key) of another table. Enforces referential integrity; DB can cascade update/delete or restrict. Helps joins and documentation."

Q12: How do you delete duplicate rows (keep one)?
> "Depends on DB. In PostgreSQL: DELETE FROM t a USING t b WHERE a.id < b.id AND a.col = b.col (keep row with smaller id). Or use ctid/rowid. Or SELECT DISTINCT INTO new table and replace."

Q13: What is the difference between COUNT(*) and COUNT(col)?
> "COUNT(*) counts all rows including NULLs. COUNT(col) counts rows where col IS NOT NULL. Use COUNT(*) for total rows; COUNT(col) when you care about non-null values in that column."

Q14: What is a transaction isolation level?
> "Controls what one transaction sees of others' uncommitted or committed changes. Read Uncommitted (dirty reads) to Serializable (strictest). Read Committed is common default; Repeatable Read avoids non-repeatable reads."

Q15: How do you optimize a slow query?
> "Check execution plan (EXPLAIN); add or adjust indexes on filtered/joined/sorted columns; avoid SELECT *; reduce joins or subqueries; consider partitioning or materialized views for heavy aggregates."

Q16: What is a view?
> "Virtual table defined by a SELECT. Simplifies queries and can enforce security. Materialized view: stored result (refreshed periodically) for faster reads at cost of staleness."

Q17: What is the difference between CHAR and VARCHAR?
> "CHAR(n): fixed length, padded; VARCHAR(n): variable length up to n. Use VARCHAR for variable text; CHAR when length is always same (e.g. codes). In many DBs TEXT is for large variable text."

Q18: What is a trigger?
> "Stored procedure that runs automatically on INSERT/UPDATE/DELETE (before or after). Use for audit, derived columns, or complex rules; can make behavior hard to reason about and test."

Q19: What is a stored procedure?
> "Named block of SQL (and procedural code in some DBs) stored in DB. Reduces round-trips, centralizes logic; can be harder to version and test than application code."

Q20: How does SQL relate to RAG/Gen AI?
> "RAG often uses a relational DB for metadata, user data, or logging. SQL skills help: querying for analytics on retrieval quality, storing and querying chunk metadata, or joining vector DB results with relational data in a hybrid pipeline."

---

## Key Talking Points

- SELECT, WHERE, JOINs, GROUP BY, HAVING; subqueries and window functions.
- Indexes: when they help; composite index column order.
- Transactions: ACID, isolation levels.
- Normalization vs denormalization; when to use each.

---

## See Also

- [8_Databases_Comparison_Summary.md](8_Databases_Comparison_Summary.md) – SQL vs NoSQL, DB comparison, resume summary
- [0_GEN_AI_MASTER_INDEX.md](0_GEN_AI_MASTER_INDEX.md) – Master index
