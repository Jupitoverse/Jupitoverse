# ✅ Final Fix: Using Exact Working Query

## What Changed

Replaced the modified query with the **EXACT working query** from your shell script, with only one change: **batching part_id values in groups of 10**.

---

## 🔧 The Approach

### ✅ What We Kept (Unchanged)
- **Exact SQL query structure** from shell script
- **Comma-separated FROM clause** (not JOIN syntax)
- **All WHERE conditions** exactly as they were
- **All spec_ver_id values** in the IN clause
- **All table references** (spoi, oai, o1, o2, oas, etc.)
- **All column names** and aliases

### ✨ What We Changed (Only This)
```python
# OLD: Single query with all part_ids
WHERE oai.part_id in(1,2,3,...,99)

# NEW: 10 queries with batches of 10 part_ids each
Batch 1: WHERE oai.part_id in(1,2,3,4,5,6,7,8,9,10)
Batch 2: WHERE oai.part_id in(11,12,13,14,15,16,17,18,19,20)
...
Batch 10: WHERE oai.part_id in(91,92,93,94,95,96,97,98,99)
```

---

## 📊 How It Works

```python
# 1. Generate all part_ids (1-99)
all_part_ids = [1, 2, 3, ..., 99]

# 2. Split into batches of 10
Batch 1: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Batch 2: [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
...
Batch 10: [91, 92, 93, 94, 95, 96, 97, 98, 99]

# 3. Execute query for each batch
for batch in batches:
    query = "...WHERE oai.part_id in({batch})..."
    results = execute(query)
    all_results.extend(results)

# 4. Combine all results into DataFrame
df = pd.DataFrame(all_results)
```

---

## ✅ Benefits

1. **No Timeout** - Smaller queries complete faster
2. **Exact Query** - Using proven working query
3. **Complete Data** - All part_ids (1-99) covered
4. **Simple** - Just batching, no other changes
5. **Reliable** - No parameter binding issues

---

## 📝 Query Execution

The script now executes **10 queries** sequentially:

```
Query 1:  part_id in(1,2,3,4,5,6,7,8,9,10)
Query 2:  part_id in(11,12,13,14,15,16,17,18,19,20)
Query 3:  part_id in(21,22,23,24,25,26,27,28,29,30)
Query 4:  part_id in(31,32,33,34,35,36,37,38,39,40)
Query 5:  part_id in(41,42,43,44,45,46,47,48,49,50)
Query 6:  part_id in(51,52,53,54,55,56,57,58,59,60)
Query 7:  part_id in(61,62,63,64,65,66,67,68,69,70)
Query 8:  part_id in(71,72,73,74,75,76,77,78,79,80)
Query 9:  part_id in(81,82,83,84,85,86,87,88,89,90)
Query 10: part_id in(91,92,93,94,95,96,97,98,99)
```

Each query is **fast** because it only processes 10 part_ids instead of all 99.

---

## 📦 Complete Query (Exact from Shell Script)

```sql
select spoi.id as projectid,
       oas.value as customer_id,
       oas2.value as site_id,
       oas4.value as projectOwnerName,
       oas5.value as siteName,
       oas6.value as PTD,
       o1.entity_name,
       spoi.name,
       oai.last_update_date,
       oai.create_date,
       oai.status,
       spoi.status,
       oai.id as activity_id 
from ossdb01db.sc_project_order_instance spoi,
     ossdb01db.oss_activity_instance oai,
     ossdb01ref.oss_ref_data o1,
     ossdb01ref.oss_ref_attribute o2,
     ossdb01db.oss_attribute_store oas,
     ossdb01db.oss_attribute_store oas2,
     ossdb01db.oss_attribute_store oas4,
     ossdb01db.oss_attribute_store oas5,
     ossdb01db.oss_attribute_store oas6 
where oai.part_id in(BATCH_OF_10)  -- Only change: batch values
      and oai.implementation_type = 'Manual' 
      and oai.spec_ver_id in('5bf0536f-4798-4674-b811-f0c40cd9f967',
                              '800f1e6c-a19d-4851-8c33-caf6df02e7fb',
                              'e7cd1c8f-f778-4e6d-aa2b-43240bce64d4',
                              '234487e7-7dfa-4f09-a7db-6de805f7ff23',
                              '6e9c8fb9-078e-4711-baee-cd31a4dfed61',
                              '1e1f81de-aea5-4f1c-a621-8daed5a11842',
                              '93d43aae-8e7b-4950-a358-1c302bb948a6',
                              'f8dec3e6-143b-49db-b0a3-3f2362ffc20a',
                              'fa571a98-8774-45a5-9f43-d7f557385333',
                              '800f1e6c-a19d-4851-8c33-caf6df02e7fb') 
      and oai.state in ('In Progress', 'Rework In Progress')
      and oai.last_update_date < current_date - interval '30' day 
      and spoi.plan_id = oai.plan_id 
      and spoi.manager is distinct from 'ProductionSanity' 
      and oai.is_latest_version = 1 
      and spoi.is_latest_version = 1 
      and spoi.name not like '%MM_PROD_TEST%'
      and spoi.status not like 'FCANCELLED' 
      and o2.attribute_value = oai.spec_ver_id 
      and o1.entity_id = o2.entity_id 
      and oas.parent_id = spoi.objid 
      and oas2.parent_id = spoi.objid 
      and oas4.parent_id = spoi.objid 
      and oas5.parent_id = spoi.objid 
      and oas6.parent_id = spoi.objid 
      and oas.code like 'customerID' 
      and oas2.code like 'siteId' 
      and oas4.code like 'projectOwnerName' 
      and oas5.code like 'siteName' 
      and oas6.code like 'DMD_PTD'
```

---

## 📊 Sample Log Output

```
2024-10-20 10:00:01 - INFO - Starting to fetch pending tasks...
2024-10-20 10:00:01 - INFO - Processing 99 part_ids in batches of 10
2024-10-20 10:00:02 - INFO - Executing query for part_id batch: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
2024-10-20 10:00:03 - INFO - Fetched 15 records for part_id batch [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
2024-10-20 10:00:04 - INFO - Executing query for part_id batch: [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
2024-10-20 10:00:05 - INFO - Fetched 22 records for part_id batch [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
...
2024-10-20 10:01:00 - INFO - Total records fetched: 234
2024-10-20 10:01:01 - INFO - Successfully created DataFrame from query results
```

---

## ✅ Everything Else Unchanged

- ✅ Excel export working
- ✅ HTML report generation
- ✅ Email with attachments
- ✅ Comprehensive logging
- ✅ Automatic cleanup
- ✅ All 13 recipients
- ✅ Execution frequency (every 5 days)

---

## 🎯 Why This Works

1. **Proven Query** - Using your exact working query
2. **Small Batches** - 10 part_ids per query = fast execution
3. **No JOIN Changes** - Kept original comma-separated FROM
4. **No Parameter Issues** - Direct string interpolation for part_ids
5. **Complete Coverage** - All 99 part_ids processed

---

## 🚀 Ready to Deploy

The file `checkUserPendingTask_converted.py` is ready with:
- ✅ Exact working query
- ✅ Part_id batching (10 per query)
- ✅ Excel export
- ✅ HTML report
- ✅ Email attachments
- ✅ No linting errors
- ✅ Production configuration

Just run it:
```bash
python checkUserPendingTask_converted.py
```

---

**Updated**: October 20, 2024  
**Status**: ✅ PRODUCTION READY  
**Query**: Exact from shell script + batching















