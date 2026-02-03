#!/usr/bin/env python3
"""
OSO Activity Data - Average Time Calculator
============================================
Reads spec_ver_id values from CSV, queries the database for average execution time,
and updates the CSV with Avg Time and Maximum Time values.

Author: Jupitoverse
Date: 2025
"""

import os
import sys
import logging
from datetime import datetime
import pandas as pd
import psycopg2

# =============================================================================
# CONFIGURATION
# =============================================================================

# File paths (Amdocs Server)
INPUT_CSV_PATH = "/fs_ogs/operogs/scriptbin/ogs_monitors/Jupitoverse/OSO Activity Data/OSO_activity_data.csv"
OUTPUT_CSV_PATH = "/fs_ogs/operogs/scriptbin/ogs_monitors/Jupitoverse/OSO Activity Data/OSO_activity_data.csv"
LOG_DIR = "/fs_ogs/operogs/scriptbin/ogs_monitors/Jupitoverse/OSO Activity Data/logs"

# Column names
ID_COLUMN = "spec_ver_id"
AVG_TIME_COLUMN = "Avg Time"
MAX_TIME_COLUMN = "Maximun Time"
REEXEC_COLUMN = "Reexecution Allowed"
BILLING_COLUMN = "Billing impacting"
DESC_COLUMN = "Discription"

# Process a subset (1-based, inclusive). Set both to None to process all rows.
START_ROW = 1   # e.g., 1
END_ROW   = 6   # e.g., 500

# Database configuration
DB_CONFIG = {
    "database": "prodossdb",
    "user": "ossdb01uams",
    "password": "Pr0d_ossdb01uams",
    "host": "oso-pstgr-rd.orion.comcast.com",
    "port": "6432"
}

# Schema where oss_activity_instance table exists (e.g., "oss", "ossdb", "public")
# Set to None to use default search_path, or specify schema name
DB_SCHEMA = "ossdb01db"  # <-- Change this to the correct schema name

# Query timeout in seconds (5 minutes)
QUERY_TIMEOUT_SECONDS = 300

# Part ID configuration for sliding window
PART_ID_START = 1       # Starting part_id
PART_ID_STEP = 5        # Interval size (e.g., 1-5, 6-10, 11-15)
PART_ID_MAX = 30        # Maximum part_id to try (stops sliding after this)

# =============================================================================
# LOGGING SETUP
# =============================================================================

def setup_logging():
    """Configure logging to both file and console."""
    # Create log directory if it doesn't exist
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)
    
    # Log file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_DIR, f"oso_activity_{timestamp}.log")
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__), log_file


def cleanup_logs(log_file, logger):
    """Remove log file and clean up log directory after successful execution."""
    try:
        # Close all logging handlers to release file handles
        for handler in logging.root.handlers[:]:
            handler.close()
            logging.root.removeHandler(handler)
        
        # Delete the current log file
        if os.path.exists(log_file):
            os.remove(log_file)
            print(f"Log file cleaned up: {log_file}")
        
        # Remove log directory if empty
        if os.path.exists(LOG_DIR) and not os.listdir(LOG_DIR):
            os.rmdir(LOG_DIR)
            print(f"Empty log directory removed: {LOG_DIR}")
            
    except Exception as e:
        print(f"Warning: Could not clean up logs: {str(e)}")


# =============================================================================
# SQL QUERY
# =============================================================================

def get_query_template(part_ids):
    """Generate query with specific part_id range."""
    part_id_list = ','.join(map(str, part_ids))
    return f"""
WITH latest AS (
    SELECT
        oai.actual_start_date,
        oai.actual_end_date
    FROM ossdb01db.oss_activity_instance AS oai
    WHERE oai.spec_ver_id = %s
      AND oai.state = 'Completed'
      AND oai.prev_state = 'In Progress'
      AND oai.part_id IN ({part_id_list})
    ORDER BY oai.create_date DESC
    LIMIT 30
),
durations AS (
    SELECT EXTRACT(EPOCH FROM (actual_end_date - actual_start_date)) / 60.0 AS minutes
    FROM latest
    WHERE actual_start_date IS NOT NULL
      AND actual_end_date IS NOT NULL
      AND actual_end_date > actual_start_date
),
bounds AS (
    SELECT
        percentile_disc(0.05) WITHIN GROUP (ORDER BY minutes) AS p5,
        percentile_disc(0.95) WITHIN GROUP (ORDER BY minutes) AS p95
    FROM durations
)
SELECT ROUND(AVG(d.minutes)::numeric, 2) AS avg_minutes
FROM durations d
CROSS JOIN bounds b
WHERE d.minutes BETWEEN b.p5 AND b.p95;
"""


# =============================================================================
# FUNCTIONS
# =============================================================================

def load_csv(file_path, logger):
    """Load the input CSV file."""
    logger.info(f"Loading CSV from: {file_path}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    df = pd.read_csv(file_path)
    logger.info(f"Loaded {len(df)} rows from CSV")
    
    # Validate required column exists
    if ID_COLUMN not in df.columns:
        raise KeyError(f"Required column '{ID_COLUMN}' not found in CSV. Available columns: {list(df.columns)}")
    
    # Ensure output columns exist
    if AVG_TIME_COLUMN not in df.columns:
        df[AVG_TIME_COLUMN] = None
        logger.info(f"Created column: {AVG_TIME_COLUMN}")
    
    if MAX_TIME_COLUMN not in df.columns:
        df[MAX_TIME_COLUMN] = None
        logger.info(f"Created column: {MAX_TIME_COLUMN}")
    
    # Set default values for other columns if they exist but are empty
    if REEXEC_COLUMN in df.columns:
        df[REEXEC_COLUMN] = df[REEXEC_COLUMN].fillna("Yes")
    
    if BILLING_COLUMN in df.columns:
        df[BILLING_COLUMN] = df[BILLING_COLUMN].fillna("Yes")
    
    if DESC_COLUMN in df.columns:
        df[DESC_COLUMN] = df[DESC_COLUMN].fillna("Refer OSO GUI")
    
    return df


def get_db_connection(logger):
    """Create database connection with timeout setting."""
    logger.info(f"Connecting to database: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    
    # Build connection options
    options = f"-c statement_timeout={QUERY_TIMEOUT_SECONDS * 1000}"  # timeout in milliseconds
    if DB_SCHEMA:
        options += f" -c search_path={DB_SCHEMA},public"
    
    conn = psycopg2.connect(
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        options=options
    )
    
    if DB_SCHEMA:
        logger.info(f"Using schema: {DB_SCHEMA}")
    logger.info("Database connection established successfully")
    return conn


def execute_query_for_spec_ver_id(conn, spec_ver_id, logger):
    """
    Execute the average time query for a single spec_ver_id.
    Uses sliding part_id ranges - tries 1-5, then 6-10, etc. until data is found.
    Returns the avg_minutes value or None if no data/timeout.
    """
    current_start = PART_ID_START
    
    while current_start <= PART_ID_MAX:
        # Generate part_id range for this attempt
        part_ids = list(range(current_start, current_start + PART_ID_STEP))
        query = get_query_template(part_ids)
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, (spec_ver_id,))
                result = cursor.fetchone()
                
                if result and result[0] is not None:
                    logger.info(f"  -> Data found in part_id range {part_ids[0]}-{part_ids[-1]}")
                    return float(result[0])
                else:
                    # No data in this range, try next
                    logger.debug(f"  -> No data in part_id range {part_ids[0]}-{part_ids[-1]}, trying next...")
                    current_start += PART_ID_STEP
                    continue
                    
        except psycopg2.extensions.QueryCanceledError:
            logger.warning(f"Query timeout (>{QUERY_TIMEOUT_SECONDS}s) for spec_ver_id: {spec_ver_id} (part_id: {part_ids[0]}-{part_ids[-1]})")
            conn.rollback()  # Reset connection state after timeout
            # Try next part_id range on timeout
            current_start += PART_ID_STEP
            continue
        except Exception as e:
            logger.error(f"Query error for spec_ver_id {spec_ver_id}: {str(e)}")
            conn.rollback()
            return None
    
    # No data found in any part_id range
    logger.info(f"  -> No data found in any part_id range (1-{PART_ID_MAX})")
    return None


def save_csv(df, file_path, logger):
    """Save the dataframe to CSV."""
    logger.info(f"Saving CSV to: {file_path}")
    df.to_csv(file_path, index=False)
    logger.info("CSV saved successfully")


def process_rows(df, conn, logger):
    """Process specified rows and update Avg Time and Maximum Time."""
    
    # Determine row range to process
    total_rows = len(df)
    
    if START_ROW is None and END_ROW is None:
        start_idx = 0
        end_idx = total_rows
        logger.info(f"Processing ALL rows: {total_rows}")
    else:
        if START_ROW is None or END_ROW is None:
            raise ValueError("Both START_ROW and END_ROW must be set, or both must be None")
        if START_ROW < 1 or END_ROW < START_ROW or END_ROW > total_rows:
            raise ValueError(f"Invalid row range. START_ROW={START_ROW}, END_ROW={END_ROW}, Total rows={total_rows}")
        
        start_idx = START_ROW - 1  # Convert to 0-based
        end_idx = END_ROW
        logger.info(f"Processing rows {START_ROW} to {END_ROW} (total: {end_idx - start_idx})")
    
    # Statistics
    processed = 0
    success = 0
    failed = 0
    skipped = 0
    
    logger.info("=" * 60)
    logger.info("Starting query execution...")
    logger.info("=" * 60)
    
    for idx in range(start_idx, end_idx):
        row_num = idx + 1  # 1-based for display
        spec_ver_id = df.loc[idx, ID_COLUMN]
        
        # Skip if spec_ver_id is null/empty
        if pd.isna(spec_ver_id) or str(spec_ver_id).strip() == "":
            logger.warning(f"Row {row_num}: Skipped - Empty spec_ver_id")
            skipped += 1
            continue
        
        spec_ver_id = str(spec_ver_id).strip()
        processed += 1
        
        logger.info(f"Row {row_num}/{end_idx}: Processing spec_ver_id = {spec_ver_id}")
        
        # Execute query
        avg_time = execute_query_for_spec_ver_id(conn, spec_ver_id, logger)
        
        if avg_time is not None:
            max_time = round(avg_time * 2, 2)
            df.loc[idx, AVG_TIME_COLUMN] = avg_time
            df.loc[idx, MAX_TIME_COLUMN] = max_time
            logger.info(f"Row {row_num}: SUCCESS - Avg Time = {avg_time}, Max Time = {max_time}")
            success += 1
        else:
            logger.info(f"Row {row_num}: No data returned or query failed")
            failed += 1
        
        # Save progress every 100 rows
        if processed % 100 == 0:
            save_csv(df, OUTPUT_CSV_PATH, logger)
            logger.info(f"Progress saved after {processed} rows processed")
    
    return processed, success, failed, skipped


def main():
    """Main execution function."""
    # Setup logging
    logger, log_file = setup_logging()
    
    logger.info("=" * 60)
    logger.info("OSO Activity Data - Average Time Calculator")
    logger.info("=" * 60)
    logger.info(f"Log file: {log_file}")
    logger.info(f"Input CSV: {INPUT_CSV_PATH}")
    logger.info(f"Output CSV: {OUTPUT_CSV_PATH}")
    logger.info(f"Query timeout: {QUERY_TIMEOUT_SECONDS} seconds")
    
    if START_ROW is not None and END_ROW is not None:
        logger.info(f"Row range: {START_ROW} to {END_ROW}")
    else:
        logger.info("Row range: ALL")
    
    logger.info("=" * 60)
    
    conn = None
    
    try:
        # Load CSV
        df = load_csv(INPUT_CSV_PATH, logger)
        
        # Connect to database
        conn = get_db_connection(logger)
        
        # Process rows
        processed, success, failed, skipped = process_rows(df, conn, logger)
        
        # Final save
        save_csv(df, OUTPUT_CSV_PATH, logger)
        
        # Summary
        logger.info("=" * 60)
        logger.info("EXECUTION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total rows processed: {processed}")
        logger.info(f"Successful queries:   {success}")
        logger.info(f"Failed/No data:       {failed}")
        logger.info(f"Skipped (empty ID):   {skipped}")
        logger.info(f"Success rate:         {(success/processed*100):.1f}%" if processed > 0 else "N/A")
        logger.info("=" * 60)
        logger.info("Script completed successfully!")
        
        # Clean up log files after successful execution
        cleanup_logs(log_file, logger)
        
    except FileNotFoundError as e:
        logger.error(f"File error: {str(e)}")
        sys.exit(1)
    except KeyError as e:
        logger.error(f"Column error: {str(e)}")
        sys.exit(1)
    except psycopg2.Error as e:
        logger.error(f"Database error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)
    finally:
        if conn:
            conn.close()
            print("Database connection closed")


if __name__ == "__main__":
    main()
