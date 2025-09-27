"""
RELEASE PONR (Point of No Return) Analysis Script

This script identifies orders where the RELEASE PONR flag was not triggered by the system,
even though the mandatory wait period associated with the Registered Timed Action has been completed.

QUERY OPTIMIZATION APPROACHES:
==============================

1. STAGED APPROACH ('staged'):
   - Breaks the complex query into multiple smaller queries
   - Caches eligible projects to avoid repeated scans
   - Filters data progressively to reduce dataset size
   - Best for: Production environments with large datasets
   - Pros: Minimal database load, better error handling
   - Cons: More complex logic, slightly more memory usage

2. SIMPLE APPROACH ('simple'):
   - Uses proper INNER JOINs instead of comma-separated tables
   - Optimized WHERE clause ordering
   - Single query execution per part_id range
   - Best for: Medium-sized datasets, development environments
   - Pros: Simpler logic, single query per batch
   - Cons: Higher database load than staged approach

3. CTE APPROACH ('cte'):
   - Uses Common Table Expressions for better query organization
   - Separates concerns into logical chunks
   - Database optimizer can better understand the query structure
   - Best for: Modern PostgreSQL versions with good CTE optimization
   - Pros: Clean query structure, potentially better execution plans
   - Cons: May not be supported on older database versions

CONFIGURATION:
=============
Change QUERY_APPROACH variable to switch between approaches:
- 'staged': Multi-stage approach (recommended for production)
- 'simple': Single optimized query (good for testing)
- 'cte': CTE-based query (for modern databases)

PERFORMANCE TIPS:
================
1. Ensure indexes exist on:
   - oss_activity_instance.part_id
   - oss_activity_instance.spec_ver_id
   - oss_activity_instance.plan_id
   - oss_activity_instance.state
   - oss_activity_instance.is_latest_version
   - sc_project_order_instance.plan_id
   - sc_project_order_instance.status
   - sc_project_order_instance.is_latest_version

2. Monitor execution times and adjust part_id ranges if needed
3. Consider running during off-peak hours for production databases
"""

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

# Step 3: Optimized SQL query with proper JOINs and staged approach
# First, get eligible projects to reduce the dataset
project_filter_sql = """
SELECT DISTINCT spoi.id, spoi.plan_id, spoi.version, spoi.status, spoi.name
FROM ossdb01db.sc_project_order_instance spoi
WHERE spoi.status NOT IN ('FCANCELLED', 'DCOMPLETED')
  AND spoi.name NOT LIKE '%MM_PROD_TEST%'
  AND spoi.name NOT LIKE '%MM_Prod_Test%'
  AND spoi.manager IS DISTINCT FROM 'ProductionSanity'
  AND spoi.is_latest_version = 1;
"""

# Main optimized query template
base_sql = """
WITH eligible_projects AS (
    SELECT DISTINCT spoi.id, spoi.plan_id, spoi.version, spoi.status, spoi.name
    FROM ossdb01db.sc_project_order_instance spoi
    WHERE spoi.status NOT IN ('FCANCELLED', 'DCOMPLETED')
      AND spoi.name NOT LIKE '%MM_PROD_TEST%'
      AND spoi.name NOT LIKE '%MM_Prod_Test%'
      AND spoi.manager IS DISTINCT FROM 'ProductionSanity'
      AND spoi.is_latest_version = 1
),
completed_activities AS (
    SELECT oai2.plan_id, oai2.last_update_date, oai2.complete_date
    FROM ossdb01db.oss_activity_instance oai2
    WHERE oai2.spec_ver_id = '91757a68-692f-4246-91e1-7e2280a659d8'
      AND oai2.state = 'Completed'
      AND oai2.is_latest_version = 1
      AND oai2.complete_date < CURRENT_DATE - INTERVAL '10 days'
),
in_progress_activities AS (
    SELECT oai.plan_id, oai.id, oai.status, oai.create_date
    FROM ossdb01db.oss_activity_instance oai
    WHERE oai.spec_ver_id = '03acd7f1-557a-4727-ba2e-8d44f6245047'
      AND oai.state IN ('In Progress', 'Optional')
      AND oai.is_latest_version = 1
      AND oai.part_id BETWEEN {start} AND {end}
),
blocking_activities AS (
    SELECT oai3.plan_id
    FROM ossdb01db.oss_activity_instance oai3
    WHERE oai3.spec_ver_id = '88f0860f-e647-41cd-aaac-1930adea8a3c'
      AND oai3.state NOT IN ('In Progress')
      AND oai3.is_latest_version = 1
)
SELECT 
    ep.id AS projectid,
    ep.version,
    ipa.status AS activity_status,
    ep.status AS project_status,
    ipa.id AS activity_id,
    ep.name,
    ca.last_update_date,
    ipa.create_date
FROM eligible_projects ep
INNER JOIN completed_activities ca ON ep.plan_id = ca.plan_id
INNER JOIN in_progress_activities ipa ON ep.plan_id = ipa.plan_id
INNER JOIN blocking_activities ba ON ep.plan_id = ba.plan_id;
"""

# Alternative simpler approach - breaking into multiple queries
simple_base_sql = """
SELECT spoi.id AS projectid, spoi.version, oai.status AS activity_status, 
       spoi.status AS project_status, oai.id AS activity_id,
       spoi.name, oai2.last_update_date, oai.create_date
FROM ossdb01db.sc_project_order_instance spoi
INNER JOIN ossdb01db.oss_activity_instance oai ON spoi.plan_id = oai.plan_id
INNER JOIN ossdb01db.oss_activity_instance oai2 ON oai.plan_id = oai2.plan_id
INNER JOIN ossdb01db.oss_activity_instance oai3 ON oai.plan_id = oai3.plan_id
WHERE spoi.status NOT IN ('FCANCELLED', 'DCOMPLETED')
  AND spoi.name NOT LIKE '%MM_PROD_TEST%'
  AND spoi.name NOT LIKE '%MM_Prod_Test%'
  AND spoi.manager IS DISTINCT FROM 'ProductionSanity'
  AND spoi.is_latest_version = 1
  AND oai2.spec_ver_id = '91757a68-692f-4246-91e1-7e2280a659d8'
  AND oai2.state = 'Completed'
  AND oai2.is_latest_version = 1
  AND oai2.complete_date < CURRENT_DATE - INTERVAL '10 days'
  AND oai.spec_ver_id = '03acd7f1-557a-4727-ba2e-8d44f6245047'
  AND oai.state IN ('In Progress', 'Optional')
  AND oai.is_latest_version = 1
  AND oai3.spec_ver_id = '88f0860f-e647-41cd-aaac-1930adea8a3c'
  AND oai3.state NOT IN ('In Progress')
  AND oai3.is_latest_version = 1
  AND oai.part_id BETWEEN {start} AND {end};
"""

# Step 4: Function to execute queries with different strategies
def execute_staged_query(cursor, start, end):
    """Execute query using staged approach to reduce DB load"""
    try:
        # Stage 1: Get eligible projects (cached result can be reused)
        if not hasattr(execute_staged_query, 'eligible_projects'):
            logging.info("Stage 1: Fetching eligible projects (one-time operation)")
            cursor.execute(project_filter_sql)
            rows = cursor.fetchall()
            execute_staged_query.eligible_projects = {row[1]: row for row in rows}  # plan_id -> row
            logging.info(f"Stage 1 Complete: Found {len(execute_staged_query.eligible_projects)} eligible projects")
        else:
            logging.info(f"Stage 1: Using cached eligible projects ({len(execute_staged_query.eligible_projects)} projects)")
        
        # Stage 2: Get completed activities for current part_id range
        logging.info(f"Stage 2: Fetching completed activities for part_id {start}-{end}")
        completed_activities_sql = """
        SELECT DISTINCT oai2.plan_id, oai2.last_update_date, oai2.complete_date
        FROM ossdb01db.oss_activity_instance oai2
        WHERE oai2.spec_ver_id = '91757a68-692f-4246-91e1-7e2280a659d8'
          AND oai2.state = 'Completed'
          AND oai2.is_latest_version = 1
          AND oai2.complete_date < CURRENT_DATE - INTERVAL '10 days'
          AND oai2.plan_id IN (
              SELECT DISTINCT oai_inner.plan_id 
              FROM ossdb01db.oss_activity_instance oai_inner
              WHERE oai_inner.part_id BETWEEN %s AND %s
          );
        """
        
        cursor.execute(completed_activities_sql, (start, end))
        completed_activities = {row[0]: row for row in cursor.fetchall()}
        logging.info(f"Stage 2 Complete: Found {len(completed_activities)} completed activities for part_id {start}-{end}")
        
        if not completed_activities:
            logging.info(f"Stage 2: No completed activities found for part_id {start}-{end}, skipping remaining stages")
            return []
        
        # Stage 3: Get in-progress activities
        logging.info(f"Stage 3: Fetching in-progress activities for part_id {start}-{end}")
        in_progress_sql = """
        SELECT oai.plan_id, oai.id, oai.status, oai.create_date
        FROM ossdb01db.oss_activity_instance oai
        WHERE oai.spec_ver_id = '03acd7f1-557a-4727-ba2e-8d44f6245047'
          AND oai.state IN ('In Progress', 'Optional')
          AND oai.is_latest_version = 1
          AND oai.part_id BETWEEN %s AND %s
          AND oai.plan_id = ANY(%s);
        """
        
        plan_ids = list(completed_activities.keys())
        cursor.execute(in_progress_sql, (start, end, plan_ids))
        in_progress_activities = {row[0]: row for row in cursor.fetchall()}
        logging.info(f"Stage 3 Complete: Found {len(in_progress_activities)} in-progress activities for part_id {start}-{end}")
        
        if not in_progress_activities:
            logging.info(f"Stage 3: No in-progress activities found for part_id {start}-{end}, skipping remaining stages")
            return []
        
        # Stage 4: Check blocking activities
        logging.info(f"Stage 4: Checking blocking activities for part_id {start}-{end}")
        blocking_sql = """
        SELECT DISTINCT oai3.plan_id
        FROM ossdb01db.oss_activity_instance oai3
        WHERE oai3.spec_ver_id = '88f0860f-e647-41cd-aaac-1930adea8a3c'
          AND oai3.state NOT IN ('In Progress')
          AND oai3.is_latest_version = 1
          AND oai3.plan_id = ANY(%s);
        """
        
        plan_ids_filtered = list(in_progress_activities.keys())
        cursor.execute(blocking_sql, (plan_ids_filtered,))
        blocking_activities = {row[0] for row in cursor.fetchall()}
        logging.info(f"Stage 4 Complete: Found {len(blocking_activities)} plans with blocking activities for part_id {start}-{end}")
        
        # Stage 5: Combine results
        logging.info(f"Stage 5: Combining results for part_id {start}-{end}")
        final_results = []
        for plan_id in blocking_activities:
            if (plan_id in execute_staged_query.eligible_projects and 
                plan_id in completed_activities and 
                plan_id in in_progress_activities):
                
                proj = execute_staged_query.eligible_projects[plan_id]
                comp = completed_activities[plan_id]
                prog = in_progress_activities[plan_id]
                
                final_results.append((
                    proj[0],  # projectid
                    proj[2],  # version
                    prog[2],  # activity_status
                    proj[3],  # project_status
                    prog[1],  # activity_id
                    proj[4],  # name
                    comp[1],  # last_update_date
                    prog[3]   # create_date
                ))
        
        logging.info(f"Stage 5 Complete: Generated {len(final_results)} final records for part_id {start}-{end}")
        return final_results
        
    except Exception as e:
        logging.error(f"Error in staged query for part_id {start}-{end}: {e}")
        return []

def execute_simple_query(cursor, start, end):
    """Execute the simpler optimized query"""
    try:
        query = simple_base_sql.format(start=start, end=end)
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        logging.error(f"Error in simple query for part_id {start}-{end}: {e}")
        return []

def execute_cte_query(cursor, start, end):
    """Execute the CTE-based optimized query"""
    try:
        query = base_sql.format(start=start, end=end)
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        logging.error(f"Error in CTE query for part_id {start}-{end}: {e}")
        return []

# Step 4: Run queries and collect results
# Choose your preferred approach: 'staged', 'simple', or 'cte'
QUERY_APPROACH = 'simple'  # Change this to test different approaches: 'staged', 'simple', or 'cte'

logging.info(f"Starting PONR analysis using '{QUERY_APPROACH}' approach")
logging.info("=" * 50)

results = []
total_processed = 0
failed_batches = 0

for start, end in [(1, 10), (11, 20), (21, 30),(31, 40),(41, 50),(51, 60),(61, 70),(71, 80),(81, 90),(91, 99)]:
    try:
        logging.info(f"Processing batch: part_id BETWEEN {start} AND {end}")
        
        if QUERY_APPROACH == 'staged':
            batch_results = execute_staged_query(cursor, start, end)
        elif QUERY_APPROACH == 'simple':
            batch_results = execute_simple_query(cursor, start, end)
        else:  # cte
            batch_results = execute_cte_query(cursor, start, end)
        
        results.extend(batch_results)
        total_processed += len(batch_results)
        logging.info(f"✓ Batch {start}-{end}: Found {len(batch_results)} records")
        
    except Exception as e:
        failed_batches += 1
        logging.error(f"✗ Batch {start}-{end} FAILED: {e}")
        continue

logging.info("=" * 50)
logging.info(f"Query execution completed:")
logging.info(f"- Total records found: {total_processed}")
logging.info(f"- Failed batches: {failed_batches}")
logging.info(f"- Success rate: {((10-failed_batches)/10)*100:.1f}%")

cursor.close()
conn.close()
logging.info("Database connection closed")

# Step 5: Convert results to DataFrame and HTML
try:
    logging.info("Converting results to DataFrame and generating reports...")
    columns = ["projectid", "version", "activity_status", "project_status", "activity_id", "name", "last_update_date", "create_date"]
    df = pd.DataFrame(results, columns=columns)
    
    if df.empty:
        logging.warning("No data found! DataFrame is empty.")
        html_table = "<p><strong>No PONR issues found in the current analysis.</strong></p>"
    else:
        logging.info(f"Generated DataFrame with {len(df)} rows and {len(df.columns)} columns")
        
    output_file = "ponr_report.xlsx"
    df.to_excel(output_file, index=False)
    logging.info(f"Excel report saved: {output_file}")

    html_table = df.to_html(index=False, classes='styled-table')
    logging.info("HTML table generated successfully")
    
except Exception as e:
    logging.error(f"Error generating reports: {e}")
    html_table = f"<p><strong>Error generating report: {e}</strong></p>"

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
try:
    logging.info("Preparing to send email report...")
    em = EmailMgr()
    em.send_mail()
    logging.info("✓ Email sent successfully!")
except Exception as e:
    logging.error(f"✗ Failed to send email: {e}")

logging.info("=" * 50)
logging.info("PONR Analysis Script completed successfully!")
logging.info(f"Check log file: {log_file}")
logging.info("=" * 50)















