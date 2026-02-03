#!/usr/bin/env python3
"""
Script to create history_data.db vectorstore from Excel files in past_data folder
Using a simpler pickle-based approach with sentence transformers for embeddings
"""
import os
import pandas as pd
import pickle
import numpy as np
from pathlib import Path
from datetime import datetime
import json

# Try to import sentence transformers, if not available use a simple approach
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    print("WARNING: sentence-transformers not available. Using TF-IDF instead.")
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

# Column mappings from Excel to our desired format
COLUMN_MAPPING = {
    'Customer Call ID': 'call_id',
    'Priority': 'priority',
    'Description*': 'description',
    'Functional Category': 'function_category',
    'Resolution Categorization': 'resolution_categorization',
    'Resolution': 'resolution',
    'Status_Reason': 'status_reason',
    # 'Summary*' removed - was redundant (just prefix of description)
    'WL_Summary': 'wl_summary',
    'Workaround': 'workaround'
}

# NEW COLUMNS for user feedback integration
NEW_COLUMNS = {
    'ai_generated_workaround': 'NA',  # Placeholder for AI-generated workarounds
    'user_corrected_workaround': ''   # User-provided corrections (empty by default)
}

def load_excel_files(folder_path='past_data'):
    """Load all Excel files from the specified folder"""
    print(f"Loading Excel files from {folder_path}...")
    
    all_data = []
    folder = Path(folder_path)
    excel_files = list(folder.glob('*.xls')) + list(folder.glob('*.xlsx'))
    
    print(f"Found {len(excel_files)} Excel files")
    
    for excel_file in excel_files:
        print(f"  Processing: {excel_file.name}")
        try:
            df = pd.read_excel(excel_file)
            print(f"    Loaded {len(df)} rows")
            all_data.append(df)
        except Exception as e:
            print(f"    ERROR loading {excel_file.name}: {e}")
    
    if not all_data:
        raise ValueError("No data loaded from Excel files!")
    
    # Combine all dataframes
    combined_df = pd.concat(all_data, ignore_index=True)
    print(f"\nTotal rows combined: {len(combined_df)}")
    
    # Remove duplicates based on call_id if it exists
    if 'Customer Call ID' in combined_df.columns:
        initial_count = len(combined_df)
        combined_df = combined_df.drop_duplicates(subset=['Customer Call ID'], keep='first')
        removed = initial_count - len(combined_df)
        if removed > 0:
            print(f"Removed {removed} duplicate records")
    
    return combined_df

def extract_relevant_columns(df):
    """Extract and rename relevant columns"""
    print("\nExtracting relevant columns...")
    
    # Check which columns exist in the dataframe
    available_columns = {}
    missing_columns = []
    
    for excel_col, our_col in COLUMN_MAPPING.items():
        if excel_col in df.columns:
            available_columns[excel_col] = our_col
        else:
            missing_columns.append(excel_col)
            print(f"  WARNING: Column '{excel_col}' not found in data")
    
    if missing_columns:
        print(f"\nMissing columns: {missing_columns}")
    
    # Extract available columns
    extracted_df = df[list(available_columns.keys())].copy()
    
    # Rename columns
    extracted_df.rename(columns=available_columns, inplace=True)
    
    # Fill NaN values with empty strings
    extracted_df = extracted_df.fillna('')
    
    # Convert all columns to strings
    for col in extracted_df.columns:
        extracted_df[col] = extracted_df[col].astype(str)
    
    # ADD NEW COLUMNS for user feedback integration
    print("\nAdding new columns for user feedback integration...")
    for new_col, default_value in NEW_COLUMNS.items():
        extracted_df[new_col] = default_value
        print(f"  Added column: '{new_col}' (default: '{default_value}')")
    
    print(f"Extracted {len(extracted_df)} records with {len(extracted_df.columns)} columns")
    print(f"Columns: {list(extracted_df.columns)}")
    
    return extracted_df

def create_searchable_text(row):
    """Create a searchable text from all relevant fields"""
    parts = []
    
    # Priority fields for search (summary removed - was redundant)
    priority_fields = ['description', 'resolution', 'workaround']
    
    # Add priority fields first
    for field in priority_fields:
        if field in row.index:
            value = str(row[field]).strip()
            if value and value.lower() not in ['nan', 'none', '']:
                parts.append(value)
    
    # Add other fields
    for col in row.index:
        if col not in priority_fields:
            value = str(row[col]).strip()
            if value and value.lower() not in ['nan', 'none', '']:
                parts.append(f"{col}: {value}")
    
    return " ".join(parts)

def create_vectorstore_sentence_transformers(df, db_path='history_data.db'):
    """Create vectorstore using sentence transformers"""
    print(f"\nCreating vectorstore with Sentence Transformers...")
    print("Loading model (this may take a while)...")
    
    # Load model then move to CPU (avoids meta tensor error)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    model = model.cpu()
    
    # Prepare documents
    print("Preparing documents...")
    documents = []
    metadata_list = []
    
    for idx, row in df.iterrows():
        searchable_text = create_searchable_text(row)
        documents.append(searchable_text)
        metadata_list.append(row.to_dict())
        
        if (idx + 1) % 100 == 0:
            print(f"  Prepared {idx + 1}/{len(df)} documents...")
    
    # Create embeddings
    print("\nGenerating embeddings (this may take a while)...")
    embeddings = model.encode(documents, show_progress_bar=True, batch_size=32)
    
    # Save to database
    print(f"\nSaving to {db_path}...")
    
    # Create database dictionary
    db_data = {
        'embeddings': embeddings,
        'documents': documents,
        'metadata': metadata_list,
        'model_name': 'all-MiniLM-L6-v2',
        'created_at': datetime.now().isoformat(),
        'total_records': len(df),
        'columns': list(df.columns)
    }
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Save as pickle
    with open(db_path, 'wb') as f:
        pickle.dump(db_data, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    print(f"\nVectorstore created successfully!")
    print(f"  Location: {os.path.abspath(db_path)}")
    print(f"  Total documents: {len(documents)}")
    print(f"  Embedding dimensions: {embeddings.shape}")
    
    return db_data

def create_vectorstore_tfidf(df, db_path='history_data.db'):
    """Create vectorstore using TF-IDF (fallback)"""
    print(f"\nCreating vectorstore with TF-IDF...")
    
    # Prepare documents
    print("Preparing documents...")
    documents = []
    metadata_list = []
    
    for idx, row in df.iterrows():
        searchable_text = create_searchable_text(row)
        documents.append(searchable_text)
        metadata_list.append(row.to_dict())
        
        if (idx + 1) % 100 == 0:
            print(f"  Prepared {idx + 1}/{len(df)} documents...")
    
    # Create TF-IDF vectorizer
    print("\nGenerating TF-IDF vectors...")
    vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Save to database
    print(f"\nSaving to {db_path}...")
    
    # Create database dictionary
    db_data = {
        'tfidf_matrix': tfidf_matrix,
        'vectorizer': vectorizer,
        'documents': documents,
        'metadata': metadata_list,
        'model_name': 'TF-IDF',
        'created_at': datetime.now().isoformat(),
        'total_records': len(df),
        'columns': list(df.columns)
    }
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Save as pickle
    with open(db_path, 'wb') as f:
        pickle.dump(db_data, f, protocol=pickle.HIGHEST_PROTOCOL)
    
    print(f"\nVectorstore created successfully!")
    print(f"  Location: {os.path.abspath(db_path)}")
    print(f"  Total documents: {len(documents)}")
    print(f"  Vector dimensions: {tfidf_matrix.shape}")
    
    return db_data

def search_vectorstore_sentence_transformers(db_path, query, top_k=5):
    """Search vectorstore created with sentence transformers"""
    # Load database
    with open(db_path, 'rb') as f:
        db_data = pickle.load(f)
    
    # Load model
    # Load model then move to CPU (avoids meta tensor error)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    model = model.cpu()
    
    # Encode query
    query_embedding = model.encode([query])[0]
    
    # Calculate similarities
    embeddings = db_data['embeddings']
    similarities = np.dot(embeddings, query_embedding) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_embedding)
    )
    
    # Get top k results
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        results.append({
            'score': float(similarities[idx]),
            'metadata': db_data['metadata'][idx],
            'document': db_data['documents'][idx][:200] + '...'
        })
    
    return results

def search_vectorstore_tfidf(db_path, query, top_k=5):
    """Search vectorstore created with TF-IDF"""
    # Load database
    with open(db_path, 'rb') as f:
        db_data = pickle.load(f)
    
    # Vectorize query
    query_vector = db_data['vectorizer'].transform([query])
    
    # Calculate similarities
    similarities = cosine_similarity(query_vector, db_data['tfidf_matrix'])[0]
    
    # Get top k results
    top_indices = np.argsort(similarities)[::-1][:top_k]
    
    results = []
    for idx in top_indices:
        results.append({
            'score': float(similarities[idx]),
            'metadata': db_data['metadata'][idx],
            'document': db_data['documents'][idx][:200] + '...'
        })
    
    return results

def test_vectorstore(db_path='history_data.db'):
    """Test the created vectorstore with sample queries"""
    print("\n" + "="*80)
    print("Testing vectorstore with sample queries...")
    print("="*80)
    
    # Load database to check model type
    with open(db_path, 'rb') as f:
        db_data = pickle.load(f)
    
    model_name = db_data.get('model_name', 'unknown')
    print(f"\nModel: {model_name}")
    print(f"Total records: {db_data['total_records']}")
    
    # Test queries
    test_queries = [
        "password reset issue",
        "network connectivity problem",
        "database error"
    ]
    
    for query in test_queries:
        print(f"\n{'='*80}")
        print(f"Query: '{query}'")
        print('-'*80)
        
        if model_name == 'TF-IDF':
            results = search_vectorstore_tfidf(db_path, query, top_k=3)
        else:
            results = search_vectorstore_sentence_transformers(db_path, query, top_k=3)
        
        for i, result in enumerate(results, 1):
            print(f"\nResult {i} (score: {result['score']:.4f}):")
            metadata = result['metadata']
            print(f"  Call ID: {metadata.get('call_id', 'N/A')}")
            print(f"  Priority: {metadata.get('priority', 'N/A')}")
            print(f"  Description: {metadata.get('description', 'N/A')[:100]}...")
            if metadata.get('resolution'):
                print(f"  Resolution: {metadata.get('resolution', 'N/A')[:100]}...")

def main():
    """Main execution function"""
    print("="*80)
    print("HISTORICAL DATA VECTORSTORE CREATION")
    print("="*80)
    
    try:
        # Step 1: Load Excel files
        df = load_excel_files('past_data')
        
        # Step 2: Extract relevant columns
        df_clean = extract_relevant_columns(df)
        
        # Step 3: Create vectorstore
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            print("\nUsing Sentence Transformers for embeddings...")
            db_data = create_vectorstore_sentence_transformers(df_clean, 'history_data.db')
        else:
            print("\nUsing TF-IDF for embeddings (fallback)...")
            db_data = create_vectorstore_tfidf(df_clean, 'history_data.db')
        
        # Step 4: Test the vectorstore
        test_vectorstore('history_data.db')
        
        print("\n" + "="*80)
        print("SUCCESS! Vectorstore created and tested successfully!")
        print("="*80)
        print(f"\nDatabase location: {os.path.abspath('history_data.db')}")
        print(f"Total records: {db_data['total_records']}")
        print(f"Model: {db_data['model_name']}")
        
        # Save summary
        summary = {
            "created_at": datetime.now().isoformat(),
            "database_path": os.path.abspath('history_data.db'),
            "model_name": db_data['model_name'],
            "total_records": db_data['total_records'],
            "columns": list(df_clean.columns),
            "source_files": len(list(Path('past_data').glob('*.xls*')))
        }
        
        with open('vectorstore_creation_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\nSummary saved to: vectorstore_creation_summary.json")
        
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
