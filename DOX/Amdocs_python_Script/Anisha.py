import cx_Oracle
import csv
import re
import os
import cx_Oracle
import datetime as dt
import pandas as pd
import xlrd
from datetime import timedelta
from array import *
import numpy as np
import smtplib
import os
import smtplib
import mimetypes
import datetime as dt
from datetime import timedelta
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from time import sleep
from openpyxl import Workbook
 
 
# Database connection details
dsn = cx_Oracle.makedsn("10.105.2.51", 1521, service_name="CMMCM1")
conn = cx_Oracle.connect("CMMAPPC", "cmm_4c0nn", dsn)
today_date=dt.datetime.strftime(dt.datetime.now(),"%Y%m%d")
#output_file = "D2822341_Impacts_{}.xlsx".format(today_date)
output_file="attribute_impacts.xlsx"
cursor = conn.cursor()
 
def fetch_impacts():
    # Attributes and their default values
    attributes = {
        "Service Type": "*",
        "Tax Jurisdiction": "Interstate",
        "Access Provider": "*",
        "EVC Area Type": "Metro",
        "Speed Tier Name": "NA",
    }
 
    # Query template for fetching impacts
 
 
    # Connect to Oracle DB
    #conn = cx_Oracle.connect(DB_USER, DB_PASS, DB_DSN)
    #cursor = conn.cursor()
 
    # Create an Excel workbook
    wb = Workbook()
    wb.remove(wb.active)  # Remove default sheet
 
    # Loop through attributes and execute queries
    for attr_name, default_value in attributes.items():
        print(f"Fetching data for {attr_name}...")
        impact_query_template = f"""
            WITH bkp_asterisk_AP AS (
                SELECT agreement_no, offer_instance_id, param_name, param_values, sys_creation_date, effective_date, expiration_date
                FROM cm1_agreement_param
                WHERE param_name = '{attr_name}' AND param_values = '{default_value}'
                AND TRUNC(sys_creation_date) >= '07-FEB-25'
                AND (expiration_date IS NULL OR (expiration_date IS NOT NULL AND TRUNC(exp_issue_date) >= '07-FEB-25'))
                AND agreement_no IN (
                    SELECT subscriber_no FROM subscriber WHERE customer_id IN (
                        SELECT customer_id FROM customer WHERE bill_cycle IN (101, 115)
                    )
                )
                ORDER BY sys_creation_date DESC
            ),
            correct_asterisk_AP AS (
                SELECT a.*, b.param_values AS old_value
                FROM bkp_asterisk_AP a, cm1_agreement_param b
                WHERE a.agreement_no = b.agreement_no
                AND a.offer_instance_id = b.offer_instance_id
                AND b.param_name = '{attr_name}' AND b.param_values != '{default_value}'
                AND TRUNC(b.expiration_date) = TRUNC(a.effective_date)
            )
            SELECT b.customer_id, cd.target_pcn, c.bill_cycle, b.prim_resource_val, a.*, e.soc_name,
                   TO_DATE(NULL, 'DD-MON-RR HH24:MI:SS') AS patch_date, 'N' AS is_patched
            FROM correct_asterisk_AP a
            JOIN subscriber b ON a.agreement_no = b.subscriber_no
            JOIN customer c ON b.customer_id = c.customer_id
            JOIN service_agreement d ON a.agreement_no = d.agreement_no AND a.offer_instance_id = d.soc_seq_no
            JOIN csm_offer e ON d.soc = e.soc_cd
            JOIN (SELECT DISTINCT agreement_no, target_pcn FROM charge_distribute WHERE expiration_date IS NULL) cd
            ON cd.agreement_no = a.agreement_no;
            """
        # Format query
        #query = impact_query_template.format(attr_name=attr_name, default_value=default_value)
 
        # Execute SQL
        cursor.execute(impact_query_template)
        columns = [col[0] for col in cursor.description]  # Fetch column names
        data = cursor.fetchall()  # Fetch data

        # Convert to pandas DataFrame
        df = pd.DataFrame(data, columns=columns)

        # Write to a new sheet in Excel
        sheet_name = attr_name.replace(" ", "_")  # Ensure valid sheet names
        wb.create_sheet(title=sheet_name)
        with pd.ExcelWriter(output_file, engine="openpyxl", mode="a") as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
 
    # Close DB connection
    cursor.close()
    conn.close()
 
    # Save the Excel workbook
    wb.save(output_file)
    print(f"Data successfully written to {output_file}")
 
# Call the function
fetch_impacts()
 
 
# Close the connection
#cursor.close()
#conn.close()
print("Process completed successfully.")
 
excel_file = output_file
xls = pd.ExcelFile(excel_file)
 
# Create HTML table structure
html_table = "<table border='1'><tr><th>Sheet Name</th><th>Record Count</th></tr>"
 
# Loop through each sheet and get row count
for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet_name)
    row_count = len(df)   # Subtract 1 from total rows
    html_table += f"<tr><td>{sheet_name}</td><td>{row_count}</td></tr>"
 
# Close table structure
html_table += "</table>"
 
# Print or save the generated HTML table
print(html_table)
class EmailMgr:
 
        def __init__(self):
                pass
 
        def send_mail(self):
                recipients = ['anishaji@amdocs.com']
                #cc_recipients = ['GSSGMSCComcastMidMarketBackendScrumTeam@int.amdocs.com']
                #cc_recipients = ['aniket.mahale@amdocs.com','mahesh.kollipara@amdocs.com','manishw@amdocs.com','tushar.nikam@amdocs.com','sirish.katragadda@amdocs.com']
                cc_recipients = ['anishaji@amdocs.com']
                FROM="noreply@amdocs.com;"
                MESSAGE = MIMEMultipart('alternative')
                MESSAGE['subject'] = "D2822341_Impacts "+dt.datetime.strftime(dt.datetime.now(),"%Y/%m/%d")
 
                MESSAGE['To'] = ", ".join(recipients)
                MESSAGE['Cc'] = ", ".join(cc_recipients)
                MESSAGE['From'] = FROM
                MESSAGE.preamble = """
                Your mail reader does not support the report format.
                Please visit us <a href="http://www.mysite.com">online</a>!"""
 
                BODY=self.get_mail_content()
                HTML_BODY = MIMEText(BODY, 'html')
                MESSAGE.attach(HTML_BODY)
                attachments = output_file
 
                ## We'll get the type of file automatically and use a generic coding if no file is recognized
                ctype, encoding = mimetypes.guess_type(attachments)
                if ctype is None or encoding is not None:
                        ctype = 'application/octet-stream'
 
                maintype, subtype = ctype.split('/', 1)
                fp = open(attachments, 'rb')
                part2 = MIMEBase(maintype, subtype)
                part2.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(part2)
                part2.add_header('Content-Disposition', 'attachment', filename=attachments.split("/")[-1])
                MESSAGE.attach(part2)
 
                server = smtplib.SMTP('localhost')
                recipients.extend(cc_recipients)
                server.sendmail(FROM,recipients,MESSAGE.as_string())
                server.quit()
                sleep(3)
                print("Mail Sent successfully!")
        def get_mail_content(self):
                email_content = f"""
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>html title</title>
<html>
<body> <p> D2822341 Impacts </p>
{html_table}
</body>
</html>
                """
 
                return email_content
 
em=EmailMgr()
em.send_mail()
