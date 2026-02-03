#!/usr/bin/env python3
"""
User Feedback Manager - Simplified Vectorstore Only Approach
Manages user-corrected workarounds using ONLY clean_history_data.db with Sentence Transformers.
No pickle file, no TF-IDF, no metadata tracking - direct to vectorstore with preprocessing.
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional
import sys

# Add parent directory to path to import history_db_manager
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

# Setup logger FIRST
logger = logging.getLogger(__name__)

# Import history database manager
try:
    from history_db_manager import HistoryDatabaseManager
    HISTORY_DB_MANAGER_AVAILABLE = True
except ImportError:
    HISTORY_DB_MANAGER_AVAILABLE = False
    logger.error("❌ history_db_manager not available - feedback system will not work!")


class UserFeedbackManager:
    """
    Simplified user feedback manager using ONLY vectorstore.
    All feedback goes directly to clean_history_data.db with preprocessing and Sentence Transformers.
    No metadata tracking, no pickle file, no TF-IDF.
    """
    
    def __init__(self, feedback_path: str = "vector store/user_feedback.pkl"):
        """Initialize the user feedback manager"""
        # Note: feedback_path parameter kept for backward compatibility but not used
        self.total_feedback_count = 0
        
        # Initialize history database manager (ONLY storage system)
        self.history_db_manager = None
        if HISTORY_DB_MANAGER_AVAILABLE:
            try:
                history_db_path = Path("vector store/clean_history_data.db")
                if history_db_path.exists():
                    self.history_db_manager = HistoryDatabaseManager(str(history_db_path))
                    
                    # Get initial count from database
                    if self.history_db_manager.db_data:
                        stats = self.history_db_manager.get_statistics()
                        self.total_feedback_count = stats.get('user_feedback_count', 0)
                    
                    logger.info("✅ Feedback Manager initialized (Vectorstore-only mode)")
                    logger.info(f"   📊 Current user feedback count: {self.total_feedback_count}")
                    logger.info(f"   🔍 Using: Sentence Transformers (all-MiniLM-L6-v2)")
                    logger.info(f"   📋 Storage: clean_history_data.db only")
                else:
                    logger.warning(f"⚠️ History database not found at {history_db_path}")
            except Exception as e:
                logger.error(f"❌ Error initializing history database manager: {str(e)}")
        else:
            logger.error("❌ Cannot initialize - history_db_manager not available!")
    
    def add_feedback(
        self,
        sr_id: str,
        original_description: str,
        original_notes: str = "",
        original_workaround: str = "",
        user_corrected_workaround: str = "",
        user_corrected_interface: str = "",
        corrected_by: str = "user"
    ) -> bool:
        """
        Add user feedback directly to clean_history_data.db with preprocessing.
        
        Args:
            sr_id: Service Request ID
            original_description: Original SR description (will be preprocessed for search)
            original_notes: Original SR notes (will be preprocessed for search)
            original_workaround: AI-generated workaround (kept original for display)
            user_corrected_workaround: User's corrected workaround (kept original for display)
            user_corrected_interface: User's corrected interface
            corrected_by: User identifier (email, name, etc.)
        
        Returns:
            bool: Success status
        """
        try:
            if not self.history_db_manager:
                logger.error("❌ History database manager not available!")
                return False
            
            logger.info(f"💾 Saving user feedback for SR {sr_id} to vectorstore...")
            
            # Add to clean_history_data.db
            # Preprocessing is applied automatically in _create_searchable_text()
            success = self.history_db_manager.add_user_feedback_entry(
                sr_id=sr_id,
                description=original_description,  # ✅ Will be preprocessed
                notes=original_notes,  # ✅ Will be preprocessed
                user_corrected_workaround=user_corrected_workaround or "",  # ❌ NOT preprocessed (for display)
                ai_generated_workaround=original_workaround or "NA",  # ❌ NOT preprocessed (for display)
                priority="User Feedback",
                function_category=user_corrected_interface or "User Corrected",
                resolution_categorization="User Correction",
                status_reason=f"User Feedback - Corrected by {corrected_by}",
                corrected_by=corrected_by,
                feedback_date=datetime.now().isoformat()
            )
            
            if success:
                self.total_feedback_count += 1
                logger.info(f"✅ Feedback saved to clean_history_data.db for SR {sr_id}")
                logger.info(f"   📊 Total user feedback entries: {self.total_feedback_count}")
                logger.info(f"   🔍 Preprocessing: Applied to description/notes")
                logger.info(f"   🧠 Embedding: Generated using Sentence Transformers (384D)")
                logger.info(f"   💾 Storage: Vectorstore only (no pkl file)")
                logger.info(f"   ✅ Searchable: Available for future semantic searches")
                return True
            else:
                logger.error(f"❌ Failed to add feedback to vectorstore for SR {sr_id}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error adding feedback: {str(e)}")
            return False
    
    def get_feedback_by_sr_id(self, sr_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user feedback for a specific SR ID from vectorstore.
        
        Args:
            sr_id: Service Request ID
        
        Returns:
            Feedback entry dict or None if not found
        """
        try:
            if not self.history_db_manager or not self.history_db_manager.db_data:
                return None
            
            # Search through metadata in vectorstore
            metadata_list = self.history_db_manager.db_data.get('metadata', [])
            
            for metadata in metadata_list:
                # Check if this is a user feedback entry for this SR
                if (metadata.get('call_id') == sr_id and 
                    metadata.get('source') == 'user_feedback'):
                    
                    # Return in expected format
                    return {
                        'sr_id': sr_id,
                        'user_corrected_workaround': metadata.get('user_corrected_workaround', ''),
                        'user_corrected_interface': metadata.get('function_category', ''),
                        'original_description': metadata.get('description', ''),
                        'original_notes': metadata.get('summary', ''),
                        'original_workaround': metadata.get('ai_generated_workaround', ''),
                        'feedback_date': metadata.get('feedback_date', ''),
                        'corrected_by': metadata.get('corrected_by', 'user')
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Error getting feedback for SR {sr_id}: {str(e)}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get feedback statistics from vectorstore"""
        try:
            if not self.history_db_manager or not self.history_db_manager.db_data:
                return {
                    'total_feedback': 0,
                    'user_feedback_count': 0
                }
            
            stats = self.history_db_manager.get_statistics()
            
            return {
                'total_feedback': stats.get('user_feedback_count', 0),
                'user_feedback_count': stats.get('user_feedback_count', 0),
                'total_records': stats.get('total_records', 0)
            }
            
        except Exception as e:
            logger.error(f"❌ Error getting statistics: {str(e)}")
            return {
                'total_feedback': 0,
                'user_feedback_count': 0
            }
    
    def load_feedback(self) -> bool:
        """
        Load feedback - kept for backward compatibility.
        Now just checks if database is available.
        """
        if self.history_db_manager and self.history_db_manager.db_data:
            logger.info("✅ Vectorstore loaded - feedback system ready")
            return True
        else:
            logger.warning("⚠️ Vectorstore not available")
            return False
    
    def save_feedback(self) -> bool:
        """
        Save feedback - kept for backward compatibility.
        Vectorstore auto-saves when feedback is added.
        """
        # No action needed - vectorstore handles saving automatically
        return True
    
    def mark_helpful(self, sr_id: str) -> bool:
        """
        Mark a feedback entry as helpful.
        Note: Without metadata tracking, this just logs the action.
        """
        logger.info(f"✅ User marked SR {sr_id} feedback as helpful")
        return True
    
    def remove_duplicates(self) -> int:
        """
        Remove duplicates - kept for backward compatibility.
        Vectorstore prevents duplicates automatically.
        """
        return 0
