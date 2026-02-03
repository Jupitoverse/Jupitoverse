import datetime as dt
import logging
import smtplib
import mimetypes
import pandas as pd
from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
 
# Step 1: Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
 
# Step 2: Date-based execution control
Todays_Date_DD = dt.datetime.now().day
Date_Execution_Frequency = 1
 
if Todays_Date_DD % Date_Execution_Frequency != 0:
    logging.info(f"Script is set to execute only on every {Date_Execution_Frequency}th day of the month.")
    exit()
 
logging.info("Date condition met. Proceeding with script execution.")
 
# Step 3: PostgreSQL connection
try:
    import psycopg2
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
    exit()
 
# Step 4: Run query in batches
k = 10
part_ids = list(range(1, 100))  # Example part_ids from 1 to 99
results = []
 
query_template = """
SELECT ord.entity_name AS \"Activity Name\",
           oai.spec_ver_id AS \"Spec Id\",
           aocd.interface AS Interface,

           SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '1 day' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS \"Last 24 Hours\",
           SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '2 days' AND oai.actual_start_date < NOW() - INTERVAL '1 day' THEN 1 ELSE 0 END) AS \"Previous 24 Hours\",
           SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '7 days' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS \"Last 1 Week\",
           SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '1 month' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS \"Last 1 Month\",
           SUM(CASE WHEN oai.actual_start_date >= NOW() - INTERVAL '1 year' AND oai.actual_start_date < NOW() THEN 1 ELSE 0 END) AS \"Last 1 Year\"

    FROM ossdb01db.oss_activity_instance oai
    JOIN ossdb01ref.oss_ref_attribute ora ON oai.spec_ver_id = ora.attribute_value
    JOIN ossdb01ref.oss_ref_data ord ON ora.entity_id = ord.entity_id
    JOIN ossdb01db.activity_overview_custom_data aocd ON oai.spec_ver_id = aocd.spec_id

    WHERE oai.part_id in ({batch_ids})
      AND oai.last_update_date > NOW() - INTERVAL '1 year'
      AND oai.state IN ('In Progress', 'Rework In Progress')
      AND oai.is_latest_version = 1
      AND oai.implementation_type <> 'Manual'
      AND oai.spec_ver_id NOT IN (
          'f1f62e0d-6f07-4c0c-be12-631e07b7448f','3936695f-90a1-4e79-8a60-1b460fcf26b4',
          '85a4f2c9-c720-4f30-bd84-408a36da97c2','20e2328d-f681-4c4a-bdad-43ad9da2b728',
          'bf25901d-eb35-48b8-b4ad-ba39d874cbc4','d30f36e7-c671-471b-aa70-bb5ccbe8939f',
          'b0403ef6-3198-4641-8d11-7630361473b9','4bd19612-5446-4f70-bb85-e05b8bcbc9da',
          '546d9598-8d49-4fb9-b2b7-f11ac62ac1c5','2316fc59-1289-4fbf-ba10-e933cdfd9941',
          '2f4a4d90-bccd-43e4-851f-e70073b1da6a','81c7f66d-a2fc-4d89-bc96-d83ebf70b11c',
          'b0012a40-d80f-4a1e-83ce-d78455d21fdc','b4b7b8c9-e275-409d-8657-0c5ffbb28e59',
          '2580eed6-e91b-497e-9504-dd289765eb03','22a7a5a0-fc32-4af0-a929-08aa860c3c4b',
          '0d409cea-5222-45f5-ae88-109c20919bfb','811131f6-8b6b-4548-a535-8708666d1dda',
          'b5bad4ff-7935-4053-afb5-fb1d25797a44','127ecdcc-b677-4132-a95b-c509cfaa7c60',
          'a4267bbb-c25a-4d93-a7c7-3d96c579b895','1aea0862-2530-43c8-9fb0-dc120166f7f4',
          '0c81c4e0-2681-476f-b7d1-bcf14b829265','fb5043db-c056-4529-be38-db0c1bae3f20',
          'e6880c45-1cbd-4d7a-8c4a-044e667ecda5','e3a7de55-7a84-499d-8cc1-9d227d7c357f',
          '330116f0-e475-4afa-b949-697ac94b0d52','02b9b6b8-44eb-4652-b137-de7d5530416f',
          '3f9849dd-5133-46f2-a789-80a21120554e','09d7e394-39b9-4ef0-b747-bc5eeda5d9fd',
          '7597cb49-d972-4e98-b3f1-84687d4360f5','1287e89f-056b-4c3c-a2a7-e200a012bc92',
          '24e86c2a-6cb5-4e0e-ab11-e00dd14da5e4','f2a616fd-ccb0-4b1f-b413-fc915802fa25',
          '8a112601-d9f2-4d33-ab00-19f4f483104b','88f0860f-e647-41cd-aaac-1930adea8a3c',
          '92286b75-55c8-4991-be47-c04c7b3d9780','fddff199-92dc-4862-b90e-6c2bf32efcda',
          'b9e64a57-b511-4b1c-8eb7-c3d7e9feff25','55c4d13b-19d2-45a9-b1b7-a1b9e874aaff',
          '54d3e8c0-4a06-41bc-b7cf-1749177e9ff1','ce922024-75d4-4af5-9b4e-2e8d6d79f3e2',
          '7277a8b5-9eef-4421-bf4b-06b8494e91c9','bb73d434-f14e-4349-b080-83f747900676',
          '6a0bd4cf-8b31-499b-b331-378beb30a2b9','60fa385f-6e81-43e2-b129-08d72aaa5fc7',
          '776d2d5b-c7fe-49d1-a071-fd4472964c1e'
      )
    GROUP BY ord.entity_name, oai.spec_ver_id, aocd.interface
    ORDER BY \"Last 24 Hours\" DESC;
"""
 
cursor = conn.cursor()
for i in range(0, len(part_ids), k):
    batch = part_ids[i:i+k]
    batch_ids = ', '.join(map(str, batch))
    query = query_template.format(batch_ids=batch_ids)
    try:
        cursor.execute(query)
        batch_result = cursor.fetchall()
        results.extend(batch_result)
        logging.info(f"Executed batch query for part_ids: {batch}")
    except Exception as e:
        logging.error(f"Query failed for batch {batch}: {e}")
 
cursor.close()
conn.close()
 
# Step 5: Store results in Excel and HTML
columns = ['entity_name', 'spec_ver_id', 'less_than_1_months','interface','1 day', '1 week', '1 month', '1 year']
df = pd.DataFrame(results, columns=columns)
 
output_file = "query_results.xlsx"
df.to_excel(output_file, index=False)
logging.info(f"Results saved to Excel file: {output_file}")
 
html_table = df.to_html(index=False, classes='styled-table')
 
# Add CSS styling
html_table = f"""
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
{html_table}
"""
 
# Step 6: Send email
class EmailMgr:
    def __init__(self):
        pass
 
    def send_mail(self):
        recipients = ['abhisha3@amdocs.com']
        cc_recipients = ['abhisha3@amdocs.com']
        FROM = "noreply@amdocs.com"
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = "Abhi_Python Script testing " + dt.datetime.strftime(dt.datetime.now(), "%Y/%m/%d")
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
        email_content = f"""
        <html>
        <body>    
        <p>Please find below the Orion Outage Report for the past 24 hours.</p>
        <p>The first two tables highlight the impact at the project level, listing projects whose statuses have not changed as expected. These discrepancies indicate potential issues, assuming the system had        been functioning correctly.</p>
        <p>The third table outlines activities that remain stuck in either the 'In Progress' or 'Rework In Progress' status. Some of these may be due to pending third-party callbacks.</p>
        <h2>Stuck Activities and their count whose status not changed from 'In Progress' or 'Rework In Progress' in multiple interval as specified in table below</h2>
        {html_table}
        <div class='note'>For any changes in the report: Please reach out to <a href='mailto:abhisha3@amdocs.com'>abhisha3@amdocs.com</a></div>
        <div class='footer'>Regards,<br>Abhishek Agrahari</div>
        </body>
        </html>
        """
        return email_content
 
em = EmailMgr()
em.send_mail()