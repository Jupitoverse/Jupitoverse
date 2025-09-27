import datetime as dt
import logging
import smtplib
import psycopg2
import pandas as pd
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Step 1: Setup logging
log_file = f"execution_log_{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step 2: PostgreSQL connection
try:
    conn = psycopg2.connect(
        database="prodossdb",
        user='ossdb01uams',
        password='Pr0d_ossdb01uams',
        host='oso-pstgr-rd.orion.comcast.com',
        port='6432'
    )
    logging.info("Database connection established successfully.")
except Exception as e:
    logging.error(f"Database connection failed: {e}")
    raise

cursor = conn.cursor()

# Step 3: SQL query template
base_sql = """
SELECT spoi.id AS projectid, spoi.version, oai.status AS activity_status, spoi.status AS project_status, oai.id AS activity_id,
       spoi.name, oai2.last_update_date, oai.create_date
FROM ossdb01db.sc_project_order_instance spoi,
     ossdb01db.oss_activity_instance oai,
     ossdb01db.oss_activity_instance oai2
WHERE spoi.plan_id = oai.plan_id
  AND oai.plan_id = oai2.plan_id
  AND oai2.spec_ver_id = '91757a68-692f-4246-91e1-7e2280a659d8'
  AND oai2.state IN ('Completed')
  AND oai2.is_latest_version = 1
  AND oai.spec_ver_id = '03acd7f1-557a-4727-ba2e-8d44f6245047'
  AND oai.state IN ('In Progress', 'Optional')
  AND DATE_PART('day', CURRENT_DATE - oai2.complete_date) > 10
  AND spoi.status NOT IN ('FCANCELLED', 'DCOMPLETED')
  AND spoi.manager IS DISTINCT FROM 'ProductionSanity'
  AND oai.is_latest_version = 1
  AND spoi.is_latest_version = 1
  AND spoi.name NOT LIKE '%MM_PROD_TEST%'
  AND oai.part_id BETWEEN {start} AND {end};
"""

# Step 4: Run queries and collect results
results = []
for start, end in [(1, 10), (11, 20), (21, 30),(31, 40),(41, 50),(51, 60),(61, 70),(71, 80),(81, 90),(91, 99)]:
    query = base_sql.format(start=start, end=end)
    logging.info(f"Running query for part_id BETWEEN {start} AND {end}")
    cursor.execute(query)
    batch_results = cursor.fetchall()
    results.extend(batch_results)
    logging.info(f"Fetched {len(batch_results)} rows for part_id BETWEEN {start} AND {end}")

cursor.close()
conn.close()

# Step 5: Convert results to DataFrame and HTML
columns = ["projectid", "version", "activity_status", "project_status", "activity_id", "name", "last_update_date", "create_date"]
df = pd.DataFrame(results, columns=columns)

output_file = "ponr_report.xlsx"
df.to_excel(output_file, index=False)

html_table = df.to_html(index=False, classes='styled-table')

# Step 6: Email manager
class EmailMgr:
    def send_mail(self):
        recipients = ['abhisha3@amdocs.com']
        #recipients = ['abhisha3@amdocs.com','Enna.Arora@amdocs.com','Nishant.Bhatia@amdocs.com','prateek.jain5@amdocs.com','mukul.bhasin@amdocs.com','Alon.Kugel@Amdocs.com','Shreyas.Kulkarni@amdocs.com', 'Smitesh.Kadia@amdocs.com']
        cc_recipients = ['abhisha3@amdocs.com']
        FROM = "noreply@amdocs.com"
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = "Comcast OSS || Orion Outage Report for " + dt.datetime.strftime(dt.datetime.now(), "%Y/%m/%d")
        MESSAGE['To'] = ", ".join(recipients)
        MESSAGE['Cc'] = ", ".join(cc_recipients)
        MESSAGE['From'] = FROM

        BODY = self.get_mail_content()
        HTML_BODY = MIMEText(BODY, 'html')
        MESSAGE.attach(HTML_BODY)

        ctype, encoding = mimetypes.guess_type(output_file)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'

        maintype, subtype = ctype.split('/', 1)
        with open(output_file, 'rb') as fp:
            part2 = MIMEBase(maintype, subtype)
            part2.set_payload(fp.read())
        encoders.encode_base64(part2)
        part2.add_header('Content-Disposition', 'attachment', filename=output_file)
        MESSAGE.attach(part2)

        try:
            server = smtplib.SMTP('localhost')
            recipients.extend(cc_recipients)
            server.sendmail(FROM, recipients, MESSAGE.as_string())
            server.quit()
            logging.info("Mail sent successfully!")
        except Exception as e:
            logging.error(f"Failed to send email: {e}")

    def get_mail_content(self):
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
        <p>Hi Team,</p>
        <p>Please find below the list of orders where the RELEASE PONR flag was not triggered by the system, even though the mandatory wait period associated with the Registered Timed Action has been completed</p>
        <p>Kindly review these orders and take the necessary corrective actions. This issue is impacting the business, as services have already been ceased at the customer sites, but billing continues to be active.</p>
        {html_table}
        <div class='note'>For any changes in the report: Please reach out to mailto:abhisha3@amdocs.comabhisha3@amdocs.com</a></div>
        <div class='footer'>Regards,<br>Abhishek Agrahari</div>
        </body>
        </html>
        """
# Step 7: Send email
em = EmailMgr()
em.send_mail()
logging.info("Script completed successfully.")















