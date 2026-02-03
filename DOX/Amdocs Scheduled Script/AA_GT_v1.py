#!/usr/bin/env python3
"""
#############################################################################
# NAME        : All Pending GT Report
# AUTHOR      : Abhishek Agrahari
# DATE        : 12/11/2024
# DESCRIPTION : Check ALL User Pending Tasks (not just billing-impacting) and generate report
# NOTE        : Extended version with comprehensive spec_ver_id list
#############################################################################
"""

import datetime as dt
import logging
import smtplib
import mimetypes
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import psycopg2
import os
import sys
import traceback
from pathlib import Path


# ============================================================================
# CONFIGURATION
# ============================================================================

# ============================================================================
# TOGGLE FOR TESTING
# ============================================================================
# Set TEST_MODE = True to send emails to test recipient only
# Set TEST_MODE = False to send emails to production recipients
TEST_MODE = True  # ← CHANGE THIS TO False FOR PRODUCTION

# ============================================================================

DB_CONFIG = {
    'database': 'prodossdb',
    'user': 'ossdb01uams',
    'password': 'Pr0d_ossdb01uams',
    'host': 'oso-pstgr-rd.orion.comcast.com',
    'port': '6432'
}

# Production Recipients
PRODUCTION_RECIPIENTS = [
    'abhisha3@amdocs.com',
    'prateek.jain5@amdocs.com',
    'Nishant.Bhatia@amdocs.com',
    'Enna.Arora@amdocs.com',
    'RAJIVKUM@amdocs.com',
    'mukul.bhasin@amdocs.com',
    'Natasha.Deshpande@amdocs.com',
    'Alon.Kugel@Amdocs.com',
    'Shreyas.Kulkarni@amdocs.com'
    
]

# Test Recipient
TEST_RECIPIENT = ['abhisha3@amdocs.com']

# Email Configuration - Recipients are determined by TEST_MODE
EMAIL_CONFIG = {
    'recipients': TEST_RECIPIENT if TEST_MODE else PRODUCTION_RECIPIENTS,
    'cc_recipients': [],  # Optional CC recipients
    'from': 'noreplyreports@amdocs.com',
    'error_recipients': ['abhisha3@amdocs.com']
}

# Frequency configuration: Script runs daily (every 1 day)
EXECUTION_FREQUENCY = 1

# Directory for logs and output files
LOGS_DIR = Path("LOGS")
LOGS_DIR.mkdir(exist_ok=True)

# Timestamp for file naming
TIMESTAMP = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = LOGS_DIR / f"All_Pending_GT_Report_{TIMESTAMP}.log"
HTML_FILE = f"All_Pending_GT_Report_{TIMESTAMP}.html"
EXCEL_FILE = f"All_Pending_GT_Report_{TIMESTAMP}.xlsx"


# ============================================================================
# LOGGING SETUP
# ============================================================================
def setup_logging():
    """
    Configure logging to write to both console and file
    Includes automatic log rotation and cleanup of old logs
    """
    # Create logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    logger.handlers = []
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # File handler
    file_handler = logging.FileHandler(LOG_FILE, mode='w')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    logging.info("=" * 80)
    logging.info("Script: Check User Pending Task Impacting Billing")
    logging.info(f"Start Time: {dt.datetime.now()}")
    logging.info("=" * 80)


def cleanup_old_logs(days_to_keep=30):
    """
    Clean up old log, HTML, and Excel files older than specified days
    
    Args:
        days_to_keep (int): Number of days to retain files
    """
    try:
        current_time = dt.datetime.now()
        cutoff_time = current_time - dt.timedelta(days=days_to_keep)
        
        deleted_count = 0
        
        # Clean up log files
        for log_file in LOGS_DIR.glob("checkUserPendingTask_*.log"):
            file_time = dt.datetime.fromtimestamp(log_file.stat().st_mtime)
            if file_time < cutoff_time:
                log_file.unlink()
                deleted_count += 1
        
        # Clean up HTML files
        for html_file in LOGS_DIR.glob("checkUserPendingTask_*.html"):
            file_time = dt.datetime.fromtimestamp(html_file.stat().st_mtime)
            if file_time < cutoff_time:
                html_file.unlink()
                deleted_count += 1
        
        # Clean up Excel files
        for excel_file in LOGS_DIR.glob("checkUserPendingTask_*.xlsx"):
            file_time = dt.datetime.fromtimestamp(excel_file.stat().st_mtime)
            if file_time < cutoff_time:
                excel_file.unlink()
                deleted_count += 1
        
        if deleted_count > 0:
            logging.info(f"Cleaned up {deleted_count} old files (logs, HTML, Excel)")
    except Exception as e:
        logging.warning(f"Error during file cleanup: {e}")


# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================
def get_db_connection():
    """
    Establish and return PostgreSQL database connection
    
    Returns:
        psycopg2.connection: Database connection object
    
    Raises:
        SystemExit: If connection fails
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logging.info("Database connection established successfully")
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        send_error_notification(f"Database connection failed: {e}")
        sys.exit(1)


def check_execution_day():
    """
    Check if script should execute based on day of month
    Script runs every Nth day based on EXECUTION_FREQUENCY
    
    Returns:
        bool: True if script should execute, False otherwise
    """
    current_day = dt.datetime.now().day
    should_execute = (current_day % EXECUTION_FREQUENCY == 0)
    
    if should_execute:
        logging.info(f"Execution check passed: Day {current_day} is a multiple of {EXECUTION_FREQUENCY}")
    else:
        logging.info(f"Execution skipped: Day {current_day} is not a multiple of {EXECUTION_FREQUENCY}")
    
    return should_execute


def fetch_pending_tasks_batch(cursor, part_id_batch):
    """
    Fetch ALL pending user tasks with comprehensive spec_ver_id list
    Batches part_id values in groups of 5 to avoid timeout
    
    Args:
        cursor: Database cursor
        part_id_batch (list): List of part_id values (max 5)
    
    Returns:
        list: Query results as list of tuples
    """
    # Query with comprehensive spec_ver_id list (1000+ IDs, filtered to exclude _WA)
    part_id_list = ','.join(map(str, part_id_batch))
    
    # Comprehensive spec_ver_id list - ALL tasks (not just billing-impacting)
    # NOTE: Automatically filters out entries ending with _WA
    spec_ver_ids = '''0035e3b6-e6ab-473e-b921-7b6ed75c7b8f,005d4fb9-10c4-4098-9b1b-d3128efee28c,0083576b-8af2-43bf-a923-4ba0b7de1394,009e94e8-fa93-4856-a481-940b3ee961a0,018b71e7-a684-4dc3-9d81-c18fbfa58d1e,01b2e46b-f54c-4a46-b02b-90ebc242411e,01dd56c2-ec11-4c00-bcd5-94946af9e67d,01fca60d-730a-4fa5-a028-88b9a3e78dc5,0268657c-2b84-45db-a5cb-f58a5c529b25,02957722-01b8-4589-81b7-a56d704a8111,02caf2ec-b4ec-4128-b17b-b9bcce67f5ee,03cacabc-6fd1-4d11-b230-2a9bbb2f589a,054ba367-056d-42e8-8f2c-028015689f08,063ce5b7-6928-465b-92b1-1a0abeee80e5,06580f52-8753-44a2-ba84-d4d5b0e3a0f5,06e20c4a-a1b8-4208-960b-9ac05e5a11b9,071bd8f5-b2f2-4d70-a6f4-fdbbc20e5ff4,07ffe7fe-4029-443d-aba9-cfbe51a7b3db,0886cced-91e4-41be-af77-2a4f2950df16,08c210c6-669c-46a9-b452-6ef789ff8fa3,096a8063-8189-4e21-a5a3-f76c3c019c90,09dc7307-cd32-4131-8e61-cf548829926f,0a23f17e-5b04-40e0-bff6-4b54ef7c9ad9,0ac578ae-f93d-409b-bc24-c0ed5587f357,0ac6c448-6770-44c9-a793-414c0dfb8364,0b7c4d7c-6fc5-448c-bc98-1b3eed171206,0cb0c9f9-51e6-4731-8c01-4c2cffe92793,0cd01088-6008-4246-962c-350c583e994d,0cf1692d-4063-4b71-8456-70c02a467dae,0d3332c6-d133-4e00-b631-50ce6c35364c,0d5f4b56-1c9c-4bee-8e43-c58ff2778788,0d6d61ca-36aa-4cfe-8664-a4070dc0c9c5,0ddc2099-cd04-4c66-99a9-18d65b727a2b,0df41b94-02b8-4db8-a358-d850207de1bb,0df41b94-02b8-4db8-a358-d850207de1bb_WA,0e63797f-7e5e-4071-be2e-00437873fefe,0fe8ed5b-c6eb-4a65-ad2f-593555e85211,101f5ad1-0c82-4294-b5b2-bb69737ec705,107ddedd-816d-4e41-8a83-45facf03ec98,12184f75-50df-47d7-b8c6-81078e165285,1286d210-0b0f-48e0-bdf6-8c2d5a6d331f,12d1fbf5-3878-4f89-91bc-deb221d89610,13031ea5-0a9d-4a3f-a152-3b7d707ebbd6,13675be7-2cbe-46a7-894f-0dfff16492bd,13e755c9-0bca-467b-89a6-3f3987d2b9ae,144252de-f128-4bfd-8be3-51286883f178,1478e653-25d9-4e7c-ada1-5dc6cef7d163,155854c2-0d92-4e05-a612-166428aa7a5b,15d1d902-5ced-4d55-9ca3-bd464e9191c4,16229d76-b0e0-4867-846f-2efe4244be24,1695cdc2-ea7d-43ee-8426-a90e7c3a5618,16e3ca88-d0c7-4154-84bb-b405ae4e2a3e,170eb42c-4686-47e0-a1f9-8a67ad0ca94e,1731b835-4fee-4b4c-95c4-030c488c4128,1759190e-67d1-4338-8044-c8254ef5f24c,17792b0b-d224-4f8a-8794-2e60897011c2,186bc9bd-d745-4620-8005-95cea28ca8ab,187c7c78-d4e8-4145-8732-3705eec36388,19396fde-5018-4a1f-b0d3-235e59bae12b,196e55a5-532c-45b8-b53a-3fd2c8b50caa,19dee07b-742b-4b36-ba35-192b6b7cbbc4,1a6919de-d821-46be-8626-5fe04492a91d,1b02ba1a-54b9-43d7-b0af-0fca03bed003,1b1fba1a-0e4b-4c4c-9059-0c01b8b7e41d,1b1fba1a-0e4b-4c4c-9059-0c01b8b7e41d_WA,1bbe1c34-c80d-4768-88f0-0b9f7389c74d,1c339acf-07a6-4f14-8acf-a270f955b23a,1c37eeaa-0f70-47cc-92a5-42c50facf71f,1c8978e3-a0b5-46a2-8e1f-b7ed77a703ff,1cb09989-2e4d-474c-bbc2-50db815f4ff2,1d210db4-13c5-4ced-af22-55d0686e6e7b,1e1f81de-aea5-4f1c-a621-8daed5a11842,1e1f81de-aea5-4f1c-a621-8daed5a11842_WA,1e228771-78cc-4689-9c49-9dea5fea24b7,1e28cc7c-f380-406d-b974-f5d3e29f87e1,1e4f5d6c-7f3f-48e6-9b7d-aaf71ddd7872,1e5db2d7-b607-4b5d-8498-2544ea730e97,1e704e13-4396-4208-9df8-457673f8740c,1ef8f4bb-d3c7-421d-bcc6-b7c8efe9aee6,1f0e4e96-7529-4fdb-bc48-b860f2ba7e07,1f3f46fc-a217-4258-8c7f-db14e1516de5,1f67507b-e741-48e4-8557-c2eb776150c1,203fa4c5-f77c-48f1-9757-0996e23e3673,2045ecd1-49d2-4f4f-ba28-83774edf815d,20af588c-5e7d-490b-bfbc-853212d77606,20e0f82c-da11-47e5-a484-bd98a69cd873,210df3f7-8526-4ae9-9396-2394118a0222,21109c57-d48f-46f2-8a78-3c6f52664a16,219589a6-c05e-4af6-948b-40ac438da2dc,21ab110f-7e5a-4c28-904d-3622516102ff,21ae9581-dd74-491c-82d6-d74a01dd562b,2274a5bd-39d3-47b3-9cea-d55a475cdd5a,22766611-cf7a-4293-8573-942b97117d85,22959b29-be6c-403e-aad1-bed31a55055c,22c8a057-9299-4f06-8882-122e09584ec8,231d2d48-8671-475c-a33e-448a5e0934ee,234487e7-7dfa-4f09-a7db-6de805f7ff23,24cbb36a-3878-4cf8-b714-3e1fd845c305,252e00fc-8f52-4e54-abcb-960a036059b1,255ade9e-2260-4988-89d4-f897dcc1b010,25f2d0ac-8a79-4bb3-8c5b-0793ca8e0bda,260dd0eb-224d-45e1-b2a3-be8b68e8cd73,2636b956-9fdd-482f-a37b-79dc19f59ae7,267a4ef0-f713-4bc8-b127-89e83930865d,274d72ee-1457-4b63-beb3-55b244ad7287,2790ad5c-5095-4c61-82df-1ff36d8f1f94,27c14c12-63a3-4183-a08c-ca1097df21c2,2852bfa9-e5d4-425a-823f-4200312b8786,28ae046a-eaf4-42b5-9b72-db3e888eba72,28eaa365-6b99-4081-af9c-f2636e982bdf,2943e080-10a7-4b28-b811-bc076d065bd6,29fee761-f60a-48ba-b813-835ae017a4cb,2a3aa7ba-193b-401b-a6de-128eff01cfc2,2a9fc03d-d92c-4014-9e77-e8bff27e6c7f,2aa157cc-2063-4a6e-9dbc-1062a8fdfb6a,2aeb0ede-6a8e-41e8-89a3-eabb64cf6ade,2aff568f-5bbf-4f9c-bcc4-8ee6409d371a,2b20700f-04b5-43f2-a87f-f3a5016e2a18,2b389a35-131a-4534-bbec-604be6dbbb23,2b3e9b07-e18d-4254-be1a-b12b474cae85,2b78216d-7e41-45d5-91f4-844bd77328e4,2be797e2-7ffc-45b7-ae84-d834380b92ad,2c803afd-3a25-41f3-b3c6-f7ecda8ef88d,2cab1de8-115d-4acf-b4ad-4dd7404b1944,2ce8f963-2ab0-4ab2-8144-4e7d7be43eab,2d10ace8-a193-4652-abe4-7a93191022c6,2d2f2cff-d4d0-4691-afd3-5e0313b4156e,2d81e505-8700-4a61-b3e4-7d52c91133d9,2da0defc-b2f7-4b8d-ad46-b5f09927acc4,2da4d9d8-2b59-4421-ad3b-d90f575caef8,2da54371-c9fb-4506-b47a-3e253685be54,2e6bd600-0fd8-49bf-a86e-00ae96f68331,2f34b557-49e6-4c1f-a5a7-63a53d00b03e,2f3ef698-f46f-459b-b4f4-a1ce2748838d,2f809619-7bec-4d67-a4ec-280c908b3cf3,3098d92c-26a5-4acc-9cc6-9bb9ba2a0b6d,309af31a-44c5-46d3-93a9-beb207cb085a,30cd9503-5334-4d3a-b66b-d9fa1f53b975,30d925f5-1c93-4ede-8b97-ff6cc266512d,311bcebb-7c67-405b-a265-a337e98c9c9a,31364921-58f8-4317-b3d7-2159740a14f5,31398d51-f376-4512-ada8-5f90c8b456a7,316da62e-c89b-444a-881a-d74bf6b28fb5,31e8b1d3-783e-4b75-8ff4-f74de0bb60ff,32420aa9-79c4-4973-b2a5-7fed24eb72a1,3252b045-3d1e-4c71-9980-cc51d25a6f05,32ce607c-fe07-48d8-a7d5-8f93a8341b42,3350e490-04f5-4636-94b9-d55b361deb5b,33ebad91-c1d1-481e-b214-9b19e82170b2,34d9e0f1-5443-4aef-9331-51e53d99b8ad,34ed6d8a-1f8f-4575-9965-816c1c28a152,34efdd9a-c620-4ca6-9234-be2e6af48b7e,3592ba2b-6ca6-481e-acf6-4fa1ed4e6a68,359c5dbb-d767-4103-b4ad-86c67399b322,36ee2b1a-adf6-4134-bc97-f55c21f9a987,3757d58a-c4fc-4910-ae34-ef05f39e80df,3830c205-ddc1-44b5-b6e7-c3375be96c13,396f72ca-c033-4b37-b2cf-565e719c7650,39d46428-83d4-4c9b-95be-9aef6943d357,39ec4961-c511-4f67-99d8-baf70ecedd06,3a8f7182-b8e9-425a-a330-3635459c1ce9,3b0b8600-3c74-4a4c-b24d-61c5edb78fa8,3c7a4a9f-63f0-49a8-95aa-4e76e83f7ad6,3cd06e1d-074b-40ad-b34f-faa67230e6ea,3cd27fb4-1b37-421d-98e3-adff3d5bde9f,3d157dc7-aef5-4512-9d98-7162ee087f58,3dd69ada-08ae-409a-af69-f25fae7bba94,3dde5be9-030e-49bb-98ea-dbb5519d9204,3df77180-60b1-4c24-91f5-6fa5077099fa,3dfe66aa-e4b5-4eea-848a-52ace3bdb847,3e27fc61-3fe1-4ede-938b-e4b76af5478f,3e8f9006-1c2b-4bdf-82cf-28eefe54dbc3,3e9a0abb-7ec2-4a70-9722-41e91feff5c0,3ec7ac3c-eb95-418a-87c6-e730c316014b,3f62c5b8-937e-4135-9351-e3ce36df441e,3fc5ab96-cd7f-4a21-ba4d-d4255ba90c4e,3ff3fcdd-8cde-4f04-bf23-5da707543353,40dfdfd6-996d-4657-8b93-475b9b5ab928,410e8485-cb0b-4a5b-8957-f24bf2ad352e,4176d8d1-29c8-4cb4-9934-66c28b33b9ac,41b4f52b-83f1-4ab9-afdc-75dc532a1314,42c4653a-8992-4991-83d6-58836a983c33,42d4e0fd-c799-438b-9c0c-112285ec3540,42eba1bc-50d8-429e-94a9-7c1af101580a,4341c59a-1941-4956-9c77-90755b38b02b,43589296-c74e-4050-88b1-847be0a9dc74,438aefdc-51ee-45f7-ac83-cc6a30ef6d8f,43950afe-4817-434d-bca6-8dd53af697cc,43bbeaef-307c-444f-82cf-a68d16b96c89,43c16ffe-70ae-448c-acb4-f0362b6dbb65,44f8d595-3c8d-4e33-91d4-def5e90d472e,44fbafe3-af4b-483f-9dd8-bc4ae70a6e48,456736b1-b962-4b89-8cd6-3ddb4fff04fa,4572d780-e2a3-47fd-9e8a-caf17ac5cfc9,45a8a07f-fdd1-4487-9ee0-eea510cb7c11,45ce11e2-9527-4c66-ba78-c727ec77c326,46b8dac2-d30d-4a52-93a0-92c949504785,46e594d7-d007-4a72-acf2-413bc37e8431,46e8d772-399d-4e7c-8573-f9d4f0657ef7,473d3cd7-614e-4432-bb0f-ccc98805038c,474dd642-af55-4a48-be51-443659bee22a,47b30e7d-5377-48ce-bd70-3d46aa732cb3,47e07b7c-26cc-4c15-855d-e0d4f657577c,47f1c6c8-faf2-4fc4-ba68-c01617c7af61,48124a54-6d59-4765-a148-1abf2c3c412e,4836fcb5-e131-450c-abca-bbdc9af883c5,4885d03d-586b-4e92-ae6a-32cf339e86dd,48a9f32a-baf8-4676-b5ea-4eeb67b853f2,48dd21d7-fe67-4b64-ad47-93963f6f9cde,491a83aa-3ce5-49b5-9fe5-91ecb5e4d420,49875d74-963a-4c16-8bff-2b17c31098d5,4a8356ff-6d73-4d73-8cb5-5fc44eed9e20,4a8c6b4e-2bd6-405c-b27c-d56d04b2a091,4aa477c1-6bb4-482e-9d14-45c19ba1a2fd,4abca914-affa-4c08-8f23-389bea4632ad,4bb4f768-838b-4eb2-9a53-7402494f13e1,4bfe8075-2129-41b6-9caf-2b00764f8e21,4c25ecdb-f50e-4759-b5cb-5e4347b28a55,4cc477fd-c91a-475d-952d-57c4e4db5331,4cc7c4cf-4fe8-4882-8c0d-459c0b0d708a,4d193231-6261-407d-ae19-be6ded807be7,4d582cac-812a-418b-802f-3fd79cab344b,4d61e6df-a7ab-4fcf-86bd-abce7b548272,4d7a7e94-ab1e-4da0-b11a-c49bada2a36f,4ddf0cef-6b65-49c2-9b52-1123a4b6ec81,4e76af33-fe36-45c4-bbc5-7877dfe1c5f7,4eaeb6bb-62ea-495a-8ef6-f625a88c2716,4f2c2175-7a49-4933-83ef-c31e3b95d4fd,4f57c93b-5d6b-4eba-aa7d-e59f7678e22f,4f69df2f-f867-44d9-af6f-2e5e52464683,4f80f882-7e64-43d2-b808-25621611c414,503fca23-de46-4e3e-bc94-a96d40782540,505784c5-2644-4c40-b1cb-b40dfaad8e9c,509f6f1c-97d8-4be5-9fe3-f22b617e3fd5,51a6ca49-6e52-483d-8964-4a29a9069dc0,51c25230-d06c-42e3-a2c9-235b22390446,527399db-2f34-41ff-9f46-2370c9eb44c9,527d8c02-c0b8-4232-b7ce-d3d30dc32b5f,52adb399-8dad-4383-8abf-f817632844ba,52e06554-3c2a-4f90-adc7-22c1aaab3a13,52e7474a-3282-48d6-bde7-ebc035ec9d9f,53fc5915-4c6a-45b1-8f58-139ab23577e5,55fa720e-86a3-4f1c-84b9-070ce60daf86,563614a5-4001-4726-a7f6-f2c20eaaf107,56d0915c-aac7-40ba-a6aa-35b97c59c6c0,56ee18a3-7ec9-4a41-8fcf-537a44045053,5722142f-d7d8-4ed9-ae79-bd9a55b6fa2d,57d3296d-c035-4692-9996-ab991cd00133,583eb9ed-7751-41d1-841a-ca64398971e9,5843c8f9-3883-4ea7-908d-c291ddea0c70,5908e079-8e79-4673-a108-a0cead1d80cc,59128464-cfd1-4dcb-919c-a2d5d035cd3a,59152ed6-2042-4474-9738-2cbc4743349a,59cd59d8-5962-4bc7-98d8-0652081fbe68,5a8fdfa3-0b6a-47fd-b0d4-bb4041de82c5,5a970e1c-ea54-4f92-95aa-606d133d7abe,5aa3e755-5476-42ea-9036-694c03c37cf2,5ab602fd-93e1-4b8c-a118-8c26ed2a578c,5adce2fa-0bfe-49bc-9b47-059bd12c1f22,5bd4c97e-5842-4867-967b-68698574ef88,5bf0536f-4798-4674-b811-f0c40cd9f967,5bf0536f-4798-4674-b811-f0c40cd9f967_WA,5c22ced8-6f13-4bac-8c37-dd2d3092bb56,5c2f4f83-ea6f-4093-8e0b-31d9e32f3fe5,5c60557d-af70-4c92-b326-56ef145a276e,5cff4292-c7c2-4787-9efb-f626d2c53e8e,5d1bd476-4bdf-4c76-9ffa-9f0752bbf88d,5d846d35-d974-41c9-be89-a7f341f60b50,5da63fe4-64da-4775-901f-26e82e83754e,5db4a5e9-11a8-40fe-804f-122d24f0412b,5e16a423-b412-44c8-a479-64517fad9e7a,5e5883e5-25cd-4643-83bd-0dc255505804,5ed63c6e-7969-4b31-b859-5ac44762d5e8,5f17817e-9bc1-4008-a005-146817e4e104,5fc3eaf3-1e40-4fc9-a0cf-a2ebcaedaf5e,5ff58212-1e28-4dd2-bd77-8c21036b26c7,60420079-c726-4710-89ba-53d4c4d1f38b,6054f41f-6f0f-42ab-b3d5-ee409e9d01cd,60ce167a-84f6-4014-983e-f9d99ffbc140,61329b9a-689f-4b8a-a4a5-b69a251bd194,6209bfe7-593c-4cc8-817a-d223803074c5,6281d901-e0d1-4c04-9d8e-84bba92c4af6,62a245f7-8527-480b-94d6-063bb3059061,62dccf5d-3f8e-43cd-a8f5-50c57608a784,63446dbc-ff88-46a0-ab85-1b042d924620,63b6fe9c-ed0e-41c1-b033-f43fe318f0fa,63bd9490-bf80-434b-8117-a7882a82e743,6420a820-0247-4cc1-b670-00806b8a8eab,64325ca5-f601-4705-acb2-029cff645897,646cc832-bf43-426e-9465-81df27a41838,64e20f33-5b38-41ee-b378-622def8860ca,64fe6bcd-9a93-430e-b3fb-ae015ee30914,65292e7e-c09a-4331-87af-dd9861f3c53e,6540e48f-8fb3-4b9d-9398-6cc5a9285db0,65a89214-ae99-4659-bfe3-d550791f6d53,6634a66e-9378-4d18-a39f-8942a702f73d,663e14bf-af46-4207-80bb-f979317d8634,668600fb-01a8-4990-861d-5001766f913e,66d5e5b9-e520-4199-adcc-040266d2b168,67609cc0-e5c6-4107-a0d3-e557210d0a56,676f51ce-562c-4555-aa98-00fa1219e75c,67f29c70-d319-460b-a139-cf6e812d04a8,682f8fd9-a529-4d09-982a-5f19c6a37f07,68aa68d7-4f15-4730-8351-d694fe6892e9,68ac020e-cae1-4ad7-97f2-b99ab1dc9ad0,68ca9646-a10a-48cc-9590-3a3e6409ad24,6964469f-9e84-465e-96e7-7e9f6016eb86,69a66a50-4578-4e28-87a4-3d38b963dec5,69e1b2d3-f110-4aee-941f-14527bece2e7,69fa8469-f469-4afa-9125-ad8420e5241b,6a332288-72c6-4891-b3b9-2aa842dc7ee0,6aa5e27b-278a-4662-bfee-c3957863a331,6ab45847-4300-4a18-a1e3-76ca4fd20c34,6ac69ee7-cd1b-4e8d-bf99-d8f3a1217a6e,6ae73b38-3c60-4ec8-9775-b9b89055ca6e,6b468f86-0c48-40ea-9cad-bb8313e48273,6b9b8c35-dab2-4db9-b0e5-01e450ca8e25,6b9f3200-bbf6-4835-b3f7-e3edeb6b55cb,6be98ebe-f177-485b-a1b5-62120ae73348,6c16eaef-def0-40f9-b162-0212af7a31ce,6c5619de-705b-4bb6-9b8f-27ab182ddc28,6c6ea24b-41d6-459f-bef1-e816e38cb394,6cbc9cdd-4731-4f05-9d86-3b3e64f0bbda,6cd74de1-1240-4d15-b387-76bb1d43fe2a,6cf6205c-841d-4992-9a14-39806ac5e3fb,6d5ae177-2bb8-4651-944e-2d30c9071e8c,6d5ae177-2bb8-4651-944e-2d30c9071e8c_WA,6e763199-01ce-4bf6-b942-4b9c81534dc3,6e9c8fb9-078e-4711-baee-cd31a4dfed61,6f286ae8-18a0-4bf5-a13b-edc3a9847d7a,6f68f2dc-8652-4efc-8a1b-e09f7e8bcb10,6f9f959b-3e8d-4379-b289-c96fe1ecd9bb,6fa9ba17-338b-4701-bd21-8f2b05e5df7c,6fb59ef7-ade6-4b7c-a580-752b514d29d8,6fefdc01-c851-403a-a2bb-11a6191eb0f1,7013e4bf-c632-48bd-9bf5-4a4cbc227810,70423c55-8dc6-44c8-bd12-e45f5a1d2240,705bae39-cd96-4c3e-a549-21b0f1a7d758,70926b8f-4171-404a-8ece-ae271d1fd913,70bc26e8-4217-4f95-b736-b3a9d0d5899d,70c2f0ae-0439-4162-a3c7-dec80d83ca4f,70f77114-7804-4ef6-b363-6e05e524bc6d,718816b5-8b0f-4c05-accf-03bbc42f9205,719c71f6-9d0a-4b88-bd6c-192ced00e833,71d4d9f3-7b28-44c5-afef-4d63f346e93a,71ef15b1-e4c9-4bb2-a045-696c5aa49360,73a05be2-348c-4cf2-8dcf-5af1209eebe6,73c3d990-f397-4cd9-9c73-f799a8f416d7,742581f1-c750-4ec7-a11e-dcbb0eae04e1,749264dc-bb28-4377-a15b-81442ad146ae,74c615a7-12b0-407f-91c4-3f45b8fa8d02,76319d88-3f40-4726-912e-5aa769ff2f61,7644317f-20bf-4ccf-90a6-045838e8710a,767e63fc-0711-427d-9660-acd434907f3e,7691abf1-7d5d-4252-97d1-023064cef8b4,769be702-27ef-4354-9a83-fbaa8cc61680,76a94ca8-887a-4222-9d01-2d0b20da3b44,76dc831d-4169-4b65-bb1b-18e1cfa7574f,776d2d5b-c7fe-49d1-a071-fd4472964c1e,77b2973c-3704-4b48-8031-c5a9c6fc0073,77e1ca9e-18e5-40d5-bb91-f2c10a0f59b8,786bb1b4-b8d1-489b-b2de-a1f7dd81ad7c,7883750c-e942-4b7c-ab98-0aa40175b0ad,7904f25c-eaba-4d52-abc7-becd0f74d862,7943a327-647e-40ce-8e5b-ed15f5445efc,7963039c-3dcd-43dd-9510-623ebe9351ca,798bb16c-0b4c-4f27-b262-260b1123aeb5,7a6ad5d0-7a13-4503-9ace-179ca052b800,7af53b26-8340-45b3-a18e-c4e27f02c5ae,7b28be39-2b55-4948-9cfd-34d253372029,7b81f738-148c-4d45-9f8c-9e22cc507724,7cc2a990-e9db-4798-b0b1-d99da0a3a61b,7cc64919-13aa-476a-aee4-feb1a95b478d,7da68b43-d25a-4216-a736-fc116c9db955,7dee7996-f2e1-4b02-ab72-898ab4dac1f4,7e060cbb-8782-4c9e-82fe-e371bd8d3f31,7e4bdb27-2a8f-4490-b0ee-24a3c6a495cc,7e5a1f6f-c46d-4862-aa12-4b41628360a9,7e6b5b36-6800-45d1-863e-4b83b35933e0,7f5f5e19-e9d1-420d-bffd-55b087950b1a,800f1e6c-a19d-4851-8c33-caf6df02e7fb,801c3b45-8eb6-41e7-be7f-39aba5b3cb59,8062b90c-271a-48b2-8d3a-4cfbd7c60414,808485b9-ebf0-47ef-b9e0-95fc44d64835,808485b9-ebf0-47ef-b9e0-95fc44d64835_WA,8160d07a-3dd5-4fbe-b999-bc24e6ee5608,8160d07a-3dd5-4fbe-b999-bc24e6ee5608_WA,826df75c-f721-4431-bf30-63ca045b8528,82ee68e0-4b3b-496a-9a71-e00fa81f0112,83690b97-db13-40a1-a595-2975c575a4af,8412e79c-1562-45c9-8ee4-737846d3e027,8412e79c-1562-45c9-8ee4-737846d3e027_WA,84458dc1-f6f5-420e-89a6-0357236c04f8,850dff5b-36d9-4b79-b0b6-b87ab2463c97,85133cb9-e32d-4a1d-bd8c-7479edc8a096,853ca00f-ef27-49e5-bdbd-92b84f6d82ec,8561c410-d954-405c-bef5-8e9c1112ce1a,85a295a0-c4e3-4ba9-9e01-d98463c0a36c,86230e66-cbcb-4fe7-b5ca-71c223174e30,869b0c7a-8ac7-496a-acc6-8a6db61fac09,878db2f2-a424-46f4-b66f-1a004362becb,878db2f2-a424-46f4-b66f-1a004362becb_WA,8800e39e-3a6b-48cd-83e3-5f25367f2310,882c6786-b8f1-4527-9dde-7dda998d6971,886945f8-d535-4940-b372-bc1664f76fbe,88857786-bbc5-43e8-93b7-ab264cb5a269,88acf8e1-3922-4492-8ff2-7de0376b9ec1,895f6508-37d0-473b-9abb-b69dbc40e4d7,89848452-3c93-4fcb-8f73-03e79f30be22,89b8c32a-f6e7-4fdc-b8b8-b2e188962f80,89d4ddd9-108c-4ddc-bc6b-cddece8f856c,89f7760a-395a-42c9-a188-2703c61a0f31,8abe0aab-2319-49e9-a3e8-f396e7641195,8aef2cbd-bc38-4e78-b0cb-cabc24d21747,8b5e6ea1-5e2f-4538-ab21-bfebb1b943e3,8c77a4d2-1be9-42e9-aa00-246b8973bac4,8c7dd4dc-8420-469a-bd81-7418822eaf00,8c85d298-ce67-47cf-833a-fa63bc4d0f2f,8ccf4f1c-4e46-4a0e-9819-296cce9ffdc9,8da6ea7f-b0dc-4fb6-87f6-b6f801b2757d,8dc5c2bd-f743-4c41-9286-22d8d5f78908,8de98301-127e-4840-b7ac-d5955d077c7c,8e3df2ac-cefc-411b-a675-4af41790b5b9,8e9fdb46-2163-4552-9987-b50b32f3e752,8f49bb14-8ed9-4a91-b19a-0888400f57a0,8f510608-c5a1-4720-93e2-0f77c8089438,8f6d7d3b-2431-4029-b501-1fc9c5278672,8f6d7d3b-2431-4029-b501-1fc9c5278672_WA,9070ebed-d09d-4d7a-b9ac-cb1843c56b5c,907f061d-d37a-4c57-8944-7a55f82f4ffc,908432d0-a5d1-433d-9658-8c5481879bd3,910c5002-e381-4d42-ae8c-48aa487a1254,9140965d-9c18-42ce-814b-c4abfe28b2cc,91aaf103-b16f-4cb9-b81c-1394dd4aef29,9215d17c-7d46-4784-ac93-1eafefda8c66,92bf42fd-f180-40f1-a5d9-5fe95d0f8dc7,92d50f48-ca5b-4bf1-8374-47ca6fb4bbe8,932f86e5-b283-44bf-b41b-d951a33d0fe6,93ac7f8d-d832-47ce-9c10-75a1a8842f93,93d43aae-8e7b-4950-a358-1c302bb948a6,94054b7a-a170-4c6f-a708-e50c7f360eac,94054b7a-a170-4c6f-a708-e50c7f360eac_WA,9448c702-ecd0-4153-8e17-0f18cfbdd31a,947c2db9-e32e-4afa-be3d-8c4a48f234dd,947c2db9-e32e-4afa-be3d-8c4a48f234dd_WA,94b63214-0ba2-41fa-94a1-064082739b7e,954a6421-3159-406f-9e25-a951c06dc194,95c69f42-351a-4658-b0ab-50f4d376a4a6,96217a56-ecbb-40ab-bb8f-a575e3b363b3,966c713e-5400-41da-a5b8-6edefe768af2,9670561b-8730-474f-9ae9-69ae96ea898e,97968614-062e-47e9-81b7-6ba54e63a7a2,97a9767f-d1c1-4e19-8ef2-037f1bcdf204,97f5d820-b75e-43c6-9327-fb0e5cad4cc8,98164b8c-66ca-44bf-b55b-e06814379468,98ca8020-e557-4d92-99b2-76310af9e6fa,9924aaf6-46bd-4184-b808-cad62c246925,992f9344-dcad-414b-bb9f-c90fb0ea2f8b,995edeb4-84ba-495f-b1c2-0c5700e436c2,99cfce3e-45e0-44a3-8bdc-6bfa52dda01d,99e6d07a-d141-4bcd-8abe-2a99a5eed3ae,9b1c1706-6f9f-4920-b3f3-29353f001454,9d4e5af7-a256-43d2-8724-f8485c9e6b6c,9deb4bfc-bbab-4134-b900-5f1347f214af,9e5e2005-7503-4c41-b329-679b1cef3817,9e8bd040-cda2-4c44-a4ee-d0c43bcdbebb,9eb106f3-f4e8-485d-b318-b9ee0818b1fd,9eb97758-4665-4fd8-8995-8ef544f11faf,9f111ad5-631a-4b2d-ac8b-45b6c79d4522,9f199b3f-659d-456b-9158-e626537a84b1,a02ac742-7ac4-44e5-a0ca-abfa9e5292a9,a06332aa-e299-436c-a1e7-14d3c2b71153,a0ab4eec-63de-4185-bd7d-86597137073c,a1128c53-06f7-4499-8607-4ce0c1f4499f,a232b2a6-8169-41b2-b6eb-e6d1a86c97aa,a23a4aa1-7518-42df-a4ed-a5cb30d9be7c,a26c16ba-3a71-4329-94bc-53f758bd5bc2,a2a964d7-8338-431c-8225-2791a7713303,a2e4c548-945d-4411-a52b-7cdc0f2d6eb9,a314cc17-7882-473d-8b8f-1549181dc090,a33714f4-851d-423d-a0ac-b4abc22a96d1,a361c2cc-dbc8-49af-8724-d6cd1e43b33a,a3e4b317-ff46-43d9-8f0f-d7c9b8b08316,a3f014dd-649f-4829-b7d0-ead3507ab773,a3ff3aba-a05b-45fb-934a-3e30358a5882,a49a12ef-8349-41b2-8b24-512ae29e78f9,a49c9d5b-2c4a-4e66-bf87-e9e72b55cc54,a535a6ed-dbe3-419c-8d97-8b034020c095,a61de702-f7c1-480d-bda3-d04b705ff124,a6228719-6b06-47a2-b342-001d828ca674,a6445edf-6c0d-4d3c-8742-a2609d55bdab,a64ae5ee-30fe-4204-aea5-879c70f60973,a70707ba-8b5e-4f9b-87c0-2fa5af1cba01,a76f687a-c363-4d43-9ea4-1477e83454f8,a7b3f0b8-8e56-472a-a400-92f616efc3cc,a7baae71-3caf-4c25-a1c7-9907d6bc67c3,a8142981-4aa7-4a1b-872c-1a6462a90bac,a815096d-c4bc-4c15-b032-f0ce41ec2b1c,a936078d-fe75-44a5-b1a4-cad6a8d97274,a9704164-8945-43a4-9413-b30ed93b54a9,a9ffa7b7-3243-4f7a-802d-0692c3fb39a9,aaa136f0-6dcc-4efc-b706-b852af86adc3,aadbb81e-2e83-48df-97dd-1e4fdbb3b5a2,aaed16a5-7d94-400e-9351-af2cbaa4635e,aaf035b6-6528-4189-9927-d3e54af702b1,aaf6151c-8f16-4e18-8984-1590d5f84767,ab11387a-47e7-404b-b75c-96fba68478e1,ab13fc05-4556-4f75-b523-0cd4b6982f8b,ab27669b-48a0-4bcf-90a3-302ad13ab8f9,ab295e73-086c-470a-84ec-255392f4f7f7,ab538fcf-a107-4131-aaa7-15e25f28be65,ab5c1304-dfe8-4ec3-bc04-8a08aea9b865,ab7c710b-a320-41a3-a02a-968ac22ad48e,ac53cf3b-f570-4b08-bc23-2f0904a88661,ac5c13f9-bf8c-4b02-8f9c-1dccdbb8f94c,aebaf458-acdf-41e1-9985-7a8695cc88bf,aede3f93-c3da-4603-9a92-2d0d734ba968,af4d834d-e68f-4728-bd03-d83a1865fb70,af672d16-2620-465a-b1c5-e30e9e0301ea,af79944d-6200-4814-8ffb-bb260ef1fd3c,aff7b600-c825-41fd-9281-eb78cf8c40af,b010da3a-e30a-4580-9c6a-6a0a99c2523f,b05b52f0-a705-478a-bb59-0313a1ea08c6,b0c841f7-86b2-42b4-aa31-49b5119ffa0c,b12b3977-02a4-4a1b-966b-78c30b2facbd,b16d52fa-58d8-4915-a25d-cbe914c900a5,b16fc0d4-4de6-4fed-92a3-04ee6a901935,b22ce05e-2e16-4ed8-bfd2-24838c745051,b2af7a4d-4df0-4ace-99f3-cec2cac85743,b2b204b2-b84c-40bc-b284-8c26f8752a1b,b30e6b83-6042-4c34-b63e-df5a0d6425b9,b3877b5a-b24c-4dfa-8ae0-a9b24b759529,b496e5f2-ab31-4369-bf75-0e24812f9bd0,b4a2367e-439f-465e-9b27-746cd9b17fb9,b4b029ee-0060-42fd-a228-25d6143a62b7,b4dc16d4-e1ed-4f2c-a1e8-4edb2e85710e,b53ee325-dbc1-4f4e-bb19-c594df3e6c30,b560ba9a-a14e-4010-aafc-ae68614bb8cc,b5700e48-8cdb-48a6-9a40-b8ceb59b38cb,b5cc1fc6-967b-42da-9cc0-38d7deef6dc2,b5d44061-7eb1-4df5-b78a-2c5df7e3662c,b5ed2c84-3ecf-4ba6-99cc-6aa9436e7327,b638203e-a891-4817-83ca-ca0926ded6a5,b6535f11-0140-45d5-b181-de23802cb9a2,b6b15d6a-f85e-45bd-8d42-d8fcd57c7c2a,b7f5e736-5bee-470e-93c9-f48c95842ab8,b83c4e22-9a94-49f1-b665-a5bb5dbdedf4,b8ebaf3c-f1e4-477d-9360-9dce3f2ab1a4,b96127e2-073a-484a-a6bb-87c8b61aa3f5,b965d720-1396-4959-97a6-1cf21137c841,b9ee73ce-34a5-4b19-8649-bd5a52e1bf60,ba3513fb-169f-46e5-8950-c41a22b29da4,ba9829e0-8d98-46d6-ac4c-37ae3993931e,bb208702-fb76-4b8c-948e-30b65383f600,bb303200-237d-4f88-acd4-1277be0889a2,bb34a962-e961-407c-89b1-ae99de5dbd7a,bb667b72-8efb-46f7-ba0e-188bbb919544,bbb368fe-d60d-49e3-aa05-fef7cdd0843f,bc5ff5e7-a2fd-4953-9840-c08649875786,bc996936-764a-41b4-94bf-a321433ba098,bcac6232-ab6e-4e7f-9363-13e79d6d00dc,bcc5948d-75f6-4643-90d5-f302923451e0,bd7fced3-c715-4a24-9f0b-f0b1de547d09,bda31785-c2c1-4f00-baf9-a42ee4e5d434,bdcd297e-5e36-4476-bb36-10ea344cbef8,bdf62935-5789-4a71-9b89-52527b9fae39,bdf869c3-461d-4da9-ae42-352a7d496589,bf289f39-fb63-4c9d-8cc8-780ad85ea2b4,c08ccd32-097c-4663-b456-c9b2738484db,c0b825f4-2dac-4918-acf2-3e6d36b1c96d,c0fd48d7-d9ab-475e-a8c2-c518a37c31b0,c12cbb64-46aa-498e-ac33-2a15f25b3335,c15f1254-8645-4c63-abe8-46c2fe208f8e,c15f1254-8645-4c63-abe8-46c2fe208f8e_WA,c1b7e2ff-6663-4651-99a4-a307394e3642,c1cf541c-54b0-47d5-a89c-57aa9c6dbc91,c2fda938-0eab-4796-98b7-a26a40b5ebe7,c31673b4-eaf4-4a62-b6e6-1cef8faab8e4,c32c7860-b62a-442f-ad61-c543234e39fd,c42bab2a-4b0b-4736-9ad5-f16ec7c46956,c4b19295-8046-40fa-a05b-e301b65e407c,c529ebe4-2a5e-4676-b79d-16be60306c4c,c5335ee5-0b9a-4aa7-8ece-c8d9490d4c6f,c5aa9921-4fdb-450a-a7af-ffc33e781db5,c5b7f7ee-3521-49cb-8057-d2e8e69101aa,c5cacf78-6295-4206-b1d0-1f38ff57e1f8,c6644bee-370a-4059-9747-f120f2aeffad,c66ba186-764c-44e0-b54d-b53beb4aca02,c68342a4-e8a5-43cb-8fcf-365f2c80b5ea,c6b3b549-aff0-45e1-9b2a-55b966c97cc2,c6c8b65d-e294-444c-ad40-3dba2380e663,c72e5c42-8aec-464c-ab92-21e999431c16,c7422855-bf42-4663-bb66-3f79a20fdc2e,c79a81aa-ceee-4601-9980-e9c8904d805a,c7f3af40-42ae-4ced-8283-e2296352d5e2,c82bb76a-dd6a-43a7-9ce9-77220ef238f2,c8864cae-3ff5-41fd-9f78-dddad5c63ca0,c8b3b85e-cfa0-4902-95c4-f5654a0fde23,c9b2735a-0ebb-4b1f-9345-7f0aa8878546,ca92d240-54e5-4d08-b365-ff7b520ad16d,cada1077-ab58-4531-85f3-d27b922576a0,cae37d9f-edf8-4671-bdae-ac1d5a9af3f0,cafa11fc-dfce-4ab0-ba7d-263134062672,cb0e4b1e-5393-47cf-b047-8d7f7e3a5a0a,cd458487-a0e8-4426-a298-100eaeb9c754,cdb9f4bf-70a3-47ae-9278-dcb601dbbd28,cde38dac-b4a3-48f9-874f-0a178334671f,ce47d90a-a677-4e3f-90c2-852991580a96,ce90355d-a46f-4ae4-82c2-3c6ca78459b6,ce9c7c19-6689-4ddc-94af-1d55cf3ade3b,cea2fb7c-ca50-4f5f-8bf9-4ebbf536cc2d,ceb03698-1196-44f2-9af9-9870e5d65d8b,cef9c6d1-38b1-45c6-aa97-6de07a2aa7c7,cf683dc3-3121-4805-8c58-32e4305e2944,cf6d3993-7b83-446c-a1e3-bd313fff6edf,cfce89fe-e5a1-4988-a7aa-97e9c56fabb2,cfde8b18-efe7-42d0-9a63-f86ed756f653,d05cdede-0b17-4dcf-ab0d-9154d1c73d89,d065aa1c-569e-4eb9-a504-9d750801df93,d074b14e-6912-49b3-9710-b31da3a93bd1,d131938a-170a-4660-a1cb-3300537baa09,d1968379-53ff-4a12-876f-ee1dff780aed,d1d9305d-9896-4f1d-9d5d-0a1740b86865,d20562b2-1df9-4a08-8e64-9547f44496d1,d20562b2-1df9-4a08-8e64-9547f44496d1_WA,d37b7e62-29a4-4e04-b579-598a7bcb6344,d3b4a56f-176f-473f-abb8-7783f1e7d9e2,d3df53c1-9c4e-4f2a-a55b-5136ffad941d,d408cbb0-2f72-4c65-ad71-175466bc606d,d40d6d3c-181a-4702-8205-b4930612c6a0,d4597392-dfee-46d8-beef-802e15d26ab7,d464e0e8-3ee1-4fbf-ad21-f500d3b3f042,d6033d96-3122-4e9b-b6bb-16f9613a7a97,d6e62150-1088-4f2a-8598-1f73c27e0a4e,d7fe7037-3841-46ed-b6cd-fd7f0259d453,d85de670-a1a3-405a-9188-53e2350eb9fe,d8befac0-315b-4eec-a49c-763010971607,d912363c-bf5b-4d18-9f05-0c3bce0ff050,d93ca390-fc30-4024-861f-c649b638ebce,d94f0d1f-416f-4d36-9b3d-7a83c14d3076,d9bd7df5-84bd-4a0f-8e80-6c0833bf56fa,d9ca5f6c-c943-42fd-a423-ab9bb394a559,da9ee41c-5fe8-4beb-8cb4-f7e1605996b1,daeda1ff-2df5-4764-a901-59d2c660d8d8,db639d1c-d594-46ac-a225-688cd459dfc0,dba9bfae-d4c3-43a1-a18c-8b25dc3fce00,dba9bfae-d4c3-43a1-a18c-8b25dc3fce00_WA,dbc31cf1-2a9c-4285-9ed0-c9c73ab66a8e,dbf8a0ec-080e-4ea9-8a57-73bf3da31949,dc0752a9-570a-4e04-8549-29d296d0c685,dc56a77f-3361-4ca2-aef0-8b6562494d54,dc8f108b-f729-4e11-84eb-61909120c7cf,dd0edcfc-4f04-424a-86a9-b4d5811f4b6b,dd1dace7-9abd-4ac2-ae82-b07279f3f40f,dd9ff599-c185-41cc-b6f2-0773acf00d1f,ddb97e53-e5be-4224-b671-588d9f10b0be,de051afb-b17e-440b-9466-0f3775feda25,de3e4198-c57d-4867-b8ec-786ceb6c2d20,df406876-4bd0-4705-92bd-a624d5abaf9a,dfbbe562-bc50-4c00-9858-b391e7c41843,dfce5dbd-e46c-4f31-9f7f-8254ec354532,dfff6d5d-aea0-4960-b97b-0ac8a800c041,e0328b80-7dc8-4223-83a7-ad42a1e10f5b,e09b008b-5188-43ee-bfeb-b8e990e6cd84,e0c7263d-7482-4576-8526-9c1f9cf72dda,e1a0bef4-4242-441b-b96d-6b37baf14ea0,e30ac7ac-2a7e-4f97-a3da-c58a6eea5885,e33baa5c-fead-426a-bea4-e34583bc250b,e33eb004-9f37-4fda-be91-e7819cdc11c6,e36f4f58-909d-4281-a785-a3b39b2832df,e3a2d26e-5b81-49ca-b3fe-0aa2a7f65775,e403959c-d6dc-455b-a1b9-d4605ae87800,e564a8b9-dae4-4354-a565-af8e6ad148b6,e5c35e02-210d-42af-87d6-ea9f46b8d5d1,e5d5b11c-d989-43e7-9749-133feac1f421,e600d8f9-2ee2-471c-9d69-3142ffb8bae6,e686d3eb-bd8c-462f-bdce-ed830d8244af,e6d9c879-0469-4ef3-b1db-57d6fe6bd291,e6f4f8cd-8677-4415-8263-90ee898a68d2,e7150d66-18f0-47a9-aa14-9a46c28dd339,e738d1f0-02c9-44ba-9856-10c38cae8067,e762a877-3119-446e-82a4-dac68402f6c9,e76cb511-715e-4213-a1dd-a57506e4b7f2,e779bb4a-4e1e-43cb-ba72-27c2f4cb30e1,e7805954-4907-4e5e-8214-b1cd4cb73fd0,e7805954-4907-4e5e-8214-b1cd4cb73fd0_WA,e799746e-63e4-4558-a919-f2b055cb840f,e7c8a353-b3a4-49c0-b3a4-7331772fe2cf,e7cd1c8f-f778-4e6d-aa2b-43240bce64d4,e7f438cc-23e6-431a-92ba-c76bfbafde32,e7fd105b-df64-4236-9daf-15a4e7c596dd,e83073ee-3079-4489-a125-1007aee95737,e865636f-cb5b-4957-8207-12fa9c2dc4d7,e87619e2-9149-47db-b1fb-8799e294c1d0,e910c3df-c074-48d3-9ba7-4477288a1ddc,e91ad083-2a30-421c-b4e3-2c75973f7a62,e92439aa-9866-4cfd-b2d5-a45b28fe2e93,e94dd78b-4f4a-476f-a222-a3d99f650f4c,e94fd6c0-9258-495e-b2ac-5ef9142ac2be,ea30a4b3-e8ce-4995-a9d2-5d06d30de2ae,ea60ccd0-e61f-4c83-ba02-6c84fe1a8960,eae0dfc6-eb9d-4a96-a077-6affd7c5a9ca,eb11400e-edca-403c-972b-d1e754e23a24,eb276c5f-bbae-4186-8150-3b4f10c414bc,ec81ee65-1b59-425d-a705-def4950a2aa0,ed68ed71-6802-47e6-b93a-7dee9f18abfc,ed978ed6-0a38-4dd2-ace8-e9f94bfb2b55,ee21678b-e301-4b85-94ae-5e247e41555d,ef9e88b4-0ba5-4161-bbf1-0e37e4e88f5a,effd22fb-f66d-4117-9371-f74567d542f8,f0022dd7-c940-4998-b082-5117246ac9f4,f07998c2-3c10-48bc-bd22-b62e7c11f9f3,f0bab89f-404c-4436-aae7-383b14a49bf7,f0f1a1f0-252f-4ecd-bc11-153c553bf2e7,f1093dcd-862b-4e8d-9699-664befb38343,f1323580-0038-4b95-b0b7-802371884daf,f1364e89-854d-40f8-8c73-d1ac132140e4,f16ebd65-d569-428f-90b1-aec704f47a3c,f1d5d59d-99d8-457e-98f2-22c0623a6b2c,f2250ebd-55cc-4804-9ace-13446169ee28,f25ddb07-f831-401c-b592-2a17ccb912c9,f2b8c171-b001-4f2b-904e-5bb0ffc94532,f3600d5a-80e1-4318-bc0b-9f3e25cedb4e,f3e631be-043d-439d-ae31-43ec5ffa387c,f50dc53b-1868-49fa-bcc5-7cfe5f433bbf,f51910f6-59a6-445b-a008-1e869be025fc,f5931195-51f6-47b6-8c0c-c99619183f5f,f5a72d99-ed95-45d1-8727-9a46b46287ca,f6da5212-dccc-4322-9c5d-bc149301b051,f6ed63bb-0e89-406c-a296-7e7f4d45e407,f7b81bba-2007-47ea-84b1-52b38589d661,f7c4bb9e-ded5-4e2b-aa4f-752027888d1a,f7f8a7fe-04fb-41cd-8928-b8cc28c51145,f88a12f8-81af-442e-92e2-b4b8fcbc1879,f8dec3e6-143b-49db-b0a3-3f2362ffc20a,f8fd4d1a-cf8d-408a-8066-3359b4158cc5,f9d80e35-aab2-41f7-94b4-43afea2ec809,fa20689c-6b16-4bcf-9d43-9c78c9b1bfce,fa571a98-8774-45a5-9f43-d7f557385333,fad26d8a-a136-4299-8e56-fcb98575a476,fb21af5c-363e-4ad8-9da8-7047ee64bd71,fb24b718-0577-4818-8ac3-c0b9475ef025,fc52b6e0-9f46-4cde-b811-a6d0033a32b0,fc7ec6c0-80b8-486f-9480-20ab013a308c,fc82962b-3afc-4489-af6e-bdb2868ab8ac,fca90b3c-687f-4436-9df2-32d7c26f0a71,fd60b818-76f7-40ef-b9f6-f17aaea1379a,fd61c010-d97e-4a31-abf8-9e53e92b602b,fe451704-3af7-462c-bc62-c9546ed8be98,fe5df609-c32e-4631-8dfe-20849be3d3bb,fe987781-b0d9-4c70-b21a-324d2199ca2d'''
    
    # Filter out _WA entries and format for SQL
    spec_list = [f"'{s.strip()}'" for s in spec_ver_ids.split(',') if not s.strip().endswith('_WA')]
    spec_ver_id_sql = ','.join(spec_list)
    
    query = f"""
    select spoi.id as projectid,
           oas.value as customer_id,
           oas2.value as site_id,
           oas4.value as projectOwnerName,
           oas5.value as siteName,
           oas6.value as PTD,
           o1.entity_name,
           spoi.name,
           oai.last_update_date,
           oai.create_date,
           oai.status,
           spoi.status,
           oai.id as activity_id,
           oai.spec_ver_id
    from ossdb01db.sc_project_order_instance spoi,
         ossdb01db.oss_activity_instance oai,
         ossdb01ref.oss_ref_data o1,
         ossdb01ref.oss_ref_attribute o2,
         ossdb01db.oss_attribute_store oas,
         ossdb01db.oss_attribute_store oas2,
         ossdb01db.oss_attribute_store oas4,
         ossdb01db.oss_attribute_store oas5,
         ossdb01db.oss_attribute_store oas6 
    where oai.part_id in({part_id_list})
          and oai.implementation_type = 'Manual' 
          and oai.spec_ver_id in({spec_ver_id_sql})
          and oai.state in ('In Progress', 'Rework In Progress')
          and oai.last_update_date < current_date - interval '30' day 
          and spoi.plan_id = oai.plan_id 
          and spoi.manager is distinct from 'ProductionSanity' 
          and oai.is_latest_version = 1 
          and spoi.is_latest_version = 1 
          and spoi.name not like '%MM_PROD_TEST%'
          and spoi.status not like 'FCANCELLED' 
          and o2.attribute_value = oai.spec_ver_id 
          and o1.entity_id = o2.entity_id 
          and oas.parent_id = spoi.objid 
          and oas2.parent_id = spoi.objid 
          and oas4.parent_id = spoi.objid 
          and oas5.parent_id = spoi.objid 
          and oas6.parent_id = spoi.objid 
          and oas.code like 'customerID' 
          and oas2.code like 'siteId' 
          and oas4.code like 'projectOwnerName' 
          and oas5.code like 'siteName' 
          and oas6.code like 'DMD_PTD'
    ORDER BY o1.entity_name ASC
    """
    
    try:
        logging.info(f"Executing query for part_id batch: {part_id_batch}")
        cursor.execute(query)
        results = cursor.fetchall()
        
        record_count = len(results) if results else 0
        logging.info(f"✓ BATCH COMPLETE: Fetched {record_count} records for part_id {part_id_batch}")
        
        if record_count > 0:
            logging.info(f"  → Sample first record columns count: {len(results[0])}")
        
        return results
    except Exception as e:
        logging.error(f"✗ ERROR in batch {part_id_batch}")
        logging.error(f"Error details: {type(e).__name__} - {str(e)}")
        logging.error(f"Traceback: {traceback.format_exc()}")
        return []


def fetch_workqueue(cursor, activity_id):
    """
    Fetch workqueue for a given activity_id
    
    Args:
        cursor: Database cursor
        activity_id: Activity ID from oai.id
    
    Returns:
        str: WorkQueue name or 'N/A'
    """
    query = """
    select text_ 
    from act_ru_variable 
    where task_id_ in (
        select task_id_ 
        from act_ru_variable arv 
        where text_ = %s 
        and name_ = 'activityId'
    ) 
    and name_ in ('WorkQueue')
    """
    
    try:
        # Convert activity_id to string and log
        activity_id_str = str(activity_id)
        logging.info(f"    → Querying WorkQueue for activity_id: {activity_id_str}")
        
        # Execute query
        cursor.execute(query, (activity_id_str,))
        result = cursor.fetchone()
        
        if result:
            workqueue = result[0]
            logging.info(f"    ✓ Found WorkQueue: {workqueue}")
            return workqueue
        else:
            logging.warning(f"    ✗ No WorkQueue found in database")
            # Try to debug - check if this activity_id exists in act_ru_variable
            try:
                debug_query = """
                select count(*) 
                from act_ru_variable 
                where text_ = %s and name_ = 'activityId'
                """
                cursor.execute(debug_query, (activity_id_str,))
                count = cursor.fetchone()[0]
                logging.warning(f"    → Debug: Found {count} rows with activityId={activity_id_str} in act_ru_variable")
                
                if count == 0:
                    logging.warning(f"    → This activity_id doesn't exist in act_ru_variable table!")
            except Exception as debug_e:
                logging.warning(f"    → Debug query failed: {debug_e}")
            return 'N/A'
            
    except Exception as e:
        logging.error(f"    ✗ Database error for activity_id={activity_id}: {e}")
        logging.error(f"    → Query was: {query}")
        logging.error(f"    → Parameter: {activity_id}")
        return 'N/A'


def create_summary_table(df):
    """
    Create summary table with task counts and age ranges
    
    Args:
        df (pd.DataFrame): Main data with all tasks
    
    Returns:
        pd.DataFrame: Summary table
    """
    logging.info("Creating summary table...")
    
    if df.empty:
        logging.warning("No data to summarize")
        return pd.DataFrame()
    
    summary_data = []
    
    # Group by Entity Name
    grouped = df.groupby('Entity Name')
    
    for entity_name, group in grouped:
        total_count = len(group)
        
        # Calculate age ranges based on Age column
        last_2_months = len(group[group['Age'] <= 60])
        last_3_months = len(group[group['Age'] <= 90])
        last_6_months = len(group[group['Age'] <= 180])
        older_than_6_months = len(group[group['Age'] > 180])
        
        summary_data.append({
            'Task Name': entity_name,
            'Total Count': total_count,
            'Last 2 Months': last_2_months,
            'Last 3 Months': last_3_months,
            'Last 6 Months': last_6_months,
            'Older than 6 Months': older_than_6_months
        })
        
        logging.info(f"  {entity_name}: Total={total_count}, 2M={last_2_months}, 3M={last_3_months}, 6M={last_6_months}")
    
    summary_df = pd.DataFrame(summary_data)
    
    logging.info(f"✓ Summary table created with {len(summary_df)} rows")
    
    return summary_df


def pull_all_pending_tasks():
    """
    Pull ALL pending tasks using comprehensive spec_ver_id list
    Batches part_id values in groups of 5 to avoid timeout
    
    Returns:
        pd.DataFrame: Combined results from all queries
    """
    # All part_id values (1-99)
    all_part_ids = list(range(1, 100))
    
    # Batch size - reduced to 5 to handle larger spec_ver_id list
    batch_size = 5
    
    all_results = []
    column_names = [
        'Project ID', 'Customer ID', 'Site ID', 'Project Owner Name', 
        'Site Name', 'PTD', 'Entity Name', 'Project Name',
        'Last Update Date', 'Create Date', 'Activity Status', 
        'Project Status', 'Activity ID', 'Spec Ver ID'
    ]
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        logging.info("=" * 80)
        logging.info("STARTING DATA FETCH")
        logging.info("=" * 80)
        logging.info(f"Total part_ids to process: {len(all_part_ids)}")
        logging.info(f"Batch size: {batch_size}")
        logging.info(f"Number of batches: {len(range(0, len(all_part_ids), batch_size))}")
        logging.info("-" * 80)
        
        # Process part_ids in batches of 10
        batch_number = 1
        total_batches = len(range(0, len(all_part_ids), batch_size))
        
        for i in range(0, len(all_part_ids), batch_size):
            part_id_batch = all_part_ids[i:i + batch_size]
            logging.info(f"\n>>> BATCH {batch_number}/{total_batches}")
            
            results = fetch_pending_tasks_batch(cursor, part_id_batch)
            all_results.extend(results)
            
            # Show running total
            logging.info(f">>> Running Total: {len(all_results)} records so far")
            batch_number += 1
        
        logging.info("-" * 80)
        logging.info(f"✓ DATA FETCH COMPLETE")
        logging.info(f"✓ TOTAL RECORDS FETCHED: {len(all_results)}")
        logging.info("=" * 80)
        
        # Convert to DataFrame
        if all_results:
            df = pd.DataFrame(all_results, columns=column_names)
            logging.info(f"✓ DataFrame created successfully with {len(df)} rows and {len(df.columns)} columns")
            
            # Calculate Age column (days since last_update_date)
            logging.info("Calculating Age column...")
            df['Age'] = (pd.Timestamp.now() - pd.to_datetime(df['Last Update Date'])).dt.days
            logging.info(f"✓ Age column added (range: {df['Age'].min()} to {df['Age'].max()} days)")
            
            logging.info(f"  Columns: {', '.join(df.columns.tolist())}")
        else:
            df = pd.DataFrame(columns=column_names + ['Age'])
            logging.warning("⚠ No pending tasks found - DataFrame is empty")
        
        return df
        
    except Exception as e:
        logging.error(f"Error during data fetch: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
        logging.info("Database connection closed")


# ============================================================================
# HTML GENERATION
# ============================================================================
def generate_charts_html(summary_df):
    """
    Generate visual charts HTML from summary data
    
    Args:
        summary_df (pd.DataFrame): Summary table with task counts and age ranges
    
    Returns:
        str: HTML with charts
    """
    if summary_df is None or len(summary_df) == 0:
        return ""
    
    # Sort by total count descending for better visualization
    summary_sorted = summary_df.sort_values('Total Count', ascending=False).head(10)  # Top 10 tasks
    
    # Calculate max value for scaling
    max_count = summary_sorted['Total Count'].max()
    
    # Generate bar chart HTML for task distribution
    chart_html = """
    <div style="background-color: white; padding: 20px; margin: 20px 0; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h3 style="color: #004080; margin-top: 0;">📊 Task Distribution Overview</h3>
        <p style="color: #666;">Top tasks by count with age breakdown</p>
        <div style="margin-top: 20px;">
    """
    
    # Create horizontal bars for each task
    for idx, row in summary_sorted.iterrows():
        task_name = row['Task Name'][:50]  # Truncate long names
        total = row['Total Count']
        last_3m = row['Last 3 Months']
        last_6m = row['Last 6 Months']
        older = row['Older than 6 Months']
        
        # Calculate percentages for stacked bar
        bar_width = (total / max_count) * 100
        last_3m_pct = (last_3m / total * bar_width) if total > 0 else 0
        last_6m_pct = ((last_6m - last_3m) / total * bar_width) if total > 0 else 0
        older_pct = (older / total * bar_width) if total > 0 else 0
        
        chart_html += f"""
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
                <span style="font-weight: bold; font-size: 0.9em; color: #333;">{task_name}</span>
                <span style="font-size: 0.85em; color: #666;">Total: {total}</span>
            </div>
            <div style="background-color: #e0e0e0; height: 30px; border-radius: 5px; overflow: hidden; position: relative;">
                <div style="display: flex; height: 100%;">
                    <div style="background-color: #FFD700; width: {last_3m_pct}%; display: flex; align-items: center; justify-content: center; color: #333; font-size: 0.75em; font-weight: bold;" title="Last 3 Months: {last_3m}">
                        {last_3m if last_3m > 0 else ''}
                    </div>
                    <div style="background-color: #87CEEB; width: {last_6m_pct}%; display: flex; align-items: center; justify-content: center; color: #333; font-size: 0.75em; font-weight: bold;" title="3-6 Months: {last_6m - last_3m}">
                        {last_6m - last_3m if (last_6m - last_3m) > 0 else ''}
                    </div>
                    <div style="background-color: #FFA500; width: {older_pct}%; display: flex; align-items: center; justify-content: center; color: white; font-size: 0.75em; font-weight: bold;" title="Older than 6 Months: {older}">
                        {older if older > 0 else ''}
                    </div>
                </div>
            </div>
        </div>
        """
    
    # Add legend
    chart_html += """
        </div>
        <div style="margin-top: 20px; padding: 10px; background-color: #f8f9fa; border-radius: 5px;">
            <strong>Legend:</strong>
            <span style="margin-left: 15px;"><span style="display: inline-block; width: 15px; height: 15px; background-color: #FFD700; border-radius: 3px; margin-right: 5px;"></span>Last 3 Months (Medium)</span>
            <span style="margin-left: 15px;"><span style="display: inline-block; width: 15px; height: 15px; background-color: #87CEEB; border-radius: 3px; margin-right: 5px;"></span>6 Months (High)</span>
            <span style="margin-left: 15px;"><span style="display: inline-block; width: 15px; height: 15px; background-color: #FFA500; border-radius: 3px; margin-right: 5px;"></span>Older (Critical)</span>
        </div>
    </div>
    """
    
    return chart_html


def generate_ptd_summary_html(df):
    """
    Generate PTD-based visual summary with Past and Future PTD categories
    
    Args:
        df (pd.DataFrame): Main data with PTD column
    
    Returns:
        str: HTML with PTD summary
    """
    if df.empty or 'PTD' not in df.columns:
        return ""
    
    # Convert PTD to datetime
    try:
        df_copy = df.copy()
        df_copy['PTD'] = pd.to_datetime(df_copy['PTD'], errors='coerce')
        current_date = pd.Timestamp.now()
        
        # Calculate PTD categories
        past_ptd_under_1m = len(df_copy[(df_copy['PTD'] < current_date) & (df_copy['PTD'] >= current_date - pd.DateOffset(months=1))])
        past_ptd_under_3m = len(df_copy[(df_copy['PTD'] < current_date) & (df_copy['PTD'] >= current_date - pd.DateOffset(months=3))])
        past_ptd_under_6m = len(df_copy[(df_copy['PTD'] < current_date) & (df_copy['PTD'] >= current_date - pd.DateOffset(months=6))])
        past_ptd_older = len(df_copy[df_copy['PTD'] < current_date - pd.DateOffset(months=6)])
        
        future_ptd_in_3m = len(df_copy[(df_copy['PTD'] >= current_date) & (df_copy['PTD'] < current_date + pd.DateOffset(months=3))])
        future_ptd_2026 = len(df_copy[(df_copy['PTD'] >= pd.Timestamp('2026-01-01')) & (df_copy['PTD'] < pd.Timestamp('2027-01-01'))])
        future_ptd_beyond_2026 = len(df_copy[df_copy['PTD'] >= pd.Timestamp('2027-01-01')])
        
        total_past = past_ptd_under_1m + past_ptd_under_3m + past_ptd_under_6m + past_ptd_older
        total_future = future_ptd_in_3m + future_ptd_2026 + future_ptd_beyond_2026
        
    except Exception as e:
        logging.warning(f"Error calculating PTD summary: {e}")
        return ""
    
    ptd_html = f"""
    <div style="background-color: white; padding: 20px; margin: 20px 0; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1);">
        <h3 style="color: #004080; margin-top: 0;">📅 PTD (Planned Task Date) Summary</h3>
        <p style="color: #666;">Task distribution based on PTD relative to current date</p>
        
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 20px;">
            <!-- Past PTD Section -->
            <div style="border: 2px solid #ff6b6b; border-radius: 8px; padding: 15px; background-color: #fff5f5;">
                <h4 style="color: #ff6b6b; margin-top: 0;">⏰ Past PTD ({total_past} tasks)</h4>
                <div style="margin-top: 15px;">
                    <div style="display: flex; justify-content: space-between; padding: 10px; background-color: white; border-radius: 5px; margin-bottom: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <span style="font-weight: 500;">Under 1 Month</span>
                        <span style="background-color: #ffd43b; padding: 3px 12px; border-radius: 12px; font-weight: bold;">{past_ptd_under_1m}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 10px; background-color: white; border-radius: 5px; margin-bottom: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <span style="font-weight: 500;">Under 3 Months</span>
                        <span style="background-color: #ffd43b; padding: 3px 12px; border-radius: 12px; font-weight: bold;">{past_ptd_under_3m}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 10px; background-color: white; border-radius: 5px; margin-bottom: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <span style="font-weight: 500;">Under 6 Months</span>
                        <span style="background-color: #87CEEB; padding: 3px 12px; border-radius: 12px; font-weight: bold;">{past_ptd_under_6m}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 10px; background-color: white; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <span style="font-weight: 500;">Older than 6 Months</span>
                        <span style="background-color: #FFA500; padding: 3px 12px; border-radius: 12px; font-weight: bold; color: white;">{past_ptd_older}</span>
                    </div>
                </div>
            </div>
            
            <!-- Future PTD Section -->
            <div style="border: 2px solid #51cf66; border-radius: 8px; padding: 15px; background-color: #f0fdf4;">
                <h4 style="color: #51cf66; margin-top: 0;">🔮 Future PTD ({total_future} tasks)</h4>
                <div style="margin-top: 15px;">
                    <div style="display: flex; justify-content: space-between; padding: 10px; background-color: white; border-radius: 5px; margin-bottom: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <span style="font-weight: 500;">In Next 3 Months</span>
                        <span style="background-color: #c3fae8; padding: 3px 12px; border-radius: 12px; font-weight: bold;">{future_ptd_in_3m}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 10px; background-color: white; border-radius: 5px; margin-bottom: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <span style="font-weight: 500;">PTD in 2026</span>
                        <span style="background-color: #c3fae8; padding: 3px 12px; border-radius: 12px; font-weight: bold;">{future_ptd_2026}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 10px; background-color: white; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                        <span style="font-weight: 500;">PTD Beyond 2026</span>
                        <span style="background-color: #c3fae8; padding: 3px 12px; border-radius: 12px; font-weight: bold;">{future_ptd_beyond_2026}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return ptd_html


def generate_html_report(df, summary_df=None):
    """
    Generate HTML report from DataFrame with styled table and visual charts
    
    Args:
        df (pd.DataFrame): Main data to include in the report
        summary_df (pd.DataFrame): Summary table (optional)
    
    Returns:
        str: HTML content
    """
    css_style = """
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .header {
            background-color: #004080;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .description {
            background-color: white;
            padding: 15px;
            margin-bottom: 20px;
            border-left: 4px solid #004080;
            border-radius: 3px;
        }
        .styled-table {
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 0.9em;
            font-family: sans-serif;
            min-width: 100%;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
            background-color: white;
        }
        .styled-table thead tr {
            background-color: #004080;
            color: #ffffff;
            text-align: left;
        }
        .styled-table th,
        .styled-table td {
            padding: 12px 15px;
            border: 1px solid #dddddd;
        }
        .styled-table tbody tr {
            border-bottom: 1px solid #dddddd;
        }
        .styled-table tbody tr:nth-of-type(even) {
            background-color: #f3f3f3;
        }
        .styled-table tbody tr:hover {
            background-color: #e8f4f8;
        }
        .footer {
            margin-top: 30px;
            padding: 15px;
            background-color: white;
            border-radius: 3px;
            font-size: 0.9em;
            color: #666;
        }
        .record-count {
            background-color: #28a745;
            color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
            font-weight: bold;
        }
    </style>
    """
    
    header_html = """
    <div class="header">
        <h1>Orion:All User Pending Task Report</h1>
        <h3>Tasks Impacting Billing,Creating Bad Debt SR's, blocking Non Pay Cease etc</h3>
    </div>
    """
    
    description_html = f"""
    <div class="description">
        <h4>Report Description</h4>
        <p>This is an Amdocs generated report for all pending User tasks for more than 30 days.</p>
        <p>If a task is not being completed intentionally, we should proactively reach out to the user to encourage progress or consider updating the Planned Task Date (PTD) based on their requirements. This approach can help reduce overall order completion time, minimize the need to raise Service Requests (SRs) for pending tasks, and avoid manual efforts related to non-pay cease orders or bad debt customers—who were the leading contributors to SR volume in the last quarter.</p>
        <p>Please take follow-up action with the respective work queue or task owner.</p>
        <p>Please refer to this list before raising any bad debt SRs, especially if the OSO GUI has not been checked.</p>
        <p><strong>Report Generated:</strong> {dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    """
    
    record_count_html = f"""
    <div class="record-count">
        Total Pending Tasks Found: {len(df)}
    </div>
    """
    
    # Generate Visual Charts (shown first)
    charts_html = generate_charts_html(summary_df) if summary_df is not None else ""
    
    # Generate PTD Summary HTML
    ptd_summary_html = generate_ptd_summary_html(df)
    
    # Generate Summary Table HTML
    summary_html = ""
    if summary_df is not None and len(summary_df) > 0:
        summary_html = f"""
        <h2 style="color: #004080; margin-top: 30px;">📋 Summary by Task Type</h2>
        <p><strong>This table shows aggregated counts by task name with age ranges and work queues.</strong></p>
        {summary_df.to_html(index=False, classes='styled-table', escape=False)}
        <hr style="margin: 40px 0;">
        """
    
    # Convert Main DataFrame to HTML
    detailed_table_header = "<h2 style='color: #004080; margin-top: 30px;'>Detailed Task List</h2>"
    if len(df) > 0:
        table_html = detailed_table_header + df.to_html(index=False, classes='styled-table', escape=False)
    else:
        table_html = "<p style='text-align:center; padding:20px; background-color:white;'>No pending tasks found.</p>"
    
    footer_html = """
    <div class="footer">
        <p><strong>Note:</strong> This report includes manual activities that have not been updated for more than 30 days.</p>
        <p><strong>For any changes or clarification, please reach out to:</strong> Abhishek Agrahari (<a href="mailto:abhisha3@amdocs.com">abhisha3@amdocs.com</a>)</p>
        <hr style="margin: 20px 0;">
        <div style="margin-top: 20px;">
            <p style="margin: 5px 0;"><strong>Thanks & Regards,</strong></p>
            <p style="margin: 5px 0;"><strong>Abhishek Agrahari</strong></p>
        </div>
        <hr style="margin: 20px 0;">
        <p style="text-align: center; color: #999; font-size: 0.85em;">Automated Report - Do Not Reply</p>
    </div>
    """
    
    # Combine all HTML parts
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Orion User Pending Task Report</title>
        {css_style}
    </head>
    <body>
        {header_html}
        {description_html}
        {record_count_html}
        {charts_html}
        {ptd_summary_html}
        {summary_html}
        {table_html}
        {footer_html}
    </body>
    </html>
    """
    
    return full_html


def save_html_report(html_content):
    """
    Save HTML content to file
    
    Args:
        html_content (str): HTML content to save
    """
    try:
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logging.info(f"HTML report saved: {HTML_FILE}")
    except Exception as e:
        logging.error(f"Error saving HTML report: {e}")
        raise


def save_excel_report(df, summary_df=None):
    """
    Save DataFrame to Excel file with two sheets
    
    Args:
        df (pd.DataFrame): Main data to export to Excel
        summary_df (pd.DataFrame): Summary data (optional)
    """
    try:
        with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl') as writer:
            # Sheet 1: Summary (if available)
            if summary_df is not None and len(summary_df) > 0:
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                logging.info(f"  Sheet 'Summary' added with {len(summary_df)} rows")
            
            # Sheet 2: Detailed data
            df.to_excel(writer, sheet_name='Detailed Tasks', index=False)
            logging.info(f"  Sheet 'Detailed Tasks' added with {len(df)} rows")
            
        logging.info(f"Excel report saved: {EXCEL_FILE}")
    except Exception as e:
        logging.error(f"Error saving Excel report: {e}")
        raise


# ============================================================================
# EMAIL FUNCTIONS
# ============================================================================
class EmailMgr:
    """Email manager class for sending reports - matches Outage_Report.py pattern"""
    
    def __init__(self, html_content, subject, excel_file=None):
        """
        Initialize email manager
        
        Args:
            html_content (str): HTML content to send
            subject (str): Email subject line
            excel_file (str): Path to Excel file to attach (optional)
        """
        self.html_content = html_content
        self.subject = subject
        self.excel_file = excel_file
    
    def send_mail(self):
        """Send HTML email with the generated report and Excel attachment"""
        logging.info("=" * 80)
        logging.info("PREPARING EMAIL")
        logging.info("=" * 80)
        
        recipients = EMAIL_CONFIG['recipients']
        cc_recipients = EMAIL_CONFIG.get('cc_recipients', [])
        FROM = EMAIL_CONFIG['from']
        
        logging.info(f"From: {FROM}")
        logging.info(f"To Recipients: {len(recipients)}")
        for i, r in enumerate(recipients, 1):
            logging.info(f"  {i}. {r}")
        if cc_recipients:
            logging.info(f"CC Recipients: {len(cc_recipients)}")
            for i, r in enumerate(cc_recipients, 1):
                logging.info(f"  {i}. {r}")
        logging.info(f"Subject: {self.subject}")
        
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['subject'] = self.subject
        MESSAGE['To'] = ", ".join(recipients)
        if cc_recipients:
            MESSAGE['Cc'] = ", ".join(cc_recipients)
        MESSAGE['From'] = FROM
        
        # Attach HTML content
        HTML_BODY = MIMEText(self.html_content, 'html')
        MESSAGE.attach(HTML_BODY)
        logging.info(f"✓ HTML body attached (size: {len(self.html_content)} bytes)")
        
        # Attach Excel file if provided
        if self.excel_file and os.path.exists(self.excel_file):
            try:
                excel_size = os.path.getsize(self.excel_file)
                logging.info(f"Attaching Excel file: {self.excel_file} (size: {excel_size} bytes)")
                
                ctype, encoding = mimetypes.guess_type(self.excel_file)
                if ctype is None or encoding is not None:
                    ctype = 'application/octet-stream'
                
                maintype, subtype = ctype.split('/', 1)
                with open(self.excel_file, 'rb') as fp:
                    attachment = MIMEBase(maintype, subtype)
                    attachment.set_payload(fp.read())
                encoders.encode_base64(attachment)
                
                # Use just the filename for the attachment, not full path
                filename = os.path.basename(self.excel_file)
                attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                MESSAGE.attach(attachment)
                logging.info(f"✓ Excel file attached: {filename}")
            except Exception as e:
                logging.warning(f"⚠ Failed to attach Excel file: {e}")
        else:
            logging.info(f"Excel file not found or not provided: {self.excel_file}")
        
        try:
            logging.info("-" * 80)
            logging.info("SENDING EMAIL...")
            logging.info(f"Connecting to SMTP server: localhost")
            
            server = smtplib.SMTP('localhost')
            logging.info("✓ Connected to SMTP server")
            
            all_recipients = recipients.copy()
            if cc_recipients:
                all_recipients.extend(cc_recipients)
            
            logging.info(f"Sending to {len(all_recipients)} total recipients...")
            server.sendmail(FROM, all_recipients, MESSAGE.as_string())
            server.quit()
            
            logging.info("=" * 80)
            logging.info(f"✓✓✓ EMAIL SENT SUCCESSFULLY to {len(all_recipients)} recipients!")
            logging.info("=" * 80)
        except Exception as e:
            logging.error("=" * 80)
            logging.error(f"✗✗✗ FAILED TO SEND EMAIL")
            logging.error(f"Error: {type(e).__name__} - {str(e)}")
            logging.error(f"Traceback: {traceback.format_exc()}")
            logging.error("=" * 80)
            raise


def send_html_email(html_file, subject, excel_file=None):
    """
    Send HTML email with the generated report and Excel attachment
    Uses the same pattern as Outage_Report.py
    
    Args:
        html_file (str): Path to HTML file to send
        subject (str): Email subject line
        excel_file (str): Path to Excel file to attach (optional)
    """
    try:
        # Read HTML content
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Use EmailMgr class (same as reference script) with Excel attachment
        em = EmailMgr(html_content, subject, excel_file)
        em.send_mail()
        
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        raise


def send_error_notification(error_message):
    """
    Send error notification email
    
    Args:
        error_message (str): Error message to include in email
    """
    try:
        subject = "FAILURE - Orion User Pending Task Report"
        body = f"""
        <html>
        <body>
            <h2 style="color: red;">Script Execution Failed</h2>
            <p><strong>Script:</strong> Check User Pending Task</p>
            <p><strong>Time:</strong> {dt.datetime.now()}</p>
            <p><strong>Error:</strong></p>
            <pre>{error_message}</pre>
        </body>
        </html>
        """
        
        recipients = EMAIL_CONFIG['error_recipients']
        FROM = EMAIL_CONFIG['from']
        
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['Subject'] = subject
        MESSAGE['From'] = FROM
        MESSAGE['To'] = ", ".join(recipients)
        
        HTML_BODY = MIMEText(body, 'html')
        MESSAGE.attach(HTML_BODY)
        
        server = smtplib.SMTP('localhost')
        server.sendmail(FROM, recipients, MESSAGE.as_string())
        server.quit()
        
        logging.info("Error notification sent")
        
    except Exception as e:
        logging.error(f"Failed to send error notification: {e}")


def send_skip_notification():
    """
    Send notification email when script execution is skipped
    """
    try:
        current_day = dt.datetime.now().day
        subject = f"Comcast OSS ||ALL User Pending Task Report || Production (Day {current_day})"
        body = f"""
        <html>
        <body>
            <h3>Script Execution Skipped</h3>
            <p>The User Pending Task report is scheduled to run every {EXECUTION_FREQUENCY}th day of the month.</p>
            <p><strong>Current Day:</strong> {current_day}</p>
            <p><strong>Next Execution:</strong> Day {((current_day // EXECUTION_FREQUENCY) + 1) * EXECUTION_FREQUENCY}</p>
            <p>No action required.</p>
        </body>
        </html>
        """
        
        recipients = EMAIL_CONFIG['error_recipients']
        FROM = EMAIL_CONFIG['from']
        
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE['Subject'] = subject
        MESSAGE['From'] = FROM
        MESSAGE['To'] = ", ".join(recipients)
        
        HTML_BODY = MIMEText(body, 'html')
        MESSAGE.attach(HTML_BODY)
        
        server = smtplib.SMTP('localhost')
        server.sendmail(FROM, recipients, MESSAGE.as_string())
        server.quit()
        
        logging.info("Skip notification sent")
        
    except Exception as e:
        logging.error(f"Failed to send skip notification: {e}")


# ============================================================================
# CLEANUP FUNCTIONS
# ============================================================================
def cleanup_files():
    """
    Move generated files to LOGS directory for archival
    """
    try:
        # Move HTML file to LOGS directory
        if os.path.exists(HTML_FILE):
            dest_path = LOGS_DIR / HTML_FILE
            os.rename(HTML_FILE, dest_path)
            logging.info(f"Moved {HTML_FILE} to LOGS directory")
        
        # Move Excel file to LOGS directory
        if os.path.exists(EXCEL_FILE):
            dest_path = LOGS_DIR / EXCEL_FILE
            os.rename(EXCEL_FILE, dest_path)
            logging.info(f"Moved {EXCEL_FILE} to LOGS directory")
        
        logging.info("Cleanup completed successfully")
        
    except Exception as e:
        logging.warning(f"Error during cleanup: {e}")


# ============================================================================
# MAIN EXECUTION
# ============================================================================
def main():
    """
    Main execution function
    Orchestrates the entire script workflow
    """
    # Setup logging
    setup_logging()
    
    # Log execution mode
    logging.info("=" * 80)
    logging.info("SCRIPT CONFIGURATION")
    logging.info("=" * 80)
    mode = "TEST MODE (emails to abhisha3@amdocs.com only)" if TEST_MODE else "PRODUCTION MODE (emails to all recipients)"
    logging.info(f"🔧 Execution Mode: {mode}")
    logging.info(f"📅 Execution Frequency: Every {EXECUTION_FREQUENCY} day(s)")
    logging.info(f"📧 Recipients: {len(EMAIL_CONFIG['recipients'])} recipient(s)")
    if TEST_MODE:
        logging.info(f"   ⚠️  TEST MODE ACTIVE - Sending to: {', '.join(EMAIL_CONFIG['recipients'])}")
    else:
        logging.info(f"   ✅ PRODUCTION MODE - Sending to {len(EMAIL_CONFIG['recipients'])} recipients")
    logging.info("=" * 80)
    logging.info("")
    
    try:
        # Clean up old logs
        cleanup_old_logs(days_to_keep=30)
        
        # Check if script should execute today
        if not check_execution_day():
            logging.info("Script execution skipped based on day of month")
            send_skip_notification()
            cleanup_files()
            logging.info("Script completed (skipped)")
            return 0
        
        # Fetch pending tasks data
        logging.info("\n")
        logging.info("=" * 80)
        logging.info("STEP 1: FETCHING PENDING TASKS DATA")
        logging.info("=" * 80)
        df_pending_tasks = pull_all_pending_tasks()
        logging.info(f"✓ Data fetch completed. Records: {len(df_pending_tasks)}")
        
        # Create summary table
        logging.info("\n")
        logging.info("=" * 80)
        logging.info("STEP 2: CREATING SUMMARY TABLE")
        logging.info("=" * 80)
        df_summary = create_summary_table(df_pending_tasks)
        logging.info(f"✓ Summary table created with {len(df_summary)} task types")
        
        # Generate HTML report
        logging.info("\n")
        logging.info("=" * 80)
        logging.info("STEP 3: GENERATING HTML REPORT")
        logging.info("=" * 80)
        html_content = generate_html_report(df_pending_tasks, df_summary)
        logging.info(f"HTML content size: {len(html_content)} bytes")
        save_html_report(html_content)
        logging.info(f"✓ HTML report saved: {HTML_FILE}")
        logging.info(f"  File exists: {os.path.exists(HTML_FILE)}")
        if os.path.exists(HTML_FILE):
            logging.info(f"  File size: {os.path.getsize(HTML_FILE)} bytes")
        
        # Generate Excel report
        logging.info("\n")
        logging.info("=" * 80)
        logging.info("STEP 4: GENERATING EXCEL REPORT")
        logging.info("=" * 80)
        save_excel_report(df_pending_tasks, df_summary)
        logging.info(f"✓ Excel report saved: {EXCEL_FILE}")
        logging.info(f"  File exists: {os.path.exists(EXCEL_FILE)}")
        if os.path.exists(EXCEL_FILE):
            logging.info(f"  File size: {os.path.getsize(EXCEL_FILE)} bytes")
        
        # Send email with report and Excel attachment
        logging.info("\n")
        logging.info("=" * 80)
        logging.info("STEP 5: SENDING EMAIL")
        logging.info("=" * 80)
        subject = f"Comcast OSS ||ALL User Pending Task Report || Production - {dt.datetime.now().strftime('%Y-%m-%d')}"
        logging.info(f"Subject: {subject}")
        logging.info(f"HTML File: {HTML_FILE}")
        logging.info(f"Excel File: {EXCEL_FILE}")
        send_html_email(HTML_FILE, subject, EXCEL_FILE)
        
        # Cleanup
        cleanup_files()
        
        logging.info("=" * 80)
        logging.info("Script completed successfully")
        logging.info(f"End Time: {dt.datetime.now()}")
        logging.info("=" * 80)
        
        return 0
        
    except Exception as e:
        logging.error("=" * 80)
        logging.error(f"Script failed with error: {e}")
        logging.error("=" * 80)
        
        # Send error notification
        try:
            send_error_notification(str(e))
        except:
            pass
        
        cleanup_files()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

