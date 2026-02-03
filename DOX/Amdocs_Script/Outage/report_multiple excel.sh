#!/bin/ksh

################################################################################
#
# NAME   : Orion Outage Report Generator
# AUTHOR : System Administrator
# DATE   : 06/12/2025
# DESCRIPTION:
#   Generates a 24-hour outage impact report with three distinct sections.
#   It emails the report as an HTML body and attaches a zip file containing
#   the data from each of the three sections as separate CSV files.
#
################################################################################

# --- Configuration and Setup ---

# Define script exit codes for clarity.
SUCCESS=0
FAILURE=1

# Generate a unique timestamp for all generated files.
TS=$(date +%Y%m%d%H%M%S)
SCRIPT_NAME="orion_outage_report"
LOG_FILE="${SCRIPT_NAME}_${TS}.log"

# Define final zip file name for the attachment
ZIP_FILE="orion_report_${TS}.zip"

# --- Email Configuration ---
EMAIL_RECIP="abhisha3@amdocs.com,Enna.Arora@amdocs.com,Nishant.Bhatia@amdocs.com,prateek.jain5@amdocs.com"
EMAIL_FROM="noreplyreports@amdocs.com"
EMAIL_SUBJECT="Orion Daily Outage & Stuck Activity Report"

# --- Database Connection ---
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
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
    margin: 0;
    padding: 20px;
    background-color: #f0f2f5;
  }
  .container {
    max-width: 1200px;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 30px;
    border-radius: 8px;
    border: 1px solid #e1e4e8;
  }
  h2 {
    color: #005a9c;
    border-bottom: 2px solid #005a9c;
    padding-bottom: 10px;
    margin-top: 30px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
  }
  th, td {
    border: 1px solid #dfe2e5;
    padding: 12px 15px;
    text-align: left;
  }
  th {
    background-color: #24292e;
    color: white;
    font-weight: 600;
  }
  tr:nth-child(even) {
    background-color: #f6f8fa;
  }
</style>
EOF
}

# --- Data Extraction Functions (HTML and CSV) ---

# Pulls a summary count of stuck projects for the HTML body.
function pull_data_summary {
    log "Pulling stuck project summary for HTML body..."
    psql "$DB_CONN" -H -c "SELECT spoi.status AS Activity_Status, COUNT(*) AS Activity_status_count FROM ossdb01db.sc_project_order_instance spoi WHERE spoi.status IN ('BNOT STARTED','CDRELEASE IN PROGRESS','AHHOLD IN PROGRESS') AND spoi.last_updated >= NOW() - interval '1 day' AND spoi.last_updated <= now() GROUP BY spoi.status;" -o summary.html
    (( $? != SUCCESS )) && return $FAILURE
    return $SUCCESS
}

# Pulls the same summary data for the CSV attachment.
function pull_data_summary_csv {
    log "Pulling stuck project summary for CSV attachment..."
    psql "$DB_CONN" --csv -c "SELECT spoi.status AS Activity_Status, COUNT(*) AS Activity_status_count FROM ossdb01db.sc_project_order_instance spoi WHERE spoi.status IN ('BNOT STARTED','CDRELEASE IN PROGRESS','AHHOLD IN PROGRESS') AND spoi.last_updated >= NOW() - interval '1 day' AND spoi.last_updated <= now() GROUP BY spoi.status;" -o summary.csv
    (( $? != SUCCESS )) && return $FAILURE
    return $SUCCESS
}

# Pulls a detailed list of stuck projects for the HTML body.
function pull_data {
    log "Pulling detailed list of stuck projects for HTML body..."
    psql "$DB_CONN" -H -c "SELECT spoi.id, spoi.name, spoi.start_date, spoi.last_updated, spoi.status, spoi.objid, spoi.type, spoi.parent_project_id, spoi.path_to_root FROM ossdb01db.sc_project_order_instance spoi WHERE spoi.status IN ('BNOT STARTED','CDRELEASE IN PROGRESS','AHHOLD IN PROGRESS') AND spoi.last_updated >= NOW() - interval '1 day' AND spoi.last_updated <= now();" -o p.html
    (( $? != SUCCESS )) && return $FAILURE
    return $SUCCESS
}

# Pulls the same detailed list for the CSV attachment.
function pull_data_csv {
    log "Pulling detailed list of stuck projects for CSV attachment..."
    psql "$DB_CONN" --csv -c "SELECT spoi.id, spoi.name, spoi.start_date, spoi.last_updated, spoi.status, spoi.objid, spoi.type, spoi.parent_project_id, spoi.path_to_root FROM ossdb01db.sc_project_order_instance spoi WHERE spoi.status IN ('BNOT STARTED','CDRELEASE IN PROGRESS','AHHOLD IN PROGRESS') AND spoi.last_updated >= NOW() - interval '1 day' AND spoi.last_updated <= now();" -o stuck_projects.csv
    (( $? != SUCCESS )) && return $FAILURE
    return $SUCCESS
}

# Pulls data on stuck activities for the HTML body.
function pull_data_activities {
    log "Pulling stuck activities data for HTML body..."
    psql "$DB_CONN" -H -c "SELECT ord.entity_name, oai.spec_ver_id, SUM(CASE WHEN oai.actual_start_date >= now() - interval '1 day' AND oai.actual_start_date < now() THEN 1 ELSE 0 END) AS \"last 24 hours\" FROM ossdb01db.oss_activity_instance oai, ossdb01ref.oss_ref_attribute ora, ossdb01ref.oss_ref_data ord WHERE oai.part_id BETWEEN 1 AND 99 AND oai.last_update_date > now() - interval '1 days' AND oai.state IN ('In Progress', 'Rework In Progress') AND oai.is_latest_version = 1 AND oai.implementation_type <> 'Manual' AND oai.spec_ver_id = ora.attribute_value AND ora.entity_id = ord.entity_id AND oai.spec_ver_id NOT IN ('20e2328d-f681-4c4a-bdad-43ad9da2b728','bf25901d-eb35-48b8-b4ad-ba39d874cbc4','d30f36e7-c671-471b-aa70-bb5ccbe8939f','b0403ef6-3198-4641-8d11-7630361473b9') GROUP BY ord.entity_name, oai.spec_ver_id;" -o activities.html
    (( $? != SUCCESS )) && return $FAILURE
    return $SUCCESS
}

# Pulls the same stuck activities data for the CSV attachment.
function pull_data_activities_csv {
    log "Pulling stuck activities data for CSV attachment..."
    psql "$DB_CONN" --csv -c "SELECT ord.entity_name, oai.spec_ver_id, SUM(CASE WHEN oai.actual_start_date >= now() - interval '1 day' AND oai.actual_start_date < now() THEN 1 ELSE 0 END) AS \"last 24 hours\" FROM ossdb01db.oss_activity_instance oai, ossdb01ref.oss_ref_attribute ora, ossdb01ref.oss_ref_data ord WHERE oai.part_id BETWEEN 1 AND 99 AND oai.last_update_date > now() - interval '1 days' AND oai.state IN ('In Progress', 'Rework In Progress') AND oai.is_latest_version = 1 AND oai.implementation_type <> 'Manual' AND oai.spec_ver_id = ora.attribute_value AND ora.entity_id = ord.entity_id AND oai.spec_ver_id NOT IN ('20e2328d-f681-4c4a-bdad-43ad9da2b728','bf25901d-eb35-48b8-b4ad-ba39d874cbc4','d30f36e7-c671-471b-aa70-bb5ccbe8939f','b0403ef6-3198-4641-8d11-7630361473b9') GROUP BY ord.entity_name, oai.spec_ver_id;" -o stuck_activities.csv
    (( $? != SUCCESS )) && return $FAILURE
    return $SUCCESS
}

# Assembles and sends the final HTML email report with the zip attachment.
function send_html_report {
    log "Assembling final email body."
    local email_body_file="email_body_${TS}.html"
    {
        echo "<html><head><title>${EMAIL_SUBJECT}</title>"
        get_css
        echo "</head><body><div class='container'>"
        echo "<h2>Orion Outage Report - Last 24 Hours</h2>"
        echo "<p>Hi Team,</p>"
        echo "<p>Please find below the Orion Outage Report for the past 24 hours. The same data is attached as a zip file containing three separate CSV files for your convenience.</p>"
        echo "<h2>Count of Stuck Projects</h2>"
        cat summary.html
        echo "<h2>Detailed List of Stuck Projects</h2>"
        cat p.html
        echo "<h2>Stuck Activities In Progress</h2>"
        cat activities.html
        echo "</div></body></html>"
    } > "${email_body_file}"

    log "Sending email with zip attachment to: ${EMAIL_RECIP}"
    # Use mutt to send the email with the zip file as an attachment.
    mutt -e "set content_type=text/html" -s "${EMAIL_SUBJECT}" -a "${ZIP_FILE}" -- "${EMAIL_RECIP}" < "${email_body_file}"

    if [[ $? -eq 0 ]]; then
        log "Email with attachment sent successfully."
    else
        log "ERROR: mutt command failed to send email."
    fi
    rm -f "${email_body_file}"
}


# --- Main Execution ---

log "================== Orion Outage Report Script Started =================="

# --- Step 1: Execute all data pull functions for HTML and CSV ---
pull_data_summary       || { log "FATAL: pull_data_summary failed."; exit ${FAILURE}; }
pull_data_summary_csv   || { log "FATAL: pull_data_summary_csv failed."; exit ${FAILURE}; }

pull_data               || { log "FATAL: pull_data failed."; exit ${FAILURE}; }
pull_data_csv           || { log "FATAL: pull_data_csv failed."; exit ${FAILURE}; }

pull_data_activities    || { log "FATAL: pull_data_activities failed."; exit ${FAILURE}; }
pull_data_activities_csv|| { log "FATAL: pull_data_activities_csv failed."; exit ${FAILURE}; }
log "All data has been exported to HTML and CSV formats."

# --- Step 2: Create the Zip Archive ---
log "Creating zip archive: ${ZIP_FILE}"
zip "${ZIP_FILE}" summary.csv stuck_projects.csv stuck_activities.csv
if [[ $? -ne 0 ]]; then
    log "FATAL: Failed to create zip archive."
    exit ${FAILURE}
fi
log "Zip archive created successfully."

# --- Step 3: Send the Report ---
log "Checking for necessary files before sending email."
if [[ -f summary.html && -f p.html && -f activities.html && -f "${ZIP_FILE}" ]]; then
    send_html_report
else
    log "FATAL: One or more HTML/ZIP files are missing. Cannot generate the final report."
    exit ${FAILURE}
fi

# --- Step 4: Cleanup ---
log "Cleaning up temporary files."
rm -f summary.html p.html activities.html
rm -f summary.csv stuck_projects.csv stuck_activities.csv
rm -f "${ZIP_FILE}"
log "================== Orion Outage Report Script Finished =================="

exit ${SUCCESS}
