#!/usr/bin/env python3
"""
History Database Manager
Manages dynamic updates to clean_history_data.db vectorstore including user feedback integration
"""

import pickle
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional
import numpy as np

# Setup logger
logger = logging.getLogger(__name__)

# Try to import sentence transformers
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    logger.warning("sentence-transformers not available - limited functionality")

# 🆕 Try to import SR text preprocessor
try:
    from sr_text_preprocessor import SRTextPreprocessor
    PREPROCESSOR_AVAILABLE = True
except ImportError:
    PREPROCESSOR_AVAILABLE = False
    logger.warning("SRTextPreprocessor not available - text won't be preprocessed")


class HistoryDatabaseManager:
    """
    Manages the clean_history_data.db vectorstore with support for:
    - Loading existing database
    - Adding user feedback as new entries
    - Updating existing entries
    - Maintaining semantic search index with preprocessing
    """
    
    def __init__(self, db_path: str = "vector store/clean_history_data.db"):
        """Initialize the history database manager"""
        self.db_path = Path(db_path)
        self.db_data = None
        self.model = None
        self.model_name = None
        self.preprocessor = SRTextPreprocessor() if PREPROCESSOR_AVAILABLE else None
        
        # Load database if it exists
        if self.db_path.exists():
            self.load_database()
        else:
            logger.warning(f"Database not found at {self.db_path}")
    
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
                    # Try loading with device='cpu' to avoid PyTorch device issues
                    self.model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
                    logger.info("✅ Model loaded successfully!")
                except Exception as model_error:
                    logger.warning(f"⚠️ Could not load model with device='cpu': {str(model_error)}")
                    try:
                        # Fallback: Try without device specification
                        self.model = SentenceTransformer('all-MiniLM-L6-v2')
                        logger.info("✅ Model loaded successfully (fallback method)!")
                    except Exception as fallback_error:
                        logger.error(f"❌ Failed to load model: {str(fallback_error)}")
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
        Add a new entry to the history database from user feedback
        
        Args:
            sr_id: Service Request ID
            description: SR description
            notes: SR notes (used for better matching)
            user_corrected_workaround: User's corrected workaround
            ai_generated_workaround: AI-generated workaround (default "NA")
            priority: Priority level (default "User Feedback")
            additional_fields: Any additional metadata fields
        
        Returns:
            bool: Success status
        """
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
                'summary': notes if notes else description[:100],
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
                'assigned_to': additional_fields.get('assigned_to', 'Not Assigned')
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
                existing_metadata['summary'] = notes
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
        
        # Priority fields for search (description and summary for matching)
        matching_fields = ['description', 'summary']
        
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
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
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
    manager = HistoryDatabaseManager('vector store/history_data.db')
    
    if not manager.db_data:
        print("\n[ERROR] Database not found")
        print("Please ensure history_data.db exists in vector store/ directory")
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

