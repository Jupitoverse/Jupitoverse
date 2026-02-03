#!/usr/bin/env python3
"""
Historical Data Injector
========================
Reads Excel files from this folder and ADDS them to the existing 
clean_history_data ChromaDB collection (without replacing existing data)

USAGE:
1. Place your Excel files in: data/vectorstore/historical data injector/
2. Run: python push_historical_data.py
3. Data will be ADDED to the existing clean_history_data collection

EXPECTED COLUMNS in Excel:
- Customer Call ID (or call_id)
- Summary* (or summary)
- Description* (or description)
- Priority (or priority)
- WL_Summary (or wl_summary)
- Workaround (or workaround)
- Resolution Categorization
- SLA Resolution Categorization T1
- SLA Resolution Category

Any additional columns will be preserved as metadata.
"""
import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import argparse
import logging
import re

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Path setup - this script is in data/vectorstore/historical data injector/
SCRIPT_DIR = Path(__file__).parent.absolute()
VECTORSTORE_DIR = SCRIPT_DIR.parent  # data/vectorstore/
DATA_DIR = VECTORSTORE_DIR.parent  # data/
PROJECT_ROOT = DATA_DIR.parent  # semantic-resolution/

# ChromaDB store location (sibling folder)
CHROMADB_STORE = VECTORSTORE_DIR / "chromadb_store"

sys.path.insert(0, str(PROJECT_ROOT))

# Try imports
try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logger.error("ChromaDB not installed. Run: pip install chromadb")

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.error("sentence-transformers not installed. Run: pip install sentence-transformers")

# Try to import preprocessor (optional)
try:
    from analyzers.sr_text_preprocessor import SRTextPreprocessor
    PREPROCESSOR_AVAILABLE = True
except ImportError:
    PREPROCESSOR_AVAILABLE = False


# Column mapping: Excel column names -> standardized names
COLUMN_MAPPING = {
    'customer call id': 'call_id',
    'customer_call_id': 'call_id',
    'call id': 'call_id',
    'callid': 'call_id',
    'sr id': 'call_id',
    'sr_id': 'call_id',
    'incident id': 'incident_id',
    'incident_id': 'incident_id',
    # 'summary' column mapping removed - was redundant (just prefix of description)
    'description*': 'description',
    'description': 'description',
    'priority': 'priority',
    'customer priority': 'priority',
    'wl_summary': 'wl_summary',
    'wl summary': 'wl_summary',
    'workaround': 'workaround',
    'resolution categorization': 'resolution_categorization',
    'resolution_categorization': 'resolution_categorization',
    'resolution categorization(resolution category tier 3)': 'resolution_categorization_tier3',
    'resolution category tier 3': 'resolution_categorization_tier3',
    'resolution_categorization_tier3': 'resolution_categorization_tier3',
    'sla resolution categorization t1': 'sla_resolution_categorization_t1',
    'sla_resolution_categorization_t1': 'sla_resolution_categorization_t1',
    'sla resolution category': 'sla_resolution_category',
    'sla_resolution_category': 'sla_resolution_category',
    'assigned to': 'assigned_to',
    'assigned_to': 'assigned_to',
    'assignee': 'assigned_to',
    'status': 'status',
    'status*': 'status',
    'resolution': 'resolution',
    'reported date': 'reported_date',
    'reported_date': 'reported_date',
    'last modified date': 'last_modified_date',
    'last_modified_date': 'last_modified_date',
}


def sanitize_column_name(name: str) -> str:
    """Sanitize column name for compatibility"""
    if not name or pd.isna(name):
        return "unnamed_column"
    
    name = str(name).strip().lower()
    name = re.sub(r'[^\w\s]', '_', name)
    name = re.sub(r'\s+', '_', name)
    name = re.sub(r'_+', '_', name)
    name = name.strip('_')
    
    if name and name[0].isdigit():
        name = 'col_' + name
    
    if not name:
        name = "unnamed_column"
    
    return name


class HistoricalDataInjector:
    """
    Injects data from Excel files to the existing clean_history_data ChromaDB collection
    """
    
    def __init__(
        self,
        input_folder: str = None,
        chromadb_path: str = None,
        collection_name: str = "clean_history_data",
        model_name: str = "all-MiniLM-L6-v2",
        use_preprocessing: bool = False
    ):
        self.input_folder = Path(input_folder or SCRIPT_DIR)
        self.chromadb_path = Path(chromadb_path or CHROMADB_STORE)
        self.collection_name = collection_name
        self.model_name = model_name
        self.use_preprocessing = use_preprocessing and PREPROCESSOR_AVAILABLE
        
        self.model = None
        self.preprocessor = None
        self.client = None
        self.collection = None
        
    def initialize(self):
        """Initialize models and ChromaDB client"""
        logger.info("=" * 80)
        logger.info("INITIALIZING HISTORICAL DATA INJECTOR")
        logger.info("=" * 80)
        
        if not CHROMADB_AVAILABLE:
            raise ImportError("ChromaDB required. Install: pip install chromadb")
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError("sentence-transformers required. Install: pip install sentence-transformers")
        
        # Check ChromaDB store exists
        if not self.chromadb_path.exists():
            raise FileNotFoundError(f"ChromaDB store not found at: {self.chromadb_path}")
        
        # Load embedding model
        logger.info(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        logger.info("[OK] Model loaded")
        
        # Initialize preprocessor if available and requested
        if self.use_preprocessing and PREPROCESSOR_AVAILABLE:
            self.preprocessor = SRTextPreprocessor()
            logger.info("[OK] Preprocessor initialized")
        
        # Connect to existing ChromaDB
        logger.info(f"Connecting to ChromaDB at: {self.chromadb_path}")
        self.client = chromadb.PersistentClient(path=str(self.chromadb_path))
        
        # Get existing collection
        try:
            self.collection = self.client.get_collection(self.collection_name)
            existing_count = self.collection.count()
            logger.info(f"[OK] Connected to collection: {self.collection_name}")
            logger.info(f"     Existing records: {existing_count}")
        except Exception as e:
            logger.error(f"Collection '{self.collection_name}' not found: {e}")
            raise
        
        return True
    
    def load_excel_files(self) -> pd.DataFrame:
        """Load all Excel files from this folder"""
        logger.info("=" * 80)
        logger.info("LOADING EXCEL FILES")
        logger.info("=" * 80)
        logger.info(f"Input folder: {self.input_folder}")
        
        # Find all Excel files
        excel_files = []
        for ext in ['*.xlsx', '*.xls']:
            excel_files.extend(self.input_folder.glob(ext))
        
        # Filter out temp files
        excel_files = [f for f in excel_files if not f.name.startswith('~')]
        
        if not excel_files:
            logger.warning(f"No Excel files found in {self.input_folder}")
            logger.info("Place your Excel files in this folder and run again.")
            return None
        
        logger.info(f"Found {len(excel_files)} Excel files:")
        
        all_data = []
        for i, file_path in enumerate(sorted(excel_files), 1):
            try:
                logger.info(f"  [{i}/{len(excel_files)}] Loading {file_path.name}...")
                df = pd.read_excel(file_path)
                
                # Normalize column names
                original_cols = df.columns.tolist()
                new_cols = []
                for col in original_cols:
                    col_lower = sanitize_column_name(col)
                    # Apply mapping if available
                    mapped = COLUMN_MAPPING.get(col_lower, col_lower)
                    new_cols.append(mapped)
                
                df.columns = new_cols
                
                # Add source tracking
                df['_source_file'] = file_path.name
                df['_injected_date'] = datetime.now().isoformat()
                
                all_data.append(df)
                logger.info(f"     [OK] Loaded {len(df)} rows, {len(df.columns)} columns")
                
            except Exception as e:
                logger.error(f"     [ERROR] {e}")
        
        if not all_data:
            logger.error("No data loaded from any files")
            return None
        
        # Combine all dataframes
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df = combined_df.fillna('')
        
        logger.info(f"\n[OK] Total records loaded: {len(combined_df)}")
        
        # Log columns
        logger.info("Columns after mapping:")
        for col in combined_df.columns[:15]:
            logger.info(f"  - {col}")
        if len(combined_df.columns) > 15:
            logger.info(f"  ... and {len(combined_df.columns) - 15} more")
        
        return combined_df
    
    def create_searchable_text(self, row) -> str:
        """Create searchable text from row data"""
        parts = []
        
        # Primary text fields for embedding (summary removed - was redundant)
        text_fields = ['description', 'wl_summary']
        
        for field in text_fields:
            if field in row.index:
                value = str(row[field]).strip()
                if value and value.lower() not in ['nan', 'none', '', 'na', 'nat']:
                    if self.use_preprocessing and self.preprocessor:
                        try:
                            value = self.preprocessor.clean_for_semantic_search(value)
                        except:
                            pass
                    if value and len(value) > 5:
                        parts.append(value)
        
        # Add categorization fields for context
        category_fields = [
            'resolution_categorization',
            'resolution_categorization_tier3',
            'sla_resolution_categorization_t1',
            'sla_resolution_category'
        ]
        for field in category_fields:
            if field in row.index:
                value = str(row[field]).strip()
                if value and value.lower() not in ['nan', 'none', '', 'na', 'nat']:
                    parts.append(f"{field}: {value}")
        
        return " ".join(parts)
    
    def inject_data(self, df: pd.DataFrame) -> int:
        """Inject data to the existing ChromaDB collection"""
        logger.info("=" * 80)
        logger.info("INJECTING DATA TO CLEAN_HISTORY_DATA")
        logger.info("=" * 80)
        
        existing_count = self.collection.count()
        logger.info(f"Existing records: {existing_count}")
        logger.info(f"New records to inject: {len(df)}")
        
        # Get existing IDs to avoid duplicates
        try:
            existing_results = self.collection.get(include=[])
            existing_ids = set(existing_results.get('ids', []))
            existing_ids_lower = set(x.lower() for x in existing_ids if isinstance(x, str))
            logger.info(f"Checking against {len(existing_ids)} existing IDs for duplicates")
        except:
            existing_ids = set()
            existing_ids_lower = set()
        
        # Prepare documents
        documents = []
        metadatas = []
        ids = []
        skipped_duplicates = 0
        skipped_empty = 0
        
        for idx, row in df.iterrows():
            # Get call_id for deduplication
            call_id = str(row.get('call_id', '')).strip()
            if not call_id or call_id.lower() in ['nan', 'none', '', 'na']:
                call_id = f"injected_{idx}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Skip if already exists (deduplication)
            if call_id in existing_ids or call_id.lower() in existing_ids_lower:
                skipped_duplicates += 1
                continue
            
            # Create searchable text
            doc_text = self.create_searchable_text(row)
            
            if not doc_text or len(doc_text) < 10:
                skipped_empty += 1
                continue
            
            documents.append(doc_text)
            
            # Create metadata - ALL columns
            metadata = {}
            for col in row.index:
                if col.startswith('_'):
                    continue
                val = row[col]
                try:
                    if isinstance(val, pd.Series):
                        val = val.iloc[0] if len(val) > 0 else ''
                    if val is not None and str(val).strip() and str(val).lower() not in ['nan', 'none', 'nat']:
                        metadata[col] = str(val)[:5000]
                except:
                    pass
            
            # Add default columns if not present
            if 'ai_generated_workaround' not in metadata:
                metadata['ai_generated_workaround'] = 'NA'
            if 'user_corrected_workaround' not in metadata:
                metadata['user_corrected_workaround'] = ''
            
            metadatas.append(metadata)
            ids.append(call_id)
            
            if (idx + 1) % 500 == 0:
                logger.info(f"  Prepared {idx + 1}/{len(df)} records...")
        
        logger.info(f"\n[OK] Prepared {len(documents)} new records")
        logger.info(f"     Skipped {skipped_duplicates} duplicates")
        logger.info(f"     Skipped {skipped_empty} empty/invalid records")
        
        if len(documents) == 0:
            logger.warning("No new records to inject!")
            return 0
        
        # Add to ChromaDB in batches
        logger.info(f"\nGenerating embeddings and injecting to ChromaDB...")
        
        batch_size = 500
        total_batches = (len(documents) + batch_size - 1) // batch_size
        added_count = 0
        
        for batch_idx in range(total_batches):
            start = batch_idx * batch_size
            end = min(start + batch_size, len(documents))
            
            batch_docs = documents[start:end]
            batch_metas = metadatas[start:end]
            batch_ids = ids[start:end]
            
            # Generate embeddings
            embeddings = self.model.encode(batch_docs, show_progress_bar=False).tolist()
            
            # Add to collection (upsert for safety)
            self.collection.upsert(
                documents=batch_docs,
                metadatas=batch_metas,
                embeddings=embeddings,
                ids=batch_ids
            )
            
            added_count += len(batch_docs)
            logger.info(f"  Batch {batch_idx + 1}/{total_batches}: Injected {len(batch_docs)} records")
        
        # Verify final count
        final_count = self.collection.count()
        logger.info(f"\n[OK] Injection complete!")
        logger.info(f"     Records before: {existing_count}")
        logger.info(f"     Records added: {added_count}")
        logger.info(f"     Records after: {final_count}")
        
        return added_count
    
    def run(self) -> bool:
        """Main execution"""
        print("\n" + "=" * 80)
        print(" HISTORICAL DATA INJECTOR - CLEAN_HISTORY_DATA")
        print("=" * 80)
        print(f" Input:      {self.input_folder}")
        print(f" ChromaDB:   {self.chromadb_path}")
        print(f" Collection: {self.collection_name}")
        print("=" * 80 + "\n")
        
        try:
            self.initialize()
            
            df = self.load_excel_files()
            if df is None or len(df) == 0:
                logger.warning("No data to process. Place Excel files in this folder and run again.")
                return False
            
            added_count = self.inject_data(df)
            
            print("\n" + "=" * 80)
            if added_count > 0:
                print(f"[SUCCESS] Injected {added_count} new records")
                print(f"Collection: {self.collection_name}")
                print(f"Total records: {self.collection.count()}")
            else:
                print("[INFO] No new records to inject (all duplicates or invalid)")
            print("=" * 80)
            
            return True
            
        except Exception as e:
            logger.error(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Inject historical data to clean_history_data ChromaDB collection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python push_historical_data.py
  python push_historical_data.py --preprocess

This script ADDS data to the existing collection without replacing it.
Place your Excel files in this folder before running.

EXPECTED EXCEL COLUMNS:
  Required:
    - Customer Call ID (unique identifier)
    - Summary* or Summary
    - Description* or Description
    
  Optional (will be stored as metadata):
    - Priority
    - WL_Summary
    - Workaround
    - Resolution Categorization
    - SLA Resolution Categorization T1
    - SLA Resolution Category
    - Assigned To
    - Status
    - Any other columns...
        """
    )
    
    parser.add_argument('--preprocess', action='store_true',
                        help='Enable text preprocessing for embeddings')
    
    args = parser.parse_args()
    
    injector = HistoricalDataInjector(
        use_preprocessing=args.preprocess
    )
    
    success = injector.run()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

