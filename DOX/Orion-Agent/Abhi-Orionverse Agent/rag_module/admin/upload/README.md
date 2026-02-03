# 📤 Upload Processing Module

> **Admin Excel Upload and RAG Processing**

This folder contains the main admin workflow script for uploading Excel files and running the full RAG pipeline.

---

## 📁 Structure

```
upload/
├── README.md
└── admin_upload_and_merge_with_rag.py     # Main workflow script
```

---

## 📦 Main Function: `upload_and_merge_with_rag()`

Orchestrates the complete 6-step admin workflow from Excel upload to ChromaDB update.

```python
from admin.upload.admin_upload_and_merge_with_rag import upload_and_merge_with_rag

# Run full workflow
result = upload_and_merge_with_rag(
    excel_file_path="path/to/uploaded_file.xlsx"
)

# Returns summary dictionary
print(result['total_processed'])
print(result['new_records'])
print(result['updated_records'])
```

---

## 🔄 6-Step Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    upload_and_merge_with_rag()               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  STEP 1: Semantic Analysis                                   │
│  ├── Read Excel file                                         │
│  ├── Clean data (remove blanks, footers)                     │
│  ├── Standardize column names                                │
│  └── Run ComprehensiveSRAnalyzer                             │
│                                                              │
│  STEP 2: Save Initial Results                                │
│  └── Save to output/reports/Admin_Upload_TIMESTAMP.xlsx      │
│                                                              │
│  STEP 3: Prepare for RAG                                     │
│  ├── Merge semantic workarounds with original data           │
│  └── Save to RAG/input/ for pipeline                         │
│                                                              │
│  STEP 4: Run RAG Pipeline                                    │
│  ├── Initialize MultiModelSRPipeline                         │
│  ├── Process all SRs with 5 LLM calls                        │
│  ├── Save output to RAG/llm output/                          │
│  └── Log usage statistics                                    │
│                                                              │
│  STEP 5: Merge to ChromaDB                                   │
│  ├── For each SR:                                            │
│  │   ├── If exists: UPDATE (preserve user feedback)          │
│  │   └── If new: INSERT                                      │
│  └── Track new vs updated counts                             │
│                                                              │
│  STEP 5.5: Inject New SRs                                    │
│  └── Only inject truly new SRs to vector store               │
│                                                              │
│  STEP 5.6: Cleanup                                           │
│  └── Delete temp files from RAG input/output                 │
│                                                              │
│  STEP 6: Generate Summary                                    │
│  ├── Total processed                                         │
│  ├── New vs updated counts                                   │
│  ├── Assignment distribution                                 │
│  └── Error count                                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Helper Functions

### `clean_excel_data(df)`
Removes blank rows and date footers from Excel.

```python
def clean_excel_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleaning steps:
    1. Remove rows where all columns are NaN
    2. Remove footer rows (date patterns like "12/5/2024")
    3. Reset index
    """
```

### `standardize_columns(df)`
Maps various column name formats to standard names.

```python
# Column mapping examples:
{
    'call id': 'Call ID',
    'sr id': 'SR ID',
    'case id': 'Call ID',
    'description': 'Description',
    'notes': 'Notes',
    'wl summary': 'Notes',
    'priority': 'Priority'
}
```

---

## 📊 Output Summary

The function returns a summary dictionary:

```python
{
    'total_processed': 50,
    'new_records': 35,
    'updated_records': 15,
    'errors': 0,
    'assignment_distribution': {
        'John Smith': 12,
        'Jane Doe': 10,
        'Bob Wilson': 8,
        ...
    },
    'rag_output_path': 'RAG/llm output/...',
    'semantic_output_path': 'output/reports/...'
}
```

---

## 🔧 Configuration

### File Size Limit
```python
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
```

### Supported Formats
```python
ALLOWED_EXTENSIONS = ['.xls', '.xlsx']
```

---

## 🔗 Integration Points

### Called By
- `app/routes/admin.py` - Web upload endpoint
- `main_runner.py` - CLI runner
- Scheduled jobs

### Calls
- `ComprehensiveSRAnalyzer` - Semantic analysis
- `MultiModelSRPipeline` - RAG processing
- `HistoryDatabaseManager` - ChromaDB updates

---

## ⚠️ Error Handling

The script includes robust error handling:

```python
try:
    # Step 4: Run RAG Pipeline
    pipeline = MultiModelSRPipeline()
    pipeline.run()
except Exception as e:
    logger.error(f"RAG pipeline failed: {e}")
    # Fallback: Use semantic-only results
    rag_output = semantic_output
```

---

## 📈 Logging

Detailed logging for each step:

```
INFO: Step 1: Starting semantic analysis...
INFO: Cleaned 50 rows from Excel
INFO: Step 2: Saving initial results...
INFO: Step 3: Preparing for RAG pipeline...
INFO: Step 4: Running RAG pipeline...
INFO: LLM Usage - Total calls: 125, Cost: $0.45
INFO: Step 5: Merging to ChromaDB...
INFO: New: 35, Updated: 15
INFO: Step 6: Complete - 50 SRs processed
```

---

*Part of SR-Analyzer Admin Module*
