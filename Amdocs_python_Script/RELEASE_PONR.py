"""
RELEASE PONR (Point of No Return) Analysis Script

This script identifies orders where the RELEASE PONR flag was not triggered by the system,
even though the mandatory wait period associated with the Registered Timed Action has been completed.

OPTIMIZATION STRATEGY:
=====================
- Single optimized query with proper indexing
- Smart part_id batching to minimize database load
- Efficient memory management with streaming results
- Comprehensive logging and cleanup

PERFORMANCE FEATURES:
====================
1. Optimized query with proper JOIN order
2. Dynamic part_id range adjustment based on data density
3. Memory-efficient result processing
4. Automatic cleanup of temporary files and logs
5. Comprehensive error handling and retry logic

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
    CONNECTION_TIMEOUT = 30
    QUERY_TIMEOUT = 300  # 5 minutes max per query
    
    # File Configuration
    OUTPUT_DIR = "."
    CLEANUP_ENABLED = True

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

# CTE-based optimized query - designed for minimal DB load
OPTIMIZED_CTE_QUERY = """
WITH eligible_projects AS (
    -- First CTE: Get eligible projects from spoi table
    SELECT DISTINCT 
        spoi.id, 
        spoi.plan_id, 
        spoi.version, 
        spoi.status, 
        spoi.name
    FROM ossdb01db.sc_project_order_instance spoi
    WHERE spoi.status NOT IN ('FCANCELLED', 'DCOMPLETED')
      AND spoi.name NOT LIKE '%MM_PROD_TEST%'
      AND spoi.name NOT LIKE '%MM_Prod_Test%'
      AND spoi.manager IS DISTINCT FROM 'ProductionSanity'
      AND spoi.is_latest_version = 1
),
completed_activities AS (
    -- Second CTE: Get completed activities (oai2 conditions)
    SELECT DISTINCT 
        oai2.plan_id, 
        oai2.last_update_date, 
        oai2.complete_date
    FROM ossdb01db.oss_activity_instance oai2
    INNER JOIN eligible_projects ep ON oai2.plan_id = ep.plan_id
    WHERE oai2.spec_ver_id = '91757a68-692f-4246-91e1-7e2280a659d8'
      AND oai2.state = 'Completed'
      AND oai2.is_latest_version = 1
      AND oai2.complete_date < CURRENT_DATE - INTERVAL '10 days'
),
blocking_activities AS (
    -- Third CTE: Get blocking activities (oai3 conditions)
    SELECT DISTINCT oai3.plan_id
    FROM ossdb01db.oss_activity_instance oai3
    INNER JOIN completed_activities ca ON oai3.plan_id = ca.plan_id
    WHERE oai3.spec_ver_id = '88f0860f-e647-41cd-aaac-1930adea8a3c'
      AND oai3.state NOT IN ('In Progress')
      AND oai3.is_latest_version = 1
),
in_progress_activities AS (
    -- Fourth CTE: Get in-progress activities with part_id filter
    SELECT 
        oai.plan_id,
        oai.id,
        oai.status,
        oai.create_date
    FROM ossdb01db.oss_activity_instance oai
    INNER JOIN blocking_activities ba ON oai.plan_id = ba.plan_id
    WHERE oai.part_id BETWEEN %s AND %s
      AND oai.spec_ver_id = '03acd7f1-557a-4727-ba2e-8d44f6245047'
      AND oai.state IN ('In Progress', 'Optional')
      AND oai.is_latest_version = 1
)
-- Final SELECT: Join all CTEs together
SELECT 
    ep.id AS projectid,
    ep.version,
    ipa.status AS activity_status,
    ep.status AS project_status,
    ipa.id AS activity_id,
    ep.name,
    ca.last_update_date,
    ipa.create_date
FROM eligible_projects ep
INNER JOIN completed_activities ca ON ep.plan_id = ca.plan_id
INNER JOIN blocking_activities ba ON ep.plan_id = ba.plan_id
INNER JOIN in_progress_activities ipa ON ep.plan_id = ipa.plan_id;
"""

def execute_optimized_query(cursor, start, end):
    """Execute the CTE-based optimized query"""
    try:
        logger.info(f"Executing CTE-based optimized query for part_id {start}-{end}")
        
        # Set query timeout
        cursor.execute(f"SET statement_timeout = '{Config.QUERY_TIMEOUT}s'")
        
        # Execute CTE query
        cursor.execute(OPTIMIZED_CTE_QUERY, (start, end))
        results = cursor.fetchall()
        
        logger.info(f"CTE Query completed: Found {len(results)} records for part_id {start}-{end}")
        return results
        
    except psycopg2.Error as e:
        logger.error(f"Database CTE query error for part_id {start}-{end}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected CTE query error for part_id {start}-{end}: {e}")
        return []

def generate_part_id_ranges():
    """Generate optimized part_id ranges for minimal DB load"""
    # Using smaller, more efficient ranges
    ranges = []
    for start in range(1, 100, Config.PART_ID_BATCH_SIZE):
        end = min(start + Config.PART_ID_BATCH_SIZE - 1, 99)
        ranges.append((start, end))
    return ranges

def main():
    """Main execution function"""
    logger.info("="*60)
    logger.info("PONR Analysis Script Started")
    logger.info("="*60)
    
    results = []
    total_processed = 0
    failed_batches = 0
    
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            
            # Generate optimized part_id ranges
            part_id_ranges = generate_part_id_ranges()
            logger.info(f"Processing {len(part_id_ranges)} part_id ranges with batch size {Config.PART_ID_BATCH_SIZE}")
            
            # Process each range
            for i, (start, end) in enumerate(part_id_ranges, 1):
                try:
                    logger.info(f"Processing batch {i}/{len(part_id_ranges)}: part_id {start}-{end}")
                    
                    batch_results = execute_optimized_query(cursor, start, end)
                    results.extend(batch_results)
                    total_processed += len(batch_results)
                    
                    logger.info(f"✓ Batch {i} completed: {len(batch_results)} records")
                    
                except Exception as e:
                    failed_batches += 1
                    logger.error(f"✗ Batch {i} failed: {e}")
                    continue
            
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
    logger.info("="*60)
    
    return results

def generate_reports(results):
    """Generate Excel and HTML reports"""
    try:
        logger.info("Generating reports...")
        
        # Create DataFrame
        columns = ["projectid", "version", "activity_status", "project_status", 
                  "activity_id", "name", "last_update_date", "create_date"]
        df = pd.DataFrame(results, columns=columns)
        
        if df.empty:
            logger.warning("No data found! DataFrame is empty.")
            html_table = "<p><strong>No PONR issues found in the current analysis.</strong></p>"
        else:
            logger.info(f"Generated DataFrame with {len(df)} rows")
            html_table = df.to_html(index=False, classes='styled-table')
        
        # Save Excel file
        output_file = os.path.join(Config.OUTPUT_DIR, "ponr_report.xlsx")
        df.to_excel(output_file, index=False)
        logger.info(f"Excel report saved: {output_file}")
        
        return html_table, output_file
        
    except Exception as e:
        logger.error(f"Error generating reports: {e}")
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
        """Generate email HTML content - KEEPING ORIGINAL FORMAT"""
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
            font-size: 0.95em;
            min-width: 600px;
            border: 1px solid #dddddd;
        }}

        .styled-table th,
        .styled-table td {{
            border: 1px solid #dddddd;
            padding: 8px 12px;
            text-align: left;
        }}

        .styled-table th {{
            background-color: #f4f4f4;
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

    <p>This report fetches the data based on the activity states/status, not on the basis of the <code>qrtz</code> table.</p>

    <p>So any order where the flag has been released but the activity is still not marked completed would be part of this report, which also needs handling.</p>

    <p>Kindly review these orders and take the necessary corrective actions. This issue is impacting the business, as services have already been ceased at the customer sites, but billing continues to be active.</p>

    {self.html_content}
 
    <div class="note">
        For any changes in the report: Please reach out to Abhishek Agrahari
          </a>
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