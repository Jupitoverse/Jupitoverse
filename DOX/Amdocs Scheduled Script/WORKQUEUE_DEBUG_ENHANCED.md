# 🔍 Enhanced WorkQueue Debugging

## Changes Made

I've significantly enhanced the WorkQueue fetching logic with detailed logging to help identify why WorkQueues are not being retrieved.

---

## What's New

### 1. More Explicit Row Selection ✅

**OLD Approach:**
```python
entity_spec_map = df.groupby('Entity Name')['Activity ID'].first().to_dict()
```

**NEW Approach:**
```python
# For each unique Entity Name, get one row explicitly
for entity_name in unique_entities:
    # Get all rows for this entity name
    entity_rows = df[df['Entity Name'] == entity_name]
    
    # Take the first row's activity_id
    first_row = entity_rows.iloc[0]
    activity_id = first_row['Activity ID']
    
    # Fetch workqueue using this activity_id
    workqueue = fetch_workqueue(cursor, activity_id)
```

**Benefits:**
- More explicit and clear
- Better visibility of what's happening
- Easier to debug

---

### 2. Comprehensive Logging ✅

The script now logs:

#### Step 1: Task Discovery
```
Fetching WorkQueue for main table...
============================================================
Found 8 unique entity names (tasks)
```

#### Step 2: For Each Task
```
Processing: Create RMA in NetX
  - Found 45 rows for this task
  - Taking Activity ID: 123456789
    → Querying WorkQueue for activity_id: 123456789
    ✓ Found WorkQueue: Production-Queue
  - WorkQueue Result: Production-Queue
```

#### Step 3: Mapping Results
```
Mapping WorkQueues to all rows...
============================================================
✓ WorkQueue column added to main table
  WorkQueue mapping summary:
    Create RMA in NetX: Production-Queue (applied to 45 rows)
    Modify Service Order: Billing-Team (applied to 32 rows)
    ...
============================================================
```

---

### 3. Enhanced Debugging in fetch_workqueue() ✅

When a WorkQueue is **NOT** found, the function now:

1. **Logs the issue:**
   ```
   ✗ No WorkQueue found in database
   ```

2. **Checks if activity_id exists:**
   ```sql
   select count(*) 
   from act_ru_variable 
   where text_ = %s and name_ = 'activityId'
   ```

3. **Reports findings:**
   ```
   → Debug: Found 0 rows with activityId=123456789 in act_ru_variable
   → This activity_id doesn't exist in act_ru_variable table!
   ```

This helps identify if:
- The activity_id doesn't exist in the database
- The activity_id exists but has no WorkQueue
- There's a data format issue

---

## The Query Being Used

```sql
select text_ 
from act_ru_variable 
where task_id_ in (
    select task_id_ 
    from act_ru_variable arv 
    where text_ = %s 
    and name_ = 'activityId'
) 
and name_ in ('WorkQueue')
```

Where `%s` = the activity_id (oai.id) from your data

---

## Log Output Examples

### Success Case:
```
Fetching WorkQueue for main table...
============================================================
Found 8 unique entity names (tasks)

Processing: Create RMA in NetX
  - Found 45 rows for this task
  - Taking Activity ID: 123456789
    → Querying WorkQueue for activity_id: 123456789
    ✓ Found WorkQueue: Production-Queue
  - WorkQueue Result: Production-Queue

Processing: Modify Service Order
  - Found 32 rows for this task
  - Taking Activity ID: 987654321
    → Querying WorkQueue for activity_id: 987654321
    ✓ Found WorkQueue: Billing-Team
  - WorkQueue Result: Billing-Team

...

Mapping WorkQueues to all rows...
============================================================
✓ WorkQueue column added to main table
  WorkQueue mapping summary:
    Create RMA in NetX: Production-Queue (applied to 45 rows)
    Modify Service Order: Billing-Team (applied to 32 rows)
============================================================
```

### Failure Case (activity_id not found):
```
Processing: Some Task Name
  - Found 10 rows for this task
  - Taking Activity ID: 999999999
    → Querying WorkQueue for activity_id: 999999999
    ✗ No WorkQueue found in database
    → Debug: Found 0 rows with activityId=999999999 in act_ru_variable
    → This activity_id doesn't exist in act_ru_variable table!
  - WorkQueue Result: N/A
```

### Failure Case (activity_id exists but no workqueue):
```
Processing: Another Task
  - Found 15 rows for this task
  - Taking Activity ID: 111111111
    → Querying WorkQueue for activity_id: 111111111
    ✗ No WorkQueue found in database
    → Debug: Found 5 rows with activityId=111111111 in act_ru_variable
  - WorkQueue Result: N/A
```
*(In this case, the activity_id exists in act_ru_variable but has no WorkQueue assigned)*

---

## How to Use This Information

### When you run the script:

1. **Check the logs immediately after "Fetching WorkQueue for main table..."**

2. **Look for each task:**
   - Does it show the activity_id?
   - Does it say "✓ Found WorkQueue" or "✗ No WorkQueue found"?

3. **If WorkQueue is not found:**
   - Check the debug message
   - If it says "Found 0 rows with activityId=...", the activity_id doesn't exist in act_ru_variable table
   - If it says "Found N rows with activityId=..." (N > 0), the activity_id exists but has no WorkQueue

4. **Check the summary at the end:**
   - Shows which tasks got WorkQueues
   - Shows how many rows each WorkQueue was applied to

---

## Possible Issues & Solutions

### Issue 1: activity_id doesn't exist in act_ru_variable

**Symptom:**
```
→ Debug: Found 0 rows with activityId=123456789 in act_ru_variable
→ This activity_id doesn't exist in act_ru_variable table!
```

**Possible Causes:**
- The activity_id from your main query doesn't match what's in act_ru_variable
- Data type mismatch (we convert to string, but maybe needs to be int?)
- The activity has no corresponding entry in act_ru_variable

**Solutions:**
- Verify the activity_id value is correct
- Check if act_ru_variable uses a different ID format
- Check if there's a mapping table between oai.id and act_ru_variable

---

### Issue 2: activity_id exists but no WorkQueue

**Symptom:**
```
→ Debug: Found 5 rows with activityId=123456789 in act_ru_variable
```
*(but still no WorkQueue found)*

**Possible Causes:**
- The WorkQueue field is not populated for this activity
- The name_ field might not be exactly 'WorkQueue' (case sensitive?)
- There's a task_id_ mismatch

**Solutions:**
- Check the actual data in act_ru_variable for this activity_id
- Verify the name_ values in act_ru_variable
- Check if WorkQueue is stored under a different name

---

### Issue 3: Query syntax issue

**Symptom:**
```
✗ Database error for activity_id=123456789: [error message]
```

**Possible Causes:**
- SQL syntax error
- Parameter binding issue
- Database permissions

**Solutions:**
- Check the error message in logs
- Verify database connectivity
- Test the query manually in database client

---

## Next Steps

### After Running the Script:

1. **Look at the log file** in `LOGS/` directory

2. **Find the "Fetching WorkQueue" section**

3. **Identify which tasks are failing** and why

4. **Share the relevant log section** if you need help debugging

### Example of what to share:
```
Processing: [Task Name]
  - Found X rows for this task
  - Taking Activity ID: XXXXX
    → Querying WorkQueue for activity_id: XXXXX
    [Result here - success or failure with details]
```

---

## Testing

Run the script:
```bash
python checkUserPendingTask_converted.py
```

Then check:
```bash
# View the latest log file
cat LOGS/checkUserPendingTask_*.log | grep -A 10 "Fetching WorkQueue"

# Or open the log file directly
```

---

## What Changed in Code

### File: `checkUserPendingTask_converted.py`

#### Lines 454-503: Enhanced WorkQueue Fetching
```python
# For each unique Entity Name, get one row explicitly
for entity_name in unique_entities:
    # Get all rows for this entity name
    entity_rows = df[df['Entity Name'] == entity_name]
    
    # Take the first row's activity_id
    first_row = entity_rows.iloc[0]
    activity_id = first_row['Activity ID']
    
    # Detailed logging
    logging.info(f"Processing: {entity_name}")
    logging.info(f"  - Found {len(entity_rows)} rows for this task")
    logging.info(f"  - Taking Activity ID: {activity_id}")
    
    # Fetch workqueue
    workqueue = fetch_workqueue(cursor, activity_id)
    
    logging.info(f"  - WorkQueue Result: {workqueue}")
```

#### Lines 303-362: Enhanced fetch_workqueue() with Debugging
```python
def fetch_workqueue(cursor, activity_id):
    try:
        activity_id_str = str(activity_id)
        logging.info(f"    → Querying WorkQueue for activity_id: {activity_id_str}")
        
        cursor.execute(query, (activity_id_str,))
        result = cursor.fetchone()
        
        if result:
            logging.info(f"    ✓ Found WorkQueue: {workqueue}")
            return workqueue
        else:
            logging.warning(f"    ✗ No WorkQueue found in database")
            
            # Debug check
            cursor.execute(debug_query, (activity_id_str,))
            count = cursor.fetchone()[0]
            logging.warning(f"    → Debug: Found {count} rows...")
            
            return 'N/A'
    except Exception as e:
        logging.error(f"    ✗ Database error...")
        return 'N/A'
```

---

## Summary

✅ **More explicit row selection**  
✅ **Comprehensive logging at every step**  
✅ **Debug information when WorkQueue not found**  
✅ **Activity ID existence check**  
✅ **Summary of WorkQueue mapping**  

The logs will now tell you exactly:
- Which activity_id is being used for each task
- Whether the query succeeds or fails
- Why it fails (activity_id doesn't exist vs. no WorkQueue assigned)
- How many rows each WorkQueue is applied to

---

**Run the script and check the logs - they will show exactly what's happening!**














