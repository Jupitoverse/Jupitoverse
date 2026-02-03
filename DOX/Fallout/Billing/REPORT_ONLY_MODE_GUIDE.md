# REPORT-ONLY MODE Guide

## Overview

**REPORT_ONLY_MODE** is a new feature that allows the script to run without requiring WRITE database access. Perfect for situations where:
- Write DB is inaccessible or read-only
- You want to preview what would be inserted
- You need daily monitoring without modifying the database

## How It Works

### Normal Mode (REPORT_ONLY_MODE = False)
```
READ DB → Fetch Data → Check Duplicates → INSERT to WRITE DB → Generate Report → Email
```

### Report-Only Mode (REPORT_ONLY_MODE = True)
```
READ DB → Fetch Data → Check Duplicates → Generate Report (no inserts) → Email
```

## Configuration

### Enable Report-Only Mode

Edit `OSO_Service_Activated.py`:

```python
# Report-Only Mode: Set to True to avoid write DB issues (no INSERT operations)
REPORT_ONLY_MODE = True  # True = Only generates reports (no database writes)
```

### Disable Report-Only Mode (Normal Operation)

```python
REPORT_ONLY_MODE = False  # False = Normal mode with INSERT operations
```

## Features in Report-Only Mode

### 1. No Write DB Required
- ✅ Only connects to READ DB
- ✅ No INSERT operations
- ✅ No write locks or transactions
- ✅ Safer for production environments

### 2. Multi-Sheet Excel Report

The generated Excel file contains **3 sheets**:

#### Sheet 1: All Records
- Complete tracking table data
- All columns including RCA, Status, etc.
- Total count shown

#### Sheet 2: NEW Records
- Records that **would be inserted** (but weren't)
- These don't exist in the tracking table yet
- Action required: Review for new service activations

#### Sheet 3: EXISTING Records
- Records that **already exist** in the tracking table
- Identified by: `service_id + site_id + version`
- No action needed (already tracked)

### 3. Enhanced Email Report

Email subject includes **[REPORT-ONLY]** tag:
```
Comcast OSS || OSO Service Activated Report [REPORT-ONLY] - 2025-12-01
```

Email body shows:
- 🔍 **REPORT-ONLY MODE** banner
- Summary statistics:
  - NEW records found (would be inserted)
  - EXISTING records (already in table)
  - Total records in tracking table
- Database information
- Sheet-by-sheet breakdown

### 4. Console Output

```
================================================================================
  OSO Service Activated - Data Sync & Email Report
  MODE: REPORT-ONLY (No Database Writes)
  Execution Date: 2025-12-01
  Execution Time: 16:51:54
================================================================================

Step 4: Checking records (REPORT-ONLY MODE - no inserts)...
Will check 88 records against existing table...
[INFO] REPORT_ONLY_MODE is enabled - no database writes will be performed

[OK] Check Complete:
    Total checked: 88 records
    NEW records: 12 (would be inserted)
    EXISTING records: 76 (already in table)
================================================================================

[OK] REPORT-ONLY MODE COMPLETED!
    (No database writes performed)
```

## Use Cases

### Use Case 1: Write DB Access Issues
**Problem:** WRITE DB is read-only, inaccessible, or has connection issues

**Solution:** Enable REPORT_ONLY_MODE
- Get daily reports without needing write access
- Monitor new service activations
- Manually handle inserts or work with DBA later

### Use Case 2: Preview Before Insert
**Problem:** Want to see what would be inserted before committing

**Solution:** Run in REPORT_ONLY_MODE first
- Review the "NEW Records" sheet
- Verify data quality
- Then switch to normal mode if satisfied

### Use Case 3: Read-Only Monitoring
**Problem:** Need visibility without modifying production data

**Solution:** REPORT_ONLY_MODE provides:
- Daily monitoring reports
- Trend analysis (how many new records daily)
- No risk of accidental data changes

### Use Case 4: Parallel Environments
**Problem:** Different teams manage READ and WRITE databases

**Solution:**
- READ team: Use REPORT_ONLY_MODE for monitoring
- WRITE team: Use normal mode for data sync
- Both get visibility without stepping on each other

## Comparison Table

| Feature | Normal Mode | Report-Only Mode |
|---------|-------------|------------------|
| READ DB Connection | ✅ Required | ✅ Required |
| WRITE DB Connection | ✅ Required | ❌ Not Used |
| INSERT Operations | ✅ Yes | ❌ No |
| Excel Sheets | 2 (All + Fetched) | 3 (All + NEW + EXISTING) |
| Email Subject | Standard | [REPORT-ONLY] tag |
| NEW records identification | ✅ Yes | ✅ Yes |
| EXISTING records identification | ✅ Yes | ✅ Yes |
| Database writes | ✅ Yes | ❌ No |
| Safe for production | ⚠️ Writes data | ✅ Read-only |

## How to Switch Between Modes

### Quick Toggle

**Line 38** in `OSO_Service_Activated.py`:

```python
# Enable Report-Only Mode (no writes)
REPORT_ONLY_MODE = True

# OR

# Disable Report-Only Mode (normal operation with writes)
REPORT_ONLY_MODE = False
```

### No Other Changes Needed
- All other configuration stays the same
- Email recipients unchanged
- SQL query unchanged
- Logging and error handling unchanged

## Examples

### Example 1: Daily Monitoring (Report-Only)

```python
# Configuration
REPORT_ONLY_MODE = True
SEND_EMAIL = True
DATE_EXECUTION_FREQUENCY = 1  # Daily
```

**Result:**
- Runs every day
- Checks for new service activations
- Emails report with NEW vs EXISTING breakdown
- No database modifications

### Example 2: Weekly Data Sync (Normal Mode)

```python
# Configuration
REPORT_ONLY_MODE = False
SEND_EMAIL = True
DATE_EXECUTION_FREQUENCY = 7  # Weekly
```

**Result:**
- Runs every 7 days
- Inserts new records into WRITE DB
- Emails report with inserted vs skipped counts
- Database updated

### Example 3: One-Time Analysis

```python
# Configuration
REPORT_ONLY_MODE = True
SEND_EMAIL = False  # Save email, just generate Excel
DATE_EXECUTION_FREQUENCY = 1
```

**Result:**
- Generates Excel report locally
- No email sent
- Review Excel to understand data landscape

## Logs Difference

### Normal Mode Logs
```
2025-12-01 16:51:54 - INFO - Report-Only Mode: DISABLED
2025-12-01 16:52:15 - INFO - STEP 4: Checking existence and inserting new records via WRITE DB
2025-12-01 16:52:30 - INFO - Inserted: 12, Skipped: 76
```

### Report-Only Mode Logs
```
2025-12-01 16:51:54 - INFO - Report-Only Mode: ENABLED
2025-12-01 16:52:15 - INFO - STEP 4: REPORT-ONLY MODE - Checking new vs existing records (no writes)
2025-12-01 16:52:30 - INFO - NEW records found: 12, EXISTING records: 76
```

## FAQ

### Q: Can I switch modes without modifying the script?
**A:** Currently no, but you could add a command-line argument:
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--report-only', action='store_true')
args = parser.parse_args()
REPORT_ONLY_MODE = args.report_only
```

Then run:
```bash
python OSO_Service_Activated.py --report-only
```

### Q: Does Report-Only Mode affect performance?
**A:** Minimal difference:
- Same READ DB queries
- Same duplicate checking logic
- Saves time: No INSERT operations, no WRITE DB connection
- Overall: Slightly faster in Report-Only Mode

### Q: Will the Excel file be smaller in Report-Only Mode?
**A:** No, it might be slightly larger due to the extra sheets (NEW Records, EXISTING Records).

### Q: Can I use Report-Only Mode permanently?
**A:** Yes! If you only need monitoring/reporting and another process handles data insertion, Report-Only Mode is perfect for your needs.

### Q: What if I want to insert records after running in Report-Only Mode?
**A:** The "NEW Records" sheet in the Excel file shows exactly what needs to be inserted. You can:
1. Manually insert using SQL
2. Switch to normal mode and run again
3. Provide the Excel to another team for processing

## Troubleshooting

### Issue: "WRITE DB is same as READ DB" Warning

**Cause:** Both configs point to the same host

**Impact in Report-Only Mode:** None! WRITE DB isn't used

**Fix:** Update WRITE_DB_CONFIG when ready for normal mode

---

### Issue: Still seeing WRITE DB connection attempts

**Check:** Ensure line 38 has:
```python
REPORT_ONLY_MODE = True
```

**Verify:** Console output should show:
```
MODE: REPORT-ONLY (No Database Writes)
```

---

### Issue: Excel doesn't have NEW/EXISTING sheets

**Check:** 
1. REPORT_ONLY_MODE = True?
2. Script ran without errors?
3. Data was fetched successfully?

**Debug:** Check logs for:
```
Sheet 'NEW Records': X rows (would be inserted)
Sheet 'EXISTING Records': Y rows (already in table)
```

---

## Conclusion

**REPORT_ONLY_MODE** provides:
- ✅ Safe monitoring without write access
- ✅ Detailed analysis of what would be inserted
- ✅ Flexibility for different use cases
- ✅ No database impact
- ✅ Complete visibility

Perfect for situations where **write access is problematic** but **monitoring is essential**!

---

**Need help?** Check the main README or contact the automation team.









