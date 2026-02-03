import cx_Oracle
import psycopg2
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import mimetypes
import datetime as dt
from datetime import datetime
import logging
from time import sleep
import html
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmailMgr:
    def __init__(self, html_content=None, html_file_path=None):
        self.html_content = html_content
        self.html_file_path = html_file_path

    def send_mail(self):
        recipients = ['anishaji@amdocs.com','Abhishek.Bajpai@amdocs.com','abhisha3@amdocs.com','Nikhilesh.Srivastava@amdocs.com']
        cc_recipients = ['anishaji@amdocs.com','Nishant.Bhatia@amdocs.com','Mukul.Bhasin@amdocs.com','gssgmsccomcastmidmarketbackendscrumteam@amdocs']
        FROM = 'noreply@amdocs.com'

        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = "Rebill Data Report with OSO Inputs - " + dt.datetime.strftime(dt.datetime.now(), "%Y/%m/%d")
        MESSAGE['To'] = ", ".join(recipients)
        MESSAGE['Cc'] = ", ".join(cc_recipients)
        MESSAGE['From'] = FROM
        MESSAGE.preamble = """
        Your mail reader does not support the report format.
        Please visit us online for better viewing!"""

        BODY = self.get_mail_content()
        HTML_BODY = MIMEText(BODY, 'html')
        MESSAGE.attach(HTML_BODY)

        # Attach HTML file if path is provided
        if self.html_file_path:
            try:
                ctype, encoding = mimetypes.guess_type(self.html_file_path)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'

                maintype, subtype = ctype.split('/', 1)
                with open(self.html_file_path, 'rb') as fp:
                    part2 = MIMEBase(maintype, subtype)
                    part2.set_payload(fp.read())

                encoders.encode_base64(part2)
                part2.add_header('Content-Disposition', 'attachment',
                                 filename=os.path.basename(self.html_file_path))
                MESSAGE.attach(part2)
                logger.info(f"Attached file: {self.html_file_path}")
            except Exception as e:
                logger.error(f"Error attaching file: {e}")

        try:
            server = smtplib.SMTP('localhost')
            all_recipients = recipients + cc_recipients
            server.sendmail(FROM, all_recipients, MESSAGE.as_string())
            server.quit()
            sleep(3)
            logger.info("Mail sent successfully!")
            print("Mail Sent successfully!")
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            raise

    def get_mail_content(self):
        if self.html_content:
            # If HTML content is provided, use it directly
            return self.html_content
        else:
            # Default email content
            email_content = """
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>Rebill Data Report</title>
            <html>
                <body> 
                    <p>Dear Team,</p>
                    <p>Please find the Rebill Data Report with OSO Inputs attached.</p>
                    <p>This report contains data from temp_rebill_data_final table along with corresponding OSO activity information.</p>
                    <p>Best Regards,<br>Automated Reporting System</p>
                </body>
            </html>
            """
            return email_content

class RebillDataProcessor:
    def __init__(self):
        # Oracle connection details
        self.oracle_connection_str = "CMMAPPC" + "/" + "cmm_4c0nn" + "@" + "cmmprdscan2" + ":" + str(1521) + "/" + "CMMCM1"

        # PostgreSQL connection details
        self.postgres_config = {
            "database": "prodossdb",
            "user": "ossdb01db",
            "password": "Pr0d_ossdb01db",
            "host": "oso-pstgr-rd.orion.comcast.com",
            "port": "6432"
        }

    def clean_text(self, text):
        """Clean text by removing unwanted characters and formatting"""
        if text is None:
            return "N/A"

        # Convert to string if not already
        text = str(text)

        # Remove newlines, carriage returns, and extra whitespace
        text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

        # Remove multiple spaces
        while '  ' in text:
            text = text.replace('  ', ' ')

        # Strip leading/trailing whitespace
        text = text.strip()

        # If empty after cleaning, return N/A
        if not text:
            return "N/A"

        return text

    def connect_oracle(self):
        """Establish connection to Oracle database"""
        try:
            conn = cx_Oracle.connect(self.oracle_connection_str)
            logger.info("Successfully connected to Oracle database")
            return conn
        except Exception as e:
            logger.error(f"Error connecting to Oracle database: {e}")
            raise

    def connect_postgres(self):
        """Establish connection to PostgreSQL database"""
        try:
            conn = psycopg2.connect(**self.postgres_config)
            logger.info("Successfully connected to PostgreSQL database")
            return conn
        except Exception as e:
            logger.error(f"Error connecting to PostgreSQL database: {e}")
            raise

    def fetch_rebill_data(self):
        """Fetch all data from temp_rebill_data_final table"""
        oracle_conn = self.connect_oracle()
        try:
            query = """
            SELECT NO_OF_DAYS_DELAYED, CUSTOMER_ID, START_DATE, END_DATE, ISSUE_DATE,
                   SERVICE_ID, L9_SITE_ID, L9_SITE_NAME, CUSTOMER_NAME, APPLICATION,
                   BILLING_ACTIVITIES, BILLING_DATE, ABP_COMMENTS
            FROM temp_rebill_data_final
            """
            df = pd.read_sql(query, oracle_conn)
            logger.info(f"Fetched {len(df)} records from temp_rebill_data_final")
            return df
        except Exception as e:
            logger.error(f"Error fetching data from Oracle: {e}")
            raise
        finally:
            oracle_conn.close()

    def get_task_owner_name(self, activity_id):
        """Get task owner name for a given activity ID"""
        postgres_conn = self.connect_postgres()
        try:
            query = """
            select text_ as task_owner_name from act_ru_variable where task_id_ in
            (select task_id_ from act_ru_variable arv where  
            text_ = %s and name_= 'activityId') and
            name_ in ('task_owner_name')
            """
            cursor = postgres_conn.cursor()
            cursor.execute(query, (str(activity_id),))
            result = cursor.fetchone()
            return self.clean_text(result[0]) if result else "N/A"
        except Exception as e:
            logger.error(f"Error fetching task owner name for activity {activity_id}: {e}")
            return "Error"
        finally:
            postgres_conn.close()

    def get_work_queue(self, activity_id):
        """Get work queue for a given activity ID"""
        postgres_conn = self.connect_postgres()
        try:
            query = """
            select text_ as work_queue from act_ru_variable where task_id_ in
            (select task_id_ from act_ru_variable arv where text_ = %s and name_= 'activityId') and 
            name_ in ('WorkQueue')
            """
            cursor = postgres_conn.cursor()
            cursor.execute(query, (str(activity_id),))
            result = cursor.fetchone()
            return self.clean_text(result[0]) if result else "N/A"
        except Exception as e:
            logger.error(f"Error fetching work queue for activity {activity_id}: {e}")
            return "Error"
        finally:
            postgres_conn.close()

    def query_postgres_for_service(self, prim_resource_val, billing_date, issue_date):
        """Query PostgreSQL for specific service ID, billing date, and issue date"""
        postgres_conn = self.connect_postgres()
        try:
            # Format issue_date to have 23:59:59 timestamp
            if isinstance(issue_date, str):
                # If it's already a string, extract just the date part and add 23:59:59
                issue_date_formatted = issue_date.split()[0] + " 23:59:59"
            elif hasattr(issue_date, 'strftime'):
                # If it's a datetime object, format it properly
                issue_date_formatted = issue_date.strftime('%Y-%m-%d') + " 23:59:59"
            else:
                # If it's some other type, convert to string and try to extract date
                issue_date_str = str(issue_date)
                if ' ' in issue_date_str:
                    issue_date_formatted = issue_date_str.split()[0] + " 23:59:59"
                else:
                    issue_date_formatted = issue_date_str + " 23:59:59"

            # Format billing_date properly as well
            if isinstance(billing_date, str):
                billing_date_formatted = billing_date.split()[0] if ' ' in billing_date else billing_date
            elif hasattr(billing_date, 'strftime'):
                billing_date_formatted = billing_date.strftime('%Y-%m-%d')
            else:
                billing_date_formatted = str(billing_date).split()[0] if ' ' in str(billing_date) else str(billing_date)

            logger.info(f"Querying PostgreSQL with service_id: {prim_resource_val}, billing_date: {billing_date_formatted}, issue_date: {issue_date_formatted}")

            query = """
            with prod_proj as (
                select distinct dpv2.project_id as pv_prj_id
                from dd_product_version dpv
                left join dd_sol_leg_site_2_prod_version dslspv on dpv.id = dslspv.prod_ver_id
                left join dd_sol_leg_site_2_prod_version dslspv2 on dslspv.solution_leg_site_id = dslspv2.solution_leg_site_id
                left join dd_product_version dpv2 on dslspv2.prod_ver_id = dpv2.id
                where dpv.service_id = %s
            )
            select
                distinct ord.entity_name, spoi."type",
                oai.actual_start_date, oai.actual_end_date, 
                oai.actual_end_date - oai.actual_start_date as time_elapsed, 
                oai.implementation_type, oai.id
            from prod_proj
            left join sc_project_order_instance spoi on pv_prj_id = spoi.id
            left join oss_activity_instance oai on spoi.plan_id = oai.plan_id and oai.is_latest_version = 1
            left join ossdb01ref.oss_ref_attribute ora on oai.spec_ver_id = ora.attribute_value
            left join ossdb01ref.oss_ref_data ord on ora.entity_id = ord.entity_id
            where oai.actual_start_date > %s 
            and actual_end_date <= %s 
            and actual_end_date > actual_start_date + interval '20 minutes'
            order by oai.actual_start_date
            """

            cursor = postgres_conn.cursor()
            cursor.execute(query, (prim_resource_val, billing_date_formatted, issue_date_formatted))
            results = cursor.fetchall()

            # Process results and create tabular format
            table_rows = []
            for row in results:
                entity_name, spoi_type, actual_start_date, actual_end_date, time_elapsed, implementation_type, activity_id = row

                task_owner_name = "N/A"
                work_queue = "N/A"

                # If implementation_type is 'Manual', fetch additional details
                if implementation_type == 'Manual':
                    task_owner_name = self.get_task_owner_name(activity_id)
                    work_queue = self.get_work_queue(activity_id)

                table_rows.append({
                    'task_type': self.clean_text(implementation_type),
                    'task_name': self.clean_text(entity_name),
                    'flow': self.clean_text(spoi_type),
                    'start_date': str(actual_start_date) if actual_start_date else "N/A",
                    'end_date': str(actual_end_date) if actual_end_date else "N/A",
                    'time_elapsed': str(time_elapsed) if time_elapsed else "N/A",
                    'task_owner_name': task_owner_name,
                    'work_queue': work_queue
                })

            return table_rows

        except Exception as e:
            logger.error(f"Error querying PostgreSQL for service {prim_resource_val}: {e}")
            return [{'error': f"Error querying OSO data: {str(e)}"}]
        finally:
            postgres_conn.close()

    def format_oso_data_as_table(self, oso_data_list):
        """Format OSO data as HTML table"""
        if not oso_data_list:
            return "No OSO data available"

        # Check if there's an error
        if len(oso_data_list) == 1 and 'error' in oso_data_list[0]:
            return oso_data_list[0]['error']

        html_table = """
        <table border='1' style='border-collapse: collapse; font-size: 10px; width: 100%; margin: 5px 0;'>
            <tr style='background-color: #f2f2f2;'>
                <th style='padding: 4px; text-align: left;'>Task Type</th>
                <th style='padding: 4px; text-align: left;'>Task Name</th>
                <th style='padding: 4px; text-align: left;'>Flow</th>
                <th style='padding: 4px; text-align: left;'>Start Date</th>
                <th style='padding: 4px; text-align: left;'>End Date</th>
                <th style='padding: 4px; text-align: left;'>Time Elapsed</th>
                <th style='padding: 4px; text-align: left;'>Task Owner</th>
                <th style='padding: 4px; text-align: left;'>Work Queue</th>
            </tr>
        """

        for row in oso_data_list:
            html_table += f"""
            <tr>
                <td style='padding: 4px; word-wrap: break-word;'>{html.escape(row.get('task_type', 'N/A'))}</td>
                <td style='padding: 4px; word-wrap: break-word;'>{html.escape(row.get('task_name', 'N/A'))}</td>
                <td style='padding: 4px; word-wrap: break-word;'>{html.escape(row.get('flow', 'N/A'))}</td>
                <td style='padding: 4px; word-wrap: break-word;'>{html.escape(row.get('start_date', 'N/A'))}</td>
                <td style='padding: 4px; word-wrap: break-word;'>{html.escape(row.get('end_date', 'N/A'))}</td>
                <td style='padding: 4px; word-wrap: break-word;'>{html.escape(row.get('time_elapsed', 'N/A'))}</td>
                <td style='padding: 4px; word-wrap: break-word;'>{html.escape(row.get('task_owner_name', 'N/A'))}</td>
                <td style='padding: 4px; word-wrap: break-word;'>{html.escape(row.get('work_queue', 'N/A'))}</td>
            </tr>
            """

        html_table += "</table>"
        return html_table

    def process_rebill_data(self):
        """Main processing function"""
        # Fetch rebill data
        df = self.fetch_rebill_data()

        # Clean all text columns in the dataframe
        text_columns = ['NO_OF_DAYS_DELAYED', 'SERVICE_ID', 'L9_SITE_ID', 'L9_SITE_NAME',
                        'CUSTOMER_NAME', 'APPLICATION', 'BILLING_ACTIVITIES', 'ABP_COMMENTS']

        for col in text_columns:
            if col in df.columns:
                df[col] = df[col].apply(self.clean_text)

        # Add OSO_Inputs column
        df['OSO_INPUTS'] = ""

        # Process each row
        for index, row in df.iterrows():
            logger.info(f"Processing row {index + 1} of {len(df)}")

            service_ids = str(row['SERVICE_ID']).split(',') if pd.notna(row['SERVICE_ID']) else []
            billing_date = row['BILLING_DATE']
            issue_date = row['ISSUE_DATE']

            all_oso_data = []

            # Process each service ID
            for service_id in service_ids:
                prim_resource_val = service_id.strip()
                if prim_resource_val:
                    logger.info(f"Processing service ID: {prim_resource_val}")
                    oso_data = self.query_postgres_for_service(prim_resource_val, billing_date, issue_date)
                    if oso_data:
                        # Add service ID header with better styling
                        service_header = f"<div style='margin: 10px 0; font-weight: bold; color: #333;'>Service ID: {html.escape(prim_resource_val)}</div>"
                        service_table = self.format_oso_data_as_table(oso_data)
                        all_oso_data.append(service_header + service_table)

            # Update the dataframe with OSO inputs
            df.at[index, 'OSO_INPUTS'] = "".join(all_oso_data) if all_oso_data else "No OSO data available"

        return df

    def create_html_table(self, df):
        """Create HTML table from dataframe"""
        html_style = """
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            table.main-table {
                border-collapse: collapse;
                width: 100%;
                font-family: Arial, sans-serif;
                font-size: 11px;
            }
            table.main-table th, table.main-table td {
                border: 1px solid #ddd;
                padding: 6px;
                text-align: left;
                vertical-align: top;
                word-wrap: break-word;
            }
            table.main-table th {
                background-color: #f2f2f2;
                font-weight: bold;
                position: sticky;
                top: 0;
            }
            table.main-table tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            .oso-inputs {
                max-width: 500px;
                word-wrap: break-word;
                overflow-wrap: break-word;
            }
            h2 {
                color: #333;
                border-bottom: 2px solid #ddd;
                padding-bottom: 10px;
            }
        </style>
        """

        # Clean the dataframe before converting to HTML
        df_clean = df.copy()
        for col in df_clean.columns:
            if df_clean[col].dtype == 'object':
                df_clean[col] = df_clean[col].apply(lambda x: self.clean_text(x) if pd.notna(x) else "N/A")

        # Convert dataframe to HTML with proper escaping
        html_table = df_clean.to_html(escape=False, index=False, classes='main-table',
                                      table_id='rebill-data-table')

        # Complete HTML document
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Rebill Data Report</title>
            <meta charset="UTF-8">
            {html_style}
        </head>
        <body>
            <h2>Rebill Data Report with OSO Inputs</h2>
            <p><strong>Generated on:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Total Records:</strong> {len(df)}</p>
            {html_table}
        </body>
        </html>
        """

        return html_content

    def run(self):
        """Main execution function"""
        try:
            logger.info("Starting rebill data processing...")

            # Process the data
            processed_df = self.process_rebill_data()

            # Create HTML table
            html_content = self.create_html_table(processed_df)

            # Save HTML to file (optional)
            html_filename = f"rebill_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.info(f"HTML report saved to file: {html_filename}")

            # Send email using EmailMgr class
            email_manager = EmailMgr(html_content=html_content, html_file_path=html_filename)
            email_manager.send_mail()

            logger.info("Rebill data processing completed successfully!")

        except Exception as e:
            logger.error(f"Error in main execution: {e}")
            raise

if __name__ == "__main__":
    # Create and run the processor
    processor = RebillDataProcessor()
    processor.run()
