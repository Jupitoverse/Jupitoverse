import re
import os
import cx_Oracle
import datetime as dt
import pandas as pd
import xlrd
#from datetime import timedelta
#from EmailManager import EmailMgr
from array import *
import numpy as np
import smtplib
import os
import smtplib
import mimetypes
import datetime as dt
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from time import sleep
#em=EmailMgr()

print("started the Usage report for cycle")
cycle_month=int(input("Enter the cycle Month: "))
cylce_month=int(cycle_month)
cycle_code=int(input("Enter the cycle Code: "))
today_date=dt.datetime.strftime(dt.datetime.now(),"%Y%m%d")                #no need of timedelta
print(today_date)

Rebill_report_path="/CYCLE_USAGE_REPORT.csv"

#connectionStrABP = "CMMAPPC" + "/" + "cmm_4c0nn" + "@" + "10.105.2.51" + ":" + str(1521) + "/" + "CMMCM1"    #Prod
#connectionStrABPEP = "CMMEPC" + "/" + "cmm_4c0nn" + "@" + "10.105.2.51" + ":" + str(1521) + "/" + "CMMEP1"    #Prod EP
connectionStrUSG1 = "CMMUSG1C" + "/" + "cmm_4c0nn" + "@" + "10.105.2.51" + ":" + str(1521) + "/" + "CMMUSG1"  #Prod Usg1
#cursor=connectionStrABP.cursor()
conn=cx_Oracle.connect(connectionStrUSG1)

a=conn.cursor()
a.execute("""select b.l9_legal_name,a.customer_id,a.L9_NUM_CHANNELS,UOM,F_5,  quota, a.L9_UTILIZED_QUOTA , round(a.L9_REMAINING_QUOTA) L9_REMAINING_QUOTA from APE1_ACCUMULATORS a , customer@CMMAPPC.CMMCM1 b where CYCLE_INSTANCE=""" +str(cycle_month)+ """and ACCUM_TYPE_ID=124 and CYCLE_CODE=""" +str(cycle_code)+ """and a.customer_id = b.customer_id and  l9_utilized_quota >= QUOTA""")
usage1=a.fetchall()
df=pd.DataFrame(usage1,columns=['L9_LEGAL_NAME','CUSTOMER_ID','L9_NUM_CHANNELS','UOM','F_5','QUOTA','L9_UTILIZED_QUOTA','L9_REMAINING_QUOTA'])
df.to_csv("/CYCLE_USAGE_REPORT.csv",index=False)
a.close()

c=conn.cursor()
c.execute("""with usg_chg as ( select customer_id, sum(l3_charge_amount) usg_charge from ape1_Rated_Event where cycle_code=""" +str(cycle_code)+ """and cycle_instance=""" +str(cycle_month)+ """and source_id!=0 and l3_charge_Amount > 0 group by customer_id order by 2 desc ) select a.* , cpc.pym_channel_no, b.l9_legal_name from usg_chg a , customer@CMMAPPC.CMMCM1 b , csm_pay_channel@CMMAPPC.CMMCM1 cpc where a.customer_id =b.customer_id and a.customer_id = cpc.customer_id""")
usage1=c.fetchall()
df=pd.DataFrame(usage1,columns=['CUSTOMER_ID','USG_CHARGE','PYM_CHANNEL_NO','L9_LEGAL_NAME'])
df.to_csv("/CYCLE_USAGE_CHARGES_REPORT.csv",index=False)
c.close()





class EmailMgr:

        def __init__(self):
                pass

        def send_mail(self):
               # recipients = ['aniket.mahale@amdocs.com','manishw@amdocs.com','sandeep.singh@amdocs.com','sirish.katragadda@amdocs.com','mahesh.kollipara@amdocs.com','tushar.nikam@amdocs.com','Bryan_DeNinnis@cable.comcast.com','Patrick_Reilly@comcast.com','Katelyn_McNicholas@Comcast.com','DX_EDWF_BIE@comcast.com','NDW-BUSINESS_SERVICES_SPOC@comcast.com']
                recipients = ['porwalp@amdocs.com']
                #cc_recipients = ['GSSGMSCComcastMidMarketBackendScrumTeam@int.amdocs.com']
                cc_recipients = ['porwalp@amdocs.com']
#,'mahesh.kollipara@amdocs.com','manishw@amdocs.com','tushar.nikam@amdocs.com','sirish.katragadda@amdocs.com']
                FROM="AutomationFramework@amdocs.com;"
                MESSAGE = MIMEMultipart('alternative')
                MESSAGE['subject'] = "Rebill Report "+dt.datetime.strftime(dt.datetime.now(),"%Y/%m/%d")

                MESSAGE['To'] = ", ".join(recipients)
                MESSAGE['Cc'] = ", ".join(cc_recipients)
                MESSAGE['From'] = FROM
                MESSAGE.preamble = """
                Your mail reader does not support the report format.
                Please visit us <a href="http://www.mysite.com">online</a>!"""

                BODY=self.get_mail_content()
                HTML_BODY = MIMEText(BODY, 'html')
                MESSAGE.attach(HTML_BODY)
		attachments = "/tclocal/fs_users/tccm04/users/MM_BE_Automation/usage_reports/CYCLE_USAGE_REPORT.csv"
		attachments1 = "/tclocal/fs_users/tccm04/users/MM_BE_Automation/usage_reports/CYCLE_USAGE_CHARGES_REPORT.csv"

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

		ctype, encoding = mimetypes.guess_type(attachments1)
                if ctype is None or encoding is not None:
                        ctype = 'application/octet-stream'

                maintype, subtype = ctype.split('/', 1)
                fp = open(attachments, 'rb')
                part2 = MIMEBase(maintype, subtype)
                part2.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(part2)
                part2.add_header('Content-Disposition', 'attachment', filename=attachments1.split("/")[-1])
                MESSAGE.attach(part2)


		server = smtplib.SMTP('localhost')
                recipients.extend(cc_recipients)
                server.sendmail(FROM,recipients,MESSAGE.as_string())
                server.quit()
                sleep(3)
                print("Mail Sent successfully!")
				
	def get_mail_content(self):
		email_content = """
        	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        	<title>html title</title>
		<html>
                	<body> <p> Cycle Usage Reports Attached for cycle """+str(cycle_code)+""" and month """+str(cycle_month)+""" </p>                       
                	</body>
		</html>
		"""

		return email_content

em=EmailMgr()
em.send_mail()

