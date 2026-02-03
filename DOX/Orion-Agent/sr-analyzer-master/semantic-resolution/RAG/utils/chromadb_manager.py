#!/usr/bin/env python3
"""
ChromaDB Manager
Unified interface for all ChromaDB operations
Replaces the old pickle-based vectorstores
"""
import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False

logger = logging.getLogger(__name__)

# Default paths - databases are now in data/
DEFAULT_CHROMADB_PATH = "data/vectorstore/chromadb_store"

# Collection names (mapped from old file names)
COLLECTION_NAMES = {
    'sr_history': 'clean_history_data',
    'code_search': 'comcast_code',
    'java_mapping': 'java_mapping',  # NEW - migrated from SQLite javaMapping.db
    'resolution_mapping': 'resolution_mapping'
    # Note: 'abbreviations' now in SQLite (abbreviation.db), not ChromaDB
}


class ChromaDBManager:
    """
    Unified ChromaDB manager for all vectorstore operations
    
    Usage:
        manager = ChromaDBManager()
        
        # Search SR history
        results = manager.search_sr_history("job failed batch processing", top_k=5)
        
        # Search code
        results = manager.search_code("Activity activation", top_k=10)
        
        # Add new SR
        manager.add_sr_entry(sr_id="CAS123", description="...", ...)
    """
    
    _instance = None
    _client = None
    _model = None
    
    def __new__(cls, chromadb_path: str = None):
        """Singleton pattern to reuse client"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, chromadb_path: str = None):
        """Initialize ChromaDB manager"""
        if not CHROMADB_AVAILABLE:
            raise ImportError("ChromaDB not installed. Run: pip install chromadb")
        
        # Use default path if not specified
        if chromadb_path is None:
            # Try to find the path relative to common locations
            possible_paths = [
                DEFAULT_CHROMADB_PATH,
                os.path.join(os.path.dirname(__file__), "..", "..", "data", "vectorstore", "chromadb_store"),
                os.path.join(os.path.dirname(__file__), "chromadb_store"),
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    chromadb_path = path
                    break
            
            if chromadb_path is None:
                chromadb_path = DEFAULT_CHROMADB_PATH
        
        self.chromadb_path = chromadb_path
        
        # Initialize client if not already done
        if ChromaDBManager._client is None:
            self._init_client()
        
        # Initialize embedding model if not already done
        if ChromaDBManager._model is None and SENTENCE_TRANSFORMERS_AVAILABLE:
            self._init_model()
    
    def _init_client(self):
        """Initialize ChromaDB client"""
        try:
            ChromaDBManager._client = chromadb.PersistentClient(path=self.chromadb_path)
            logger.info(f"ChromaDB client initialized at: {self.chromadb_path}")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            raise
    
    def _init_model(self):
        """Initialize embedding model"""
        from pathlib import Path
        try:
            # Try local model first for reliability
            local_model_path = Path(__file__).parent.parent.parent / "models" / "sentence-transformers_all-MiniLM-L6-v2"
            if local_model_path.exists():
                ChromaDBManager._model = SentenceTransformer(str(local_model_path))
                logger.info("Sentence Transformer model loaded from local")
            else:
                ChromaDBManager._model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("Sentence Transformer model loaded from HuggingFace")
        except Exception as e:
            logger.warning(f"Model load failed: {e}, trying fallback...")
            try:
                ChromaDBManager._model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("Model loaded (fallback)")
            except Exception as e2:
                logger.error(f"All model loading methods failed: {e2}")
    
    @property
    def client(self):
        """Get ChromaDB client"""
        return ChromaDBManager._client
    
    @property
    def model(self):
        """Get embedding model"""
        return ChromaDBManager._model
    
    def get_collection(self, name: str):
        """Get a collection by name"""
        try:
            return self.client.get_collection(name)
        except Exception as e:
            logger.error(f"Collection '{name}' not found: {e}")
            return None
    
    def list_collections(self) -> List[str]:
        """List all available collections"""
        collections = self.client.list_collections()
        return [col.name for col in collections]
    
    # =========================================================================
    # SR HISTORY OPERATIONS
    # =========================================================================
    
    def search_sr_history(
        self, 
        query: str, 
        top_k: int = 5,
        filter_dict: Dict = None
    ) -> List[Dict[str, Any]]:
        """
        Search SR history for similar cases
        
        Args:
            query: Search query text
            top_k: Number of results to return
            filter_dict: Optional metadata filters (e.g., {"priority": "P1"})
        
        Returns:
            List of matching SRs with metadata and similarity scores
        """
        collection = self.get_collection(COLLECTION_NAMES['sr_history'])
        if collection is None:
            logger.warning("SR history collection not found")
            return []
        
        try:
            # Generate query embedding
            if self.model:
                query_embedding = self.model.encode([query])[0].tolist()
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    where=filter_dict,
                    include=["documents", "metadatas", "distances"]
                )
            else:
                # Fallback to text-based query
                results = collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    where=filter_dict,
                    include=["documents", "metadatas", "distances"]
                )
            
            # Format results
            formatted = []
            if results and results['ids'] and len(results['ids']) > 0:
                for i, id_ in enumerate(results['ids'][0]):
                    result = {
                        'id': id_,
                        'document': results['documents'][0][i] if results['documents'] else '',
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else 0,
                        'similarity': 1 - (results['distances'][0][i] if results['distances'] else 0)
                    }
                    formatted.append(result)
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error searching SR history: {e}")
            return []
    
    def add_sr_entry(
        self,
        sr_id: str,
        description: str,
        priority: str = "",
        application: str = "",
        workaround: str = "",
        ai_workaround: str = "NA",
        user_corrected_workaround: str = "",
        **metadata
    ) -> bool:
        """
        Add or update an SR entry in the history.
        
        UPDATED: Uses call_id as the document ID and upserts to prevent duplicates.
        
        Args:
            sr_id: SR ID
            description: SR description (summary removed - was redundant)
            priority: Priority level
            application: Application name
            workaround: Workaround text
            ai_workaround: AI-generated workaround
            user_corrected_workaround: User-corrected workaround
            **metadata: Additional metadata fields
        
        Returns:
            bool: Success status
        """
        collection = self.get_collection(COLLECTION_NAMES['sr_history'])
        if collection is None:
            logger.error("SR history collection not found")
            return False
        
        try:
            sr_id_upper = sr_id.upper().strip()
            
            # Create document text (only description, summary removed as redundant)
            doc_text = description
            
            # Create metadata
            meta = {
                'call_id': sr_id_upper,
                'description': description[:500] if description else '',
                # 'summary' removed - was redundant
                'priority': str(priority),
                'application': str(application),
                'workaround': workaround[:1000] if workaround else '',
                'ai_generated_workaround': ai_workaround[:1000] if ai_workaround else 'NA',
                'user_corrected_workaround': user_corrected_workaround[:5000] if user_corrected_workaround else '',
                'added_date': datetime.now().isoformat(),
                **{k: str(v)[:500] for k, v in metadata.items() if v is not None}
            }
            
            # Use call_id as document ID (prevents duplicates)
            unique_id = sr_id_upper
            
            # Generate embedding and upsert
            if self.model:
                embedding = self.model.encode([doc_text])[0].tolist()
                collection.upsert(
                    ids=[unique_id],
                    embeddings=[embedding],
                    documents=[doc_text],
                    metadatas=[meta]
                )
            else:
                collection.upsert(
                    ids=[unique_id],
                    documents=[doc_text],
                    metadatas=[meta]
                )
            
            logger.info(f"Upserted SR {sr_id_upper} to history")
            return True
            
        except Exception as e:
            logger.error(f"Error adding/updating SR entry: {e}")
            return False
    
    def get_sr_by_id(self, sr_id: str) -> Optional[Dict]:
        """Get SR by ID (searches in metadata)"""
        collection = self.get_collection(COLLECTION_NAMES['sr_history'])
        if collection is None:
            return None
        
        try:
            results = collection.get(
                where={"call_id": sr_id},
                include=["documents", "metadatas"]
            )
            
            if results and results['ids']:
                return {
                    'id': results['ids'][0],
                    'document': results['documents'][0] if results['documents'] else '',
                    'metadata': results['metadatas'][0] if results['metadatas'] else {}
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting SR {sr_id}: {e}")
            return None
    
    # =========================================================================
    # CODE SEARCH OPERATIONS
    # =========================================================================
    
    def search_code(
        self, 
        query: str, 
        top_k: int = 10,
        filter_dict: Dict = None
    ) -> List[Dict[str, Any]]:
        """
        Search code chunks for relevant code
        
        Args:
            query: Search query (e.g., "Activity activation handler")
            top_k: Number of results
            filter_dict: Optional filters (e.g., {"module": "activation"})
        
        Returns:
            List of matching code chunks
        """
        collection = self.get_collection(COLLECTION_NAMES['code_search'])
        if collection is None:
            logger.warning("Code search collection not found")
            return []
        
        try:
            if self.model:
                query_embedding = self.model.encode([query])[0].tolist()
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    where=filter_dict,
                    include=["documents", "metadatas", "distances"]
                )
            else:
                results = collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    where=filter_dict,
                    include=["documents", "metadatas", "distances"]
                )
            
            formatted = []
            if results and results['ids'] and len(results['ids']) > 0:
                for i, id_ in enumerate(results['ids'][0]):
                    result = {
                        'id': id_,
                        'code': results['documents'][0][i] if results['documents'] else '',
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else 0,
                        'similarity': 1 - (results['distances'][0][i] if results['distances'] else 0)
                    }
                    formatted.append(result)
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error searching code: {e}")
            return []
    
    # =========================================================================
    # ABBREVIATION OPERATIONS (Now uses SQLite, not ChromaDB)
    # =========================================================================
    
    def search_abbreviations(
        self, 
        query: str, 
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search abbreviations from SQLite database (not ChromaDB).
        Abbreviations are now stored in SQLite for fast text-based lookups.
        
        Args:
            query: Search query (abbreviation or full form)
            top_k: Number of results
        
        Returns:
            List of matching abbreviations
        """
        import re
        import sqlite3
        
        # Find abbreviation.db path
        abbreviation_db = Path(self.chromadb_path).parent / "abbreviation.db"
        
        if not abbreviation_db.exists():
            logger.warning(f"abbreviation.db not found at {abbreviation_db}")
            return []
        
        try:
            conn = sqlite3.connect(abbreviation_db)
            cursor = conn.cursor()
            
            results = []
            seen = set()
            
            # 1. Extract uppercase words (potential abbreviations) from query
            words = set(re.findall(r'\b[A-Z]{2,6}\b', query.upper()))
            
            for word in words:
                cursor.execute("""
                    SELECT short_form, full_form, context FROM abbreviations 
                    WHERE short_form = ? LIMIT 1
                """, (word,))
                row = cursor.fetchone()
                if row and row[0] not in seen:
                    seen.add(row[0])
                    results.append({
                        'short_form': row[0],
                        'full_form': row[1],
                        'context': row[2] or '',
                        'similarity': 1.0  # Exact match
                    })
            
            # 2. Context/full form search if room for more
            if len(results) < top_k:
                search_terms = query.lower().split()[:5]
                if search_terms:
                    placeholders = " OR ".join(["full_form LIKE ? OR context LIKE ?"] * len(search_terms))
                    params = []
                    for term in search_terms:
                        params.extend([f'%{term}%', f'%{term}%'])
                    
                    cursor.execute(f"""
                        SELECT short_form, full_form, context FROM abbreviations 
                        WHERE {placeholders} LIMIT ?
                    """, (*params, top_k - len(results)))
                    
                    for row in cursor.fetchall():
                        if row[0] not in seen:
                            seen.add(row[0])
                            results.append({
                                'short_form': row[0],
                                'full_form': row[1],
                                'context': row[2] or '',
                                'similarity': 0.8  # Partial match
                            })
            
            conn.close()
            return results[:top_k]
            
        except Exception as e:
            logger.error(f"Error searching abbreviations: {e}")
            return []
    
    # =========================================================================
    # JAVA MAPPING OPERATIONS (NEW - migrated from SQLite)
    # =========================================================================
    
    def search_java_mapping(
        self, 
        query: str, 
        top_k: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search Java class mappings from ChromaDB.
        This was migrated from SQLite javaMapping.db for semantic search capability.
        
        Args:
            query: Search query (class name, package, or description)
            top_k: Number of results
        
        Returns:
            List of matching Java classes
        """
        collection = self.get_collection(COLLECTION_NAMES['java_mapping'])
        if collection is None:
            logger.warning("Java mapping collection not found")
            return []
        
        try:
            if self.model:
                query_embedding = self.model.encode([query])[0].tolist()
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    include=["documents", "metadatas", "distances"]
                )
            else:
                results = collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    include=["documents", "metadatas", "distances"]
                )
            
            formatted = []
            if results and results['ids'] and len(results['ids']) > 0:
                for i, id_ in enumerate(results['ids'][0]):
                    meta = results['metadatas'][0][i] if results['metadatas'] else {}
                    result = {
                        'id': id_,
                        'class_name': meta.get('class_name', ''),
                        'package': meta.get('package', ''),
                        'file_path': meta.get('file_path', ''),
                        'class_type': meta.get('class_type', ''),
                        'fqn': meta.get('full_qualified_name', ''),
                        'annotations': meta.get('annotations', ''),
                        'similarity': 1 - (results['distances'][0][i] if results['distances'] else 0)
                    }
                    formatted.append(result)
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error searching Java mapping: {e}")
            return []
    
    def get_java_class_by_name(self, class_name: str) -> Optional[Dict]:
        """Get Java class details by exact class name"""
        collection = self.get_collection(COLLECTION_NAMES['java_mapping'])
        if collection is None:
            return None
        
        try:
            results = collection.get(
                where={"class_name": class_name},
                include=["documents", "metadatas"]
            )
            
            if results and results['ids']:
                meta = results['metadatas'][0] if results['metadatas'] else {}
                return {
                    'id': results['ids'][0],
                    'class_name': meta.get('class_name', ''),
                    'package': meta.get('package', ''),
                    'file_path': meta.get('file_path', ''),
                    'class_type': meta.get('class_type', ''),
                    'fqn': meta.get('full_qualified_name', '')
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting Java class {class_name}: {e}")
            return None
    
    # =========================================================================
    # RESOLUTION MAPPING OPERATIONS
    # =========================================================================
    
    def search_resolution_mapping(
        self, 
        query: str, 
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search resolution mappings for workaround suggestions
        
        Args:
            query: Search query (resolution category or description)
            top_k: Number of results
        
        Returns:
            List of matching resolution mappings
        """
        collection = self.get_collection(COLLECTION_NAMES['resolution_mapping'])
        if collection is None:
            return []
        
        try:
            if self.model:
                query_embedding = self.model.encode([query])[0].tolist()
                results = collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    include=["documents", "metadatas", "distances"]
                )
            else:
                results = collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    include=["documents", "metadatas", "distances"]
                )
            
            formatted = []
            if results and results['ids'] and len(results['ids']) > 0:
                for i, id_ in enumerate(results['ids'][0]):
                    result = {
                        'id': id_,
                        'document': results['documents'][0][i] if results['documents'] else '',
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'similarity': 1 - (results['distances'][0][i] if results['distances'] else 0)
                    }
                    formatted.append(result)
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error searching resolution mapping: {e}")
            return []
    
    # =========================================================================
    # UTILITY METHODS
    # =========================================================================
    
    def get_collection_stats(self) -> Dict[str, int]:
        """Get record counts for all collections"""
        stats = {}
        for name in COLLECTION_NAMES.values():
            collection = self.get_collection(name)
            if collection:
                stats[name] = collection.count()
            else:
                stats[name] = 0
        return stats
    
    def health_check(self) -> Dict[str, Any]:
        """Check health of ChromaDB"""
        return {
            'chromadb_available': CHROMADB_AVAILABLE,
            'client_initialized': self.client is not None,
            'model_available': self.model is not None,
            'chromadb_path': self.chromadb_path,
            'collections': self.list_collections(),
            'stats': self.get_collection_stats()
        }


# Convenience function for quick access
def get_chromadb_manager(path: str = None) -> ChromaDBManager:
    """Get or create ChromaDB manager instance"""
    return ChromaDBManager(path)


# Test if run directly
if __name__ == '__main__':
    print("="*60)
    print("ChromaDB Manager Test")
    print("="*60)
    
    manager = ChromaDBManager()
    health = manager.health_check()
    
    print(f"\nHealth Check:")
    for key, value in health.items():
        print(f"  {key}: {value}")
    
    print("\nTest Search (SR History):")
    results = manager.search_sr_history("job failed batch processing", top_k=3)
    for i, r in enumerate(results):
        print(f"  [{i+1}] {r['metadata'].get('call_id', 'N/A')} (sim: {r['similarity']:.3f})")
    
    print("\nTest Search (Code):")
    results = manager.search_code("Activity activation", top_k=3)
    for i, r in enumerate(results):
        print(f"  [{i+1}] {r['metadata'].get('file_name', 'N/A')} (sim: {r['similarity']:.3f})")
    
    print("\nTest Search (Java Mapping):")
    results = manager.search_java_mapping("ValidateAddress", top_k=3)
    for i, r in enumerate(results):
        print(f"  [{i+1}] {r['class_name']} ({r['class_type']}) (sim: {r['similarity']:.3f})")
    
    print("\nTest Search (Abbreviations - SQLite):")
    results = manager.search_abbreviations("ALI ANI ACP", top_k=3)
    for i, r in enumerate(results):
        print(f"  [{i+1}] {r['short_form']} = {r['full_form']}")
    
    print("\n[OK] ChromaDB Manager working correctly!")

