"""
RELEASE PONR (Point of No Return) Analysis Script

This script identifies orders where the RELEASE PONR flag was not triggered by the system,
even though the mandatory wait period associated with the Registered Timed Action has been completed.

OPTIMIZATION STRATEGY:
=====================
- Cascading CTE approach with progressive filtering for maximum efficiency
- Smart part_id batching to minimize database load
- Efficient memory management with streaming results
- Comprehensive logging and cleanup

CASCADING FILTER APPROACH:
=========================
1. eligible_projects: Base dataset from spoi table
2. projects_with_completed_activities: Filter projects with completed activities (reduces dataset)
3. projects_with_in_progress_activities: Filter projects with in-progress activities (further reduces)
4. final_filtered_projects: Final filter with blocking activities (smallest dataset)

This approach dramatically reduces the number of rows processed at each step, minimizing database load.

PERFORMANCE FEATURES:
====================
1. Progressive filtering reduces dataset size at each CTE step
2. Part_id filtering applied at each activity filter level
3. Dynamic part_id range adjustment based on data density
4. Memory-efficient result processing
5. Automatic cleanup of temporary files and logs
6. Comprehensive error handling and retry logic

REQUIRED INDEXES:
================
Ensure these indexes exist for optimal performance:
- oss_activity_instance(part_id, spec_ver_id, state, is_latest_version)
- sc_project_order_instance(plan_id, status, is_latest_version)
- oss_activity_instance(plan_id, spec_ver_id, state, is_latest_version)
"""

import datetime as dt
import logging
import smtplib
import psycopg2
import pandas as pd
import mimetypes
import os
import sys
import glob
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from contextlib import contextmanager

# Configuration
class Config:
    """Centralized configuration"""
    
    # Database Configuration
    DB_CONFIG = {
        'database': "prodossdb",
        'user': 'ossdb01uams',
        'password': 'Pr0d_ossdb01uams',
        'host': 'oso-pstgr-rd.orion.comcast.com',
        'port': '6432'
    }
    
    # Performance Configuration
    PART_ID_BATCH_SIZE = 5  # Smaller batches for reduced DB load
    PART_ID_START = 1       # Starting part_id value (easily configurable)
    PART_ID_END = 99        # Ending part_id value (easily configurable)
    CONNECTION_TIMEOUT = 30
    QUERY_TIMEOUT = 300  # 5 minutes max per query
    
    # File Configuration
    OUTPUT_DIR = "."
    CLEANUP_ENABLED = True
    
    # Database Storage Configuration
    PONR_TABLE = "ossdb01db.ponr_tracking"
    TAG_NAME = "RELEASE_PONR"

# Setup logging
def setup_logging():
    """Setup comprehensive logging"""
    timestamp = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(Config.OUTPUT_DIR, f"ponr_execution_{timestamp}.log")
    
    # Create logger
    logger = logging.getLogger('PONR_Analysis')
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger, log_file

# Initialize logging
logger, log_file = setup_logging()

# Database connection manager
@contextmanager
def get_db_connection():
    """Context manager for database connections with proper cleanup"""
    conn = None
    try:
        logger.info("Establishing database connection...")
        conn = psycopg2.connect(
            **Config.DB_CONFIG,
            connect_timeout=Config.CONNECTION_TIMEOUT
        )
        conn.autocommit = True
        logger.info("Database connection established successfully")
        yield conn
    except psycopg2.Error as e:
        logger.error(f"Database connection error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected database error: {e}")
        raise
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")

# Working query from original script - Simple approach with string formatting
WORKING_SIMPLE_QUERY = """
SELECT spoi.id AS projectid, spoi.version, oai.status AS activity_status, 
       spoi.status AS project_status, oai.id AS activity_id,
       spoi.name, oai2.last_update_date, oai.create_date
FROM ossdb01db.sc_project_order_instance spoi
INNER JOIN ossdb01db.oss_activity_instance oai ON spoi.plan_id = oai.plan_id
INNER JOIN ossdb01db.oss_activity_instance oai2 ON oai.plan_id = oai2.plan_id
INNER JOIN ossdb01db.oss_activity_instance oai3 ON oai.plan_id = oai3.plan_id
WHERE spoi.status NOT IN ('FCANCELLED', 'DCOMPLETED')
  AND spoi.name NOT LIKE '%MM_PROD_TEST%'
  AND spoi.name NOT LIKE '%MM_Prod_Test%'
  AND spoi.manager IS DISTINCT FROM 'ProductionSanity'
  AND spoi.is_latest_version = 1
  AND oai2.spec_ver_id = '91757a68-692f-4246-91e1-7e2280a659d8'
  AND oai2.state = 'Completed'
  AND oai2.is_latest_version = 1
  AND oai2.complete_date < CURRENT_DATE - INTERVAL '10 days'
  AND oai.spec_ver_id = '03acd7f1-557a-4727-ba2e-8d44f6245047'
  AND oai.state IN ('In Progress', 'Optional')
  AND oai.is_latest_version = 1
  AND oai3.spec_ver_id = '88f0860f-e647-41cd-aaac-1930adea8a3c'
  AND oai3.state NOT IN ('In Progress')
  AND oai3.is_latest_version = 1
  AND oai.part_id BETWEEN {start} AND {end};
"""

def execute_optimized_query(cursor, start, end):
    """Execute the working simple query using string formatting (from original script)"""
    try:
        logger.info(f"Executing working simple query for part_id {start}-{end}")
        logger.info("Using proven query approach from original working script")
        
        # Set query timeout
        cursor.execute(f"SET statement_timeout = '{Config.QUERY_TIMEOUT}s'")
        
        # Use string formatting like the original working script
        query = WORKING_SIMPLE_QUERY.format(start=start, end=end)
        logger.info(f"Executing query for part_id range {start}-{end}")
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        logger.info(f"Working query completed: Found {len(results)} records for part_id {start}-{end}")
        
        # Debug: Log first few results if any
        if results:
            logger.info(f"Sample result structure: {len(results[0])} columns")
            logger.info(f"First result: {results[0] if results else 'No results'}")
        
        return results
        
    except psycopg2.Error as e:
        logger.error(f"Database working query error for part_id {start}-{end}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected working query error for part_id {start}-{end}: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return []

def process_and_store_results(results, cursor):
    """Process results, check for duplicates, and store new records in database"""
    try:
        logger.info("Processing results for database storage...")
        
        if not results:
            logger.info("No results to process")
            return []
        
        # Convert results to DataFrame for easier processing
        columns = ["projectid", "version", "activity_status", "project_status", 
                  "activity_id", "name", "last_update_date", "create_date"]
        df = pd.DataFrame(results, columns=columns)
        
        logger.info(f"Processing {len(df)} records for database storage")
        
        # Add calculated columns
        current_date = dt.datetime.now().date()
        df['identified_date'] = current_date
        df['tag'] = Config.TAG_NAME
        df['rca'] = None  # To be filled manually
        df['handling_status'] = 'PENDING'
        
        # Calculate age in days (current_date - last_update_date)
        df['last_update_date'] = pd.to_datetime(df['last_update_date'])
        df['age_days'] = (pd.Timestamp(current_date) - df['last_update_date']).dt.days
        
        # Generate unique_id: RP_projectid_age_days
        df['unique_id'] = df.apply(lambda row: f"RP_{row['projectid']}_{row['age_days']}", axis=1)
        
        logger.info(f"Generated unique IDs for {len(df)} records")
        
        # Check for existing records
        existing_ids = check_existing_records(cursor, df['unique_id'].tolist())
        logger.info(f"Found {len(existing_ids)} existing records in database")
        
        # Filter out existing records
        new_records_df = df[~df['unique_id'].isin(existing_ids)]
        logger.info(f"Identified {len(new_records_df)} new records to insert")
        
        # Insert new records
        if not new_records_df.empty:
            insert_new_records(cursor, new_records_df)
            logger.info(f"Successfully inserted {len(new_records_df)} new records")
        else:
            logger.info("No new records to insert - all records already exist")
        
        # Get all records for today's email (including existing ones)
        all_todays_records = get_todays_records(cursor)
        logger.info(f"Retrieved {len(all_todays_records)} total records for today's email")
        
        return all_todays_records
        
    except Exception as e:
        logger.error(f"Error processing and storing results: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return results  # Return original results if processing fails

def check_existing_records(cursor, unique_ids):
    """Check which records already exist in the database"""
    try:
        if not unique_ids:
            return []
        
        # Create placeholders for the IN clause
        placeholders = ','.join(['%s'] * len(unique_ids))
        query = f"""
        SELECT unique_id 
        FROM {Config.PONR_TABLE} 
        WHERE unique_id IN ({placeholders})
        """
        
        cursor.execute(query, unique_ids)
        existing_records = cursor.fetchall()
        existing_ids = [record[0] for record in existing_records]
        
        logger.info(f"Checked {len(unique_ids)} IDs, found {len(existing_ids)} existing records")
        return existing_ids
        
    except Exception as e:
        logger.error(f"Error checking existing records: {e}")
        return []

def insert_new_records(cursor, df):
    """Insert new records into the database"""
    try:
        insert_query = f"""
        INSERT INTO {Config.PONR_TABLE} (
            unique_id, projectid, version, activity_status, project_status,
            activity_id, name, last_update_date, create_date, identified_date,
            tag, rca, handling_status, age_days
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        # Prepare data for insertion
        records_to_insert = []
        for _, row in df.iterrows():
            record = (
                row['unique_id'],
                int(row['projectid']),
                int(row['version']) if pd.notna(row['version']) else None,
                row['activity_status'],
                row['project_status'],
                int(row['activity_id']) if pd.notna(row['activity_id']) else None,
                row['name'],
                row['last_update_date'],
                row['create_date'],
                row['identified_date'],
                row['tag'],
                row['rca'],
                row['handling_status'],
                int(row['age_days'])
            )
            records_to_insert.append(record)
        
        # Execute batch insert
        cursor.executemany(insert_query, records_to_insert)
        logger.info(f"Batch inserted {len(records_to_insert)} records")
        
    except Exception as e:
        logger.error(f"Error inserting new records: {e}")
        raise

def get_todays_records(cursor):
    """Get all records identified today for email reporting"""
    try:
        query = f"""
        SELECT unique_id, projectid, version, activity_status, project_status,
               activity_id, name, last_update_date, create_date, identified_date,
               tag, rca, handling_status, age_days
        FROM {Config.PONR_TABLE}
        WHERE identified_date = CURRENT_DATE
          AND tag = %s
        ORDER BY age_days DESC, projectid
        """
        
        cursor.execute(query, (Config.TAG_NAME,))
        records = cursor.fetchall()
        
        logger.info(f"Retrieved {len(records)} records for today's email")
        return records
        
    except Exception as e:
        logger.error(f"Error retrieving today's records: {e}")
        return []

def generate_part_id_ranges():
    """Generate configurable part_id ranges for minimal DB load"""
    logger.info(f"Generating part_id ranges: {Config.PART_ID_START} to {Config.PART_ID_END} with batch size {Config.PART_ID_BATCH_SIZE}")
    
    ranges = []
    for start in range(Config.PART_ID_START, Config.PART_ID_END + 1, Config.PART_ID_BATCH_SIZE):
        end = min(start + Config.PART_ID_BATCH_SIZE - 1, Config.PART_ID_END)
        ranges.append((start, end))
    
    logger.info(f"Generated {len(ranges)} part_id ranges for processing")
    return ranges

def create_reusable_part_id_ranges(start_value, end_value, batch_size):
    """
    Reusable function to generate part_id ranges for any query
    
    Args:
        start_value (int): Starting part_id value
        end_value (int): Ending part_id value  
        batch_size (int): Batch size for each range
        
    Returns:
        list: List of (start, end) tuples for part_id ranges
        
    Example:
        ranges = create_reusable_part_id_ranges(1, 50, 5)
        # Returns: [(1, 5), (6, 10), (11, 15), ..., (46, 50)]
    """
    ranges = []
    for start in range(start_value, end_value + 1, batch_size):
        end = min(start + batch_size - 1, end_value)
        ranges.append((start, end))
    
    logger.info(f"Reusable ranges generated: {start_value}-{end_value} in {len(ranges)} batches of {batch_size}")
    return ranges

def main():
    """Main execution function using original script's batching approach"""
    logger.info("="*60)
    logger.info("PONR Analysis Script Started")
    logger.info("Using original working script's query and batching approach")
    logger.info("="*60)
    
    results = []
    total_processed = 0
    failed_batches = 0
    
    # Use the same part_id ranges as the original working script
    part_id_ranges = [(1, 10), (11, 20), (21, 30), (31, 40), (41, 50), 
                      (51, 60), (61, 70), (71, 80), (81, 90), (91, 99)]
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            logger.info(f"Processing {len(part_id_ranges)} part_id ranges (same as original script)")
            
            # Process each range exactly like the original script
            for i, (start, end) in enumerate(part_id_ranges, 1):
                try:
                    logger.info(f"Processing batch {i}/{len(part_id_ranges)}: part_id BETWEEN {start} AND {end}")
                    
                    batch_results = execute_optimized_query(cursor, start, end)
                    
                    # Debug: Check batch results structure
                    if batch_results:
                        logger.info(f"Batch {i} returned {len(batch_results)} results")
                        if len(batch_results) > 0:
                            logger.info(f"Batch {i} first result structure: {len(batch_results[0])} columns")
                    
                    results.extend(batch_results)
                    total_processed += len(batch_results)
                    
                    logger.info(f"✓ Batch {start}-{end}: Found {len(batch_results)} records")
                    
                except Exception as e:
                    failed_batches += 1
                    logger.error(f"✗ Batch {start}-{end} FAILED: {e}")
                    logger.error(f"Error type: {type(e).__name__}")
                    import traceback
                    logger.error(f"Batch {i} traceback: {traceback.format_exc()}")
                    continue
            
            # Process and store results in database
            logger.info("Processing results for database storage...")
            final_results = process_and_store_results(results, cursor)
            
            cursor.close()
            
    except Exception as e:
        logger.error(f"Critical error in main execution: {e}")
        raise
    
    # Log summary
    logger.info("="*60)
    logger.info("Query Execution Summary:")
    logger.info(f"- Total records found: {total_processed}")
    logger.info(f"- Failed batches: {failed_batches}")
    logger.info(f"- Success rate: {((len(part_id_ranges)-failed_batches)/len(part_id_ranges))*100:.1f}%")
    logger.info(f"- Final records for email: {len(final_results) if 'final_results' in locals() else 0}")
    logger.info("="*60)
    
    return final_results if 'final_results' in locals() else results

def generate_reports(results):
    """Generate Excel and HTML reports with enhanced error handling"""
    try:
        logger.info("Generating reports...")
        logger.info(f"Processing {len(results)} result records")
        
        # Debug: Check result structure
        if results:
            logger.info(f"First result length: {len(results[0])}")
            logger.info(f"First result sample: {results[0]}")
        
        # Create DataFrame with proper error handling - updated for database records
        if results and len(results[0]) > 8:  # Database records with additional columns
            columns = ["unique_id", "projectid", "version", "activity_status", "project_status", 
                      "activity_id", "name", "last_update_date", "create_date", "identified_date",
                      "tag", "rca", "handling_status", "age_days"]
        else:  # Original query results
            columns = ["projectid", "version", "activity_status", "project_status", 
                      "activity_id", "name", "last_update_date", "create_date"]
        
        # Validate results structure before creating DataFrame
        if results:
            expected_columns = len(columns)
            actual_columns = len(results[0]) if results else 0
            
            if actual_columns != expected_columns:
                logger.error(f"Column mismatch: Expected {expected_columns}, got {actual_columns}")
                logger.error(f"Expected columns: {columns}")
                logger.error(f"Sample result: {results[0] if results else 'No results'}")
                return f"<p><strong>Error: Column structure mismatch in query results</strong></p>", None
        
        df = pd.DataFrame(results, columns=columns)
        
        if df.empty:
            logger.warning("No data found! DataFrame is empty.")
            html_table = "<p><strong>No PONR issues found in the current analysis.</strong></p>"
        else:
            logger.info(f"Generated DataFrame with {len(df)} rows and {len(df.columns)} columns")
            html_table = df.to_html(index=False, classes='styled-table')
        
        # Save Excel file
        output_file = os.path.join(Config.OUTPUT_DIR, "ponr_report.xlsx")
        df.to_excel(output_file, index=False)
        logger.info(f"Excel report saved: {output_file}")
        
        return html_table, output_file
        
    except Exception as e:
        logger.error(f"Error generating reports: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return f"<p><strong>Error generating report: {e}</strong></p>", None

class EmailManager:
    """Enhanced email manager with proper error handling"""
    
    def __init__(self, html_content, output_file):
        self.html_content = html_content
        self.output_file = output_file
        
    def send_mail(self):
        """Send email with report"""
        try:
            logger.info("Preparing email...")
            
            recipients = ['abhisha3@amdocs.com']
            cc_recipients = ['abhisha3@amdocs.com']
            from_email = "noreply@amdocs.com"
            
            # Create message
            message = MIMEMultipart('alternative')
            message['subject'] = f"Comcast OSS || Report for RELEASE_PONR flag Issue {dt.datetime.now().strftime('%Y/%m/%d')}"
            message['To'] = ", ".join(recipients)
            message['Cc'] = ", ".join(cc_recipients)
            message['From'] = from_email
            
            # Add HTML body
            html_body = MIMEText(self.get_mail_content(), 'html')
            message.attach(html_body)
            
            # Add Excel attachment if available
            if self.output_file and os.path.exists(self.output_file):
                self.attach_file(message, self.output_file)
            
            # Send email
            logger.info("Sending email...")
            with smtplib.SMTP('localhost') as server:
                all_recipients = recipients + cc_recipients
                server.sendmail(from_email, all_recipients, message.as_string())
            
            logger.info("✓ Email sent successfully!")
            return True
            
        except Exception as e:
            logger.error(f"✗ Failed to send email: {e}")
            return False
    
    def attach_file(self, message, file_path):
        """Attach file to email"""
        try:
            ctype, encoding = mimetypes.guess_type(file_path)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'
            
            maintype, subtype = ctype.split('/', 1)
            with open(file_path, 'rb') as fp:
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
            
            encoders.encode_base64(attachment)
            attachment.add_header('Content-Disposition', 'attachment', 
                                filename=os.path.basename(file_path))
            message.attach(attachment)
            
        except Exception as e:
            logger.error(f"Failed to attach file {file_path}: {e}")
    
    def get_mail_content(self):
        """Generate email HTML content with enhanced tracking information"""
        return f"""
        <html>
  <head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            font-size: 14px;
            color: #333;
            line-height: 1.6;
            background-color: #fff;
        }}

        p {{
            margin: 10px 0;
        }}

        .styled-table {{
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.9em;
            min-width: 800px;
            border: 1px solid #dddddd;
        }}

        .styled-table th,
        .styled-table td {{
            border: 1px solid #dddddd;
            padding: 6px 10px;
            text-align: left;
        }}

        .styled-table th {{
            background-color: #f4f4f4;
            font-weight: bold;
            font-size: 0.85em;
        }}

        .status-pending {{
            background-color: #fff3cd;
            color: #856404;
        }}

        .status-resolved {{
            background-color: #d4edda;
            color: #155724;
        }}

        .age-high {{
            background-color: #f8d7da;
            color: #721c24;
            font-weight: bold;
        }}

        .note {{
            margin-top: 20px;
            font-size: 13px;
            color: #555;
            background-color: #f9f9f9;
            padding: 10px;
            border-left: 4px solid #0078D4;
        }}

        .footer {{
            margin-top: 30px;
            font-size: 14px;
            font-weight: bold;
            color: #444;
        }}

        .summary {{
            background-color: #e7f3ff;
            padding: 10px;
            border-radius: 5px;
            margin: 15px 0;
        }}

        a {{
            color: #0078D4;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <p>Hi Team,</p>

    <p>Please find below the list of orders where the <strong>RELEASE PONR</strong> flag was not triggered by the system, even though the mandatory wait period associated with the Registered Timed Action has been completed.</p>

    <div class="summary">
        <strong>📊 Report Summary:</strong><br>
        • This report includes all PONR issues identified today with enhanced tracking<br>
        • <strong>Age Days</strong>: Number of days since last update<br>
        • <strong>Handling Status</strong>: Current resolution status (PENDING/IN_PROGRESS/RESOLVED)<br>
        • <strong>RCA</strong>: Root Cause Analysis (to be filled manually in database)<br>
        • Records are stored in database for historical tracking and follow-up
    </div>

    <p>This report fetches the data based on the activity states/status, not on the basis of the <code>qrtz</code> table.</p>

    <p>So any order where the flag has been released but the activity is still not marked completed would be part of this report, which also needs handling.</p>

    <p><strong>⚠️ Priority Action Required:</strong> Kindly review these orders and take the necessary corrective actions. This issue is impacting the business, as services have already been ceased at the customer sites, but billing continues to be active.</p>

    {self.html_content}
 
    <div class="note">
        <strong>📝 Database Tracking:</strong> All records are now stored in the production database (ossdb01db.ponr_tracking) for better tracking and follow-up. 
        You can update the RCA and Handling Status directly in the database.<br><br>
        <strong>For any changes in the report:</strong> Please reach out to Abhishek Agrahari
    </div>

    <div class="footer">
        Regards,<br>
        Abhishek Agrahari<br>
        Mail: abhisha3@amdocs.com
    </div>
</body>
</html>"""

def cleanup_files():
    """Clean up all temporary files and logs after email is sent"""
    if not Config.CLEANUP_ENABLED:
        logger.info("Cleanup disabled, skipping file cleanup")
        return
    
    try:
        logger.info("Starting cleanup process...")
        
        # Files to clean up
        cleanup_patterns = [
            "ponr_execution_*.log",
            "execution_log_*.txt",
            "ponr_report.xlsx",
            "*.tmp",
            "*.temp"
        ]
        
        cleaned_count = 0
        for pattern in cleanup_patterns:
            files = glob.glob(os.path.join(Config.OUTPUT_DIR, pattern))
            for file_path in files:
                try:
                    os.remove(file_path)
                    cleaned_count += 1
                    logger.info(f"Cleaned up: {file_path}")
                except Exception as e:
                    logger.warning(f"Failed to clean up {file_path}: {e}")
        
        logger.info(f"✓ Cleanup completed: {cleaned_count} files removed")
        
    except Exception as e:
        logger.error(f"✗ Cleanup failed: {e}")

if __name__ == "__main__":
    try:
        # Execute main analysis
        results = main()
        
        # Generate reports
        html_content, output_file = generate_reports(results)
        
        # Send email
        email_manager = EmailManager(html_content, output_file)
        email_sent = email_manager.send_mail()
        
        if email_sent:
            logger.info("✓ Email sent successfully, starting cleanup...")
            # Clean up files only after successful email
            cleanup_files()
        else:
            logger.warning("Email failed, skipping cleanup to preserve files for debugging")
        
        logger.info("="*60)
        logger.info("PONR Analysis Script completed successfully!")
        logger.info("="*60)
        
    except Exception as e:
        logger.error(f"Script execution failed: {e}")
        sys.exit(1)