#!/bin/ksh

################################################################################
#
# NAME   : Orion Outage Report Generator
# AUTHOR : System Administrator
# DATE   : 06/11/2025
# DESCRIPTION:
#   This script generates a daily report on stuck projects and activities
#   in the Orion system. It performs the following actions:
#   1. Connects to a PostgreSQL database.
#   2. Runs queries to get a summary and a detailed list of stuck projects.
#   3. Runs a complex query for stuck activities, split into three parts to
#      reduce database load, and merges the results into a single table.
#   4. Applies enhanced CSS for a professional HTML report.
#   5. Emails the final report to a predefined list of recipients.
#   6. Logs every step to a timestamped file for easy debugging.
#
################################################################################

# --- Configuration and Setup ---

# Define script exit codes for clarity.
SUCCESS=0
FAILURE=1

# Generate a unique timestamp for the log file (e.g., 20250611_235500).
TS=$(date +%Y%m%d_%H%M%S)

# Base name for the script, used for the log file.
SCRIPT_NAME="orion_outage_report"

# Define the full log file path.
LOG_FILE="${SCRIPT_NAME}_${TS}.log"

# --- Email Configuration ---
EMAIL_RECIP="abhisha3@amdocs.com,Enna.Arora@amdocs.com,Nishant.Bhatia@amdocs.com,prateek.jain5@amdocs.com"
EMAIL_FROM="noreplyreports@amdocs.com"
EMAIL_SUBJECT="Orion Daily Outage & Stuck Activity Report"

# --- Database Connection ---
# Format: postgresql://[user]:[password]@[hostname]:[port]/[database]
DB_CONN="postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb"


# --- Logging Function ---

# Central function to handle logging. Appends a timestamped message to the log file.
# Usage: log "Your message here"
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
    max-width: 1200px;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 30px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }
  h2 {
    color: #005a9c; /* A professional blue */
    border-bottom: 2px solid #005a9c;
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
    background-color: #005a9c;
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
    color: #005a9c;
    text-decoration: none;
  }
  .note a:hover {
    text-decoration: underline;
  }
</style>
EOF
}

# Pulls a summary count of stuck projects.
function pull_data_summary {
    log "Function 'pull_data_summary' started."
    psql "$DB_CONN" -H -c \
    "SELECT spoi.status AS Activity_Status, COUNT(*) AS Activity_status_count
     FROM ossdb01db.sc_project_order_instance spoi
     WHERE spoi.status IN ('BNOT STARTED','CDRELEASE IN PROGRESS','AHHOLD IN PROGRESS')
     AND spoi.last_updated >= NOW() - interval '1 day'
     AND spoi.last_updated <= now()
     GROUP BY spoi.status;" -o summary.html

    if [[ $? -eq ${SUCCESS} && -f summary.html ]]; then
        log "Function 'pull_data_summary' completed successfully. 'summary.html' created."
        return ${SUCCESS}
    else
        log "ERROR: Function 'pull_data_summary' failed. psql command error or file not created."
        return ${FAILURE}
    fi
}

# Pulls a detailed list of stuck projects.
function pull_data {
    log "Function 'pull_data' started."
    psql "$DB_CONN" -H -c \
    "SELECT spoi.id, spoi.name, spoi.start_date, spoi.last_updated, spoi.status, spoi.objid, spoi.type, spoi.parent_project_id, spoi.path_to_root
     FROM ossdb01db.sc_project_order_instance spoi
     WHERE spoi.status IN ('BNOT STARTED','CDRELEASE IN PROGRESS','AHHOLD IN PROGRESS')
     AND spoi.last_updated >= NOW() - interval '1 day'
     AND spoi.last_updated <= now();" -o p.html

    if [[ $? -eq ${SUCCESS} && -f p.html ]]; then
        log "Function 'pull_data' completed successfully. 'p.html' created."
        return ${SUCCESS}
    else
        log "ERROR: Function 'pull_data' failed. psql command error or file not created."
        return ${FAILURE}
    fi
}

# Pulls data on stuck activities, split into three queries for performance.
function pull_data_activities {
    log "Function 'pull_data_activities' started."
    local QUERY_TEMPLATE=$(cat <<'EOT'
select ord.entity_name as "Activty Name", oai.spec_ver_id as "Spec Id", aocd.interface as Interface, sum(case when oai.actual_start_date >= now() - interval '1 days' and oai.actual_start_date < now() then 1 else 0 end) as "less than 24 hours"
from oss_activity_instance oai, ossdb01ref.oss_ref_attribute ora,ossdb01ref.oss_ref_data ord,	activity_overview_custom_data aocd
where oai.part_id BETWEEN %d AND %d
and oai.last_update_date > now() - interval '1 days'
and oai.state in ('In Progress', 'Rework In Progress')
and oai.is_latest_version = 1 and oai.implementation_type <> 'Manual'
and oai.spec_ver_id = ora.attribute_value
and ora.entity_id = ord.entity_id
and oai.spec_ver_id = aocd.spec_id
and oai.spec_ver_id not in ('f1f62e0d-6f07-4c0c-be12-631e07b7448f','3936695f-90a1-4e79-8a60-1b460fcf26b4','85a4f2c9-c720-4f30-bd84-408a36da97c2','20e2328d-f681-4c4a-bdad-43ad9da2b728','bf25901d-eb35-48b8-b4ad-ba39d874cbc4','d30f36e7-c671-471b-aa70-bb5ccbe8939f','b0403ef6-3198-4641-8d11-7630361473b9','4bd19612-5446-4f70-bb85-e05b8bcbc9da','546d9598-8d49-4fb9-b2b7-f11ac62ac1c5','2316fc59-1289-4fbf-ba10-e933cdfd9941','2f4a4d90-bccd-43e4-851f-e70073b1da6a','81c7f66d-a2fc-4d89-bc96-d83ebf70b11c','b0012a40-d80f-4a1e-83ce-d78455d21fdc','b4b7b8c9-e275-409d-8657-0c5ffbb28e59','2580eed6-e91b-497e-9504-dd289765eb03','22a7a5a0-fc32-4af0-a929-08aa860c3c4b','0d409cea-5222-45f5-ae88-109c20919bfb','811131f6-8b6b-4548-a535-8708666d1dda','b5bad4ff-7935-4053-afb5-fb1d25797a44','127ecdcc-b677-4132-a95b-c509cfaa7c60','a4267bbb-c25a-4d93-a7c7-3d96c579b895','1aea0862-2530-43c8-9fb0-dc120166f7f4','0c81c4e0-2681-476f-b7d1-bcf14b829265','fb5043db-c056-4529-be38-db0c1bae3f20','e6880c45-1cbd-4d7a-8c4a-044e667ecda5','e3a7de55-7a84-499d-8cc1-9d227d7c357f','330116f0-e475-4afa-b949-697ac94b0d52','02b9b6b8-44eb-4652-b137-de7d5530416f','3f9849dd-5133-46f2-a789-80a21120554e','09d7e394-39b9-4ef0-b747-bc5eeda5d9fd','09d7e394-39b9-4ef0-b747-bc5eeda5d9fd','7597cb49-d972-4e98-b3f1-84687d4360f5','1287e89f-056b-4c3c-a2a7-e200a012bc92','24e86c2a-6cb5-4e0e-ab11-e00dd14da5e4','f2a616fd-ccb0-4b1f-b413-fc915802fa25','8a112601-d9f2-4d33-ab00-19f4f483104b','88f0860f-e647-41cd-aaac-1930adea8a3c','88f0860f-e647-41cd-aaac-1930adea8a3c','88f0860f-e647-41cd-aaac-1930adea8a3c','88f0860f-e647-41cd-aaac-1930adea8a3c','88f0860f-e647-41cd-aaac-1930adea8a3c','88f0860f-e647-41cd-aaac-1930adea8a3c','88f0860f-e647-41cd-aaac-1930adea8a3c','88f0860f-e647-41cd-aaac-1930adea8a3c','88f0860f-e647-41cd-aaac-1930adea8a3c','88f0860f-e647-41cd-aaac-1930adea8a3c','88f0860f-e647-41cd-aaac-1930adea8a3c','92286b75-55c8-4991-be47-c04c7b3d9780','fddff199-92dc-4862-b90e-6c2bf32efcda','b9e64a57-b511-4b1c-8eb7-c3d7e9feff25','55c4d13b-19d2-45a9-b1b7-a1b9e874aaff','54d3e8c0-4a06-41bc-b7cf-1749177e9ff1','ce922024-75d4-4af5-9b4e-2e8d6d79f3e2','7277a8b5-9eef-4421-bf4b-06b8494e91c9','bb73d434-f14e-4349-b080-83f747900676','bb73d434-f14e-4349-b080-83f747900676','6a0bd4cf-8b31-499b-b331-378beb30a2b9','60fa385f-6e81-43e2-b129-08d72aaa5fc7','776d2d5b-c7fe-49d1-a071-fd4472964c1e','776d2d5b-c7fe-49d1-a071-fd4472964c1e')
group by ord.entity_name, oai.spec_ver_id, 	aocd.interface
order by "less than 24 hours" desc;
EOT
    )

    log "Preparing to run queries for stuck activities."
    local query1=$(printf "$QUERY_TEMPLATE" 1 30)
    local query2=$(printf "$QUERY_TEMPLATE" 31 60)
    local query3=$(printf "$QUERY_TEMPLATE" 61 99)

    psql "$DB_CONN" -H -c "$query1" -o activities_part1.html || { log "ERROR: Query for part_id 1-30 failed."; return ${FAILURE}; }
    psql "$DB_CONN" -H -c "$query2" -o activities_part2.html || { log "ERROR: Query for part_id 31-60 failed."; return ${FAILURE}; }
    psql "$DB_CONN" -H -c "$query3" -o activities_part3.html || { log "ERROR: Query for part_id 61-99 failed."; return ${FAILURE}; }

    log "All activity queries completed. Starting merge process."
    sed -n '/<table/,/<\/table>/p' activities_part1.html > activities.html
    
    DATA_ROWS_FILE="activities_data_rows.html"
    grep '<tr' activities_part2.html | grep -v '<th' >  "${DATA_ROWS_FILE}"
    grep '<tr' activities_part3.html | grep -v '<th' >> "${DATA_ROWS_FILE}"

    if [[ -s "${DATA_ROWS_FILE}" ]]; then
        awk '/<\/tbody>/{while((getline line<"'"$DATA_ROWS_FILE"'")>0)print line}1' activities.html > temp.html && mv temp.html activities.html
    fi
    
    log "Cleaning up temporary activity files."
    rm -f activities_part*.html "${DATA_ROWS_FILE}"
    log "Function 'pull_data_activities' completed successfully."
    return ${SUCCESS}
}

# Assembles and sends the final HTML email report.
function send_html_report {
    log "Function 'send_html_report' started. Assembling final email."
    local FINAL_HTML_FILE="final_report_${TS}.html"
    {
        echo "<html><head><title>${EMAIL_SUBJECT}</title>"
        get_css
        echo "</head><body><div class='container'>"
        echo "<h2>${EMAIL_SUBJECT}</h2>"
        echo "<p>Hi Team,</p>"
        echo "<p>Please find below the Orion Outage Report for the past 24 hours. The tables highlight projects and activities that may require attention.</p>"

        echo "<h2>Count of Stuck Projects (Last 24 Hours)</h2>"
        cat summary.html

        echo "<h2>Detailed List of Stuck Projects (Last 24 Hours)</h2>"
        cat p.html

        echo "<h2>Stuck Activities In Progress (Last 24 Hours)</h2>"
        if [[ -f activities.html ]]; then
            cat activities.html
        else
            echo "<p><i>Data for stuck activities is currently unavailable.</i></p>"
        fi

        echo "<div class='note'>For any questions, please contact the support team.</div>"
        echo "<div class='footer'>Regards,<br>Orion Reporting Team</div>"
        echo "</div></body></html>"
    } > "${FINAL_HTML_FILE}"

    cat "${FINAL_HTML_FILE}" | /usr/sbin/sendmail -t
    
    if [[ $? -eq ${SUCCESS} ]]; then
        log "Email sent successfully to: ${EMAIL_RECIP}."
    else
        log "ERROR: Failed to send email."
    fi

    log "Cleaning up final HTML report file: ${FINAL_HTML_FILE}"
    rm -f "${FINAL_HTML_FILE}"
}

# --- Main Execution ---

log "================== Orion Outage Report Script Started =================="

pull_data_summary    || { log "FATAL: Script terminated due to failure in 'pull_data_summary'."; exit ${FAILURE}; }
pull_data            || { log "FATAL: Script terminated due to failure in 'pull_data'."; exit ${FAILURE}; }
pull_data_activities || { log "FATAL: Script terminated due to failure in 'pull_data_activities'."; exit ${FAILURE}; }

log "All data queries completed. Checking for final HTML files..."
if [[ -f summary.html && -f p.html && -f activities.html ]]; then
    log "All necessary HTML files are present. Proceeding to send email."
    send_html_report
else
    log "FATAL: One or more data files are missing. Cannot generate the final report."
    exit ${FAILURE}
fi

log "Cleaning up temporary data files (summary.html, p.html, activities.html)."
rm -f summary.html p.html activities.html

log "================== Orion Outage Report Script Finished Successfully =================="
exit ${SUCCESS}
