# 📋 Semantic Workarounds Merger Tool

## Overview

This tool automatically merges **AI-generated semantic workarounds** into your original input Excel file, adding a new column called **"Semantic Workaround"** while preserving all existing columns and data.

---

## 🚀 Quick Start

### Option 1: Using Batch File (Easiest)
```bash
EXTRACT_WORKAROUNDS.bat
```

### Option 2: Using Python Directly
```bash
cd "DTU MOD"
python extract_semantic_workarounds.py
```

---

## 📁 Files & Locations

### Script Files
- `extract_semantic_workarounds.py` - Main Python merger script
- `EXTRACT_WORKAROUNDS.bat` - Windows batch file for easy execution

### Input Files (Automatic Detection)
- **Analysis File:** `output/reports/Admin_Upload_*.xlsx` (latest)
- **Original File:** `uploads/*.xls` or `uploads/*.xlsx` (latest)

### Output Location
```
DTU MOD/
└── Semantic workarounds/
    └── [OriginalFileName]_with_Semantic_Workarounds_YYYYMMDD_HHMMSS.xlsx
```

---

## 🔄 Complete Workflow

```
Step 1: Upload & Analyze
├─→ python admin_upload_and_merge.py "uploads/Mukul 5.xls"
├─→ Creates: output/reports/Admin_Upload_20251114_105843.xlsx
└─→ Contains: 30+ AI analysis columns

Step 2: Merge Workarounds (THIS TOOL)
├─→ EXTRACT_WORKAROUNDS.bat
├─→ Finds: Latest analysis file + Latest original file
├─→ Merges: By SR ID / Call ID
└─→ Creates: Mukul 5_with_Semantic_Workarounds_20251114_113324.xlsx

Result: Original file + 1 new "Semantic Workaround" column
```

---

## 📊 Input vs Output

### Original Input File (Mukul 5.xls)
```
┌──────────┬──────────┬─────────────┬────────┬─────────────┬──────┐
│ Call ID  │ Priority │ Assigned    │ STATUS │ Description │ ...  │
│          │          │ Group       │        │             │      │
├──────────┼──────────┼─────────────┼────────┼─────────────┼──────┤
│ CAS12345 │ P1       │ SOM_MM      │ Open   │ User issue  │ ...  │
│ CAS12346 │ P2       │ SQO_MM      │ Open   │ Login fail  │ ...  │
└──────────┴──────────┴─────────────┴────────┴─────────────┴──────┘
11 original columns, 110 rows
```

### Output File (Mukul 5_with_Semantic_Workarounds_*.xlsx)
```
┌──────────┬──────────┬─────────────┬────────┬─────────────┬──────┬──────────────────────┐
│ Call ID  │ Priority │ Assigned    │ STATUS │ Description │ ...  │ Semantic Workaround  │
│          │          │ Group       │        │             │      │ 🆕 NEW COLUMN        │
├──────────┼──────────┼─────────────┼────────┼─────────────┼──────┼──────────────────────┤
│ CAS12345 │ P1       │ SOM_MM      │ Open   │ User issue  │ ...  │ 🌟 (User Feedback    │
│          │          │             │        │             │      │ 100%) SR CAS67890:   │
│          │          │             │        │             │      │ Check config...      │
├──────────┼──────────┼─────────────┼────────┼─────────────┼──────┼──────────────────────┤
│ CAS12346 │ P2       │ SQO_MM      │ Open   │ Login fail  │ ...  │ (75%) SR CAS11111    │
│          │          │             │        │             │      │ workaround: Reset... │
└──────────┴──────────┴─────────────┴────────┴─────────────┴──────┴──────────────────────┘
12 columns (11 original + 1 new), 110 rows
```

**Key Point:** ALL original columns preserved, just ONE new column added!

---

## ✨ Features

### 🎯 Smart File Detection
- **Automatically finds latest analysis file** from `output/reports/`
- **Automatically finds latest original file** from `uploads/`
- Supports both `.xls` and `.xlsx` formats
- No manual file selection needed!

### 🔗 Intelligent Merging
- Matches records by SR ID (handles various column names: `Call ID`, `SR ID`, `Inc Call ID`, etc.)
- Preserves ALL original columns and data
- Adds only ONE new column: "Semantic Workaround"
- Left join ensures no records are lost

### 📋 Complete Data Preservation
- Original file structure: 100% preserved ✓
- Original column order: Maintained ✓
- Original data: Unchanged ✓
- New column: Added at the end ✓

### 🌟 Rich Workaround Content
Semantic workarounds include:
1. **User Feedback** (🌟 indicator) - Highest quality, verified by users
2. **Phase 1 Enhanced** - Structured multi-option workarounds
3. **Historical Cases** - From 1.18M+ similar resolved SRs
4. **Java Mapping** - For backend technical issues

### 📝 Comprehensive Output
- Timestamped filenames (no overwrites)
- Clear console summary
- Column list with 🆕 marker for new column
- Sample data preview
- Match statistics

---

## 🎯 What You Get

### Original Columns (Preserved)
```
1. Call ID
2. Customer Priority
3. Assigned Group
4. STATUS
5. Status_Reason_Hidden
6. Description
7. Notes
8. QC Defect ID
9. Categorization Tier 3
10. Submit Date
11. Last Date Duration Calculated
```

### New Column (Added)
```
🆕 12. Semantic Workaround
```

Contains AI-generated workarounds with:
- Similarity scores (e.g., "75%")
- Source SR IDs for reference
- User feedback indicators (🌟)
- Structured steps for complex issues

---

## 📈 Example Console Output

```
🔍 Finding latest Admin_Upload Excel file (with AI analysis)...
   ✓ Found: Admin_Upload_20251114_105843.xlsx

🔍 Finding latest original input Excel file...
   ✓ Found: Mukul 5.xls

================================================================================
ADD SEMANTIC WORKAROUNDS TO ORIGINAL FILE
================================================================================

📁 Reading analysis file: Admin_Upload_20251114_105843.xlsx
   ✓ Loaded 110 analyzed records

📁 Reading original file: Mukul 5.xls
   ✓ Loaded 110 original records
   ✓ SR ID column identified: 'Call ID'

🔗 Merging semantic workarounds...
   ✓ Merged 51/110 records with workarounds

💾 Saving merged file...
   ✓ Saved to: DTU MOD\Semantic workarounds\Mukul 5_with_Semantic_Workarounds_20251114_113324.xlsx

================================================================================
✅ MERGE COMPLETE
================================================================================

📊 Summary:
   • Original file: Mukul 5.xls
   • Original columns: 11
   • Records: 110
   • Workarounds added: 51
   • New column: 'Semantic Workaround'
   • Total columns: 12
   • Output file: Mukul 5_with_Semantic_Workarounds_20251114_113324.xlsx
   • Location: DTU MOD\Semantic workarounds

📋 Output Columns:
--------------------------------------------------------------------------------
      1. Call ID
      2. Customer Priority
      3. Assigned Group
      4. STATUS
      5. Status_Reason_Hidden
      6. Description
      7. Notes
      8. QC Defect ID
      9. Categorization Tier 3
      10. Submit Date
      11. Last Date Duration Calculated
   🆕 12. Semantic Workaround
--------------------------------------------------------------------------------

📋 Sample Data (first 3 records with workarounds):
--------------------------------------------------------------------------------
   CAS3068866: 🌟 (User Feedback 100%) SR CAS3068866: Test 6 mri...
   CAS3073640: Java mapping: Implementation class: ResourceConfig...
   CAS3085975: (76%) SR CAS2567652 - Possible Workarounds...
--------------------------------------------------------------------------------

🎉 Success! Original file enhanced with semantic workarounds.
```

---

## 🎯 Use Cases

### 1. **Executive Reports**
- Keep original data format for compatibility
- Add AI insights in one extra column
- Easy to share with management

### 2. **Team Distribution**
- Share enhanced file with entire team
- Everyone sees original context + AI suggestions
- No need for multiple files

### 3. **Historical Tracking**
- Timestamped files show workaround evolution
- Compare AI suggestions over time
- Track improvement in workaround quality

### 4. **Quality Review**
- Review AI workarounds alongside original data
- Context-aware evaluation
- Easy to validate against actual resolution

### 5. **Import to Other Systems**
- Original format maintained
- Can import back to ticketing systems
- Semantic workaround as additional field

---

## 🔧 Technical Details

### How It Works

```python
1. Find latest analysis file (Admin_Upload_*.xlsx)
   └─ Contains: AI analysis with "Suggested Workaround" column

2. Find latest original file (uploads/*.xls or *.xlsx)
   └─ Contains: Original input data

3. Extract SR ID and Suggested Workaround from analysis
   └─ Create mapping: {SR_ID: Workaround}

4. Identify SR ID column in original file
   └─ Handles: Call ID, SR ID, Inc Call ID, etc.

5. Merge using LEFT JOIN
   └─ original_df.merge(workarounds_df, on=sr_id_column, how='left')

6. Rename merged column to "Semantic Workaround"

7. Save to: Semantic workarounds/[original_name]_with_Semantic_Workarounds_[timestamp].xlsx
```

### Column Name Mapping

The script automatically handles various SR ID column names:
- `Call ID` ✓
- `SR ID` ✓
- `call id` ✓
- `sr id` ✓
- `Inc Call ID` ✓

### File Format Support

**Input (Original):**
- `.xls` (Excel 97-2003) - Uses xlrd engine
- `.xlsx` (Excel 2007+) - Uses openpyxl engine

**Output:**
- `.xlsx` (Excel 2007+) - Universal compatibility

### Performance

| Metric | Value |
|--------|-------|
| **Processing Time** | 2-5 seconds for 110 SRs |
| **Memory Usage** | ~100-200 MB |
| **File Size** | Similar to original (~500 KB) |
| **Match Rate** | Depends on SR ID overlap |

---

## 🐛 Troubleshooting

### "No Admin_Upload Excel files found"
**Problem:** Can't find analysis file.

**Solutions:**
1. Run `admin_upload_and_merge.py` first
2. Check `output/reports/` directory exists
3. Verify files match pattern: `Admin_Upload_*.xlsx`

### "No Excel files found in uploads"
**Problem:** Can't find original input file.

**Solutions:**
1. Ensure input file is in `uploads/` directory
2. Check file extension is `.xls` or `.xlsx`
3. Verify file isn't corrupted

### "Could not find SR ID column in original file"
**Problem:** Original file has non-standard column names.

**Solutions:**
1. Check original file has one of: `Call ID`, `SR ID`, `Inc Call ID`
2. Add your column name to `possible_sr_columns` list in script (line 129)
3. Ensure SR ID column exists and has data

### "Merged 0/X records with workarounds"
**Problem:** SR IDs don't match between files.

**Causes:**
- Different SR IDs in analysis vs original file
- Using wrong original file (doesn't match analyzed file)
- SR ID format mismatch (e.g., "CAS123" vs "123")

**Solutions:**
1. Verify you're using the same input file that was analyzed
2. Check SR ID format is consistent
3. Ensure analysis file corresponds to original file

### "Unicode encoding error" in console
**Problem:** Windows console can't display emojis.

**Impact:** None - File is created successfully, just console display issue

**Solution:** Ignore it or check file directly in Excel

---

## 💡 Pro Tips

### 1. **Run Immediately After Analysis**
```bash
# Upload and analyze
python admin_upload_and_merge.py "uploads/Mukul 5.xls"

# Merge workarounds right away
EXTRACT_WORKAROUNDS.bat
```

### 2. **Keep Files Organized**
- Analysis files in: `output/reports/`
- Original files in: `uploads/`
- Merged files in: `DTU MOD/Semantic workarounds/`

### 3. **Use Descriptive Original Filenames**
Output filename includes original name:
- Input: `Mukul 5.xls`
- Output: `Mukul 5_with_Semantic_Workarounds_20251114_113324.xlsx`

### 4. **Track Match Rate**
Console shows: `Merged 51/110 records with workarounds`
- High match rate (>80%) = Good data alignment
- Low match rate (<50%) = Check if using correct files

### 5. **Review Sample Data**
Console shows 3 sample workarounds - quick quality check!

---

## 📊 Real-World Example

### Scenario
You uploaded **Mukul 5.xls** (110 SRs) for analysis.

### Results
```
Input:   Mukul 5.xls (110 SRs, 11 columns)
         ↓
Analyze: admin_upload_and_merge.py
         ↓
Output:  Admin_Upload_20251114_105843.xlsx (110 SRs, 30+ analysis columns)
         ↓
Merge:   EXTRACT_WORKAROUNDS.bat
         ↓
Final:   Mukul 5_with_Semantic_Workarounds_20251114_113324.xlsx
         (110 SRs, 12 columns = 11 original + 1 semantic workaround)
```

### What You Get
- **All original data**: Call IDs, descriptions, notes, status, etc.
- **Plus AI workarounds**: One extra column with smart suggestions
- **Easy distribution**: Share single file with team
- **Context preserved**: Workarounds shown alongside original issue details

---

## 📂 File Structure

```
semantic-nlpupdate/
├── uploads/                          ← Original input files
│   └── Mukul 5.xls
│
├── output/
│   └── reports/                      ← AI analysis results
│       └── Admin_Upload_20251114_105843.xlsx
│
└── DTU MOD/
    ├── extract_semantic_workarounds.py     ← Main script
    ├── EXTRACT_WORKAROUNDS.bat             ← Easy launcher
    ├── README_SEMANTIC_WORKAROUNDS.md      ← This file
    └── Semantic workarounds/               ← Merged output
        └── Mukul 5_with_Semantic_Workarounds_20251114_113324.xlsx
```

---

## ✅ Success Checklist

After running the tool:
- [ ] Console shows "✅ MERGE COMPLETE"
- [ ] New file created in "Semantic workarounds" folder
- [ ] File has timestamp in filename
- [ ] Excel opens with ALL original columns
- [ ] New column "Semantic Workaround" at the end
- [ ] Workarounds visible (not all NaN)
- [ ] Record count matches original file

---

## 🎉 Summary

This tool provides a **smart, automated way** to enhance your original Excel files with AI-generated workarounds:

### What It Does
✅ Preserves 100% of original data  
✅ Adds ONE new "Semantic Workaround" column  
✅ Automatically finds and merges latest files  
✅ Creates timestamped outputs  
✅ Shows clear summary and statistics  

### What It Doesn't Do
❌ Doesn't modify original files  
❌ Doesn't remove any columns  
❌ Doesn't change data formats  
❌ Doesn't overwrite previous outputs  

### Perfect For
- Sharing with teams (single enhanced file)
- Executive reports (original format + insights)
- Historical tracking (timestamped versions)
- Quality review (workarounds in context)

**Typical workflow time:** ~5 seconds from execution to enhanced Excel file!

---

**Version:** 2.0 - Merger Edition  
**Created:** November 14, 2024  
**Status:** ✅ Production Ready  
**Type:** Merge Tool (Original + AI Workarounds)
