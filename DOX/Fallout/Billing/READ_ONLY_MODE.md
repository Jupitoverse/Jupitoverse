# Read-Only Database Solution

## Problem

Your server can only access the READ database (`oso-pstgr-rd.orion.comcast.com`), which is a **read-only replica**. It cannot:
- CREATE TABLE
- INSERT records
- UPDATE records

The WRITE database (`OSS-PROD1-PGRDS-NLB-1fe6faf4eb2c6ea3.elb.us-east-2.amazonaws.com`) times out after 30 seconds from your server.

---

## Solution Applied

The script now automatically detects when you're using a read-only database and handles it gracefully:

### What the Script Does Now:

1. **Step 1**: Tests connections (READ DB will connect)
2. **Step 2**: Checks if table exists (instead of trying to create)
   - ✅ If table exists: Continues in read-only mode
   - ❌ If table doesn't exist: Shows error with instructions
3. **Step 3-5**: Fetches and compares data (read operations work fine)
4. **Step 6**: Skips insert (read-only, cannot insert)
5. **Step 7-9**: Continues with email report (read operations)

### Result:

The script will run and generate reports, but **cannot insert new records** into the database.

---

## Current Modes

### Mode 1: Read-Only Mode (Current - Your Server)

**What Works:**
- ✅ Fetch service activation data
- ✅ Compare against existing records
- ✅ Generate Excel report
- ✅ Send email with report

**What Doesn't Work:**
- ❌ Cannot insert new records into database
- ❌ Cannot create table if it doesn't exist

**Use Case:** 
- Monitoring and reporting
- Checking what new records would be inserted
- Regular status reports

---

### Mode 2: Full Write Mode (Requires WRITE DB Access)

**What Works:**
- ✅ Everything in Read-Only Mode PLUS:
- ✅ Insert new records into database
- ✅ Create table if doesn't exist

**Requires:**
- Access to WRITE DB from your server
- Network/firewall rules allowing connection
- Writable database credentials

---

## How to Run Now

### Option A: Run in Read-Only Mode (Monitoring/Reporting Only)

```bash
# This will work on your current server
python OSO_Service_Activated.py
```

**Expected Output:**
```
Step 2: Creating/Verifying table...
[WARNING] Using read-only replica - checking if table exists...
[OK] Table 'OSO_Service_Activated_Data' exists with 1250 records
[OK] Table exists - proceeding (read-only mode)

...

Step 6: [SKIPPED - read-only database]
[WARNING] Cannot insert records into read-only database
    500 new records found but cannot be inserted
    To fix: Run script from server with WRITE DB access
```

The script will still:
- Generate a full Excel report
- Send email with all data
- Log all findings

---

### Option B: Full Mode with Inserts (Need WRITE DB Access)

**To enable full write mode, you need to:**

1. **Run from a different server** that has access to WRITE DB
2. **Or** Request network/firewall access to:
   ```
   Host: OSS-PROD1-PGRDS-NLB-1fe6faf4eb2c6ea3.elb.us-east-2.amazonaws.com
   Port: 6432
   ```

3. **Or** Use a database you have write access to

---

## Manual Table Creation (If Table Doesn't Exist)

If the table doesn't exist on the READ DB, you need to create it on a writable database first.

### SQL to Create Table:

```sql
CREATE TABLE OSO_Service_Activated_Data (
    -- Primary data columns
    customer_id TEXT,
    site_id TEXT,
    service_id TEXT,
    product_agreement_instance_id TEXT,
    solution_id TEXT,
    version TEXT,
    ptd TEXT,
    customer_name TEXT,
    framework_agreement_id TEXT,
    division TEXT,
    region TEXT,
    business_action TEXT,
    solution_leg_state TEXT,
    solution_name TEXT,
    ptd_status TEXT,
    activation_date TEXT,
    customer_accepted TEXT,
    product_spec TEXT,
    send_to_billing TEXT,
    cpm TEXT,
    customer_acceptance_days TEXT,
    customer_acceptance_state TEXT,
    customer_acceptance_plan_id TEXT,
    customer_acceptance_activity_id TEXT,
    ticketid TEXT,
    create_ticket TEXT,
    
    -- Tracking columns
    RCA TEXT,
    RCA_Category TEXT,
    Owned_By TEXT,
    WorkQueue TEXT,
    Task_Owner TEXT,
    Tracking_ID TEXT,
    Next_Action TEXT,
    Handling_Status TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Unique constraint
    CONSTRAINT unique_service_site_version UNIQUE (service_id, site_id, version)
);
```

**To create:**
1. Connect to a writable database (not the read replica)
2. Execute the SQL above
3. Then run the script - it will detect the table exists

---

## Alternative: Create Local Tracking

If you cannot get WRITE DB access, consider creating a local tracking mechanism:

### Option: Export to Excel Only (No Database Insert)

The script already generates Excel reports. You could:
1. Use Excel files as your tracking mechanism
2. Compare current vs previous Excel files
3. Store Excel files in a shared location
4. Use Excel as the "database"

This is what the script does now in read-only mode!

---

## Recommended Approach

**For Now (Immediate Solution):**
```bash
# Run in read-only mode for monitoring/reporting
python OSO_Service_Activated.py
```

This gives you:
- Complete visibility of service activations
- Excel reports with all data
- Email notifications
- Comparison of new vs existing records

**For Future (Full Solution):**
1. **Request network access** to WRITE DB from your server
2. **Or** Set up a writable database that your server can access
3. **Or** Schedule script to run on a server with WRITE DB access

---

## Current Configuration

```python
# READ DB - Working ✅
READ_DB_CONFIG = {
    'host': 'oso-pstgr-rd.orion.comcast.com',
    'port': 6432,
    ...
}

# WRITE DB - Using READ DB (read-only) ⚠️
WRITE_DB_CONFIG = {
    'host': 'oso-pstgr-rd.orion.comcast.com',  # Same as READ
    'port': 6432,
    ...
}
```

---

## Summary

✅ **What's Working:**
- Script runs successfully
- Fetches all service activation data
- Compares against existing records
- Generates Excel reports
- Sends email notifications
- Provides full visibility

⚠️ **Limitation:**
- Cannot insert new records into database
- Database remains unchanged
- New records only appear in Excel report

💡 **This is fine for:**
- Monitoring and alerting
- Reporting purposes
- Identifying issues
- Tracking service activations
- Email notifications to team

🎯 **Run the script now - it will work in read-only mode!**

---

**Updated**: November 29, 2025  
**Mode**: Read-Only (Monitoring/Reporting)  
**Status**: ✅ Functional












