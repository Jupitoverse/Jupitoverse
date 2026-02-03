#!/usr/bin/env python3
"""
History Database Manager
Manages ChromaDB vectorstore for SR history data
ChromaDB-only mode - no pickle fallback

UPDATED: 
- Fixed duplicate entries issue - now updates existing records instead of creating new ones
- User workarounds stored as JSON array to support multiple users
- Columns no longer used (kept for backward compatibility): corrected_by, feedback_date
  These are now stored inside the JSON in user_corrected_workaround field
"""

import logging
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Setup logger
logger = logging.getLogger(__name__)

# Try to import ChromaDB
try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    logger.error("ChromaDB not available - pip install chromadb")

# Fix for meta tensor error with accelerate library
# Must be set BEFORE importing sentence_transformers
import os
os.environ['ACCELERATE_TORCH_DEVICE'] = 'cpu'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['ACCELERATE_DISABLE_RICH'] = '1'

# Try to import sentence transformers
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning("sentence-transformers not available - limited functionality")

# 🆕 Try to import SR text preprocessor
try:
    from analyzers.sr_text_preprocessor import SRTextPreprocessor
    PREPROCESSOR_AVAILABLE = True
except ImportError:
    PREPROCESSOR_AVAILABLE = False


class HistoryDatabaseManager:
    """
    Manages ChromaDB vectorstore for SR history with support for:
    - Semantic search using sentence transformers
    - Adding/updating SR entries
    - User feedback integration
    """
    
    def __init__(self, db_path: str = None, chromadb_path: str = None):
        """
        Initialize the history database manager
        
        Args:
            db_path: Legacy parameter (ignored, kept for backward compatibility)
            chromadb_path: Path to ChromaDB store directory
        """
        self.db_data = None  # Legacy compatibility
        self.model = None
        self.model_name = 'all-MiniLM-L6-v2'
        self.preprocessor = SRTextPreprocessor() if PREPROCESSOR_AVAILABLE else None
        
        # ChromaDB support
        self.chromadb_client = None
        self.chromadb_collection = None
        self.use_chromadb = False
        
        # Determine ChromaDB path
        if chromadb_path:
            self.chromadb_path = Path(chromadb_path)
        else:
            # Default: data/vectorstore/chromadb_store
            base_dir = Path(__file__).parent.parent.parent
            self.chromadb_path = base_dir / "data" / "vectorstore" / "chromadb_store"
        
        # Initialize ChromaDB
        if CHROMADB_AVAILABLE and self.chromadb_path.exists():
            try:
                # Use basic PersistentClient without Settings to avoid "different settings" error
                self.chromadb_client = chromadb.PersistentClient(path=str(self.chromadb_path))
                self.chromadb_collection = self.chromadb_client.get_collection('clean_history_data')
                self.use_chromadb = True
                logger.info(f"[OK] ChromaDB initialized (records: {self.chromadb_collection.count()})")
                self._load_model()
            except Exception as e:
                logger.error(f"ChromaDB init failed: {e}")
                self.use_chromadb = False
        else:
            if not CHROMADB_AVAILABLE:
                logger.error("ChromaDB not installed")
            else:
                logger.error(f"ChromaDB store not found at {self.chromadb_path}")
    
    def _load_model(self):
        """Load the sentence transformer model"""
        if not SENTENCE_TRANSFORMERS_AVAILABLE:
            return
        
        try:
            # Method 1: Direct CPU loading (works if accelerate env vars are set)
            self.model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
            self.model_name = 'all-MiniLM-L6-v2'
            logger.info("[OK] Model loaded")
        except (NotImplementedError, RuntimeError) as e:
            # Method 2: Fallback - load without device, then set target device
            try:
                logger.info("Trying fallback model loading...")
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
                self.model._target_device = 'cpu'
                self.model_name = 'all-MiniLM-L6-v2'
                logger.info("[OK] Model loaded (fallback)")
            except Exception as e2:
                logger.warning(f"Model load failed: {e2}")
                self.model = None
        except Exception as e:
            logger.warning(f"Model load failed: {e}")
            self.model = None
    
    def load_database(self) -> bool:
        """Load the history database"""
        try:
            logger.info(f"Loading history database from {self.db_path}...")
            with open(self.db_path, 'rb') as f:
                self.db_data = pickle.load(f)
            
            self.model_name = self.db_data.get('model_name', 'unknown')
            logger.info(f"✅ Database loaded successfully!")
            logger.info(f"   Model: {self.model_name}")
            logger.info(f"   Total records: {self.db_data.get('total_records', 0)}")
            logger.info(f"   Columns: {self.db_data.get('columns', [])}")
            
            # Load the sentence transformer model if available
            if SENTENCE_TRANSFORMERS_AVAILABLE and self.model_name == 'all-MiniLM-L6-v2':
                logger.info("Loading Sentence Transformer model...")
                try:
                    # Load model with device='cpu' to avoid meta tensor error
                    self.model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
                    logger.info("✅ Model loaded successfully!")
                except Exception as model_error:
                    logger.warning(f"⚠️ Could not load model: {str(model_error)}")
                    logger.warning("⚠️ Continuing without model - embeddings won't be updated")
                    self.model = None
            
            return True
        except Exception as e:
            logger.error(f"❌ Error loading database: {str(e)}")
            return False
    
    def save_database(self) -> bool:
        """Save the history database"""
        try:
            logger.info(f"Saving history database to {self.db_path}...")
            
            # Update metadata
            if self.db_data:
                self.db_data['last_updated'] = datetime.now().isoformat()
                self.db_data['total_records'] = len(self.db_data.get('metadata', []))
            
            # Save to pickle
            with open(self.db_path, 'wb') as f:
                pickle.dump(self.db_data, f, protocol=pickle.HIGHEST_PROTOCOL)
            
            logger.info(f"✅ Database saved successfully!")
            return True
        except Exception as e:
            logger.error(f"❌ Error saving database: {str(e)}")
            return False
    
    def _append_user_workaround(self, existing_wa_json: str, new_wa: str, user: str) -> str:
        """
        Append new user workaround to JSON history array.
        
        Format: [{"user": "email", "wa": "workaround text", "date": "ISO timestamp"}, ...]
        
        Args:
            existing_wa_json: Existing JSON string or plain text workaround
            new_wa: New workaround text to append
            user: User who provided the workaround
        
        Returns:
            Updated JSON string with new workaround appended
        """
        # Get existing history or create new
        try:
            history = json.loads(existing_wa_json) if existing_wa_json else []
            if not isinstance(history, list):
                # Old format was plain text, convert to list
                history = [{'user': 'legacy', 'wa': str(existing_wa_json), 'date': 'legacy'}]
        except json.JSONDecodeError:
            # Old format was plain text
            if existing_wa_json and str(existing_wa_json).strip():
                history = [{'user': 'legacy', 'wa': str(existing_wa_json), 'date': 'legacy'}]
            else:
                history = []
        
        # Append new entry
        history.append({
            'user': str(user) if user else 'user',
            'wa': str(new_wa),
            'date': datetime.now().isoformat()
        })
        
        return json.dumps(history)
    
    def _get_latest_user_workaround(self, wa_json: str) -> Dict[str, str]:
        """
        Get the latest user workaround from JSON array.
        
        Returns:
            Dict with 'user', 'wa', 'date' keys, or empty dict if none
        """
        try:
            history = json.loads(wa_json) if wa_json else []
            if isinstance(history, list) and len(history) > 0:
                return history[-1]  # Return latest entry
        except json.JSONDecodeError:
            # Plain text format - return as-is
            if wa_json and str(wa_json).strip():
                return {'user': 'unknown', 'wa': str(wa_json), 'date': ''}
        return {}
    
    def add_user_feedback_entry(
        self,
        sr_id: str,
        description: str = "",
        notes: str = "",
        user_corrected_workaround: str = "",
        ai_generated_workaround: str = "NA",
        priority: str = "User Feedback",
        **additional_fields
    ) -> bool:
        """
        Add or update an entry in the history database.
        
        UPDATED BEHAVIOR:
        - If SR exists: UPDATE the existing record (prevents duplicates)
        - If SR doesn't exist: ADD new record
        - User workarounds are stored as JSON array (supports multiple users)
        
        Args:
            sr_id: Service Request ID
            description: SR description
            notes: SR notes (used for better matching)
            user_corrected_workaround: User's corrected workaround (will be appended to history)
            ai_generated_workaround: AI-generated workaround (default "NA")
            priority: Priority level (default "User Feedback")
            additional_fields: Any additional metadata fields
        
        Returns:
            bool: Success status
        """
        # Use ChromaDB if available
        if self.use_chromadb and self.chromadb_collection and self.model:
            try:
                sr_id_upper = str(sr_id).upper().strip()
                
                # Ensure all inputs are strings
                description_str = str(description) if description else ''
                notes_str = str(notes) if notes else ''
                ai_wa_str = str(ai_generated_workaround) if ai_generated_workaround else 'NA'
                user_wa_str = str(user_corrected_workaround) if user_corrected_workaround else ''
                
                # Determine if this is user feedback
                is_user_feedback = bool(user_wa_str) or 'corrected_by' in additional_fields
                corrected_by = str(additional_fields.get('corrected_by', 'user'))
                
                # CHECK IF SR ALREADY EXISTS
                existing_results = self.chromadb_collection.get(
                    where={"call_id": sr_id_upper},
                    include=['metadatas', 'documents']
                )
                
                if existing_results and existing_results['ids']:
                    # ===== RECORD EXISTS - UPDATE IT =====
                    record_id = existing_results['ids'][0]
                    existing_metadata = existing_results['metadatas'][0].copy()
                    old_doc = existing_results['documents'][0] if existing_results['documents'] else ''
                    
                    logger.info(f"[UPDATE] SR {sr_id_upper} exists - updating instead of creating duplicate")
                    
                    # Update description/notes only if provided and not empty
                    if description_str:
                        existing_metadata['description'] = description_str[:500]
                    # 'summary' field removed - was redundant
                    if notes_str:
                        existing_metadata['wl_summary'] = notes_str[:500]
                    
                    # Update priority if meaningful
                    if priority and priority != "User Feedback":
                        existing_metadata['priority'] = str(priority)
                    
                    # Update AI workaround only if provided and not 'NA'
                    if ai_wa_str and ai_wa_str not in ['NA', 'N/A', '']:
                        existing_metadata['ai_generated_workaround'] = ai_wa_str[:1000]
                    
                    # Handle user workaround - APPEND to JSON history
                    if is_user_feedback and user_wa_str:
                        existing_wa = existing_metadata.get('user_corrected_workaround', '')
                        updated_wa_json = self._append_user_workaround(existing_wa, user_wa_str, corrected_by)
                        existing_metadata['user_corrected_workaround'] = updated_wa_json[:5000]  # Increased limit for JSON
                        logger.info(f"   [APPEND] Added user workaround from {corrected_by}")
                    
                    # Update other fields from additional_fields
                    field_mapping = {
                        'workaround': 'workaround',
                        'application': 'application',
                        'resolution_categorization': 'resolution_categorization',
                        'function_category': 'function_category',
                        'status': 'status',
                        'assigned_to': 'assigned_to',
                        'resolution': 'resolution',
                        'sla_resolution_categorization_t1': 'sla_resolution_categorization_t1',
                        'sla_resolution_category': 'sla_resolution_category',
                        'reported_date': 'Reported Date'
                    }
                    
                    for src_field, dst_field in field_mapping.items():
                        if src_field in additional_fields:
                            val = additional_fields[src_field]
                            if val and str(val).strip() not in ['', 'NA', 'N/A', 'None', 'nan', 'Unknown']:
                                existing_metadata[dst_field] = str(val)[:500]
                    
                    existing_metadata['last_updated'] = datetime.now().isoformat()
                    existing_metadata['source'] = 'user_feedback' if is_user_feedback else 'admin_upload'
                    
                    # Update added_date for admin uploads so SR appears in today's dashboard
                    if not is_user_feedback:
                        existing_metadata['added_date'] = datetime.now().strftime('%Y-%m-%d')
                    
                    # Keep legacy columns populated for backward compatibility (but not used)
                    # These are now redundant - data is in the JSON user_corrected_workaround
                    existing_metadata['corrected_by'] = corrected_by if is_user_feedback else existing_metadata.get('corrected_by', '')
                    existing_metadata['feedback_date'] = datetime.now().isoformat() if is_user_feedback else existing_metadata.get('feedback_date', '')
                    
                    # Re-encode document (only description, summary removed as redundant)
                    doc_text = existing_metadata.get('description', '')
                    new_embedding = self.model.encode([doc_text])[0].tolist()
                    
                    # Delete old and add updated (ChromaDB update pattern)
                    self.chromadb_collection.delete(ids=[record_id])
                    self.chromadb_collection.add(
                        ids=[record_id],  # Keep same ID
                        embeddings=[new_embedding],
                        documents=[doc_text],
                        metadatas=[existing_metadata]
                    )
                    
                    logger.info(f"[OK] Updated SR {sr_id_upper} in ChromaDB (user_feedback: {is_user_feedback})")
                    return True
                    
                else:
                    # ===== RECORD DOESN'T EXIST - ADD NEW =====
                    logger.info(f"[ADD] SR {sr_id_upper} is new - adding to ChromaDB")
                    
                    doc_text = f"{description_str} {notes_str}"
                    embedding = self.model.encode([doc_text])[0].tolist()
                    
                    # Build initial user workaround as JSON if provided
                    user_wa_json = ''
                    if is_user_feedback and user_wa_str:
                        user_wa_json = json.dumps([{
                            'user': corrected_by,
                            'wa': user_wa_str,
                            'date': datetime.now().isoformat()
                        }])
                    
                    metadata = {
                        'call_id': sr_id_upper,
                        'priority': str(priority) if priority != "User Feedback" else 'P3',
                        'description': description_str[:500],
                        # 'summary' removed - was redundant (just prefix of description)
                        'wl_summary': (notes_str if notes_str else '')[:500],
                        'workaround': str(additional_fields.get('workaround', ''))[:1000],
                        'ai_generated_workaround': ai_wa_str[:1000],
                        'user_corrected_workaround': user_wa_json[:5000],  # JSON format
                        'application': str(additional_fields.get('application', 'Unknown')),
                        'resolution_categorization': str(additional_fields.get('resolution_categorization', '')),
                        'function_category': str(additional_fields.get('function_category', '')),
                        'status': str(additional_fields.get('status', '')),
                        'assigned_to': str(additional_fields.get('assigned_to', '')),
                        'added_date': datetime.now().isoformat(),
                        'source': 'user_feedback' if is_user_feedback else 'admin_upload',
                        # Legacy columns - kept for backward compatibility but not used
                        'corrected_by': corrected_by if is_user_feedback else '',
                        'feedback_date': datetime.now().isoformat() if is_user_feedback else ''
                    }
                    
                    # Use call_id as the document ID (no timestamp suffix)
                    unique_id = sr_id_upper
                    
                    self.chromadb_collection.add(
                        ids=[unique_id],
                        embeddings=[embedding],
                        documents=[doc_text],
                        metadatas=[metadata]
                    )
                    
                    logger.info(f"[OK] Added new SR {sr_id_upper} to ChromaDB")
                    return True
                
            except Exception as e:
                logger.error(f"ChromaDB add/update error: {e}")
                import traceback
                logger.error(f"Traceback: {traceback.format_exc()}")
                return False
        
        # Fallback to pickle
        try:
            if not self.db_data:
                logger.error("No database loaded!")
                return False
            
            # Check if entry already exists
            existing_index = self._find_entry_by_sr_id(sr_id)
            
            # Create metadata entry
            metadata = {
                'call_id': sr_id,
                'priority': priority,
                'description': description,
                # 'summary' removed - was redundant
                'wl_summary': notes if notes else '',
                'resolution_categorization': additional_fields.get('resolution_categorization', ''),
                'resolution_categorization_tier3': additional_fields.get('resolution_categorization_tier3', ''),
                'sla_resolution_categorization_t1': additional_fields.get('sla_resolution_categorization_t1', ''),
                'sla_resolution_category': additional_fields.get('sla_resolution_category', ''),
                'workaround': additional_fields.get('workaround', ''),
                'ai_generated_workaround': ai_generated_workaround,
                'user_corrected_workaround': user_corrected_workaround,
                'feedback_date': datetime.now().isoformat(),
                'source': 'admin_upload',
                'status': additional_fields.get('status', 'Resolved'),
                'application': additional_fields.get('application', 'Unknown'),
                'assigned_to': additional_fields.get('assigned_to', 'Not Assigned'),
                'Reported Date': additional_fields.get('reported_date', None)  # 🆕 For age calculation
            }
            
            # Create searchable document
            searchable_text = self._create_searchable_text(metadata)
            
            # Generate embedding
            if self.model and SENTENCE_TRANSFORMERS_AVAILABLE:
                embedding = self.model.encode([searchable_text])[0]
            else:
                logger.warning("No model available for embedding generation")
                return False
            
            if existing_index is not None:
                # Update existing entry - PRESERVE EXISTING DATA!
                logger.info(f"Updating existing entry for SR {sr_id} at index {existing_index}")
                
                # Get existing metadata to preserve fields
                existing_metadata = self.db_data['metadata'][existing_index]
                
                # 🔒 PRESERVE ai_generated_workaround if new one is 'NA' but old one exists
                if metadata['ai_generated_workaround'] == 'NA':
                    old_ai_wa = existing_metadata.get('ai_generated_workaround', '')
                    if old_ai_wa and old_ai_wa not in ['NA', 'N/A', '', 'None', 'nan']:
                        metadata['ai_generated_workaround'] = old_ai_wa
                        logger.info(f"   🔒 Preserved existing AI workaround (not overwritten)")
                
                # 🔒 PRESERVE other important fields if not provided in new metadata
                preserve_fields = [
                    'resolution_categorization', 
                    'sla_resolution_categorization_t1',
                    'workaround',
                    'status',
                    'application',
                    'assigned_to'
                ]
                
                for field in preserve_fields:
                    # If new value is empty/NA and old value exists, preserve old value
                    new_val = metadata.get(field, '')
                    old_val = existing_metadata.get(field, '')
                    
                    if not new_val or str(new_val).strip() in ['', 'NA', 'N/A', 'None', 'nan', 'Unknown']:
                        if old_val and str(old_val).strip() not in ['', 'NA', 'N/A', 'None', 'nan', 'Unknown']:
                            metadata[field] = old_val
                
                # Update the entry
                self.db_data['metadata'][existing_index] = metadata
                self.db_data['documents'][existing_index] = searchable_text
                self.db_data['embeddings'][existing_index] = embedding
                
                logger.info(f"   ✅ Updated entry (preserved existing AI workaround and other fields)")
            else:
                # Add new entry
                logger.info(f"Adding new entry for SR {sr_id}")
                self.db_data['metadata'].append(metadata)
                self.db_data['documents'].append(searchable_text)
                
                # Append to embeddings array
                if isinstance(self.db_data['embeddings'], np.ndarray):
                    self.db_data['embeddings'] = np.vstack([
                        self.db_data['embeddings'],
                        embedding.reshape(1, -1)
                    ])
                else:
                    logger.error("Embeddings array format not supported")
                    return False
            
            # Save database
            self.save_database()
            
            logger.info(f"✅ Successfully added/updated entry for SR {sr_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error adding user feedback entry: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def update_workaround(self, sr_id: str, user_corrected_workaround: str) -> bool:
        """
        Update the user_corrected_workaround field for an existing entry
        
        Args:
            sr_id: Service Request ID
            user_corrected_workaround: New user-corrected workaround
        
        Returns:
            bool: Success status
        """
        # Use ChromaDB if available
        if self.use_chromadb and self.chromadb_collection:
            try:
                sr_id_upper = sr_id.upper().strip()
                # Find existing record
                results = self.chromadb_collection.get(
                    where={"call_id": sr_id_upper},
                    include=['metadatas', 'documents', 'embeddings']
                )
                
                if results and results['ids']:
                    record_id = results['ids'][0]
                    old_metadata = results['metadatas'][0]
                    old_doc = results['documents'][0] if results['documents'] else ''
                    
                    # Update metadata
                    old_metadata['user_corrected_workaround'] = str(user_corrected_workaround)[:1000]
                    old_metadata['last_updated'] = datetime.now().isoformat()
                    
                    # Re-encode if model available
                    new_embedding = None
                    if self.model:
                        new_embedding = self.model.encode([old_doc])[0].tolist()
                    
                    # Delete and re-add (ChromaDB doesn't support direct metadata update)
                    self.chromadb_collection.delete(ids=[record_id])
                    self.chromadb_collection.add(
                        ids=[record_id],
                        embeddings=[new_embedding] if new_embedding else None,
                        documents=[old_doc],
                        metadatas=[old_metadata]
                    )
                    
                    logger.info(f"✅ Successfully updated workaround for SR {sr_id} in ChromaDB")
                    return True
                else:
                    logger.warning(f"SR {sr_id} not found in ChromaDB")
                    return False
                    
            except Exception as e:
                logger.error(f"ChromaDB update error: {e}")
                return False
        
        # Fallback to pickle
        try:
            if not self.db_data:
                logger.error("No database loaded!")
                return False
            
            # Find the entry
            index = self._find_entry_by_sr_id(sr_id)
            
            if index is not None:
                # Update the workaround field
                self.db_data['metadata'][index]['user_corrected_workaround'] = user_corrected_workaround
                self.db_data['metadata'][index]['last_updated'] = datetime.now().isoformat()
                
                # Update searchable text and embedding
                searchable_text = self._create_searchable_text(self.db_data['metadata'][index])
                self.db_data['documents'][index] = searchable_text
                
                if self.model and SENTENCE_TRANSFORMERS_AVAILABLE:
                    embedding = self.model.encode([searchable_text])[0]
                    self.db_data['embeddings'][index] = embedding
                
                # Save database
                self.save_database()
                
                logger.info(f"✅ Successfully updated workaround for SR {sr_id}")
                return True
            else:
                logger.warning(f"SR {sr_id} not found in database")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error updating workaround: {str(e)}")
            return False
    
    def update_ai_workaround(self, sr_id: str, new_ai_workaround: str) -> bool:
        """
        Update the ai_generated_workaround field for an existing entry
        This is called when user approves a regenerated AI workaround
        
        Args:
            sr_id: Service Request ID
            new_ai_workaround: New approved AI-generated workaround
        
        Returns:
            bool: Success status
        """
        # Use ChromaDB if available
        if self.use_chromadb and self.chromadb_collection:
            try:
                sr_id_upper = sr_id.upper().strip()
                # Find existing record
                results = self.chromadb_collection.get(
                    where={"call_id": sr_id_upper},
                    include=['metadatas', 'documents', 'embeddings']
                )
                
                if results and results['ids']:
                    record_id = results['ids'][0]
                    old_metadata = results['metadatas'][0]
                    old_doc = results['documents'][0] if results['documents'] else ''
                    old_workaround = old_metadata.get('ai_generated_workaround', 'NA')
                    
                    # Update metadata
                    old_metadata['ai_generated_workaround'] = str(new_ai_workaround)[:1000]
                    old_metadata['ai_workaround_updated'] = datetime.now().isoformat()
                    old_metadata['ai_workaround_previous'] = str(old_workaround)[:500]
                    
                    # Re-encode if model available
                    new_embedding = None
                    if self.model:
                        new_embedding = self.model.encode([old_doc])[0].tolist()
                    
                    # Delete and re-add (ChromaDB doesn't support direct metadata update)
                    self.chromadb_collection.delete(ids=[record_id])
                    self.chromadb_collection.add(
                        ids=[record_id],
                        embeddings=[new_embedding] if new_embedding else None,
                        documents=[old_doc],
                        metadatas=[old_metadata]
                    )
                    
                    logger.info(f"✅ Successfully updated AI workaround for SR {sr_id} in ChromaDB")
                    logger.info(f"   Old: {str(old_workaround)[:50]}...")
                    logger.info(f"   New: {new_ai_workaround[:50]}...")
                    return True
                else:
                    logger.warning(f"SR {sr_id} not found in ChromaDB")
                    return False
                    
            except Exception as e:
                logger.error(f"ChromaDB update error: {e}")
                return False
        
        # Fallback to pickle
        try:
            if not self.db_data:
                logger.error("No database loaded!")
                return False
            
            # Find the entry
            index = self._find_entry_by_sr_id(sr_id)
            
            if index is not None:
                # Update the AI workaround field
                old_workaround = self.db_data['metadata'][index].get('ai_generated_workaround', 'NA')
                self.db_data['metadata'][index]['ai_generated_workaround'] = new_ai_workaround
                self.db_data['metadata'][index]['ai_workaround_updated'] = datetime.now().isoformat()
                self.db_data['metadata'][index]['ai_workaround_previous'] = old_workaround  # Keep history
                
                # Update searchable text and embedding
                searchable_text = self._create_searchable_text(self.db_data['metadata'][index])
                self.db_data['documents'][index] = searchable_text
                
                if self.model and SENTENCE_TRANSFORMERS_AVAILABLE:
                    embedding = self.model.encode([searchable_text])[0]
                    self.db_data['embeddings'][index] = embedding
                
                # Save database
                self.save_database()
                
                logger.info(f"✅ Successfully updated AI workaround for SR {sr_id}")
                logger.info(f"   Old: {old_workaround[:50]}...")
                logger.info(f"   New: {new_ai_workaround[:50]}...")
                return True
            else:
                logger.warning(f"SR {sr_id} not found in database")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error updating AI workaround: {str(e)}")
            return False
    
    def update_sr_from_admin(
        self,
        sr_id: str,
        ai_generated_workaround: str = None,
        description: str = None,
        notes: str = None,
        priority: str = None,
        function_category: str = None,
        resolution_categorization: str = None,
        sla_resolution_categorization_t1: str = None,
        sla_resolution_category: str = None,
        resolution: str = None,
        workaround: str = None,
        status: str = None,
        application: str = None,
        preserve_user_feedback: bool = True,
        **additional_fields
    ) -> bool:
        """
        Update existing SR with new data from admin upload (RAG pipeline)
        
        IMPORTANT: Preserves user_corrected_workaround if preserve_user_feedback=True
        
        This method is used when:
        - Admin re-uploads an existing SR with new RAG analysis
        - We want to update AI workaround and other fields
        - But preserve any user corrections/feedback
        
        Args:
            sr_id: SR ID to update
            ai_generated_workaround: New AI workaround from RAG
            description: Updated description
            notes: Updated notes/summary
            preserve_user_feedback: If True, don't overwrite user_corrected_workaround (default: True)
            ... other fields to update
        
        Returns:
            bool: Success
        """
        # Use ChromaDB if available
        if self.use_chromadb and self.chromadb_collection:
            try:
                sr_id_upper = sr_id.upper().strip()
                
                # Find existing record
                results = self.chromadb_collection.get(
                    where={"call_id": sr_id_upper},
                    include=['metadatas', 'documents', 'embeddings']
                )
                
                if not results or not results['ids']:
                    logger.warning(f"⚠️ SR {sr_id} not found in ChromaDB - will be added as new entry")
                    return self.add_user_feedback_entry(
                        sr_id=sr_id,
                        description=description or '',
                        notes=notes or '',
                        user_corrected_workaround='',
                        ai_generated_workaround=ai_generated_workaround or 'NA',
                        priority=priority or 'P3',
                        function_category=function_category,
                        resolution_categorization=resolution_categorization,
                        sla_resolution_categorization_t1=sla_resolution_categorization_t1,
                        sla_resolution_category=sla_resolution_category,
                        workaround=workaround,
                        resolution=resolution,
                        status=status,
                        application=application,
                        **additional_fields
                    )
                
                record_id = results['ids'][0]
                existing_metadata = results['metadatas'][0].copy()
                old_doc = results['documents'][0] if results['documents'] else ''
                
                # Preserve user feedback if requested
                existing_user_workaround = existing_metadata.get('user_corrected_workaround', '')
                
                # Update metadata with new values (only if provided)
                if ai_generated_workaround is not None:
                    existing_metadata['ai_generated_workaround'] = str(ai_generated_workaround)[:1000]
                    existing_metadata['ai_workaround_updated'] = datetime.now().isoformat()
                if description is not None:
                    existing_metadata['description'] = str(description)[:500]
                if notes is not None:
                    # 'summary' removed - was redundant
                    existing_metadata['wl_summary'] = str(notes)[:500]
                if priority is not None:
                    existing_metadata['priority'] = str(priority)
                if function_category is not None:
                    existing_metadata['function_category'] = str(function_category)
                if resolution_categorization is not None:
                    existing_metadata['resolution_categorization'] = str(resolution_categorization)
                if sla_resolution_categorization_t1 is not None:
                    existing_metadata['sla_resolution_categorization_t1'] = str(sla_resolution_categorization_t1)
                if sla_resolution_category is not None:
                    existing_metadata['sla_resolution_category'] = str(sla_resolution_category)
                if resolution is not None:
                    existing_metadata['resolution'] = str(resolution)[:1000]
                if workaround is not None:
                    existing_metadata['workaround'] = str(workaround)[:1000]
                if status is not None:
                    existing_metadata['status'] = str(status)
                if application is not None:
                    existing_metadata['application'] = str(application)
                
                # Add additional fields
                for key, value in additional_fields.items():
                    if value is not None:
                        if key == 'reported_date':
                            existing_metadata['Reported Date'] = str(value)
                        else:
                            existing_metadata[key] = str(value)[:500] if isinstance(value, str) else value
                
                # Preserve user feedback if requested
                if preserve_user_feedback and existing_user_workaround:
                    existing_metadata['user_corrected_workaround'] = existing_user_workaround
                    logger.info(f"   🔒 Preserved user feedback for SR {sr_id}")
                
                existing_metadata['admin_updated'] = datetime.now().isoformat()
                existing_metadata['added_date'] = datetime.now().strftime('%Y-%m-%d')  # Update to today so it shows in today's dashboard
                existing_metadata['source'] = 'admin_upload'
                
                # Re-encode (only description, summary removed as redundant)
                doc_text = existing_metadata.get('description', '')
                new_embedding = None
                if self.model:
                    new_embedding = self.model.encode([doc_text])[0].tolist()
                
                # Delete and re-add
                self.chromadb_collection.delete(ids=[record_id])
                self.chromadb_collection.add(
                    ids=[record_id],
                    embeddings=[new_embedding] if new_embedding else None,
                    documents=[doc_text],
                    metadatas=[existing_metadata]
                )
                
                logger.info(f"✅ Updated SR {sr_id} from admin upload in ChromaDB (preserved user feedback: {preserve_user_feedback and bool(existing_user_workaround)})")
                return True
                
            except Exception as e:
                logger.error(f"ChromaDB update error for SR {sr_id}: {e}")
                import traceback
                traceback.print_exc()
                return False
        
        # Fallback to pickle
        try:
            if not self.db_data:
                logger.error("No database loaded!")
                return False
            
            # Find existing SR
            sr_index = self._find_entry_by_sr_id(sr_id)
            
            if sr_index is None:
                logger.warning(f"⚠️ SR {sr_id} not found for update - will be added as new entry")
                # Fall back to add_user_feedback_entry for new SRs
                return self.add_user_feedback_entry(
                    sr_id=sr_id,
                    description=description or '',
                    notes=notes or '',
                    user_corrected_workaround='',
                    ai_generated_workaround=ai_generated_workaround or 'NA',
                    priority=priority or 'P3',
                    function_category=function_category,
                    resolution_categorization=resolution_categorization,
                    sla_resolution_categorization_t1=sla_resolution_categorization_t1,
                    sla_resolution_category=sla_resolution_category,
                    workaround=workaround,
                    resolution=resolution,
                    status=status,
                    application=application,
                    **additional_fields
                )
            
            # Get existing metadata
            existing_metadata = self.db_data['metadata'][sr_index].copy()
            
            # 🔒 Preserve user feedback if requested
            existing_user_workaround = existing_metadata.get('user_corrected_workaround', '')
            
            # Update metadata with new values (only if provided)
            if ai_generated_workaround is not None:
                existing_metadata['ai_generated_workaround'] = ai_generated_workaround
                existing_metadata['ai_workaround_updated'] = datetime.now().isoformat()
            
            if description is not None:
                existing_metadata['description'] = description
            
            if notes is not None:
                # 'summary' removed - was redundant
                existing_metadata['wl_summary'] = notes
            
            if priority is not None:
                existing_metadata['priority'] = priority
            
            if function_category is not None:
                existing_metadata['function_category'] = function_category
            
            if resolution_categorization is not None:
                existing_metadata['resolution_categorization'] = resolution_categorization
            
            if sla_resolution_categorization_t1 is not None:
                existing_metadata['sla_resolution_categorization_t1'] = sla_resolution_categorization_t1
            
            if sla_resolution_category is not None:
                existing_metadata['sla_resolution_category'] = sla_resolution_category
            
            if resolution is not None:
                existing_metadata['resolution'] = resolution
            
            if workaround is not None:
                existing_metadata['workaround'] = workaround
            
            if status is not None:
                existing_metadata['status'] = status
            
            if application is not None:
                existing_metadata['application'] = application
            
            # Add any additional fields
            for key, value in additional_fields.items():
                if value is not None:
                    # 🆕 Map reported_date to 'Reported Date' for consistency
                    if key == 'reported_date':
                        existing_metadata['Reported Date'] = value
                    else:
                        existing_metadata[key] = value
            
            # 🔒 PRESERVE user feedback if requested
            if preserve_user_feedback and existing_user_workaround:
                existing_metadata['user_corrected_workaround'] = existing_user_workaround
                logger.info(f"   🔒 Preserved user feedback for SR {sr_id}")
            
            # Mark as updated from admin
            existing_metadata['admin_updated'] = datetime.now().isoformat()
            existing_metadata['source'] = 'admin_upload'
            
            # Update searchable text and embedding
            searchable_text = self._create_searchable_text(existing_metadata)
            
            if self.model and SENTENCE_TRANSFORMERS_AVAILABLE:
                new_embedding = self.model.encode([searchable_text])[0]
                self.db_data['embeddings'][sr_index] = new_embedding
            else:
                logger.warning("No model available for embedding generation")
            
            # Update metadata and document
            self.db_data['metadata'][sr_index] = existing_metadata
            self.db_data['documents'][sr_index] = searchable_text
            
            # Save to disk
            self.save_database()
            
            logger.info(f"✅ Updated SR {sr_id} from admin upload (preserved user feedback: {preserve_user_feedback and bool(existing_user_workaround)})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error updating SR {sr_id} from admin: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def _find_entry_by_sr_id(self, sr_id: str) -> Optional[int]:
        """Find an entry index by SR ID"""
        if not self.db_data or 'metadata' not in self.db_data:
            return None
        
        for idx, metadata in enumerate(self.db_data['metadata']):
            if metadata.get('call_id') == sr_id:
                return idx
        
        return None
    
    def _create_searchable_text(self, metadata: Dict[str, Any]) -> str:
        """Create searchable text from metadata with preprocessing"""
        parts = []
        
        # Priority field for search (summary removed - was redundant)
        matching_fields = ['description']
        
        # Add matching fields
        for field in matching_fields:
            value = str(metadata.get(field, '')).strip()
            if value and value.lower() not in ['nan', 'none', '', 'na']:
                parts.append(value)
        
        # Add NEW categorization fields (kept original, used for context)
        category_fields = [
            'resolution_categorization',
            'resolution_categorization_tier3',
            'sla_resolution_categorization_t1',
            'sla_resolution_category'
        ]
        
        for field in category_fields:
            value = str(metadata.get(field, '')).strip()
            if value and value.lower() not in ['nan', 'none', '', 'na']:
                parts.append(f"{field}: {value}")
        
        # Add workaround fields (kept original, not used for matching)
        other_fields = ['workaround', 'wl_summary', 'user_corrected_workaround', 'ai_generated_workaround']
        for field in other_fields:
            value = str(metadata.get(field, '')).strip()
            if value and value.lower() not in ['nan', 'none', '', 'na']:
                parts.append(value)
        
        searchable_text = " ".join(parts)
        
        # 🆕 PREPROCESS if database uses preprocessing
        db_is_preprocessed = self.db_data.get('preprocessed', False) if self.db_data else False
        if db_is_preprocessed and self.preprocessor:
            searchable_text = self.preprocessor.clean_for_semantic_search(searchable_text)
            
        return searchable_text
    
    def get_all_user_feedback_for_sr(self, sr_id: str) -> List[Dict[str, Any]]:
        """
        Get ALL user feedback entries for a specific SR ID.
        Supports multiple user workarounds per SR (stored as JSON array).
        
        NEW BEHAVIOR: Parses the JSON user_corrected_workaround field to return
        individual feedback entries for each user.
        
        Args:
            sr_id: Service Request ID
        
        Returns:
            List of user feedback dictionaries, sorted by date (newest first)
        """
        user_feedback_list = []
        sr_id_upper = str(sr_id).upper().strip()
        
        # Use ChromaDB if available
        if self.use_chromadb and self.chromadb_collection:
            try:
                # Get the SR record (single record per SR now)
                results = self.chromadb_collection.get(
                    where={"call_id": sr_id_upper},
                    include=['metadatas']
                )
                
                if results and results.get('metadatas'):
                    metadata = results['metadatas'][0]
                    record_id = results['ids'][0] if results.get('ids') else sr_id_upper
                    
                    # Parse JSON user_corrected_workaround field
                    user_wa_field = metadata.get('user_corrected_workaround', '')
                    
                    try:
                        wa_history = json.loads(user_wa_field) if user_wa_field else []
                        if not isinstance(wa_history, list):
                            # Old plain text format
                            wa_history = [{'user': 'legacy', 'wa': str(user_wa_field), 'date': ''}] if user_wa_field else []
                    except json.JSONDecodeError:
                        # Old plain text format
                        wa_history = [{'user': 'legacy', 'wa': str(user_wa_field), 'date': ''}] if user_wa_field else []
                    
                    # Create individual feedback entries from JSON array
                    for i, entry in enumerate(wa_history):
                        feedback_entry = {
                            'id': f"{record_id}_wa_{i}",
                            'sr_id': sr_id_upper,
                            'user_corrected_workaround': entry.get('wa', ''),
                            'corrected_by': entry.get('user', 'user'),
                            'feedback_date': entry.get('date', ''),
                            'function_category': metadata.get('function_category', ''),
                            'resolution_categorization': metadata.get('resolution_categorization', ''),
                            'description': metadata.get('description', ''),
                            'notes': metadata.get('wl_summary', metadata.get('description', '')[:100]),
                            'ai_generated_workaround': metadata.get('ai_generated_workaround', 'NA'),
                            'source': 'user_feedback'
                        }
                        user_feedback_list.append(feedback_entry)
                
                # Sort by feedback_date (newest first)
                user_feedback_list.sort(
                    key=lambda x: x.get('feedback_date', ''),
                    reverse=True
                )
                
                logger.info(f"Found {len(user_feedback_list)} user feedback entries for SR {sr_id_upper}")
                return user_feedback_list
                
            except Exception as e:
                logger.warning(f"ChromaDB user feedback search error: {e}")
        
        # Fallback to pickle (legacy behavior)
        if self.db_data and 'metadata' in self.db_data:
            for idx, metadata in enumerate(self.db_data['metadata']):
                if metadata.get('call_id', '').upper() == sr_id_upper:
                    user_wa_field = metadata.get('user_corrected_workaround', '')
                    if user_wa_field:
                        feedback_entry = {
                            'id': f"pickle_{idx}",
                            'sr_id': sr_id_upper,
                            'user_corrected_workaround': user_wa_field,
                            'corrected_by': metadata.get('corrected_by', 'user'),
                            'feedback_date': metadata.get('feedback_date', ''),
                            'function_category': metadata.get('function_category', ''),
                            'resolution_categorization': metadata.get('resolution_categorization', ''),
                            'description': metadata.get('description', ''),
                            'notes': metadata.get('wl_summary', metadata.get('description', '')[:100]),
                            'ai_generated_workaround': metadata.get('ai_generated_workaround', 'NA'),
                            'source': 'user_feedback'
                        }
                        user_feedback_list.append(feedback_entry)
            
            # Sort by feedback_date (newest first)
            user_feedback_list.sort(
                key=lambda x: x.get('feedback_date', ''),
                reverse=True
            )
        
        logger.info(f"Found {len(user_feedback_list)} user feedback entries for SR {sr_id_upper}")
        return user_feedback_list
    
    def get_user_feedback_count_for_sr(self, sr_id: str) -> int:
        """Get count of user feedback entries for a specific SR"""
        return len(self.get_all_user_feedback_for_sr(sr_id))
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        # Use ChromaDB if available
        if self.use_chromadb and self.chromadb_collection:
            try:
                count = self.chromadb_collection.count()
                
                # Count user feedback entries
                user_feedback_count = 0
                try:
                    user_feedback_results = self.chromadb_collection.get(
                        where={"source": {"$eq": "user_feedback"}},
                        include=['metadatas']
                    )
                    if user_feedback_results and user_feedback_results.get('ids'):
                        user_feedback_count = len(user_feedback_results['ids'])
                except Exception:
                    pass  # ChromaDB might not support this query
                
                return {
                    'total_records': count,
                    'user_feedback_count': user_feedback_count,
                    'columns': ['call_id', 'description', 'workaround', 'ai_generated_workaround', 'user_corrected_workaround'],
                    'model_name': 'all-MiniLM-L6-v2',
                    'storage': 'ChromaDB',
                    'created_at': 'ChromaDB',
                    'last_updated': 'ChromaDB'
                }
            except Exception as e:
                logger.warning(f"ChromaDB stats error: {e}")
        
        # Fallback to pickle
        if not self.db_data:
            return {
                'total_records': 0,
                'user_feedback_count': 0,
                'columns': []
            }
        
        metadata_list = self.db_data.get('metadata', [])
        user_feedback_count = sum(
            1 for m in metadata_list 
            if m.get('source') == 'user_feedback' or m.get('user_corrected_workaround', '').strip()
        )
        
        return {
            'total_records': len(metadata_list),
            'user_feedback_count': user_feedback_count,
            'columns': self.db_data.get('columns', []),
            'model_name': self.db_data.get('model_name', 'unknown'),
            'created_at': self.db_data.get('created_at', 'unknown'),
            'last_updated': self.db_data.get('last_updated', 'unknown')
        }


if __name__ == '__main__':
    # Test the manager
    print("="*80)
    print("HISTORY DATABASE MANAGER - TEST")
    print("="*80)
    
    # Try the local path
    manager = HistoryDatabaseManager('data/database/clean_history_data.db')
    
    if not manager.db_data:
        print("\n[ERROR] Database not found")
        print("Please ensure clean_history_data.db exists in data/database/ directory")
        exit(1)
    
    # Get statistics
    stats = manager.get_statistics()
    print("\nDatabase Statistics:")
    print(f"  Total Records: {stats['total_records']}")
    print(f"  User Feedback Count: {stats['user_feedback_count']}")
    print(f"  Model: {stats.get('model_name', 'unknown')}")
    print(f"  Columns: {len(stats['columns'])} - {stats['columns']}")
    print(f"  Created: {stats.get('created_at', 'unknown')}")
    print(f"  Last Updated: {stats.get('last_updated', 'unknown')}")
    
    print("\n" + "="*80)
    print("[OK] Test complete! History database is ready.")
    print("="*80)

