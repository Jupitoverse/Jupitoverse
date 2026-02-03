#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
OSO_Service_Activated_local.py - Service Activation Data Extractor (Local)
================================================================================

DESCRIPTION:
    Simplified version that:
    1. Connects to READ DB only (PostgreSQL)
    2. Runs the service activation query
    3. Exports results to Excel (single sheet)
    4. Sends email report with attachment
    
    Perfect for local development and custom logic addition.

AUTHOR: Abhishek
CREATED: 2025-12-01
VERSION: 1.0 (Local Simplified Version)
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
# CONFIGURATION
# =============================================================================

# Email Toggle: Set to False to skip email sending
SEND_EMAIL = True

# Date Execution Control: Script runs every N days
DATE_EXECUTION_FREQUENCY = 1  # 1 = daily, 7 = weekly, etc.

# Email Recipients
EMAIL_RECIPIENTS = ['abhishek_agrahari@comcast.com']
EMAIL_CC_RECIPIENTS = ['abhisha3@amdocs.com']

# Query Timeout Settings
QUERY_TIMEOUT_SECONDS = 600  # 10 minutes
ENABLE_QUERY_TIMEOUT = True

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# =============================================================================
# DATE EXECUTION CHECK
# =============================================================================

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
logger.info("OSO_Service_Activated_local.py - Script Started")
logger.info(f"Execution Date: {Execution_Date}")
logger.info(f"Execution Time: {Execution_DateTime}")
logger.info("=" * 80)

# =============================================================================
# IMPORT REQUIRED LIBRARIES
# =============================================================================

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
    print("\n" + "=" * 80)
    sys.exit(1)

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
    print("\n" + "=" * 80)
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
    'connect_timeout': 120  # 2 minutes timeout
}

logger.info(f"Read DB: {READ_DB_CONFIG['host']}:{READ_DB_CONFIG['port']}/{READ_DB_CONFIG['database']}")

# =============================================================================
# SQL QUERY - Service Activation Data
# =============================================================================

SERVICE_ACTIVATION_QUERY = """
select * from (select
da.customer_id "Customer_Id",
da.customer_name "Customer_Name",
da.framework_agreement_id "Framework_Agreement_Id",
dso.site_id "Site_ID",
dso.division "Division",
dso.region "Region",
dsl.business_action "Business_Action",
dsl.state "Solution_Leg_State",
dsl.solution_name "Solution_Name",
dsl.solution_id "Solution_Id",
dsl.ptd "PTD",
dsl.ptd_status "PTD_Status",
dsl.activation_date "Activation_Date",
dsl.customer_accepted "Customer_Accepted",
dpv.product_agreement_instance_id "Product_Agreement_Instance_Id",
dpv.version "Version",
dpv.service_id "Service_Id",
dpv.product_spec "Product_Spec",
oai.state "Send_To_Billing",
count(dpv.product_agreement_instance_id) over (partition by dso.site_id) as num_product,
sum(case when oai.state = 'Completed' then 1 else 0 end) over (partition by dso.site_id) as num_completed_product,
case when count(dpv.product_agreement_instance_id) over (partition by dso.site_id) = sum(case when dsl.solution_name like '%Underlay%' then 1 else 0 end) over (partition by dso.site_id) then 0
    when (count(dpv.product_agreement_instance_id) over (partition by dso.site_id)) -
    (sum(case when poi_not."action" = 'Cease' then 1 else 0 end) over (partition by dso.site_id))
    != sum(case when oai.state = 'Completed' then 1 else 0 end) over (partition by dso.site_id) then 1
else 0
end rpt,
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

# =============================================================================
# EMAIL MANAGER CLASS
# =============================================================================

class EmailMgr:
    """Email Manager class for sending reports with Excel attachments."""
    
    def __init__(self, excel_file, record_count, analysis_count=0):
        """
        Initialize Email Manager.
        
        Args:
            excel_file: Path to Excel file to attach
            record_count: Number of records in the service activation data
            analysis_count: Number of records in the OSO analysis sheet
        """
        self.excel_file = excel_file
        self.record_count = record_count
        self.analysis_count = analysis_count
    
    def send_mail(self):
        """
        Send email with Excel attachment to configured recipients.
        
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
        """Generate HTML email content with execution summary."""
        
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
            min-width: 400px;
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
        <h2>OSO Service Activated - Data Report</h2>
        
        <p>Hi Team,</p>
        
        <p>Please find the <strong>OSO Service Activation Data Report</strong> that ran on <span class="highlight">{Execution_DateTime}</span>.</p>
        
        <div class="summary-box">
        <h3>Execution Summary</h3>
        <table class="stats-table">
        <tr>
            <th>Metric</th>
            <th>Count</th>
        </tr>
        <tr>
            <td>Total Records Fetched</td>
            <td class="highlight">{self.record_count}</td>
        </tr>
        <tr>
            <td>OSO Analysis Records</td>
            <td class="highlight">{self.analysis_count}</td>
        </tr>
        <tr>
            <td>Execution Date</td>
            <td>{Execution_Date}</td>
        </tr>
        <tr>
            <td>Execution Time</td>
            <td>{Execution_DateTime}</td>
        </tr>
        </table>
        </div>
        
        <h3>Database Information</h3>
        <ul>
            <li><strong>Read Database:</strong> {READ_DB_CONFIG['host']}:{READ_DB_CONFIG['port']}/{READ_DB_CONFIG['database']}</li>
            <li><strong>Query Timeout:</strong> {QUERY_TIMEOUT_SECONDS} seconds</li>
        </ul>
        
        <h3>Attached Report</h3>
        <p>The attached Excel file contains <strong>2 sheets</strong>:</p>
        <ul>
            <li><strong>Sheet 1 - Service Activation Data:</strong> {self.record_count} records extracted from the database</li>
            <li><strong>Sheet 2 - OSO_Analysis:</strong> {self.analysis_count} analysis records with RCA, Task Owner, WorkQueue, and Interface details</li>
        </ul>
        <p>The analysis sheet includes complex nested query results for services with in-progress activities.</p>
        
        <div class="note">
        <strong>Note:</strong> This is a simplified local version for development. Add your custom columns and logic as needed.
        </div>
        
        <h3>Next Steps</h3>
        <ol>
            <li>Review the attached Excel report</li>
            <li>Add your custom processing logic to the script</li>
            <li>Update column calculations as needed</li>
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
# DATABASE FUNCTIONS
# =============================================================================

def get_db_connection():
    """
    Establish connection to PostgreSQL READ database.
    
    Returns:
        connection object or None if connection fails
    """
    try:
        logger.info("Connecting to READ database...")
        
        # Set query timeout if enabled
        if ENABLE_QUERY_TIMEOUT:
            conn = psycopg2.connect(
                **READ_DB_CONFIG,
                options=f'-c statement_timeout={QUERY_TIMEOUT_SECONDS * 1000}'  # milliseconds
            )
            logger.info(f"[OK] Database connection established (Query timeout: {QUERY_TIMEOUT_SECONDS}s)")
        else:
            conn = psycopg2.connect(**READ_DB_CONFIG)
            logger.info("[OK] Database connection established (No timeout)")
        
        return conn
        
    except psycopg2.OperationalError as e:
        logger.error(f"[ERROR] PostgreSQL Operational Error: {e}")
        return None
    except psycopg2.Error as e:
        logger.error(f"[ERROR] PostgreSQL Error: {e}")
        return None
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error: {e}")
        logger.debug(traceback.format_exc())
        return None


def fetch_service_activation_data():
    """
    Fetch service activation data from READ DB using the provided query.
    
    Returns:
        pandas DataFrame or None
    """
    conn = None
    cursor = None
    
    try:
        logger.info("Fetching service activation data from READ DB...")
        
        conn = get_db_connection()
        if not conn:
            logger.error("Failed to connect to database")
            return None
        
        logger.info("Executing query...")
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute(SERVICE_ACTIVATION_QUERY)
        
        results = cursor.fetchall()
        logger.info(f"Query executed successfully. Fetched {len(results)} records.")
        
        if not results:
            logger.warning("Query returned no data")
            return None
        
        # Convert to pandas DataFrame
        df = pd.DataFrame(results)
        
        # Convert all columns to string to avoid type issues
        for col in df.columns:
            if col not in ['num_product', 'num_completed_product', 'rpt']:  # Keep numeric columns as-is
                df[col] = df[col].astype(str)
        
        logger.info(f"DataFrame created - Shape: {df.shape}")
        logger.info(f"Columns: {', '.join(df.columns.tolist())}")
        
        return df
        
    except psycopg2.extensions.QueryCanceledError as e:
        logger.error(f"[ERROR] Query timeout - Query exceeded {QUERY_TIMEOUT_SECONDS} seconds")
        logger.error("Query was aborted to prevent database impact")
        return None
        
    except psycopg2.Error as e:
        logger.error(f"[ERROR] PostgreSQL Error: {e}")
        logger.debug(traceback.format_exc())
        return None
        
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error: {e}")
        logger.debug(traceback.format_exc())
        return None
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            logger.info("Database connection closed")


# =============================================================================
# OSO ANALYSIS FUNCTIONS
# =============================================================================

def execute_query(query, params=None):
    """
    Execute a query and return results.
    
    Args:
        query: SQL query string
        params: Query parameters (optional)
    
    Returns:
        list of dict or None
    """
    conn = None
    cursor = None
    
    try:
        conn = get_db_connection()
        if not conn:
            return None
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        results = cursor.fetchall()
        return results
        
    except Exception as e:
        logger.error(f"Query execution error: {e}")
        return None
        
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def check_in_progress_count(service_id):
    """
    Q1: Check count of in-progress activities for a service_id.
    
    Returns:
        int: Count of in-progress activities
    """
    query = f"""
    with temp_abhi as (
        select distinct dpv2.project_id as pv_prj_id
        from ossdb01db.dd_product_version dpv
        left join ossdb01db.dd_sol_leg_site_2_prod_version dslspv on dpv.id = dslspv.prod_ver_id
        left join ossdb01db.dd_sol_leg_site_2_prod_version dslspv2 on dslspv.solution_leg_site_id = dslspv2.solution_leg_site_id
        left join ossdb01db.dd_product_version dpv2 on dslspv2.prod_ver_id = dpv2.id
        where dpv.service_id = '{service_id}'
    )
    select count(oai.id) as cnt
    from temp_abhi
    left join ossdb01db.sc_project_order_instance spoi on pv_prj_id = spoi.id
    left join ossdb01db.oss_activity_instance oai on spoi.plan_id = oai.plan_id and oai.is_latest_version = 1
    left join ossdb01ref.oss_ref_attribute ora on oai.spec_ver_id = ora.attribute_value
    left join ossdb01ref.oss_ref_data ord on ora.entity_id = ord.entity_id
    where oai.status='In Progress'
    """
    
    results = execute_query(query)
    if results and len(results) > 0:
        return results[0].get('cnt', 0) or 0
    return 0


def get_implementation_types(service_id):
    """
    Q2: Get implementation types for a service_id.
    
    Returns:
        list: List of implementation types
    """
    query = f"""
    with temp_abhi as (
        select distinct dpv2.project_id as pv_prj_id
        from ossdb01db.dd_product_version dpv
        left join ossdb01db.dd_sol_leg_site_2_prod_version dslspv on dpv.id = dslspv.prod_ver_id
        left join ossdb01db.dd_sol_leg_site_2_prod_version dslspv2 on dslspv.solution_leg_site_id = dslspv2.solution_leg_site_id
        left join ossdb01db.dd_product_version dpv2 on dslspv2.prod_ver_id = dpv2.id
        where dpv.service_id = '{service_id}'
    )
    select distinct oai.implementation_type
    from temp_abhi
    left join ossdb01db.sc_project_order_instance spoi on pv_prj_id = spoi.id
    left join ossdb01db.oss_activity_instance oai on spoi.plan_id = oai.plan_id and oai.is_latest_version = 1
    left join ossdb01ref.oss_ref_attribute ora on oai.spec_ver_id = ora.attribute_value
    left join ossdb01ref.oss_ref_data ord on ora.entity_id = ord.entity_id
    where oai.status='In Progress'
    group by oai.implementation_type
    """
    
    results = execute_query(query)
    if results:
        return [r.get('implementation_type') for r in results if r.get('implementation_type')]
    return []


def get_rca_details_manual(service_id):
    """
    Q3: Get RCA details for Manual implementation type.
    
    Returns:
        str: RCA details
    """
    query = f"""
    with temp_abhi as (
        select distinct dpv2.project_id as pv_prj_id
        from ossdb01db.dd_product_version dpv
        left join ossdb01db.dd_sol_leg_site_2_prod_version dslspv on dpv.id = dslspv.prod_ver_id
        left join ossdb01db.dd_sol_leg_site_2_prod_version dslspv2 on dslspv.solution_leg_site_id = dslspv2.solution_leg_site_id
        left join ossdb01db.dd_product_version dpv2 on dslspv2.prod_ver_id = dpv2.id
        where dpv.service_id = '{service_id}'
    )
    select distinct ord.entity_name, spoi.name, oai.id,
        now() - oai.actual_start_date as time_elapsed, oai.implementation_type
    from temp_abhi
    left join ossdb01db.sc_project_order_instance spoi on pv_prj_id = spoi.id
    left join ossdb01db.oss_activity_instance oai on spoi.plan_id = oai.plan_id and oai.is_latest_version = 1
    left join ossdb01ref.oss_ref_attribute ora on oai.spec_ver_id = ora.attribute_value
    left join ossdb01ref.oss_ref_data ord on ora.entity_id = ord.entity_id
    where oai.status='In Progress'
    """
    
    results = execute_query(query)
    if results:
        # Combine all results into a single string
        rca_parts = []
        for r in results:
            entity_name = r.get('entity_name', '')
            name = r.get('name', '')
            time_elapsed = r.get('time_elapsed', '')
            rca_parts.append(f"{entity_name} | {name} | {time_elapsed}")
        return " || ".join(rca_parts)
    return ""


def get_activity_ids(service_id):
    """
    Q4: Get oai.id values for a service_id.
    
    Returns:
        list: List of activity IDs
    """
    query = f"""
    with temp_abhi as (
        select distinct dpv2.project_id as pv_prj_id
        from ossdb01db.dd_product_version dpv
        left join ossdb01db.dd_sol_leg_site_2_prod_version dslspv on dpv.id = dslspv.prod_ver_id
        left join ossdb01db.dd_sol_leg_site_2_prod_version dslspv2 on dslspv.solution_leg_site_id = dslspv2.solution_leg_site_id
        left join ossdb01db.dd_product_version dpv2 on dslspv2.prod_ver_id = dpv2.id
        where dpv.service_id = '{service_id}'
    )
    select distinct oai.id
    from temp_abhi
    left join ossdb01db.sc_project_order_instance spoi on pv_prj_id = spoi.id
    left join ossdb01db.oss_activity_instance oai on spoi.plan_id = oai.plan_id and oai.is_latest_version = 1
    left join ossdb01ref.oss_ref_attribute ora on oai.spec_ver_id = ora.attribute_value
    left join ossdb01ref.oss_ref_data ord on ora.entity_id = ord.entity_id
    where oai.status='In Progress'
    group by oai.id
    """
    
    results = execute_query(query)
    if results:
        return [r.get('id') for r in results if r.get('id')]
    return []


def get_task_owner(activity_id):
    """
    Q5: Get task owner name for an activity ID.
    
    Returns:
        str: Task owner name
    """
    query = f"""
    select text_ as task_owner_name from ossdb01db.act_ru_variable where task_id_ in
    (select task_id_ from ossdb01db.act_ru_variable arv where text_ = '{activity_id}' and name_= 'activityId') 
    and name_ in ('task_owner_name')
    """
    
    results = execute_query(query)
    if results and len(results) > 0:
        return results[0].get('task_owner_name', '')
    return ""


def get_work_queue(activity_id):
    """
    Q6: Get work queue for an activity ID.
    
    Returns:
        str: Work queue
    """
    query = f"""
    select text_ as work_queue from ossdb01db.act_ru_variable where task_id_ in
    (select task_id_ from ossdb01db.act_ru_variable arv where text_ = '{activity_id}' and name_= 'activityId') 
    and name_ in ('WorkQueue')
    """
    
    results = execute_query(query)
    if results and len(results) > 0:
        return results[0].get('work_queue', '')
    return ""


def get_rca_details_automatic(service_id):
    """
    Q7: Get RCA details for Automatic implementation type.
    
    Returns:
        str: RCA details
    """
    query = f"""
    with temp_abhi as (
        select distinct dpv2.project_id as pv_prj_id
        from ossdb01db.dd_product_version dpv
        left join ossdb01db.dd_sol_leg_site_2_prod_version dslspv on dpv.id = dslspv.prod_ver_id
        left join ossdb01db.dd_sol_leg_site_2_prod_version dslspv2 on dslspv.solution_leg_site_id = dslspv2.solution_leg_site_id
        left join ossdb01db.dd_product_version dpv2 on dslspv2.prod_ver_id = dpv2.id
        where dpv.service_id = '{service_id}'
    )
    select distinct ord.entity_name, spoi.name, oai.id,
        now() - oai.actual_start_date as time_elapsed, oai.implementation_type
    from temp_abhi
    left join ossdb01db.sc_project_order_instance spoi on pv_prj_id = spoi.id
    left join ossdb01db.oss_activity_instance oai on spoi.plan_id = oai.plan_id and oai.is_latest_version = 1
    left join ossdb01ref.oss_ref_attribute ora on oai.spec_ver_id = ora.attribute_value
    left join ossdb01ref.oss_ref_data ord on ora.entity_id = ord.entity_id
    where oai.status='In Progress'
    """
    
    results = execute_query(query)
    if results:
        # Combine all results into a single string
        rca_parts = []
        for r in results:
            entity_name = r.get('entity_name', '')
            name = r.get('name', '')
            time_elapsed = r.get('time_elapsed', '')
            rca_parts.append(f"{entity_name} | {name} | {time_elapsed}")
        return " || ".join(rca_parts)
    return ""


def get_spec_ver_ids(service_id):
    """
    Q8: Get spec_ver_id values for a service_id.
    
    Returns:
        list: List of spec_ver_id values
    """
    query = f"""
    with temp_abhi as (
        select distinct dpv2.project_id as pv_prj_id
        from ossdb01db.dd_product_version dpv
        left join ossdb01db.dd_sol_leg_site_2_prod_version dslspv on dpv.id = dslspv.prod_ver_id
        left join ossdb01db.dd_sol_leg_site_2_prod_version dslspv2 on dslspv.solution_leg_site_id = dslspv2.solution_leg_site_id
        left join ossdb01db.dd_product_version dpv2 on dslspv2.prod_ver_id = dpv2.id
        where dpv.service_id = '{service_id}'
    )
    select distinct oai.spec_ver_id
    from temp_abhi
    left join ossdb01db.sc_project_order_instance spoi on pv_prj_id = spoi.id
    left join ossdb01db.oss_activity_instance oai on spoi.plan_id = oai.plan_id and oai.is_latest_version = 1
    left join ossdb01ref.oss_ref_attribute ora on oai.spec_ver_id = ora.attribute_value
    left join ossdb01ref.oss_ref_data ord on ora.entity_id = ord.entity_id
    where oai.status='In Progress'
    group by oai.spec_ver_id
    """
    
    results = execute_query(query)
    if results:
        return [r.get('spec_ver_id') for r in results if r.get('spec_ver_id')]
    return []


def get_interface(spec_id='28519df3-7986-4d3d-9c8b-5bb0ccc2cc0a'):
    """
    Q9: Get interface from oso_activity_data.
    
    Returns:
        str: Interface
    """
    query = f"""
    select oad.interface from ossdb01db.oso_activity_data oad  
    where oad.spec_id = '{spec_id}'
    """
    
    results = execute_query(query)
    if results:
        interfaces = [r.get('interface', '') for r in results if r.get('interface')]
        return " || ".join(interfaces)
    return ""


def perform_oso_analysis(df_data):
    """
    Perform OSO Analysis on the service activation data.
    Creates analysis with nested loops: Customer_Id -> Site_ID -> Service_Id
    
    Args:
        df_data: DataFrame with service activation data
    
    Returns:
        DataFrame: Analysis results with columns: Customer_Id, Site_ID, Service_Id, RCA, Task_Owner, Workqueue, Interface
    """
    logger.info("Starting OSO Analysis...")
    print("\n" + "=" * 80)
    print("Performing OSO Analysis (Complex Query Logic)")
    print("=" * 80)
    
    analysis_results = []
    
    # Group by Customer_Id and Site_ID
    grouped = df_data.groupby(['Customer_Id', 'Site_ID'])
    total_groups = len(grouped)
    
    print(f"Processing {total_groups} Customer_Id/Site_ID combinations...")
    
    processed = 0
    
    for (customer_id, site_id), group in grouped:
        processed += 1
        
        # Get all Service_Ids for this Site_ID
        service_ids = group['Service_Id'].unique()
        
        if processed % 10 == 0:
            print(f"  Progress: {processed}/{total_groups} processed...")
        
        logger.info(f"Processing Customer_Id: {customer_id}, Site_ID: {site_id}, Services: {len(service_ids)}")
        
        # Process each Service_Id
        for service_id in service_ids:
            try:
                # Q1: Check if there are in-progress activities
                count = check_in_progress_count(service_id)
                
                if count == 0:
                    # Skip if no in-progress activities
                    logger.debug(f"  Service_Id {service_id}: No in-progress activities, skipping")
                    continue
                
                logger.info(f"  Service_Id {service_id}: Found {count} in-progress activities")
                
                # Q2: Get implementation types
                impl_types = get_implementation_types(service_id)
                
                if not impl_types:
                    continue
                
                # Process each implementation type
                for impl_type in impl_types:
                    rca = ""
                    task_owner = ""
                    work_queue = ""
                    interface = ""
                    
                    if impl_type == 'Manual':
                        logger.info(f"    Processing Manual implementation for Service_Id: {service_id}")
                        
                        # Q3: Get RCA details
                        rca = get_rca_details_manual(service_id)
                        
                        # Q4: Get activity IDs
                        activity_ids = get_activity_ids(service_id)
                        
                        # Q5 & Q6: Get task owner and work queue for each activity
                        task_owners = []
                        work_queues = []
                        
                        for activity_id in activity_ids:
                            owner = get_task_owner(activity_id)
                            queue = get_work_queue(activity_id)
                            if owner:
                                task_owners.append(owner)
                            if queue:
                                work_queues.append(queue)
                        
                        task_owner = " || ".join(task_owners) if task_owners else ""
                        work_queue = " || ".join(work_queues) if work_queues else ""
                        
                    elif impl_type == 'Automatic':
                        logger.info(f"    Processing Automatic implementation for Service_Id: {service_id}")
                        
                        # Q7: Get RCA details
                        rca = get_rca_details_automatic(service_id)
                        
                        # Q8: Get spec_ver_ids
                        spec_ver_ids = get_spec_ver_ids(service_id)
                        
                        # Q9: Get interface (using hardcoded spec_id as per Q9)
                        interface = get_interface()
                    
                    # Add result
                    analysis_results.append({
                        'Customer_Id': customer_id,
                        'Site_ID': site_id,
                        'Service_Id': service_id,
                        'RCA': rca,
                        'Task_Owner': task_owner,
                        'Workqueue': work_queue,
                        'Interface': interface
                    })
                    
            except Exception as e:
                logger.error(f"Error processing Service_Id {service_id}: {e}")
                continue
    
    print(f"[OK] Analysis complete: {len(analysis_results)} records generated")
    logger.info(f"OSO Analysis completed: {len(analysis_results)} analysis records")
    
    if analysis_results:
        df_analysis = pd.DataFrame(analysis_results)
        
        # Sort by Customer_Id, Site_ID, Service_Id (parent to child)
        df_analysis = df_analysis.sort_values(['Customer_Id', 'Site_ID', 'Service_Id'], ascending=True)
        
        return df_analysis
    else:
        # Return empty DataFrame with correct columns
        return pd.DataFrame(columns=['Customer_Id', 'Site_ID', 'Service_Id', 'RCA', 'Task_Owner', 'Workqueue', 'Interface'])


# =============================================================================
# EXCEL EXPORT FUNCTION
# =============================================================================

def save_to_excel(df, df_analysis=None, filename=None):
    """
    Save DataFrame to Excel file for email attachment.
    Creates multiple sheets: Service Activation Data + OSO_Analysis
    
    Args:
        df: pandas DataFrame (service activation data)
        df_analysis: pandas DataFrame (OSO analysis data) - optional
        filename: Output filename (auto-generated if None)
    
    Returns:
        str: Path to saved file or None
    """
    try:
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"OSO_Service_Activated_Local_{timestamp}.xlsx"
        
        logger.info(f"Saving data to Excel: {filename}")
        
        print("\n" + "=" * 80)
        print("Saving data to Excel...")
        print("=" * 80)
        
        # Save to Excel with multiple sheets
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Sheet 1: Service Activation Data
            df.to_excel(writer, index=False, sheet_name='Service Activation Data')
            print(f"  Sheet 'Service Activation Data': {len(df)} rows")
            logger.info(f"  Sheet 'Service Activation Data': {len(df)} rows")
            
            # Sheet 2: OSO_Analysis (if provided)
            if df_analysis is not None and not df_analysis.empty:
                df_analysis.to_excel(writer, index=False, sheet_name='OSO_Analysis')
                print(f"  Sheet 'OSO_Analysis': {len(df_analysis)} rows")
                logger.info(f"  Sheet 'OSO_Analysis': {len(df_analysis)} rows")
            else:
                # Create empty sheet with headers
                empty_df = pd.DataFrame(columns=['Customer_Id', 'Site_ID', 'Service_Id', 'RCA', 'Task_Owner', 'Workqueue', 'Interface'])
                empty_df.to_excel(writer, index=False, sheet_name='OSO_Analysis')
                print(f"  Sheet 'OSO_Analysis': 0 rows (no data to analyze)")
                logger.info(f"  Sheet 'OSO_Analysis': 0 rows")
        
        if os.path.exists(filename):
            file_size = os.path.getsize(filename) / 1024
            logger.info(f"[OK] Excel file created: {filename} ({file_size:.2f} KB)")
            print(f"[OK] Excel file saved: {filename}")
            print(f"    Size: {file_size:.2f} KB")
            print(f"    Sheet 1 Records: {len(df)}")
            if df_analysis is not None:
                print(f"    Sheet 2 Records: {len(df_analysis)}")
            print("=" * 80)
            return os.path.abspath(filename)
        
        return None
        
    except Exception as e:
        logger.error(f"[ERROR] Failed to save Excel: {e}")
        print(f"[ERROR] Failed to save Excel: {e}")
        logger.debug(traceback.format_exc())
        return None


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    """
    Main execution flow:
    1. Connect to READ DB
    2. Fetch service activation data
    3. Export to Excel
    4. Send email report
    """
    
    logger.info("=" * 80)
    logger.info("MAIN EXECUTION - Starting")
    logger.info(f"Email Toggle: {'ENABLED' if SEND_EMAIL else 'DISABLED'}")
    logger.info("=" * 80)
    
    print("\n" + "=" * 80)
    print("  OSO Service Activated - Local Data Extractor")
    print(f"  Execution Date: {Execution_Date}")
    print(f"  Execution Time: {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 80)
    
    # ==========================================================================
    # STEP 1: Test Database Connection
    # ==========================================================================
    print("\nStep 1: Testing database connection...")
    logger.info("STEP 1: Testing READ DB connection")
    
    test_conn = get_db_connection()
    if not test_conn:
        print("[ERROR] Database connection failed. Cannot proceed.")
        logger.error("Database connection test failed")
        sys.exit(1)
    else:
        print("[OK] Database connection successful!")
        test_conn.close()
    
    # ==========================================================================
    # STEP 2: Fetch Service Activation Data
    # ==========================================================================
    print("\nStep 2: Fetching service activation data...")
    logger.info("STEP 2: Fetching data from READ DB")
    
    df_data = fetch_service_activation_data()
    
    if df_data is None or df_data.empty:
        print("[ERROR] No data fetched or query failed")
        logger.error("Data fetch failed or returned no results")
        sys.exit(1)
    else:
        print(f"[OK] Retrieved {len(df_data)} records")
        
        # Display sample
        print("\nSample Data (first 3 rows):")
        print("-" * 80)
        print(df_data.head(3).to_string())
        print("-" * 80)
    
    # ==========================================================================
    # STEP 3: Perform OSO Analysis
    # ==========================================================================
    print("\nStep 3: Performing OSO Analysis (complex nested queries)...")
    logger.info("STEP 3: Running OSO Analysis")
    
    df_analysis = None
    try:
        df_analysis = perform_oso_analysis(df_data)
        
        if df_analysis is not None and not df_analysis.empty:
            print(f"[OK] Analysis completed: {len(df_analysis)} analysis records")
        else:
            print("[INFO] Analysis completed but no records generated (no in-progress activities found)")
            logger.info("Analysis completed with no results")
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        logger.debug(traceback.format_exc())
        print(f"[WARNING] Analysis failed: {e}")
        print("[INFO] Continuing with data export only...")
        df_analysis = None
    
    # ==========================================================================
    # STEP 4: Save to Excel
    # ==========================================================================
    print("\nStep 4: Saving to Excel...")
    logger.info("STEP 4: Saving Excel file")
    
    excel_file = save_to_excel(df_data, df_analysis)
    
    if not excel_file:
        print("[ERROR] Failed to create Excel file")
        logger.error("Excel export failed")
        sys.exit(1)
    
    # ==========================================================================
    # STEP 5: Send Email Report
    # ==========================================================================
    email_sent = False
    
    if SEND_EMAIL and excel_file:
        print("\nStep 5: Sending email report...")
        logger.info("STEP 5: Sending email report")
        
        analysis_count = len(df_analysis) if df_analysis is not None else 0
        email_mgr = EmailMgr(excel_file, len(df_data), analysis_count)
        email_sent = email_mgr.send_mail()
        
        if email_sent:
            print("[OK] Email sent successfully!")
        else:
            print("[WARNING] Email sending failed")
    else:
        print("\nStep 5: [SKIPPED - Email toggle is OFF]")
        logger.info("STEP 5: Skipped - Email toggle disabled")
    
    # ==========================================================================
    # Final Summary
    # ==========================================================================
    print("\n" + "=" * 80)
    print("[OK] ALL OPERATIONS COMPLETED!")
    print("=" * 80)
    print(f"Execution Date: {Execution_Date}")
    print(f"Execution Time: {Execution_DateTime}")
    print("-" * 80)
    print(f"Records fetched: {len(df_data)}")
    print(f"Excel file: {excel_file}")
    if SEND_EMAIL:
        print(f"Email sent: {'Yes' if email_sent else 'Failed'}")
    print("=" * 80)
    
    logger.info("=" * 80)
    logger.info("MAIN EXECUTION - Completed Successfully")
    logger.info("=" * 80)
    
    sys.exit(0)

