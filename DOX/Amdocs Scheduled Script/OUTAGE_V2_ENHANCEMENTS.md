# Outage_v2.py Enhancements Summary

## 📋 Changes Made

### ✅ 1. Added More Time Intervals to Activity Summary Table

The Activity Summary table now includes **3 additional time intervals**:

**New Columns Added:**
- `Last 1 Hour` - Activities stuck in the last 1 hour
- `Last 6 Hours` - Activities stuck in the last 6 hours  
- `Last 12 Hours` - Activities stuck in the last 12 hours

**Updated Column Order:**
1. Activity Name
2. Spec Id
3. Interface
4. **Last 1 Hour** ⭐ NEW
5. **Last 6 Hours** ⭐ NEW
6. **Last 12 Hours** ⭐ NEW
7. Last 24 Hours
8. Previous 24 Hours
9. Last 1 Week
10. Last 1 Month
11. Last 1 Year

---

### ✅ 2. Added Interface-wise Summary Table

A **new table** has been added that shows the count of stuck activities **grouped by Interface** for the last 24 hours.

**Table Structure:**
| Interface | Count (Last 24 Hours) |
|-----------|----------------------|
| ARM       | 34                   |
| OGW       | 23                   |
| ...       | ...                  |

**Features:**
- Shows total count per Interface
- Sorted by count (descending)
- Only includes activities from the last 24 hours
- Helps identify which interfaces have the most stuck activities

---

## 📊 Report Structure (Updated)

### Email Report Order:
1. **Count of Stuck Projects** (Summary table)
2. **List of Stuck Projects** (Detailed project list)
3. **Interface-wise Activity Count** ⭐ NEW TABLE
4. **Stuck Activities with Time Intervals** (Enhanced with 3 new columns)

### Excel File Sheets:
1. `Summary` - Project count summary
2. `Projects` - Stuck projects details
3. `Interface Summary` ⭐ NEW SHEET - Interface-wise count
4. `Activities` - Activity details with enhanced time intervals

---

## 🔍 Technical Details

### New Query Added: `Interface_Summary`
```sql
SELECT aocd.interface AS Interface,
       COUNT(*) AS "Count (Last 24 Hours)"
FROM ossdb01db.oss_activity_instance oai
JOIN ossdb01db.activity_overview_custom_data aocd ON oai.spec_ver_id = aocd.spec_id
WHERE oai.part_id in ({batch_ids})
  AND oai.actual_start_date >= NOW() - INTERVAL '1 day'
  AND oai.actual_start_date < NOW()
  -- ... (same filters as activity query)
GROUP BY aocd.interface
ORDER BY "Count (Last 24 Hours)" DESC;
```

### Enhanced Query: `Stuck_Activity`
Added three new time interval calculations:
- `INTERVAL '1 hour'`
- `INTERVAL '6 hours'`
- `INTERVAL '12 hours'`

---

## 🎯 Benefits

1. **Faster Issue Detection**: 1-hour, 6-hour, and 12-hour intervals help identify issues more quickly
2. **Interface-level Visibility**: Quickly see which interfaces are experiencing the most problems
3. **Better Trend Analysis**: More granular time intervals allow for better pattern recognition
4. **Improved Prioritization**: Interface summary helps teams prioritize which areas need attention

---

## 📧 Email Report Preview

The email now includes:

```
Hi Team,

...

[Table 1: Count of Stuck Projects]

[Table 2: List of Stuck Projects]

[Table 3: Interface-wise Activity Count (Last 24 Hours)] ⭐ NEW
This table shows the count of stuck activities grouped by Interface for the last 24 hours.

[Table 4: Stuck Activities with Enhanced Time Intervals]
Now includes: Last 1 Hour, Last 6 Hours, Last 12 Hours, Last 24 Hours, ...

...
```

---

## 🚀 Usage

The script works exactly the same way as before:

```bash
python Outage_v2.py
```

**Output:**
- Excel file: `Orion Outage Report for YYYY/MM/DD/Abhi.xlsx`
- Email sent to configured recipients with all 4 tables

---

## 📝 Notes

- All existing functionality remains unchanged
- The script still uses batched queries for performance
- Database connection and error handling remain the same
- Email recipients and configuration unchanged

---

**Last Updated:** November 14, 2025  
**Modified By:** AI Assistant  
**Version:** 2.1





