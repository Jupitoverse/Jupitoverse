# Outage_v2.py - CLIPS & Test Mode Update

## 📋 Changes Summary

### ✅ 1. TEST_MODE Toggle Added

A new **TEST_MODE** toggle has been added at the top of the script to control email recipients.

**Location:** Lines 17-23

```python
# ============================================
# TEST MODE TOGGLE
# ============================================
# Set to True for testing (sends email to abhisha3@amdocs.com only)
# Set to False for production (sends to all recipients)
TEST_MODE = True
# ============================================
```

**Behavior:**
- **TEST_MODE = True**: 
  - Email sent to `abhisha3@amdocs.com` only
  - No CC recipients
  - Subject includes `[TEST MODE]` prefix
  - Logs: "TEST_MODE is ON - Sending email to abhisha3@amdocs.com only"

- **TEST_MODE = False**:
  - Email sent to all production recipients
  - CC: `abhisha3@amdocs.com`
  - Normal subject line
  - Logs: "TEST_MODE is OFF - Sending email to all recipients"

---

### ✅ 2. Additional Excluded spec_ver_ids

**10 new spec_ver_ids** have been added to the exclusion list across all queries:

```
8dd6c6d1-b87b-4aa5-8bc9-d277a2ed21de
6e30691c-a411-48a2-b60b-5a81309dea95
02237fa6-6a9c-4704-b59e-150d3f3f10b0
dcf796be-d4f4-409d-9a45-77272aab2423
976db4b1-b94c-4146-ab56-9b442f37cde3
d48edea5-5eb0-4f2c-bc50-805dd3196d7e
3245250b-6c2f-4f59-898c-a33646e9494c
c8f0a6c5-ccb2-4251-9d78-7cd2200f7031
756cbaf8-2e32-438b-8a1d-7e6708132725
46ca1e5e-4f6a-41eb-9522-11925fc1d911
```

**Total excluded spec_ver_ids:** 58 (was 48, added 10)

**Applied to:**
- Interface Summary query
- Activity Summary query
- CLIPS Count Summary query
- CLIPS Activity Summary query

---

### ✅ 3. CLIPS Stuck Activities Count Table

**New Table:** Shows total count of stuck activities for CLIPS-related interfaces (USM, ARM, ASD).

**Query:** `CLIPS_Count_Summary`

**Filters:**
- `aocd.interface IN ('USM', 'ARM', 'ASD')`
- All standard filters (state, version, implementation_type)
- All 58 excluded spec_ver_ids

**Columns (8 time intervals):**
1. Last 1 Hour
2. Last 6 Hours
3. Last 12 Hours
4. Last 24 Hours
5. Previous 24 Hours
6. Last 1 Week
7. Last 1 Month
8. Last 1 Year

**Output:**
- **Email:** Table 4 "CLIPS Stuck Activities Count (USM + ARM + ASD)"
- **Excel:** Sheet 5 "CLIPS Count"

**Example:**

| Last 1 Hour | Last 6 Hours | Last 12 Hours | Last 24 Hours | Previous 24 Hours | Last 1 Week | Last 1 Month | Last 1 Year |
|-------------|--------------|---------------|---------------|-------------------|-------------|--------------|-------------|
| 8           | 25           | 43            | 57            | 48                | 215         | 870          | 4200        |

---

### ✅ 4. CLIPS-Specific Activity Summary Table

**New Table:** Detailed activity breakdown filtered by CLIPS interfaces (USM, ARM, ASD).

**Query:** `CLIPS_Activity_Summary`

**Filters:**
- `aocd.interface IN ('USM', 'ARM', 'ASD')`
- All standard filters (state, version, implementation_type)
- All 58 excluded spec_ver_ids

**Columns (11 total):**
1. Activity Name
2. Spec Id
3. Interface
4. Last 1 Hour
5. Last 6 Hours
6. Last 12 Hours
7. Last 24 Hours
8. Previous 24 Hours
9. Last 1 Week
10. Last 1 Month
11. Last 1 Year

**Output:**
- **Email:** Table 5 "CLIPS-Specific Activity Summary (USM, ARM, ASD Interfaces Only)"
- **Excel:** Sheet 6 "CLIPS Activities"

**Example:**

| Activity Name | Spec Id | Interface | Last 1 Hr | Last 6 Hrs | Last 12 Hrs | Last 24 Hrs | ... |
|---------------|---------|-----------|-----------|------------|-------------|-------------|-----|
| Process Order | abc-123 | ARM       | 3         | 10         | 18          | 25          | ... |
| Update Inventory | def-456 | USM    | 2         | 7          | 12          | 18          | ... |
| Validate Data | ghi-789 | ASD       | 3         | 8          | 13          | 14          | ... |

---

## 📊 Complete Report Structure (Updated)

### Email Report (7 Tables):
1. **Count of Stuck Projects** (2 columns)
2. **List of Stuck Projects** (9 columns)
3. **Interface-wise Activity Count** (9 columns)
4. **CLIPS Stuck Activities Count** ⭐ NEW (8 columns)
5. **CLIPS-Specific Activity Summary** ⭐ NEW (11 columns)
6. **Stuck Activities Summary** (11 columns)

### Excel File (6 Sheets):
1. **Summary** - Project count summary
2. **Projects** - Stuck projects details
3. **Interface Summary** - Interface-wise count (9 columns)
4. **Activities** - Activity details (11 columns)
5. **CLIPS Count** ⭐ NEW - CLIPS total count (8 columns)
6. **CLIPS Activities** ⭐ NEW - CLIPS activity details (11 columns)

---

## 🎯 Use Cases

### Use Case 1: CLIPS Outage Analysis

**Scenario:** CLIPS system is down, need to see impact

**Steps:**
1. Check **Table 4: CLIPS Stuck Activities Count**
   - See total count across USM, ARM, ASD interfaces
   - Example: "Last 1 Hour: 8 stuck" means 8 new CLIPS-related activities stuck

2. Drill into **Table 5: CLIPS-Specific Activity Summary**
   - See which specific activities are stuck
   - Identify which interface (USM, ARM, or ASD) has most issues

**Example:**
```
Table 4 shows: 8 stuck in last hour
Table 5 breakdown:
  - ARM: 3 stuck (Process Order activity)
  - USM: 2 stuck (Update Inventory activity)
  - ASD: 3 stuck (Validate Data activity)

Action: Contact CLIPS team about these 3 activities
```

---

### Use Case 2: Testing New Changes

**Scenario:** Made changes to the script, want to test before production

**Steps:**
1. Set `TEST_MODE = True` at line 22
2. Run the script
3. Check your email (abhisha3@amdocs.com only)
4. Verify all tables look correct
5. Set `TEST_MODE = False` for production
6. Run again to send to all recipients

**Benefits:**
- No spam to production recipients during testing
- Easy to identify test emails with `[TEST MODE]` prefix
- Quick toggle between test and production

---

### Use Case 3: Compare CLIPS vs All Interfaces

**Question:** What percentage of stuck activities are CLIPS-related?

**Answer:** Compare Table 3 (all interfaces) vs Table 4 (CLIPS only)

**Example:**
```
Table 3 (Interface Summary):
  Last 24 Hours Total: 118 stuck activities

Table 4 (CLIPS Count):
  Last 24 Hours: 57 stuck activities

Calculation: 57/118 = 48% of stuck activities are CLIPS-related
```

---

## 🔧 Technical Details

### Query Structure: CLIPS Count Summary

```sql
SELECT 
  SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '1 hour' ...) AS "Last 1 Hour",
  SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '6 hours' ...) AS "Last 6 Hours",
  -- ... more time intervals
FROM ossdb01db.oss_activity_instance oai
JOIN ossdb01db.activity_overview_custom_data aocd ON oai.spec_ver_id = aocd.spec_id
WHERE oai.part_id in ({batch_ids})
  AND aocd.interface IN ('USM', 'ARM', 'ASD')  ← CLIPS filter
  AND oai.spec_ver_id NOT IN (...)  ← 58 excluded IDs
```

### Query Structure: CLIPS Activity Summary

```sql
SELECT 
  ord.entity_name AS "Activity Name",
  oai.spec_ver_id AS "Spec Id",
  aocd.interface AS Interface,
  SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '1 hour' ...) AS "Last 1 Hour",
  -- ... more time intervals
FROM ossdb01db.oss_activity_instance oai
JOIN ossdb01ref.oss_ref_attribute ora ON oai.spec_ver_id = ora.attribute_value
JOIN ossdb01ref.oss_ref_data ord ON ora.entity_id = ord.entity_id
JOIN ossdb01db.activity_overview_custom_data aocd ON oai.spec_ver_id = aocd.spec_id
WHERE oai.part_id in ({batch_ids})
  AND aocd.interface IN ('USM', 'ARM', 'ASD')  ← CLIPS filter
  AND oai.spec_ver_id NOT IN (...)  ← 58 excluded IDs
GROUP BY ord.entity_name, oai.spec_ver_id, aocd.interface
ORDER BY "Last 24 Hours" DESC;
```

---

## 📧 Email Subject Changes

### Test Mode:
```
Subject: [TEST MODE] Comcast OSS || Orion Outage Report for 2025/11/14
```

### Production Mode:
```
Subject: Comcast OSS || Orion Outage Report for 2025/11/14
```

---

## 📈 Data Flow

```
1. Execute CLIPS Count Summary query (batched)
   ↓
2. Aggregate results across all batches
   ↓
3. Create df_clips_count_total DataFrame (1 row, 8 columns)
   ↓
4. Execute CLIPS Activity Summary query (batched)
   ↓
5. Aggregate results across all batches
   ↓
6. Group by Activity Name, Spec Id, Interface
   ↓
7. Create df_clips_activity DataFrame (N rows, 11 columns)
   ↓
8. Sort by "Last 24 Hours" descending
   ↓
9. Export to Excel (Sheets 5 & 6)
   ↓
10. Generate HTML tables
   ↓
11. Include in email (Tables 4 & 5)
```

---

## ✅ Verification Checklist

After running the script:

- [ ] Excel file has **6 sheets** (not 4)
- [ ] Sheet 5 is "CLIPS Count" with 8 columns
- [ ] Sheet 6 is "CLIPS Activities" with 11 columns
- [ ] Email has **6 tables** (not 4)
- [ ] Table 4 is "CLIPS Stuck Activities Count"
- [ ] Table 5 is "CLIPS-Specific Activity Summary"
- [ ] TEST_MODE = True sends to abhisha3@amdocs.com only
- [ ] TEST_MODE = True adds "[TEST MODE]" to subject
- [ ] TEST_MODE = False sends to all recipients
- [ ] CLIPS tables only show USM, ARM, ASD interfaces
- [ ] All 58 spec_ver_ids are excluded

---

## 🚀 Quick Start

### For Testing:
```python
# Line 22: Set TEST_MODE
TEST_MODE = True

# Run script
python Outage_v2.py

# Check email at abhisha3@amdocs.com
```

### For Production:
```python
# Line 22: Set TEST_MODE
TEST_MODE = False

# Run script
python Outage_v2.py

# Email sent to all recipients
```

---

## 📞 Support

For questions or issues:
- **Email:** abhisha3@amdocs.com
- **Documentation:** See other .md files in this folder

---

**Last Updated:** November 14, 2025  
**Version:** 2.3 (CLIPS + Test Mode)





