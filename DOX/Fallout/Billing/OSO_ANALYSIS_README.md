# OSO Analysis Feature - Complex Nested Query Logic

## Overview

The **OSO_Analysis** sheet is a powerful addition to the OSO_Service_Activated_local.py script that performs deep analysis on service activation data using a series of nested PostgreSQL queries.

## What It Does

The analysis processes data hierarchically:

```
Customer_Id
  └─► Site_ID (multiple per customer)
       └─► Service_Id (multiple per site)
            └─► Run 9 different queries
                 └─► Generate analysis record
```

## Output Columns

The **OSO_Analysis** sheet contains:

| Column | Description |
|--------|-------------|
| `Customer_Id` | Customer identifier |
| `Site_ID` | Site identifier |
| `Service_Id` | Service identifier |
| `RCA` | Root Cause Analysis details |
| `Task_Owner` | Task owner name(s) |
| `Workqueue` | Work queue assignment(s) |
| `Interface` | Interface details |

## Query Flow Logic

### Step 1: Check In-Progress Activities (Q1)

For each `Service_Id`, check if there are any in-progress activities:

```sql
-- If count > 0, proceed to Step 2
-- If count = 0, skip this service
```

### Step 2: Get Implementation Types (Q2)

Get all implementation types (Manual, Automatic, or both):

```sql
-- Returns: ['Manual'], ['Automatic'], or ['Manual', 'Automatic']
```

### Step 3A: Manual Implementation Path

If implementation_type = 'Manual':

1. **Q3**: Get RCA details (entity_name, name, time_elapsed)
2. **Q4**: Get activity ID(s)
3. **Q5**: Get task owner name(s) using activity ID
4. **Q6**: Get work queue(s) using activity ID

**Result:**
- `RCA`: Combined entity details
- `Task_Owner`: Task owner name(s)
- `Workqueue`: Work queue assignment(s)
- `Interface`: Empty

### Step 3B: Automatic Implementation Path

If implementation_type = 'Automatic':

1. **Q7**: Get RCA details (entity_name, name, time_elapsed)
2. **Q8**: Get spec_ver_id(s)
3. **Q9**: Get interface details using spec_id

**Result:**
- `RCA`: Combined entity details
- `Task_Owner`: Empty
- `Workqueue`: Empty
- `Interface`: Interface details

### Step 4: Handle Multiple Implementation Types

If a service has BOTH Manual and Automatic:
- Process Manual path → Create record
- Process Automatic path → Create record
- Result: 2 rows for the same Service_Id

## Query Definitions

### Q1: Count In-Progress Activities
```sql
with temp_abhi as (
    select distinct dpv2.project_id as pv_prj_id
    from dd_product_version dpv
    left join dd_sol_leg_site_2_prod_version dslspv on dpv.id = dslspv.prod_ver_id
    left join dd_sol_leg_site_2_prod_version dslspv2 on dslspv.solution_leg_site_id = dslspv2.solution_leg_site_id
    left join dd_product_version dpv2 on dslspv2.prod_ver_id = dpv2.id
    where dpv.service_id = '$Service_Id'
)
select count(oai.id) as cnt
from temp_abhi
left join sc_project_order_instance spoi on pv_prj_id = spoi.id
left join oss_activity_instance oai on spoi.plan_id = oai.plan_id and oai.is_latest_version = 1
left join ossdb01ref.oss_ref_attribute ora on oai.spec_ver_id = ora.attribute_value
left join ossdb01ref.oss_ref_data ord on ora.entity_id = ord.entity_id
where oai.status='In Progress'
```

### Q2: Get Implementation Types
```sql
-- Same CTE as Q1
select distinct oai.implementation_type
from temp_abhi
...
where oai.status='In Progress'
group by oai.implementation_type
```

### Q3: RCA Details (Manual)
```sql
-- Same CTE as Q1
select distinct ord.entity_name, spoi.name, oai.id,
    now() - oai.actual_start_date as time_elapsed, oai.implementation_type
from temp_abhi
...
where oai.status='In Progress'
```

### Q4: Get Activity IDs
```sql
-- Same CTE as Q1
select distinct oai.id
from temp_abhi
...
where oai.status='In Progress'
group by oai.id
```

### Q5: Get Task Owner
```sql
select text_ as task_owner_name 
from act_ru_variable 
where task_id_ in (
    select task_id_ 
    from act_ru_variable arv 
    where text_ = '$activity_id' and name_= 'activityId'
) 
and name_ in ('task_owner_name')
```

### Q6: Get Work Queue
```sql
select text_ as work_queue 
from act_ru_variable 
where task_id_ in (
    select task_id_ 
    from act_ru_variable arv 
    where text_ = '$activity_id' and name_= 'activityId'
) 
and name_ in ('WorkQueue')
```

### Q7: RCA Details (Automatic)
```sql
-- Same as Q3, but for Automatic implementation
```

### Q8: Get Spec Ver IDs
```sql
-- Same CTE as Q1
select distinct oai.spec_ver_id
from temp_abhi
...
where oai.status='In Progress'
group by oai.spec_ver_id
```

### Q9: Get Interface
```sql
select oad.interface 
from oso_activity_data oad  
where oad.spec_id = '28519df3-7986-4d3d-9c8b-5bb0ccc2cc0a'
```

## Example Output

### Example 1: Manual Implementation

| Customer_Id | Site_ID | Service_Id | RCA | Task_Owner | Workqueue | Interface |
|-------------|---------|------------|-----|------------|-----------|-----------|
| 12345 | S001 | SVC001 | Create_Circuit \| Project_A \| 2 days | John Doe | OSO_Manual_Queue | |

### Example 2: Automatic Implementation

| Customer_Id | Site_ID | Service_Id | RCA | Task_Owner | Workqueue | Interface |
|-------------|---------|------------|-----|------------|-----------|-----------|
| 12345 | S002 | SVC002 | Activate_Service \| Project_B \| 5 hours | | | SOAP/REST API |

### Example 3: Both Manual and Automatic

| Customer_Id | Site_ID | Service_Id | RCA | Task_Owner | Workqueue | Interface |
|-------------|---------|------------|-----|------------|-----------|-----------|
| 12345 | S003 | SVC003 | Manual_Step \| Project_C \| 1 day | Jane Smith | OSO_Queue_1 | |
| 12345 | S003 | SVC003 | Auto_Step \| Project_C \| 6 hours | | | HTTP Interface |

## Processing Details

### Nested Loops

```python
for each Customer_Id:
    for each Site_ID:
        for each Service_Id:
            # Run Q1-Q9 logic
            # Generate analysis record(s)
```

### Data Aggregation

When multiple results are found:
- **Task Owner**: Combined with " || " separator
- **Work Queue**: Combined with " || " separator
- **RCA**: Combined with " || " separator
- **Interface**: Combined with " || " separator

Example:
```
Task_Owner: "John Doe || Jane Smith || Mike Johnson"
```

### Sorting

Results are sorted hierarchically:
```python
df_analysis.sort_values(['Customer_Id', 'Site_ID', 'Service_Id'], ascending=True)
```

This ensures parent-to-child ordering in the Excel sheet.

## Performance Considerations

### Query Complexity
- Each Service_Id may trigger 3-9 database queries
- Total queries = Services × (1 to 9 queries per service)

### Example Calculation
If you have:
- 88 records in main data
- 20 unique Service_Ids
- Average 5 queries per service

**Total queries:** 20 × 5 = **100 database queries**

### Optimization Tips

1. **Timeout Protection**: Already implemented (600 seconds)
2. **Error Handling**: Continues processing even if one service fails
3. **Progress Updates**: Shows progress every 10 customer/site combinations
4. **Logging**: Detailed logs for debugging

### Expected Runtime

| Records | Service_Ids | Estimated Time |
|---------|-------------|----------------|
| 88 | 20 | 2-5 minutes |
| 200 | 50 | 5-10 minutes |
| 500 | 100 | 10-20 minutes |

**Factors affecting runtime:**
- Database response time
- Number of in-progress activities
- Network latency
- Implementation type distribution

## Console Output

During analysis, you'll see:

```
================================================================================
Performing OSO Analysis (Complex Query Logic)
================================================================================
Processing 45 Customer_Id/Site_ID combinations...
  Progress: 10/45 processed...
  Progress: 20/45 processed...
  Progress: 30/45 processed...
  Progress: 40/45 processed...
[OK] Analysis complete: 23 records generated
```

## Error Handling

### Service-Level Errors
If a service fails:
- Error is logged
- Processing continues with next service
- Failed service is skipped in analysis

### Analysis Failure
If entire analysis fails:
- Warning is logged
- Script continues
- Excel created with empty OSO_Analysis sheet

## Debugging

### Enable Detailed Logging

In the script, change:
```python
logging.basicConfig(level=logging.INFO, ...)
```

To:
```python
logging.basicConfig(level=logging.DEBUG, ...)
```

### Check Logs

Look for:
```
2025-12-01 16:52:30 - INFO - Processing Customer_Id: 12345, Site_ID: S001, Services: 3
2025-12-01 16:52:31 - INFO -   Service_Id SVC001: Found 2 in-progress activities
2025-12-01 16:52:32 - INFO -     Processing Manual implementation for Service_Id: SVC001
```

## Customization

### Modify Q9 Spec ID

Currently hardcoded to `28519df3-7986-4d3d-9c8b-5bb0ccc2cc0a`:

```python
def get_interface(spec_id='28519df3-7986-4d3d-9c8b-5bb0ccc2cc0a'):
```

To use dynamic spec_id from Q8:
```python
# In perform_oso_analysis(), Automatic section:
spec_ver_ids = get_spec_ver_ids(service_id)
for spec_id in spec_ver_ids:
    interface = get_interface(spec_id)
```

### Add Additional Columns

In `perform_oso_analysis()`, add to the result dict:
```python
analysis_results.append({
    'Customer_Id': customer_id,
    'Site_ID': site_id,
    'Service_Id': service_id,
    'RCA': rca,
    'Task_Owner': task_owner,
    'Workqueue': work_queue,
    'Interface': interface,
    'Custom_Column': your_value,  # ADD HERE
})
```

Also update the empty DataFrame columns:
```python
pd.DataFrame(columns=[..., 'Custom_Column'])
```

## Troubleshooting

### Issue: Analysis sheet is empty

**Possible Causes:**
1. No services have in-progress activities (Q1 returns 0 for all)
2. Database connection issues
3. Query timeout

**Solution:**
- Check logs for "No in-progress activities, skipping"
- Verify database has data with `oai.status='In Progress'`

### Issue: Analysis taking too long

**Solutions:**
1. Reduce dataset size (filter main query)
2. Increase query timeout
3. Run during off-peak hours
4. Add database indexes (see QUERY_OPTIMIZATION_ANALYSIS.md)

### Issue: Missing Task_Owner or Workqueue

**Causes:**
- Q5/Q6 returning no data
- activity_id not found in act_ru_variable table

**Solution:**
- Check if activity_id exists in database
- Verify table/column names are correct

## Integration with Main Script

The analysis is automatically integrated:

1. **Step 1-2**: Fetch main service activation data
2. **Step 3**: Run OSO Analysis (NEW)
3. **Step 4**: Save both sheets to Excel
4. **Step 5**: Send email with both sheets

No manual intervention needed!

## Excel File Structure

```
OSO_Service_Activated_Local_YYYYMMDD_HHMMSS.xlsx
│
├─ Sheet 1: Service Activation Data (88 records)
│   ├─ Customer_Id
│   ├─ Customer_Name
│   ├─ Site_ID
│   ├─ Service_Id
│   ├─ ... (28 columns total)
│
└─ Sheet 2: OSO_Analysis (23 records)
    ├─ Customer_Id
    ├─ Site_ID
    ├─ Service_Id
    ├─ RCA
    ├─ Task_Owner
    ├─ Workqueue
    └─ Interface
```

## Email Report Update

The email now includes:

```
Execution Summary:
- Total Records Fetched: 88
- OSO Analysis Records: 23      ← NEW
- Execution Date: 2025-12-01
- Execution Time: 16:52:30

Attached Report:
- Sheet 1 - Service Activation Data: 88 records
- Sheet 2 - OSO_Analysis: 23 analysis records  ← NEW
```

## Summary

✅ **Automated**: Runs automatically as part of the script
✅ **Comprehensive**: 9 different queries per service
✅ **Hierarchical**: Customer → Site → Service structure
✅ **Error-Resistant**: Continues even if services fail
✅ **Well-Logged**: Detailed logging for debugging
✅ **Flexible**: Easy to customize and extend

**Result**: Rich analysis data in a separate Excel sheet with RCA, task ownership, and interface details!

---

**Ready to use!** Just run the script and check the OSO_Analysis sheet in the Excel file! 🚀









