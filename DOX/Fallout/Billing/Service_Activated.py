#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Service_Activated_Windows.py - Billing Report Automation Script (Windows RDP)
================================================================================

DESCRIPTION:
    Windows-compatible script for Remote Desktop machines.
    Connects to MySQL database, generates Excel report, and sends email.

DATABASE INFO:
    - Type: MySQL
    - Host: oriontrack600.oncomcast.com
    - Database: tier1ops
    - Port: 3306
    - User: WUATAdmin
    - Password: Welcome1

REQUIREMENTS:
    pip install mysql-connector-python pandas openpyxl

USAGE:
    # Full run (with email)
    python Service_Activated_Windows.py
    
    # Dry run (without email)
    python Service_Activated_Windows.py --dry-run

AUTHOR: Abhishek
CREATED: 2025-01-27
VERSION: 3.0 (Windows RDP Compatible)
================================================================================
"""

import sys
import os
from datetime import datetime
import logging
import traceback

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# =============================================================================
# IMPORT REQUIRED LIBRARIES
# =============================================================================

logger.info("=" * 80)
logger.info("Service_Activated_Windows.py - Starting")
logger.info("=" * 80)

# Check for MySQL connector
try:
    import mysql.connector
    from mysql.connector import Error as MySQLError
    logger.info("[OK] mysql-connector-python imported successfully")
except ImportError:
    logger.error("[ERROR] mysql-connector-python not installed!")
    print("\n" + "=" * 80)
    print("[ERROR] mysql-connector-python not installed!")
    print("=" * 80)
    print("\nTo install, run:")
    print("  pip install mysql-connector-python")
    print("=" * 80)
    sys.exit(1)

# Check for pandas
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
# CONFIGURATION
# =============================================================================

DB_CONFIG = {
    'host': 'oriontrack600.oncomcast.com',
    'database': 'tier1ops',
    'port': 3306,
    'user': 'WUATAdmin',
    'password': 'Welcome1',
    'connection_timeout': 30
}

EMAIL_CONFIG = {
    'recipient': 'abhishek_agrahari@comcast.com',
    'subject_prefix': 'Billing - Activated Not Billing Report'
}

logger.info(f"Database: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
logger.info(f"Email Recipient: {EMAIL_CONFIG['recipient']}")

# =============================================================================
# DATABASE FUNCTIONS
# =============================================================================

def get_db_connection():
    """
    Establish MySQL database connection.
    
    Returns:
        connection object or None
    """
    try:
        logger.info("Connecting to MySQL database...")
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            connection_timeout=DB_CONFIG['connection_timeout']
        )
        
        if connection.is_connected():
            logger.info("[OK] Database connection established")
            return connection
        else:
            logger.error("[ERROR] Connection failed")
            return None
            
    except MySQLError as e:
        logger.error(f"[ERROR] MySQL Error: {e}")
        return None
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error: {e}")
        return None


def test_db_connection():
    """
    Test database connection and display information.
    
    Returns:
        bool: True if successful, False otherwise
    """
    connection = None
    cursor = None
    
    try:
        print("\n" + "=" * 80)
        print("Testing MySQL Database Connection...")
        print("=" * 80)
        print(f"Host:     {DB_CONFIG['host']}")
        print(f"Database: {DB_CONFIG['database']}")
        print(f"Port:     {DB_CONFIG['port']}")
        print(f"User:     {DB_CONFIG['user']}")
        print("-" * 80)
        
        connection = get_db_connection()
        
        if not connection or not connection.is_connected():
            print("[ERROR] CONNECTION FAILED!")
            print("=" * 80)
            return False
        
        print("[OK] CONNECTION SUCCESSFUL!")
        print("-" * 80)
        
        cursor = connection.cursor(dictionary=True)
        
        # Get MySQL version
        cursor.execute("SELECT VERSION() AS version")
        result = cursor.fetchone()
        print(f"MySQL Version: {result['version']}")
        
        # Get current database
        cursor.execute("SELECT DATABASE() AS current_db")
        result = cursor.fetchone()
        print(f"Current Database: {result['current_db']}")
        
        # Check for target table
        cursor.execute("""
            SELECT COUNT(*) AS table_exists
            FROM information_schema.tables 
            WHERE table_schema = %s AND table_name = 'activated_not_billing'
        """, (DB_CONFIG['database'],))
        result = cursor.fetchone()
        
        if result['table_exists'] > 0:
            print("\n[OK] Target table 'activated_not_billing' found!")
            
            # Get row count
            cursor.execute("SELECT COUNT(*) AS row_count FROM activated_not_billing")
            result = cursor.fetchone()
            print(f"  Row count: {result['row_count']}")
        else:
            print("\n[WARNING] Target table 'activated_not_billing' NOT found!")
        
        print("=" * 80)
        print("[OK] Database connection test completed successfully!")
        print("=" * 80)
        
        return True
        
    except MySQLError as e:
        logger.error(f"[ERROR] MySQL Error: {e}")
        print("[ERROR] DATABASE CONNECTION FAILED!")
        print(f"Error: {e}")
        print("=" * 80)
        return False
        
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error: {e}")
        print("[ERROR] UNEXPECTED ERROR!")
        print(f"Error: {e}")
        print("=" * 80)
        return False
        
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            logger.info("Database connection closed")


def fetch_activated_not_billing_data():
    """
    Fetch data from activated_not_billing table.
    
    Returns:
        pandas DataFrame or None
    """
    connection = None
    cursor = None
    
    try:
        logger.info("Fetching data from 'activated_not_billing' table...")
        
        print("\n" + "=" * 80)
        print("Fetching Activated Not Billing Data...")
        print("=" * 80)
        
        connection = get_db_connection()
        if not connection:
            logger.error("Failed to establish connection")
            return None
        
        # SQL query
        query = """
            SELECT 
                anb.customer_id,
                anb.site_id,
                anb.service_id,
                anb.product_agreement_instance_id,
                anb.version,
                anb.business_action,
                anb.solution_id,
                anb.ptd,
                anb.activation_date,
                anb.customer_accepted
            FROM activated_not_billing anb
            ORDER BY anb.ptd, anb.customer_id, anb.site_id, anb.product_agreement_instance_id
        """
        
        logger.info("Executing query...")
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        
        results = cursor.fetchall()
        logger.info(f"Fetched {len(results)} rows")
        
        if not results:
            logger.warning("Query returned no results")
            print("[WARNING] No data found")
            print("=" * 80)
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame(results)
        
        logger.info(f"DataFrame created - Shape: {df.shape}")
        print(f"[OK] Fetched {len(df)} records")
        print(f"Columns: {', '.join(df.columns.tolist())}")
        print("=" * 80)
        
        return df
        
    except MySQLError as e:
        logger.error(f"[ERROR] MySQL Error: {e}")
        print(f"[ERROR] Database error: {e}")
        return None
        
    except Exception as e:
        logger.error(f"[ERROR] Unexpected error: {e}")
        print(f"[ERROR] Error: {e}")
        return None
        
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


# =============================================================================
# FILE EXPORT FUNCTIONS
# =============================================================================

def save_to_excel(df, filename=None):
    """
    Save DataFrame to Excel file.
    
    Args:
        df: pandas DataFrame
        filename: Output filename (auto-generated if None)
    
    Returns:
        str: Path to saved file or None
    """
    try:
        logger.info("Saving data to Excel...")
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"Activated_Not_Billing_Report_{timestamp}.xlsx"
        
        print("\n" + "=" * 80)
        print("Saving data to Excel...")
        print("=" * 80)
        print(f"Filename: {filename}")
        print(f"Records:  {len(df)}")
        print(f"Columns:  {len(df.columns)}")
        print("-" * 80)
        
        logger.info(f"Writing to Excel file: {filename}")
        df.to_excel(filename, index=False, engine='openpyxl', sheet_name='Activated Not Billing')
        
        if os.path.exists(filename):
            file_size = os.path.getsize(filename)
            file_size_kb = file_size / 1024
            
            logger.info(f"[OK] File created: {filename} ({file_size_kb:.2f} KB)")
            print(f"[OK] File saved successfully!")
            print(f"  Path: {os.path.abspath(filename)}")
            print(f"  Size: {file_size_kb:.2f} KB")
            print("=" * 80)
            
            return os.path.abspath(filename)
        else:
            logger.error("File was not created")
            print("[ERROR] File was not created")
            return None
        
    except Exception as e:
        logger.error(f"[ERROR] Error saving Excel: {e}")
        print(f"[ERROR] Error saving to Excel: {e}")
        return None


# =============================================================================
# EMAIL FUNCTIONS
# =============================================================================

def send_email_with_outlook(excel_file, df):
    """
    Send email using Outlook COM object (Windows only).
    
    Args:
        excel_file: Path to Excel attachment
        df: DataFrame for preview
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logger.info("Attempting to send email via Outlook...")
        
        print("\n" + "=" * 80)
        print("Sending Email via Outlook...")
        print("=" * 80)
        
        # Import win32com for Outlook
        try:
            import win32com.client
        except ImportError:
            logger.error("[ERROR] pywin32 not installed!")
            print("[ERROR] pywin32 not installed!")
            print("To install: pip install pywin32")
            print("=" * 80)
            return False
        
        # Validate Excel file
        if not os.path.exists(excel_file):
            logger.error(f"Excel file not found: {excel_file}")
            print(f"[ERROR] Excel file not found: {excel_file}")
            return False
        
        # Create Outlook application object
        outlook = win32com.client.Dispatch("Outlook.Application")
        mail = outlook.CreateItem(0)  # 0 = MailItem
        
        # Set email properties
        mail.To = EMAIL_CONFIG['recipient']
        mail.Subject = f"{EMAIL_CONFIG['subject_prefix']} - {datetime.now().strftime('%Y-%m-%d')}"
        
        # Create HTML body
        html_body = f"""
        <html>
        <head>
        <style>
        body {{
            font-family: Calibri, Arial, sans-serif;
            font-size: 11pt;
            color: #000000;
        }}
        h3 {{
            color: #1F4E78;
            margin-bottom: 10px;
        }}
        table {{
            border-collapse: collapse;
            font-size: 10pt;
            margin-top: 15px;
        }}
        th, td {{
            border: 1px solid #CCCCCC;
            padding: 6px 10px;
            text-align: left;
        }}
        th {{
            background-color: #4472C4;
            color: white;
            font-weight: bold;
        }}
        .info-box {{
            background-color: #E7F3FF;
            border-left: 4px solid #1F4E78;
            padding: 10px;
            margin: 15px 0;
        }}
        </style>
        </head>
        <body>
        <p>Hi Team,</p>
        
        <p>Please find attached the <strong>Activated Not Billing Report</strong> for services that have been activated but are not yet billing.</p>
        
        <div class="info-box">
        <strong>Report Summary:</strong><br>
        - Total Records: <strong>{len(df)}</strong><br>
        - Report Date: <strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong><br>
        - Database: <strong>{DB_CONFIG['database']}@{DB_CONFIG['host']}</strong>
        </div>
        
        <p><strong>Report Columns:</strong></p>
        <ul>
            <li>Customer ID</li>
            <li>Site ID</li>
            <li>Service ID</li>
            <li>Product Agreement Instance ID</li>
            <li>Version</li>
            <li>Business Action</li>
            <li>Solution ID</li>
            <li>PTD (Planned Target Date)</li>
            <li>Activation Date</li>
            <li>Customer Accepted</li>
        </ul>
        
        <p><strong>Note:</strong> Complete data is available in the attached Excel file.</p>
        
        <p>Best Regards,<br>
        Billing Automation Team</p>
        </body>
        </html>
        """
        
        mail.HTMLBody = html_body
        
        # Attach Excel file
        mail.Attachments.Add(excel_file)
        logger.info(f"Attached file: {os.path.basename(excel_file)}")
        
        # Send email
        print(f"To: {EMAIL_CONFIG['recipient']}")
        print(f"Subject: {mail.Subject}")
        print(f"Attachment: {os.path.basename(excel_file)}")
        print("-" * 80)
        
        mail.Send()
        
        logger.info("[OK] Email sent successfully via Outlook")
        print("[OK] Email sent successfully!")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        logger.error(f"[ERROR] Failed to send email: {e}")
        logger.debug(traceback.format_exc())
        print(f"[ERROR] Failed to send email: {e}")
        print("=" * 80)
        return False


def send_email_alternative(excel_file, df):
    """
    Alternative email method: Save email draft for manual sending.
    
    Args:
        excel_file: Path to Excel attachment
        df: DataFrame for info
    
    Returns:
        bool: True if draft saved
    """
    try:
        logger.info("Creating email draft file...")
        
        print("\n" + "=" * 80)
        print("Creating Email Draft...")
        print("=" * 80)
        
        draft_file = f"Email_Draft_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        draft_content = f"""
TO: {EMAIL_CONFIG['recipient']}
SUBJECT: {EMAIL_CONFIG['subject_prefix']} - {datetime.now().strftime('%Y-%m-%d')}
ATTACHMENT: {excel_file}

---

Hi Team,

Please find attached the Activated Not Billing Report for services that have been 
activated but are not yet billing.

REPORT SUMMARY:
- Total Records: {len(df)}
- Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- Database: {DB_CONFIG['database']}@{DB_CONFIG['host']}

REPORT COLUMNS:
- Customer ID
- Site ID
- Service ID
- Product Agreement Instance ID
- Version
- Business Action
- Solution ID
- PTD (Planned Target Date)
- Activation Date
- Customer Accepted

Note: Complete data is available in the attached Excel file.

Best Regards,
Billing Automation Team

---
INSTRUCTIONS:
1. Copy the email address from "TO:" line
2. Copy the subject from "SUBJECT:" line
3. Attach the file from "ATTACHMENT:" line
4. Copy the message body above
5. Send the email manually

"""
        
        with open(draft_file, 'w') as f:
            f.write(draft_content)
        
        print(f"[OK] Email draft saved: {draft_file}")
        print(f"[INFO] Please send email manually using the draft")
        print("=" * 80)
        
        logger.info(f"Email draft created: {draft_file}")
        return True
        
    except Exception as e:
        logger.error(f"[ERROR] Failed to create email draft: {e}")
        print(f"[ERROR] Failed to create draft: {e}")
        return False


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    """
    Main execution flow:
    1. Test database connection
    2. Fetch data
    3. Save to Excel
    4. Send email (or create draft)
    """
    
    logger.info("=" * 80)
    logger.info("MAIN EXECUTION - Starting")
    logger.info("=" * 80)
    
    print("\n" + "=" * 80)
    print("  Service Activated - Billing Report Script (Windows)")
    print("=" * 80)
    
    # Check for dry-run flag
    skip_email = '--dry-run' in sys.argv or '--no-email' in sys.argv
    
    if skip_email:
        logger.info("DRY-RUN mode enabled")
        print("\n[INFO] Running in DRY-RUN mode (email will not be sent)\n")
    
    # ==========================================================================
    # STEP 1: Test Database Connection
    # ==========================================================================
    print("\nStep 1: Testing database connection...")
    logger.info("STEP 1: Testing database connection")
    
    success = test_db_connection()
    
    if not success:
        logger.error("Database connection test failed")
        print("\n[ERROR] Database connection failed.")
        print("Please check:")
        print("  1. Network connectivity")
        print("  2. VPN connection (if required)")
        print("  3. Database credentials")
        print("  4. Firewall settings")
        sys.exit(1)
    
    # ==========================================================================
    # STEP 2: Fetch Data
    # ==========================================================================
    print("\nStep 2: Fetching data...")
    logger.info("STEP 2: Fetching data")
    
    df = fetch_activated_not_billing_data()
    
    if df is None or df.empty:
        logger.error("No data retrieved")
        print("[ERROR] No data retrieved or query failed.")
        sys.exit(1)
    
    print(f"\n[OK] Retrieved {len(df)} records")
    
    # Display sample data
    print("\nSample Data (first 5 rows):")
    print("-" * 80)
    print(df.head().to_string())
    print("-" * 80)
    
    # ==========================================================================
    # STEP 3: Save to Excel
    # ==========================================================================
    print("\nStep 3: Saving to Excel...")
    logger.info("STEP 3: Saving to Excel")
    
    excel_file = save_to_excel(df)
    
    if not excel_file:
        logger.error("Failed to save Excel file")
        print("[ERROR] Failed to save Excel file.")
        sys.exit(1)
    
    # ==========================================================================
    # STEP 4: Send Email
    # ==========================================================================
    if skip_email:
        logger.info("STEP 4: Skipped (dry-run mode)")
        print("\n[INFO] Skipping email (dry-run mode)")
        print("=" * 80)
        print("[OK] DRY-RUN COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print(f"Records: {len(df)}")
        print(f"Excel file: {excel_file}")
        print(f"Email: Not sent (dry-run mode)")
        print("=" * 80)
        sys.exit(0)
    
    print("\nStep 4: Sending email...")
    logger.info("STEP 4: Sending email")
    
    # Try Outlook first
    email_sent = send_email_with_outlook(excel_file, df)
    
    # If Outlook fails, create draft
    if not email_sent:
        logger.warning("Outlook failed, creating email draft")
        print("\n[WARNING] Outlook email failed, creating draft instead...")
        send_email_alternative(excel_file, df)
    
    # Final summary
    print("\n" + "=" * 80)
    if email_sent:
        print("[OK] ALL OPERATIONS COMPLETED SUCCESSFULLY!")
    else:
        print("[OK] REPORT GENERATED - EMAIL DRAFT CREATED")
    print("=" * 80)
    print(f"Records: {len(df)}")
    print(f"Excel file: {excel_file}")
    print(f"Email: {'Sent' if email_sent else 'Draft created'}")
    print("=" * 80)
    
    logger.info("=" * 80)
    logger.info("MAIN EXECUTION - Completed")
    logger.info("=" * 80)
    
    sys.exit(0)

