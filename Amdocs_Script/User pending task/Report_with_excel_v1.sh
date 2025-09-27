#!/bin/ksh -x

################################################################################
#
# NAME   : Pending User Task Billing Impact Report
# AUTHOR : System Administrator
# DATE   : 06/12/2025
# DESCRIPTION:
#   This script identifies pending manual user tasks that are older than 30
#   days and are impacting the billing process. It is designed to run only
#   on days of the month divisible by 5. The script generates an HTML report
#   in the email body and attaches the same data as a CSV file.
#
################################################################################

# --- Configuration and Setup ---

# Define script exit codes for clarity.
SUCCESS=0
FAILURE=1

# Generate a unique timestamp for log/HTML/CSV files.
TS=$(date +%Y%m%d_%H%M%S)
SCRIPT_NAME="pending_task_billing_report"
LOG_FILE="${SCRIPT_NAME}_${TS}.log"
HTML_FILE="${SCRIPT_NAME}_${TS}.html"
CSV_FILE="${SCRIPT_NAME}_${TS}.csv" # Define CSV filename

# --- Email Configuration ---
EMAIL_RECIP="abhisha3@amdocs.com,prateek.jain5@amdocs.com,anarghaarsha_alexander@comcast.com,chandradeepthi_doruvupalagiri@comcast.com,venkataraghavendrakalyan_ankem@comcast.com,sonalika_sapra2@comcast.com,joseph_thottukadavil@cable.comcast.com,Nishant.Bhatia@amdocs.com,Enna.Arora@amdocs.com,RAJIVKUM@amdocs.com,mukul.bhasin@amdocs.com,daleszandro_jasper@cable.comcast.com,Natasha.Deshpande@amdocs.com"
ERR_RECIP="abhisha3@amdocs.com" # Recipient for failure notifications
EMAIL_FROM="noreplyreports@amdocs.com"
EMAIL_SUBJECT="Report || Orion User Pending Task Impacting Billing"

# --- Database Connection ---
DB_CONN="postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb"


# --- Logging Function ---

# Central function to handle logging. Appends a timestamped message to the log file.
function log {
    printf '%s --- %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" >> "${LOG_FILE}"
}


# --- Core Functions ---

# Function to generate the CSS styles for the HTML report.
function get_css {
cat <<EOF
<style>
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
    margin: 0;
    padding: 0;
    background-color: #f0f2f5;
    color: #333;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  .email-wrapper {
    padding: 20px;
  }
  .container {
    max-width: 1400px;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 20px 40px;
    border-radius: 12px;
    border: 1px solid #e1e4e8;
  }
  .header {
    border-bottom: 1px solid #e1e4e8;
    padding-bottom: 20px;
    margin-bottom: 20px;
  }
  .header h2 {
    color: #c9302c;
    margin: 0;
    font-size: 24px;
  }
  p, li {
    line-height: 1.7;
    font-size: 16px;
    color: #3c4043;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 25px;
  }
  th, td {
    border: 1px solid #dfe2e5;
    padding: 14px 18px;
    text-align: left;
    vertical-align: top;
    font-size: 14px;
  }
  th {
    background-color: #24292e;
    color: white;
    font-weight: 600;
  }
  tr:nth-child(even) {
    background-color: #f6f8fa;
  }
  tr:hover {
    background-color: #f1f8ff;
  }
  .footer {
    margin-top: 30px;
    padding-top: 20px;
    border-top: 1px solid #e1e4e8;
    font-size: 14px;
    color: #586069;
  }
  .footer a {
    color: #0366d6;
    text-decoration: none;
  }
  .footer a:hover {
    text-decoration: underline;
  }
</style>
EOF
}

# Checks the current day of the month to see if the script should run.
function check_count {
    log "Checking current day of the month..."
    local day_of_month=$(psql "${DB_CONN}" -t -c "select date_part('day',now());")
    if [[ $? -ne 0 || -z "$day_of_month" ]]; then
        log "ERROR: Failed to retrieve day of the month from the database."
        # Return a value that will not pass the modulo check
        echo "1"
    else
        log "Database returned day of month: ${day_of_month}"
        echo "${day_of_month}"
    fi
}

# Generic query runner for both HTML and CSV
function run_query {
    local start_id=$1
    local end_id=$2
    local output_file=$3
    local format_option=$4 # psql format option (-H for HTML, -A -F, for CSV)

    local sql="select spoi.id as projectid,oas.value as customer_id ,oas2.value as site_id ,oas4.value as projectOwnerName,oas5.value as siteName ,oas6.value as PTD,o1.entity_name,spoi.name,oai.last_update_date,oai.create_date,oai.status ,spoi.status,oai.id as activity_id from ossdb01db.sc_project_order_instance spoi,ossdb01db.oss_activity_instance oai,ossdb01ref.oss_ref_data o1,ossdb01ref.oss_ref_attribute o2,ossdb01db.oss_attribute_store oas,ossdb01db.oss_attribute_store oas2 ,ossdb01db.oss_attribute_store oas4 ,ossdb01db.oss_attribute_store oas5,ossdb01db.oss_attribute_store oas6 where oai.part_id in(${start_id}) and oai.implementation_type = 'Manual' and oai.spec_ver_id in('5bf0536f-4798-4674-b811-f0c40cd9f967','800f1e6c-a19d-4851-8c33-caf6df02e7fb','e7cd1c8f-f778-4e6d-aa2b-43240bce64d4','234487e7-7dfa-4f09-a7db-6de805f7ff23','234487e7-7dfa-4f09-a7db-6de805f7ff23','6e9c8fb9-078e-4711-baee-cd31a4dfed61','1e1f81de-aea5-4f1c-a621-8daed5a11842','93d43aae-8e7b-4950-a358-1c302bb948a6','f8dec3e6-143b-49db-b0a3-3f2362ffc20a','fa571a98-8774-45a5-9f43-d7f557385333') and oai.state in ('In Progress', 'Rework In Progress')and oai.last_update_date < current_date - interval '30' day and spoi.plan_id = oai.plan_id and spoi.manager is distinct from'ProductionSanity' and oai.is_latest_version = 1 and spoi.is_latest_version = 1 and spoi.name not like '%MM_PROD_TEST%'and spoi.status not like 'FCANCELLED' and o2.attribute_value = oai.spec_ver_id and o1.entity_id = o2.entity_id and oas.parent_id = spoi.objid and oas2.parent_id = spoi.objid and oas4.parent_id = spoi.objid and oas5.parent_id = spoi.objid and oas6.parent_id = spoi.objid and oas.code like 'customerID' and oas2.code like 'siteId' and oas4.code like 'projectOwnerName' and oas5.code like 'siteName' and oas6.code like 'DMD_PTD';"
    
    log "Executing query for part_id range ${start_id} -> ${output_file}"
    psql "${DB_CONN}" ${format_option} -c "${sql}" -o "${output_file}"
    
    if [[ $? -ne ${SUCCESS} ]]; then
        log "ERROR in query execution for ${output_file}. psql command failed."
        return ${FAILURE}
    fi
    log "Query for ${output_file} completed successfully."
    return ${SUCCESS}
}

# Handles script cleanup by moving generated files to a LOGS directory.
function cleanup {
    log "Starting cleanup process."
    mkdir -p LOGS
    mv "${LOG_FILE}" LOGS/ 2>/dev/null
    mv "${HTML_FILE}" LOGS/ 2>/dev/null
    mv "${CSV_FILE}" LOGS/ 2>/dev/null
    rm -f p.html q.html r.html # Remove temporary data files
    rm -f p.csv q.csv r.csv   # Remove temporary csv files
    log "Cleanup complete."
    return ${SUCCESS}
}

# Handles final tasks: sending the correct email and cleaning up files.
function exit_process {
    local exit_code=$1
    log "Starting exit_process with code: ${exit_code}."
    
    if [[ ${exit_code} -eq ${SUCCESS} ]]; then
        log "Assembling and sending final success report to ${EMAIL_RECIP}."
        
        # Create a temporary file for the full email body
        local email_body_file="email_body_${TS}.html"
        {
            echo "<html><head><title>${EMAIL_SUBJECT}</title>"
            get_css
            echo "</head><body><div class='email-wrapper'><div class='container'>"
            echo "<div class='header'><h2>${EMAIL_SUBJECT}</h2></div>"
            echo "<p>Hi Team,</p>"
            echo "<p>Please find the Amdocs generated report of showing billing impacted poending user task.please check with respective workqueue owner to close this asap in order to avoid delay in the NB call and hence reducing Rebill effort.</p>"
            cat "${HTML_FILE}" # Append the merged table
            echo "<div class='footer'>"
            echo "<p>For any changes in the script, Please reach out to <a href='mailto:abhisha3@amdocs.com'>abhisha3@amdocs.com</a></p>"
            echo "<p>Thanks<br>Abhishek Agrahari</p>"
            echo "</div>"
            echo "</div></div></body></html>"
        } > "${email_body_file}"

        # Send email with mutt for attachment support
        # The body is read from the temp file, and the CSV is attached.
        mutt -e "set content_type=text/html" -s "${EMAIL_SUBJECT}" -a "${CSV_FILE}" -- "${EMAIL_RECIP}" < "${email_body_file}"

        if [[ $? -eq 0 ]]; then
            log "Success email with attachment sent successfully."
        else
            log "ERROR: mutt command failed to send email with attachment."
        fi
        rm -f "${email_body_file}"

    else
        log "Sending failure notification email to ${ERR_RECIP}."
        cat "${LOG_FILE}" | mailx -s "FAILURE - ${SCRIPT_NAME}" "${ERR_RECIP}"
    fi

    cleanup
    log "Script finished."
    exit ${exit_code}
}


# --- Main Execution ---
log "================== Pending Task Billing Report Script Started =================="

count=$(check_count)
if (( count % 5 == 0 )); then
    log "Condition met (day ${count} % 5 == 0). The report will proceed."
    
    # --- Step 1: Run Queries for HTML and CSV ---
    log "Starting data pull for HTML and CSV formats."
    part_ids1="1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33"
    part_ids2="34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76"
    part_ids3="77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99"

    run_query "${part_ids1}" "p.html" "-H" || exit_process ${FAILURE}
    run_query "${part_ids2}" "q.html" "-H" || exit_process ${FAILURE}
    run_query "${part_ids3}" "r.html" "-H" || exit_process ${FAILURE}
    
    run_query "${part_ids1}" "p.csv" "--csv" || exit_process ${FAILURE}
    run_query "${part_ids2}" "q.csv" "--csv" || exit_process ${FAILURE}
    run_query "${part_ids3}" "r.csv" "--csv" || exit_process ${FAILURE}
    log "All data pull functions completed successfully."

    # --- Step 2: Merge HTML and CSV results ---
    log "Starting HTML and CSV merge process."
    sed -n '/<table/,/<\/table>/p' p.html > "${HTML_FILE}"
    if [[ ! -s "${HTML_FILE}" ]]; then echo "<table><tr><th>No Data Found</th></tr></table>" > "${HTML_FILE}"; fi
    
    # Combine CSV files, stripping header from 2nd and 3rd files
    cat p.csv > "${CSV_FILE}"
    tail -n +2 q.csv >> "${CSV_FILE}"
    tail -n +2 r.csv >> "${CSV_FILE}"

    DATA_ROWS_FILE="data_rows_temp.html"
    grep '<tr' q.html | grep -v '<th' >  "${DATA_ROWS_FILE}"
    grep '<tr' r.html | grep -v '<th' >> "${DATA_ROWS_FILE}"
    if [[ -s "${DATA_ROWS_FILE}" ]]; then
        awk '/<\/tbody>/{while((getline line<"'"$DATA_ROWS_FILE"'")>0)print line}1' "${HTML_FILE}" > temp.html && mv temp.html "${HTML_FILE}"
    fi
    log "HTML and CSV merge process completed."
    
    # --- Step 3: Trigger Final Email and Cleanup ---
    exit_process ${SUCCESS}

else
    log "Condition not met (day ${count} % 5 != 0). The script will not generate a report."
    printf "Skipping Billing Impact Report today (Day ${count}). Report only runs on days divisible by 5." | mailx -r "${EMAIL_FROM}" -s "INFO - Billing Impact Report Skipped" "${EMAIL_RECIP}"
    log "Skipped-run notification sent. Exiting."
    cleanup
    exit ${SUCCESS}
fi
