#!/usr/bin/env python3
"""
Script to create workaround_comments.db vectorstore
Loads Workaround_Comments_Final.xlsx and creates semantic embeddings for workaround guidelines
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

# Try to import sentence transformers
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("ERROR: sentence-transformers not available. Please install with: pip install sentence-transformers")
    sys.exit(1)


def load_workaround_comments_excel(file_path='category mapping/Workaround_Comments_Final.xlsx'):
    """Load workaround comments from Excel file"""
    print(f"\n{'='*80}")
    print(f"LOADING WORKAROUND COMMENTS DATA")
    print(f"{'='*80}")
    print(f"File: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        return None
    
    try:
        print(f"Loading {file_path}...", end='')
        df = pd.read_excel(file_path)
        print(f" ✓ ({len(df)} rows)")
        
        # Show columns
        print(f"\nColumns found:")
        for col in df.columns:
            print(f"  - {col}")
        
        # Clean up column names (remove extra spaces)
        df.columns = df.columns.str.strip()
        
        # Show data info
        print(f"\nData Summary:")
        print(f"  - Total records: {len(df)}")
        print(f"  - Unique SLA Resolution Categories: {df['SLA Resolution Category'].nunique()}")
        print(f"  - Unique Resolution Categorization T2: {df['Resolution Categorization T2'].nunique()}")
        print(f"  - Unique Resolution Category Tier 3: {df['Resolution Category Tier 3'].nunique()}")
        
        return df
    except Exception as e:
        print(f" ✗ Error: {e}")
        return None


def create_searchable_text(row):
    """
    Create searchable text from row data for semantic matching
    
    Combines categorization fields with workaround information for better matching
    """
    parts = []
    
    # Add categorization fields for context
    category_fields = [
        'Resolution Categorization T2',
        'Resolution Category Tier 3',
        'SLA Resolution Categorization T1',
        'SLA Resolution Category'
    ]
    
    for field in category_fields:
        if field in row.index:
            value = str(row[field]).strip()
            if value and value.lower() not in ['nan', 'none', '', 'na']:
                # Normalize whitespace
                value = ' '.join(value.split())
                parts.append(value)
    
    # Add actual workaround comment (the actual text from past records)
    if 'Actual Workaround Comment' in row.index:
        value = str(row['Actual Workaround Comment']).strip()
        if value and value.lower() not in ['nan', 'none', '', 'na']:
            parts.append(f"Comment: {value}")
    
    # Add workaround guideline (the standardized guideline)
    if 'Workaround Guideline' in row.index:
        value = str(row['Workaround Guideline']).strip()
        if value and value.lower() not in ['nan', 'none', '', 'na']:
            parts.append(f"Guideline: {value}")
    
    return " | ".join(parts)


def create_vectorstore(df, output_path='data/vectorstore/workaround_comments.db'):
    """
    Create vectorstore using Sentence Transformers
    """
    print(f"\n{'='*80}")
    print(f"CREATING WORKAROUND COMMENTS VECTORSTORE")
    print(f"{'='*80}")
    
    # Load Sentence Transformer model
    print("\nLoading Sentence Transformer model (all-MiniLM-L6-v2)...")
    # Load model then move to CPU (avoids meta tensor error)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    model = model.cpu()
    print("✓ Model loaded")
    
    # Prepare documents
    print(f"\nPreparing {len(df)} documents...")
    documents = []
    metadata_list = []
    
    for idx, row in df.iterrows():
        # Create searchable text
        searchable_text = create_searchable_text(row)
        documents.append(searchable_text)
        metadata_list.append(row.to_dict())
        
        if (idx + 1) % 500 == 0:
            print(f"  Processed {idx + 1}/{len(df)} documents...")
    
    print(f"✓ All {len(documents)} documents prepared")
    
    # Generate embeddings
    print(f"\nGenerating embeddings...")
    print("  (This may take several minutes depending on data size)")
    embeddings = model.encode(documents, show_progress_bar=True, batch_size=32)
    print(f"✓ Embeddings generated: shape {embeddings.shape}")
    
    # Create database dictionary
    print(f"\nCreating database structure...")
    db_data = {
        'embeddings': embeddings,
        'documents': documents,
        'metadata': metadata_list,
        'model_name': 'all-MiniLM-L6-v2',
        'created_at': datetime.now().isoformat(),
        'total_records': len(df),
        'columns': list(df.columns),
        'description': 'Workaround Comments Vectorstore - Maps resolution categories to workaround guidelines',
        'version': '1.0'
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
    
    # Get file size
    file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
    print(f"✓ Vectorstore saved successfully! (Size: {file_size:.2f} MB)")
    
    return db_data


def validate_vectorstore(db_path='data/vectorstore/workaround_comments.db'):
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
        print(f"  - Version: {db_data.get('version', 'N/A')}")
        print(f"  - Embedding shape: {db_data['embeddings'].shape}")
        print(f"  - Columns: {len(db_data.get('columns', []))}")
        print(f"  - Created: {db_data.get('created_at', 'unknown')}")
        print(f"  - Description: {db_data.get('description', 'N/A')}")
        
        # Show sample documents
        print(f"\nSample documents (first 3):")
        for i, doc in enumerate(db_data['documents'][:3], 1):
            print(f"  [{i}] {doc[:200]}...")
        
        # Show sample metadata
        print(f"\nSample metadata (first record):")
        if db_data['metadata']:
            first_meta = db_data['metadata'][0]
            for key, value in first_meta.items():
                print(f"  - {key}: {value}")
        
        print(f"\n✓ Validation complete!")
        return True
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return False


def main():
    """Main function"""
    print("\n" + "="*80)
    print(" CREATE WORKAROUND COMMENTS VECTORSTORE")
    print("="*80)
    print(f" Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Step 1: Load Excel file
    df = load_workaround_comments_excel('category mapping/Workaround_Comments_Final.xlsx')
    if df is None:
        print("\n✗ Failed to load data. Exiting.")
        return False
    
    # Step 2: Create vectorstore
    output_path = 'data/vectorstore/workaround_comments.db'
    db_data = create_vectorstore(df, output_path)
    
    # Step 3: Validate
    success = validate_vectorstore(output_path)
    
    # Summary
    print(f"\n{'='*80}")
    if success:
        print("✅ SUCCESS! Workaround Comments vectorstore created successfully")
        print(f"{'='*80}")
        print(f"\nOutput file: {os.path.abspath(output_path)}")
        print(f"Total records: {db_data['total_records']}")
        print(f"\nUsage:")
        print(f"  This vectorstore can be used to find relevant workaround guidelines")
        print(f"  based on resolution categories and past workaround comments.")
        print(f"\nExample query:")
        print(f"  - Search by category: 'Code Quality', 'Configuration Issue', etc.")
        print(f"  - Search by problem description: 'database connection error'")
        print(f"  - Search by workaround type: 'config change', 'restart service', etc.")
    else:
        print("✗ FAILED! Check errors above")
        print(f"{'='*80}")
    
    print(f"\nFinished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    return success


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)



