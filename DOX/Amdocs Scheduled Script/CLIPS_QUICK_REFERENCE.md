# CLIPS Features - Quick Reference

## 🎯 What is CLIPS?

**CLIPS** = **C**ombined **L**egacy **I**nterface **P**latform **S**ervice

Interfaces tracked: **USM, ARM, ASD**

---

## 📊 New Tables

### Table 4: CLIPS Count
**Purpose:** Total count of stuck activities for CLIPS interfaces

**Columns:** 8 (all time intervals)

**Example:**
| Last 1 Hr | Last 6 Hrs | Last 12 Hrs | Last 24 Hrs | ... |
|-----------|------------|-------------|-------------|-----|
| 8         | 25         | 43          | 57          | ... |

---

### Table 5: CLIPS Activities
**Purpose:** Detailed breakdown by activity

**Columns:** 11 (Activity Name + Spec Id + Interface + 8 time intervals)

**Example:**
| Activity | Spec Id | Interface | Last 1 Hr | ... |
|----------|---------|-----------|-----------|-----|
| Process Order | abc-123 | ARM | 3 | ... |
| Update Inv | def-456 | USM | 2 | ... |

---

## 🔧 TEST_MODE

### Enable Test Mode
```python
# Line 22 in Outage_v2.py
TEST_MODE = True
```

**Result:**
- ✅ Email to abhisha3@amdocs.com only
- ✅ Subject: `[TEST MODE] Comcast OSS || Orion Outage Report...`
- ✅ No spam to production users

### Enable Production Mode
```python
# Line 22 in Outage_v2.py
TEST_MODE = False
```

**Result:**
- ✅ Email to all recipients
- ✅ Subject: `Comcast OSS || Orion Outage Report...`
- ✅ CC: abhisha3@amdocs.com

---

## 📧 Email Structure

```
Table 1: Project Count
Table 2: Project List
Table 3: Interface Summary (all interfaces)
Table 4: CLIPS Count (USM+ARM+ASD) ⭐
Table 5: CLIPS Activities (USM+ARM+ASD) ⭐
Table 6: All Activities
```

---

## 📁 Excel Structure

```
Sheet 1: Summary
Sheet 2: Projects
Sheet 3: Interface Summary
Sheet 4: Activities
Sheet 5: CLIPS Count ⭐
Sheet 6: CLIPS Activities ⭐
```

---

## 🎯 Quick Analysis

### Check CLIPS Impact
1. Open Email → Table 4
2. Look at "Last 1 Hour" column
3. If > 5: **High Priority**
4. If 1-5: **Monitor**
5. If 0: **Stable**

### Identify Problem Activities
1. Open Email → Table 5
2. Sort by "Last 1 Hour" (descending)
3. Top 3 activities = focus areas

### Compare CLIPS vs Total
1. Table 3: All interfaces total
2. Table 4: CLIPS total
3. Calculate: CLIPS / Total = % impact

---

## ✅ Quick Checks

**After Running Script:**
- [ ] 6 tables in email
- [ ] 6 sheets in Excel
- [ ] Table 4 shows USM+ARM+ASD only
- [ ] Table 5 shows USM+ARM+ASD only
- [ ] TEST_MODE setting is correct

---

## 📞 Support

**Email:** abhisha3@amdocs.com

---

**Version:** 2.3 | **Date:** Nov 14, 2025





