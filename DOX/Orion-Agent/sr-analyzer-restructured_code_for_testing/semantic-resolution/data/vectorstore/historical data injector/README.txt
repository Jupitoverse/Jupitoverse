================================================================================
                    HISTORICAL DATA INJECTOR
================================================================================

PURPOSE:
--------
This folder is used to ADD new historical SR data to the existing 
clean_history_data ChromaDB vectorstore without replacing existing data.

LOCATION:
---------
data/vectorstore/historical data injector/

HOW TO USE:
-----------
1. Place your Excel file(s) (.xlsx or .xls) in this folder

2. Open PowerShell/Command Prompt and navigate to this folder:
   cd "C:\Users\praveerd\Videos\praveer mod\chatgpt\sr-analyzer\semantic-resolution\data\vectorstore\historical data injector"

3. Run the script:
   python push_historical_data.py

4. Wait for completion. The script will:
   - Load all Excel files from this folder
   - Check for duplicates (based on Customer Call ID)
   - Generate embeddings for new records
   - Add new records to the clean_history_data collection

EXPECTED EXCEL COLUMNS:
-----------------------
Required columns (at least one identifier + description):
  - Customer Call ID  (or call_id, SR ID)     <- Unique identifier
  - Summary*          (or Summary)             <- SR summary text
  - Description*      (or Description)         <- SR description text

Optional columns (will be stored as metadata):
  - Priority          (P1, P2, P3, P4)
  - WL_Summary        (Worklog summary)
  - Workaround        (Applied workaround)
  - Resolution Categorization
  - Resolution Categorization(Resolution Category Tier 3)
  - SLA Resolution Categorization T1
  - SLA Resolution Category
  - Assigned To       (Assignee name)
  - Status            (Current status)
  - Reported Date
  - Last Modified Date
  - Any other columns...  <- All will be preserved as metadata

COLUMN NAME FLEXIBILITY:
------------------------
The script automatically maps common column name variations:
  - "Customer Call ID" -> call_id
  - "Summary*" or "Summary" -> summary
  - "Description*" or "Description" -> description
  - "WL_Summary" or "WL Summary" -> wl_summary
  - etc.

DEDUPLICATION:
--------------
The script automatically skips records that already exist in the vectorstore
(based on Customer Call ID). This means you can safely re-run the script
without creating duplicates.

EXAMPLE OUTPUT:
---------------
================================================================================
 HISTORICAL DATA INJECTOR - CLEAN_HISTORY_DATA
================================================================================
 Input:      C:\...\historical data injector
 ChromaDB:   C:\...\chromadb_store
 Collection: clean_history_data
================================================================================

2026-01-06 10:15:00 - INFO - INITIALIZING HISTORICAL DATA INJECTOR
2026-01-06 10:15:02 - INFO - [OK] Model loaded
2026-01-06 10:15:02 - INFO - [OK] Connected to collection: clean_history_data
2026-01-06 10:15:02 - INFO -      Existing records: 23241

2026-01-06 10:15:02 - INFO - LOADING EXCEL FILES
2026-01-06 10:15:02 - INFO - Found 1 Excel files:
2026-01-06 10:15:03 - INFO -   [1/1] Loading new_data.xlsx...
2026-01-06 10:15:03 - INFO -      [OK] Loaded 500 rows, 15 columns

2026-01-06 10:15:03 - INFO - INJECTING DATA TO CLEAN_HISTORY_DATA
2026-01-06 10:15:03 - INFO - Existing records: 23241
2026-01-06 10:15:03 - INFO - New records to inject: 500
2026-01-06 10:15:05 - INFO - [OK] Prepared 485 new records
2026-01-06 10:15:05 - INFO -      Skipped 15 duplicates
2026-01-06 10:15:10 - INFO -   Batch 1/1: Injected 485 records

================================================================================
[SUCCESS] Injected 485 new records
Collection: clean_history_data
Total records: 23726
================================================================================

OPTIONAL FLAGS:
---------------
  --preprocess    Enable text preprocessing for better semantic matching
                  (removes customer names, project IDs, etc.)

  Example: python push_historical_data.py --preprocess

TROUBLESHOOTING:
----------------
1. "No Excel files found" 
   -> Make sure your Excel file is in THIS folder (not a subfolder)
   -> Check file extension is .xlsx or .xls

2. "ChromaDB store not found"
   -> The main vectorstore must exist at: data/vectorstore/chromadb_store/
   -> Run the main app at least once to create it

3. "Collection not found"
   -> The clean_history_data collection must exist
   -> This is created by the main vectorstore creation process

================================================================================




