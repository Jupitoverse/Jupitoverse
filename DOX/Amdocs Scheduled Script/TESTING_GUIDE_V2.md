# Testing Guide - Outage_v2.py Enhanced Version

## 🧪 Quick Testing Checklist

### ✅ Pre-Run Checks

1. **Database Connection**
   - Host: `oso-pstgr-rd.orion.comcast.com`
   - Port: `6432`
   - Database: `prodossdb`
   - User: `ossdb01uams`

2. **Dependencies**
   ```bash
   pip install pandas psycopg2 openpyxl
   ```

3. **Date Execution Check**
   - Script runs only on days where: `day_of_month % 1 == 0`
   - Currently set to run every day (frequency = 1)

---

## 🚀 Running the Script

### Standard Execution
```bash
cd "C:\Users\abhisha3\Desktop\Projects\Amdocs Scheduled Script"
python Outage_v2.py
```

### Expected Console Output
```
2025-11-14 10:00:00 - INFO - Date condition met. Proceeding with script execution.
2025-11-14 10:00:01 - INFO - Database connection established successfully.
2025-11-14 10:00:02 - INFO - Executed Stuck Project Count Query
2025-11-14 10:00:03 - INFO - Executed Stuck Project Query
2025-11-14 10:00:04 - INFO - Executed Interface Summary batch query for part_ids: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
2025-11-14 10:00:05 - INFO - Executed Interface Summary batch query for part_ids: [11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
...
2025-11-14 10:00:15 - INFO - Executed Activity batch query for part_ids: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
...
2025-11-14 10:00:30 - INFO - Mail sent successfully!
```

---

## 📊 Verifying Output

### 1. Check Excel File

**Location:** `Orion Outage Report for YYYY/MM/DD/Abhi.xlsx`

**Expected Sheets:**
1. ✅ `Summary` - Project count summary
2. ✅ `Projects` - Stuck projects list
3. ✅ `Interface Summary` ⭐ NEW - Interface-wise count
4. ✅ `Activities` - Activity details with 11 columns

**Verify Interface Summary Sheet:**
- Column 1: `Interface` (text)
- Column 2: `Count (Last 24 Hours)` (number)
- Sorted by count (descending)
- No null values in Interface column

**Verify Activities Sheet:**
- Column 1: `Activity Name`
- Column 2: `Spec Id`
- Column 3: `Interface`
- Column 4: `Last 1 Hour` ⭐ NEW
- Column 5: `Last 6 Hours` ⭐ NEW
- Column 6: `Last 12 Hours` ⭐ NEW
- Column 7: `Last 24 Hours`
- Column 8: `Previous 24 Hours`
- Column 9: `Last 1 Week`
- Column 10: `Last 1 Month`
- Column 11: `Last 1 Year`

---

### 2. Check Email

**Recipients:**
- abhisha3@amdocs.com
- Enna.Arora@amdocs.com
- Nishant.Bhatia@amdocs.com
- prateek.jain5@amdocs.com
- mukul.bhasin@amdocs.com
- Alon.Kugel@Amdocs.com
- Shreyas.Kulkarni@amdocs.com
- Smitesh.Kadia@amdocs.com

**Subject:** `Comcast OSS || Orion Outage Report for YYYY/MM/DD`

**Expected Email Structure:**
1. ✅ Greeting and introduction
2. ✅ Table 1: Count of Stuck Projects
3. ✅ Table 2: List of Stuck Projects
4. ✅ Table 3: Interface-wise Activity Count ⭐ NEW
5. ✅ Table 4: Stuck Activities (with 11 columns)
6. ✅ Footer with contact info
7. ✅ Excel attachment

**Verify Table 3 (Interface Summary):**
- Has heading: "Interface-wise Activity Count (Last 24 Hours)"
- Has description paragraph
- Table has 2 columns: Interface, Count (Last 24 Hours)
- Styled with borders and proper formatting

**Verify Table 4 (Activities):**
- Has 11 columns (3 new ones added)
- Columns are in correct order
- Data is sorted by "Last 24 Hours" descending

---

## 🔍 Manual Database Verification

### Query 1: Verify Interface Summary Data
```sql
SELECT aocd.interface AS Interface,
       COUNT(*) AS "Count (Last 24 Hours)"
FROM ossdb01db.oss_activity_instance oai
JOIN ossdb01db.activity_overview_custom_data aocd ON oai.spec_ver_id = aocd.spec_id
WHERE oai.part_id BETWEEN 1 AND 10
  AND oai.actual_start_date >= NOW() - INTERVAL '1 day'
  AND oai.actual_start_date < NOW()
  AND oai.last_update_date > NOW() - INTERVAL '1 year'
  AND oai.state IN ('In Progress', 'Rework In Progress')
  AND oai.is_latest_version = 1
  AND oai.implementation_type <> 'Manual'
GROUP BY aocd.interface
ORDER BY "Count (Last 24 Hours)" DESC;
```

**Expected Result:**
- List of interfaces with counts
- No null interfaces
- Counts should be positive integers

---

### Query 2: Verify Time Interval Data
```sql
SELECT 
    SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '1 hour' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS "Last 1 Hour",
    SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '6 hours' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS "Last 6 Hours",
    SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '12 hours' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS "Last 12 Hours",
    SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '1 day' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS "Last 24 Hours"
FROM ossdb01db.oss_activity_instance oai
WHERE oai.part_id BETWEEN 1 AND 10
  AND oai.last_update_date > NOW() - INTERVAL '1 year'
  AND oai.state IN ('In Progress', 'Rework In Progress')
  AND oai.is_latest_version = 1
  AND oai.implementation_type <> 'Manual';
```

**Expected Result:**
- 4 columns with counts
- Last 1 Hour ≤ Last 6 Hours ≤ Last 12 Hours ≤ Last 24 Hours
- All values should be non-negative

---

## 🐛 Common Issues & Solutions

### Issue 1: Missing Interface Summary Sheet
**Symptom:** Excel file only has 3 sheets instead of 4

**Solution:**
- Check if `df_interface_summary` is empty
- Verify database query returns data
- Check part_ids range (1-99)

---

### Issue 2: New Time Interval Columns Show Zero
**Symptom:** Last 1 Hour, Last 6 Hours, Last 12 Hours all show 0

**Solution:**
- Check if there are any activities in those time ranges
- Verify `actual_start_date` field is populated
- Run manual query to confirm data exists

---

### Issue 3: Email Table 3 Not Showing
**Symptom:** Email only shows 3 tables instead of 4

**Solution:**
- Check if `html_interface_summary` variable is defined
- Verify the email template includes `{html_interface_summary}`
- Check for any HTML rendering errors

---

### Issue 4: Column Order Wrong in Activities Table
**Symptom:** New columns appear at the end instead of beginning

**Solution:**
- Verify DataFrame column order in aggregation
- Check if column names match exactly (case-sensitive)
- Ensure groupby aggregation includes all columns

---

## 📋 Test Scenarios

### Scenario 1: Normal Execution
- **Input:** Run script on a valid execution day
- **Expected:** 4 sheets in Excel, 4 tables in email, mail sent successfully
- **Verify:** All new columns and table present

---

### Scenario 2: No Data for Interface Summary
- **Input:** Run script when no activities in last 24 hours
- **Expected:** Interface Summary sheet exists but is empty
- **Verify:** No errors, email still sent

---

### Scenario 3: No Data for New Time Intervals
- **Input:** Run script when no activities in last 1/6/12 hours
- **Expected:** New columns show 0, but other columns have data
- **Verify:** Script completes successfully

---

## ✅ Success Criteria

All of the following must be true:

- [ ] Script runs without errors
- [ ] Excel file created in correct folder
- [ ] Excel file has 4 sheets (not 3)
- [ ] Interface Summary sheet has data (if activities exist)
- [ ] Activities sheet has 11 columns (not 8)
- [ ] New columns: Last 1 Hour, Last 6 Hours, Last 12 Hours present
- [ ] Email sent successfully
- [ ] Email contains 4 tables (not 3)
- [ ] Table 3 is "Interface-wise Activity Count"
- [ ] Table 4 has 11 columns
- [ ] Excel file attached to email
- [ ] No Python errors in console
- [ ] Database connection closed properly

---

## 🔧 Quick Fixes

### If Script Fails:

1. **Check Database Connection**
   ```bash
   psql -h oso-pstgr-rd.orion.comcast.com -p 6432 -U ossdb01uams -d prodossdb
   ```

2. **Verify Dependencies**
   ```bash
   pip list | findstr "pandas psycopg2 openpyxl"
   ```

3. **Check Logs**
   - Look for ERROR level messages in console output
   - Check for database connection errors
   - Verify email server is accessible

4. **Test Queries Manually**
   - Run Interface_Summary query in database
   - Run Stuck_Activity query in database
   - Verify data exists for current time ranges

---

## 📞 Support

For issues or questions:
- **Email:** abhisha3@amdocs.com
- **Script Location:** `C:\Users\abhisha3\Desktop\Projects\Amdocs Scheduled Script\Outage_v2.py`
- **Documentation:** See `OUTAGE_V2_ENHANCEMENTS.md` and `BEFORE_AFTER_COMPARISON.md`

---

**Last Updated:** November 14, 2025  
**Version:** 2.1





