#!/bin/ksh -x

################################################################################
#
# NAME   : Pending User Task Billing Impact Report
# AUTHOR : System Administrator
# DATE   : 06/11/2025
# DESCRIPTION:
#   This script identifies pending manual user tasks that are older than 30
#   days and are impacting the billing process.
#   It performs the following actions:
#   1. Checks if the current day of the month is divisible by 5 to determine
#      if the report should run.
#   2. If the condition is met, it runs a query for pending tasks, split into
#      three parts to reduce database load.
#   3. Merges the results into a single, clean HTML table.
#   4. Applies enhanced CSS for a professional report look.
#   5. Emails the final report to a predefined list of recipients.
#   6. Logs every step to a timestamped file for easy debugging.
#
################################################################################

# --- Configuration and Setup ---

# Define script exit codes for clarity.
SUCCESS=0
FAILURE=1

# Generate a unique timestamp for log/HTML files (e.g., 20250611_143000).
TS=$(date +%Y%m%d_%H%M%S)
SCRIPT_NAME="pending_task_billing_report"
LOG_FILE="${SCRIPT_NAME}_${TS}.log"
HTML_FILE="${SCRIPT_NAME}_${TS}.html"

# --- Email Configuration ---
EMAIL_RECIP="abhisha3@amdocs.com"
#EMAIL_RECIP="abhisha3@amdocs.com,prateek.jain5@amdocs.com,anarghaarsha_alexander@comcast.com,chandradeepthi_doruvupalagiri@comcast.com,venkataraghavendrakalyan_ankem@comcast.com,sonalika_sapra2@comcast.com,joseph_thottukadavil@cable.comcast.com,Nishant.Bhatia@amdocs.com,Enna.Arora@amdocs.com,RAJIVKUM@amdocs.com,mukul.bhasin@amdocs.com,daleszandro_jasper@cable.comcast.com,Natasha.Deshpande@amdocs.com"
ERR_RECIP="abhisha3@amdocs.com" # Recipient for failure notifications
EMAIL_FROM="noreplyreports@amdocs.com"
EMAIL_SUBJECT="Report || Orion User Pending Task Impacting Billing"

# --- Database Connection ---
# Format: postgresql://[user]:[password]@[hostname]:[port]/[database]
DB_CONN="postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb"


# --- Logging Function ---

# Central function to handle logging.
function log {
    printf '%s --- %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" >> "${LOG_FILE}"
}


# --- Core Functions ---

# Function to generate the CSS styles for the HTML report.
function get_css {
cat <<EOF
<style>
  body {
    font-family: Arial, Helvetica, sans-serif;
    margin: 0;
    padding: 20px;
    background-color: #f4f7f6;
    color: #333;
  }
  .container {
    max-width: 1400px;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }
  h2, h4 {
    color: #c9302c; /* A strong red for high alert */
    border-bottom: 2px solid #c9302c;
    padding-bottom: 10px;
    margin-top: 30px;
  }
  p {
    line-height: 1.6;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  }
  th, td {
    border: 1px solid #ddd;
    padding: 12px 15px;
    text-align: left;
    vertical-align: top;
    font-size: 0.9em;
  }
  th {
    background-color: #337ab7;
    color: white;
    font-weight: bold;
  }
  tr:nth-child(even) {
    background-color: #f9f9f9;
  }
  tr:hover {
    background-color: #f1f1f1;
  }
  .note, .footer {
    margin-top: 30px;
    font-size: 0.9em;
    color: #555;
  }
  .note a {
    color: #337ab7;
    text-decoration: none;
  }
  .note a:hover {
    text-decoration: underline;
  }
</style>
EOF
}

# Checks the current day of the month. The report only runs on days divisible by 5.
function check_run_day {
    log "Checking if report should run today."
    local day_of_month=$(psql "${DB_CONN}" -t -c "select date_part('day', now());")
    
    if [[ -z "$day_of_month" ]]; then
        log "ERROR: Could not retrieve day of the month from database."
        return ${FAILURE}
    fi
    
    log "Current day of the month is: ${day_of_month}."
    if (( day_of_month % 5 == 0 )); then
        log "Condition met (day % 5 == 0). The report will proceed."
        return ${SUCCESS}
    else
        log "Condition not met. The script will send a notification and exit."
        # Send a simple notification that the report did not run.
        echo "Skipping Billing Impact Report today (Day ${day_of_month}). Report only runs on days divisible by 5." | mailx -r "${EMAIL_FROM}" -s "INFO - Billing Impact Report Skipped" "${EMAIL_RECIP}"
        return ${FAILURE}
    fi
}

# Executes a SQL query for a given part_id range and saves the result as HTML.
function run_query {
    local start_id=$1
    local end_id=$2
    local output_file=$3

    # The SQL query is defined once as a template.
    local sql_template="
select spoi.id as projectid,oas.value as customer_id ,oas2.value as site_id ,oas4.value as projectOwnerName,oas5.value as siteName ,oas6.value as PTD,o1.entity_name,spoi.name,oai.last_update_date,oai.create_date,oai.status ,spoi.status,oai.id as activity_id
from ossdb01db.sc_project_order_instance spoi,ossdb01db.oss_activity_instance oai,ossdb01ref.oss_ref_data o1,ossdb01ref.oss_ref_attribute o2,ossdb01db.oss_attribute_store oas,ossdb01db.oss_attribute_store oas2 ,ossdb01db.oss_attribute_store oas4 ,ossdb01db.oss_attribute_store oas5,ossdb01db.oss_attribute_store oas6
where oai.part_id BETWEEN ${start_id} AND ${end_id}
and oai.implementation_type = 'Manual'
and oai.spec_ver_id in('5bf0536f-4798-4674-b811-f0c40cd9f967','800f1e6c-a19d-4851-8c33-caf6df02e7fb','e7cd1c8f-f778-4e6d-aa2b-43240bce64d4','234487e7-7dfa-4f09-a7db-6de805f7ff23','234487e7-7dfa-4f09-a7db-6de805f7ff23','6e9c8fb9-078e-4711-baee-cd31a4dfed61','1e1f81de-aea5-4f1c-a621-8daed5a11842','93d43aae-8e7b-4950-a358-1c302bb948a6','f8dec3e6-143b-49db-b0a3-3f2362ffc20a','fa571a98-8774-45a5-9f43-d7f557385333')
and oai.state in ('In Progress', 'Rework In Progress')
and oai.last_update_date < current_date - interval '30' day
and spoi.plan_id = oai.plan_id and spoi.manager is distinct from'ProductionSanity'
and oai.is_latest_version = 1 and spoi.is_latest_version = 1
and spoi.name not like '%MM_PROD_TEST%'
and spoi.status not like 'FCANCELLED'
and o2.attribute_value = oai.spec_ver_id and o1.entity_id = o2.entity_id and oas.parent_id = spoi.objid and oas2.parent_id = spoi.objid and oas4.parent_id = spoi.objid and oas5.parent_id = spoi.objid and oas6.parent_id = spoi.objid
and oas.code like 'customerID' and oas2.code like 'siteId' and oas4.code like 'projectOwnerName' and oas5.code like 'siteName' and oas6.code like 'DMD_PTD';
"
    log "Executing query for part_id range ${start_id}-${end_id} -> ${output_file}"
    psql "${DB_CONN}" -H -c "${sql_template}" -o "${output_file}"

    if [[ $? -ne ${SUCCESS} || ! -f "${output_file}" ]]; then
        log "ERROR: Query failed or output file not created for part_id range ${start_id}-${end_id}."
        return ${FAILURE}
    fi
    
    log "Query for part_id range ${start_id}-${end_id} completed successfully."
    return ${SUCCESS}
}

# Handles final tasks: sending the correct email and cleaning up files.
function exit_process {
    local exit_code=$1
    log "Starting exit_process with code: ${exit_code}."
    
    if [[ ${exit_code} -eq ${SUCCESS} ]]; then
        log "Assembling and sending final success report."
        # Construct the final HTML for the email
        {
            echo "<html><head><title>${EMAIL_SUBJECT}</title>"
            get_css
            echo "</head><body><div class='container'>"
            echo "<h2>${EMAIL_SUBJECT}</h2>"
            echo "<h4>This is an auto-generated report for all pending manual user tasks older than 30 days that are impacting billing. Please take follow-up action with the respective work queue or task owner.</h4>"
            
            # Append the merged table data
            cat "${HTML_FILE}"

            echo "<div class='note'>For assistance, please contact the support team.</div>"
            echo "<div class='footer'>Regards,<br>Orion Reporting Team</div>"
            echo "</div></body></html>"
        } | /usr/sbin/sendmail -t -r "${EMAIL_FROM}" -S "${EMAIL_SUBJECT}" "${EMAIL_RECIP}"
        log "Success email sent."
    else
        log "Sending failure notification email to ${ERR_RECIP}."
        # Send the entire log file on failure
        cat "${LOG_FILE}" | mailx -s "FAILURE - ${SCRIPT_NAME}" "${ERR_RECIP}"
    fi

    log "Cleaning up log and HTML files."
    # Create LOGS directory if it doesn't exist
    mkdir -p LOGS
    mv "${LOG_FILE}" LOGS/
    mv "${HTML_FILE}"* LOGS/ 2>/dev/null
    rm -f part*.html data_rows_temp.html

    log "Script finished."
    exit ${exit_code}
}


# --- Main Execution ---
log "================== Pending Task Billing Report Script Started =================="

# Check if the report should run today. If not, exit_process will not be called.
check_run_day || exit 0

# --- Step 1: Run the three parts of the query ---
log "Starting data pull."
run_query 1 33 "part1.html"  || exit_process ${FAILURE}
run_query 34 76 "part2.html" || exit_process ${FAILURE}
run_query 77 99 "part3.html" || exit_process ${FAILURE}
log "All queries completed successfully."

# --- Step 2: Merge the HTML results ---
log "Starting HTML merge process."
# Use sed to grab the full table from the first file as our base.
sed -n '/<table/,/<\/table>/p' part1.html > "${HTML_FILE}"

# If the first file had no data, the base file will be empty.
if [[ ! -s "${HTML_FILE}" ]]; then
    log "WARNING: No data found in the first query part. The report might be empty."
    # Create an empty table to avoid errors.
    echo "<table><thead><tr><th>No Data Found</th></tr></thead><tbody></tbody></table>" > "${HTML_FILE}"
fi

# Merge data rows from the other parts.
DATA_ROWS_FILE="data_rows_temp.html"
grep '<tr' part2.html | grep -v '<th' >  "${DATA_ROWS_FILE}"
grep '<tr' part3.html | grep -v '<th' >> "${DATA_ROWS_FILE}"

if [[ -s "${DATA_ROWS_FILE}" ]]; then
    log "Merging additional data rows into the final table."
    # Use awk to insert the new rows before the closing </tbody> tag.
    awk '/<\/tbody>/{while((getline line<"'"$DATA_ROWS_FILE"'")>0)print line}1' "${HTML_FILE}" > temp.html && mv temp.html "${HTML_FILE}"
else
    log "No additional data rows found in subsequent query parts."
fi

log "HTML merge process completed."

# --- Step 3: Trigger Final Email and Cleanup ---
exit_process ${SUCCESS}
