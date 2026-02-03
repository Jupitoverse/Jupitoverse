# CLIPS Outage Report - Manual Testing Guide

**Date**: November 11, 2025  
**Script**: CLIPS_Outage_Report.py

---

## 🎯 Changes Made

### 1. **TEST_MODE Toggle Added**
```python
TEST_MODE = True  # Set to False for production
```
- **True**: Sends email only to test recipients, adds "[TEST MODE]" to subject
- **False**: Sends to all production recipients

### 2. **Connection Resilience**
- Automatic reconnection on connection loss
- Handles `SerializationFailure` and `InterfaceError`
- Retry logic with configurable attempts (default: 3)

### 3. **Enhanced Error Handling**
- Each batch retries up to 3 times before skipping
- Detailed logging for each retry attempt
- Connection health check before each batch

### 4. **Configuration Section**
All configurable parameters in one place:
- `TEST_MODE`: Enable/disable test mode
- `PART_IDS_BATCH_SIZE`: 20 (adjustable)
- `SPEC_IDS_BATCH_SIZE`: 50 (adjustable)
- `MAX_RETRIES`: 3 (adjustable)
- `RETRY_DELAY`: 2 seconds (adjustable)

---

## 🔍 Manual Testing Queries

### **Query 1: Test Activity Summary (Single Part ID)**

Test if basic query works for a single partition:

```sql
-- Test Query 1: Activity Summary for part_id 1
SELECT ord.entity_name AS "Activity Name",
       oai.spec_ver_id AS "Spec Id",
       aocd.interface AS Interface,
       SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '1 hour' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS "Last 1 Hour",
       SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '2 hours' AND oai.actual_start_date < NOW() - INTERVAL '1 hour' THEN 1 ELSE 0 END) AS "Previous 1 Hour",
       SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '12 hours' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS "Last 12 Hours",
       SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '1 day' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS "Last 24 Hours",
       SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '2 days' AND oai.actual_start_date < NOW() - INTERVAL '1 day' THEN 1 ELSE 0 END) AS "Previous 24 Hours",
       SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '7 days' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS "Last 1 Week",
       SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '1 month' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS "Last 1 Month",
       SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '1 year' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS "Last 1 Year"
FROM ossdb01db.oss_activity_instance oai
JOIN ossdb01ref.oss_ref_attribute ora ON oai.spec_ver_id = ora.attribute_value
JOIN ossdb01ref.oss_ref_data ord ON ora.entity_id = ord.entity_id
JOIN ossdb01db.activity_overview_custom_data aocd ON oai.spec_ver_id = aocd.spec_id
WHERE oai.part_id IN (1)  -- Test with single part_id
  AND oai.last_update_date > NOW() - INTERVAL '1 year'
  AND oai.state IN ('In Progress', 'Rework In Progress')
  AND oai.is_latest_version = 1
  AND oai.implementation_type <> 'Manual'
  AND aocd.interface IN ('ARM','ASD')
GROUP BY ord.entity_name, oai.spec_ver_id, aocd.interface
ORDER BY "Last 1 Hour" DESC, "Last 12 Hours" DESC, "Last 24 Hours" DESC
LIMIT 10;
```

**Expected Result**: Should return 0-10 rows with activity counts

---

### **Query 2: Count Total Stuck Activities**

Quick count to see if there are any stuck activities:

```sql
-- Count of stuck activities by interface
SELECT aocd.interface AS Interface,
       COUNT(*) AS "Total Stuck Activities"
FROM ossdb01db.oss_activity_instance oai
JOIN ossdb01db.activity_overview_custom_data aocd ON oai.spec_ver_id = aocd.spec_id
WHERE oai.part_id BETWEEN 1 AND 99
  AND oai.last_update_date > NOW() - INTERVAL '1 year'
  AND oai.state IN ('In Progress', 'Rework In Progress')
  AND oai.is_latest_version = 1
  AND oai.implementation_type <> 'Manual'
  AND aocd.interface IN ('ARM','ASD')
GROUP BY aocd.interface
ORDER BY "Total Stuck Activities" DESC;
```

**Expected Result**: 
```
Interface | Total Stuck Activities
----------|----------------------
ARM       | 150
ASD       | 75
```

---

### **Query 3: Test Detailed Query (Simplified)**

Test if the CTE and joins work correctly:

```sql
-- Simplified detailed query for testing
WITH filtered_projects AS (
    SELECT 
        spoi.id,
        spoi.name,
        spoi.status,
        spoi.plan_id,
        spoi.objid,
        MAX(CASE WHEN oas.code = 'customerID' THEN oas.value END) as customer_id,
        MAX(CASE WHEN oas.code = 'siteId' THEN oas.value END) as site_id,
        MAX(CASE WHEN oas.code = 'DMD_PTD' THEN oas.value END) as PTD
    FROM ossdb01db.sc_project_order_instance spoi
    LEFT JOIN ossdb01db.oss_attribute_store oas 
        ON oas.parent_id = spoi.objid 
        AND oas.code IN ('customerID', 'siteId', 'DMD_PTD')
    WHERE spoi.is_latest_version = 1
      AND spoi.manager IS DISTINCT FROM 'ProductionSanity'
      AND spoi.name NOT LIKE '%MM_PROD_TEST%'
      AND spoi.status NOT LIKE 'FCANCELLED'
    GROUP BY spoi.id, spoi.name, spoi.status, spoi.plan_id, spoi.objid
    LIMIT 1000  -- Limit for testing
)
SELECT 
    fp.id as projectid,
    fp.customer_id,
    fp.site_id,
    fp.PTD,
    o1.entity_name,
    fp.name,
    oai.last_update_date,
    oai.create_date,
    oai.status,
    fp.status as project_status,
    oai.id as activity_id,
    EXTRACT(EPOCH FROM (NOW() - oai.last_update_date)) / 3600 as age_hours
FROM ossdb01db.oss_activity_instance oai
INNER JOIN ossdb01ref.oss_ref_attribute o2 
    ON o2.attribute_value = oai.spec_ver_id
INNER JOIN ossdb01ref.oss_ref_data o1 
    ON o1.entity_id = o2.entity_id
INNER JOIN filtered_projects fp 
    ON fp.plan_id = oai.plan_id
WHERE oai.part_id IN (1, 2, 3, 4, 5)  -- Test with few part_ids
  AND oai.state IN ('In Progress', 'Rework In Progress')
  AND oai.is_latest_version = 1
ORDER BY age_hours DESC
LIMIT 10;
```

**Expected Result**: Should return 0-10 detailed activity records

---

### **Query 4: Check if spec_ver_ids exist in both queries**

Verify that spec_ver_ids from Query 1 have matching data for Query 2:

```sql
-- Step 1: Get sample spec_ver_ids from Query 1
WITH stuck_activities AS (
    SELECT DISTINCT oai.spec_ver_id
    FROM ossdb01db.oss_activity_instance oai
    JOIN ossdb01db.activity_overview_custom_data aocd ON oai.spec_ver_id = aocd.spec_id
    WHERE oai.part_id IN (1, 2, 3)
      AND oai.last_update_date > NOW() - INTERVAL '1 year'
      AND oai.state IN ('In Progress', 'Rework In Progress')
      AND oai.is_latest_version = 1
      AND oai.implementation_type <> 'Manual'
      AND aocd.interface IN ('ARM','ASD')
    LIMIT 5
)
-- Step 2: Check if these spec_ver_ids have matching activities with projects
SELECT 
    sa.spec_ver_id,
    COUNT(DISTINCT oai.id) as activity_count,
    COUNT(DISTINCT spoi.id) as project_count
FROM stuck_activities sa
LEFT JOIN ossdb01db.oss_activity_instance oai 
    ON oai.spec_ver_id = sa.spec_ver_id
    AND oai.is_latest_version = 1
LEFT JOIN ossdb01db.sc_project_order_instance spoi 
    ON spoi.plan_id = oai.plan_id
    AND spoi.is_latest_version = 1
GROUP BY sa.spec_ver_id;
```

**Expected Result**:
```
spec_ver_id                          | activity_count | project_count
-------------------------------------|----------------|---------------
f1f62e0d-6f07-4c0c-be12-631e07b7448f | 5              | 5
3936695f-90a1-4e79-8a60-1b460fcf26b4 | 3              | 3
```

---

### **Query 5: Diagnostic - Why Query 2 Returns No Results**

Find out why the detailed query might be returning 0 results:

```sql
-- Diagnostic query to understand the mismatch
WITH stuck_activities AS (
    SELECT DISTINCT 
        oai.spec_ver_id,
        oai.plan_id,
        oai.part_id
    FROM ossdb01db.oss_activity_instance oai
    JOIN ossdb01db.activity_overview_custom_data aocd ON oai.spec_ver_id = aocd.spec_id
    WHERE oai.part_id IN (1, 2, 3)
      AND oai.last_update_date > NOW() - INTERVAL '1 year'
      AND oai.state IN ('In Progress', 'Rework In Progress')
      AND oai.is_latest_version = 1
      AND oai.implementation_type <> 'Manual'
      AND aocd.interface IN ('ARM','ASD')
    LIMIT 10
)
SELECT 
    sa.spec_ver_id,
    sa.plan_id,
    sa.part_id,
    CASE WHEN spoi.id IS NOT NULL THEN 'YES' ELSE 'NO' END as has_project,
    CASE WHEN spoi.manager = 'ProductionSanity' THEN 'FILTERED' ELSE 'OK' END as manager_check,
    CASE WHEN spoi.name LIKE '%MM_PROD_TEST%' THEN 'FILTERED' ELSE 'OK' END as name_check,
    CASE WHEN spoi.status LIKE 'FCANCELLED' THEN 'FILTERED' ELSE 'OK' END as status_check,
    spoi.status as project_status
FROM stuck_activities sa
LEFT JOIN ossdb01db.sc_project_order_instance spoi 
    ON spoi.plan_id = sa.plan_id
    AND spoi.is_latest_version = 1;
```

**Expected Result**: Shows why each activity is included/excluded from Query 2

---

### **Query 6: Test Connection Resilience**

Test if connection can handle long-running queries:

```sql
-- Long-running query to test connection stability
SELECT 
    COUNT(*) as total_activities,
    COUNT(DISTINCT spec_ver_id) as unique_specs,
    COUNT(DISTINCT plan_id) as unique_plans
FROM ossdb01db.oss_activity_instance oai
WHERE oai.part_id BETWEEN 1 AND 99
  AND oai.last_update_date > NOW() - INTERVAL '1 year'
  AND oai.state IN ('In Progress', 'Rework In Progress')
  AND oai.is_latest_version = 1;
```

**Expected Result**: Should complete without connection errors

---

## 📊 Summary Table for Manual Testing

| Test | Query | Purpose | Expected Result |
|------|-------|---------|-----------------|
| 1 | Activity Summary (Single Part) | Test basic query | 0-10 rows |
| 2 | Count Stuck Activities | Verify data exists | Count by interface |
| 3 | Simplified Detailed Query | Test CTE and joins | 0-10 detailed records |
| 4 | Spec Ver ID Match | Verify data linkage | Match counts |
| 5 | Diagnostic Query | Find mismatch reasons | Filter analysis |
| 6 | Connection Test | Test stability | Total counts |

---

## 🐛 Troubleshooting the Error

### **Error Analysis:**

```
SerializationFailure: terminating connection due to conflict with recovery
DETAIL: User query might have needed to see row versions that must be removed.
HINT: In a moment you should be able to reconnect to the database and repeat your command.
SSL connection has been closed unexpectedly
```

**Root Cause**: PostgreSQL hot standby conflict - the read replica is removing old row versions that your query needs.

**Solutions Implemented:**

1. **Automatic Reconnection**: Script now reconnects automatically
2. **Retry Logic**: Each batch retries up to 3 times
3. **Connection Health Check**: Verifies connection before each batch
4. **Smaller Batches**: Reduces query execution time

### **Additional Recommendations:**

1. **Reduce Batch Sizes** (if errors persist):
```python
PART_IDS_BATCH_SIZE = 10  # Reduce from 20
SPEC_IDS_BATCH_SIZE = 25  # Reduce from 50
```

2. **Increase Retry Delay**:
```python
RETRY_DELAY = 5  # Increase from 2 seconds
```

3. **Use Primary Database** (if available):
```python
DB_CONFIG = {
    'host': 'primary-db-host',  # Instead of read replica
    ...
}
```

4. **Add Query Timeout**:
```python
cursor.execute("SET statement_timeout = '60s'")  # 60 second timeout
```

---

## ✅ Testing Checklist

- [ ] Run Query 1 (Activity Summary) manually
- [ ] Run Query 2 (Count Stuck Activities) manually
- [ ] Run Query 3 (Simplified Detailed) manually
- [ ] Run Query 4 (Spec Ver ID Match) manually
- [ ] Run Query 5 (Diagnostic) manually
- [ ] Run Query 6 (Connection Test) manually
- [ ] Set `TEST_MODE = True` in script
- [ ] Run script and verify Excel file created
- [ ] Check log file for errors
- [ ] Verify email is prepared (not sent in test mode)
- [ ] Set `TEST_MODE = False` for production
- [ ] Monitor first production run

---

## 📝 Configuration for Production

```python
# Production settings
TEST_MODE = False
PART_IDS_BATCH_SIZE = 20
SPEC_IDS_BATCH_SIZE = 50
MAX_RETRIES = 3
RETRY_DELAY = 2
```

---

**Last Updated**: November 11, 2025  
**Author**: Abhishek Agrahari


