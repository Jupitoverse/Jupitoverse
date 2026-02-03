"""
People Skills Database System
Manages team member skills, specializations, and load capacity with ML learning
"""

import sqlite3
import pandas as pd
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import numpy as np
from collections import defaultdict, Counter

class PeopleSkillsDatabase:
    """
    Database system for managing team skills with ML learning capabilities
    """
    
    def __init__(self, db_path: str = "people_skills.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._init_database()
        
    def _init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Team members table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS team_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            employee_id TEXT UNIQUE,
            status TEXT DEFAULT 'active',
            created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_date DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Skills table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            application TEXT NOT NULL,
            skill_level REAL NOT NULL CHECK(skill_level >= 1.0 AND skill_level <= 5.0),
            specializations TEXT, -- JSON array of specializations
            max_load INTEGER NOT NULL DEFAULT 10,
            confidence_score REAL DEFAULT 0.5, -- ML confidence in skill assessment
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (member_id) REFERENCES team_members (id),
            UNIQUE(member_id, application)
        )
        ''')
        
        # Assignment history for ML learning
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS assignment_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            sr_id TEXT,
            application TEXT,
            area TEXT,
            assigned_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            complexity_score REAL,
            success_rate REAL, -- 1.0 = perfect, 0.0 = failed
            resolution_time_hours REAL,
            feedback_score REAL, -- Customer/team feedback
            keywords TEXT, -- JSON array of matched keywords
            FOREIGN KEY (member_id) REFERENCES team_members (id)
        )
        ''')
        
        # Skill evolution tracking
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS skill_evolution (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            application TEXT,
            old_skill_level REAL,
            new_skill_level REAL,
            change_reason TEXT,
            ml_confidence REAL,
            updated_by TEXT, -- 'ML' or 'USER' or 'ADMIN'
            update_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (member_id) REFERENCES team_members (id)
        )
        ''')
        
        # Configuration changes log
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS config_changes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            change_type TEXT, -- 'SKILL_UPDATE', 'LOAD_CHANGE', 'SPECIALIZATION_ADD'
            member_id INTEGER,
            field_name TEXT,
            old_value TEXT,
            new_value TEXT,
            changed_by TEXT, -- 'CHATBOT', 'ML', 'ADMIN'
            change_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (member_id) REFERENCES team_members (id)
        )
        ''')
        
        # Availability tracking table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS availability_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER NOT NULL,
            availability_percent INTEGER NOT NULL CHECK(availability_percent >= 0 AND availability_percent <= 100),
            availability_type TEXT DEFAULT 'full_day', -- 'full_day', 'half_day', 'unavailable', 'custom'
            reason TEXT, -- Reason for availability change
            start_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            end_date DATETIME, -- NULL means indefinite
            updated_by TEXT DEFAULT 'ADMIN',
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (member_id) REFERENCES team_members (id)
        )
        ''')
        
        conn.commit()
        conn.close()
        
        # Check and upgrade schema if needed
        self._upgrade_schema_if_needed()
        
        self.logger.info("Database initialized successfully")
    
    def _upgrade_schema_if_needed(self):
        """Upgrade database schema to add unique constraints if needed"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if skills table has the unique constraint
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='skills'")
            result = cursor.fetchone()
            
            if result and 'UNIQUE(member_id, application)' not in result[0]:
                print("[TOOL] Upgrading skills table schema to add unique constraint...")
                
                # First, clean up any duplicate records
                self._cleanup_duplicate_skills()
                
                # Create new table with unique constraint
                cursor.execute('''
                CREATE TABLE skills_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id INTEGER NOT NULL,
                    application TEXT NOT NULL,
                    skill_level REAL NOT NULL CHECK(skill_level >= 1.0 AND skill_level <= 5.0),
                    specializations TEXT,
                    max_load INTEGER NOT NULL DEFAULT 10,
                    confidence_score REAL DEFAULT 0.5,
                    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (member_id) REFERENCES team_members (id),
                    UNIQUE(member_id, application)
                )
                ''')
                
                # Copy data from old table (this will fail if there are still duplicates)
                cursor.execute('''
                INSERT INTO skills_new (member_id, application, skill_level, specializations, 
                                       max_load, confidence_score, last_updated)
                SELECT member_id, application, skill_level, specializations, 
                       max_load, confidence_score, last_updated
                FROM skills
                GROUP BY member_id, application
                HAVING id = MAX(id)
                ''')
                
                # Drop old table and rename new one
                cursor.execute('DROP TABLE skills')
                cursor.execute('ALTER TABLE skills_new RENAME TO skills')
                
                conn.commit()
                print("[OK] Schema upgrade completed successfully")
            else:
                print("[OK] Skills table schema is already up to date")
            
            conn.close()
            
        except Exception as e:
            print(f"[WARNING] Schema upgrade error: {str(e)}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
    
    def _cleanup_duplicate_skills(self):
        """Clean up duplicate (member_id, application) records, keeping the latest"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Find duplicates
            cursor.execute('''
                SELECT member_id, application, COUNT(*) as count
                FROM skills
                GROUP BY member_id, application
                HAVING COUNT(*) > 1
            ''')
            duplicates = cursor.fetchall()
            
            if duplicates:
                print(f"[CLEAN] Cleaning up {len(duplicates)} duplicate skill combinations...")
                
                deleted_count = 0
                for member_id, application, count in duplicates:
                    # Keep only the record with the highest ID (most recent)
                    cursor.execute('''
                        DELETE FROM skills 
                        WHERE member_id = ? AND application = ? 
                        AND id NOT IN (
                            SELECT MAX(id) 
                            FROM skills 
                            WHERE member_id = ? AND application = ?
                        )
                    ''', (member_id, application, member_id, application))
                    
                    deleted_count += cursor.rowcount
                
                conn.commit()
                print(f"[OK] Cleaned up {deleted_count} duplicate records")
            else:
                print("[OK] No duplicate records found")
            
            conn.close()
            
        except Exception as e:
            print(f"[ERROR] Error cleaning duplicates: {str(e)}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
    
    def make_member_id_unique_only(self):
        """Alternative method: Make member_id unique (one skill record per member total)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            print("[WARNING] WARNING: This will keep only ONE skill record per member!")
            print("Each member will lose skills in other applications.")
            
            # Create new table with member_id unique
            cursor.execute('''
            CREATE TABLE skills_unique_member (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER UNIQUE NOT NULL,
                application TEXT NOT NULL,
                skill_level REAL NOT NULL CHECK(skill_level >= 1.0 AND skill_level <= 5.0),
                specializations TEXT,
                max_load INTEGER NOT NULL DEFAULT 10,
                confidence_score REAL DEFAULT 0.5,
                last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (member_id) REFERENCES team_members (id)
            )
            ''')
            
            # Insert only one record per member (the latest one)
            cursor.execute('''
            INSERT INTO skills_unique_member (member_id, application, skill_level, specializations, 
                                            max_load, confidence_score, last_updated)
            SELECT member_id, application, skill_level, specializations, 
                   max_load, confidence_score, last_updated
            FROM skills s1
            WHERE s1.id = (
                SELECT MAX(s2.id) 
                FROM skills s2 
                WHERE s2.member_id = s1.member_id
            )
            ''')
            
            records_kept = cursor.rowcount
            
            # Replace old table
            cursor.execute('DROP TABLE skills')
            cursor.execute('ALTER TABLE skills_unique_member RENAME TO skills')
            
            conn.commit()
            conn.close()
            
            print(f"[OK] Member ID made unique. Kept {records_kept} records (one per member)")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error making member_id unique: {str(e)}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            return False
    
    def _get_current_skills_schema(self) -> List[str]:
        """Get current column names from skills table"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("PRAGMA table_info(skills)")
            schema_info = cursor.fetchall()
            conn.close()
            
            # Extract column names (index 1 in PRAGMA result)
            columns = [col[1] for col in schema_info]
            return columns
            
        except Exception as e:
            print(f"[WARNING] Error getting skills table schema: {str(e)}")
            return []
    
    def _detect_new_columns(self, excel_df: pd.DataFrame) -> List[Tuple[str, str]]:
        """Detect new columns in Excel that don't exist in skills table"""
        print("[INFO] Detecting new columns in People.xlsx...")
        
        # Standard column mappings (Excel column -> DB column)
        standard_mappings = {
            'Team Member': 'member_name',  # handled separately
            'Skill Level': 'skill_level',
            'App': 'application', 
            'Specialization': 'specializations',
            'Max Load': 'max_load'
        }
        
        # Get current skills table schema
        current_columns = self._get_current_skills_schema()
        print(f"   [DATA] Current skills table columns: {current_columns}")
        
        # Get Excel columns
        excel_columns = list(excel_df.columns)
        print(f"   [LIST] People.xlsx columns: {excel_columns}")
        
        # Find new columns
        new_columns = []
        for excel_col in excel_columns:
            # Skip standard columns we already handle
            if excel_col in standard_mappings:
                continue
                
            # Convert Excel column name to database column name
            db_col_name = excel_col.lower().replace(' ', '_').replace('-', '_')
            
            # Check if this column exists in skills table
            if db_col_name not in current_columns:
                new_columns.append((excel_col, db_col_name))
                print(f"   [NEW] New column detected: '{excel_col}' -> '{db_col_name}'")
        
        if not new_columns:
            print("   [OK] No new columns detected")
        else:
            print(f"   [TARGET] Found {len(new_columns)} new column(s) to add")
        
        return new_columns
    
    def _remove_columns_from_skills_table(self, columns_to_remove: List[str]) -> bool:
        """
        Remove specified columns from skills table
        SQLite doesn't support DROP COLUMN directly, so we recreate the table
        """
        if not columns_to_remove:
            return True
        
        print(f"[DELETE] Removing {len(columns_to_remove)} column(s) from skills table...")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current schema
            cursor.execute("PRAGMA table_info(skills)")
            current_schema = cursor.fetchall()
            
            # Build new schema excluding columns to remove
            columns_to_keep = []
            for col_info in current_schema:
                col_name = col_info[1]
                col_type = col_info[2]
                col_constraints = col_info[5]  # Primary key flag
                
                if col_name not in columns_to_remove:
                    if col_constraints == 1:  # Primary key
                        columns_to_keep.append(f"{col_name} {col_type} PRIMARY KEY AUTOINCREMENT")
                    else:
                        # Add constraints for known columns
                        if col_name == 'skill_level':
                            columns_to_keep.append(f"{col_name} {col_type} NOT NULL CHECK(skill_level >= 1.0 AND skill_level <= 5.0)")
                        elif col_name == 'member_id':
                            columns_to_keep.append(f"{col_name} {col_type} NOT NULL")
                        elif col_name == 'application':
                            columns_to_keep.append(f"{col_name} {col_type} NOT NULL")
                        elif col_name == 'max_load':
                            columns_to_keep.append(f"{col_name} {col_type} NOT NULL DEFAULT 10")
                        elif col_name == 'confidence_score':
                            columns_to_keep.append(f"{col_name} {col_type} DEFAULT 0.5")
                        elif col_name == 'last_updated':
                            columns_to_keep.append(f"{col_name} {col_type} DEFAULT CURRENT_TIMESTAMP")
                        else:
                            columns_to_keep.append(f"{col_name} {col_type}")
                else:
                    print(f"   [DELETE] Removing column: {col_name}")
            
            # Create new table schema
            new_schema = ',\n            '.join(columns_to_keep)
            
            # Step 1: Create backup table with new schema
            create_new_table_sql = f'''
            CREATE TABLE skills_new (
                {new_schema},
                FOREIGN KEY (member_id) REFERENCES team_members (id),
                UNIQUE(member_id, application)
            )
            '''
            
            cursor.execute(create_new_table_sql)
            print(f"   [OK] Created new table structure")
            
            # Step 2: Copy data (excluding removed columns)
            select_columns = [col_info[1] for col_info in current_schema if col_info[1] not in columns_to_remove]
            select_columns_str = ', '.join(select_columns)
            
            copy_data_sql = f'''
            INSERT INTO skills_new ({select_columns_str})
            SELECT {select_columns_str} FROM skills
            '''
            
            cursor.execute(copy_data_sql)
            print(f"   [OK] Copied data to new table")
            
            # Step 3: Drop old table and rename new table
            cursor.execute("DROP TABLE skills")
            cursor.execute("ALTER TABLE skills_new RENAME TO skills")
            print(f"   [OK] Replaced old table with new structure")
            
            conn.commit()
            conn.close()
            
            print("[OK] Column removal completed successfully")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error removing columns from skills table: {str(e)}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            return False
    
    def _add_columns_to_skills_table(self, new_columns: List[Tuple[str, str]], excel_df: pd.DataFrame) -> bool:
        """Add new columns to skills table"""
        if not new_columns:
            return True
        
        print(f"[TOOL] Adding {len(new_columns)} new column(s) to skills table...")
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for excel_col, db_col in new_columns:
                # Determine data type based on Excel data
                sample_data = excel_df[excel_col].dropna()
                if len(sample_data) > 0:
                    sample_value = sample_data.iloc[0]
                    
                    # Determine SQLite data type
                    if isinstance(sample_value, (int, np.integer)):
                        data_type = "INTEGER"
                    elif isinstance(sample_value, (float, np.floating)):
                        data_type = "REAL"
                    else:
                        data_type = "TEXT"
                else:
                    data_type = "TEXT"  # Default
                
                # Add column to skills table
                alter_sql = f"ALTER TABLE skills ADD COLUMN {db_col} {data_type}"
                print(f"   [WRITE] Adding column: {db_col} ({data_type})")
                
                try:
                    cursor.execute(alter_sql)
                    print(f"   [OK] Successfully added column: {db_col}")
                except sqlite3.OperationalError as e:
                    if "duplicate column name" in str(e).lower():
                        print(f"   ️ Column {db_col} already exists")
                    else:
                        raise e
            
            conn.commit()
            conn.close()
            
            print("[OK] Schema update completed successfully")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error adding columns to skills table: {str(e)}")
            if 'conn' in locals():
                conn.rollback()
                conn.close()
            return False
    
    def remove_columns_from_skills_table(self, columns_to_remove: List[str]) -> bool:
        """
        Public method to remove specified columns from skills table
        """
        print(f"[START] Starting column removal from skills table")
        print("=" * 60)
        
        if not columns_to_remove:
            print("[WARNING] No columns specified for removal")
            return True
        
        print(f"[LIST] Columns to remove: {columns_to_remove}")
        
        # Verify columns exist before attempting removal
        current_columns = self._get_current_skills_schema()
        print(f"[DATA] Current skills table columns: {current_columns}")
        
        # Check which columns actually exist
        existing_columns_to_remove = []
        non_existing_columns = []
        
        for col in columns_to_remove:
            if col in current_columns:
                existing_columns_to_remove.append(col)
            else:
                non_existing_columns.append(col)
        
        if non_existing_columns:
            print(f"[WARNING] These columns don't exist and will be skipped: {non_existing_columns}")
        
        if not existing_columns_to_remove:
            print("[OK] No existing columns to remove")
            return True
        
        print(f"[TARGET] Will remove these existing columns: {existing_columns_to_remove}")
        
        # Perform the removal
        success = self._remove_columns_from_skills_table(existing_columns_to_remove)
        
        if success:
            print(f"\n[DATA] Updated skills table schema:")
            updated_columns = self._get_current_skills_schema()
            for col in updated_columns:
                print(f"    {col}")
            
            print(f"\n[SUCCESS] Successfully removed {len(existing_columns_to_remove)} column(s)!")
        
        return success
    
    def load_people_from_excel(self, excel_path: str = "People.xlsx") -> bool:
        """
        Enhanced method to load team data from People.xlsx into database
        Automatically detects new columns and updates schema accordingly
        NOW HANDLES DELETIONS: Removes records that exist in DB but not in Excel
        """
        try:
            print(f"[START] Enhanced People.xlsx Loading with Deletion Handling")
            print("=" * 70)
            
            # Load Excel file
            df = pd.read_excel(excel_path)
            print(f"[DATA] Loaded Excel file with {len(df)} rows and {len(df.columns)} columns")
            
            # Clean column names
            df.columns = df.columns.str.replace('\xa0', ' ').str.strip()
            
            # Detect new columns
            new_columns = self._detect_new_columns(df)
            
            # Update schema if needed
            if new_columns:
                schema_updated = self._add_columns_to_skills_table(new_columns, df)
                if not schema_updated:
                    print("[ERROR] Schema update failed, aborting data load")
                    return False
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # STEP 1: Handle deletions - find records in DB but not in Excel
            print(f"\n[INFO] Checking for records to delete...")
            
            # Get current records from database
            cursor.execute('''
                SELECT tm.name, s.application 
                FROM team_members tm 
                JOIN skills s ON tm.id = s.member_id 
                WHERE tm.status = 'active'
            ''')
            
            current_db_records = set((name, app) for name, app in cursor.fetchall())
            print(f"[DATA] Current database has {len(current_db_records)} records")
            
            # Get records from Excel file
            excel_records = set((row['Team Member'], row['App']) for _, row in df.iterrows())
            print(f"[DATA] Excel file has {len(excel_records)} records")
            
            # Find records to delete (in DB but not in Excel)
            records_to_delete = current_db_records - excel_records
            
            if records_to_delete:
                print(f"[DELETE] Found {len(records_to_delete)} records to DELETE:")
                deleted_count = 0
                
                for name, app in records_to_delete:
                    print(f"   [DELETE] Deleting: {name} - {app}")
                    
                    # Delete the skill record
                    cursor.execute('''
                        DELETE FROM skills 
                        WHERE member_id = (SELECT id FROM team_members WHERE name = ?) 
                        AND application = ?
                    ''', (name, app))
                    
                    deleted_count += cursor.rowcount
                    
                    # Check if this team member has any remaining skills
                    cursor.execute('''
                        SELECT COUNT(*) FROM skills s
                        JOIN team_members tm ON s.member_id = tm.id
                        WHERE tm.name = ?
                    ''', (name,))
                    
                    remaining_skills = cursor.fetchone()[0]
                    
                    # If no remaining skills, deactivate the team member
                    if remaining_skills == 0:
                        cursor.execute('''
                            UPDATE team_members 
                            SET status = 'inactive', updated_date = CURRENT_TIMESTAMP
                            WHERE name = ?
                        ''', (name,))
                        print(f"   [UPDATE] Deactivated team member: {name} (no remaining skills)")
                
                print(f"[OK] Deleted {deleted_count} obsolete skill records")
                
                # Special check for Smitesh Kadia - SQO_MM
                smitesh_sqo_deleted = ('Smitesh Kadia', 'SQO_MM') in records_to_delete
                if smitesh_sqo_deleted:
                    print(f"[TARGET] [OK] CONFIRMED: Smitesh Kadia - SQO_MM has been deleted from database")
                
            else:
                print(f"[OK] No records to delete - database is already in sync")
            
            print(f"\n[SAVE] Loading/updating data from Excel...")
            
            # Get updated schema for dynamic column handling
            current_columns = self._get_current_skills_schema()
            
            loaded_count = 0
            
            for _, row in df.iterrows():
                member_name = row['Team Member']
                skill_level_str = str(row['Skill Level'])
                application = row['App']
                specializations = row['Specialization']
                max_load = int(row['Max Load'])
                
                # Parse skill level (e.g., "3/5" -> 3.0)
                if '/' in skill_level_str:
                    skill_level = float(skill_level_str.split('/')[0])
                else:
                    try:
                        skill_level = float(skill_level_str)
                    except:
                        skill_level = 3.0  # Default
                
                # Insert or get team member
                cursor.execute('''
                INSERT OR IGNORE INTO team_members (name, employee_id, status)
                VALUES (?, ?, 'active')
                ''', (member_name, member_name.lower().replace(' ', '_'), ))
                
                cursor.execute('SELECT id FROM team_members WHERE name = ?', (member_name,))
                member_id = cursor.fetchone()[0]
                
                # Parse specializations
                spec_list = [s.strip() for s in specializations.split('/') if s.strip()]
                spec_json = json.dumps(spec_list)
                
                # Build dynamic INSERT statement for all columns
                columns_to_insert = ['member_id', 'application', 'skill_level', 'specializations', 'max_load', 'confidence_score']
                values_to_insert = [member_id, application, skill_level, spec_json, max_load, 0.8]
                
                # Map Excel columns to database columns and add ALL available columns
                excel_to_db_mapping = {
                    'Min Load': 'min_load'
                    # Removed: 'Priority Level', 'Experience Years', 'Certification' 
                    # Add other dynamic mappings here as needed
                }
                
                # Add all mappable columns that exist in both Excel and database
                for excel_col, db_col in excel_to_db_mapping.items():
                    if db_col in current_columns and excel_col in row.index:
                        columns_to_insert.append(db_col)
                        
                        # Handle different data types
                        value = row[excel_col]
                        if pd.isna(value):
                            values_to_insert.append(None)
                        elif isinstance(value, (int, float)):
                            values_to_insert.append(value)
                        else:
                            values_to_insert.append(str(value))
                
                # Also add any newly detected columns
                for excel_col, db_col in new_columns:
                    if db_col in current_columns and excel_col in row.index:
                        columns_to_insert.append(db_col)
                        
                        # Handle different data types
                        value = row[excel_col]
                        if pd.isna(value):
                            values_to_insert.append(None)
                        elif isinstance(value, (int, float)):
                            values_to_insert.append(value)
                        else:
                            values_to_insert.append(str(value))
                
                # Create dynamic SQL
                placeholders = ', '.join(['?' for _ in values_to_insert])
                columns_str = ', '.join(columns_to_insert)
                
                sql = f'''
                INSERT OR REPLACE INTO skills ({columns_str})
                VALUES ({placeholders})
                '''
                
                cursor.execute(sql, values_to_insert)
                loaded_count += 1
            
            conn.commit()
            conn.close()
            
            print(f"[OK] Successfully loaded {loaded_count} records from {excel_path}")
            
            # Show summary of what was loaded
            if new_columns:
                print(f"\n[LIST] New columns added and loaded:")
                for excel_col, db_col in new_columns:
                    print(f"    {excel_col} -> {db_col}")
            
            self.logger.info(f"Successfully loaded {loaded_count} records with enhanced schema from {excel_path}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error in enhanced People.xlsx loading: {str(e)}")
            self.logger.error(f"Error loading People.xlsx: {str(e)}")
            return False
    
    def get_team_configuration(self) -> Dict[str, Any]:
        """
        Get current team configuration with dynamic column support
        Automatically includes all columns from skills table
        """
        conn = sqlite3.connect(self.db_path)
        
        # Get all columns from skills table dynamically
        skill_columns = self._get_current_skills_schema()
        
        # Build dynamic query excluding certain columns
        excluded_columns = ['id', 'member_id']
        skill_cols_to_select = [f"s.{col}" for col in skill_columns if col not in excluded_columns]
        skill_cols_str = ', '.join(skill_cols_to_select)
        
        query = f'''
        SELECT tm.name, tm.status, {skill_cols_str}
        FROM team_members tm
        JOIN skills s ON tm.id = s.member_id
        WHERE tm.status = 'active'
        ORDER BY tm.name, s.application
        '''
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Convert to structured format
        config = {}
        for _, row in df.iterrows():
            member_name = row['name']
            if member_name not in config:
                config[member_name] = {
                    'status': row['status'],
                    'applications': {}
                }
            
            app = row['application']
            specializations = json.loads(row['specializations']) if row['specializations'] else []
            
            # Build skill data dynamically including all columns
            skill_data = {
                'skill_level': row['skill_level'],
                'specializations': specializations,
                'max_load': row['max_load'],
                'confidence_score': row['confidence_score'],
                'last_updated': row['last_updated']
            }
            
            # Add any additional dynamic columns
            for col in skill_columns:
                if col not in excluded_columns and col not in ['application', 'skill_level', 'specializations', 'max_load', 'confidence_score', 'last_updated']:
                    if col in row.index and pd.notna(row[col]):
                        skill_data[col] = row[col]
            
            config[member_name]['applications'][app] = skill_data
        
        return config
    
    def record_assignment(self, member_name: str, assignment_data: Dict[str, Any]) -> bool:
        """Record assignment for ML learning"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get member ID
            cursor.execute('SELECT id FROM team_members WHERE name = ?', (member_name,))
            result = cursor.fetchone()
            if not result:
                self.logger.warning(f"Member {member_name} not found")
                return False
            
            member_id = result[0]
            
            # Insert assignment record
            cursor.execute('''
            INSERT INTO assignment_history 
            (member_id, sr_id, application, area, complexity_score, 
             success_rate, resolution_time_hours, feedback_score, keywords)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                member_id,
                assignment_data.get('sr_id', ''),
                assignment_data.get('application', ''),
                assignment_data.get('area', ''),
                assignment_data.get('complexity_score', 0.5),
                assignment_data.get('success_rate', 1.0),
                assignment_data.get('resolution_time_hours', 0),
                assignment_data.get('feedback_score', 0.8),
                json.dumps(assignment_data.get('keywords', []))
            ))
            
            conn.commit()
            conn.close()
            
            # Trigger ML learning update
            self._update_skills_from_performance(member_name)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error recording assignment: {str(e)}")
            return False
    
    def _update_skills_from_performance(self, member_name: str):
        """Update skills based on performance using ML algorithms"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Get member ID
            cursor = conn.cursor()
            cursor.execute('SELECT id FROM team_members WHERE name = ?', (member_name,))
            member_id = cursor.fetchone()[0]
            
            # Get recent performance data (last 30 days)
            thirty_days_ago = datetime.now() - timedelta(days=30)
            
            query = '''
            SELECT application, AVG(success_rate) as avg_success, 
                   AVG(complexity_score) as avg_complexity,
                   COUNT(*) as assignment_count,
                   AVG(feedback_score) as avg_feedback
            FROM assignment_history 
            WHERE member_id = ? AND assigned_date >= ?
            GROUP BY application
            '''
            
            performance_df = pd.read_sql_query(query, conn, params=(member_id, thirty_days_ago))
            
            for _, perf in performance_df.iterrows():
                app = perf['application']
                avg_success = perf['avg_success']
                avg_complexity = perf['avg_complexity']
                assignment_count = perf['assignment_count']
                avg_feedback = perf['avg_feedback']
                
                # Get current skill level
                cursor.execute('''
                SELECT skill_level, confidence_score FROM skills 
                WHERE member_id = ? AND application = ?
                ''', (member_id, app))
                
                current_skill = cursor.fetchone()
                if not current_skill:
                    continue
                
                current_level, current_confidence = current_skill
                
                # ML Algorithm: Calculate new skill level
                new_skill_level = self._calculate_new_skill_level(
                    current_level, avg_success, avg_complexity, 
                    assignment_count, avg_feedback
                )
                
                # Calculate confidence based on data volume and consistency
                new_confidence = min(0.95, current_confidence + 
                                   (assignment_count * 0.02) + 
                                   (avg_success * 0.1))
                
                # Only update if significant change and high confidence
                if abs(new_skill_level - current_level) > 0.1 and new_confidence > 0.7:
                    
                    # Record skill evolution
                    cursor.execute('''
                    INSERT INTO skill_evolution 
                    (member_id, application, old_skill_level, new_skill_level, 
                     change_reason, ml_confidence, updated_by)
                    VALUES (?, ?, ?, ?, ?, ?, 'ML')
                    ''', (member_id, app, current_level, new_skill_level,
                          f"Performance-based update: success={avg_success:.2f}, complexity={avg_complexity:.2f}",
                          new_confidence))
                    
                    # Update skill level
                    cursor.execute('''
                    UPDATE skills 
                    SET skill_level = ?, confidence_score = ?, last_updated = CURRENT_TIMESTAMP
                    WHERE member_id = ? AND application = ?
                    ''', (new_skill_level, new_confidence, member_id, app))
                    
                    self.logger.info(f"ML updated {member_name} {app} skill: {current_level:.2f} -> {new_skill_level:.2f}")
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            self.logger.error(f"Error updating skills from performance: {str(e)}")
    
    def _calculate_new_skill_level(self, current_level: float, avg_success: float, 
                                 avg_complexity: float, assignment_count: int, 
                                 avg_feedback: float) -> float:
        """
        ML algorithm to calculate new skill level based on performance metrics
        """
        # Base adjustment from success rate
        success_factor = (avg_success - 0.8) * 2  # -1.6 to 0.4 range
        
        # Complexity handling bonus
        complexity_factor = min(avg_complexity / 0.8, 1.0) * 0.5  # 0 to 0.5 range
        
        # Experience bonus (more assignments = slight skill increase)
        experience_factor = min(assignment_count / 20, 0.3)  # 0 to 0.3 range
        
        # Feedback factor
        feedback_factor = (avg_feedback - 0.7) * 0.5  # -0.35 to 0.15 range
        
        # Calculate total adjustment
        total_adjustment = success_factor + complexity_factor + experience_factor + feedback_factor
        
        # Apply adjustment with learning rate
        learning_rate = 0.1  # Conservative learning
        new_level = current_level + (total_adjustment * learning_rate)
        
        # Clamp to valid range
        return max(1.0, min(5.0, new_level))
    
    def update_member_config_via_chat(self, member_name: str, updates: Dict[str, Any], 
                                    changed_by: str = "CHATBOT") -> bool:
        """Update member configuration via chatbot commands"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get member ID
            cursor.execute('SELECT id FROM team_members WHERE name = ?', (member_name,))
            result = cursor.fetchone()
            if not result:
                return False
            
            member_id = result[0]
            
            for field, new_value in updates.items():
                if field == 'skill_level':
                    app = updates.get('application', 'SOM_MM')
                    
                    # Get current value
                    cursor.execute('SELECT skill_level FROM skills WHERE member_id = ? AND application = ?', 
                                 (member_id, app))
                    old_value = cursor.fetchone()[0]
                    
                    # Update skill level
                    cursor.execute('''
                    UPDATE skills SET skill_level = ?, last_updated = CURRENT_TIMESTAMP
                    WHERE member_id = ? AND application = ?
                    ''', (new_value, member_id, app))
                    
                    # Log change
                    cursor.execute('''
                    INSERT INTO config_changes 
                    (change_type, member_id, field_name, old_value, new_value, changed_by)
                    VALUES ('SKILL_UPDATE', ?, ?, ?, ?, ?)
                    ''', (member_id, f"{app}_skill_level", str(old_value), str(new_value), changed_by))
                
                elif field == 'max_load':
                    app = updates.get('application', 'SOM_MM')
                    
                    cursor.execute('SELECT max_load FROM skills WHERE member_id = ? AND application = ?',
                                 (member_id, app))
                    old_value = cursor.fetchone()[0]
                    
                    cursor.execute('''
                    UPDATE skills SET max_load = ?, last_updated = CURRENT_TIMESTAMP
                    WHERE member_id = ? AND application = ?
                    ''', (new_value, member_id, app))
                    
                    cursor.execute('''
                    INSERT INTO config_changes 
                    (change_type, member_id, field_name, old_value, new_value, changed_by)
                    VALUES ('LOAD_CHANGE', ?, ?, ?, ?, ?)
                    ''', (member_id, f"{app}_max_load", str(old_value), str(new_value), changed_by))
                
                elif field == 'add_specialization':
                    app = updates.get('application', 'SOM_MM')
                    specialization = new_value
                    
                    # Get current specializations
                    cursor.execute('SELECT specializations FROM skills WHERE member_id = ? AND application = ?',
                                 (member_id, app))
                    current_specs = json.loads(cursor.fetchone()[0] or '[]')
                    
                    if specialization not in current_specs:
                        current_specs.append(specialization)
                        
                        cursor.execute('''
                        UPDATE skills SET specializations = ?, last_updated = CURRENT_TIMESTAMP
                        WHERE member_id = ? AND application = ?
                        ''', (json.dumps(current_specs), member_id, app))
                        
                        cursor.execute('''
                        INSERT INTO config_changes 
                        (change_type, member_id, field_name, old_value, new_value, changed_by)
                        VALUES ('SPECIALIZATION_ADD', ?, ?, ?, ?, ?)
                        ''', (member_id, f"{app}_specialization", '', specialization, changed_by))
            
            conn.commit()
            conn.close()
            
            # Also update People.xlsx file to maintain consistency
            excel_update_success = self._update_people_excel_file(member_name, updates)
            if not excel_update_success:
                print(f"[WARNING] Database updated but Excel update failed for {member_name}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating member config: {str(e)}")
            return False
    
    def _update_people_excel_file(self, member_name: str, updates: Dict[str, Any], 
                                 excel_path: str = "People.xlsx") -> bool:
        """Update People.xlsx file with chat command changes"""
        try:
            import os
            import shutil
            from datetime import datetime
            
            # Check if file exists
            if not os.path.exists(excel_path):
                print(f"[WARNING] Excel file {excel_path} not found for update")
                return False
            
            # Read the Excel file
            df = pd.read_excel(excel_path)
            
            # Clean column names (in case of encoding issues)
            df.columns = df.columns.str.replace('\xa0', ' ').str.strip()
            
            # Track updates made
            updated_rows = 0
            
            # Process each update field
            for field, new_value in updates.items():
                if field in ['skill_level', 'max_load']:
                    app = updates.get('application', 'SOM_MM')
                    
                    # Find rows matching member name and application
                    mask = (df['Team Member'] == member_name) & (df['App'] == app)
                    matching_rows = df[mask]
                    
                    if len(matching_rows) == 0:
                        print(f"[WARNING] No matching row found in Excel for {member_name} {app}")
                        continue
                    
                    if field == 'skill_level':
                        # Update skill level (format as X.X/5)
                        for idx in matching_rows.index:
                            old_skill = df.loc[idx, 'Skill Level']
                            df.loc[idx, 'Skill Level'] = f"{new_value:.1f}/5"
                            updated_rows += 1
                            print(f"[OK] Updated {member_name} {app} skill level: {old_skill}  {new_value:.1f}/5")
                    
                    elif field == 'max_load':
                        # Update max load
                        for idx in matching_rows.index:
                            old_load = df.loc[idx, 'Max Load']
                            df.loc[idx, 'Max Load'] = new_value
                            updated_rows += 1
                            print(f"[OK] Updated {member_name} {app} max load: {old_load}  {new_value}")
            
            if updated_rows > 0:
                # Create backup of original file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"People_backup_{timestamp}.xlsx"
                shutil.copy2(excel_path, backup_path)
                print(f"[FILE] Created backup: {backup_path}")
                
                # Save updated file
                df.to_excel(excel_path, index=False)
                print(f"[SAVE] Updated {excel_path} with {updated_rows} changes")
                
                # Cleanup old backups using enhanced method (keep only latest 1)
                self.cleanup_people_backups(keep_count=1)
                
                return True
            else:
                print("️ No updates were needed in Excel file")
                return True
                
        except Exception as e:
            print(f"[ERROR] Error updating Excel file: {str(e)}")
            return False
    
    def _cleanup_old_backups(self, pattern: str, keep_count: int = 3):
        """Clean up old backup files, keeping only the most recent ones"""
        try:
            import glob
            import os
            
            # Find all backup files matching pattern
            backup_files = glob.glob(pattern)
            
            if len(backup_files) > keep_count:
                # Sort by creation time (newest first)
                backup_files.sort(key=os.path.getctime, reverse=True)
                
                # Keep only the newest ones, delete the rest
                files_to_delete = backup_files[keep_count:]
                
                for file_path in files_to_delete:
                    try:
                        os.remove(file_path)
                        print(f"[DELETE] Deleted old backup: {file_path}")
                    except Exception as e:
                        print(f"[WARNING] Could not delete {file_path}: {str(e)}")
        
        except Exception as e:
            print(f"[WARNING] Error during backup cleanup: {str(e)}")
    
    def cleanup_people_backups(self, keep_count: int = 1):
        """Enhanced cleanup specifically for People_backup*.xlsx files"""
        try:
            import glob
            import os
            import re
            from datetime import datetime
            
            print(f"[CLEAN] Cleaning up People backup files (keeping latest {keep_count})...")
            
            # Find all People backup files
            backup_pattern = "People_backup_*.xlsx"
            backup_files = glob.glob(backup_pattern)
            
            if len(backup_files) <= keep_count:
                print(f"   ️ Found {len(backup_files)} backup files, no cleanup needed")
                return True
            
            print(f"   [DATA] Found {len(backup_files)} backup files")
            
            # Enhanced sorting: Extract timestamp from filename for reliable ordering
            def extract_timestamp(filename):
                """Extract timestamp from People_backup_YYYYMMDD_HHMMSS.xlsx format"""
                try:
                    # Use regex to extract the timestamp part
                    match = re.search(r'People_backup_(\d{8}_\d{6})\.xlsx', filename)
                    if match:
                        timestamp_str = match.group(1)
                        # Parse the timestamp: YYYYMMDD_HHMMSS
                        return datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                    else:
                        # Fallback to file creation time if pattern doesn't match
                        return datetime.fromtimestamp(os.path.getctime(filename))
                except Exception:
                    # Final fallback to current time (will be deleted as oldest)
                    return datetime.min
            
            # Sort by timestamp extracted from filename (newest first)
            backup_files.sort(key=extract_timestamp, reverse=True)
            
            # Show current backups in order
            print("   [LIST] Current backups (newest first):")
            for i, file_path in enumerate(backup_files):
                timestamp = extract_timestamp(file_path)
                status = "KEEP" if i < keep_count else "DELETE"
                print(f"      {i+1}. {file_path} ({timestamp.strftime('%Y-%m-%d %H:%M:%S')}) - {status}")
            
            # Keep only the newest files, delete the rest
            files_to_delete = backup_files[keep_count:]
            
            deleted_count = 0
            for file_path in files_to_delete:
                try:
                    os.remove(file_path)
                    print(f"   [DELETE] Deleted: {file_path}")
                    deleted_count += 1
                except OSError as e:
                    if e.errno == 32:  # File is being used by another process
                        print(f"   [WARNING] Cannot delete {file_path}: File is in use (Excel may be open)")
                    else:
                        print(f"   [WARNING] Cannot delete {file_path}: {str(e)}")
                except Exception as e:
                    print(f"   [ERROR] Error deleting {file_path}: {str(e)}")
            
            kept_files = backup_files[:keep_count]
            print(f"   [OK] Cleanup complete: Kept {len(kept_files)} file(s), deleted {deleted_count} file(s)")
            
            if kept_files:
                print(f"   [FILE] Latest backup: {kept_files[0]}")
            
            return True
            
        except Exception as e:
            print(f"[ERROR] Error during People backup cleanup: {str(e)}")
            return False
    
    def cleanup_all_people_backups_to_latest(self):
        """Utility method to clean up all People backups keeping only the very latest one"""
        print("[START] Enhanced People Backup Cleanup - Keep Only Latest")
        print("=" * 55)
        return self.cleanup_people_backups(keep_count=1)
    
    def get_skill_evolution_report(self, member_name: str = None, days: int = 30) -> Dict[str, Any]:
        """Get skill evolution report for analysis"""
        conn = sqlite3.connect(self.db_path)
        
        where_clause = ""
        params = [datetime.now() - timedelta(days=days)]
        
        if member_name:
            where_clause = "AND tm.name = ?"
            params.append(member_name)
        
        query = f'''
        SELECT tm.name, se.application, se.old_skill_level, se.new_skill_level,
               se.change_reason, se.ml_confidence, se.updated_by, se.update_date
        FROM skill_evolution se
        JOIN team_members tm ON se.member_id = tm.id
        WHERE se.update_date >= ? {where_clause}
        ORDER BY se.update_date DESC
        '''
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        if df.empty:
            return {'total_changes': 0, 'changes': []}
        
        changes = []
        for _, row in df.iterrows():
            changes.append({
                'member': row['name'],
                'application': row['application'],
                'old_level': row['old_skill_level'],
                'new_level': row['new_skill_level'],
                'change': row['new_skill_level'] - row['old_skill_level'],
                'reason': row['change_reason'],
                'confidence': row['ml_confidence'],
                'updated_by': row['updated_by'],
                'date': row['update_date']
            })
        
        return {
            'total_changes': len(changes),
            'changes': changes,
            'summary': {
                'ml_updates': len([c for c in changes if c['updated_by'] == 'ML']),
                'user_updates': len([c for c in changes if c['updated_by'] in ['USER', 'CHATBOT']]),
                'avg_confidence': np.mean([c['confidence'] for c in changes if c['confidence']])
            }
        }
    
    def export_current_config_to_excel(self, output_path: str = "current_team_config.xlsx") -> bool:
        """Export current configuration to Excel format"""
        try:
            config = self.get_team_configuration()
            
            records = []
            for member_name, member_data in config.items():
                for app, app_data in member_data['applications'].items():
                    records.append({
                        'Team Member': member_name,
                        'Skill Level': f"{app_data['skill_level']:.1f}/5",
                        'App': app,
                        'Specialization': '/'.join(app_data['specializations']),
                        'Max Load': app_data['max_load'],
                        'Confidence Score': f"{app_data['confidence_score']:.2f}",
                        'Last Updated': app_data['last_updated']
                    })
            
            df = pd.DataFrame(records)
            df.to_excel(output_path, index=False)
            
            self.logger.info(f"Configuration exported to {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error exporting config: {str(e)}")
            return False
    
    def get_top_experts(self, application: str, top_n: int = 3) -> List[int]:
        """
        Get top N team members by skill level for given application
        Used for priority SR assignment (P0, P1, P2 get expert attention)
        
        Args:
            application: Application area (SOM_MM, SQO_MM, BILLING_MM)
            top_n: Number of top experts to return (default: 3)
            
        Returns:
            List of member IDs sorted by skill level (highest first)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = """
            SELECT s.member_id, tm.name, s.skill_level 
            FROM skills s
            JOIN team_members tm ON s.member_id = tm.id
            WHERE s.application = ? AND s.skill_level >= 4.0 AND tm.status = 'active'
            ORDER BY s.skill_level DESC, s.confidence_score DESC
            LIMIT ?
            """
            
            cursor = conn.cursor()
            cursor.execute(query, (application, top_n))
            results = cursor.fetchall()
            conn.close()
            
            if results:
                expert_ids = [row[0] for row in results]
                expert_names = [row[1] for row in results]
                expert_levels = [row[2] for row in results]
                
                self.logger.info(f"Found {len(expert_ids)} experts for {application}: {expert_names} (levels: {expert_levels})")
                return expert_ids
            else:
                self.logger.warning(f"No experts found for {application} with skill >= 4.0")
                return []
                
        except Exception as e:
            self.logger.error(f"Error getting top experts: {str(e)}")
            return []
    
    def get_all_member_names(self) -> List[str]:
        """
        Get all active team member names
        Used for extracting existing assignees from notes/comments
        
        Returns:
            List of team member names
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = """
            SELECT name 
            FROM team_members 
            WHERE status = 'active'
            ORDER BY name
            """
            
            cursor = conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            conn.close()
            
            return [row[0] for row in results]
            
        except Exception as e:
            self.logger.error(f"Error getting member names: {str(e)}")
            return []
    
    def get_all_people(self) -> List[Dict[str, Any]]:
        """
        Get all active team members with their current availability and skill levels
        
        Returns:
            List of dicts with member info including availability
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all active team members
            cursor.execute('''
                SELECT DISTINCT tm.name, tm.status
                FROM team_members tm
                WHERE tm.status = 'active'
            ''')
            
            members = []
            for row in cursor.fetchall():
                name = row[0]
                
                # Get current availability (from latest availability record or default to 100%)
                try:
                    cursor.execute('''
                        SELECT availability_percent 
                        FROM availability_history 
                        WHERE member_id = (SELECT id FROM team_members WHERE name = ?)
                        ORDER BY updated_at DESC
                        LIMIT 1
                    ''', (name,))
                    
                    avail_result = cursor.fetchone()
                    availability = avail_result[0] if avail_result else 100
                except sqlite3.OperationalError:
                    # Table doesn't exist yet - default to 100% availability
                    availability = 100
                
                # Get ALL applications this person has expertise in
                cursor.execute('''
                    SELECT skill_level, application
                    FROM skills
                    WHERE member_id = (SELECT id FROM team_members WHERE name = ?)
                    ORDER BY skill_level DESC
                ''', (name,))
                
                skills_results = cursor.fetchall()
                
                if skills_results:
                    # Get highest skill level
                    highest_skill = max([s[0] for s in skills_results])
                    if highest_skill >= 4.5:
                        skill_level = 'Expert'
                    elif highest_skill >= 3.5:
                        skill_level = 'Advanced'
                    elif highest_skill >= 2.5:
                        skill_level = 'Intermediate'
                    else:
                        skill_level = 'Fresher'
                    
                    # Get all applications (comma-separated for primary, but also keep list)
                    applications = [s[1] for s in skills_results]
                    primary_app = applications[0] if applications else 'SOM_MM'
                else:
                    skill_level = 'Intermediate'
                    applications = ['SOM_MM']
                    primary_app = 'SOM_MM'
                
                members.append({
                    'name': name,
                    'status': row[1],
                    'current_availability': availability,
                    'skill_level': skill_level,
                    'application': primary_app,  # For backwards compatibility
                    'applications': applications  # List of ALL apps this person can handle
                })
            
            conn.close()
            return members
            
        except Exception as e:
            self.logger.error(f"Error getting all people: {e}")
            return []
    
    def get_member_id_by_name(self, member_name: str) -> Optional[int]:
        """
        Get member ID by name (case-insensitive)
        
        Args:
            member_name: Team member name
            
        Returns:
            Member ID or None if not found
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            query = """
            SELECT id 
            FROM team_members 
            WHERE LOWER(name) = LOWER(?) AND status = 'active'
            """
            
            cursor = conn.cursor()
            cursor.execute(query, (member_name,))
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else None
            
        except Exception as e:
            self.logger.error(f"Error getting member ID: {str(e)}")
            return None
    
    def set_member_availability(self, member_name: str, availability_percent: int, 
                               availability_type: str = 'full_day', reason: str = '', 
                               end_date: Optional[str] = None, updated_by: str = 'ADMIN') -> bool:
        """
        Set member availability percentage
        
        Args:
            member_name: Team member name
            availability_percent: 0-100 (0 = unavailable, 50 = half day, 100 = full day)
            availability_type: 'full_day', 'half_day', 'unavailable', 'custom'
            reason: Reason for availability change
            end_date: End date for temporary availability (None = permanent)
            updated_by: Who updated the availability
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get member ID
            member_id = self.get_member_id_by_name(member_name)
            if not member_id:
                self.logger.error(f"Member {member_name} not found")
                return False
            
            # Insert availability record
            cursor.execute('''
                INSERT INTO availability_history 
                (member_id, availability_percent, availability_type, reason, end_date, updated_by)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (member_id, availability_percent, availability_type, reason, end_date, updated_by))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Set availability for {member_name}: {availability_percent}% ({availability_type})")
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting availability: {str(e)}")
            return False
    
    def get_member_availability(self, member_name: str) -> Dict[str, Any]:
        """
        Get current availability for a member
        
        Args:
            member_name: Team member name
            
        Returns:
            Dict with availability info or default 100% if not set
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            member_id = self.get_member_id_by_name(member_name)
            if not member_id:
                return {'availability_percent': 100, 'availability_type': 'full_day', 'reason': ''}
            
            # Get latest availability record that is still active
            cursor.execute('''
                SELECT availability_percent, availability_type, reason, start_date, end_date
                FROM availability_history
                WHERE member_id = ? AND (end_date IS NULL OR end_date >= datetime('now'))
                ORDER BY updated_at DESC
                LIMIT 1
            ''', (member_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'availability_percent': result[0],
                    'availability_type': result[1],
                    'reason': result[2] or '',
                    'start_date': result[3],
                    'end_date': result[4]
                }
            else:
                return {'availability_percent': 100, 'availability_type': 'full_day', 'reason': ''}
            
        except Exception as e:
            self.logger.error(f"Error getting availability: {str(e)}")
            return {'availability_percent': 100, 'availability_type': 'full_day', 'reason': ''}
    
    def get_all_members_availability(self) -> List[Dict[str, Any]]:
        """
        Get availability for all active members
        
        Returns:
            List of dicts with member name and availability info
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all active members with their latest availability
            cursor.execute('''
                SELECT tm.name, tm.id
                FROM team_members tm
                WHERE tm.status = 'active'
                ORDER BY tm.name
            ''')
            
            members = []
            for row in cursor.fetchall():
                name = row[0]
                member_id = row[1]
                
                # Get latest availability
                cursor.execute('''
                    SELECT availability_percent, availability_type, reason, start_date, end_date
                    FROM availability_history
                    WHERE member_id = ? AND (end_date IS NULL OR end_date >= datetime('now'))
                    ORDER BY updated_at DESC
                    LIMIT 1
                ''', (member_id,))
                
                avail_result = cursor.fetchone()
                
                if avail_result:
                    members.append({
                        'name': name,
                        'availability_percent': avail_result[0],
                        'availability_type': avail_result[1],
                        'reason': avail_result[2] or '',
                        'start_date': avail_result[3],
                        'end_date': avail_result[4]
                    })
                else:
                    # Default to 100% if not set
                    members.append({
                        'name': name,
                        'availability_percent': 100,
                        'availability_type': 'full_day',
                        'reason': '',
                        'start_date': None,
                        'end_date': None
                    })
            
            conn.close()
            return members
            
        except Exception as e:
            self.logger.error(f"Error getting all members availability: {str(e)}")
            return []

def demo_people_skills_database():
    """Demonstrate the people skills database system"""
    print("[STORAGE] People Skills Database Demo")
    print("=" * 60)
    
    # Initialize database
    db = PeopleSkillsDatabase()
    
    # Load from Excel
    print("[DATA] Loading People.xlsx...")
    success = db.load_people_from_excel()
    print(f"[OK] Load successful: {success}")
    
    # Get current configuration
    print("\n[TEAM] Current Team Configuration:")
    config = db.get_team_configuration()
    for member, data in list(config.items())[:2]:  # Show first 2 members
        print(f"\n{member}:")
        for app, app_data in data['applications'].items():
            print(f"  {app}: Level {app_data['skill_level']}, Load {app_data['max_load']}")
            print(f"    Specializations: {app_data['specializations'][:3]}...")  # First 3
    
    # Simulate assignment recording
    print("\n[WRITE] Recording sample assignment...")
    assignment_data = {
        'sr_id': 'SR001',
        'application': 'SOM_MM',
        'area': 'Provisioning',
        'complexity_score': 0.7,
        'success_rate': 0.9,
        'resolution_time_hours': 2.5,
        'feedback_score': 0.85,
        'keywords': ['EVC', 'Bandwidth', 'Activation']
    }
    
    db.record_assignment('Prateek Jain', assignment_data)
    print("[OK] Assignment recorded and ML learning triggered")
    
    # Simulate chatbot config update
    print("\n[CHAT] Simulating chatbot configuration update...")
    updates = {
        'application': 'SOM_MM',
        'skill_level': 4.8,
        'max_load': 16
    }
    
    success = db.update_member_config_via_chat('Prateek Jain', updates)
    print(f"[OK] Config update successful: {success}")
    
    # Get skill evolution report
    print("\n[CHART] Skill Evolution Report:")
    evolution = db.get_skill_evolution_report(days=7)
    print(f"Total changes in last 7 days: {evolution['total_changes']}")
    if evolution['total_changes'] > 0:
        print(f"ML updates: {evolution['summary']['ml_updates']}")
        print(f"User updates: {evolution['summary']['user_updates']}")
    else:
        print("No recent changes - ready for learning from new data")
    
    # Export updated config
    print("\n Exporting updated configuration...")
    db.export_current_config_to_excel("updated_team_config.xlsx")
    print("[OK] Export complete")

if __name__ == "__main__":
    demo_people_skills_database()
