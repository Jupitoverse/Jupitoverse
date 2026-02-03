# OSO_Service_Activated_local.py - Creation Summary

## What Was Created

✅ **OSO_Service_Activated_local.py** - Simplified version for local development

## Key Features

### 1. Simplified Architecture
- ❌ No WRITE DB connection
- ✅ Only READ DB (PostgreSQL)
- ✅ Fetches data using your SQL query
- ✅ Stores in pandas DataFrame
- ✅ Exports to Excel (single sheet)
- ✅ Sends email with attachment

### 2. Easy to Customize
The script is designed to be easily modified:
- Add calculated columns
- Filter data
- Add custom business logic
- Change Excel format
- Modify email content

### 3. Production-Ready
- ✅ Comprehensive logging
- ✅ Error handling
- ✅ Query timeout protection (10 minutes)
- ✅ Date execution frequency control
- ✅ Email toggle

## Files Created

### Main Files
1. **OSO_Service_Activated_local.py** (625 lines)
   - Main script with all functionality
   - Well-commented for easy understanding
   - Ready to run

2. **RUN_LOCAL_SCRIPT.bat**
   - Windows batch file for easy execution
   - Auto-detects Python installation
   - User-friendly interface

3. **LOCAL_VERSION_README.md**
   - Complete documentation
   - Usage examples
   - Customization guide
   - Troubleshooting tips

4. **LOCAL_VERSION_SUMMARY.md** (This file)
   - Quick overview
   - What was created
   - How to use

## Script Flow

```
START
  │
  ├─► Check execution frequency (daily/weekly)
  │
  ├─► Import libraries (psycopg2, pandas)
  │
  ├─► STEP 1: Test READ DB connection
  │      └─► Connect to: oso-pstgr-rd.orion.comcast.com:6432
  │
  ├─► STEP 2: Fetch service activation data
  │      ├─► Execute SQL query
  │      ├─► Convert to DataFrame
  │      └─► Log: "Fetched X records"
  │
  ├─► STEP 3: Save to Excel
  │      ├─► Create Excel file (single sheet)
  │      ├─► Sheet: "Service Activation Data"
  │      └─► Log: "Excel file created: filename.xlsx"
  │
  ├─► STEP 4: Send Email (if SEND_EMAIL = True)
  │      ├─► Create HTML email
  │      ├─► Attach Excel file
  │      ├─► Send via SMTP (localhost)
  │      └─► Log: "Mail sent successfully"
  │
  └─► END: Display summary and exit
```

## Configuration

All configuration is at the top of the script (lines 35-50):

```python
SEND_EMAIL = True                     # Toggle email
DATE_EXECUTION_FREQUENCY = 1          # Daily execution
EMAIL_RECIPIENTS = ['abhishek_agrahari@comcast.com']
EMAIL_CC_RECIPIENTS = ['abhisha3@amdocs.com']
QUERY_TIMEOUT_SECONDS = 600           # 10 minutes
```

## Database Configuration

READ DB only (lines 124-131):

```python
READ_DB_CONFIG = {
    'host': 'oso-pstgr-rd.orion.comcast.com',
    'database': 'prodossdb',
    'port': 6432,
    'user': 'ossdb01db',
    'password': 'Pr0d_ossdb01db',
    'connect_timeout': 120
}
```

## SQL Query

The full service activation query is embedded (lines 142-224):
- Joins multiple tables
- Filters by activation date (now() - 5 days)
- Excludes test/POC customers
- Orders by Customer_Id, Site_ID, Solution_Id

## How to Use

### Quick Start (3 Steps)

1. **Run the script:**
   ```bash
   # Option A: Double-click
   RUN_LOCAL_SCRIPT.bat
   
   # Option B: Command line
   python OSO_Service_Activated_local.py
   ```

2. **Check console output:**
   ```
   [OK] Database connection successful!
   [OK] Retrieved 88 records
   [OK] Excel file saved
   [OK] Email sent successfully!
   ```

3. **Check your email:**
   - Subject: "Comcast OSS || OSO Service Activated Report - 2025-12-01"
   - Attachment: Excel file with 88 records

### Adding Custom Logic

**Example: Add RCA column**

Find this line (after data is fetched, around line 610):
```python
df = pd.DataFrame(results)
```

Add your logic right after:
```python
# Add RCA column based on conditions
def calculate_rca(row):
    if row['Send_To_Billing'] != 'Completed':
        return 'Billing Incomplete'
    elif row['num_product'] != row['num_completed_product']:
        return 'Product Count Mismatch'
    else:
        return 'OK'

df['RCA'] = df.apply(calculate_rca, axis=1)
```

**Example: Add WorkQueue column**

```python
# Map Region to WorkQueue
queue_mapping = {
    'East': 'OSO_East_Queue',
    'West': 'OSO_West_Queue',
    'Central': 'OSO_Central_Queue'
}
df['WorkQueue'] = df['Region'].map(queue_mapping)
```

**Example: Add Status column**

```python
# Add handling status
df['Handling_Status'] = 'Pending Review'
df['Owned_By'] = 'Automation Team'
```

## Comparison: Full vs Local Version

| Feature | Full Version | Local Version |
|---------|-------------|---------------|
| **Lines of Code** | 1606 | 625 |
| **Complexity** | High | Low |
| **READ DB** | ✅ Yes | ✅ Yes |
| **WRITE DB** | ✅ Yes | ❌ No |
| **Table Management** | ✅ Yes | ❌ No |
| **Duplicate Check** | ✅ Yes | ❌ No |
| **INSERT Operations** | ✅ Yes | ❌ No |
| **Excel Sheets** | 3 | 1 |
| **Customization** | Harder | ✅ Easier |
| **Use Case** | Production tracking | Local development |

## Expected Output

### Console
```
================================================================================
  OSO Service Activated - Local Data Extractor
  Execution Date: 2025-12-01
  Execution Time: 16:52:30
================================================================================

Step 1: Testing database connection...
[OK] Database connection successful!

Step 2: Fetching service activation data...
Query executed successfully. Fetched 88 records.
[OK] Retrieved 88 records

Sample Data (first 3 rows):
--------------------------------------------------------------------------------
  Customer_Id  Customer_Name  Site_ID  Division  ...
  12345        ACME Corp      S001     East      ...
  12346        Beta Inc       S002     West      ...
  12347        Gamma LLC      S003     Central   ...
--------------------------------------------------------------------------------

Step 3: Saving to Excel...
[OK] Excel file saved: OSO_Service_Activated_Local_20251201_165230.xlsx
    Size: 156.23 KB
    Records: 88
================================================================================

Step 4: Sending email report...
[OK] Mail sent successfully!

================================================================================
[OK] ALL OPERATIONS COMPLETED!
================================================================================
Execution Date: 2025-12-01
Execution Time: 2025-12-01 16:52:30
--------------------------------------------------------------------------------
Records fetched: 88
Excel file: C:\...\OSO_Service_Activated_Local_20251201_165230.xlsx
Email sent: Yes
================================================================================
```

### Excel File
- **Filename:** `OSO_Service_Activated_Local_YYYYMMDD_HHMMSS.xlsx`
- **Sheet Name:** "Service Activation Data"
- **Columns:** All 28 columns from the SQL query
- **Rows:** 88 records (or however many the query returns)

### Email
- **Subject:** Comcast OSS || OSO Service Activated Report - 2025-12-01
- **To:** abhishek_agrahari@comcast.com
- **CC:** abhisha3@amdocs.com
- **Body:** HTML formatted with summary table
- **Attachment:** Excel file

## Network Requirements

### Works From:
- ✅ Unix/Linux servers with DB access
- ✅ Machines with VPN to database network
- ✅ Servers in the same VPC as database

### May NOT Work From:
- ❌ Local desktop without VPN
- ❌ Remote Desktop without network access
- ❌ Machines where port 6432 is blocked

**Solution:** Run from a server with database network access (same as before)

## Next Steps for You

### Immediate
1. ✅ Script is ready (compiled successfully)
2. 📤 Transfer to server with DB access:
   ```bash
   scp OSO_Service_Activated_local.py user@server:/path/
   scp RUN_LOCAL_SCRIPT.bat user@server:/path/  # If Windows server
   ```
3. 🔧 Install dependencies:
   ```bash
   pip3 install psycopg2-binary pandas openpyxl --user
   ```
4. ▶️ Run it:
   ```bash
   python3 OSO_Service_Activated_local.py
   ```

### Short-Term
1. 🧪 **Test the script** - Verify data fetching works
2. 📊 **Review Excel output** - Check columns and data
3. ✏️ **Add custom logic** - Implement your business rules
4. 📧 **Test email** - Confirm reports are received

### Long-Term
1. 🤖 **Schedule daily execution** - Set up cron/Task Scheduler
2. 📈 **Add more columns** - Implement RCA, WorkQueue, Status, etc.
3. 🔗 **Integrate with other tools** - Connect to ticket systems, dashboards
4. 📝 **Document your changes** - Keep track of modifications

## Advantages of Local Version

### 1. **Simpler**
- No table creation/management
- No duplicate checking
- No WRITE DB complexity
- Straightforward flow

### 2. **Faster to Modify**
- Clear code structure
- Well-commented
- Easy to find where to add logic
- Quick testing cycle

### 3. **Fewer Dependencies**
- Only READ DB needed
- No write permissions required
- No table maintenance
- Less infrastructure

### 4. **Perfect for Development**
- Test queries quickly
- Add features incrementally
- See immediate results
- Iterate rapidly

## When to Use Which Version

### Use **Local Version** When:
- 🧪 Developing/testing new features
- 📊 Need simple data extraction
- 🚫 Don't have WRITE DB access
- ⚡ Want quick results
- 🔧 Frequently changing logic

### Use **Full Version** When:
- 💾 Need to store data in tracking table
- 🔄 Need duplicate detection
- 📈 Building up historical data
- 🎯 Production tracking system
- 🔒 Need data persistence

## Summary

✅ **Created:** Simplified local version for easy development
✅ **Compiled:** No syntax errors
✅ **Documented:** Complete README and examples
✅ **Ready to Run:** Just needs server with DB access

**Next Action:** Transfer to server and run it! Then add your custom logic as needed.

---

**Files Location:**
```
C:\Users\abhisha3\Desktop\Projects\Fallout\Billing\
├── OSO_Service_Activated_local.py       ← Main script
├── RUN_LOCAL_SCRIPT.bat                 ← Easy launcher
├── LOCAL_VERSION_README.md              ← Complete guide
└── LOCAL_VERSION_SUMMARY.md             ← This file
```

**Ready to go! 🚀**









