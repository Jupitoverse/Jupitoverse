#!/usr/bin/env python3
"""
Script to create clean_history_data.db vectorstore with PREPROCESSING
Loads Excel files from past_data folder and applies text cleaning before embedding
"""
import os
import sys
import pandas as pd
import pickle
import numpy as np
from pathlib import Path
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import preprocessing utility
from sr_text_preprocessor import SRTextPreprocessor

# Try to import sentence transformers
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("ERROR: sentence-transformers not available. Please install with: pip install sentence-transformers")
    sys.exit(1)

# Column mappings from Excel to our desired format
COLUMN_MAPPING = {
    'Customer Call ID': 'call_id',
    'Priority': 'priority',
    'Description*': 'description',
    'Resolution Categorization': 'resolution_categorization',
    'Resolution Categorization(Resolution Category Tier 3)': 'resolution_categorization_tier3',
    'SLA Resolution Categorization T1': 'sla_resolution_categorization_t1',
    'SLA Resolution Category': 'sla_resolution_category',
    'Summary*': 'summary',
    'WL_Summary': 'wl_summary',
    'Workaround': 'workaround'
}

# NEW COLUMNS for AI and user feedback
NEW_COLUMNS = {
    'ai_generated_workaround': 'NA',  # Placeholder for AI-generated workarounds
    'user_corrected_workaround': ''   # User-provided corrections (empty by default)
}


def load_excel_files(folder_path='past_data'):
    """Load all Excel files from the specified folder"""
    print(f"\n{'='*80}")
    print(f"LOADING EXCEL FILES")
    print(f"{'='*80}")
    print(f"Folder: {folder_path}")
    
    all_data = []
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f"ERROR: Folder not found: {folder_path}")
        return None
    
    excel_files = list(folder.glob('*.xls')) + list(folder.glob('*.xlsx'))
    
    if not excel_files:
        print(f"ERROR: No Excel files found in {folder_path}")
        return None
    
    print(f"Found {len(excel_files)} Excel files")
    
    for i, file_path in enumerate(sorted(excel_files), 1):
        try:
            print(f"  [{i}/{len(excel_files)}] Loading {file_path.name}...", end='')
            df = pd.read_excel(file_path)
            
            # Rename columns according to mapping
            df.rename(columns=COLUMN_MAPPING, inplace=True)
            
            all_data.append(df)
            print(f" ✓ ({len(df)} rows)")
        except Exception as e:
            print(f" ✗ Error: {e}")
    
    if not all_data:
        print("ERROR: No data loaded from any file")
        return None
    
    # Combine all dataframes
    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"\n✓ Total records loaded: {len(combined_df)}")
    
    # Add new columns with default values
    for col, default_val in NEW_COLUMNS.items():
        if col not in combined_df.columns:
            combined_df[col] = default_val
    
    return combined_df


def create_searchable_text_with_preprocessing(row, preprocessor):
    """
    Create searchable text from row data WITH PREPROCESSING
    
    ✅ ONLY preprocess fields used for MATCHING (description/summary)
    ❌ DO NOT preprocess workarounds/resolutions (they're shown to users - keep full details!)
    """
    parts = []
    
    # 🎯 MATCHING FIELDS - Apply preprocessing (these find similar problems)
    # Only description and summary are used for semantic matching
    matching_fields = ['description', 'summary']
    
    for field in matching_fields:
        if field in row.index:
            value = str(row[field]).strip()
            if value and value.lower() not in ['nan', 'none', '', 'na']:
                # 🆕 PREPROCESS - Remove customer/project noise for better matching
                cleaned_value = preprocessor.clean_for_semantic_search(value)
                if cleaned_value and len(cleaned_value) > 5:
                    parts.append(cleaned_value)
    
    # ✋ IMPORTANT: Resolution, workaround, wl_summary, etc. are NOT preprocessed
    # They stay ORIGINAL in metadata because:
    # 1. They're NOT used for matching (only description/summary are)
    # 2. They're shown to users (need full details like contact names, steps, etc.)
    
    # Add NEW categorization fields for context (light processing only)
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
                # Light preprocessing for category fields (just normalize whitespace)
                value = ' '.join(value.split())
                parts.append(f"{field}: {value}")
    
    return " ".join(parts)


def create_vectorstore_with_preprocessing(df, output_path='vector store/clean_history_data.db'):
    """
    Create vectorstore using Sentence Transformers with PREPROCESSED text
    """
    print(f"\n{'='*80}")
    print(f"CREATING CLEAN VECTORSTORE WITH PREPROCESSING")
    print(f"{'='*80}")
    
    # Initialize preprocessor
    preprocessor = SRTextPreprocessor()
    print("✓ Preprocessor initialized")
    
    # Load Sentence Transformer model
    print("\nLoading Sentence Transformer model (all-MiniLM-L6-v2)...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✓ Model loaded")
    
    # Prepare documents with preprocessing
    print(f"\nPreparing and preprocessing {len(df)} documents...")
    documents = []
    metadata_list = []
    
    for idx, row in df.iterrows():
        # Create searchable text WITH PREPROCESSING
        searchable_text = create_searchable_text_with_preprocessing(row, preprocessor)
        documents.append(searchable_text)
        metadata_list.append(row.to_dict())
        
        if (idx + 1) % 500 == 0:
            print(f"  Processed {idx + 1}/{len(df)} documents...")
    
    print(f"✓ All {len(documents)} documents preprocessed")
    
    # Generate embeddings from CLEANED text
    print(f"\nGenerating embeddings from preprocessed text...")
    print("  (This may take several minutes depending on data size)")
    embeddings = model.encode(documents, show_progress_bar=True, batch_size=32)
    print(f"✓ Embeddings generated: shape {embeddings.shape}")
    
    # Create database dictionary
    print(f"\nCreating database structure...")
    db_data = {
        'embeddings': embeddings,
        'documents': documents,  # These are PREPROCESSED (description/summary only)
        'metadata': metadata_list,  # 🆕 Workarounds/resolutions stay ORIGINAL here!
        'model_name': 'all-MiniLM-L6-v2',
        'created_at': datetime.now().isoformat(),
        'total_records': len(df),
        'columns': [
            'call_id',
            'priority',
            'description',
            'resolution_categorization',
            'resolution_categorization_tier3',
            'sla_resolution_categorization_t1',
            'sla_resolution_category',
            'summary',
            'wl_summary',
            'workaround',
            'ai_generated_workaround',
            'user_corrected_workaround'
        ],
        'preprocessed': True,  # 🆕 FLAG to indicate preprocessing was applied
        'preprocessing_version': '3.0',  # Updated version with new categorization fields
        'preprocessing_applied': {
            'fields_preprocessed': ['description', 'summary'],  # ONLY these!
            'fields_kept_original': [
                'workaround', 
                'wl_summary', 
                'ai_generated_workaround', 
                'user_corrected_workaround',
                'resolution_categorization',
                'resolution_categorization_tier3',
                'sla_resolution_categorization_t1',
                'sla_resolution_category'
            ],
            'customer_data_removed': True,
            'project_data_removed': True,
            'plan_data_removed': True,
            'ids_removed': True,
            'timestamps_removed': True,
            'activity_names_preserved': True,
            'technical_terms_preserved': True,
            'workarounds_preserved': True,
            'categorization_preserved': True  # SLA categorization fields
        }
    }
    
    # Ensure output directory exists
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Remove existing file if it exists
    if Path(output_path).exists():
        print(f"  Removing existing file: {output_path}")
        os.remove(output_path)
    
    # Save to pickle
    print(f"\nSaving to {output_path}...")
    with open(output_path, 'wb') as f:
        pickle.dump(db_data, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    print(f"✓ Vectorstore saved successfully!")
    
    return db_data


def validate_vectorstore(db_path='vector store/clean_history_data.db'):
    """Validate the created vectorstore"""
    print(f"\n{'='*80}")
    print(f"VALIDATING VECTORSTORE")
    print(f"{'='*80}")
    
    try:
        with open(db_path, 'rb') as f:
            db_data = pickle.load(f)
        
        print(f"✓ File loaded successfully")
        print(f"\nDatabase Info:")
        print(f"  - Total records: {db_data.get('total_records', 0)}")
        print(f"  - Model: {db_data.get('model_name', 'unknown')}")
        print(f"  - Preprocessed: {db_data.get('preprocessed', False)}")
        print(f"  - Preprocessing version: {db_data.get('preprocessing_version', 'N/A')}")
        print(f"  - Embedding shape: {db_data['embeddings'].shape}")
        print(f"  - Columns: {len(db_data.get('columns', []))}")
        print(f"  - Created: {db_data.get('created_at', 'unknown')}")
        
        # Show sample of preprocessed text
        print(f"\nSample preprocessed documents (first 3):")
        for i, doc in enumerate(db_data['documents'][:3], 1):
            print(f"  [{i}] {doc[:150]}...")
        
        print(f"\n✓ Validation complete!")
        return True
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return False


def main():
    """Main function"""
    print("\n" + "="*80)
    print(" CREATE CLEAN HISTORY VECTORSTORE WITH PREPROCESSING")
    print("="*80)
    print(f" Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Step 1: Load Excel files
    df = load_excel_files('past_data')
    if df is None:
        print("\n✗ Failed to load data. Exiting.")
        return False
    
    # Step 2: Create vectorstore with preprocessing
    output_path = 'vector store/clean_history_data.db'
    db_data = create_vectorstore_with_preprocessing(df, output_path)
    
    # Step 3: Validate
    success = validate_vectorstore(output_path)
    
    # Summary
    print(f"\n{'='*80}")
    if success:
        print("✅ SUCCESS! Clean vectorstore created successfully")
        print(f"{'='*80}")
        print(f"\nOutput file: {os.path.abspath(output_path)}")
        print(f"Total records: {db_data['total_records']}")
        print(f"Preprocessed: YES")
        print(f"\nNext steps:")
        print(f"  1. Update batch_sr_analyser.py to use clean_history_data.db")
        print(f"  2. Update batch_sr_analyser.py to preprocess queries")
        print(f"  3. Test with sample queries to verify improved matching")
    else:
        print("✗ FAILED! Check errors above")
        print(f"{'='*80}")
    
    print(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    return success


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

