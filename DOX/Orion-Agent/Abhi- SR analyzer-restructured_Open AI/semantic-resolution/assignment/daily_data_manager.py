"""
Daily Data Manager - Handles daily Excel uploads and merges into historical index
"""

import os
import pickle
import pandas as pd
from datetime import datetime
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class DailyDataManager:
    """Manages daily SR uploads and integration into historical knowledge base"""
    
    def __init__(self):
        self.staging_path = 'data/vectorstore/staging_sr_data.pkl'
        self.historical_path = 'data/vectorstore/historical_sr_index.pkl'
        self.daily_uploads_dir = 'daily_uploads'
        self.processed_dir = 'daily_uploads/processed'
        
        # Create directories if they don't exist
        os.makedirs(self.daily_uploads_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        os.makedirs('data/vectorstore', exist_ok=True)
        
        # Initialize staging data
        self.staging_data = self._load_staging_data()
        
    def _load_staging_data(self):
        """Load staging data or create new"""
        if os.path.exists(self.staging_path):
            try:
                with open(self.staging_path, 'rb') as f:
                    return pickle.load(f)
            except:
                logger.warning("Could not load staging data, creating new")
        
        return {
            'srs': [],
            'last_updated': None,
            'upload_count': 0
        }
    
    def _save_staging_data(self):
        """Save staging data"""
        with open(self.staging_path, 'wb') as f:
            pickle.dump(self.staging_data, f)
    
    def process_daily_upload(self, excel_file, analyzer):
        """
        Process uploaded Excel file and stage new SRs
        
        Args:
            excel_file: Path to Excel file
            analyzer: AIEnhancedServiceRequestAnalyzer instance
            
        Returns:
            dict: Processed SR data indexed by SR ID
        """
        logger.info(f"Processing daily upload: {excel_file}")
        
        # Read Excel file
        df = pd.read_excel(excel_file)
        
        # Convert to SR records
        sr_records = []
        for idx, row in df.iterrows():
            # Try multiple column names for SR ID
            sr_id = (row.get('Call ID') or row.get('SR ID') or row.get('SR Number') or 
                    row.get('Ticket ID') or row.get('SR') or f'SR_{idx}')
            
            sr_record = {
                'SR ID': sr_id,
                'Description': row.get('Description', row.get('Summary', '')),
                'Notes': row.get('Notes', row.get('Additional Notes', row.get('Resolution', ''))),
                'Priority': row.get('Priority', row.get('Customer Priority', 'P3')),
                'Status': row.get('Status', row.get('STATUS', 'Open')),
                'Application': row.get('Application', row.get('Assigned Group', '')),
                'Created Date': row.get('Created Date', row.get('Submit Date', row.get('Open Date', ''))),
            }
            sr_records.append(sr_record)
        
        # Analyze SRs
        logger.info(f"Analyzing {len(sr_records)} SRs...")
        analysis_results = analyzer.analyze_sr_batch(sr_records)
        
        # Index by SR ID for easy lookup
        indexed_results = {}
        for result in analysis_results:
            sr_id = result.get('SR ID', 'Unknown')
            indexed_results[sr_id] = result
        
        # Add to staging
        self.staging_data['srs'].extend(analysis_results)
        self.staging_data['last_updated'] = datetime.now().isoformat()
        self.staging_data['upload_count'] += 1
        self._save_staging_data()
        
        # Move file to processed
        filename = os.path.basename(excel_file)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_filename = f"{timestamp}_{filename}"
        processed_path = os.path.join(self.processed_dir, new_filename)
        
        try:
            import shutil
            shutil.move(excel_file, processed_path)
            logger.info(f"Moved processed file to: {processed_path}")
        except Exception as e:
            logger.warning(f"Could not move file: {e}")
        
        logger.info(f"✓ Processed {len(indexed_results)} SRs")
        return indexed_results
    
    def get_sr_by_id(self, sr_id):
        """Get SR from staging data by ID"""
        for sr in self.staging_data['srs']:
            if sr.get('SR ID') == sr_id:
                return sr
        return None
    
    def get_all_staging_srs(self):
        """Get all SRs in staging"""
        return self.staging_data['srs']
    
    def merge_daily_data(self):
        """
        Merge staging data into historical index
        This should be run as a nightly job
        
        Returns:
            int: Number of new SRs added
        """
        logger.info("Starting nightly merge of daily data...")
        
        if not self.staging_data['srs']:
            logger.info("No staging data to merge")
            return 0
        
        # Load historical index
        try:
            with open(self.historical_path, 'rb') as f:
                historical_index = pickle.load(f)
        except FileNotFoundError:
            logger.error("Historical index not found!")
            return 0
        
        historical_data = historical_index.get('historical_data', [])
        existing_sr_ids = {sr.get('sr_id') for sr in historical_data}
        
        # Convert staging SRs to historical format
        new_records = []
        for sr in self.staging_data['srs']:
            sr_id = sr.get('SR ID')
            
            # Skip if already exists
            if sr_id in existing_sr_ids:
                continue
            
            # Convert to historical format
            historical_record = {
                'sr_id': sr_id,
                'description': sr.get('Original Description', sr.get('Description', '')),
                'searchable_text': f"{sr.get('Original Description', '')} {sr.get('Original Notes/Summary', '')}",
                'priority': sr.get('Priority', 'P3'),
                'assigned_group': sr.get('Application', 'Unknown'),
                'status': sr.get('Status', 'Resolved'),
                'outcome': {
                    'has_workaround': sr.get('Suggested Workaround', 'NA') != 'NA',
                    'workaround_text': sr.get('Suggested Workaround', ''),
                    'resolution_type': 'Daily Upload'
                },
                'source_file': 'daily_upload',
                'resolution': sr.get('Suggested Workaround', ''),
                'created_date': sr.get('Created Date', datetime.now().isoformat()),
                'success_flag': True,
                'application': sr.get('Application', 'Unknown'),
                'functional_area': sr.get('Interface', 'Unknown'),
                'keywords': [],
                'phase1_workaround': sr.get('phase1_workaround', {})
            }
            
            new_records.append(historical_record)
        
        if not new_records:
            logger.info("No new records to add")
            return 0
        
        # Add to historical data
        historical_data.extend(new_records)
        historical_index['historical_data'] = historical_data
        historical_index['indexed_at'] = datetime.now().isoformat()
        
        # Backup old index
        backup_path = f"{self.historical_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        try:
            import shutil
            shutil.copy2(self.historical_path, backup_path)
            logger.info(f"Created backup: {backup_path}")
        except Exception as e:
            logger.warning(f"Could not create backup: {e}")
        
        # Save updated index
        with open(self.historical_path, 'wb') as f:
            pickle.dump(historical_index, f)
        
        logger.info(f"✓ Added {len(new_records)} new SRs to historical index")
        logger.info(f"✓ Total historical records: {len(historical_data)}")
        
        # Clear staging
        self.staging_data['srs'] = []
        self.staging_data['last_updated'] = datetime.now().isoformat()
        self._save_staging_data()
        
        logger.info("✓ Cleared staging data")
        
        return len(new_records)
    
    def get_staging_stats(self):
        """Get statistics about staging data"""
        return {
            'sr_count': len(self.staging_data['srs']),
            'last_updated': self.staging_data.get('last_updated'),
            'upload_count': self.staging_data.get('upload_count', 0)
        }

