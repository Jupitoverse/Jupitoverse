# Query Timeout Protection - Documentation

## Overview

The OSO_Service_Activated.py script now includes **automatic query timeout protection** to prevent long-running queries from impacting the database.

---

## Configuration

### Timeout Settings (Top of Script)

```python
# Query Timeout Settings (Safety mechanism to prevent long-running queries)
QUERY_TIMEOUT_SECONDS = 300  # 5 minutes - abort query if it takes longer
ENABLE_QUERY_TIMEOUT = True  # Set to False to disable timeout
```

### Default Configuration

- **Default Timeout**: 300 seconds (5 minutes)
- **Status**: ENABLED by default
- **Applies to**: All database queries (SELECT, INSERT, UPDATE)

---

## How It Works

### 1. Connection Level Timeout

When a database connection is established:

```python
SET statement_timeout = 300000  # 300 seconds = 300,000 milliseconds
```

This PostgreSQL setting automatically cancels any query that runs longer than the specified time.

### 2. Automatic Query Cancellation

If a query exceeds the timeout:
- PostgreSQL **automatically aborts** the query
- Script catches `QueryCanceledError` exception
- Logs the timeout event
- Displays user-friendly error message
- **Prevents database impact** from runaway queries

### 3. Graceful Handling

**For SELECT queries (data fetching):**
- Query is aborted
- Returns None
- Script exits cleanly
- No data corruption

**For INSERT queries (data insertion):**
- Query is aborted
- Already inserted records are **committed**
- Remaining records are skipped
- Partial success is logged
- No data loss

---

## Example Scenarios

### Scenario 1: Query Takes Too Long (SELECT)

```
2025-01-27 10:30:15 - INFO - Executing query...
2025-01-27 10:30:15 - INFO - Query timeout set to 300 seconds
2025-01-27 10:35:16 - ERROR - Query exceeded timeout limit of 300 seconds
2025-01-27 10:35:16 - ERROR - The query was automatically aborted to prevent database impact

[ERROR] Query Timeout!
The query took longer than 300 seconds and was aborted.

Recommendations:
  1. Check if database is under heavy load
  2. Consider increasing QUERY_TIMEOUT_SECONDS in script
  3. Review query optimization (see QUERY_OPTIMIZATION_ANALYSIS.md)
  4. Contact DBA to check database performance
```

**Result**: Script exits safely, no database impact

---

### Scenario 2: Insert Operation Times Out

```
2025-01-27 10:40:00 - INFO - Processing 500 records...
2025-01-27 10:40:15 - INFO - Committed batch: 100 records inserted so far...
2025-01-27 10:40:30 - INFO - Committed batch: 200 records inserted so far...
2025-01-27 10:45:01 - ERROR - Insert timeout on row 250
2025-01-27 10:45:01 - WARNING - Committing already inserted records before aborting...

[WARNING] Insert operation timed out after 250 records
Successfully inserted: 250 records
Remaining records were not processed to prevent database impact
```

**Result**: 250 records inserted successfully, script continues to email step

---

## Configuration Options

### Option 1: Standard Protection (Default)

```python
QUERY_TIMEOUT_SECONDS = 300  # 5 minutes
ENABLE_QUERY_TIMEOUT = True
```

**Use when:**
- Running in production
- Want to protect database from long queries
- Standard operational mode

---

### Option 2: Extended Timeout

```python
QUERY_TIMEOUT_SECONDS = 600  # 10 minutes
ENABLE_QUERY_TIMEOUT = True
```

**Use when:**
- Query is known to take 5-10 minutes
- Database is slower than usual
- Processing large datasets
- During maintenance windows

---

### Option 3: No Timeout (Use with Caution!)

```python
QUERY_TIMEOUT_SECONDS = 300
ENABLE_QUERY_TIMEOUT = False  # Disabled
```

**Use when:**
- Running in development/test environment
- Need to measure actual query time
- Database maintenance mode
- **NOT recommended for production**

---

### Option 4: Quick Timeout (Testing)

```python
QUERY_TIMEOUT_SECONDS = 60  # 1 minute
ENABLE_QUERY_TIMEOUT = True
```

**Use when:**
- Testing timeout functionality
- Quick validation runs
- Ensuring queries are fast enough

---

## Benefits

### 1. Database Protection ✅

**Before Timeout Protection:**
- Long query runs indefinitely
- Locks database resources
- Impacts other applications
- Requires manual intervention

**After Timeout Protection:**
- Query auto-aborts after 5 minutes
- Resources released automatically
- No manual intervention needed
- Database performance protected

---

### 2. Early Problem Detection ✅

If timeout occurs repeatedly:
- Indicates query performance issues
- Alerts you to database problems
- Prompts optimization review
- Prevents production incidents

---

### 3. Safe Failure Mode ✅

When timeout occurs:
- No data corruption
- Clean error messages
- Logged for investigation
- Partial inserts are committed

---

## Monitoring Timeout Events

### Check Logs

```bash
# Search for timeout events in logs
grep -i "timeout" script_log.txt
grep -i "Query exceeded" script_log.txt
grep -i "QueryCanceledError" script_log.txt
```

### Database Side

```sql
-- Check PostgreSQL logs for canceled queries
SELECT * FROM pg_stat_activity 
WHERE state = 'idle in transaction (aborted)';

-- Check long-running queries
SELECT 
    pid,
    now() - query_start as duration,
    query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;
```

---

## Troubleshooting

### Problem: Query Times Out Frequently

**Symptoms:**
- Script fails with timeout error every run
- Query consistently takes > 5 minutes

**Solutions:**

1. **Increase Timeout** (Quick fix)
   ```python
   QUERY_TIMEOUT_SECONDS = 600  # 10 minutes
   ```

2. **Optimize Query** (Recommended)
   - Run `create_indexes.sql` to add missing indexes
   - Review `QUERY_OPTIMIZATION_ANALYSIS.md`
   - Check database load during execution

3. **Check Database Health**
   - Contact DBA to check database performance
   - Review database locks and blocking queries
   - Check disk I/O and CPU usage

4. **Schedule During Off-Peak**
   - Run script during low-traffic hours
   - Avoid peak database usage times

---

### Problem: Insert Operation Times Out

**Symptoms:**
- Insert completes partially
- Timeout occurs mid-insertion

**Solutions:**

1. **Reduce Batch Size**
   ```python
   # In insert_new_records function
   if inserted_count % 50 == 0:  # Changed from 100
       connection.commit()
   ```

2. **Process in Chunks**
   - Split large datasets into smaller runs
   - Process incrementally over multiple executions

3. **Check Write Performance**
   - Verify database has adequate IOPS
   - Check for index overhead on write operations

---

### Problem: Timeout Disabled but Queries Still Cancel

**Symptoms:**
- `ENABLE_QUERY_TIMEOUT = False`
- Queries still timing out

**Possible Causes:**

1. **Database-level timeout set**
   ```sql
   -- Check database timeout settings
   SHOW statement_timeout;  -- If not 0, database has timeout
   ```

2. **Connection pooler timeout**
   - PgBouncer or connection pooler has its own timeout

3. **Network timeout**
   - Firewall or load balancer has connection timeout

---

## Performance Impact

### Timeout Check Overhead

**Impact**: Negligible (< 1ms per query)

The `SET statement_timeout` command:
- Executes once per connection
- No per-query overhead
- PostgreSQL-native feature
- Highly efficient

### When Timeout Triggers

**Database Side:**
- Query is canceled immediately
- Resources are released
- Connection remains usable
- No data corruption

**Application Side:**
- Exception is caught
- Clean shutdown
- Logs written
- Exit gracefully

---

## Best Practices

### 1. Always Enable in Production ✅

```python
ENABLE_QUERY_TIMEOUT = True  # Always in production
```

### 2. Set Reasonable Timeout ✅

```python
# Too short: frequent false alarms
QUERY_TIMEOUT_SECONDS = 30  # Bad

# Reasonable: allows normal operation, catches problems
QUERY_TIMEOUT_SECONDS = 300  # Good (5 minutes)

# Too long: defeats purpose
QUERY_TIMEOUT_SECONDS = 3600  # Bad (1 hour)
```

### 3. Monitor and Adjust ✅

- Review logs weekly
- If timeouts occur, investigate
- Adjust timeout based on actual performance
- Document any changes

### 4. Combine with Optimization ✅

```
Timeout Protection + Query Optimization = Best Performance
```

- Use timeout as safety net
- Also implement index optimizations
- Monitor query performance
- Continuous improvement

---

## Testing Timeout Functionality

### Test 1: Verify Timeout is Set

```python
# Add this temporarily to test
import psycopg2
conn = psycopg2.connect(...)
cursor = conn.cursor()
cursor.execute("SHOW statement_timeout;")
print(cursor.fetchone())  # Should show: 300000 (or your value)
```

### Test 2: Simulate Timeout

```sql
-- Add this to query temporarily (DO NOT USE IN PRODUCTION)
SELECT pg_sleep(400), * FROM ...  -- Sleeps 400 seconds, will timeout at 300
```

### Test 3: Check Error Handling

```bash
# Run with short timeout
QUERY_TIMEOUT_SECONDS = 10  # Set to 10 seconds
python OSO_Service_Activated.py --dry-run

# Verify timeout error is caught and logged properly
```

---

## Summary

### Key Features

- ✅ **Automatic timeout protection** at connection level
- ✅ **Configurable timeout** via simple variable
- ✅ **Graceful error handling** with detailed messages
- ✅ **Partial insert commit** prevents data loss
- ✅ **Zero overhead** when not timing out
- ✅ **Enable/disable toggle** for flexibility

### Default Settings

```python
QUERY_TIMEOUT_SECONDS = 300      # 5 minutes
ENABLE_QUERY_TIMEOUT = True       # Enabled
```

### Recommendation

**Keep timeout enabled in production** with a reasonable value (5-10 minutes).

This protects your database while allowing normal operations to complete successfully.

---

## Related Documentation

- **QUERY_OPTIMIZATION_ANALYSIS.md** - Query optimization guide
- **create_indexes.sql** - Index creation scripts
- **OPTIMIZATION_SUMMARY.txt** - Quick optimization reference

---

**Author**: Abhishek  
**Date**: 2025-01-27  
**Version**: 2.1 (with Timeout Protection)


