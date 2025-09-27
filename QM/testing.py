import smtplib
import pymysql
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Database connection details
DB_HOST = 'prod-db-host'
DB_USER = 'your-username'
DB_PASSWORD = 'your-password'
DB_NAME = 'your-database'

# Email details
SMTP_SERVER = 'smtp.your-email-provider.com'
SMTP_PORT = 587
EMAIL_USER = 'your-email@example.com'
EMAIL_PASSWORD = 'your-email-password'
RECIPIENT_EMAIL = 'recipient@example.com'

def fetch_data_from_db(query):
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("Connected to the database.")
        df = pd.read_sql(query, connection)
        return df
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

def send_email_with_report(report_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = 'Automated Report'

        body = 'Please find the attached report.'
        msg.attach(MIMEText(body, 'plain'))

        attachment = open(report_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename={report_path.split('/')[-1]}")
        msg.attach(part)
        attachment.close()

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USER, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    query = "SELECT * FROM your_table LIMIT 100;"  # Replace with your SQL query
    report_path = 'report.csv'

    # Fetch data and save to CSV
    df = fetch_data_from_db(query)
    if df is not None:
        df.to_csv(report_path, index=False)
        print(f"Report saved to {report_path}.")

        # Send email with the report
        send_email_with_report(report_path)

if __name__ == "__main__":
    RECIPIENT_EMAIL = 'abhi@jupitoverse.com'
    main()