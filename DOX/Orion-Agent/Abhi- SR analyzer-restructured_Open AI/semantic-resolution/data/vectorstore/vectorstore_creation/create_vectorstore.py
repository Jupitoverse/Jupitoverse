#!/usr/bin/env python3
"""
Universal Vectorstore Creator - FULLY DYNAMIC
Reads all Excel files from this folder and subfolders, creates ChromaDB vectorstore

PLUG AND PLAY USAGE:
1. Put your Excel files in: data/vectorstore/vectorstore_creation/
   - Or organize in subfolders
2. Run: python create_vectorstore.py
3. Vectorstore created at: data/vectorstore/test_store/

DYNAMIC FEATURES:
- All Excel columns are stored in ChromaDB metadata (no column mapping needed)
- Embedding text is generated from all text columns automatically
- Works with any Excel format - no configuration needed

This makes the RAG model reusable for different users - just add your Excel files!
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

# Path setup - this script is in data/vectorstore/vectorstore_creation/
SCRIPT_DIR = Path(__file__).parent.absolute()
VECTORSTORE_DIR = SCRIPT_DIR.parent  # data/vectorstore/
DATA_DIR = VECTORSTORE_DIR.parent    # data/
PROJECT_ROOT = DATA_DIR.parent       # semantic-resolution/

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


def sanitize_column_name(name: str) -> str:
    """
    Sanitize column name for compatibility
    - Replace special characters with underscores
    - Remove leading/trailing whitespace
    """
    if not name or pd.isna(name):
        return "unnamed_column"
    
    name = str(name).strip()
    
    # Replace special characters with underscore
    name = re.sub(r'[^\w\s]', '_', name)
    
    # Replace spaces with underscore
    name = re.sub(r'\s+', '_', name)
    
    # Remove consecutive underscores
    name = re.sub(r'_+', '_', name)
    
    # Remove leading/trailing underscores
    name = name.strip('_')
    
    # Ensure it doesn't start with a number
    if name and name[0].isdigit():
        name = 'col_' + name
    
    # Handle empty result
    if not name:
        name = "unnamed_column"
    
    return name.lower()


class UniversalVectorstoreCreator:
    """
    Creates ChromaDB vectorstore from Excel files - FULLY DYNAMIC
    
    Directory Structure:
        data/vectorstore/
        |-- vectorstore_creation/     <-- This folder (put Excel files here)
        |   |-- create_vectorstore.py <-- This script
        |   |-- data_2024.xlsx
        |   |-- data_2025.xlsx
        |   +-- subfolders/           <-- Optional subfolders
        |       +-- more_data.xlsx
        +-- test_store/               <-- Output vectorstore
    
    Features:
        - All Excel columns stored in metadata (dynamic)
        - Embedding generated from all text columns (dynamic)
        - No column mapping required
    """
    
    def __init__(
        self,
        input_folder: str = None,
        output_folder: str = None,
        collection_name: str = "data",
        model_name: str = "all-MiniLM-L6-v2",
        use_preprocessing: bool = False,
        text_columns: list = None,
        id_column: str = None
    ):
        # Input: this folder (vectorstore_creation)
        self.input_folder = Path(input_folder or SCRIPT_DIR)
        
        # Output: test_store in parent folder
        self.output_folder = Path(output_folder or VECTORSTORE_DIR / "test_store")
        
        self.collection_name = collection_name
        self.model_name = model_name
        self.use_preprocessing = use_preprocessing and PREPROCESSOR_AVAILABLE
        
        # Dynamic configuration
        self.text_columns = text_columns  # If None, auto-detect text columns
        self.id_column = id_column  # If None, use index
        
        self.model = None
        self.preprocessor = None
        self.client = None
        self.collection = None
        
    def initialize(self):
        """Initialize models and ChromaDB client"""
        logger.info("=" * 80)
        logger.info("INITIALIZING UNIVERSAL VECTORSTORE CREATOR (DYNAMIC)")
        logger.info("=" * 80)
        
        if not CHROMADB_AVAILABLE:
            raise ImportError("ChromaDB required. Install: pip install chromadb")
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            raise ImportError("sentence-transformers required. Install: pip install sentence-transformers")
        
        # Load embedding model
        logger.info(f"Loading embedding model: {self.model_name}")
        self.model = SentenceTransformer(self.model_name)
        logger.info("[OK] Model loaded")
        
        # Initialize preprocessor if available and requested
        if self.use_preprocessing and PREPROCESSOR_AVAILABLE:
            self.preprocessor = SRTextPreprocessor()
            logger.info("[OK] Preprocessor initialized")
        
        # Ensure output directory exists
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB
        logger.info(f"Initializing ChromaDB at: {self.output_folder}")
        self.client = chromadb.PersistentClient(path=str(self.output_folder))
        logger.info("[OK] ChromaDB client initialized")
        
        return True
    
    def load_excel_files(self) -> pd.DataFrame:
        """Load all Excel files from this folder and subfolders"""
        logger.info("=" * 80)
        logger.info("LOADING EXCEL FILES")
        logger.info("=" * 80)
        logger.info(f"Input folder: {self.input_folder}")
        
        # Find all Excel files (including in subfolders)
        excel_files = []
        for ext in ['*.xlsx', '*.xls']:
            excel_files.extend(self.input_folder.rglob(ext))
        
        # Filter out temp files, db files, and this script
        excel_files = [
            f for f in excel_files 
            if not f.name.startswith('~') 
            and not f.name.endswith('.db')
            and f.name != Path(__file__).name
        ]
        
        if not excel_files:
            logger.warning(f"No Excel files found in {self.input_folder}")
            return None
        
        logger.info(f"Found {len(excel_files)} Excel files:")
        
        all_data = []
        for i, file_path in enumerate(sorted(excel_files), 1):
            try:
                relative_path = file_path.relative_to(self.input_folder)
                logger.info(f"  [{i}/{len(excel_files)}] Loading {relative_path}...")
                
                df = pd.read_excel(file_path)
                
                # Sanitize column names
                original_cols = df.columns.tolist()
                sanitized_cols = []
                for col in original_cols:
                    san_col = sanitize_column_name(col)
                    # Handle duplicates
                    base = san_col
                    counter = 1
                    while san_col in sanitized_cols:
                        san_col = f"{base}_{counter}"
                        counter += 1
                    sanitized_cols.append(san_col)
                
                df.columns = sanitized_cols
                
                # Add source tracking
                df['_source_file'] = str(relative_path)
                
                all_data.append(df)
                logger.info(f"     [OK] Loaded {len(df)} rows, {len(df.columns)} columns")
                
            except Exception as e:
                logger.error(f"     [ERROR] {e}")
        
        if not all_data:
            logger.error("No data loaded from any files")
            return None
        
        # Combine all dataframes
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Fill NaN values
        combined_df = combined_df.fillna('')
        
        # Log column info
        logger.info(f"\n[OK] Total records: {len(combined_df)}")
        logger.info(f"Columns ({len(combined_df.columns)}):")
        for col in combined_df.columns[:10]:
            dtype = combined_df[col].dtype
            logger.info(f"  - {col} ({dtype})")
        if len(combined_df.columns) > 10:
            logger.info(f"  ... and {len(combined_df.columns) - 10} more")
        
        return combined_df
    
    def detect_text_columns(self, df: pd.DataFrame) -> list:
        """Auto-detect text columns suitable for embedding"""
        text_cols = []
        
        for col in df.columns:
            if col.startswith('_'):
                continue
            
            # Check if column has text data
            if df[col].dtype == 'object':
                # Check average length of non-empty values
                non_empty = df[col].astype(str).str.strip()
                non_empty = non_empty[non_empty != '']
                
                if len(non_empty) > 0:
                    avg_len = non_empty.str.len().mean()
                    # Consider it a text column if average length > 10
                    if avg_len > 10:
                        text_cols.append(col)
        
        return text_cols
    
    def detect_id_column(self, df: pd.DataFrame) -> str:
        """Auto-detect ID column"""
        # Common ID column names
        id_patterns = ['id', 'call_id', 'sr_id', 'incident_id', 'ticket_id', 'case_id', 'customer_call_id']
        
        for col in df.columns:
            col_lower = col.lower()
            for pattern in id_patterns:
                if pattern in col_lower:
                    # Verify uniqueness
                    if df[col].nunique() > len(df) * 0.9:  # At least 90% unique
                        return col
        
        return None
    
    def create_searchable_text(self, row, text_columns: list) -> str:
        """Create searchable text from row data - DYNAMIC"""
        parts = []
        
        for col in text_columns:
            if col in row.index:
                value = str(row[col]).strip()
                if value and value.lower() not in ['nan', 'none', '', 'na', 'nat']:
                    # Optional preprocessing
                    if self.use_preprocessing and self.preprocessor:
                        try:
                            value = self.preprocessor.clean_for_semantic_search(value)
                        except:
                            pass
                    if value and len(value) > 5:
                        parts.append(value)
        
        return " ".join(parts)
    
    def create_vectorstore(self, df: pd.DataFrame) -> bool:
        """Create ChromaDB vectorstore from dataframe - FULLY DYNAMIC"""
        logger.info("=" * 80)
        logger.info("CREATING CHROMADB VECTORSTORE (DYNAMIC)")
        logger.info("=" * 80)
        
        # Auto-detect text columns if not specified
        text_columns = self.text_columns
        if text_columns is None:
            text_columns = self.detect_text_columns(df)
            logger.info(f"Auto-detected text columns for embedding: {text_columns}")
        
        if not text_columns:
            logger.warning("No text columns found for embedding. Using all object columns.")
            text_columns = [col for col in df.columns if df[col].dtype == 'object' and not col.startswith('_')]
        
        # Auto-detect ID column if not specified
        id_column = self.id_column
        if id_column is None:
            id_column = self.detect_id_column(df)
            if id_column:
                logger.info(f"Auto-detected ID column: {id_column}")
            else:
                logger.info("No ID column detected. Using row index.")
        
        # Delete existing collection if exists
        try:
            self.client.delete_collection(self.collection_name)
            logger.info(f"Deleted existing collection: {self.collection_name}")
        except:
            pass
        
        # Create new collection
        self.collection = self.client.create_collection(
            name=self.collection_name,
            metadata={
                "created_at": datetime.now().isoformat(),
                "model": self.model_name,
                "total_records": len(df),
                "text_columns": ",".join(text_columns),
                "id_column": id_column or "index",
                "dynamic": "true"
            }
        )
        logger.info(f"[OK] Created collection: {self.collection_name}")
        
        # Prepare documents
        logger.info(f"\nPreparing {len(df)} documents...")
        logger.info(f"Text columns for embedding: {text_columns}")
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, row in df.iterrows():
            # Create searchable text from all text columns
            doc_text = self.create_searchable_text(row, text_columns)
            
            if not doc_text or len(doc_text) < 10:
                continue
            
            documents.append(doc_text)
            
            # Create metadata - ALL columns (dynamic)
            metadata = {}
            for col in row.index:
                if not col.startswith('_'):
                    val = row[col]
                    try:
                        if isinstance(val, pd.Series):
                            val = val.iloc[0] if len(val) > 0 else ''
                        if val is not None and str(val).strip() and str(val).lower() not in ['nan', 'none', 'nat']:
                            # Truncate long values (ChromaDB limit)
                            metadata[col] = str(val)[:5000]
                    except:
                        pass
            
            metadatas.append(metadata)
            
            # Create unique ID
            if id_column and id_column in row.index:
                doc_id = str(row[id_column]).strip()
            else:
                doc_id = str(idx)
            
            # Ensure unique ID
            if doc_id in ids:
                doc_id = f"{doc_id}_{idx}"
            ids.append(doc_id)
            
            if (idx + 1) % 1000 == 0:
                logger.info(f"  Prepared {idx + 1}/{len(df)} documents...")
        
        logger.info(f"[OK] Prepared {len(documents)} valid documents")
        
        if len(documents) == 0:
            logger.error("No valid documents to add!")
            return False
        
        # Add to ChromaDB in batches
        logger.info(f"\nGenerating embeddings and adding to ChromaDB...")
        
        batch_size = 500
        total_batches = (len(documents) + batch_size - 1) // batch_size
        
        for batch_idx in range(total_batches):
            start = batch_idx * batch_size
            end = min(start + batch_size, len(documents))
            
            batch_docs = documents[start:end]
            batch_metas = metadatas[start:end]
            batch_ids = ids[start:end]
            
            embeddings = self.model.encode(batch_docs, show_progress_bar=False).tolist()
            
            self.collection.add(
                documents=batch_docs,
                metadatas=batch_metas,
                embeddings=embeddings,
                ids=batch_ids
            )
            
            logger.info(f"  Batch {batch_idx + 1}/{total_batches}: Added {len(batch_docs)} documents")
        
        logger.info(f"\n[OK] Vectorstore created!")
        logger.info(f"  Collection: {self.collection_name}")
        logger.info(f"  Records: {self.collection.count()}")
        logger.info(f"  Location: {self.output_folder}")
        
        return True
    
    def validate(self) -> bool:
        """Validate the created vectorstore"""
        logger.info("=" * 80)
        logger.info("VALIDATING VECTORSTORE")
        logger.info("=" * 80)
        
        try:
            collection = self.client.get_collection(self.collection_name)
            count = collection.count()
            
            logger.info(f"[OK] Collection: {self.collection_name}")
            logger.info(f"  Records: {count}")
            
            if count > 0:
                # Test search
                test_embedding = self.model.encode("test query").tolist()
                results = collection.query(query_embeddings=[test_embedding], n_results=1)
                if results and results.get('ids'):
                    logger.info(f"[OK] Test search successful")
                    
                    # Show sample metadata fields
                    if results.get('metadatas') and results['metadatas'][0]:
                        sample_meta = results['metadatas'][0][0]
                        logger.info(f"  Sample metadata fields: {list(sample_meta.keys())[:5]}...")
            
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] Validation failed: {e}")
            return False
    
    def run(self) -> bool:
        """Main execution"""
        print("\n" + "=" * 80)
        print(" UNIVERSAL VECTORSTORE CREATOR (DYNAMIC)")
        print("=" * 80)
        print(f" Input:  {self.input_folder}")
        print(f" Output: {self.output_folder}")
        print(" Mode:   Fully Dynamic (all columns from Excel)")
        print("=" * 80 + "\n")
        
        try:
            self.initialize()
            
            df = self.load_excel_files()
            if df is None or len(df) == 0:
                logger.warning("No data to process.")
                return False
            
            self.create_vectorstore(df)
            success = self.validate()
            
            print("\n" + "=" * 80)
            if success:
                print("[SUCCESS] Vectorstore created")
                print(f"Location: {self.output_folder}")
                print(f"Collection: {self.collection_name}")
                print(f"Records: {self.collection.count()}")
            else:
                print("[FAILED]")
            print("=" * 80)
            
            return success
            
        except Exception as e:
            logger.error(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    parser = argparse.ArgumentParser(
        description="Create ChromaDB vectorstore from Excel files (DYNAMIC)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_vectorstore.py
  python create_vectorstore.py --collection my_data
  python create_vectorstore.py --text-columns "description,summary,notes"
  python create_vectorstore.py --id-column "call_id"

Dynamic Features:
  - All Excel columns stored in metadata automatically
  - Text columns auto-detected for embedding generation
  - ID column auto-detected (or use --id-column)
  - Works with any Excel format - no configuration needed
        """
    )
    
    parser.add_argument('--collection', type=str, default='data',
                        help='Collection name (default: data)')
    parser.add_argument('--output', type=str, default=None,
                        help='Output folder name (default: test_store)')
    parser.add_argument('--text-columns', type=str, default=None,
                        help='Comma-separated list of columns for embedding (default: auto-detect)')
    parser.add_argument('--id-column', type=str, default=None,
                        help='Column to use as document ID (default: auto-detect)')
    parser.add_argument('--preprocess', action='store_true',
                        help='Enable text preprocessing')
    
    args = parser.parse_args()
    
    output_folder = None
    if args.output:
        output_folder = VECTORSTORE_DIR / args.output
    
    text_columns = None
    if args.text_columns:
        text_columns = [c.strip() for c in args.text_columns.split(',')]
    
    creator = UniversalVectorstoreCreator(
        output_folder=output_folder,
        collection_name=args.collection,
        text_columns=text_columns,
        id_column=args.id_column,
        use_preprocessing=args.preprocess
    )
    
    success = creator.run()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
