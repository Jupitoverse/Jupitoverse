#!/usr/bin/env python3
"""
Universal SQLite Database Creator
Reads Excel files from subfolders and creates a SQLite database for each subfolder

PLUG AND PLAY USAGE:
1. Create subfolders in: data/database/database_creation/
   - Each subfolder name becomes the database name
   - Put Excel files in each subfolder
   
2. Example structure:
   database_creation/
   ├── create_database.py          ← This script
   ├── people_skills/              ← Subfolder name = database name
   │   ├── team_data.xlsx
   │   └── skills_data.xlsx
   ├── sr_tracking/
   │   └── sr_history.xlsx
   └── custom_data/
       └── data.xlsx

3. Run: python create_database.py

4. Output:
   data/database/
   ├── people_skills.db            ← Created from people_skills/ folder
   ├── sr_tracking.db              ← Created from sr_tracking/ folder
   └── custom_data.db              ← Created from custom_data/ folder
"""
import os
import sys
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime
import argparse
import logging
import re

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Path setup - this script is in data/database/database_creation/
SCRIPT_DIR = Path(__file__).parent.absolute()
DATABASE_DIR = SCRIPT_DIR.parent  # data/database/


def sanitize_column_name(name: str) -> str:
    """
    Sanitize column name for SQLite compatibility
    - Replace special characters with underscores
    - Remove leading/trailing whitespace
    - Handle empty names
    """
    if not name or pd.isna(name):
        return "unnamed_column"
    
    name = str(name).strip()
    
    # Replace special characters with underscore
    name = re.sub(r'[^\w\s]', '_', name)
    
    # Replace spaces with underscore
    name = re.sub(r'\s+', '_', name)
    
    # Remove consecutive underscores
    name = re.sub(r'_+', '_', name)
    
    # Remove leading/trailing underscores
    name = name.strip('_')
    
    # Ensure it doesn't start with a number
    if name and name[0].isdigit():
        name = 'col_' + name
    
    # Handle empty result
    if not name:
        name = "unnamed_column"
    
    return name


def get_sqlite_type(dtype) -> str:
    """
    Map pandas dtype to SQLite type
    """
    dtype_str = str(dtype).lower()
    
    if 'int' in dtype_str:
        return 'INTEGER'
    elif 'float' in dtype_str:
        return 'REAL'
    elif 'datetime' in dtype_str or 'timestamp' in dtype_str:
        return 'TIMESTAMP'
    elif 'bool' in dtype_str:
        return 'INTEGER'  # SQLite doesn't have boolean
    else:
        return 'TEXT'


class UniversalDatabaseCreator:
    """
    Creates SQLite databases from Excel files in subfolders
    
    Each subfolder becomes a database:
    - Subfolder name = database name
    - All Excel files in subfolder are combined
    - Column names preserved from Excel (sanitized for SQLite)
    """
    
    def __init__(
        self,
        input_folder: str = None,
        output_folder: str = None,
        table_name: str = "data"
    ):
        self.input_folder = Path(input_folder or SCRIPT_DIR)
        self.output_folder = Path(output_folder or DATABASE_DIR)
        self.default_table_name = table_name
        
        self.created_databases = []
        
    def get_subfolders(self) -> list:
        """Get all subfolders (each will become a database)"""
        subfolders = []
        
        for item in self.input_folder.iterdir():
            if item.is_dir() and not item.name.startswith('.') and not item.name.startswith('__'):
                subfolders.append(item)
        
        return sorted(subfolders)
    
    def load_excel_files(self, folder: Path) -> pd.DataFrame:
        """Load all Excel files from a folder"""
        excel_files = []
        for ext in ['*.xlsx', '*.xls']:
            excel_files.extend(folder.glob(ext))
        
        # Filter out temp files
        excel_files = [f for f in excel_files if not f.name.startswith('~')]
        
        if not excel_files:
            return None
        
        logger.info(f"  Found {len(excel_files)} Excel files")
        
        all_data = []
        for file_path in sorted(excel_files):
            try:
                logger.info(f"    Loading {file_path.name}...")
                df = pd.read_excel(file_path)
                
                # Add source tracking
                df['_source_file'] = file_path.name
                
                all_data.append(df)
                logger.info(f"      Loaded {len(df)} rows, {len(df.columns)} columns")
                
            except Exception as e:
                logger.error(f"      Error loading {file_path.name}: {e}")
        
        if not all_data:
            return None
        
        # Combine all dataframes
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Fill NaN with empty string for text columns
        for col in combined_df.columns:
            if combined_df[col].dtype == 'object':
                combined_df[col] = combined_df[col].fillna('')
        
        return combined_df
    
    def create_database(self, folder: Path) -> bool:
        """Create SQLite database from folder contents"""
        folder_name = folder.name
        db_name = f"{folder_name}.db"
        db_path = self.output_folder / db_name
        
        logger.info(f"\nProcessing folder: {folder_name}")
        logger.info(f"  Output: {db_path}")
        
        # Load Excel files
        df = self.load_excel_files(folder)
        
        if df is None or len(df) == 0:
            logger.warning(f"  No data found in {folder_name}")
            return False
        
        logger.info(f"  Total records: {len(df)}")
        
        # Sanitize column names
        original_columns = df.columns.tolist()
        sanitized_columns = []
        column_mapping = {}
        
        for col in original_columns:
            sanitized = sanitize_column_name(col)
            
            # Handle duplicate column names
            base_name = sanitized
            counter = 1
            while sanitized in sanitized_columns:
                sanitized = f"{base_name}_{counter}"
                counter += 1
            
            sanitized_columns.append(sanitized)
            column_mapping[col] = sanitized
        
        df.columns = sanitized_columns
        
        # Log column mapping if names changed
        changed_cols = [(orig, san) for orig, san in column_mapping.items() if orig != san]
        if changed_cols:
            logger.info(f"  Column name changes:")
            for orig, san in changed_cols[:5]:
                logger.info(f"    '{orig}' -> '{san}'")
            if len(changed_cols) > 5:
                logger.info(f"    ... and {len(changed_cols) - 5} more")
        
        # Remove existing database if exists
        if db_path.exists():
            logger.info(f"  Removing existing database: {db_name}")
            os.remove(db_path)
        
        # Create SQLite database
        try:
            conn = sqlite3.connect(db_path)
            
            # Determine table name (use folder name or default)
            table_name = sanitize_column_name(folder_name)
            if not table_name:
                table_name = self.default_table_name
            
            # Create table with proper types
            columns_with_types = []
            for col in df.columns:
                col_type = get_sqlite_type(df[col].dtype)
                columns_with_types.append(f'"{col}" {col_type}')
            
            # Add auto-increment ID
            create_sql = f'''
                CREATE TABLE IF NOT EXISTS "{table_name}" (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    {", ".join(columns_with_types)}
                )
            '''
            
            conn.execute(create_sql)
            
            # Insert data
            df.to_sql(table_name, conn, if_exists='replace', index=False)
            
            # Create index on common columns if they exist
            common_index_columns = ['call_id', 'sr_id', 'incident_id', 'name', 'id']
            for col in common_index_columns:
                if col in df.columns:
                    try:
                        conn.execute(f'CREATE INDEX IF NOT EXISTS idx_{table_name}_{col} ON "{table_name}" ("{col}")')
                    except:
                        pass
            
            conn.commit()
            
            # Verify
            cursor = conn.cursor()
            cursor.execute(f'SELECT COUNT(*) FROM "{table_name}"')
            count = cursor.fetchone()[0]
            
            conn.close()
            
            logger.info(f"  [SUCCESS] Created {db_name}")
            logger.info(f"    Table: {table_name}")
            logger.info(f"    Records: {count}")
            logger.info(f"    Columns: {len(df.columns)}")
            
            self.created_databases.append({
                'name': db_name,
                'path': str(db_path),
                'table': table_name,
                'records': count,
                'columns': len(df.columns)
            })
            
            return True
            
        except Exception as e:
            logger.error(f"  [FAILED] Error creating database: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def run(self) -> bool:
        """Main execution"""
        print("\n" + "=" * 80)
        print(" UNIVERSAL DATABASE CREATOR")
        print("=" * 80)
        print(f" Input:  {self.input_folder}")
        print(f" Output: {self.output_folder}")
        print("=" * 80 + "\n")
        
        # Ensure output folder exists
        self.output_folder.mkdir(parents=True, exist_ok=True)
        
        # Get subfolders
        subfolders = self.get_subfolders()
        
        if not subfolders:
            logger.warning("No subfolders found!")
            logger.info("\nTo create databases:")
            logger.info("  1. Create subfolders in this directory")
            logger.info("  2. Each subfolder name becomes the database name")
            logger.info("  3. Put Excel files in each subfolder")
            logger.info("  4. Run this script again")
            return False
        
        logger.info(f"Found {len(subfolders)} subfolders to process:")
        for folder in subfolders:
            excel_count = len(list(folder.glob('*.xlsx')) + list(folder.glob('*.xls')))
            logger.info(f"  - {folder.name}/ ({excel_count} Excel files)")
        
        # Process each subfolder
        success_count = 0
        for folder in subfolders:
            if self.create_database(folder):
                success_count += 1
        
        # Summary
        print("\n" + "=" * 80)
        print(" SUMMARY")
        print("=" * 80)
        
        if self.created_databases:
            print(f"\n[SUCCESS] Created {len(self.created_databases)} databases:\n")
            for db in self.created_databases:
                print(f"  {db['name']}")
                print(f"    Table: {db['table']}, Records: {db['records']}, Columns: {db['columns']}")
                print(f"    Path: {db['path']}")
                print()
        else:
            print("\n[WARNING] No databases created")
        
        print("=" * 80)
        
        return success_count > 0


def main():
    parser = argparse.ArgumentParser(
        description="Create SQLite databases from Excel files in subfolders",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python create_database.py
  python create_database.py --output ./custom_output

Directory Structure:
  database_creation/
  ├── create_database.py     ← This script
  ├── people_skills/         ← Subfolder = database name
  │   └── team_data.xlsx
  └── sr_tracking/
      └── sr_history.xlsx
      
Output:
  data/database/
  ├── people_skills.db       ← From people_skills/ folder
  └── sr_tracking.db         ← From sr_tracking/ folder
        """
    )
    
    parser.add_argument('--output', type=str, default=None,
                        help='Output folder for databases (default: data/database/)')
    parser.add_argument('--table', type=str, default='data',
                        help='Default table name (default: "data")')
    
    args = parser.parse_args()
    
    creator = UniversalDatabaseCreator(
        output_folder=args.output,
        table_name=args.table
    )
    
    success = creator.run()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

