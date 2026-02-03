#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
OSO_Service_Activated.py - Service Activation Tracking System
================================================================================

DESCRIPTION:
    Connects to OSO PostgreSQL databases (Read and Write), fetches service
    activation data, maintains tracking table with RCA and status columns,
    and sends email reports with Excel attachment.

AUTHOR: Abhishek
CREATED: 2025-01-27 
VERSION: 2.0 (with Email Support)
================================================================================
"""

import sys
import os
from datetime import datetime
import logging
import traceback
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# =============================================================================
# CONFIGURATION TOGGLES
# =============================================================================

# Email Toggle: Set to False to skip email sending
SEND_EMAIL = True

# Date Execution Control: Script runs every N days
DATE_EXECUTION_FREQUENCY = 1  # 1 = daily, 7 = weekly, etc.

# Email Recipients
EMAIL_RECIPIENTS = ['abhishek_agrahari@comcast.com']
EMAIL_CC_RECIPIENTS = ['abhisha3@amdocs.com']

# Query Timeout Settings (Safety mechanism to prevent long-running queries)
QUERY_TIMEOUT_SECONDS = 600  # 10 minutes - increased for complex query with ~250 records
ENABLE_QUERY_TIMEOUT = True  # Set to False to disable timeout

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

# Configure comprehensive logging with timestamps
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# =============================================================================
# DATE EXECUTION CHECK
# =============================================================================

# Get current date information
Todays_Date_DD = datetime.now().day
Execution_Date = datetime.now().strftime("%Y-%m-%d")
Execution_DateTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Check if script should run based on date frequency
if Todays_Date_DD % DATE_EXECUTION_FREQUENCY != 0:
    logger.info(f"Script is set to execute only on every {DATE_EXECUTION_FREQUENCY}th day of the month.")
    logger.info(f"Today is day {Todays_Date_DD}. Script will not execute.")
    print(f"\nScript execution skipped for today ({Execution_Date}).")
    print(f"Next execution: Day {(Todays_Date_DD // DATE_EXECUTION_FREQUENCY + 1) * DATE_EXECUTION_FREQUENCY}")
    sys.exit(0)

logger.info("=" * 80)
logger.info("OSO_Service_Activated.py - Script Started")
logger.info(f"Execution Date: {Execution_Date}")
logger.info(f"Execution Time: {Execution_DateTime}")
logger.info("=" * 80)

# =============================================================================
# IMPORT REQUIRED LIBRARIES
# =============================================================================

# Check for psycopg2 (PostgreSQL driver)
try:
    import psycopg2
    from psycopg2 import sql
    from psycopg2.extras import RealDictCursor
    logger.info("[OK] psycopg2 imported successfully")
except ImportError:
    logger.error("[ERROR] psycopg2 not installed!")
    print("\n" + "=" * 80)
    print("[ERROR] psycopg2 not installed!")
    print("=" * 80)
    print("\nTo install, run:")
    print("  pip install psycopg2-binary")
    print("=" * 80)
    sys.exit(1)

# Check for pandas (Data manipulation)
try:
    import pandas as pd
    logger.info("[OK] pandas imported successfully")
except ImportError:
    logger.error("[ERROR] pandas not installed!")
    print("\n" + "=" * 80)
    print("[ERROR] pandas not installed!")
    print("=" * 80)
    print("\nTo install, run:")
    print("  pip install pandas openpyxl")
    print("=" * 80)
    sys.exit(1)

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================

# Read Database Configuration (Data Source)
READ_DB_CONFIG = {
    'host': 'oso-pstgr-rd.orion.comcast.com',
    'database': 'prodossdb',
    'port': 6432,
    'user': 'ossdb01db',
    'password': 'Pr0d_ossdb01db',
    'connect_timeout': 30
}

# Write Database Configuration (Data Storage + Tracking)
# East Region - Writable Database (via Load Balancer)
WRITE_DB_CONFIG = {
    'host': 'OSS-PROD1-PGRDS-NLB-1fe6faf4eb2c6ea3.elb.us-east-2.amazonaws.com',  # East region writable
    'database': 'prodossdb',
    'port': 6432,
    'user': 'ossdb01db',
    'password': 'Pr0d_ossdb01db',
    'connect_timeout': 500  # 2 minutes timeout (increased from 30s)
}

# Table name for tracking data
TABLE_NAME = "OSO_Service_Activated_Data"

logger.info(f"Read DB: {READ_DB_CONFIG['host']}:{READ_DB_CONFIG['port']}/{READ_DB_CONFIG['database']}")
logger.info(f"Write DB: {WRITE_DB_CONFIG['host']}:{WRITE_DB_CONFIG['port']}/{WRITE_DB_CONFIG['database']}")
logger.info(f"Target Table: {TABLE_NAME}")

# =============================================================================
# EMAIL MANAGER CLASS (Adapted from Outage_Report.py)
# =============================================================================

class EmailMgr:
    """
    Email Manager class for sending reports with Excel attachments.
    Handles HTML email formatting and SMTP communication.
    """
    
    def __init__(self, excel_file, summary_stats):
        """
        Initialize Email Manager.
        
        Args:
            excel_file: Path to Excel file to attach
            summary_stats: Dictionary with execution statistics
        """
        self.excel_file = excel_file
        self.summary_stats = summary_stats
    
    def send_mail(self):
        """
        Send email with Excel attachment to configured recipients.
        Uses SMTP localhost for sending.
        
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            logger.info("Preparing email...")
            
            # Email configuration
            recipients = EMAIL_RECIPIENTS
            cc_recipients = EMAIL_CC_RECIPIENTS
            FROM = "noreply@amdocs.com"
            
            # Create email message
            MESSAGE = MIMEMultipart('alternative')
            MESSAGE['subject'] = f"Comcast OSS || OSO Service Activated Report - {Execution_Date}"
            MESSAGE['To'] = ", ".join(recipients)
            MESSAGE['Cc'] = ", ".join(cc_recipients)
            MESSAGE['From'] = FROM
            
            logger.info(f"Email To: {', '.join(recipients)}")
            logger.info(f"Email Cc: {', '.join(cc_recipients)}")
            
            # Get HTML email body
            BODY = self.get_mail_content()
            HTML_BODY = MIMEText(BODY, 'html')
            MESSAGE.attach(HTML_BODY)
            
            # Attach Excel file
            if self.excel_file and os.path.exists(self.excel_file):
                ctype, encoding = mimetypes.guess_type(self.excel_file)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'
                
                maintype, subtype = ctype.split('/', 1)
                with open(self.excel_file, 'rb') as fp:
                    part = MIMEBase(maintype, subtype)
                    part.set_payload(fp.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(self.excel_file))
                MESSAGE.attach(part)
                logger.info(f"Attached file: {os.path.basename(self.excel_file)}")
            else:
                logger.warning(f"Excel file not found: {self.excel_file}")
            
            # Send email via SMTP
            logger.info("Connecting to SMTP server...")
            server = smtplib.SMTP('localhost')
            
            all_recipients = recipients + cc_recipients
            server.sendmail(FROM, all_recipients, MESSAGE.as_string())
            server.quit()
            
            logger.info("[OK] Mail sent successfully!")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] Failed to send email: {e}")
            logger.debug(traceback.format_exc())
            return False
    
    def get_mail_content(self):
        """
        Generate HTML email content with execution summary and data preview.
        
        Returns:
            str: HTML formatted email body
        """
        # Get statistics
        total_records = self.summary_stats.get('total_records', 0)
        new_records = self.summary_stats.get('new_records', 0)
        existing_records = self.summary_stats.get('existing_records', 0)
        table_total = self.summary_stats.get('table_total', 0)
        
        # HTML email template
        html_content = f"""
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
        
        .summary-box {{
            background-color: #f0f8ff;
            border-left: 4px solid #004080;
            padding: 15px;
            margin: 20px 0;
        }}
        
        .stats-table {{
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.95em;
            min-width: 500px;
        }}
        
        .stats-table th, .stats-table td {{
            border: 1px solid #dddddd;
            padding: 10px 15px;
            text-align: left;
        }}
        
        .stats-table th {{
            background-color: #004080;
            color: white;
            font-weight: bold;
        }}
        
        .stats-table tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        
        .note {{
            margin-top: 20px;
            font-size: 13px;
            color: #555;
            background-color: #fffbea;
            padding: 10px;
            border-left: 3px solid #ffc107;
        }}
        
        .footer {{
            margin-top: 30px;
            font-size: 14px;
            font-weight: bold;
            color: #666;
        }}
        
        .highlight {{
            color: #004080;
            font-weight: bold;
        }}
        </style>
        </head>
        <body>
        <h2>OSO Service Activated - Daily Sync Report</h2>
        
        <p>Hi Team,</p>
        
        <p>Please find below the execution summary for the <strong>OSO Service Activated Data Sync</strong> process that ran on <span class="highlight">{Execution_DateTime}</span>.</p>
        
        <div class="summary-box">
        <h3>Execution Summary</h3>
        <table class="stats-table">
        <tr>
            <th>Metric</th>
            <th>Count</th>
        </tr>
        <tr>
            <td>Records Fetched from READ DB</td>
            <td class="highlight">{total_records}</td>
        </tr>
        <tr>
            <td>New Records Inserted</td>
            <td class="highlight">{new_records}</td>
        </tr>
        <tr>
            <td>Existing Records Skipped</td>
            <td>{existing_records}</td>
        </tr>
        <tr>
            <td><strong>Total Records in Tracking Table</strong></td>
            <td class="highlight"><strong>{table_total}</strong></td>
        </tr>
        </table>
        </div>
        
        <h3>Database Information</h3>
        <ul>
            <li><strong>Read Database:</strong> {READ_DB_CONFIG['host']}:{READ_DB_CONFIG['port']}/{READ_DB_CONFIG['database']}</li>
            <li><strong>Write Database:</strong> {WRITE_DB_CONFIG['host']}:{WRITE_DB_CONFIG['port']}/{WRITE_DB_CONFIG['database']}</li>
            <li><strong>Table:</strong> {TABLE_NAME}</li>
        </ul>
        
        <h3>Attached Report</h3>
        <p>The attached Excel file contains <strong>ALL records</strong> currently in the tracking table ({table_total} records). This includes:</p>
        <ul>
            <li>All data columns from the source query</li>
            <li>Tracking columns: RCA, RCA_Category, Owned_By, WorkQueue, Task_Owner, Tracking_ID, Next_Action, Handling_Status</li>
            <li>Metadata: created_at, updated_at timestamps</li>
        </ul>
        
        <div class="note">
        <strong>Note:</strong> The tracking columns (RCA, Status, etc.) can be updated manually in the database or through a separate update process. Records are uniquely identified by: <code>service_id + site_id + version</code>
        </div>
        
        <h3>Next Steps</h3>
        <ol>
            <li>Review the attached Excel report for new service activations</li>
            <li>Update RCA and tracking columns as needed</li>
            <li>Monitor services that require action</li>
        </ol>
        
        <p>For any questions or changes to this report, please contact the automation team.</p>
        
        <div class='footer'>
        Regards,<br>
        OSO Automation Team<br>
        Orion Service Activation Tracking System
        </div>
        </body>
        </html>
        """
        
        return html_content


# =============================================================================
# DATABASE CONNECTION FUNCTIONS
# =============================================================================

def get_db_connection(db_config, db_type="READ"):
    """
    Establish PostgreSQL database connection with query timeout protection.
    
    Args:
        db_config: Database configuration dictionary
        db_type: Type of connection (READ/WRITE) for logging
    
    Returns:
        connection object or None
    """
    try:
        logger.info(f"Connecting to {db_type} database...")
        connection = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            connect_timeout=db_config['connect_timeout']
        )
        
        # Set query timeout to prevent long-running queries from impacting database
        if ENABLE_QUERY_TIMEOUT:
            cursor = connection.cursor()
            timeout_ms = QUERY_TIMEOUT_SECONDS * 1000  # Convert to milliseconds
            cursor.execute(f"SET statement_timeout = {timeout_ms}")
            cursor.close()
            logger.info(f"[OK] {db_type} database connection established (Query timeout: {QUERY_TIMEOUT_SECONDS}s)")
        else:
            logger.info(f"[OK] {db_type} database connection established (No timeout)")
        
        return connection
        
    except psycopg2.Error as e:
        logger.error(f"[ERROR] PostgreSQL Error ({db_type}): {e}")
        return None
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error ({db_type}): {e}")
        return None


def test_db_connections():
    """
    Test both READ and WRITE database connections.
    
    Returns:
        tuple: (read_success, write_success)
    """
    print("\n" + "=" * 80)
    print("Testing Database Connections...")
    print("=" * 80)
    
    # Test READ DB
    print("\n[1] Testing READ Database...")
    print(f"    Host: {READ_DB_CONFIG['host']}")
    print(f"    Port: {READ_DB_CONFIG['port']}")
    print(f"    Database: {READ_DB_CONFIG['database']}")
    print("-" * 80)
    
    read_conn = get_db_connection(READ_DB_CONFIG, "READ")
    read_success = False
    
    if read_conn:
        try:
            cursor = read_conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"[OK] READ DB Connected!")
            print(f"    Version: {version[:50]}...")
            cursor.close()
            read_success = True
        except Exception as e:
            print(f"[ERROR] READ DB Query failed: {e}")
            logger.error(f"READ DB Query failed: {e}")
        finally:
            read_conn.close()
    else:
        print("[ERROR] READ DB Connection failed!")
    
    # Test WRITE DB
    print("\n[2] Testing WRITE Database...")
    print(f"    Host: {WRITE_DB_CONFIG['host']}")
    print(f"    Port: {WRITE_DB_CONFIG['port']}")
    print(f"    Database: {WRITE_DB_CONFIG['database']}")
    print("-" * 80)
    
    write_conn = get_db_connection(WRITE_DB_CONFIG, "WRITE")
    write_success = False
    
    if write_conn:
        try:
            cursor = write_conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"[OK] WRITE DB Connected!")
            print(f"    Version: {version[:50]}...")
            cursor.close()
            write_success = True
        except Exception as e:
            print(f"[ERROR] WRITE DB Query failed: {e}")
            logger.error(f"WRITE DB Query failed: {e}")
        finally:
            write_conn.close()
    else:
        print("[ERROR] WRITE DB Connection failed!")
    
    print("=" * 80)
    
    return read_success, write_success


# =============================================================================
# TABLE MANAGEMENT FUNCTIONS
# =============================================================================

def check_table_exists():
    """
    Check if the tracking table exists on READ DB.
    Used when WRITE DB is not accessible.
    
    Returns:
        bool: True if table exists, False otherwise
    """
    read_conn = None
    cursor = None
    
    try:
        logger.info("Checking if table exists on READ DB...")
        
        read_conn = get_db_connection(READ_DB_CONFIG, "READ")
        if not read_conn:
            return False
        
        cursor = read_conn.cursor()
        
        # Check if table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, (TABLE_NAME.lower(),))
        
        exists = cursor.fetchone()[0]
        
        if exists:
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
            count = cursor.fetchone()[0]
            logger.info(f"[OK] Table exists with {count} records")
            print(f"[OK] Table '{TABLE_NAME}' exists with {count} records")
            return True
        else:
            logger.error(f"[ERROR] Table '{TABLE_NAME}' does not exist")
            print(f"[ERROR] Table '{TABLE_NAME}' does not exist on READ DB")
            return False
        
    except psycopg2.Error as e:
        logger.error(f"[ERROR] PostgreSQL Error: {e}")
        return False
        
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error: {e}")
        return False
        
    finally:
        if cursor:
            cursor.close()
        if read_conn:
            read_conn.close()


def create_table_if_not_exists():
    """
    Create the OSO_Service_Activated_Data table if it doesn't exist.
    Includes all data columns + tracking columns + metadata columns.
    
    Returns:
        bool: True if successful, False otherwise
    """
    connection = None
    cursor = None
    
    try:
        logger.info("Checking/Creating table...")
        
        connection = get_db_connection(WRITE_DB_CONFIG, "WRITE")
        if not connection:
            return False
        
        cursor = connection.cursor()
        
        # Create table SQL with comprehensive schema
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            -- Primary data columns from query
            customer_id TEXT,
            site_id TEXT,
            service_id TEXT,
            product_agreement_instance_id TEXT,
            solution_id TEXT,
            version TEXT,
            ptd TEXT,
            customer_name TEXT,
            framework_agreement_id TEXT,
            division TEXT,
            region TEXT,
            business_action TEXT,
            solution_leg_state TEXT,
            solution_name TEXT,
            ptd_status TEXT,
            activation_date TEXT,
            customer_accepted TEXT,
            product_spec TEXT,
            send_to_billing TEXT,
            cpm TEXT,
            customer_acceptance_days TEXT,
            customer_acceptance_state TEXT,
            customer_acceptance_plan_id TEXT,
            customer_acceptance_activity_id TEXT,
            ticketid TEXT,
            create_ticket TEXT,
            
            -- Additional tracking columns for RCA and status management
            RCA TEXT,
            RCA_Category TEXT,
            Owned_By TEXT,
            WorkQueue TEXT,
            Task_Owner TEXT,
            Tracking_ID TEXT,
            Next_Action TEXT,
            Handling_Status TEXT,
            
            -- Metadata columns for audit trail
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            -- Composite unique constraint to prevent duplicates
            CONSTRAINT unique_service_site_version UNIQUE (service_id, site_id, version)
        );
        """
        
        logger.info("Executing CREATE TABLE IF NOT EXISTS...")
        cursor.execute(create_table_sql)
        connection.commit()
        
        logger.info("[OK] Table created/verified successfully")
        
        # Create index for faster lookups on composite key
        index_sql = f"""
        CREATE INDEX IF NOT EXISTS idx_service_site_version 
        ON {TABLE_NAME} (service_id, site_id, version);
        """
        cursor.execute(index_sql)
        connection.commit()
        
        logger.info("[OK] Index created/verified")
        
        print("\n" + "=" * 80)
        print(f"[OK] Table '{TABLE_NAME}' is ready")
        print("=" * 80)
        
        return True
        
    except psycopg2.Error as e:
        logger.error(f"[ERROR] PostgreSQL Error: {e}")
        if connection:
            connection.rollback()
        print(f"[ERROR] Failed to create table: {e}")
        return False
        
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error: {e}")
        logger.debug(traceback.format_exc())
        print(f"[ERROR] Failed to create table: {e}")
        return False
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# =============================================================================
# DATA FETCHING FUNCTIONS
# =============================================================================

def fetch_service_activation_data():
    """
    Fetch service activation data from READ database using complex SQL query.
    Query filters for activated services not yet billing.
    
    Returns:
        pandas DataFrame or None
    """
    connection = None
    cursor = None
    
    try:
        logger.info("Fetching service activation data from READ DB...")
        
        print("\n" + "=" * 80)
        print("Fetching Data from READ Database...")
        print("=" * 80)
        
        connection = get_db_connection(READ_DB_CONFIG, "READ")
        if not connection:
            return None
        
        # The main SQL query - fetches activated services not yet billing
        query = """
        select * from (select
        da.customer_id "Customer_Id", da.customer_name "Customer_Name", da.framework_agreement_id "Framework_Agreement_Id",
        dso.site_id "Site_ID", dso.division "Division", dso.region "Region", dsl.business_action "Business_Action",
        dsl.state "Solution_Leg_State", dsl.solution_name "Solution_Name", dsl.solution_id "Solution_Id",
        dsl.ptd "PTD", dsl.ptd_status "PTD_Status", dsl.activation_date "Activation_Date",
        dsl.customer_accepted "Customer_Accepted",
        dpv.product_agreement_instance_id "Product_Agreement_Instance_Id", dpv.version "Version",
        dpv.service_id "Service_Id", dpv.product_spec "Product_Spec",
        oai.state "Send_To_Billing",
        count(dpv.product_agreement_instance_id) over (partition by dso.site_id) as num_product,
        sum(case when oai.state = 'Completed' then 1 else 0 end) over (partition by dso.site_id) as num_completed_product,
        case when count(dpv.product_agreement_instance_id) over (partition by dso.site_id) = sum(case when dsl.solution_name like '%Underlay%' then 1 else 0 end) over (partition by dso.site_id) then 0
            when (count(dpv.product_agreement_instance_id) over (partition by dso.site_id)) -
            (sum(case when poi_not."action" = 'Cease' then 1 else 0 end) over (partition by dso.site_id))
            != sum(case when oai.state = 'Completed' then 1 else 0 end) over (partition by dso.site_id) then 1 else 0 end rpt,
        coalesce(cpm_secondary.guid, cpm_primary.guid) cpm,
        '-' "Customer_Acceptance_Days",
        null "Customer_Acceptance_State",
        null "Customer_Acceptance_Plan_Id",
        null "Customer_Acceptance_Activity_Id"
        FROM ossdb01db.DD_AGREEMENT DA
        left join ossdb01db.DD_SOLUTION_LEG DSL ON DSL.AGREEMENT_ID = DA.ID and dsl.ptd_status in('Activated', 'Completed')
        left JOIN ossdb01db.DD_SOLUTION_LEG_SITE DSLS ON DSLS.SOLUTION_LEG_ID = DSL.ID
        left JOIN ossdb01db.DD_SITE_ORDER DSO ON DSO.ID = DSLS.SITE_ORDER_ID and dso.is_latest = 1
        left join ossdb01db.dd_sol_leg_site_2_prod_version dslspv on DSLS.id = dslspv.solution_leg_site_id
        left join ossdb01db.dd_product_version dpv on dslspv.prod_ver_id = dpv.id and dpv.is_latest = 1 and dpv.product_spec in('UNI', 'Business_Internet','EVC_Endpoint', 'SIP', 'PRI', 'BVE')
        left JOIN ossdb01db.SC_PROJECT_ORDER_INSTANCE poi_del ON poi_del.ID = DSO.S2D_PROJECT_ID and poi_del.is_latest_version = 1
        left join ossdb01db.SC_PROJECT_ORDER_INSTANCE poi_not ON poi_del.ID = poi_not.parent_project_id and poi_not.is_latest_version = 1 and poi_not.status not in('DCOMPLETED')
        left join ossdb01db.SC_PROJECT_ORDER_INSTANCE poi_prd ON poi_not.ID = poi_prd.parent_project_id and poi_prd.is_latest_version = 1
        left join ossdb01db.oss_attribute_store oas on poi_prd.objid = oas.parent_id
            and oas.part_id = floor(mod(substring(poi_prd.objid,33) ::int / 72000, 200))::int   
            and oas.code = 'productId'
            and oas.value = dpv.product_agreement_instance_id
        left join ossdb01db.oss_activity_instance oai on poi_not.plan_id = oai.plan_id and oai.spec_ver_id = 'e698608e-f76b-468e-a7ac-ed3d8c3072e9' and oai.is_latest_version = 1
        left join ossdb01db.dd_project_assignment_details cpm_secondary on da.customer_id = cpm_secondary.customer_id
            and da.framework_agreement_id = cpm_secondary.agreement_id
            and dso.site_id = cpm_secondary.site_id
            and cpm_secondary.entity_type = 'DD_SITE_ORDER'
            and cpm_secondary.type = 'SECONDARY'
            and cpm_secondary.assignment_status = 'ASSIGNED'
        left join ossdb01db.dd_project_assignment_details cpm_primary on da.customer_id = cpm_primary.customer_id
            and da.framework_agreement_id = cpm_primary.agreement_id
            and cpm_primary.entity_type = 'DD_AGREEMENT'
            and cpm_primary.type = 'PRIMARY'
            and cpm_primary.assignment_status = 'ASSIGNED'
        left join ossdb01db.SC_PROJECT_ORDER_INSTANCE poi_dpv ON dpv.project_id = poi_dpv.id and poi_dpv.is_latest_version = 1
            and poi_dpv."action" = poi_not."action"
        where da.is_latest = 1
        and dpv.product_agreement_instance_id is not null
        and oas.value is not null
        AND dsl.activation_date <= CAST(now()AS date) - 5
        and da.customer_name !~* '(POC)|(_TEST)|(MM_PROD)|(PROD TEST)|(PROD_MM)|(TESTCOMPANY)'
        ) tmp
        where rpt = 1
        and "Solution_Name" not like '%Underlay%'
        order by "Customer_Id", "Site_ID", "Solution_Id"
        """
        
        logger.info("Executing query...")
        if ENABLE_QUERY_TIMEOUT:
            logger.info(f"Query timeout set to {QUERY_TIMEOUT_SECONDS} seconds")
        
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        # Execute query with timeout protection
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            logger.info(f"Query returned {len(results)} rows")
        except psycopg2.extensions.QueryCanceledError as e:
            logger.error(f"[ERROR] Query exceeded timeout limit of {QUERY_TIMEOUT_SECONDS} seconds")
            logger.error("The query was automatically aborted to prevent database impact")
            print(f"\n[ERROR] Query Timeout!")
            print(f"The query took longer than {QUERY_TIMEOUT_SECONDS} seconds and was aborted.")
            print("Recommendations:")
            print("  1. Check if database is under heavy load")
            print("  2. Consider increasing QUERY_TIMEOUT_SECONDS in script")
            print("  3. Review query optimization (see QUERY_OPTIMIZATION_ANALYSIS.md)")
            print("  4. Contact DBA to check database performance")
            return None
        
        if not results:
            logger.warning("Query returned no results")
            print("[WARNING] No data found")
            print("=" * 80)
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame(results)
        
        # Normalize column names to match table schema (lowercase with underscores)
        column_mapping = {
            'Customer_Id': 'customer_id',
            'Customer_Name': 'customer_name',
            'Framework_Agreement_Id': 'framework_agreement_id',
            'Site_ID': 'site_id',
            'Division': 'division',
            'Region': 'region',
            'Business_Action': 'business_action',
            'Solution_Leg_State': 'solution_leg_state',
            'Solution_Name': 'solution_name',
            'Solution_Id': 'solution_id',
            'PTD': 'ptd',
            'PTD_Status': 'ptd_status',
            'Activation_Date': 'activation_date',
            'Customer_Accepted': 'customer_accepted',
            'Product_Agreement_Instance_Id': 'product_agreement_instance_id',
            'Version': 'version',
            'Service_Id': 'service_id',
            'Product_Spec': 'product_spec',
            'Send_To_Billing': 'send_to_billing',
            'cpm': 'cpm',
            'Customer_Acceptance_Days': 'customer_acceptance_days',
            'Customer_Acceptance_State': 'customer_acceptance_state',
            'Customer_Acceptance_Plan_Id': 'customer_acceptance_plan_id',
            'Customer_Acceptance_Activity_Id': 'customer_acceptance_activity_id'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Remove extra columns not in table schema (num_product, num_completed_product, rpt)
        columns_to_keep = list(column_mapping.values())
        df = df[[col for col in df.columns if col in columns_to_keep]]
        
        # Convert all columns to string type (table schema is all TEXT)
        for col in df.columns:
            df[col] = df[col].astype(str)
        
        # Replace 'None' string with actual None
        df = df.replace('None', None)
        df = df.replace('nan', None)
        df = df.replace('NaT', None)
        
        logger.info(f"DataFrame created - Shape: {df.shape}")
        print(f"[OK] Fetched {len(df)} records")
        print(f"Columns: {len(df.columns)}")
        print("=" * 80)
        
        return df
        
    except psycopg2.extensions.QueryCanceledError as e:
        logger.error(f"[ERROR] Query timeout - Query execution exceeded {QUERY_TIMEOUT_SECONDS} seconds")
        logger.error("Query was aborted to prevent database impact")
        print(f"\n[ERROR] Query Timeout!")
        print(f"The query exceeded the {QUERY_TIMEOUT_SECONDS} second limit and was aborted.")
        print("=" * 80)
        return None
        
    except psycopg2.Error as e:
        logger.error(f"[ERROR] PostgreSQL Error: {e}")
        print(f"[ERROR] Database error: {e}")
        return None
        
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error: {e}")
        logger.debug(traceback.format_exc())
        print(f"[ERROR] Error: {e}")
        return None
        
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# =============================================================================
# DATA INSERTION FUNCTIONS
# =============================================================================

def get_existing_records_keys():
    """
    Fetch all existing composite keys (service_id + site_id + version) from READ DB.
    This allows us to compare against existing records without querying for each row.
    
    Returns:
        set: Set of tuples (service_id, site_id, version) or None
    """
    read_conn = None
    cursor = None
    
    try:
        logger.info("Fetching existing record keys from READ DB (tracking table)...")
        
        read_conn = get_db_connection(READ_DB_CONFIG, "READ")
        if not read_conn:
            return None
        
        cursor = read_conn.cursor()
        
        # Fetch only the composite keys for comparison
        query = f"""
        SELECT service_id, site_id, version 
        FROM {TABLE_NAME}
        WHERE service_id IS NOT NULL 
        AND site_id IS NOT NULL 
        AND version IS NOT NULL
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Create a set of tuples for fast lookup
        existing_keys = {(row[0], row[1], row[2]) for row in results}
        
        logger.info(f"Found {len(existing_keys)} existing records in tracking table")
        print(f"    Existing records in table: {len(existing_keys)}")
        
        return existing_keys
        
    except psycopg2.Error as e:
        # If table doesn't exist yet, return empty set
        if 'does not exist' in str(e):
            logger.info("Table doesn't exist yet - no existing records")
            return set()
        logger.error(f"[ERROR] Failed to fetch existing keys: {e}")
        return set()
        
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error fetching keys: {e}")
        logger.debug(traceback.format_exc())
        return set()
        
    finally:
        if cursor:
            cursor.close()
        if read_conn:
            read_conn.close()


def filter_new_records(df, existing_keys):
    """
    Filter the fetched DataFrame to keep only new records.
    Compare against existing_keys to identify which records are new.
    
    Args:
        df: pandas DataFrame with all fetched records
        existing_keys: set of tuples (service_id, site_id, version)
        
    Returns:
        tuple: (new_records_df, skipped_count)
    """
    try:
        logger.info(f"Filtering {len(df)} fetched records against existing records...")
        
        # Create a composite key column for comparison
        df['_temp_key'] = df.apply(
            lambda row: (row.get('service_id'), row.get('site_id'), row.get('version')), 
            axis=1
        )
        
        # Filter out existing records
        new_records_df = df[~df['_temp_key'].isin(existing_keys)].copy()
        
        # Drop the temporary key column
        new_records_df.drop('_temp_key', axis=1, inplace=True)
        
        skipped_count = len(df) - len(new_records_df)
        
        logger.info(f"New records to insert: {len(new_records_df)}, Existing records: {skipped_count}")
        print(f"    New records to insert: {len(new_records_df)}")
        print(f"    Existing records (skipped): {skipped_count}")
        
        return new_records_df, skipped_count
        
    except Exception as e:
        logger.error(f"[ERROR] Failed to filter records: {e}")
        logger.debug(traceback.format_exc())
        return df, 0


def insert_new_records(df):
    """
    Insert new records into the table using WRITE DB.
    Checks existence one-by-one and inserts only new records.
    
    Args:
        df: pandas DataFrame with data to insert (new records only)
    
    Returns:
        tuple: (inserted_count, skipped_count)
    """
    write_conn = None
    cursor = None
    
    try:
        logger.info("Connecting to WRITE DB for inserting records...")
        
        print("\n" + "=" * 80)
        print("Inserting Records into WRITE Database...")
        print("=" * 80)
        
        write_conn = get_db_connection(WRITE_DB_CONFIG, "WRITE")
        if not write_conn:
            print("[ERROR] Could not connect to WRITE DB")
            return 0, len(df)
        
        cursor = write_conn.cursor()
        
        inserted_count = 0
        skipped_count = 0
        
        # Prepare columns for insertion
        columns = df.columns.tolist()
        
        # Add empty values for tracking columns (will be populated later)
        tracking_columns = ['RCA', 'RCA_Category', 'Owned_By', 'WorkQueue', 
                           'Task_Owner', 'Tracking_ID', 'Next_Action', 'Handling_Status',
                           'ticketid', 'create_ticket']
        
        for col in tracking_columns:
            if col not in columns:
                df[col] = None
        
        columns = df.columns.tolist()
        
        # Prepare insert SQL
        placeholders = ', '.join(['%s'] * len(columns))
        columns_str = ', '.join(columns)
        
        insert_sql = f"""
        INSERT INTO {TABLE_NAME} ({columns_str})
        VALUES ({placeholders})
        """
        
        # Process each record one-by-one
        logger.info(f"Processing {len(df)} records (checking existence and inserting)...")
        print(f"Processing {len(df)} records...")
        
        for idx, row in df.iterrows():
            try:
                service_id = row.get('service_id')
                site_id = row.get('site_id')
                version = row.get('version')
                
                # Validate required fields
                if not service_id or not site_id or version is None:
                    logger.warning(f"Skipping row {idx}: Missing required fields (service_id/site_id/version)")
                    skipped_count += 1
                    continue
                
                # Convert version to string (column is TEXT type)
                version = str(version)
                service_id = str(service_id)
                site_id = str(site_id)
                
                # Check if record already exists (one-by-one check using WRITE DB)
                check_sql = f"""
                SELECT COUNT(*) FROM {TABLE_NAME}
                WHERE service_id = %s AND site_id = %s AND version = %s
                """
                
                cursor.execute(check_sql, (service_id, site_id, version))
                exists = cursor.fetchone()[0] > 0
                
                if exists:
                    logger.debug(f"Record exists: service_id={service_id}, site_id={site_id}, version={version}")
                    skipped_count += 1
                    continue
                
                # Prepare values for insert - ensure all values are properly typed
                values = []
                for col in columns:
                    val = row.get(col)
                    # Convert to string if not None
                    if val is not None and not isinstance(val, str):
                        val = str(val)
                    values.append(val)
                
                # Execute insert
                cursor.execute(insert_sql, values)
                
                inserted_count += 1
                logger.debug(f"Inserted: service_id={service_id}, site_id={site_id}, version={version}")
                
                # Commit in batches of 50 for better performance and visibility
                if inserted_count % 50 == 0:
                    write_conn.commit()
                    logger.info(f"Committed batch: {inserted_count} records inserted so far...")
                    print(f"    Progress: {inserted_count} inserted, {skipped_count} skipped (out of {idx + 1} processed)")
                
            except psycopg2.extensions.QueryCanceledError as e:
                logger.error(f"[ERROR] Insert timeout on row {idx} - Operation exceeded {QUERY_TIMEOUT_SECONDS} seconds")
                logger.warning("Committing already inserted records before aborting...")
                write_conn.commit()
                print(f"\n[WARNING] Insert operation timed out after {inserted_count} records")
                print(f"Successfully inserted: {inserted_count} records")
                print(f"Remaining records were not processed to prevent database impact")
                return inserted_count, skipped_count
                
            except psycopg2.Error as e:
                logger.error(f"Error inserting row {idx}: {e}")
                skipped_count += 1
                continue
            
            except Exception as e:
                logger.error(f"Unexpected error on row {idx}: {e}")
                skipped_count += 1
                continue
        
        # Final commit for remaining records
        write_conn.commit()
        
        logger.info(f"[OK] Inserted: {inserted_count}, Skipped: {skipped_count}")
        
        print(f"\n[OK] Processing Complete:")
        print(f"    Total processed: {len(df)} records")
        print(f"    Inserted: {inserted_count} new records")
        print(f"    Skipped:  {skipped_count} existing records")
        print("=" * 80)
        
        return inserted_count, skipped_count
        
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error: {e}")
        logger.debug(traceback.format_exc())
        if write_conn:
            write_conn.rollback()
        print(f"[ERROR] Failed to insert records: {e}")
        return 0, len(df)
        
    finally:
        if cursor:
            cursor.close()
        if write_conn:
            write_conn.close()


# =============================================================================
# DATA EXPORT FUNCTIONS
# =============================================================================

def fetch_all_table_data():
    """
    Fetch ALL records from the tracking table for email report.
    This includes all columns: data columns + tracking columns + metadata.
    Uses READ DB for all SELECT operations.
    
    Returns:
        pandas DataFrame or None
    """
    read_conn = None
    cursor = None
    
    try:
        logger.info("Fetching ALL records from tracking table via READ DB...")
        
        read_conn = get_db_connection(READ_DB_CONFIG, "READ")
        if not read_conn:
            return None
        
        # Fetch all records with all columns
        query = f"""
        SELECT * FROM {TABLE_NAME}
        ORDER BY created_at DESC, customer_id, site_id
        """
        
        cursor = read_conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        
        results = cursor.fetchall()
        logger.info(f"Fetched {len(results)} total records from table via READ DB")
        
        if not results:
            logger.warning("Table is empty")
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame(results)
        
        logger.info(f"Table data DataFrame created - Shape: {df.shape}")
        return df
        
    except psycopg2.Error as e:
        logger.error(f"[ERROR] PostgreSQL Error: {e}")
        return None
        
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error: {e}")
        logger.debug(traceback.format_exc())
        return None
        
    finally:
        if cursor:
            cursor.close()
        if read_conn:
            read_conn.close()


def save_to_excel(df, filename=None, df_fetched=None):
    """
    Save DataFrame to Excel file for email attachment.
    Creates multiple sheets: All Records + Fetched Data (if provided)
    
    Args:
        df: pandas DataFrame (all table data)
        filename: Output filename (auto-generated if None)
        df_fetched: Optional DataFrame with freshly fetched data
    
    Returns:
        str: Path to saved file or None
    """
    try:
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"OSO_Service_Activated_{timestamp}.xlsx"
        
        logger.info(f"Saving data to Excel: {filename}")
        
        print("\n" + "=" * 80)
        print("Saving data to Excel for email...")
        print("=" * 80)
        
        # Save to Excel with multiple sheets
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Sheet 1: All records from tracking table
            df.to_excel(writer, index=False, sheet_name='All Records')
            print(f"  Sheet 'All Records': {len(df)} rows")
            logger.info(f"  Sheet 'All Records': {len(df)} rows")
            
            # Sheet 2: Fetched data from SQL query (if provided)
            if df_fetched is not None and not df_fetched.empty:
                df_fetched.to_excel(writer, index=False, sheet_name='Fetched Data')
                print(f"  Sheet 'Fetched Data': {len(df_fetched)} rows")
                logger.info(f"  Sheet 'Fetched Data': {len(df_fetched)} rows")
        
        if os.path.exists(filename):
            file_size = os.path.getsize(filename) / 1024
            logger.info(f"[OK] Excel file created: {filename} ({file_size:.2f} KB)")
            print(f"[OK] Excel file saved: {filename}")
            print(f"    Size: {file_size:.2f} KB")
            print(f"    Records: {len(df)}" + (f" + {len(df_fetched)}" if df_fetched is not None else ""))
            print("=" * 80)
            return os.path.abspath(filename)
        
        return None
        
    except Exception as e:
        logger.error(f"[ERROR] Failed to save Excel: {e}")
        print(f"[ERROR] Failed to save Excel: {e}")
        return None


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    """
    Main execution flow:
    1. Test database connections
    2. Create/verify table structure
    3. Fetch service activation data from READ DB
    4. Insert new records into WRITE DB
    5. Fetch all table data
    6. Export to Excel
    7. Send email report (if toggle is enabled)
    """
    
    logger.info("=" * 80)
    logger.info("MAIN EXECUTION - Starting")
    logger.info(f"Email Toggle: {'ENABLED' if SEND_EMAIL else 'DISABLED'}")
    logger.info("=" * 80)
    
    print("\n" + "=" * 80)
    print("  OSO Service Activated - Data Sync & Email Report")
    print(f"  Execution Date: {Execution_Date}")
    print(f"  Execution Time: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 80)
    
    # Check for dry-run flag
    dry_run = '--dry-run' in sys.argv
    
    if dry_run:
        logger.info("DRY-RUN mode enabled")
        print("\n[INFO] Running in DRY-RUN mode (no data insertion or email)\n")
    
    # ==========================================================================
    # STEP 1: Test Database Connections
    # ==========================================================================
    print("\nStep 1: Testing database connections...")
    logger.info("STEP 1: Testing connections")
    
    read_success, write_success = test_db_connections()
    
    if not read_success:
        logger.error("READ database connection failed")
        print("\n[ERROR] READ database connection failed. Cannot proceed.")
        sys.exit(1)
    
    if not write_success and not dry_run:
        logger.error("WRITE database connection failed")
        print("\n[ERROR] WRITE database connection failed. Cannot proceed.")
        sys.exit(1)
    
    # ==========================================================================
    # STEP 2: Verify Table Exists
    # ==========================================================================
    if not dry_run:
        print("\nStep 2: Verifying table exists...")
        logger.info("STEP 2: Verifying table exists")
        
        table_exists = check_table_exists()
        
        if not table_exists:
            logger.error("Table does not exist")
            print("[ERROR] Table 'OSO_Service_Activated_Data' does not exist.")
            print("Please create the table using CREATE_TABLE_OSO.sql")
            sys.exit(1)
    else:
        print("\nStep 2: [SKIPPED in dry-run mode]")
    
    # ==========================================================================
    # STEP 3: Fetch Service Activation Data from READ DB
    # ==========================================================================
    print("\nStep 3: Fetching service activation data from READ DB...")
    logger.info("STEP 3: Fetching data from READ DB")
    
    df_fetched_data = fetch_service_activation_data()
    
    if df_fetched_data is None or df_fetched_data.empty:
        logger.warning("No new data retrieved from READ DB")
        print("[WARNING] No new data retrieved.")
        print("\n[OK] Script completed - No data to process")
        sys.exit(0)
    else:
        print(f"\n[OK] Retrieved {len(df_fetched_data)} records from READ DB")
        
        # Display sample
        print("\nSample Data (first 3 rows):")
        print("-" * 80)
        print(df_fetched_data.head(3).to_string())
        print("-" * 80)
    
    # ==========================================================================
    # STEP 4: Insert Records (Check one-by-one and insert new ones)
    # ==========================================================================
    inserted = 0
    skipped = 0
    
    if not dry_run and df_fetched_data is not None and not df_fetched_data.empty:
        print("\nStep 4: Checking and inserting records (one-by-one)...")
        logger.info("STEP 4: Checking existence and inserting new records via WRITE DB")
        
        print(f"Will check {len(df_fetched_data)} records against existing table...")
        
        inserted, skipped = insert_new_records(df_fetched_data)
        
        logger.info(f"Inserted: {inserted}, Skipped: {skipped}")
    else:
        print("\nStep 4: [SKIPPED - dry-run mode or no data]")
        if df_fetched_data is not None:
            print(f"    Would check and insert {len(df_fetched_data)} records")
    
    # ==========================================================================
    # STEP 5: Fetch All Table Data for Email (from READ DB)
    # ==========================================================================
    print("\nStep 5: Fetching all table data for email (READ DB)...")
    logger.info("STEP 5: Fetching all table data from READ DB")
    
    df_all_data = fetch_all_table_data()
    
    if df_all_data is None or df_all_data.empty:
        logger.warning("No data in table or fetch failed")
        print("[WARNING] No data in tracking table.")
        df_all_data = df_fetched_data  # Fallback to fetched data
    else:
        print(f"[OK] Retrieved {len(df_all_data)} total records from table")
    
    # ==========================================================================
    # STEP 6: Save Excel File
    # ==========================================================================
    print("\nStep 6: Saving Excel file...")
    logger.info("STEP 6: Saving Excel file")
    
    excel_file = None
    if df_all_data is not None and not df_all_data.empty:
        # Pass both all data and fetched data to create multiple sheets
        excel_file = save_to_excel(
            df=df_all_data, 
            filename=None, 
            df_fetched=df_fetched_data if 'df_fetched_data' in locals() else None
        )
    else:
        logger.warning("No data to export to Excel")
        print("[WARNING] No data to export to Excel")
    
    # ==========================================================================
    # STEP 7: Send Email Report
    # ==========================================================================
    email_sent = False
    
    if not dry_run and SEND_EMAIL and excel_file:
        print("\nStep 7: Sending email report...")
        logger.info("STEP 7: Sending email report")
        
        # Prepare summary statistics
        summary_stats = {
            'total_records': len(df_fetched_data) if df_fetched_data is not None else 0,
            'new_records': inserted,
            'existing_records': skipped,
            'table_total': len(df_all_data) if df_all_data is not None else 0
        }
        
        # Send email
        email_mgr = EmailMgr(excel_file, df_all_data, summary_stats)
        email_sent = email_mgr.send_mail()
        
    elif not SEND_EMAIL:
        print("\nStep 7: [SKIPPED - Email toggle is OFF]")
        logger.info("STEP 7: Skipped - Email toggle disabled")
    elif dry_run:
        print("\nStep 7: [SKIPPED - dry-run mode]")
        logger.info("STEP 7: Skipped - Dry-run mode")
    else:
        print("\nStep 7: [SKIPPED - No Excel file to send]")
        logger.info("STEP 7: Skipped - No Excel file")
    
    # ==========================================================================
    # Final Summary
    # ==========================================================================
    print("\n" + "=" * 80)
    if dry_run:
        print("[OK] DRY-RUN COMPLETED!")
    else:
        print("[OK] ALL OPERATIONS COMPLETED!")
    print("=" * 80)
    print(f"Execution Date: {Execution_Date}")
    print(f"Execution Time: {Execution_DateTime}")
    print("-" * 80)
    if df_new_data is not None:
        print(f"Records fetched from READ DB: {len(df_new_data)}")
    if not dry_run:
        print(f"Records inserted: {inserted}")
        print(f"Records skipped: {skipped}")
    if df_all_data is not None:
        print(f"Total records in table: {len(df_all_data)}")
    if excel_file:
        print(f"Excel file: {excel_file}")
    if not dry_run and SEND_EMAIL:
        print(f"Email sent: {'Yes' if email_sent else 'Failed'}")
    print("=" * 80)
    
    logger.info("=" * 80)
    logger.info("MAIN EXECUTION - Completed Successfully")
    logger.info("=" * 80)
    
    sys.exit(0)
