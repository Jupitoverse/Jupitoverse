"""
Continuous Learning System - Auto-updates historical index with new data and feedback
"""

import os
import pickle
import logging
from datetime import datetime
from scripts.core.historical_data_indexer import HistoricalDataIndexer
from scripts.core.user_feedback_manager import UserFeedbackManager

logger = logging.getLogger(__name__)


class ContinuousLearningSystem:
    """Manages continuous learning from daily uploads and user feedback"""
    
    def __init__(self):
        self.historical_path = 'vector store/historical_sr_index.pkl'
        self.feedback_path = 'vector store/user_feedback.pkl'
        
    def rebuild_vectors(self):
        """Rebuild TF-IDF vectors after adding new data"""
        logger.info("Rebuilding TF-IDF vectors...")
        
        try:
            # Load historical index
            with open(self.historical_path, 'rb') as f:
                data = pickle.load(f)
            
            historical_data = data.get('historical_data', [])
            
            # Create new indexer
            indexer = HistoricalDataIndexer()
            
            # Build vectors
            indexer.historical_data = historical_data
            indexer._build_tfidf_vectors()
            
            # Update data
            data['vectorizer'] = indexer.vectorizer
            data['tfidf_matrix'] = indexer.tfidf_matrix
            data['indexed_at'] = datetime.now().isoformat()
            
            # Save
            with open(self.historical_path, 'wb') as f:
                pickle.dump(data, f)
            
            logger.info(f"✓ Rebuilt vectors for {len(historical_data)} records")
            return True
            
        except Exception as e:
            logger.error(f"Error rebuilding vectors: {e}")
            return False
    
    def incorporate_user_feedback(self):
        """
        Incorporate user feedback into historical index
        Creates synthetic historical records from user corrections
        """
        logger.info("Incorporating user feedback into historical index...")
        
        try:
            # Load user feedback
            if not os.path.exists(self.feedback_path):
                logger.info("No user feedback to incorporate")
                return 0
            
            feedback_manager = UserFeedbackManager()
            feedback_entries = feedback_manager.feedback_data
            
            if not feedback_entries:
                logger.info("No feedback entries found")
                return 0
            
            # Load historical index
            with open(self.historical_path, 'rb') as f:
                historical_index = pickle.load(f)
            
            historical_data = historical_index.get('historical_data', [])
            existing_sr_ids = {sr.get('sr_id') for sr in historical_data}
            
            # Create synthetic records from feedback
            new_records = []
            for entry in feedback_entries:
                sr_id = entry.get('sr_id')
                
                # Check if we should add this (not already in historical data)
                # We add it as a separate "user-corrected" version
                synthetic_sr_id = f"{sr_id}_user_corrected"
                
                if synthetic_sr_id in existing_sr_ids:
                    continue
                
                # Create synthetic historical record
                synthetic_record = {
                    'sr_id': synthetic_sr_id,
                    'original_sr_id': sr_id,
                    'description': entry.get('original_description', ''),
                    'searchable_text': f"{entry.get('original_notes', '')} {entry.get('original_description', '')} {entry.get('user_corrected_workaround', '')}",
                    'priority': 'P3',
                    'assigned_group': 'User Feedback',
                    'status': 'Resolved',
                    'outcome': {
                        'has_workaround': True,
                        'workaround_text': entry.get('user_corrected_workaround', ''),
                        'resolution_type': 'User Corrected'
                    },
                    'source_file': 'user_feedback',
                    'resolution': entry.get('user_corrected_workaround', ''),
                    'created_date': entry.get('feedback_date', datetime.now().isoformat()),
                    'success_flag': True,
                    'application': 'User Feedback',
                    'functional_area': 'User Corrected',
                    'keywords': ['user_feedback', 'corrected'],
                    'feedback_metadata': {
                        'corrected_by': entry.get('corrected_by', 'user'),
                        'helpful_count': entry.get('helpful_count', 0),
                        'used_count': entry.get('used_count', 0)
                    }
                }
                
                new_records.append(synthetic_record)
            
            if not new_records:
                logger.info("No new feedback records to add")
                return 0
            
            # Add to historical data
            historical_data.extend(new_records)
            historical_index['historical_data'] = historical_data
            historical_index['indexed_at'] = datetime.now().isoformat()
            
            # Save updated index
            with open(self.historical_path, 'wb') as f:
                pickle.dump(historical_index, f)
            
            logger.info(f"✓ Added {len(new_records)} user feedback records")
            logger.info(f"✓ Total historical records: {len(historical_data)}")
            
            # Rebuild vectors
            self.rebuild_vectors()
            
            return len(new_records)
            
        except Exception as e:
            logger.error(f"Error incorporating feedback: {e}")
            return 0
    
    def get_learning_stats(self):
        """Get statistics about the learning system"""
        try:
            # Load historical index
            with open(self.historical_path, 'rb') as f:
                data = pickle.load(f)
            
            historical_data = data.get('historical_data', [])
            
            # Count by source
            sources = {}
            for record in historical_data:
                source = record.get('source_file', 'unknown')
                sources[source] = sources.get(source, 0) + 1
            
            # Count user feedback records
            user_feedback_count = sum(1 for r in historical_data if 'user_corrected' in r.get('sr_id', ''))
            
            return {
                'total_records': len(historical_data),
                'sources': sources,
                'user_feedback_records': user_feedback_count,
                'last_indexed': data.get('indexed_at', 'Unknown')
            }
            
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}

