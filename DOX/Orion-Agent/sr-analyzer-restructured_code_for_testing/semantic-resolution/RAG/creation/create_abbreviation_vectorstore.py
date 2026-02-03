#!/usr/bin/env python3
"""
Script to create or update abbreviation.db vectorstore from Excel file
Reads ABBREVIATION_v2.xlsx and creates a searchable vectorstore

Usage:
    python create_abbreviation_vectorstore.py
"""
import os
import sys
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# Try to import sentence transformers
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("ERROR: sentence-transformers not available. Please install with: pip install sentence-transformers")
    sys.exit(1)


# Configuration
EXCEL_FILE = "Abbreviation/ABBREVIATION_v2.xlsx"
OUTPUT_PATH = "../data/database/abbreviation.db"


def load_abbreviation_excel(file_path):
    """Load the abbreviation Excel file"""
    print(f"\n{'='*80}")
    print("LOADING ABBREVIATION EXCEL FILE")
    print(f"{'='*80}")
    print(f"File: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        return None
    
    try:
        df = pd.read_excel(file_path)
        print(f"[OK] Loaded successfully!")
        print(f"  - Total rows: {len(df)}")
        print(f"  - Columns: {list(df.columns)}")
        
        # Fill NaN values
        df = df.fillna('')
        
        # Convert all columns to strings
        for col in df.columns:
            df[col] = df[col].astype(str)
        
        return df
    except Exception as e:
        print(f"ERROR: Failed to load Excel file: {e}")
        return None


def create_searchable_text(row):
    """
    Create searchable text from abbreviation row
    Combines abbreviation and its full form/meaning for semantic search
    """
    parts = []
    
    # Add all columns to searchable text
    for col in row.index:
        value = str(row[col]).strip()
        if value and value.lower() not in ['nan', 'none', '', 'na']:
            parts.append(f"{col}: {value}")
    
    return " | ".join(parts)


def create_abbreviation_vectorstore(df, output_path):
    """
    Create or rewrite the abbreviation vectorstore
    """
    print(f"\n{'='*80}")
    print("CREATING ABBREVIATION VECTORSTORE")
    print(f"{'='*80}")
    
    # Check if vectorstore exists
    if os.path.exists(output_path):
        print(f"[INFO] Existing vectorstore found at {output_path}")
        print("[INFO] Will be overwritten with new data")
    else:
        print(f"[INFO] Creating new vectorstore at {output_path}")
    
    # Load Sentence Transformer model
    print("\nLoading Sentence Transformer model (all-MiniLM-L6-v2)...")
    # Load model then move to CPU (avoids meta tensor error)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    model = model.cpu()
    print("[OK] Model loaded successfully!")
    
    # Prepare documents
    print(f"\nPreparing {len(df)} abbreviation entries...")
    documents = []
    metadata_list = []
    
    for idx, row in df.iterrows():
        # Create searchable text
        searchable_text = create_searchable_text(row)
        documents.append(searchable_text)
        metadata_list.append(row.to_dict())
        
        if (idx + 1) % 100 == 0:
            print(f"  Processed {idx + 1}/{len(df)} entries...")
    
    print(f"[OK] All {len(documents)} entries prepared")
    
    # Generate embeddings
    print(f"\nGenerating embeddings...")
    print("  (This may take a while depending on data size)")
    embeddings = model.encode(documents, show_progress_bar=True, batch_size=32)
    print(f"[OK] Embeddings generated: shape {embeddings.shape}")
    
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
        'description': 'Abbreviation Vectorstore - Maps abbreviations to their full forms',
        'version': '1.0',
        'source_file': EXCEL_FILE
    }
    
    # Ensure output directory exists
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Remove existing file if it exists (rewrite)
    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"[OK] Removed existing vectorstore")
    
    # Save as pickle
    print(f"\nSaving vectorstore to {output_path}...")
    with open(output_path, 'wb') as f:
        pickle.dump(db_data, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    print(f"[OK] Vectorstore saved successfully!")
    print(f"  - Location: {os.path.abspath(output_path)}")
    print(f"  - Total entries: {len(documents)}")
    print(f"  - Embedding dimensions: {embeddings.shape}")
    
    return db_data


def test_vectorstore(db_path, test_query="API"):
    """Test the created vectorstore with a sample query"""
    print(f"\n{'='*80}")
    print("TESTING VECTORSTORE")
    print(f"{'='*80}")
    
    try:
        # Load database
        with open(db_path, 'rb') as f:
            db_data = pickle.load(f)
        
        print(f"[OK] Vectorstore loaded")
        print(f"  - Total records: {db_data['total_records']}")
        print(f"  - Model: {db_data['model_name']}")
        
        # Load model
        # Load model then move to CPU (avoids meta tensor error)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    model = model.cpu()
        
        # Encode test query
        print(f"\nTest query: '{test_query}'")
        query_embedding = model.encode([test_query])[0]
        
        # Calculate similarities
        embeddings = db_data['embeddings']
        similarities = np.dot(embeddings, query_embedding) / (
            np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
        )
        
        # Get top 3 results
        top_indices = np.argsort(similarities)[::-1][:3]
        
        print(f"\nTop 3 matches:")
        for i, idx in enumerate(top_indices, 1):
            metadata = db_data['metadata'][idx]
            print(f"\n  [{i}] Score: {similarities[idx]:.4f}")
            for key, value in metadata.items():
                if value and str(value).strip() not in ['nan', 'none', '']:
                    print(f"      {key}: {value}")
        
        print(f"\n[OK] Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        return False


def main():
    """Main execution function"""
    print("\n" + "="*80)
    print(" ABBREVIATION VECTORSTORE CREATOR")
    print("="*80)
    print(f" Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f" Excel file: {EXCEL_FILE}")
    print(f" Output: {OUTPUT_PATH}")
    print("="*80)
    
    try:
        # Step 1: Load Excel file
        df = load_abbreviation_excel(EXCEL_FILE)
        if df is None:
            print("\n[FAIL] Failed to load Excel file. Exiting.")
            return False
        
        # Step 2: Create vectorstore
        db_data = create_abbreviation_vectorstore(df, OUTPUT_PATH)
        
        # Step 3: Test vectorstore
        test_vectorstore(OUTPUT_PATH)
        
        # Summary
        print(f"\n{'='*80}")
        print("[SUCCESS] Abbreviation vectorstore created successfully!")
        print(f"{'='*80}")
        print(f"\nSummary:")
        print(f"  - Source: {EXCEL_FILE}")
        print(f"  - Output: {os.path.abspath(OUTPUT_PATH)}")
        print(f"  - Total entries: {db_data['total_records']}")
        print(f"  - Columns: {db_data['columns']}")
        
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

