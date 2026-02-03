# OSO_Service_Activated_local.py - Simplified Local Version

## Overview

This is a **simplified version** of the OSO Service Activated script designed for:
- ✅ Local development and testing
- ✅ Easy addition of custom logic
- ✅ No WRITE DB dependency
- ✅ Simple single-sheet Excel export
- ✅ Email reporting

## What It Does

```
┌─────────────────┐
│  READ DB        │
│  (PostgreSQL)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Run Query      │
│  Fetch Data     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  DataFrame      │
│  (88 records)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Export Excel   │
│  (Single Sheet) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Send Email     │
│  (with attach)  │
└─────────────────┘
```

## Key Differences from Full Version

| Feature | Full Version | Local Version |
|---------|-------------|---------------|
| READ DB | ✅ Yes | ✅ Yes |
| WRITE DB | ✅ Yes | ❌ No |
| Table Creation | ✅ Yes | ❌ No |
| Duplicate Check | ✅ Yes | ❌ No |
| INSERT Operations | ✅ Yes | ❌ No |
| Excel Sheets | 3 (All, NEW, EXISTING) | 1 (Service Activation Data) |
| Email | ✅ Yes | ✅ Yes |
| Custom Logic | ❌ Fixed | ✅ Easy to add |

## Quick Start

### 1. Run the Script

**Double-click the batch file:**
```
RUN_LOCAL_SCRIPT.bat
```

**Or run directly:**
```bash
python OSO_Service_Activated_local.py
```

### 2. Expected Output

```
================================================================================
  OSO Service Activated - Local Data Extractor
  Execution Date: 2025-12-01
================================================================================

Step 1: Testing database connection...
[OK] Database connection successful!

Step 2: Fetching service activation data...
[OK] Retrieved 88 records

Step 3: Saving to Excel...
[OK] Excel file saved: OSO_Service_Activated_Local_20251201_165230.xlsx
    Size: 156.23 KB
    Records: 88

Step 4: Sending email report...
[OK] Email sent successfully!

================================================================================
[OK] ALL OPERATIONS COMPLETED!
================================================================================
```

### 3. Check Your Email

You'll receive:
- **Subject:** Comcast OSS || OSO Service Activated Report - 2025-12-01
- **Attachment:** OSO_Service_Activated_Local_YYYYMMDD_HHMMSS.xlsx
  - Single sheet: "Service Activation Data"
  - 88 records with all columns

## Configuration

Edit the script to customize:

### Email Recipients (Lines 45-46)
```python
EMAIL_RECIPIENTS = ['abhishek_agrahari@comcast.com']
EMAIL_CC_RECIPIENTS = ['abhisha3@amdocs.com']
```

### Execution Frequency (Line 42)
```python
DATE_EXECUTION_FREQUENCY = 1  # 1 = daily, 7 = weekly, etc.
```

### Email Toggle (Line 38)
```python
SEND_EMAIL = True  # Set to False to skip email
```

### Query Timeout (Line 49)
```python
QUERY_TIMEOUT_SECONDS = 600  # 10 minutes
```

## Adding Your Custom Logic

### Example 1: Add a New Calculated Column

**Location:** After line 609 (after DataFrame is created)

```python
# Add custom column
df_data['My_Custom_Column'] = df_data['Customer_Id'].apply(lambda x: x[:5] + '_Custom')

# Add another calculation
df_data['Days_Since_Activation'] = (pd.Timestamp.now() - pd.to_datetime(df_data['Activation_Date'])).dt.days
```

### Example 2: Filter Data Before Export

**Location:** After line 609

```python
# Filter only specific regions
df_data = df_data[df_data['Region'].isin(['East', 'West'])]

# Filter by activation date
df_data = df_data[pd.to_datetime(df_data['Activation_Date']) >= '2024-01-01']
```

### Example 3: Add Data Enrichment

**Location:** After line 609

```python
# Example: Add RCA based on conditions
def determine_rca(row):
    if row['Send_To_Billing'] != 'Completed':
        return 'Billing Not Complete'
    elif int(row['num_product']) != int(row['num_completed_product']):
        return 'Product Mismatch'
    else:
        return 'OK'

df_data['RCA'] = df_data.apply(determine_rca, axis=1)

# Example: Add WorkQueue based on Region
queue_mapping = {
    'East': 'Queue_East_Team',
    'West': 'Queue_West_Team',
    'Central': 'Queue_Central_Team'
}
df_data['WorkQueue'] = df_data['Region'].map(queue_mapping)
```

### Example 4: Create Summary Statistics

**Location:** Before Excel export (line 618)

```python
# Create summary before export
summary = df_data.groupby('Region').agg({
    'Service_Id': 'count',
    'Customer_Id': 'nunique'
}).reset_index()

print("\n" + "=" * 80)
print("SUMMARY BY REGION:")
print(summary.to_string())
print("=" * 80)
```

### Example 5: Multi-Sheet Excel with Custom Logic

**Location:** Replace the `save_to_excel` call (line 656)

```python
# Modified Excel export with multiple sheets
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
filename = f"OSO_Service_Activated_Local_{timestamp}.xlsx"

with pd.ExcelWriter(filename, engine='openpyxl') as writer:
    # Sheet 1: All data
    df_data.to_excel(writer, index=False, sheet_name='All Data')
    
    # Sheet 2: By Region
    for region in df_data['Region'].unique():
        region_data = df_data[df_data['Region'] == region]
        sheet_name = f'Region_{region}'[:31]  # Excel sheet name limit
        region_data.to_excel(writer, index=False, sheet_name=sheet_name)
    
    # Sheet 3: Summary
    summary = df_data.groupby('Region').size().reset_index(name='Count')
    summary.to_excel(writer, index=False, sheet_name='Summary')

excel_file = os.path.abspath(filename)
print(f"[OK] Multi-sheet Excel created: {filename}")
```

## Common Modifications

### Modify the SQL Query

**Location:** Lines 142-224 (SERVICE_ACTIVATION_QUERY)

```python
# Add additional filters
SERVICE_ACTIVATION_QUERY = """
... existing query ...
where da.is_latest = 1
and dpv.product_agreement_instance_id is not null
and dso.region = 'East'  -- ADD YOUR FILTER HERE
...
"""
```

### Add Logging for Custom Steps

```python
logger.info("Starting custom processing...")
# Your custom code
logger.info("Custom processing completed")
```

### Change Excel Filename

**Location:** Line 632 in `save_to_excel()`

```python
filename = f"MyCustomReport_{timestamp}.xlsx"
```

## Dependencies

Required Python packages:
```bash
pip install psycopg2-binary pandas openpyxl
```

## Troubleshooting

### Database Connection Failed

**Error:** `[ERROR] Database connection failed`

**Solution:**
- Run from a server with database network access
- Check VPN connection
- Verify READ_DB_CONFIG credentials (lines 124-131)

### No Data Returned

**Error:** `[OK] Retrieved 0 records`

**Solution:**
- Check SQL query filters
- Verify activation_date range
- Check database has data for the query

### Email Failed

**Error:** `[WARNING] Email sending failed`

**Solution:**
- Verify SMTP server is accessible (`localhost`)
- Check email recipients are valid
- Review logs for specific SMTP errors

### Excel Export Failed

**Error:** `[ERROR] Failed to save Excel`

**Solution:**
- Ensure write permissions in current directory
- Check disk space
- Verify `openpyxl` is installed

## File Structure

```
Fallout/Billing/
├── OSO_Service_Activated_local.py    ← Main script (simplified)
├── RUN_LOCAL_SCRIPT.bat              ← Batch file to run script
├── LOCAL_VERSION_README.md           ← This file
├── OSO_Service_Activated.py          ← Full version (with WRITE DB)
└── OSO_Service_Activated_Local_*.xlsx ← Generated Excel files
```

## Example Workflow

### Daily Monitoring (No Custom Logic)
1. Run script daily via scheduler
2. Receive email with Excel
3. Review data manually

### Custom Processing (With Logic)
1. Add custom columns in script
2. Add filtering logic
3. Run script
4. Get enriched Excel report

### Development & Testing
1. Modify script locally
2. Test with `python OSO_Service_Activated_local.py`
3. Review Excel output
4. Iterate until satisfied
5. Schedule for production

## Next Steps

1. ✅ **Run the script** to verify it works
2. 📝 **Add your custom logic** where needed
3. 🧪 **Test your modifications** locally
4. 📅 **Schedule for daily execution** (if needed)
5. 📊 **Review Excel reports** and iterate

## Support

- For database issues: Contact DBA team
- For network access: Check with Network/Security team
- For script modifications: Refer to examples above
- For Python help: Check Python documentation

---

## Key Advantages of Local Version

✅ **Simpler** - No table management, no duplicate checking
✅ **Faster Development** - Easy to add custom logic
✅ **Fewer Dependencies** - Only READ DB needed
✅ **Clear Code** - Well-commented, easy to understand
✅ **Flexible** - Modify query, add columns, change logic easily

Perfect for **rapid development** and **custom data processing**! 🚀

---

**Ready to use!** Just run `RUN_LOCAL_SCRIPT.bat` and check your email!









