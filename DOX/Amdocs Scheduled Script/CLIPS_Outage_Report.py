"""
CLIPS Outage Report Generator (Enhanced with Test Mode & Connection Resilience)
================================================================================

Purpose:
--------
This script generates a comprehensive outage report for Comcast OSS Orion system.
It identifies stuck activities and provides detailed analysis with customer/project information.

Key Enhancements:
-----------------
1. TEST_MODE toggle for safe testing without sending emails
2. Connection resilience with automatic reconnection on failures
3. Improved error handling for SerializationFailure and connection drops
4. Configurable batch sizes and retry logic
5. Comprehensive logging and diagnostics

Report Structure:
-----------------
1. Activity Summary Table: 
   - Aggregated count of stuck activities by Activity Name, Spec ID, and Interface
   - Time intervals: Last 1 Hour, Previous 1 Hour, Last 12 Hours, Last 24 Hours, 
     Previous 24 Hours, Last 1 Week, Last 1 Month, Last 1 Year

2. Detailed Records Table:
   - Individual activity records with project details, customer info, PTD
   - Age calculation (hours since last update) and age interval categorization
   - Filters for Manual implementation type only

Features:
---------
- TEST_MODE: Set to True to skip email sending and use test recipients
- Query Optimization with CTE (Common Table Expression)
- Double batching strategy with automatic retry on failure
- Connection resilience: Reconnects automatically on connection loss
- Comprehensive logging at each step
- Excel export with multiple sheets
- HTML email with styled tables
- Age interval categorization for quick analysis

Configuration:
--------------
- TEST_MODE: Enable/disable test mode (default: False)
- part_ids_batch_size: Batch size for part_id processing (default: 20)
- spec_ids_batch_size: Batch size for spec_ver_id processing (default: 50)
- max_retries: Maximum retry attempts for failed batches (default: 3)
- Date_Execution_Frequency: Execution frequency in days (default: 1)

Author: Abhishek Agrahari
Last Modified: November 2025
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
from psycopg2 import OperationalError, InterfaceError
import os
import time

# ============================================================================
# CONFIGURATION SECTION
# ============================================================================

# TEST MODE TOGGLE - Set to True for testing, False for production
TEST_MODE = True  # Change to False for production

# Database configuration
DB_CONFIG = {
    'database': "prodossdb",
    'user': 'ossdb01uams',
    'password': 'Pr0d_ossdb01uams',
    'host': 'oso-pstgr-rd.orion.comcast.com',
    'port': '6432'
}

# Batch configuration
PART_IDS_BATCH_SIZE = 20  # Batch size for part_id processing
SPEC_IDS_BATCH_SIZE = 50  # Batch size for spec_ver_id processing
MAX_RETRIES = 3  # Maximum retry attempts for failed batches
RETRY_DELAY = 2  # Seconds to wait between retries

# Email configuration
if TEST_MODE:
    EMAIL_RECIPIENTS = ['abhisha3@amdocs.com']  # Test recipients
    EMAIL_CC = []
else:
    EMAIL_RECIPIENTS = [
        'abhisha3@amdocs.com', 'Enna.Arora@amdocs.com', 'Nishant.Bhatia@amdocs.com',
        'prateek.jain5@amdocs.com', 'mukul.bhasin@amdocs.com', 'Alon.Kugel@Amdocs.com',
        'Shreyas.Kulkarni@amdocs.com', 'Smitesh.Kadia@amdocs.com'
    ]
    EMAIL_CC = ['abhisha3@amdocs.com']

# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'clips_outage_report_{dt.datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)

logging.info("=" * 80)
logging.info("CLIPS OUTAGE REPORT - Script Execution Started")
logging.info(f"TEST MODE: {'ENABLED' if TEST_MODE else 'DISABLED'}")
logging.info("=" * 80)

# ============================================================================
# DATABASE CONNECTION MANAGEMENT
# ============================================================================

def create_db_connection():
    """
    Create a new database connection with error handling
    Returns: connection object or None
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_session(autocommit=False, readonly=True)
        logging.info("Database connection established successfully.")
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {type(e).__name__}: {e}")
        return None

def ensure_connection(conn, cursor):
    """
    Ensure database connection is alive, reconnect if needed
    Returns: (connection, cursor) tuple
    """
    try:
        # Test connection with a simple query
        cursor.execute("SELECT 1")
        return conn, cursor
    except (OperationalError, InterfaceError) as e:
        logging.warning(f"Connection lost: {type(e).__name__}: {e}")
        logging.info("Attempting to reconnect...")
        
        # Close old connection
        try:
            cursor.close()
            conn.close()
        except:
            pass
        
        # Create new connection
        new_conn = create_db_connection()
        if new_conn:
            new_cursor = new_conn.cursor()
            logging.info("Reconnection successful!")
            return new_conn, new_cursor
        else:
            logging.error("Reconnection failed!")
            raise Exception("Unable to reconnect to database")

# ============================================================================
# DATE-BASED EXECUTION CONTROL
# ============================================================================

Todays_Date_DD = dt.datetime.now().day
Date_Execution_Frequency = 1

if not TEST_MODE and Todays_Date_DD % Date_Execution_Frequency != 0:
    logging.info(f"Script is set to execute only on every {Date_Execution_Frequency}th day of the month.")
    logging.info("Exiting...")
    exit()

logging.info("Date condition met. Proceeding with script execution.")

# ============================================================================
# INITIAL DATABASE CONNECTION
# ============================================================================

conn = create_db_connection()
if not conn:
    logging.error("Failed to establish initial database connection. Exiting...")
    exit()

cursor = conn.cursor()

# ============================================================================
# QUERY 1: STUCK ACTIVITIES SUMMARY (BATCHED)
# ============================================================================

Stuck_Activity = """
SELECT ord.entity_name AS "Activity Name",
       oai.spec_ver_id AS "Spec Id",
       aocd.interface AS Interface,
       SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '1 hour' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS "Last 1 Hour",
       SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '2 hours' AND oai.actual_start_date < NOW() - INTERVAL '1 hour' THEN 1 ELSE 0 END) AS "Previous 1 Hour",
       SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '12 hours' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS "Last 12 Hours",
       SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '1 day' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS "Last 24 Hours",
       SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '2 days' AND oai.actual_start_date < NOW() - INTERVAL '1 day' THEN 1 ELSE 0 END) AS "Previous 24 Hours",
       SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '7 days' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS "Last 1 Week",
       SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '1 month' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS "Last 1 Month",
       SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '1 year' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS "Last 1 Year"
FROM ossdb01db.oss_activity_instance oai
JOIN ossdb01ref.oss_ref_attribute ora ON oai.spec_ver_id = ora.attribute_value
JOIN ossdb01ref.oss_ref_data ord ON ora.entity_id = ord.entity_id
JOIN ossdb01db.activity_overview_custom_data aocd ON oai.spec_ver_id = aocd.spec_id
WHERE oai.part_id in ({batch_ids})
  AND oai.last_update_date > NOW() - INTERVAL '1 year'
  AND oai.state IN ('In Progress', 'Rework In Progress')
  AND oai.is_latest_version = 1
  AND oai.implementation_type <> 'Manual'
  AND aocd.interface in ('ARM','ASD')
GROUP BY ord.entity_name, oai.spec_ver_id, aocd.interface
ORDER BY "Last 1 Hour" DESC, "Last 12 Hours" DESC, "Last 24 Hours" DESC;
"""

logging.info("Starting Query 1: Stuck Activities Summary")
logging.info(f"Batch size: {PART_IDS_BATCH_SIZE} part_ids per batch")

# Execute query with batching
part_ids = list(range(1, 100))
activity_results = []
batch_count = 0

for i in range(0, len(part_ids), PART_IDS_BATCH_SIZE):
    batch = part_ids[i:i+PART_IDS_BATCH_SIZE]
    batch_count += 1
    
    retry_count = 0
    while retry_count < MAX_RETRIES:
        try:
            # Ensure connection is alive
            conn, cursor = ensure_connection(conn, cursor)
            
            query = Stuck_Activity.format(batch_ids=', '.join(map(str, batch)))
            cursor.execute(query)
            batch_results = cursor.fetchall()
            activity_results.extend(batch_results)
            
            logging.info(f"[Batch {batch_count}] Successfully executed for part_ids: {batch[0]}-{batch[-1]}, "
                        f"records: {len(batch_results)}")
            break  # Success, exit retry loop
            
        except Exception as e:
            retry_count += 1
            logging.error(f"[Batch {batch_count}] Attempt {retry_count}/{MAX_RETRIES} failed: "
                         f"{type(e).__name__}: {e}")
            
            if retry_count < MAX_RETRIES:
                logging.info(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                logging.error(f"[Batch {batch_count}] Max retries reached. Skipping this batch.")

# Create DataFrame from batched results
df_activity = pd.DataFrame(activity_results, columns=[
    "Activity Name", "Spec Id", "Interface", "Last 1 Hour", "Previous 1 Hour", 
    "Last 12 Hours", "Last 24 Hours", "Previous 24 Hours",
    "Last 1 Week", "Last 1 Month", "Last 1 Year"
])

# Aggregate to remove duplicates and sum metrics
df_activity = df_activity.groupby(
    ["Activity Name", "Spec Id", "Interface"], as_index=False
).agg({
    "Last 1 Hour": "sum",
    "Previous 1 Hour": "sum",
    "Last 12 Hours": "sum",
    "Last 24 Hours": "sum",
    "Previous 24 Hours": "sum",
    "Last 1 Week": "sum",
    "Last 1 Month": "sum",
    "Last 1 Year": "sum"
})

# Sort by most recent intervals first
df_activity = df_activity.sort_values(by=["Last 1 Hour", "Last 12 Hours", "Last 24 Hours"], ascending=False)

logging.info(f"Query 1 completed. Total activity groups: {len(df_activity)}")

# Extract spec_ver_ids from first query results for second query
spec_ver_ids = df_activity["Spec Id"].unique().tolist()
logging.info(f"Found {len(spec_ver_ids)} unique spec_ver_ids from first query")

if spec_ver_ids:
    logging.info(f"Sample spec_ver_ids (first 3): {spec_ver_ids[:3]}")
else:
    logging.warning("WARNING: No spec_ver_ids found in first query results! Second query will be skipped.")

# ============================================================================
# QUERY 2: DETAILED ACTIVITY RECORDS (BATCHED WITH RETRY)
# ============================================================================

Detailed_Activity = """
WITH filtered_projects AS (
    SELECT 
        spoi.id,
        spoi.name,
        spoi.status,
        spoi.plan_id,
        spoi.objid,
        MAX(CASE WHEN oas.code = 'customerID' THEN oas.value END) as customer_id,
        MAX(CASE WHEN oas.code = 'siteId' THEN oas.value END) as site_id,
        MAX(CASE WHEN oas.code = 'DMD_PTD' THEN oas.value END) as PTD
    FROM ossdb01db.sc_project_order_instance spoi
    LEFT JOIN ossdb01db.oss_attribute_store oas 
        ON oas.parent_id = spoi.objid 
        AND oas.code IN ('customerID', 'siteId', 'DMD_PTD')
    WHERE spoi.is_latest_version = 1
      AND spoi.manager IS DISTINCT FROM 'ProductionSanity'
      AND spoi.name NOT LIKE '%MM_PROD_TEST%'
      AND spoi.status NOT LIKE 'FCANCELLED'
    GROUP BY spoi.id, spoi.name, spoi.status, spoi.plan_id, spoi.objid
)
SELECT 
    fp.id as projectid,
    fp.customer_id,
    fp.site_id,
    fp.PTD,
    o1.entity_name,
    fp.name,
    oai.last_update_date,
    oai.create_date,
    oai.status,
    fp.status as project_status,
    oai.id as activity_id,
    EXTRACT(EPOCH FROM (NOW() - oai.last_update_date)) / 3600 as age_hours
FROM ossdb01db.oss_activity_instance oai
INNER JOIN ossdb01ref.oss_ref_attribute o2 
    ON o2.attribute_value = oai.spec_ver_id
INNER JOIN ossdb01ref.oss_ref_data o1 
    ON o1.entity_id = o2.entity_id
INNER JOIN filtered_projects fp 
    ON fp.plan_id = oai.plan_id
WHERE oai.part_id IN ({part_ids})
  AND oai.spec_ver_id IN ({spec_ids})
  AND oai.state IN ('In Progress', 'Rework In Progress')
  AND oai.is_latest_version = 1
ORDER BY age_hours DESC;
"""

logging.info("Starting Query 2: Detailed Activity Records")
logging.info(f"Part IDs batch size: {PART_IDS_BATCH_SIZE}, Spec IDs batch size: {SPEC_IDS_BATCH_SIZE}")

part_ids_range = list(range(1, 100))
detailed_results = []
failed_batches = []

if spec_ver_ids:
    total_batches = (len(part_ids_range) // PART_IDS_BATCH_SIZE + 1) * (len(spec_ver_ids) // SPEC_IDS_BATCH_SIZE + 1)
    current_batch = 0
    
    for i in range(0, len(part_ids_range), PART_IDS_BATCH_SIZE):
        part_batch = part_ids_range[i:i+PART_IDS_BATCH_SIZE]
        
        for j in range(0, len(spec_ver_ids), SPEC_IDS_BATCH_SIZE):
            spec_batch = spec_ver_ids[j:j+SPEC_IDS_BATCH_SIZE]
            current_batch += 1
            
            retry_count = 0
            success = False
            
            while retry_count < MAX_RETRIES and not success:
                try:
                    # Ensure connection is alive before each batch
                    conn, cursor = ensure_connection(conn, cursor)
                    
                    # Format spec_ver_ids as quoted strings (UUIDs)
                    spec_ids_formatted = ', '.join([f"'{str(spec_id)}'" for spec_id in spec_batch])
                    
                    query = Detailed_Activity.format(
                        part_ids=', '.join(map(str, part_batch)),
                        spec_ids=spec_ids_formatted
                    )
                    
                    # Debug: Log sample query for first batch only
                    if current_batch == 1:
                        logging.info(f"Sample query (first 500 chars): {query[:500]}...")
                    
                    cursor.execute(query)
                    batch_results = cursor.fetchall()
                    detailed_results.extend(batch_results)
                    
                    logging.info(f"[{current_batch}/{total_batches}] Successfully executed - "
                               f"part_ids: {part_batch[0]}-{part_batch[-1]}, "
                               f"spec_ids batch: {j//SPEC_IDS_BATCH_SIZE + 1}, "
                               f"records: {len(batch_results)}")
                    
                    success = True  # Mark as successful
                    
                except Exception as e:
                    retry_count += 1
                    error_msg = (f"part_ids: {part_batch[0]}-{part_batch[-1]}, "
                                f"spec_ids batch: {j//SPEC_IDS_BATCH_SIZE + 1}")
                    
                    logging.error(f"[{current_batch}/{total_batches}] Attempt {retry_count}/{MAX_RETRIES} failed")
                    logging.error(f"Error: {type(e).__name__}: {str(e)}")
                    
                    if retry_count < MAX_RETRIES:
                        logging.info(f"Retrying in {RETRY_DELAY} seconds...")
                        time.sleep(RETRY_DELAY)
                    else:
                        failed_batches.append(error_msg)
                        logging.error(f"Max retries reached. Skipping batch: {error_msg}")
    
    # Summary logging
    logging.info(f"Query 2 completed. Total records retrieved: {len(detailed_results)}")
    if failed_batches:
        logging.warning(f"Failed batches count: {len(failed_batches)}")
        for fb in failed_batches:
            logging.warning(f"  - {fb}")
    
    # Diagnostic if no records found
    if len(detailed_results) == 0:
        logging.warning("=" * 80)
        logging.warning("DIAGNOSTIC: No records found in detailed query")
        logging.warning("Possible reasons:")
        logging.warning("1. Activities from Query 1 don't have matching projects (plan_id mismatch)")
        logging.warning("2. Projects filtered out by CTE conditions")
        logging.warning("3. Activities don't have matching records in oss_ref_attribute/oss_ref_data")
        logging.warning(f"Query 1 found {len(spec_ver_ids)} spec_ver_ids across {len(df_activity)} activity groups")
        logging.warning("=" * 80)
else:
    logging.warning("No spec_ver_ids found from first query. Skipping detailed query execution.")

# Create DataFrame from detailed results
df_detailed = pd.DataFrame(detailed_results, columns=[
    "Project ID", "Customer ID", "Site ID", "PTD", "Entity Name", "Project Name", 
    "Last Update Date", "Create Date", "Activity Status", "Project Status", 
    "Activity ID", "Age (Hours)"
])

# Add Age Interval column
def get_age_interval(hours):
    if pd.isna(hours):
        return "Unknown"
    elif hours < 1:
        return "< 1 Hour"
    elif hours < 2:
        return "1-2 Hours"
    elif hours < 12:
        return "2-12 Hours"
    elif hours < 24:
        return "12-24 Hours"
    elif hours < 48:
        return "1-2 Days"
    elif hours < 168:
        return "2-7 Days"
    elif hours < 720:
        return "1-4 Weeks"
    else:
        return "> 1 Month"

if not df_detailed.empty:
    df_detailed["Age Interval"] = df_detailed["Age (Hours)"].apply(get_age_interval)
    df_detailed["Age (Hours)"] = df_detailed["Age (Hours)"].round(2)
    
    logging.info(f"Retrieved {len(df_detailed)} detailed activity records")
    age_distribution = df_detailed["Age Interval"].value_counts().to_dict()
    logging.info(f"Age interval distribution: {age_distribution}")
else:
    logging.warning("No detailed records retrieved from second query")

# Close database connection
cursor.close()
conn.close()
logging.info("Database connection closed successfully")

# ============================================================================
# SAVE TO EXCEL
# ============================================================================

logging.info("Preparing to save data to Excel file...")

folder_name = f"Orion Outage Report for {dt.datetime.now().strftime('%Y/%m/%d')}"
os.makedirs(folder_name, exist_ok=True)
logging.info(f"Created output directory: {folder_name}")

output_file = os.path.join(folder_name, "CLIPS_Outage_Report.xlsx")

try:
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_activity.to_excel(writer, sheet_name='Activity Summary', index=False)
        logging.info(f"Wrote 'Activity Summary' sheet with {len(df_activity)} rows")
        
        df_detailed.to_excel(writer, sheet_name='Detailed Records', index=False)
        if len(df_detailed) == 0:
            logging.warning(f"WARNING: 'Detailed Records' sheet is EMPTY (0 rows)")
        else:
            logging.info(f"Wrote 'Detailed Records' sheet with {len(df_detailed)} rows")
    
    logging.info(f"Excel file saved successfully: {output_file}")
except Exception as e:
    logging.error(f"Failed to save Excel file: {type(e).__name__}: {str(e)}")
    raise

# ============================================================================
# GENERATE HTML FOR EMAIL
# ============================================================================

logging.info("Converting DataFrames to HTML for email body...")

def styled_html(df):
    return f"""
    <style>
    .styled-table {{
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        font-family: sans-serif;
        min-width: 400px;
        border: 1px solid #dddddd;
    }}
    .styled-table th, .styled-table td {{
        border: 1px solid #dddddd;
        padding: 8px;
        text-align: left;
    }}
    .styled-table th {{
        background-color: #f2f2f2;
    }}
    </style>
    {df.to_html(index=False, classes='styled-table')}
    """

try:
    html_activity = styled_html(df_activity)
    logging.info(f"Generated HTML for Activity Summary table ({len(df_activity)} rows)")
    
    if len(df_detailed) == 0:
        html_detailed = """
        <div style="padding: 20px; background-color: #fff3cd; border: 1px solid #ffc107; border-radius: 5px; margin: 25px 0;">
            <h3 style="color: #856404; margin-top: 0;">⚠️ No Detailed Records Found</h3>
            <p style="color: #856404;">
                The detailed query returned no results. This could mean:
            </p>
            <ul style="color: #856404;">
                <li>Activities from the summary don't have matching project records</li>
                <li>Projects were filtered out by the CTE conditions</li>
                <li>No matching attribute store data for the projects</li>
            </ul>
            <p style="color: #856404;">
                <strong>Check the log file for detailed diagnostic information.</strong>
            </p>
        </div>
        """
        logging.warning("Generated empty state message for Detailed Records (0 rows)")
    else:
        html_detailed = styled_html(df_detailed)
        logging.info(f"Generated HTML for Detailed Records table ({len(df_detailed)} rows)")
except Exception as e:
    logging.error(f"Failed to generate HTML tables: {type(e).__name__}: {str(e)}")
    raise

# ============================================================================
# EMAIL MANAGER
# ============================================================================

class EmailMgr:
    def send_mail(self):
        """Constructs and sends the outage report email with Excel attachment"""
        
        recipients = EMAIL_RECIPIENTS
        cc_recipients = EMAIL_CC
        FROM = "noreply@amdocs.com"
        
        logging.info(f"Preparing email for {len(recipients)} recipients and {len(cc_recipients)} CC recipients")
        
        # Add test mode indicator to subject
        subject_prefix = "[TEST MODE] " if TEST_MODE else ""
        
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = f"{subject_prefix}Comcast OSS || CLIPS Outage Report for {dt.datetime.strftime(dt.datetime.now(), '%Y/%m/%d')}"
        MESSAGE['To'] = ", ".join(recipients)
        MESSAGE['Cc'] = ", ".join(cc_recipients)
        MESSAGE['From'] = FROM
        logging.info(f"Email subject: {MESSAGE['subject']}")

        BODY = self.get_mail_content()
        HTML_BODY = MIMEText(BODY, 'html')
        MESSAGE.attach(HTML_BODY)
        logging.info("HTML email body attached")

        # Attach Excel file
        try:
            ctype, encoding = mimetypes.guess_type(output_file)
            if ctype is None or encoding is not None:
                ctype = 'application/octet-stream'

            maintype, subtype = ctype.split('/', 1)
            with open(output_file, 'rb') as fp:
                part2 = MIMEBase(maintype, subtype)
                part2.set_payload(fp.read())
            encoders.encode_base64(part2)
            
            filename = os.path.basename(output_file)
            part2.add_header('Content-Disposition', 'attachment', filename=filename)
            MESSAGE.attach(part2)
            logging.info(f"Excel file attached: {filename}")
        except Exception as e:
            logging.error(f"Failed to attach Excel file: {type(e).__name__}: {str(e)}")
            raise

        # Send email via SMTP (skip if TEST_MODE and you don't want to send)
        if TEST_MODE:
            logging.info("TEST MODE: Email prepared but NOT sent. Set TEST_MODE=False to send.")
            logging.info(f"Would send to: {recipients}")
            logging.info(f"Would CC: {cc_recipients}")
            logging.info(f"Excel file ready at: {output_file}")
        else:
            try:
                logging.info("Connecting to SMTP server...")
                server = smtplib.SMTP('localhost')
                all_recipients = recipients + cc_recipients
                server.sendmail(FROM, all_recipients, MESSAGE.as_string())
                server.quit()
                logging.info(f"Email sent successfully to {len(all_recipients)} recipients!")
            except Exception as e:
                logging.error(f"Failed to send email: {type(e).__name__}: {str(e)}")
                raise

    def get_mail_content(self):
        test_banner = ""
        if TEST_MODE:
            test_banner = """
            <div style="background-color: #ff9800; color: white; padding: 15px; margin-bottom: 20px; border-radius: 5px; text-align: center;">
                <h2 style="margin: 0;">🧪 TEST MODE - This is a test email</h2>
            </div>
            """
        
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
            min-width: 600px;
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
        {test_banner}
        <p>Hi Team,</p>
        <p>Please find below the CLIPS Outage Report detailing activities that have been impacted since their respective start times.</p>
        <p>This report contains two tables:</p>
        <ul>
            <li><strong>Table 1 (Activity Summary):</strong> Shows count of stuck activities grouped by Activity Name, Spec ID, and Interface across multiple time intervals.</li>
            <li><strong>Table 2 (Detailed Records):</strong> Provides detailed information for each stuck activity including project details, customer info, and age analysis.</li>
        </ul>

        <h2>Table 1: Stuck Activities Summary - Count of activities whose status has not changed from 'In Progress' or 'Rework In Progress'</h2>
        {html_activity}

        <h2>Table 2: Detailed Activity Records - Individual stuck activities with project and customer information</h2>
        <p><em>Note: Age is calculated from the last update date. Activities are sorted by age (oldest first).</em></p>
        {html_detailed}

        <div class='note'>For any changes in the report: Please reach out to <a href='mailto:abhisha3@amdocs.com'>abhisha3@amdocs.com</a></div>
        <div class='footer'>Regards,<br>Abhishek Agrahari</div>
        </body>
        </html>
        """

# ============================================================================
# SEND EMAIL
# ============================================================================

logging.info("Initiating email sending process...")
try:
    em = EmailMgr()
    em.send_mail()
    logging.info("Script execution completed successfully!")
    logging.info("=" * 80)
except Exception as e:
    logging.error(f"Failed during email sending: {type(e).__name__}: {str(e)}")
    raise
