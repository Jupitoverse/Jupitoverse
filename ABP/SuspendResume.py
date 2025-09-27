import cx_Oracle
import os
import csv
import re
import pandas as pd
import datetime as dt
import mimetypes
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from time import sleep

# Database connection details
dsn = cx_Oracle.makedsn("10.105.2.51", 1521, service_name="CMMCM1")
conn = cx_Oracle.connect("CMMAPPC", "cmm_4c0nn", dsn)
today_date = dt.datetime.now().strftime("%Y%m%d")
output_file = f"suspend_resume_issues{today_date}.xlsx"
cursor = conn.cursor()


# Define SQL queries
select_queries = [
    # Suspend query
    """
    WITH partial_suspend_data AS (
        SELECT customer_id, site_id, effective_date, expiration_date, account_id, suspend_project_id
        FROM cm9_odo_request_history a
        WHERE a.expiration_date IS NULL
          AND EXISTS (
              SELECT 1
              FROM subscriber b
              WHERE b.l9_site_id = a.site_id
                AND b.subscriber_no IN (
                    SELECT DISTINCT c.agreement_no
                    FROM charge_distribute c
                    WHERE c.target_pcn = a.account_id
                      AND c.expiration_date IS NULL
                )
                AND b.sub_status IN ('A')
          )
          AND a.effective_date = (
              SELECT MAX(d.effective_date)
              FROM cm9_odo_request_history d
              WHERE d.site_id = a.site_id
          )
    )
    SELECT a.customer_id, a.site_id, a.effective_date AS suspend_date, a.account_id, a.suspend_project_id,
           LISTAGG(b.prim_resource_val, ' ') WITHIN GROUP (ORDER BY b.subscriber_no) AS service_id,
           LISTAGG(b.sub_status, ',') WITHIN GROUP (ORDER BY b.subscriber_no) AS subscriber_status
    FROM partial_suspend_data a, subscriber b
    WHERE b.l9_site_id = a.site_id
      AND b.init_act_date < a.effective_date
    GROUP BY a.customer_id, a.site_id, a.effective_date, a.account_id, a.suspend_project_id
    ORDER BY a.effective_date DESC
    """,

    # Resume query
    """
    WITH partial_resume_data AS (
        SELECT customer_id, site_id, effective_date, expiration_date, account_id, suspend_project_id
        FROM cm9_odo_request_history a
        WHERE a.expiration_date IS NOT NULL
          AND EXISTS (
              SELECT 1
              FROM subscriber b
              WHERE b.l9_site_id = a.site_id
                AND b.subscriber_no IN (
                    SELECT DISTINCT c.agreement_no
                    FROM charge_distribute c
                    WHERE c.target_pcn = a.account_id
                      AND c.expiration_date IS NULL
                )
                AND b.sub_status IN ('S')
          )
          AND a.effective_date = (
              SELECT MAX(d.effective_date)
              FROM cm9_odo_request_history d
              WHERE d.site_id = a.site_id
          )
         
    )
    SELECT a.customer_id, a.site_id, a.effective_date AS suspend_date, a.expiration_date AS restore_date,
           a.account_id, a.suspend_project_id,
           LISTAGG(b.prim_resource_val, ' ') WITHIN GROUP (ORDER BY b.subscriber_no) AS service_id,
           LISTAGG(b.sub_status, ',') WITHIN GROUP (ORDER BY b.subscriber_no) AS subscriber_status
    FROM partial_resume_data a, subscriber b
    WHERE b.l9_site_id = a.site_id
      AND b.init_act_date < a.effective_date
    GROUP BY a.customer_id, a.site_id, a.effective_date, a.account_id, a.suspend_project_id, a.expiration_date
    ORDER BY a.effective_date DESC
    """
]

sheet_names = ["Incomplete_Suspend", "Incomplete_Resume"]

# Save query results to Excel
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for query, sheet_name in zip(select_queries, sheet_names):
        try:
            df = pd.read_sql(query, conn)
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"âœ… Data saved to sheet '{sheet_name}'")
        except Exception as e:
            print(f"âŒ Error executing query for {sheet_name}: {e}")

# Close DB connection
cursor.close()
conn.close()
print("âœ… Process completed successfully.")

# Generate HTML summary table
xls = pd.ExcelFile(output_file)
html_table = """
<table style='border-collapse: collapse; width: 50%; font-family: Arial, sans-serif; font-size: 14px;'>
    <tr style='background-color: #f2f2f2;'>
        <th style='border: 1px solid #999; padding: 8px; text-align: left;'>Sheet Name</th>
        <th style='border: 1px solid #999; padding: 8px; text-align: right;'>Record Count</th>
    </tr>
"""

for sheet_name in xls.sheet_names:
    df = pd.read_excel(xls, sheet_name=sheet_name)
    row_count = len(df)
    html_table += f"""
    <tr>
        <td style='border: 1px solid #999; padding: 8px;'>{sheet_name}</td>
        <td style='border: 1px solid #999; padding: 8px; text-align: right;'>{row_count}</td>
    </tr>
    """

html_table += "</table>"
print(html_table)

# Email manager class
class EmailMgr:
    def __init__(self):
        pass

    def send_mail(self):
        recipients = [
            'Abhishs49@amdocs.com','anishaji@amdocs.com','abhishek.bajpai@amdocs.com'
        ]
        cc_recipients = ['Abhishs49@amdocs.com']
        FROM = "noreply@amdocs.com"

        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['Subject'] = f"Partial Suspend Resume {dt.datetime.now().strftime('%Y/%m/%d')}"
        MESSAGE['To'] = ", ".join(recipients)
        MESSAGE['Cc'] = ", ".join(cc_recipients)
        MESSAGE['From'] = FROM

        BODY = self.get_mail_content()
        HTML_BODY = MIMEText(BODY, 'html')
        MESSAGE.attach(HTML_BODY)

        # Attach Excel file
        ctype, encoding = mimetypes.guess_type(output_file)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)

        with open(output_file, 'rb') as fp:
            part = MIMEBase(maintype, subtype)
            part.set_payload(fp.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(output_file))
            MESSAGE.attach(part)

        # Send email
        server = smtplib.SMTP('localhost')
        all_recipients = recipients + cc_recipients
        server.sendmail(FROM, all_recipients, MESSAGE.as_string())
        server.quit()
        sleep(3)
        print("ðŸ“§ Mail sent successfully!")

    def get_mail_content(self):
        return f"""
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <html>
            <body>
               <!--  <p>Suspend Resume Issues </p> -->
                {html_table}
            </body>
        </html>
        """

# Send the email
em = EmailMgr()
em.send_mail()
