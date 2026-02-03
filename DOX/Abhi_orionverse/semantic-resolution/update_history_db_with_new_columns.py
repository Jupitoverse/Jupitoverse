#!/usr/bin/env python3
"""
Update existing history_data.db to add new columns:
- ai_generated_workaround (default: "NA")
- user_corrected_workaround (default: "")

This script modifies the existing database without regenerating embeddings.
"""

import pickle
import logging
from pathlib import Path
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def update_database_with_new_columns(db_path: str = "vector store/history_data.db"):
    """Update the database to include new columns"""
    
    # Try multiple possible locations
    possible_paths = [
        Path(db_path),
        Path("semantic-resolution") / db_path,
        Path("semantic-resolution/vector store/history_data.db")
    ]
    
    db_path = None
    for path in possible_paths:
        if path.exists():
            db_path = path
            break
    
    if not db_path:
        logger.error(f"Database not found in any of these locations:")
        for path in possible_paths:
            logger.error(f"  - {path}")
        return False
    
    try:
        # Create backup
        backup_path = db_path.with_suffix('.db.backup')
        logger.info(f"Creating backup at {backup_path}...")
        import shutil
        shutil.copy2(db_path, backup_path)
        logger.info("✅ Backup created successfully")
        
        # Load database
        logger.info(f"Loading database from {db_path}...")
        with open(db_path, 'rb') as f:
            db_data = pickle.load(f)
        
        logger.info(f"✅ Database loaded successfully")
        logger.info(f"   Total records: {len(db_data.get('metadata', []))}")
        logger.info(f"   Existing columns: {db_data.get('columns', [])}")
        
        # Add new columns to metadata
        logger.info("\nAdding new columns to metadata...")
        metadata_list = db_data.get('metadata', [])
        
        updated_count = 0
        for metadata in metadata_list:
            # Add new columns if they don't exist
            if 'ai_generated_workaround' not in metadata:
                metadata['ai_generated_workaround'] = 'NA'
                updated_count += 1
            
            if 'user_corrected_workaround' not in metadata:
                metadata['user_corrected_workaround'] = ''
        
        logger.info(f"✅ Updated {updated_count} records with new columns")
        
        # Update columns list
        if 'columns' in db_data:
            if 'ai_generated_workaround' not in db_data['columns']:
                db_data['columns'].append('ai_generated_workaround')
            if 'user_corrected_workaround' not in db_data['columns']:
                db_data['columns'].append('user_corrected_workaround')
        
        logger.info(f"   New columns list: {db_data.get('columns', [])}")
        
        # Update metadata
        db_data['last_updated'] = datetime.now().isoformat()
        db_data['update_history'] = db_data.get('update_history', [])
        db_data['update_history'].append({
            'date': datetime.now().isoformat(),
            'action': 'Added ai_generated_workaround and user_corrected_workaround columns',
            'records_updated': updated_count
        })
        
        # Save updated database
        logger.info(f"\nSaving updated database...")
        with open(db_path, 'wb') as f:
            pickle.dump(db_data, f, protocol=pickle.HIGHEST_PROTOCOL)
        
        logger.info("✅ Database updated successfully!")
        logger.info(f"\nSummary:")
        logger.info(f"  - Total records: {len(metadata_list)}")
        logger.info(f"  - Records updated: {updated_count}")
        logger.info(f"  - New columns: ai_generated_workaround, user_corrected_workaround")
        logger.info(f"  - Backup saved: {backup_path}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error updating database: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("="*80)
    print("UPDATE HISTORY DATABASE WITH NEW COLUMNS")
    print("="*80)
    print()
    
    # Update the database
    success = update_database_with_new_columns()
    
    if success:
        print("\n" + "="*80)
        print("SUCCESS! Database updated with new columns")
        print("="*80)
        print("\nNew columns added:")
        print("  1. ai_generated_workaround - Placeholder for AI-generated workarounds")
        print("  2. user_corrected_workaround - User feedback corrections")
        print("\nThe original database has been backed up with .backup extension")
        print("\nYou can now:")
        print("  - Add user feedback which will appear in history searches")
        print("  - Populate ai_generated_workaround field in future")
        print("  - Search across all workarounds (historical + user feedback)")
    else:
        print("\n" + "="*80)
        print("ERROR! Database update failed")
        print("="*80)
        print("Check the error messages above for details")
    
    print()
    input("Press Enter to exit...")

