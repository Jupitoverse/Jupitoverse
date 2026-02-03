================================================================================
OSO_Service_Activated.py - Comprehensive Guide
================================================================================

PURPOSE:
  PostgreSQL-based service activation tracking system that:
  - Connects to READ and WRITE databases
  - Fetches service activation data
  - Maintains tracking table with RCA and status columns
  - Avoids duplicates based on service_id + site_id + version

================================================================================
DATABASE CONFIGURATION
================================================================================

READ DATABASE (Data Source):
  Host:     oso-pstgr-rd.orion.comcast.com
  Database: prodossdb
  Port:     6432
  User:     ossdb01db
  Password: Pr0d_ossdb01db

WRITE DATABASE (Data Storage):
  Host:     OSS-PROD1-PGRDS-NLB-1fe6faf4eb2c6ea3.elb.us-east-2.amazonaws.com
  Database: prodossdb
  Port:     6432
  User:     ossdb01db
  Password: Pr0d_ossdb01db

================================================================================
TABLE SCHEMA: OSO_Service_Activated_Data
================================================================================

QUERY DATA COLUMNS (from SQL):
  - customer_id
  - site_id  
  - service_id
  - product_agreement_instance_id
  - solution_id
  - version
  - ptd
  - customer_name
  - framework_agreement_id
  - division
  - region
  - business_action
  - solution_leg_state
  - solution_name
  - ptd_status
  - activation_date
  - customer_accepted
  - product_spec
  - send_to_billing
  - cpm
  - customer_acceptance_days
  - customer_acceptance_state
  - customer_acceptance_plan_id
  - customer_acceptance_activity_id
  - ticketid
  - create_ticket

TRACKING COLUMNS (for manual/script updates):
  - RCA (Root Cause Analysis)
  - RCA_Category
  - Owned_By
  - WorkQueue
  - Task_Owner
  - Tracking_ID
  - Next_Action
  - Handling_Status

METADATA COLUMNS (auto-populated):
  - created_at (timestamp when record created)
  - updated_at (timestamp when record updated)

UNIQUE CONSTRAINT:
  - Composite key on: service_id + site_id + version
  - Prevents duplicate entries

================================================================================
REQUIREMENTS
================================================================================

Python Packages:
  pip install psycopg2-binary pandas openpyxl

Network Access:
  - Access to oso-pstgr-rd.orion.comcast.com (READ)
  - Access to OSS-PROD1-PGRDS-NLB (WRITE)
  - VPN may be required

================================================================================
CONFIGURATION TOGGLES
================================================================================

The script has configurable toggles at the top:

1. SEND_EMAIL = True/False
   - Controls whether email is sent after execution
   - Set to False to skip email sending

2. DATE_EXECUTION_FREQUENCY = 1
   - Script runs every N days
   - 1 = daily, 7 = weekly, 30 = monthly
   - Script auto-skips if not execution day

3. EMAIL_RECIPIENTS
   - List of primary email recipients
   - Default: abhishek_agrahari@comcast.com

4. EMAIL_CC_RECIPIENTS
   - List of CC recipients
   - Default: abhisha3@amdocs.com

5. QUERY_TIMEOUT_SECONDS = 300 (NEW in v2.1)
   - Automatic query timeout in seconds
   - Default: 300 seconds (5 minutes)
   - Prevents long-running queries from impacting database
   - Query auto-aborts if it takes longer

6. ENABLE_QUERY_TIMEOUT = True (NEW in v2.1)
   - Enable/disable timeout protection
   - Default: True (enabled)
   - Set to False to disable timeout (not recommended)

================================================================================
USAGE
================================================================================

Option 1: Full Run (with data insertion + email)
  Double-click: RUN_OSO_SCRIPT.bat
  OR
  Command line: python OSO_Service_Activated.py

Option 2: Dry Run (test without insertion/email)
  Double-click: RUN_OSO_DRY_RUN.bat
  OR
  Command line: python OSO_Service_Activated.py --dry-run

================================================================================
WHAT THE SCRIPT DOES
================================================================================

STEP 1: Test Database Connections
  - Tests READ database connection
  - Tests WRITE database connection
  - Displays database versions
  - Fails if either connection fails

STEP 2: Create/Verify Table (WRITE DB)
  - Creates OSO_Service_Activated_Data table if not exists
  - Adds unique constraint on service_id + site_id + version
  - Creates index for faster lookups
  - Only runs in full mode (skipped in dry-run)

STEP 3: Fetch Data (READ DB)
  - Executes complex SQL query
  - Fetches service activation data
  - Converts to pandas DataFrame
  - Normalizes column names

STEP 4: Insert Records (WRITE DB)
  - For each record:
    * Checks if service_id + site_id + version already exists
    * Inserts if new
    * Skips if already exists
  - Shows count of inserted and skipped records
  - Only runs in full mode (skipped in dry-run)

STEP 5: Save Excel File
  - Saves fetched data to Excel
  - Filename: OSO_Service_Activated_YYYYMMDD_HHMMSS.xlsx
  - Useful for reference and verification

================================================================================
DUPLICATE DETECTION LOGIC
================================================================================

The script checks for existing records using:
  
  SELECT COUNT(*) FROM OSO_Service_Activated_Data
  WHERE service_id = ? AND site_id = ? AND version = ?

If count > 0: Record exists, SKIP insertion
If count = 0: Record is new, INSERT it

This ensures:
  - No duplicate entries
  - Data integrity
  - Safe to run multiple times

================================================================================
OUTPUT FILES
================================================================================

1. Excel File:
   - Name: OSO_Service_Activated_YYYYMMDD_HHMMSS.xlsx
   - Location: Same directory as script
   - Contents: All fetched records (for reference)

2. Log Output:
   - Displayed on console
   - Shows progress and results
   - Includes timestamps

================================================================================
SAMPLE OUTPUT
================================================================================

========================================================================
  OSO Service Activated - Data Sync Script
========================================================================

Step 1: Testing database connections...
========================================================================
Testing Database Connections...
========================================================================

[1] Testing READ Database...
    Host: oso-pstgr-rd.orion.comcast.com
    Port: 6432
    Database: prodossdb
--------------------------------------------------------------------------------
[OK] READ DB Connected!
    Version: PostgreSQL 12.x...

[2] Testing WRITE Database...
    Host: OSS-PROD1-PGRDS-NLB-1fe6faf4eb2c6ea3.elb.us-east-2.amazonaws.com
    Port: 6432
    Database: prodossdb
--------------------------------------------------------------------------------
[OK] WRITE DB Connected!
    Version: PostgreSQL 12.x...
========================================================================

Step 2: Creating/Verifying table...
========================================================================
[OK] Table 'OSO_Service_Activated_Data' is ready
========================================================================

Step 3: Fetching data from READ database...
========================================================================
Fetching Data from READ Database...
========================================================================
[OK] Fetched 156 records
Columns: 26
========================================================================

Step 4: Inserting new records...
========================================================================
Inserting Records into WRITE Database...
========================================================================

[OK] Processing Complete:
    Inserted: 45 new records
    Skipped:  111 existing records
========================================================================

Step 5: Saving Excel file...
========================================================================
Saving data to Excel for reference...
========================================================================
[OK] Excel file saved: OSO_Service_Activated_20250127_184530.xlsx
    Size: 89.45 KB
    Records: 156
========================================================================

========================================================================
[OK] ALL OPERATIONS COMPLETED!
========================================================================
Records fetched: 156
Records inserted: 45
Records skipped: 111
Excel file: C:\...\OSO_Service_Activated_20250127_184530.xlsx
========================================================================

================================================================================
TROUBLESHOOTING
================================================================================

Connection Failed?
  - Check VPN connection
  - Verify network access to databases
  - Check firewall settings
  - Verify credentials

Table Creation Failed?
  - Check WRITE database permissions
  - Verify user has CREATE TABLE privilege
  - Check disk space on database server

No Data Retrieved?
  - Check if query returns data in READ database
  - Verify date filters in query (activation_date >= now() - 5)
  - Check if test customers are filtered out

Insertion Failed?
  - Check WRITE database permissions
  - Verify user has INSERT privilege
  - Check for data type mismatches
  - Review logs for specific errors

================================================================================
TRACKING COLUMN USAGE
================================================================================

After records are inserted, you can manually update tracking columns:

UPDATE OSO_Service_Activated_Data
SET 
    RCA = 'Root cause description',
    RCA_Category = 'Configuration|Network|Application',
    Owned_By = 'Team Name',
    WorkQueue = 'Queue Name',
    Task_Owner = 'Person Name',
    Tracking_ID = 'TICKET-12345',
    Next_Action = 'Action description',
    Handling_Status = 'Open|In Progress|Resolved|Closed'
WHERE service_id = 'SERVICE123'
  AND site_id = 'SITE456'
  AND version = '1';

================================================================================
SCHEDULED EXECUTION
================================================================================

Windows Task Scheduler:
  1. Open Task Scheduler
  2. Create Basic Task
  3. Trigger: Daily at 6:00 AM
  4. Action: Start a program
     Program: C:\Python313\python.exe
     Arguments: "C:\path\to\OSO_Service_Activated.py"
  5. Save task

This will run daily and only insert new records.

================================================================================
COMPARISON WITH Service_Activated.py
================================================================================

Service_Activated.py:
  - MySQL database
  - Email report generation
  - Single query execution
  - No data persistence

OSO_Service_Activated.py:
  - PostgreSQL databases (READ + WRITE)
  - Data persistence in tracking table
  - Duplicate detection
  - RCA and status tracking columns
  - No email (focused on data management)

================================================================================
SECURITY NOTES
================================================================================

WARNING: This script contains hardcoded database credentials.

For production:
  - Use environment variables
  - Use secrets management
  - Implement role-based access
  - Enable SSL/TLS for database connections
  - Audit database access

================================================================================
Author: Abhishek
Date: 2025-01-27
Version: 1.0
================================================================================

