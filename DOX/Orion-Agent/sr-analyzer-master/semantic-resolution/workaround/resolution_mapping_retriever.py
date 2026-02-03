#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resolution Mapping Vectorstore Loader
Loads and searches the resolution mapping vectorstore for RAG applications.
Now uses ChromaDB as primary storage with pickle fallback.
"""

import sys
import os
import pickle
import sqlite3
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

logger = logging.getLogger(__name__)

# Import ChromaDB
try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logger.warning("ChromaDB not available, using pickle fallback")

# Import sentence transformers
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning("sentence-transformers not available")

# FAISS removed - using ChromaDB as primary storage with numpy-based fallback


class ResolutionMappingRetriever:
    """
    Loads and queries the resolution mapping vectorstore for RAG applications.
    Now uses ChromaDB as primary storage with pickle fallback.
    """
    
    def __init__(self, vectorstore_dir: str = "data/vectorstore"):
        """
        Initialize the retriever
        
        Args:
            vectorstore_dir: Directory containing vectorstore files
        """
        self.vectorstore_dir = Path(vectorstore_dir)
        self.model = None
        self.embeddings = None
        self.data = None
        self.index = None
        self.metadata = None
        self.use_chromadb = False
        self.chromadb_client = None
        self.collection = None
        
        self._load_vectorstore()
    
    def _load_vectorstore(self):
        """Load from ChromaDB (primary) or pickle file (fallback)"""
        
        # Try ChromaDB first
        chromadb_path = self.vectorstore_dir / "chromadb_store"
        if CHROMADB_AVAILABLE and chromadb_path.exists():
            try:
                self.chromadb_client = chromadb.PersistentClient(path=str(chromadb_path))
                self.collection = self.chromadb_client.get_collection("resolution_mapping")
                self.use_chromadb = True
                
                # Load model for queries
                if SENTENCE_TRANSFORMERS_AVAILABLE:
                    # Load without device parameter to avoid meta tensor error
                    self.model = SentenceTransformer('all-MiniLM-L6-v2')
                
                count = self.collection.count()
                self.metadata = {
                    'num_records': count,
                    'embedding_model': 'all-MiniLM-L6-v2',
                    'storage': 'ChromaDB',
                    'collection': 'resolution_mapping'
                }
                
                logger.info(f"Loaded resolution_mapping from ChromaDB: {count} records")
                return
                
            except Exception as e:
                logger.warning(f"ChromaDB load failed: {e}, falling back to pickle")
                self.use_chromadb = False
        
        # Fallback to pickle file
        try:
            db_path = self.vectorstore_dir / "resolution_mapping.db"
            
            if not db_path.exists():
                raise FileNotFoundError(f"Vectorstore not found at {db_path}")
            
            logger.info(f"Loading vectorstore from pickle: {db_path}")
            
            with open(db_path, 'rb') as f:
                db_data = pickle.load(f)
            
            # Extract components
            self.embeddings = db_data['embeddings']
            self.data = db_data['metadata']  # This is a DataFrame
            self.metadata = {
                'num_records': db_data['num_records'],
                'embedding_model': db_data['model_name'],
                'embedding_dimension': db_data['embedding_dimension'],
                'columns': db_data['columns'],
                'created_at': db_data.get('created_at', 'unknown'),
                'excel_file': db_data.get('excel_file', 'unknown'),
                'storage': 'pickle'
            }
            
            logger.info(f"Loaded {len(self.data)} records with {self.embeddings.shape[1]}-dim embeddings")
            
            # Load sentence transformer model
            if SENTENCE_TRANSFORMERS_AVAILABLE:
                model_name = db_data.get('model_name', 'all-MiniLM-L6-v2')
                # Load model then move to CPU (avoids meta tensor error)
                self.model = SentenceTransformer(model_name)
                self.model = self.model.cpu()
                logger.info(f"Loaded model: {model_name}")
            else:
                raise ImportError("sentence-transformers required for retrieval")
            
            self.index = None
                
        except Exception as e:
            logger.error(f"Error loading vectorstore: {e}")
            raise
    
    def search(self, query: str, top_k: int = 5, similarity_threshold: float = 0.0) -> List[Dict[str, Any]]:
        """
        Search the vectorstore for similar resolution mappings.
        Uses ChromaDB if available, otherwise falls back to numpy search.
        
        Args:
            query: Search query text
            top_k: Number of results to return
            similarity_threshold: Minimum similarity score (0-1)
            
        Returns:
            List of dictionaries containing search results
        """
        # Use ChromaDB if available
        if self.use_chromadb and self.collection:
            try:
                query_embedding = self.model.encode([query])[0].tolist()
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    include=["documents", "metadatas", "distances"]
                )
                
                formatted = []
                if results and results['ids'] and len(results['ids']) > 0:
                    for i, id_ in enumerate(results['ids'][0]):
                        distance = results['distances'][0][i] if results['distances'] else 0
                        similarity = 1 - distance
                        if similarity >= similarity_threshold:
                            formatted.append({
                                'index': i,
                                'similarity': similarity,
                                'data': results['metadatas'][0][i] if results['metadatas'] else {}
                            })
                return formatted
                
            except Exception as e:
                logger.error(f"ChromaDB search failed: {e}")
                # Fall through to numpy search if ChromaDB fails
        
        # Fallback to numpy search
        if self.model is None or self.embeddings is None or self.data is None:
            raise RuntimeError("Vectorstore not loaded")
        
        # Create query embedding
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        
        # Use numpy for search
        embeddings_normalized = self.embeddings / np.linalg.norm(
            self.embeddings, axis=1, keepdims=True
        )
        query_normalized = query_embedding / np.linalg.norm(query_embedding)
        
        # Compute similarities
        similarities = np.dot(embeddings_normalized, query_normalized.T).flatten()
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = []
        for idx in top_indices:
            similarity = float(similarities[idx])
            if similarity >= similarity_threshold:
                results.append({
                    'index': int(idx),
                    'similarity': similarity,
                    'data': self.data.iloc[idx].to_dict()
                })
        
        return results
    
    def search_with_context(self, query: str, top_k: int = 3) -> str:
        """
        Search and return results formatted as context for RAG
        
        Args:
            query: Search query text
            top_k: Number of results to return
            
        Returns:
            Formatted string with search results
        """
        results = self.search(query, top_k)
        
        if not results:
            return "No relevant resolution mappings found."
        
        context_parts = [f"Found {len(results)} relevant resolution mappings:\n"]
        
        for i, result in enumerate(results, 1):
            context_parts.append(f"\n{i}. (Similarity: {result['similarity']:.2f})")
            for key, value in result['data'].items():
                if value is not None and str(value).strip():
                    context_parts.append(f"   {key}: {value}")
        
        return "\n".join(context_parts)
    
    def get_by_index(self, index: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific record by index
        
        Args:
            index: Record index
            
        Returns:
            Dictionary containing the record data
        """
        if 0 <= index < len(self.data):
            return self.data.iloc[index].to_dict()
        return None
    
    def get_all_data(self):
        """Get the entire dataset as a pandas DataFrame"""
        return self.data
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the vectorstore"""
        if self.use_chromadb and self.collection:
            return {
                'num_records': self.collection.count(),
                'embedding_dimension': 384,  # all-MiniLM-L6-v2
                'storage_format': 'ChromaDB (resolution_mapping collection)',
                'metadata': self.metadata
            }
        return {
            'num_records': len(self.data) if self.data is not None else 0,
            'embedding_dimension': self.embeddings.shape[1] if self.embeddings is not None else 0,
            'columns': list(self.data.columns) if self.data is not None else [],
            'storage_format': 'Pickle file (legacy)',
            'metadata': self.metadata
        }


# Example usage and testing
def test_retriever():
    """Test the retriever with sample queries"""
    print("=" * 70)
    print("Testing Resolution Mapping Retriever")
    print("=" * 70)
    
    try:
        # Initialize retriever
        retriever = ResolutionMappingRetriever()
        
        # Print stats
        stats = retriever.get_stats()
        print(f"\n📊 Vectorstore Stats:")
        print(f"  Records: {stats['num_records']}")
        print(f"  Embedding dimension: {stats['embedding_dimension']}")
        print(f"  Columns: {', '.join(stats['columns'])}")
        print(f"  Storage: {stats['storage_format']}")
        
        # Test queries
        test_queries = [
            "network connectivity issue",
            "database connection error",
            "authentication problem"
        ]
        
        for query in test_queries:
            print("\n" + "=" * 70)
            print(f"Query: {query}")
            print("-" * 70)
            
            results = retriever.search(query, top_k=3)
            
            for i, result in enumerate(results, 1):
                print(f"\n{i}. Similarity: {result['similarity']:.4f}")
                print(f"   Data: {result['data']}")
            
            # Test context format
            print("\n📝 RAG Context Format:")
            print("-" * 70)
            context = retriever.search_with_context(query, top_k=2)
            print(context)
        
        print("\n" + "=" * 70)
        print("✓ Testing complete!")
        print("=" * 70)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_retriever()

