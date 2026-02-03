================================================================================
Service_Activated.py - Quick Reference
================================================================================

PURPOSE:
  Windows Remote Desktop compatible script that connects to MySQL database,
  generates Excel report, and sends email via Outlook.

REQUIREMENTS:
  pip install mysql-connector-python pandas openpyxl pywin32

DATABASE:
  Host:     oriontrack600.oncomcast.com
  Database: tier1ops
  Port:     3306
  User:     WUATAdmin
  Password: Welcome1

EMAIL:
  Recipient: abhishek_agrahari@comcast.com
  Method:    Outlook COM object (Windows only)
  Fallback:  Creates email draft file if Outlook fails

USAGE:
  
  # Full run (with email)
  python Service_Activated.py
  
  # Dry run (no email)
  python Service_Activated.py --dry-run

WHAT IT DOES:
  
  Step 1: Tests database connection
  Step 2: Fetches data from 'activated_not_billing' table
  Step 3: Saves to Excel (timestamped filename)
  Step 4: Sends email via Outlook (or creates draft)

OUTPUT FILES:
  - Activated_Not_Billing_Report_YYYYMMDD_HHMMSS.xlsx (data)
  - Email_Draft_YYYYMMDD_HHMMSS.txt (if Outlook fails)

FEATURES:
  [OK] Windows RDP compatible
  [OK] Uses Outlook for email (native Windows)
  [OK] Comprehensive logging
  [OK] Detailed error messages
  [OK] Creates email draft as fallback
  [OK] No Unix dependencies
  [OK] Email to: abhishek_agrahari@comcast.com

TROUBLESHOOTING:
  
  Connection failed?
    - Check VPN connection
    - Verify network access to database
    - Check firewall settings
  
  Email failed?
    - Script will create Email_Draft_*.txt file
    - Manually send email using the draft
  
  pywin32 not installed?
    - Run: pip install pywin32
    - Or use --dry-run to skip email

================================================================================
Author: Abhishek
Date: 2025-01-27
Version: 3.0 (Windows RDP)
================================================================================

