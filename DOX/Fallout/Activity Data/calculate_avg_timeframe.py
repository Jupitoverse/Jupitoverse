#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSO Activity Time Frame Calculator
===================================

This script calculates the average/typical time frame for each spec_ver_id
from the oss_activity_instance table and updates the Excel file.

PURPOSE:
========
- Calculate average completion time for each activity type (spec_ver_id)
- This helps identify activities that are taking longer than expected
- Enables alerting when an activity exceeds its typical time frame

APPROACH:
=========
1. Read spec_ver_id values from Excel file
2. For each spec_ver_id, query last 400 completed activities
3. Calculate typical time frame using median (robust to outliers)
4. Update Excel with calculated time frames and statistics

PERFORMANCE FEATURES:
====================
1. Batch processing with progress logging
2. Connection pooling and timeout handling
3. Outlier filtering for accurate averages
4. Memory-efficient processing

Author: Abhishek Agrahari
Date: December 2025
Contact: abhisha3@amdocs.com
"""

import datetime as dt
import logging
import psycopg2
import pandas as pd
import numpy as np
import os
import sys
import time
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from contextlib import contextmanager

# ============================================================================
# EXECUTION TOGGLES
# ============================================================================
TEST_MODE = True         # Toggle: True = Process only TEST_LIMIT spec_ver_ids, False = Process all
TEST_LIMIT = 3           # Number of spec_ver_ids to process in TEST_MODE

# ============================================================================
# CONFIGURATION CLASS
# ============================================================================
class Config:
    """Centralized configuration for the script"""
    
    # Database Configuration - Read-only access
    DB_CONFIG_READ = {
        'database': "prodossdb",
        'user': 'ossdb01uams',
        'password': 'Pr0d_ossdb01uams',
        'host': 'oso-pstgr-rd.orion.comcast.com',
        'port': '6432'
    }
    
    # Performance Configuration
    LIMIT_RECORDS = 400          # Number of recent records to consider per spec_ver_id
    CONNECTION_TIMEOUT = 300     # Database connection timeout in seconds
    QUERY_TIMEOUT = 600          # Query timeout in seconds
    PROGRESS_LOG_INTERVAL = 100  # Log progress every N spec_ver_ids
    
    # Retry Configuration (for read replica conflicts)
    MAX_RETRIES = 3              # Number of retries per spec_ver_id
    RETRY_DELAY = 5              # Seconds to wait before retry
    RECONNECT_ON_FAILURE = True  # Auto-reconnect if connection lost
    
    # Email Configuration
    SEND_EMAIL = True            # Toggle: True = Send email after completion
    EMAIL_RECIPIENTS = ['abhisha3@amdocs.com']  # Add more recipients as needed
    EMAIL_CC = ['abhisha3@amdocs.com']
    EMAIL_FROM = "noreply@amdocs.com"
    EMAIL_SUBJECT = "OSO Activity Time Frame Analysis Report"
    
    # File Configuration - Server paths (Jupitoverse)
    BASE_DIR = "/fs_ogs/operogs/scriptbin/ogs_monitors/Jupitoverse"
    INPUT_FILE = os.path.join(BASE_DIR, "OSO_activity_data.xlsx")
    OUTPUT_FILE = os.path.join(BASE_DIR, "OSO_activity_data_with_timeframes.xlsx")
    LOG_DIR = BASE_DIR
    
    # Local machine paths (commented out)
    # BASE_DIR = r"C:\Users\abhisha3\Desktop\Projects\Fallout\Activity Data"
    # INPUT_FILE = os.path.join(BASE_DIR, "OSO_activity_data.xlsx")
    # OUTPUT_FILE = os.path.join(BASE_DIR, "OSO_activity_data_with_timeframes.xlsx")
    # LOG_DIR = BASE_DIR


# ============================================================================
# LOGGING SETUP
# ============================================================================
def setup_logging():
    """
    Setup comprehensive logging with both file and console output.
    Log files are timestamped for easy tracking.
    """
    timestamp = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(Config.LOG_DIR, f"timeframe_calculation_{timestamp}.log")
    
    # Create logger
    logger = logging.getLogger('TimeFrameCalculator')
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # File handler - logs everything to file
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Console handler - logs to terminal
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Formatter - consistent format across handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger, log_file


# Initialize logging
logger, log_file = setup_logging()


# ============================================================================
# DATABASE CONNECTION MANAGEMENT
# ============================================================================
@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    Ensures proper connection handling and cleanup.
    
    Usage:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
    """
    conn = None
    try:
        logger.info("Establishing database connection...")
        conn = psycopg2.connect(
            database=Config.DB_CONFIG_READ['database'],
            user=Config.DB_CONFIG_READ['user'],
            password=Config.DB_CONFIG_READ['password'],
            host=Config.DB_CONFIG_READ['host'],
            port=Config.DB_CONFIG_READ['port'],
            connect_timeout=Config.CONNECTION_TIMEOUT
        )
        logger.info("Database connection established successfully.")
        yield conn
    except psycopg2.Error as e:
        logger.error(f"Database connection failed: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed.")


def test_database_connection():
    """
    Test function to verify database connection.
    Use this to validate connectivity before full execution.
    """
    try:
        logger.info("=" * 60)
        logger.info("TESTING DATABASE CONNECTION")
        logger.info("=" * 60)
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Test 1: Basic connection
            logger.info("Test 1: Basic connection - SUCCESS")
            
            # Test 2: Query execution
            cursor.execute("SELECT COUNT(*) FROM ossdb01db.oss_activity_instance LIMIT 1")
            logger.info("Test 2: Query execution - SUCCESS")
            
            # Test 3: Check table access
            cursor.execute("""
                SELECT COUNT(DISTINCT spec_ver_id) 
                FROM ossdb01db.oss_activity_instance 
                WHERE state = 'Completed'
            """)
            count = cursor.fetchone()[0]
            logger.info(f"Test 3: Table access - SUCCESS. Found {count:,} unique spec_ver_ids")
            
            cursor.close()
            
        logger.info("=" * 60)
        logger.info("ALL CONNECTION TESTS PASSED")
        logger.info("=" * 60)
        return True
        
    except Exception as e:
        logger.error(f"Connection test FAILED: {e}")
        return False


# ============================================================================
# TIME FRAME QUERY
# ============================================================================
TIMEFRAME_QUERY = """
WITH filtered AS (
    SELECT
        actual_start_date,
        actual_end_date
    FROM ossdb01db.oss_activity_instance
    WHERE spec_ver_id = %s
      AND state = 'Completed'
      AND prev_state = 'In Progress'
    ORDER BY create_date DESC
    LIMIT %s
)
SELECT
    EXTRACT(EPOCH FROM (actual_end_date - actual_start_date)) / 3600 AS time_frame_hours
FROM filtered
WHERE actual_end_date IS NOT NULL 
  AND actual_start_date IS NOT NULL
  AND actual_end_date > actual_start_date;
"""


# ============================================================================
# TIME FRAME CALCULATION FUNCTIONS
# ============================================================================
def get_timeframes_for_spec_ver_id(cursor, spec_ver_id: str) -> tuple:
    """
    Execute query to get time frames for a specific spec_ver_id.
    
    Args:
        cursor: Database cursor
        spec_ver_id: The spec_ver_id to query
    
    Returns:
        Tuple of (list of timeframes, needs_reconnect flag)
    """
    try:
        cursor.execute(TIMEFRAME_QUERY, (spec_ver_id, Config.LIMIT_RECORDS))
        results = cursor.fetchall()
        # Extract time frame values, filter out None and negative values
        timeframes = [row[0] for row in results if row[0] is not None and row[0] > 0]
        return timeframes, False
    except psycopg2.OperationalError as e:
        # Connection lost or recovery conflict - needs reconnection
        logger.warning(f"Connection issue for {spec_ver_id}: {e}")
        return [], True
    except psycopg2.Error as e:
        logger.error(f"Query failed for spec_ver_id {spec_ver_id}: {e}")
        return [], False


def create_db_connection():
    """
    Create a new database connection.
    Used for initial connection and reconnection after failures.
    """
    try:
        conn = psycopg2.connect(
            database=Config.DB_CONFIG_READ['database'],
            user=Config.DB_CONFIG_READ['user'],
            password=Config.DB_CONFIG_READ['password'],
            host=Config.DB_CONFIG_READ['host'],
            port=Config.DB_CONFIG_READ['port'],
            connect_timeout=Config.CONNECTION_TIMEOUT
        )
        return conn
    except psycopg2.Error as e:
        logger.error(f"Failed to create connection: {e}")
        return None


def calculate_typical_timeframe(timeframes: list) -> dict:
    """
    Calculate the typical/average time frame from a list of values.
    
    Uses median as primary measure (robust to outliers).
    Also calculates:
    - Mean, Std Dev for reference
    - P90 (90th percentile) for alert threshold
    
    Args:
        timeframes: List of time frame values in hours
    
    Returns:
        Dictionary with calculated statistics
    """
    result = {
        'typical_value': None,
        'count': 0,
        'mean': None,
        'median': None,
        'std_dev': None,
        'min': None,
        'max': None,
        'p90': None,
        'method': 'No data'
    }
    
    if not timeframes or len(timeframes) == 0:
        return result
    
    result['count'] = len(timeframes)
    
    if len(timeframes) == 1:
        result['typical_value'] = round(timeframes[0], 2)
        result['median'] = result['typical_value']
        result['mean'] = result['typical_value']
        result['min'] = result['typical_value']
        result['max'] = result['typical_value']
        result['method'] = 'Single value'
        return result
    
    arr = np.array(timeframes)
    
    # Remove extreme outliers (values beyond 3 standard deviations)
    mean = np.mean(arr)
    std = np.std(arr)
    
    if std > 0:
        # Filter out extreme outliers for typical value calculation
        filtered = arr[(arr > mean - 3*std) & (arr < mean + 3*std)]
        if len(filtered) == 0:
            filtered = arr
    else:
        filtered = arr
    
    # Calculate statistics
    result['mean'] = round(np.mean(filtered), 2)
    result['median'] = round(np.median(filtered), 2)
    result['std_dev'] = round(np.std(filtered), 2)
    result['min'] = round(np.min(arr), 2)
    result['max'] = round(np.max(arr), 2)
    result['p90'] = round(np.percentile(arr, 90), 2)
    
    # Use median as typical value (more robust to outliers)
    result['typical_value'] = result['median']
    result['method'] = 'Median'
    
    return result


# ============================================================================
# EMAIL MANAGER CLASS
# ============================================================================
class EmailMgr:
    """
    Email manager class for sending report emails with attachments.
    """
    
    def __init__(self, output_file, summary_stats):
        """
        Initialize email manager.
        
        Args:
            output_file: Path to the Excel file to attach
            summary_stats: Dictionary with processing summary statistics
        """
        self.output_file = output_file
        self.summary_stats = summary_stats
    
    def send_mail(self):
        """Send the email with Excel attachment."""
        recipients = Config.EMAIL_RECIPIENTS.copy()
        cc_recipients = Config.EMAIL_CC.copy()
        FROM = Config.EMAIL_FROM
        
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = f"{Config.EMAIL_SUBJECT} - {dt.datetime.strftime(dt.datetime.now(), '%Y/%m/%d')}"
        MESSAGE['To'] = ", ".join(recipients)
        MESSAGE['Cc'] = ", ".join(cc_recipients)
        MESSAGE['From'] = FROM
        
        # Add HTML body
        BODY = self.get_mail_content()
        HTML_BODY = MIMEText(BODY, 'html')
        MESSAGE.attach(HTML_BODY)
        
        # Attach Excel file
        ctype, encoding = mimetypes.guess_type(self.output_file)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        
        maintype, subtype = ctype.split('/', 1)
        
        # Get just the filename for attachment
        filename = os.path.basename(self.output_file)
        
        try:
            with open(self.output_file, 'rb') as fp:
                part = MIMEBase(maintype, subtype)
                part.set_payload(fp.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=filename)
            MESSAGE.attach(part)
        except Exception as e:
            logger.error(f"Failed to attach Excel file: {e}")
        
        # Send email
        try:
            server = smtplib.SMTP('localhost')
            all_recipients = recipients + cc_recipients
            server.sendmail(FROM, all_recipients, MESSAGE.as_string())
            server.quit()
            logger.info("Email sent successfully!")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
    
    def get_mail_content(self):
        """Generate HTML email content with summary statistics."""
        stats = self.summary_stats
        return f"""
        <html>
        <head>
        <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 14px;
            color: #333;
            line-height: 1.6;
        }}
        h2 {{
            color: #004080;
            border-bottom: 2px solid #ccc;
            padding-bottom: 5px;
        }}
        p {{
            margin: 10px 0;
        }}
        .styled-table {{
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.95em;
            min-width: 400px;
            border: 1px solid #dddddd;
        }}
        .styled-table th, .styled-table td {{
            border: 1px solid #dddddd;
            padding: 8px 12px;
            text-align: left;
        }}
        .styled-table th {{
            background-color: #f4f4f4;
            font-weight: bold;
        }}
        .success {{ color: #28a745; }}
        .warning {{ color: #ffc107; }}
        .error {{ color: #dc3545; }}
        .note {{
            margin-top: 20px;
            font-size: 13px;
            color: #555;
        }}
        .footer {{
            margin-top: 30px;
            font-size: 14px;
            font-weight: bold;
        }}
        </style>
        </head>
        <body>
        <p>Hi Team,</p>
        <p>The OSO Activity Time Frame Analysis has been completed successfully. Please find the detailed report attached.</p>
        
        <h2>Processing Summary</h2>
        <table class="styled-table">
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Total spec_ver_ids Processed</td><td>{stats.get('processed', 'N/A'):,}</td></tr>
            <tr><td>Successfully Calculated</td><td class="success">{stats.get('success', 'N/A'):,}</td></tr>
            <tr><td>No Data Available</td><td class="warning">{stats.get('no_data', 'N/A'):,}</td></tr>
            <tr><td>Errors</td><td class="error">{stats.get('errors', 'N/A')}</td></tr>
            <tr><td>Database Reconnections</td><td>{stats.get('reconnects', 'N/A')}</td></tr>
            <tr><td>Total Processing Time</td><td>{stats.get('elapsed_time', 'N/A')}</td></tr>
        </table>
        
        <h2>Report Details</h2>
        <p>The attached Excel file contains the following columns:</p>
        <ul>
            <li><strong>spec_ver_id</strong> - Activity specification ID</li>
            <li><strong>name</strong> - Activity name</li>
            <li><strong>Time Frame</strong> - Typical completion time in hours (median)</li>
            <li><strong>TF_Sample_Count</strong> - Number of samples used for calculation</li>
            <li><strong>TF_Std_Dev</strong> - Standard deviation of time frames</li>
            <li><strong>TF_P90</strong> - 90th percentile (suggested alert threshold)</li>
        </ul>
        
        <h2>Usage for Alerting</h2>
        <p>Activities taking longer than the <strong>TF_P90</strong> value should be flagged for review.</p>
        
        <div class='note'>For any questions or changes: Please reach out to <a href='mailto:abhisha3@amdocs.com'>abhisha3@amdocs.com</a></div>
        <div class='footer'>Regards,<br>Abhishek Agrahari</div>
        </body>
        </html>
        """


# ============================================================================
# MAIN PROCESSING FUNCTION
# ============================================================================
def process_excel_file():
    """
    Main function to process the Excel file and calculate time frames.
    
    Workflow:
    1. Read Excel file with spec_ver_ids
    2. Connect to database
    3. For each spec_ver_id, calculate typical time frame
    4. Update Excel with results
    5. Save output file
    """
    logger.info("=" * 70)
    logger.info("OSO ACTIVITY TIME FRAME CALCULATOR - STARTED")
    logger.info("=" * 70)
    logger.info(f"Execution Mode: SERVER (Jupitoverse)")
    logger.info(f"Test Mode: {'ENABLED (Limit: ' + str(TEST_LIMIT) + ')' if TEST_MODE else 'DISABLED (Full Run)'}")
    logger.info(f"Input File: {Config.INPUT_FILE}")
    logger.info(f"Output File: {Config.OUTPUT_FILE}")
    logger.info(f"Records per spec_ver_id: {Config.LIMIT_RECORDS}")
    logger.info("=" * 70)
    
    # Step 1: Read Excel file
    logger.info("STEP 1: Reading Excel file...")
    try:
        df = pd.read_excel(Config.INPUT_FILE)
        logger.info(f"   Columns found: {list(df.columns)}")
        logger.info(f"   Total rows: {len(df)}")
    except FileNotFoundError:
        logger.error(f"Excel file not found: {Config.INPUT_FILE}")
        return False
    except Exception as e:
        logger.error(f"Error reading Excel file: {e}")
        return False
    
    # Verify required column exists
    if 'spec_ver_id' not in df.columns:
        logger.error("'spec_ver_id' column not found in Excel file")
        logger.info(f"   Available columns: {list(df.columns)}")
        return False
    
    # Initialize output columns
    df['Time Frame'] = None
    df['TF_Sample_Count'] = None
    df['TF_Std_Dev'] = None
    df['TF_P90'] = None
    
    # Step 2: Connect to database and process
    logger.info("STEP 2: Connecting to database...")
    
    # Get unique spec_ver_ids
    spec_ver_ids = df['spec_ver_id'].dropna().unique()
    total_available = len(spec_ver_ids)
    
    # Apply TEST_MODE limit if enabled
    if TEST_MODE:
        spec_ver_ids = spec_ver_ids[:TEST_LIMIT]
        total_count = len(spec_ver_ids)
        logger.info("=" * 50)
        logger.info(f"⚠️  TEST MODE ENABLED - Processing only {total_count} spec_ver_ids")
        logger.info(f"   (Total available: {total_available:,})")
        logger.info("=" * 50)
    else:
        total_count = total_available
    
    logger.info(f"STEP 3: Processing {total_count:,} unique spec_ver_ids...")
    
    # Counters for summary
    processed = 0
    success = 0
    no_data = 0
    errors = 0
    reconnect_count = 0
    
    start_time = dt.datetime.now()
    
    # Create initial connection
    conn = create_db_connection()
    if not conn:
        logger.error("Failed to establish initial database connection")
        return False
    
    logger.info("Database connection established successfully.")
    cursor = conn.cursor()
    
    try:
        # Process each spec_ver_id
        for idx, spec_ver_id in enumerate(spec_ver_ids):
            retry_count = 0
            spec_processed = False
            
            while retry_count < Config.MAX_RETRIES and not spec_processed:
                try:
                    # Get timeframes from database
                    timeframes, needs_reconnect = get_timeframes_for_spec_ver_id(cursor, str(spec_ver_id))
                    
                    # Handle reconnection if needed
                    if needs_reconnect:
                        logger.warning(f"   Reconnecting to database (attempt {retry_count + 1}/{Config.MAX_RETRIES})...")
                        time.sleep(Config.RETRY_DELAY)
                        
                        # Close old connection safely
                        try:
                            cursor.close()
                            conn.close()
                        except:
                            pass
                        
                        # Create new connection
                        conn = create_db_connection()
                        if conn:
                            cursor = conn.cursor()
                            reconnect_count += 1
                            logger.info(f"   Reconnected successfully. Retrying spec_ver_id...")
                            retry_count += 1
                            continue
                        else:
                            logger.error("   Failed to reconnect. Skipping this spec_ver_id.")
                            errors += 1
                            spec_processed = True
                            continue
                    
                    # Process results
                    if timeframes:
                        # Calculate statistics
                        stats = calculate_typical_timeframe(timeframes)
                        
                        # Update DataFrame
                        mask = df['spec_ver_id'] == spec_ver_id
                        df.loc[mask, 'Time Frame'] = stats['typical_value']
                        df.loc[mask, 'TF_Sample_Count'] = stats['count']
                        df.loc[mask, 'TF_Std_Dev'] = stats['std_dev']
                        df.loc[mask, 'TF_P90'] = stats['p90']
                        
                        success += 1
                    else:
                        no_data += 1
                    
                    spec_processed = True
                    
                except Exception as e:
                    logger.error(f"   Error processing {spec_ver_id}: {e}")
                    retry_count += 1
                    if retry_count < Config.MAX_RETRIES:
                        logger.info(f"   Retrying in {Config.RETRY_DELAY} seconds...")
                        time.sleep(Config.RETRY_DELAY)
                    else:
                        errors += 1
                        spec_processed = True
            
            processed += 1
            
            # Progress logging
            if (idx + 1) % Config.PROGRESS_LOG_INTERVAL == 0 or (idx + 1) == total_count:
                elapsed = (dt.datetime.now() - start_time).total_seconds()
                rate = (idx + 1) / elapsed if elapsed > 0 else 0
                remaining = (total_count - idx - 1) / rate if rate > 0 else 0
                logger.info(f"   Progress: {idx + 1:,}/{total_count:,} ({(idx+1)/total_count*100:.1f}%) "
                           f"| Rate: {rate:.1f}/sec | ETA: {remaining/60:.1f} min | Reconnects: {reconnect_count}")
    
    finally:
        # Close connection
        try:
            cursor.close()
            conn.close()
            logger.info("Database connection closed.")
        except:
            pass
    
    # Step 3: Save results to Excel
    logger.info("STEP 4: Saving results to Excel...")
    try:
        df.to_excel(Config.OUTPUT_FILE, index=False, engine='openpyxl')
        logger.info(f"   Excel file saved: {Config.OUTPUT_FILE}")
    except Exception as e:
        logger.error(f"Error saving Excel file: {e}")
        # Try alternative path
        alt_path = os.path.join(Config.BASE_DIR, 
                                f"output_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        try:
            df.to_excel(alt_path, index=False, engine='openpyxl')
            logger.info(f"   Saved to alternative path: {alt_path}")
        except Exception as e2:
            logger.error(f"Failed to save to alternative path: {e2}")
            return False
    
    # Summary
    elapsed_total = (dt.datetime.now() - start_time).total_seconds()
    elapsed_str = f"{elapsed_total/60:.2f} minutes"
    
    logger.info("=" * 70)
    logger.info("PROCESSING COMPLETE - SUMMARY")
    logger.info("=" * 70)
    logger.info(f"   Total spec_ver_ids processed: {processed:,}")
    logger.info(f"   Successfully calculated: {success:,}")
    logger.info(f"   No data available: {no_data:,}")
    logger.info(f"   Errors: {errors:,}")
    logger.info(f"   Database reconnections: {reconnect_count}")
    logger.info(f"   Total time: {elapsed_str}")
    logger.info(f"   Output file: {Config.OUTPUT_FILE}")
    logger.info(f"   Log file: {log_file}")
    logger.info("=" * 70)
    
    # Send email with results
    if Config.SEND_EMAIL:
        logger.info("STEP 5: Sending email report...")
        summary_stats = {
            'processed': processed,
            'success': success,
            'no_data': no_data,
            'errors': errors,
            'reconnects': reconnect_count,
            'elapsed_time': elapsed_str
        }
        email_mgr = EmailMgr(Config.OUTPUT_FILE, summary_stats)
        email_mgr.send_mail()
    else:
        logger.info("Email sending is disabled (SEND_EMAIL = False)")
    
    return True


# ============================================================================
# ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  OSO Activity Time Frame Calculator")
    print("  Calculates average completion time for each activity type")
    print("=" * 70)
    print(f"  Execution Mode: SERVER (Jupitoverse)")
    print(f"  Test Mode: {'ENABLED (Limit: ' + str(TEST_LIMIT) + ')' if TEST_MODE else 'DISABLED (Full Run)'}")
    print(f"  Log File: {log_file}")
    print("=" * 70 + "\n")
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test':
            print("Running database connection test...\n")
            test_database_connection()
            sys.exit(0)
        elif sys.argv[1] == '--help':
            print("Usage:")
            print("  python calculate_avg_timeframe.py          # Run full processing")
            print("  python calculate_avg_timeframe.py --test   # Test database connection")
            print("  python calculate_avg_timeframe.py --help   # Show this help")
            sys.exit(0)
    
    # Run main processing
    logger.info("Starting OSO Activity Time Frame Calculator...")
    success = process_excel_file()
    
    if success:
        print("\n✅ Script completed successfully. Check log file for details.")
    else:
        print("\n❌ Script completed with errors. Check log file for details.")
    
    print(f"   Log file: {log_file}")
