#!/bin/bash

################################################################################
#
# NAME   : Release PONR Flag Report
# AUTHOR : System Administrator
# DATE   : 06/11/2025
# DESCRIPTION:
#   This script identifies orders where the 'RELEASE PONR' flag was not
#   triggered by the system after a specified waiting period.
#   It performs the following actions:
#   1. Connects to a PostgreSQL database.
#   2. Runs a query, split into three parts based on 'part_id', to reduce DB load.
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

# Generate a unique timestamp for the log/HTML files (e.g., 20250611_114900).
TS=$(date +%Y%m%d_%H%M%S)

# Define the full log file path.
LOG_FILE="execution_log_${TS}.txt"

# Define the final HTML output file name.
HTML_FILE="final_output_${TS}.html"

# --- Email Configuration ---
EMAIL_RECIP="abhisha3@amdocs.com"
EMAIL_FROM="noreplyreports@amdocs.com"
EMAIL_SUBJECT="High-Priority Report || RELEASE PONR Flag Not Released by System"

# --- Database Connection ---
# Format: postgresql://[user]:[password]@[hostname]:[port]/[database]
CONN_STR="postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb"


# --- Logging Function ---

# Central function to handle logging. Appends a timestamped message to the log file.
# Usage: log "Your message here"
function log {
    # Using printf for better formatting control and portability.
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
    max-width: 1200px;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }
  h2 {
    color: #d9534f; /* A red-ish color for alerts */
    border-bottom: 2px solid #d9534f;
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
  }
  th {
    background-color: #337ab7; /* A professional blue */
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

# Executes a SQL query for a given part_id range and saves the result as HTML.
function run_query {
    local start_id=$1
    local end_id=$2
    local output_file=$3

    # The SQL query is defined once as a template.
    # The 'BETWEEN 1 AND 1' is a placeholder that will be replaced.
    local sql_template="
SELECT spoi.id AS projectid, spoi.version, oai.status, spoi.status, oai.id AS activity_id,
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
  AND oai.part_id BETWEEN 1 AND 1;
"
    # Use 'sed' to replace the placeholder with the actual part_id range.
    local final_sql=$(echo "$sql_template" | sed "s/oai.part_id BETWEEN 1 AND 1/oai.part_id BETWEEN ${start_id} AND ${end_id}/")

    log "Executing query for part_id range ${start_id}-${end_id} -> ${output_file}"
    psql "${CONN_STR}" -H -c "${final_sql}" -o "${output_file}"

    # Check if psql command succeeded and created the output file.
    if [[ $? -ne ${SUCCESS} || ! -f "${output_file}" ]]; then
        log "ERROR: Query failed or output file not created for part_id range ${start_id}-${end_id}."
        return ${FAILURE}
    fi
    
    log "Query for part_id range ${start_id}-${end_id} completed successfully."
    return ${SUCCESS}
}

# --- Main Execution ---

log "================== RELEASE PONR Flag Report Script Started =================="

# --- Step 1: Run all three queries ---
# The script will exit immediately if any query fails.
run_query 1 33 "part1.html" || { log "FATAL: Script terminated."; exit ${FAILURE}; }
run_query 34 66 "part2.html" || { log "FATAL: Script terminated."; exit ${FAILURE}; }
run_query 67 99 "part3.html" || { log "FATAL: Script terminated."; exit ${FAILURE}; }

# --- Step 2: Merge the HTML tables into a final report ---
log "Starting HTML merge process."
{
    # Start the HTML document and add the header and CSS.
    echo "<html><head><title>${EMAIL_SUBJECT}</title>"
    get_css
    echo "</head><body><div class='container'>"
    echo "<h2>${EMAIL_SUBJECT}</h2>"

    # Add the descriptive text to the email body.
    echo "<p>Hi Team,</p>"
    echo "<p>Please find below the list of orders where the <strong>RELEASE PONR</strong> flag was not triggered by the system, even though the mandatory wait period associated with the Registered Timed Action has been completed.</p>"
    echo "<p>Kindly review these orders and take the necessary corrective actions. This issue is impacting the business, as services have already been ceased at the customer sites, but billing continues to be active.</p>"

} > "${HTML_FILE}"

# Use 'sed' to extract the complete table from the first file.
log "Extracting base table from part1.html."
sed -n '/<table/,/<\/table>/p' part1.html > final_table.html

# Check if the base table was created.
if [[ ! -s final_table.html ]]; then
    log "WARNING: No data returned from the first query (part_id 1-33). The report may be empty."
    # Create an empty table so the rest of the script doesn't fail.
    echo "<table><thead><tr><th>No Data Found</th></tr></thead><tbody></tbody></table>" > final_table.html
fi

# Create a temporary file to hold data rows from the other parts.
DATA_ROWS_FILE="data_rows_temp.html"
log "Extracting data rows from part2.html and part3.html."
grep '<tr' part2.html | grep -v '<th' >  "${DATA_ROWS_FILE}"
grep '<tr' part3.html | grep -v '<th' >> "${DATA_ROWS_FILE}"

# If data rows were found, merge them into the final table.
if [[ -s "${DATA_ROWS_FILE}" ]]; then
    log "Merging additional data rows into the final table."
    # Use 'awk' to insert the new rows before the closing </tbody> tag.
    awk '/<\/tbody>/{while((getline line<"'"$DATA_ROWS_FILE"'")>0)print line}1' final_table.html > temp.html && mv temp.html final_table.html
else
    log "No additional data rows found in subsequent parts."
fi

# Append the completed table to the main HTML file.
cat final_table.html >> "${HTML_FILE}"

# Add the footer and close the HTML document.
{
    echo "<div class='note'>For any questions, please contact the support team.</div>"
    echo "<div class='footer'>Regards,<br>Orion Reporting Team</div>"
    echo "</div></body></html>"
} >> "${HTML_FILE}"

log "HTML report '${HTML_FILE}' has been successfully created."

# --- Step 3: Send the Email ---
log "Sending email report to: ${EMAIL_RECIP}"
cat "${HTML_FILE}" | /usr/sbin/sendmail -t

if [[ $? -eq ${SUCCESS} ]]; then
    log "Email sent successfully."
else
    log "ERROR: Failed to send email."
fi

# --- Step 4: Cleanup ---
log "Cleaning up temporary files."
rm -f part1.html part2.html part3.html final_table.html "${DATA_ROWS_FILE}"

log "================== RELEASE PONR Flag Report Script Finished =================="
exit ${SUCCESS}
