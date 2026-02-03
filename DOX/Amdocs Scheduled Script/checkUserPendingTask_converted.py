#!/usr/bin/env python3
"""
#############################################################################
# NAME        : Check Pending User Task Impacting Billing
# AUTHOR      : Abhishek Agrahari && Prateek Jain
# DATE        : 12/11/2024
# DESCRIPTION : Check User Pending Task which are impacting Billing and generate report
# CONVERTED   : Shell script to Python
#############################################################################
"""

import datetime as dt
import logging
import smtplib
import mimetypes
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import psycopg2
import os
import sys
import traceback
from pathlib import Path


# ============================================================================
# CONFIGURATION
# ============================================================================

# ============================================================================
# TOGGLE FOR TESTING
# ============================================================================
# Set TEST_MODE = True to send emails to test recipient only
# Set TEST_MODE = False to send emails to production recipients
TEST_MODE = True  # ← CHANGE THIS TO False FOR PRODUCTION

# ============================================================================

DB_CONFIG = {
    'database': 'prodossdb',
    'user': 'ossdb01uams',
    'password': 'Pr0d_ossdb01uams',
    'host': 'oso-pstgr-rd.orion.comcast.com',
    'port': '6432'
}

# Production Recipients
PRODUCTION_RECIPIENTS = [
    'abhisha3@amdocs.com',
    'prateek.jain5@amdocs.com',
    'anarghaarsha_alexander@comcast.com',
    'chandradeepthi_doruvupalagiri@comcast.com',
    'venkataraghavendrakalyan_ankem@comcast.com',
    'sonalika_sapra2@comcast.com',
    'joseph_thottukadavil@cable.comcast.com',
    'Nishant.Bhatia@amdocs.com',
    'Enna.Arora@amdocs.com',
    'RAJIVKUM@amdocs.com',
    'mukul.bhasin@amdocs.com',
    'daleszandro_jasper@cable.comcast.com',
    'Natasha.Deshpande@amdocs.com'
]

# Test Recipient
TEST_RECIPIENT = ['abhisha3@amdocs.com']

# Email Configuration - Recipients are determined by TEST_MODE
EMAIL_CONFIG = {
    'recipients': TEST_RECIPIENT if TEST_MODE else PRODUCTION_RECIPIENTS,
    'cc_recipients': [],  # Optional CC recipients
    'from': 'noreplyreports@amdocs.com',
    'error_recipients': ['abhisha3@amdocs.com']
}

# Frequency configuration: Script runs daily (every 1 day)
EXECUTION_FREQUENCY = 1

# Directory for logs and output files
LOGS_DIR = Path("LOGS")
LOGS_DIR.mkdir(exist_ok=True)

# Timestamp for file naming
TIMESTAMP = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = LOGS_DIR / f"checkUserPendingTask_{TIMESTAMP}.log"
HTML_FILE = f"checkUserPendingTask_{TIMESTAMP}.html"
EXCEL_FILE = f"checkUserPendingTask_{TIMESTAMP}.xlsx"


# ============================================================================
# LOGGING SETUP
# ============================================================================
def setup_logging():
    """
    Configure logging to write to both console and file
    Includes automatic log rotation and cleanup of old logs
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE, mode='w')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    logging.info("=" * 80)
    logging.info("Script: Check User Pending Task Impacting Billing")
    logging.info(f"Start Time: {dt.datetime.now()}")
    logging.info("=" * 80)


def cleanup_old_logs(days_to_keep=30):
    """
    C   lean up old log, HTML, and Excel files older than specified days
    
    Args:
        days_to_keep (int): Number of days to retain files
    """
    try:
        current_time = dt.datetime.now()
        cutoff_time = current_time - dt.timedelta(days=days_to_keep)
        
        deleted_count = 0
        
        # Clean up log files
        for log_file in LOGS_DIR.glob("checkUserPendingTask_*.log"):
            file_time = dt.datetime.fromtimestamp(log_file.stat().st_mtime)
            if file_time < cutoff_time:
                log_file.unlink()
                deleted_count += 1
        
        # Clean up HTML files
        for html_file in LOGS_DIR.glob("checkUserPendingTask_*.html"):
            file_time = dt.datetime.fromtimestamp(html_file.stat().st_mtime)
            if file_time < cutoff_time:
                html_file.unlink()
                deleted_count += 1
        
        # Clean up Excel files
        for excel_file in LOGS_DIR.glob("checkUserPendingTask_*.xlsx"):
            file_time = dt.datetime.fromtimestamp(excel_file.stat().st_mtime)
            if file_time < cutoff_time:
                excel_file.unlink()
                deleted_count += 1
        
        if deleted_count > 0:
            logging.info(f"Cleaned up {deleted_count} old files (logs, HTML, Excel)")
    except Exception as e:
        logging.warning(f"Error during file cleanup: {e}")


# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================
def get_db_connection():
    """
    Establish and return PostgreSQL database connection
    
    Returns:
        psycopg2.connection: Database connection object
    
    Raises:
        SystemExit: If connection fails
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logging.info("Database connection established successfully")
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        send_error_notification(f"Database connection failed: {e}")
        sys.exit(1)


def check_execution_day():
    """
    Check if script should execute based on day of month
    Script runs every Nth day based on EXECUTION_FREQUENCY
    
    Returns:
        bool: True if script should execute, False otherwise
    """
    current_day = dt.datetime.now().day
    should_execute = (current_day % EXECUTION_FREQUENCY == 0)
    
    if should_execute:
        logging.info(f"Execution check passed: Day {current_day} is a multiple of {EXECUTION_FREQUENCY}")
    else:
        logging.info(f"Execution skipped: Day {current_day} is not a multiple of {EXECUTION_FREQUENCY}")
    
    return should_execute


def fetch_pending_tasks_batch(cursor, part_id_batch):
    """
    Fetch pending user tasks using the EXACT working query from shell script
    Only modification: batch part_id values in groups of 10
    
    Args:
        cursor: Database cursor
        part_id_batch (list): List of part_id values (max 10)
    
    Returns:
        list: Query results as list of tuples
    """
    # EXACT working query from shell script - DO NOT MODIFY except part_id list
    part_id_list = ','.join(map(str, part_id_batch))
    
    query = f"""
    select spoi.id as projectid,
           oas.value as customer_id,
           oas2.value as site_id,
           oas4.value as projectOwnerName,
           oas5.value as siteName,
           oas6.value as PTD,
           o1.entity_name,
           spoi.name,
           oai.last_update_date,
           oai.create_date,
           oai.status,
           spoi.status,
           oai.id as activity_id,
           oai.spec_ver_id
    from ossdb01db.sc_project_order_instance spoi,
         ossdb01db.oss_activity_instance oai,
         ossdb01ref.oss_ref_data o1,
         ossdb01ref.oss_ref_attribute o2,
         ossdb01db.oss_attribute_store oas,
         ossdb01db.oss_attribute_store oas2,
         ossdb01db.oss_attribute_store oas4,
         ossdb01db.oss_attribute_store oas5,
         ossdb01db.oss_attribute_store oas6 
    where oai.part_id in({part_id_list})
          and oai.implementation_type = 'Manual' 
          and oai.spec_ver_id in('5bf0536f-4798-4674-b811-f0c40cd9f967',
                                  '800f1e6c-a19d-4851-8c33-caf6df02e7fb',
                                  'e7cd1c8f-f778-4e6d-aa2b-43240bce64d4',
                                  '234487e7-7dfa-4f09-a7db-6de805f7ff23',
                                  '6e9c8fb9-078e-4711-baee-cd31a4dfed61',
                                  '1e1f81de-aea5-4f1c-a621-8daed5a11842',
                                  '93d43aae-8e7b-4950-a358-1c302bb948a6',
                                  'f8dec3e6-143b-49db-b0a3-3f2362ffc20a',
                                  'fa571a98-8774-45a5-9f43-d7f557385333',
                                  '800f1e6c-a19d-4851-8c33-caf6df02e7fb') 
          and oai.state in ('In Progress', 'Rework In Progress')
          and oai.last_update_date < current_date - interval '30' day 
          and spoi.plan_id = oai.plan_id 
          and spoi.manager is distinct from 'ProductionSanity' 
          and oai.is_latest_version = 1 
          and spoi.is_latest_version = 1 
          and spoi.name not like '%MM_PROD_TEST%'
          and spoi.status not like 'FCANCELLED' 
          and o2.attribute_value = oai.spec_ver_id 
          and o1.entity_id = o2.entity_id 
          and oas.parent_id = spoi.objid 
          and oas2.parent_id = spoi.objid 
          and oas4.parent_id = spoi.objid 
          and oas5.parent_id = spoi.objid 
          and oas6.parent_id = spoi.objid 
          and oas.code like 'customerID' 
          and oas2.code like 'siteId' 
          and oas4.code like 'projectOwnerName' 
          and oas5.code like 'siteName' 
          and oas6.code like 'DMD_PTD'
    ORDER BY o1.entity_name ASC
    """
    
    try:
        logging.info(f"Executing query for part_id batch: {part_id_batch}")
        cursor.execute(query)
        results = cursor.fetchall()
        
        record_count = len(results) if results else 0
        logging.info(f"✓ BATCH COMPLETE: Fetched {record_count} records for part_id {part_id_batch}")
        
        if record_count > 0:
            logging.info(f"  → Sample first record columns count: {len(results[0])}")
        
        return results
    except Exception as e:
        logging.error(f"✗ ERROR in batch {part_id_batch}")
        logging.error(f"Error details: {type(e).__name__} - {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        return []


def fetch_workqueue(cursor, activity_id):
    """
    Fetch workqueue for a given activity_id
    
    Args:
        cursor: Database cursor
        activity_id: Activity ID from oai.id
    
    Returns:
        str: WorkQueue name or 'N/A'
    """
    query = """
    select text_ 
    from act_ru_variable 
    where task_id_ in (
        select task_id_ 
        from act_ru_variable arv 
        where text_ = %s 
        and name_ = 'activityId'
    ) 
    and name_ in ('WorkQueue')
    """
    
    try:
        # Convert activity_id to string and log
        activity_id_str = str(activity_id)
        logging.info(f"    → Querying WorkQueue for activity_id: {activity_id_str}")
        
        # Execute query
        cursor.execute(query, (activity_id_str,))
        result = cursor.fetchone()
        
        if result:
            workqueue = result[0]
            logging.info(f"    ✓ Found WorkQueue: {workqueue}")
            return workqueue
        else:
            logging.warning(f"    ✗ No WorkQueue found in database")
            # Try to debug - check if this activity_id exists in act_ru_variable
            try:
                debug_query = """
                select count(*) 
                from act_ru_variable 
                where text_ = %s and name_ = 'activityId'
                """
                cursor.execute(debug_query, (activity_id_str,))
                count = cursor.fetchone()[0]
                logging.warning(f"    → Debug: Found {count} rows with activityId={activity_id_str} in act_ru_variable")
                
                if count == 0:
                    logging.warning(f"    → This activity_id doesn't exist in act_ru_variable table!")
            except Exception as debug_e:
                logging.warning(f"    → Debug query failed: {debug_e}")
            return 'N/A'
            
    except Exception as e:
        logging.error(f"    ✗ Database error for activity_id={activity_id}: {e}")
        logging.error(f"    → Query was: {query}")
        logging.error(f"    → Parameter: {activity_id}")
        return 'N/A'


def create_summary_table(df):
    """
    Create summary table with task counts and age ranges
    
    Args:
        df (pd.DataFrame): Main data with all tasks
    
    Returns:
        pd.DataFrame: Summary table
    """
    logging.info("Creating summary table...")
    
    if df.empty:
        logging.warning("No data to summarize")
        return pd.DataFrame()
    
    summary_data = []
    
    # Group by Entity Name
    grouped = df.groupby('Entity Name')
    
    for entity_name, group in grouped:
        total_count = len(group)
        
        # Calculate age ranges based on Age column
        last_1_month = len(group[group['Age'] <= 30])
        previous_1_month = len(group[(group['Age'] > 30) & (group['Age'] <= 60)])
        last_3_months = len(group[group['Age'] <= 90])
        last_6_months = len(group[group['Age'] <= 180])
        last_1_year = len(group[group['Age'] <= 365])
        
        summary_data.append({
            'Task Name': entity_name,
            'Total Count': total_count,
            'Last 1 Month': last_1_month,
            'Previous 1 Month': previous_1_month,
            'Last 3 Months': last_3_months,
            'Last 6 Months': last_6_months,
            'Last 1 Year': last_1_year
        })
        
        logging.info(f"  {entity_name}: Total={total_count}, 1M={last_1_month}, 3M={last_3_months}")
    
    summary_df = pd.DataFrame(summary_data)
    
    logging.info(f"✓ Summary table created with {len(summary_df)} rows")
    
    return summary_df


def pull_all_pending_tasks():
    """
    Pull all pending tasks using the exact working query from shell script
    Batches part_id values in groups of 10 to avoid timeout
    
    Returns:
        pd.DataFrame: Combined results from all queries
    """
    # All part_id values (1-99)
    all_part_ids = list(range(1, 100))
    
    # Batch size
    batch_size = 10
    
    all_results = []
    column_names = [
        'Project ID', 'Customer ID', 'Site ID', 'Project Owner Name', 
        'Site Name', 'PTD', 'Entity Name', 'Project Name',
        'Last Update Date', 'Create Date', 'Activity Status', 
        'Project Status', 'Activity ID', 'Spec Ver ID'
    ]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        logging.info("=" * 80)
        logging.info("STARTING DATA FETCH")
        logging.info("=" * 80)
        logging.info(f"Total part_ids to process: {len(all_part_ids)}")
        logging.info(f"Batch size: {batch_size}")
        logging.info(f"Number of batches: {len(range(0, len(all_part_ids), batch_size))}")
        logging.info("-" * 80)
        
        # Process part_ids in batches of 10
        batch_number = 1
        total_batches = len(range(0, len(all_part_ids), batch_size))
        
        for i in range(0, len(all_part_ids), batch_size):
            part_id_batch = all_part_ids[i:i + batch_size]
            logging.info(f"\n>>> BATCH {batch_number}/{total_batches}")
            
            results = fetch_pending_tasks_batch(cursor, part_id_batch)
            all_results.extend(results)
            
            # Show running total
            logging.info(f">>> Running Total: {len(all_results)} records so far")
            batch_number += 1
        
        logging.info("-" * 80)
        logging.info(f"✓ DATA FETCH COMPLETE")
        logging.info(f"✓ TOTAL RECORDS FETCHED: {len(all_results)}")
        logging.info("=" * 80)
        
        # Convert to DataFrame
        if all_results:
            df = pd.DataFrame(all_results, columns=column_names)
            logging.info(f"✓ DataFrame created successfully with {len(df)} rows and {len(df.columns)} columns")
            
            # Calculate Age column (days since last_update_date)
            logging.info("Calculating Age column...")
            df['Age'] = (pd.Timestamp.now() - pd.to_datetime(df['Last Update Date'])).dt.days
            logging.info(f"✓ Age column added (range: {df['Age'].min()} to {df['Age'].max()} days)")
            
            logging.info(f"  Columns: {', '.join(df.columns.tolist())}")
        else:
            df = pd.DataFrame(columns=column_names + ['Age'])
            logging.warning("⚠ No pending tasks found - DataFrame is empty")
        
        return df
        
    except Exception as e:
        logging.error(f"Error during data fetch: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
        logging.info("Database connection closed")


# ============================================================================
# HTML GENERATION
# ============================================================================
def generate_charts_html(summary_df):
    """
    Generate visual charts HTML from summary data
    
    Args:
        summary_df (pd.DataFrame): Summary table with task counts and age ranges
    
    Returns:
        str: HTML with charts
    """
    if summary_df is None or len(summary_df) == 0:
        return ""
    
    # Sort by total count descending for better visualization
    summary_sorted = summary_df.sort_values('Total Count', ascending=False).head(10)  # Top 10 tasks
    
    # Calculate max value for scaling
    max_count = summary_sorted['Total Count'].max()
    
    # Generate bar chart HTML for task distribution
    chart_html = """
    <div style="background-color: white; padding: 20px; margin: 20px 0; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h3 style="color: #004080; margin-top: 0;">📊 Task Distribution Overview</h3>
        <p style="color: #666;">Top tasks by count with age breakdown</p>
        <div style="margin-top: 20px;">
    """
    
    # Create horizontal bars for each task
    for idx, row in summary_sorted.iterrows():
        task_name = row['Task Name'][:50]  # Truncate long names
        total = row['Total Count']
        last_1m = row['Last 1 Month']
        prev_1m = row['Previous 1 Month']
        last_3m = row['Last 3 Months']
        
        # Calculate percentages for stacked bar
        bar_width = (total / max_count) * 100
        last_1m_pct = (last_1m / total * bar_width) if total > 0 else 0
        prev_1m_pct = (prev_1m / total * bar_width) if total > 0 else 0
        older_pct = bar_width - last_1m_pct - prev_1m_pct
        
        chart_html += f"""
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                <span style="font-weight: bold; font-size: 0.9em; color: #333;">{task_name}</span>
                <span style="font-size: 0.85em; color: #666;">Total: {total}</span>
            </div>
            <div style="background-color: #e0e0e0; height: 30px; border-radius: 5px; overflow: hidden; position: relative;">
                <div style="display: flex; height: 100%;">
                    <div style="background-color: #dc3545; width: {last_1m_pct}%; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.75em; font-weight: bold;" title="Last 1 Month: {last_1m}">
                        {last_1m if last_1m > 0 else ''}
                    </div>
                    <div style="background-color: #ffc107; width: {prev_1m_pct}%; display: flex; align-items: center; justify-content: center; color: #333; font-size: 0.75em; font-weight: bold;" title="Previous 1 Month: {prev_1m}">
                        {prev_1m if prev_1m > 0 else ''}
                    </div>
                    <div style="background-color: #17a2b8; width: {older_pct}%; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.75em; font-weight: bold;" title="Older: {total - last_1m - prev_1m}">
                        {total - last_1m - prev_1m if (total - last_1m - prev_1m) > 0 else ''}
                    </div>
                </div>
            </div>
        </div>
        """
    
    # Add legend
    chart_html += """
        </div>
        <div style="margin-top: 20px; padding: 10px; background-color: #f8f9fa; border-radius: 5px;">
            <strong>Legend:</strong>
            <span style="margin-left: 15px;"><span style="display: inline-block; width: 15px; height: 15px; background-color: #dc3545; border-radius: 3px; margin-right: 5px;"></span>Last 1 Month (Critical)</span>
            <span style="margin-left: 15px;"><span style="display: inline-block; width: 15px; height: 15px; background-color: #ffc107; border-radius: 3px; margin-right: 5px;"></span>Previous 1 Month (High)</span>
            <span style="margin-left: 15px;"><span style="display: inline-block; width: 15px; height: 15px; background-color: #17a2b8; border-radius: 3px; margin-right: 5px;"></span>Older (Medium)</span>
        </div>
    </div>
    """
    
    return chart_html


def generate_html_report(df, summary_df=None):
    """
    Generate HTML report from DataFrame with styled table and visual charts
    
    Args:
        df (pd.DataFrame): Main data to include in the report
        summary_df (pd.DataFrame): Summary table (optional)
    
    Returns:
        str: HTML content
    """
    css_style = """
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background-color: #004080;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .description {
            background-color: white;
            padding: 15px;
            margin-bottom: 20px;
            border-left: 4px solid #004080;
            border-radius: 3px;
        }
        .styled-table {
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 0.9em;
            font-family: sans-serif;
            min-width: 100%;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            background-color: white;
        }
        .styled-table thead tr {
            background-color: #004080;
            color: #ffffff;
            text-align: left;
        }
        .styled-table th,
        .styled-table td {
            padding: 12px 15px;
            border: 1px solid #dddddd;
        }
        .styled-table tbody tr {
            border-bottom: 1px solid #dddddd;
        }
        .styled-table tbody tr:nth-of-type(even) {
            background-color: #f3f3f3;
        }
        .styled-table tbody tr:hover {
            background-color: #e8f4f8;
        }
        .footer {
            margin-top: 30px;
            padding: 15px;
            background-color: white;
            border-radius: 3px;
            font-size: 0.9em;
            color: #666;
        }
        .record-count {
            background-color: #28a745;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
        }
    </style>
    """
    
    header_html = """
    <div class="header">
        <h1>Orion User Pending Task Report</h1>
        <h3>Tasks Impacting Billing and Rebill</h3>
    </div>
    """
    
    description_html = f"""
    <div class="description">
        <h4>Report Description</h4>
        <p>This is an Amdocs generated report for all pending User tasks impacting Billing.</p>
        <p>Please take follow-up action with the respective work queue or task owner.</p>
        <p><strong>Report Generated:</strong> {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    """
    
    record_count_html = f"""
    <div class="record-count">
        Total Pending Tasks Found: {len(df)}
    </div>
    """
    
    # Generate Visual Charts (shown first)
    charts_html = generate_charts_html(summary_df) if summary_df is not None else ""
    
    # Generate Summary Table HTML
    summary_html = ""
    if summary_df is not None and len(summary_df) > 0:
        summary_html = f"""
        <h2 style="color: #004080; margin-top: 30px;">📋 Summary by Task Type</h2>
        <p><strong>This table shows aggregated counts by task name with age ranges and work queues.</strong></p>
        {summary_df.to_html(index=False, classes='styled-table', escape=False)}
        <hr style="margin: 40px 0;">
        """
    
    # Convert Main DataFrame to HTML
    detailed_table_header = "<h2 style='color: #004080; margin-top: 30px;'>Detailed Task List</h2>"
    if len(df) > 0:
        table_html = detailed_table_header + df.to_html(index=False, classes='styled-table', escape=False)
    else:
        table_html = "<p style='text-align:center; padding:20px; background-color:white;'>No pending tasks found.</p>"
    
    footer_html = """
    <div class="footer">
        <p><strong>Note:</strong> This report includes manual activities that have not been updated for more than 30 days.</p>
        <p><strong>For any changes or clarification, please reach out to:</strong> Abhishek Agrahari (<a href="mailto:abhisha3@amdocs.com">abhisha3@amdocs.com</a>)</p>
        <hr style="margin: 20px 0;">
        <div style="margin-top: 20px;">
            <p style="margin: 5px 0;"><strong>Thanks & Regards,</strong></p>
            <p style="margin: 5px 0;"><strong>Abhishek Agrahari</strong></p>
        </div>
        <hr style="margin: 20px 0;">
        <p style="text-align: center; color: #999; font-size: 0.85em;">Automated Report - Do Not Reply</p>
    </div>
    """
    
    # Combine all HTML parts
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Orion User Pending Task Report</title>
        {css_style}
    </head>
    <body>
        {header_html}
        {description_html}
        {record_count_html}
        {charts_html}
        {summary_html}
        {table_html}
        {footer_html}
    </body>
    </html>
    """
    
    return full_html


def save_html_report(html_content):
    """
    Save HTML content to file
    
    Args:
        html_content (str): HTML content to save
    """
    try:
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logging.info(f"HTML report saved: {HTML_FILE}")
    except Exception as e:
        logging.error(f"Error saving HTML report: {e}")
        raise


def save_excel_report(df, summary_df=None):
    """
    Save DataFrame to Excel file with two sheets
    
    Args:
        df (pd.DataFrame): Main data to export to Excel
        summary_df (pd.DataFrame): Summary data (optional)
    """
    try:
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
            # Sheet 1: Summary (if available)
            if summary_df is not None and len(summary_df) > 0:
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                logging.info(f"  Sheet 'Summary' added with {len(summary_df)} rows")
            
            # Sheet 2: Detailed data
            df.to_excel(writer, sheet_name='Detailed Tasks', index=False)
            logging.info(f"  Sheet 'Detailed Tasks' added with {len(df)} rows")
            
        logging.info(f"Excel report saved: {EXCEL_FILE}")
    except Exception as e:
        logging.error(f"Error saving Excel report: {e}")
        raise


# ============================================================================
# EMAIL FUNCTIONS
# ============================================================================
class EmailMgr:
    """Email manager class for sending reports - matches Outage_Report.py pattern"""
    
    def __init__(self, html_content, subject, excel_file=None):
        """
        Initialize email manager
        
        Args:
            html_content (str): HTML content to send
            subject (str): Email subject line
            excel_file (str): Path to Excel file to attach (optional)
        """
        self.html_content = html_content
        self.subject = subject
        self.excel_file = excel_file
    
    def send_mail(self):
        """Send HTML email with the generated report and Excel attachment"""
        logging.info("=" * 80)
        logging.info("PREPARING EMAIL")
        logging.info("=" * 80)
        
        recipients = EMAIL_CONFIG['recipients']
        cc_recipients = EMAIL_CONFIG.get('cc_recipients', [])
        FROM = EMAIL_CONFIG['from']
        
        logging.info(f"From: {FROM}")
        logging.info(f"To Recipients: {len(recipients)}")
        for i, r in enumerate(recipients, 1):
            logging.info(f"  {i}. {r}")
        if cc_recipients:
            logging.info(f"CC Recipients: {len(cc_recipients)}")
            for i, r in enumerate(cc_recipients, 1):
                logging.info(f"  {i}. {r}")
        logging.info(f"Subject: {self.subject}")
        
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = self.subject
        MESSAGE['To'] = ", ".join(recipients)
        if cc_recipients:
            MESSAGE['Cc'] = ", ".join(cc_recipients)
        MESSAGE['From'] = FROM
        
        # Attach HTML content
        HTML_BODY = MIMEText(self.html_content, 'html')
        MESSAGE.attach(HTML_BODY)
        logging.info(f"✓ HTML body attached (size: {len(self.html_content)} bytes)")
        
        # Attach Excel file if provided
        if self.excel_file and os.path.exists(self.excel_file):
            try:
                excel_size = os.path.getsize(self.excel_file)
                logging.info(f"Attaching Excel file: {self.excel_file} (size: {excel_size} bytes)")
                
                ctype, encoding = mimetypes.guess_type(self.excel_file)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'
                
                maintype, subtype = ctype.split('/', 1)
                with open(self.excel_file, 'rb') as fp:
                    attachment = MIMEBase(maintype, subtype)
                    attachment.set_payload(fp.read())
                encoders.encode_base64(attachment)
                
                # Use just the filename for the attachment, not full path
                filename = os.path.basename(self.excel_file)
                attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                MESSAGE.attach(attachment)
                logging.info(f"✓ Excel file attached: {filename}")
            except Exception as e:
                logging.warning(f"⚠ Failed to attach Excel file: {e}")
        else:
            logging.info(f"Excel file not found or not provided: {self.excel_file}")
        
        try:
            logging.info("-" * 80)
            logging.info("SENDING EMAIL...")
            logging.info(f"Connecting to SMTP server: localhost")
            
            server = smtplib.SMTP('localhost')
            logging.info("✓ Connected to SMTP server")
            
            all_recipients = recipients.copy()
            if cc_recipients:
                all_recipients.extend(cc_recipients)
            
            logging.info(f"Sending to {len(all_recipients)} total recipients...")
            server.sendmail(FROM, all_recipients, MESSAGE.as_string())
            server.quit()
            
            logging.info("=" * 80)
            logging.info(f"✓✓✓ EMAIL SENT SUCCESSFULLY to {len(all_recipients)} recipients!")
            logging.info("=" * 80)
        except Exception as e:
            logging.error("=" * 80)
            logging.error(f"✗✗✗ FAILED TO SEND EMAIL")
            logging.error(f"Error: {type(e).__name__} - {str(e)}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            logging.error("=" * 80)
            raise


def send_html_email(html_file, subject, excel_file=None):
    """
    Send HTML email with the generated report and Excel attachment
    Uses the same pattern as Outage_Report.py
    
    Args:
        html_file (str): Path to HTML file to send
        subject (str): Email subject line
        excel_file (str): Path to Excel file to attach (optional)
    """
    try:
        # Read HTML content
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Use EmailMgr class (same as reference script) with Excel attachment
        em = EmailMgr(html_content, subject, excel_file)
        em.send_mail()
        
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        raise


def send_error_notification(error_message):
    """
    Send error notification email
    
    Args:
        error_message (str): Error message to include in email
    """
    try:
        subject = "FAILURE - Orion User Pending Task Report"
        body = f"""
        <html>
        <body>
            <h2 style="color: red;">Script Execution Failed</h2>
            <p><strong>Script:</strong> Check User Pending Task</p>
            <p><strong>Time:</strong> {dt.datetime.now()}</p>
            <p><strong>Error:</strong></p>
            <pre>{error_message}</pre>
        </body>
        </html>
        """
        
        recipients = EMAIL_CONFIG['error_recipients']
        FROM = EMAIL_CONFIG['from']
        
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['Subject'] = subject
        MESSAGE['From'] = FROM
        MESSAGE['To'] = ", ".join(recipients)
        
        HTML_BODY = MIMEText(body, 'html')
        MESSAGE.attach(HTML_BODY)
        
        server = smtplib.SMTP('localhost')
        server.sendmail(FROM, recipients, MESSAGE.as_string())
        server.quit()
        
        logging.info("Error notification sent")
        
    except Exception as e:
        logging.error(f"Failed to send error notification: {e}")


def send_skip_notification():
    """
    Send notification email when script execution is skipped
    """
    try:
        current_day = dt.datetime.now().day
        subject = f"INFO - Orion User Pending Task Report - Execution Skipped (Day {current_day})"
        body = f"""
        <html>
        <body>
            <h3>Script Execution Skipped</h3>
            <p>The User Pending Task report is scheduled to run every {EXECUTION_FREQUENCY}th day of the month.</p>
            <p><strong>Current Day:</strong> {current_day}</p>
            <p><strong>Next Execution:</strong> Day {((current_day // EXECUTION_FREQUENCY) + 1) * EXECUTION_FREQUENCY}</p>
            <p>No action required.</p>
        </body>
        </html>
        """
        
        recipients = EMAIL_CONFIG['error_recipients']
        FROM = EMAIL_CONFIG['from']
        
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['Subject'] = subject
        MESSAGE['From'] = FROM
        MESSAGE['To'] = ", ".join(recipients)
        
        HTML_BODY = MIMEText(body, 'html')
        MESSAGE.attach(HTML_BODY)
        
        server = smtplib.SMTP('localhost')
        server.sendmail(FROM, recipients, MESSAGE.as_string())
        server.quit()
        
        logging.info("Skip notification sent")
        
    except Exception as e:
        logging.error(f"Failed to send skip notification: {e}")


# ============================================================================
# CLEANUP FUNCTIONS
# ============================================================================
def cleanup_files():
    """
    Move generated files to LOGS directory for archival
    """
    try:
        # Move HTML file to LOGS directory
        if os.path.exists(HTML_FILE):
            dest_path = LOGS_DIR / HTML_FILE
            os.rename(HTML_FILE, dest_path)
            logging.info(f"Moved {HTML_FILE} to LOGS directory")
        
        # Move Excel file to LOGS directory
        if os.path.exists(EXCEL_FILE):
            dest_path = LOGS_DIR / EXCEL_FILE
            os.rename(EXCEL_FILE, dest_path)
            logging.info(f"Moved {EXCEL_FILE} to LOGS directory")
        
        logging.info("Cleanup completed successfully")
        
    except Exception as e:
        logging.warning(f"Error during cleanup: {e}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================
def main():
    """
    Main execution function
    Orchestrates the entire script workflow
    """
    # Setup logging
    setup_logging()
    
    # Log execution mode
    logging.info("=" * 80)
    logging.info("SCRIPT CONFIGURATION")
    logging.info("=" * 80)
    mode = "TEST MODE (emails to abhisha3@amdocs.com only)" if TEST_MODE else "PRODUCTION MODE (emails to all recipients)"
    logging.info(f"🔧 Execution Mode: {mode}")
    logging.info(f"📅 Execution Frequency: Every {EXECUTION_FREQUENCY} day(s)")
    logging.info(f"📧 Recipients: {len(EMAIL_CONFIG['recipients'])} recipient(s)")
    if TEST_MODE:
        logging.info(f"   ⚠️  TEST MODE ACTIVE - Sending to: {', '.join(EMAIL_CONFIG['recipients'])}")
    else:
        logging.info(f"   ✅ PRODUCTION MODE - Sending to {len(EMAIL_CONFIG['recipients'])} recipients")
    logging.info("=" * 80)
    logging.info("")
    
    try:
        # Clean up old logs
        cleanup_old_logs(days_to_keep=30)
        
        # Check if script should execute today
        if not check_execution_day():
            logging.info("Script execution skipped based on day of month")
            send_skip_notification()
            cleanup_files()
            logging.info("Script completed (skipped)")
            return 0
        
        # Fetch pending tasks data
        logging.info("\n")
        logging.info("=" * 80)
        logging.info("STEP 1: FETCHING PENDING TASKS DATA")
        logging.info("=" * 80)
        df_pending_tasks = pull_all_pending_tasks()
        logging.info(f"✓ Data fetch completed. Records: {len(df_pending_tasks)}")
        
        # Create summary table
        logging.info("\n")
        logging.info("=" * 80)
        logging.info("STEP 2: CREATING SUMMARY TABLE")
        logging.info("=" * 80)
        df_summary = create_summary_table(df_pending_tasks)
        logging.info(f"✓ Summary table created with {len(df_summary)} task types")
        
        # Generate HTML report
        logging.info("\n")
        logging.info("=" * 80)
        logging.info("STEP 3: GENERATING HTML REPORT")
        logging.info("=" * 80)
        html_content = generate_html_report(df_pending_tasks, df_summary)
        logging.info(f"HTML content size: {len(html_content)} bytes")
        save_html_report(html_content)
        logging.info(f"✓ HTML report saved: {HTML_FILE}")
        logging.info(f"  File exists: {os.path.exists(HTML_FILE)}")
        if os.path.exists(HTML_FILE):
            logging.info(f"  File size: {os.path.getsize(HTML_FILE)} bytes")
        
        # Generate Excel report
        logging.info("\n")
        logging.info("=" * 80)
        logging.info("STEP 4: GENERATING EXCEL REPORT")
        logging.info("=" * 80)
        save_excel_report(df_pending_tasks, df_summary)
        logging.info(f"✓ Excel report saved: {EXCEL_FILE}")
        logging.info(f"  File exists: {os.path.exists(EXCEL_FILE)}")
        if os.path.exists(EXCEL_FILE):
            logging.info(f"  File size: {os.path.getsize(EXCEL_FILE)} bytes")
        
        # Send email with report and Excel attachment
        logging.info("\n")
        logging.info("=" * 80)
        logging.info("STEP 5: SENDING EMAIL")
        logging.info("=" * 80)
        subject = f"Report || Orion User Pending Task Impacting Billing || Rebill - {dt.datetime.now().strftime('%Y-%m-%d')}"
        logging.info(f"Subject: {subject}")
        logging.info(f"HTML File: {HTML_FILE}")
        logging.info(f"Excel File: {EXCEL_FILE}")
        send_html_email(HTML_FILE, subject, EXCEL_FILE)
        
        # Cleanup
        cleanup_files()
        
        logging.info("=" * 80)
        logging.info("Script completed successfully")
        logging.info(f"End Time: {dt.datetime.now()}")
        logging.info("=" * 80)
        
        return 0
        
    except Exception as e:
        logging.error("=" * 80)
        logging.error(f"Script failed with error: {e}")
        logging.error("=" * 80)
        
        # Send error notification
        try:
            send_error_notification(str(e))
        except:
            pass
        
        cleanup_files()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

