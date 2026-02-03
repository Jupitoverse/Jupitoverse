#!/usr/bin/env python3
"""
Script to add new training data to existing clean_history_data.db vectorstore
Reads Excel files from 'new excel train' folder and adds new entries incrementally

Usage:
    python add_new_training_data.py
    
    Or specify a custom folder:
    python add_new_training_data.py --folder "path/to/excel/folder"
"""
import os
import sys
import pickle
import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Try to import sentence transformers
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("ERROR: sentence-transformers not available. Please install with: pip install sentence-transformers")
    sys.exit(1)

# Try to import preprocessor
try:
    from analyzers.sr_text_preprocessor import SRTextPreprocessor
    PREPROCESSOR_AVAILABLE = True
except ImportError:
    PREPROCESSOR_AVAILABLE = False
    print("WARNING: SRTextPreprocessor not available - text won't be preprocessed")

# Column mappings from Excel to our desired format
COLUMN_MAPPING = {
    'Customer Call ID': 'call_id',
    'Priority': 'priority',
    'Description*': 'description',
    'Description': 'description',  # Alternative column name
    'Functional Category': 'function_category',
    'Resolution Categorization': 'resolution_categorization',
    'Resolution Categorization(Resolution Category Tier 3)': 'resolution_categorization_tier3',
    'SLA Resolution Categorization T1': 'sla_resolution_categorization_t1',
    'SLA Resolution Category': 'sla_resolution_category',
    'Resolution': 'resolution',
    'Status_Reason': 'status_reason',
    'Summary*': 'summary',
    'Summary': 'summary',  # Alternative column name
    'WL_Summary': 'wl_summary',
    'Workaround': 'workaround',
    'Status': 'status',
    'Application': 'application',
    'Assigned To': 'assigned_to',
    'Reported Date': 'reported_date'
}

# Default values for new columns
NEW_COLUMNS = {
    'ai_generated_workaround': 'NA',
    'user_corrected_workaround': ''
}


def load_existing_vectorstore(db_path):
    """Load the existing vectorstore database"""
    print(f"\n{'='*80}")
    print("LOADING EXISTING VECTORSTORE")
    print(f"{'='*80}")
    
    if not os.path.exists(db_path):
        print(f"ERROR: Vectorstore not found at {db_path}")
        return None
    
    print(f"Loading from: {db_path}")
    
    with open(db_path, 'rb') as f:
        db_data = pickle.load(f)
    
    print(f"[OK] Vectorstore loaded successfully!")
    print(f"  - Total existing records: {db_data.get('total_records', len(db_data.get('metadata', [])))}")
    print(f"  - Model: {db_data.get('model_name', 'unknown')}")
    print(f"  - Preprocessed: {db_data.get('preprocessed', False)}")
    print(f"  - Created: {db_data.get('created_at', 'unknown')}")
    
    return db_data


def get_existing_sr_ids(db_data):
    """Extract all existing SR IDs from the vectorstore"""
    existing_ids = set()
    
    for metadata in db_data.get('metadata', []):
        sr_id = metadata.get('call_id', '')
        if sr_id:
            existing_ids.add(str(sr_id).strip().upper())
    
    return existing_ids


def load_new_excel_files(folder_path):
    """Load all Excel files from the specified folder"""
    print(f"\n{'='*80}")
    print("LOADING NEW EXCEL FILES")
    print(f"{'='*80}")
    print(f"Folder: {folder_path}")
    
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"ERROR: Folder not found: {folder_path}")
        return None
    
    # Find Excel files (exclude any .db files)
    excel_files = [f for f in folder.glob('*.xls') if not f.name.endswith('.db')]
    excel_files += [f for f in folder.glob('*.xlsx') if not f.name.endswith('.db')]
    
    if not excel_files:
        print(f"ERROR: No Excel files found in {folder_path}")
        return None
    
    print(f"Found {len(excel_files)} Excel files:")
    
    all_data = []
    for i, file_path in enumerate(sorted(excel_files), 1):
        try:
            print(f"  [{i}/{len(excel_files)}] Loading {file_path.name}...", end='')
            df = pd.read_excel(file_path)
            
            # Rename columns according to mapping
            rename_dict = {}
            for excel_col, our_col in COLUMN_MAPPING.items():
                if excel_col in df.columns:
                    rename_dict[excel_col] = our_col
            
            df.rename(columns=rename_dict, inplace=True)
            
            all_data.append(df)
            print(f" [OK] ({len(df)} rows)")
        except Exception as e:
            print(f" [ERROR] Error: {e}")
    
    if not all_data:
        print("ERROR: No data loaded from any file")
        return None
    
    # Combine all dataframes
    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"\n[OK] Total records loaded: {len(combined_df)}")
    
    # Add new columns with default values if they don't exist
    for col, default_val in NEW_COLUMNS.items():
        if col not in combined_df.columns:
            combined_df[col] = default_val
    
    # Fill NaN values
    combined_df = combined_df.fillna('')
    
    return combined_df


def create_searchable_text(row, preprocessor=None, use_preprocessing=False):
    """Create searchable text from row data
    
    NOTE: 'summary' field removed - was redundant (just prefix of description)
    """
    parts = []
    
    # Matching field - only description (summary was redundant)
    if 'description' in row.index:
        value = str(row['description']).strip()
        if value and value.lower() not in ['nan', 'none', '', 'na']:
            if use_preprocessing and preprocessor:
                value = preprocessor.clean_for_semantic_search(value)
            if value and len(value) > 5:
                parts.append(value)
    
    # Category fields (for context)
    category_fields = [
        'resolution_categorization',
        'resolution_categorization_tier3',
        'sla_resolution_categorization_t1',
        'sla_resolution_category'
    ]
    
    for field in category_fields:
        if field in row.index:
            value = str(row[field]).strip()
            if value and value.lower() not in ['nan', 'none', '', 'na']:
                parts.append(f"{field}: {value}")
    
    return " ".join(parts)


def add_new_entries_to_vectorstore(db_data, new_df, model, preprocessor=None):
    """Add new entries to the vectorstore"""
    print(f"\n{'='*80}")
    print("ADDING NEW ENTRIES TO VECTORSTORE")
    print(f"{'='*80}")
    
    # Get existing SR IDs
    existing_ids = get_existing_sr_ids(db_data)
    print(f"Existing SRs in vectorstore: {len(existing_ids)}")
    
    # Check if database uses preprocessing
    use_preprocessing = db_data.get('preprocessed', False)
    print(f"Database uses preprocessing: {use_preprocessing}")
    
    # Filter out duplicates
    new_entries = []
    duplicate_count = 0
    
    for idx, row in new_df.iterrows():
        sr_id = str(row.get('call_id', '')).strip().upper()
        
        if not sr_id:
            continue
        
        if sr_id in existing_ids:
            duplicate_count += 1
            continue
        
        new_entries.append(row)
        existing_ids.add(sr_id)  # Prevent duplicates within new data
    
    print(f"New entries to add: {len(new_entries)}")
    print(f"Duplicates skipped: {duplicate_count}")
    
    if not new_entries:
        print("\n[WARN] No new entries to add (all are duplicates)")
        return 0
    
    # Prepare new documents and embeddings
    print(f"\nPreparing {len(new_entries)} new documents...")
    
    new_documents = []
    new_metadata = []
    
    for i, row in enumerate(new_entries):
        # Create searchable text
        searchable_text = create_searchable_text(row, preprocessor, use_preprocessing)
        new_documents.append(searchable_text)
        
        # Create metadata
        metadata = {
            'call_id': str(row.get('call_id', '')).strip(),
            'priority': str(row.get('priority', '')).strip(),
            'description': str(row.get('description', '')).strip(),
            # 'summary' removed - was redundant (just prefix of description)
            'wl_summary': str(row.get('wl_summary', '')).strip(),
            'function_category': str(row.get('function_category', '')).strip(),
            'resolution_categorization': str(row.get('resolution_categorization', '')).strip(),
            'resolution_categorization_tier3': str(row.get('resolution_categorization_tier3', '')).strip(),
            'sla_resolution_categorization_t1': str(row.get('sla_resolution_categorization_t1', '')).strip(),
            'sla_resolution_category': str(row.get('sla_resolution_category', '')).strip(),
            'resolution': str(row.get('resolution', '')).strip(),
            'status_reason': str(row.get('status_reason', '')).strip(),
            'workaround': str(row.get('workaround', '')).strip(),
            'status': str(row.get('status', '')).strip(),
            'application': str(row.get('application', '')).strip(),
            'assigned_to': str(row.get('assigned_to', '')).strip(),
            'ai_generated_workaround': str(row.get('ai_generated_workaround', 'NA')).strip(),
            'user_corrected_workaround': str(row.get('user_corrected_workaround', '')).strip(),
            'source': 'new_excel_train',
            'added_date': datetime.now().isoformat()
        }
        new_metadata.append(metadata)
        
        if (i + 1) % 100 == 0:
            print(f"  Prepared {i + 1}/{len(new_entries)} documents...")
    
    print(f"[OK] All documents prepared")
    
    # Generate embeddings for new documents
    print(f"\nGenerating embeddings for {len(new_documents)} new documents...")
    print("  (This may take a while depending on data size)")
    
    new_embeddings = model.encode(new_documents, show_progress_bar=True, batch_size=32)
    print(f"[OK] Embeddings generated: shape {new_embeddings.shape}")
    
    # Append to existing data
    print(f"\nAppending to existing vectorstore...")
    
    # Update documents
    db_data['documents'].extend(new_documents)
    
    # Update metadata
    db_data['metadata'].extend(new_metadata)
    
    # Update embeddings
    if isinstance(db_data['embeddings'], np.ndarray):
        db_data['embeddings'] = np.vstack([db_data['embeddings'], new_embeddings])
    else:
        print("ERROR: Embeddings format not supported")
        return 0
    
    # Update metadata
    db_data['total_records'] = len(db_data['metadata'])
    db_data['last_updated'] = datetime.now().isoformat()
    
    print(f"[OK] New entries appended successfully!")
    print(f"  - Previous total: {len(db_data['metadata']) - len(new_entries)}")
    print(f"  - Added: {len(new_entries)}")
    print(f"  - New total: {len(db_data['metadata'])}")
    
    return len(new_entries)


def save_vectorstore(db_data, db_path):
    """Save the updated vectorstore"""
    print(f"\n{'='*80}")
    print("SAVING UPDATED VECTORSTORE")
    print(f"{'='*80}")
    
    # Create backup
    backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    if os.path.exists(db_path):
        import shutil
        shutil.copy2(db_path, backup_path)
        print(f"[OK] Backup created: {backup_path}")
    
    # Save updated vectorstore
    with open(db_path, 'wb') as f:
        pickle.dump(db_data, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    print(f"[OK] Vectorstore saved: {db_path}")
    print(f"  - Total records: {db_data['total_records']}")
    print(f"  - Embedding shape: {db_data['embeddings'].shape}")
    
    return True


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Add new training data to existing vectorstore')
    parser.add_argument('--folder', type=str, default='new excel train',
                        help='Folder containing new Excel files (default: "new excel train")')
    parser.add_argument('--vectorstore', type=str, default='data/database/clean_history_data.db',
                        help='Path to vectorstore (default: "data/database/clean_history_data.db")')
    
    args = parser.parse_args()
    
    print("\n" + "="*80)
    print(" ADD NEW TRAINING DATA TO VECTORSTORE")
    print("="*80)
    print(f" Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" Source folder: {args.folder}")
    print(f" Vectorstore: {args.vectorstore}")
    print("="*80)
    
    try:
        # Step 1: Load existing vectorstore
        db_data = load_existing_vectorstore(args.vectorstore)
        if db_data is None:
            print("\n[FAIL] Failed to load vectorstore. Exiting.")
            return False
        
        # Step 2: Load new Excel files
        new_df = load_new_excel_files(args.folder)
        if new_df is None:
            print("\n[FAIL] Failed to load new Excel files. Exiting.")
            return False
        
        # Step 3: Load sentence transformer model
        print(f"\n{'='*80}")
        print("LOADING SENTENCE TRANSFORMER MODEL")
        print(f"{'='*80}")
        model_name = db_data.get('model_name', 'all-MiniLM-L6-v2')
        print(f"Loading model: {model_name}")
        # Load model then move to CPU (avoids meta tensor error)
        model = SentenceTransformer(model_name)
        model = model.cpu()
        print("[OK] Model loaded successfully!")
        
        # Step 4: Initialize preprocessor if needed
        preprocessor = None
        if PREPROCESSOR_AVAILABLE and db_data.get('preprocessed', False):
            preprocessor = SRTextPreprocessor()
            print("[OK] Preprocessor initialized")
        
        # Step 5: Add new entries
        added_count = add_new_entries_to_vectorstore(db_data, new_df, model, preprocessor)
        
        if added_count > 0:
            # Step 6: Save updated vectorstore
            save_vectorstore(db_data, args.vectorstore)
        
        # Summary
        print(f"\n{'='*80}")
        if added_count > 0:
            print("[SUCCESS] SUCCESS! New training data added to vectorstore")
        else:
            print("[WARN] No new entries added (all duplicates)")
        print(f"{'='*80}")
        print(f"\nSummary:")
        print(f"  - Source folder: {args.folder}")
        print(f"  - Vectorstore: {args.vectorstore}")
        print(f"  - New entries added: {added_count}")
        print(f"  - Total records: {db_data['total_records']}")
        
        print(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        
        return True
        
    except Exception as e:
        print(f"\n[FAIL] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

