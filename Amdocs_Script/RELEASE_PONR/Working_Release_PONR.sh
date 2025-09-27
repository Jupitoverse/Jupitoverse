#!/bin/bash

# Log and HTML output files
LOG_FILE="execution_log_20250610_065832.txt"
HTML_FILE="final_output.html"

# Email configuration
EMAIL_RECIP="abhisha3@amdocs.com"
EMAIL_FROM="noreplyreports@amdocs.com"
EMAIL_SUBJECT="Report || RELEASE PONR flag not released by the System"

# PostgreSQL connection string
CONN_STR="postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb"

# Logging function
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> $LOG_FILE
}

# Execute SQL and save to HTML
function run_query() {
    local start=$1
    local end=$2
    local output=$3
    local sql="
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
    sql=$(echo "$sql" | sed "s/oai.part_id BETWEEN 1 AND 1/oai.part_id BETWEEN $start AND $end/")
    log "Running query for part_id BETWEEN $start AND $end"
    psql "$CONN_STR" -H -c "$sql" -o "$output"
    if [[ $? -ne 0 ]]; then
        log "Query failed for part_id BETWEEN $start AND $end"
        exit 1
    fi
}

# Run all three queries
run_query 1 33 p.html
run_query 34 66 q.html
run_query 67 99 r.html

# Merge HTML tables
log "Merging HTML outputs"
echo "<html><body>" > $HTML_FILE
echo "<p>Hi Team,</p>" >> $HTML_FILE
echo "<p>Please find below the list of orders where the RELEASE PONR flag was not triggered by the system, even though the mandatory wait period associated with the Registered Timed Action has been completed.</p>" >> $HTML_FILE
echo "<p>Kindly review these orders and take the necessary corrective actions. This issue is impacting the business, as services have already been ceased at the customer sites, but billing continues to be active.</p>" >> $HTML_FILE
echo "<table border='1'>" >> $HTML_FILE

# Extract table rows from each file (skip headers after first)
for file in p.html q.html r.html; do
    if [[ -f "$file" ]]; then
        if [[ "$file" == "p.html" ]]; then
            grep -A 1000 "<table" "$file" | grep -B 1000 "</table" >> $HTML_FILE
        else
            grep "<tr>" "$file" | grep -v "<th>" >> $HTML_FILE
        fi
    else
        log "Missing file: $file"
    fi
done

echo "</table>" >> $HTML_FILE
echo "<div class='note'>For any changes in the report: Please reach out to <a href='mailto:abhisha3@amdocs.com'>abhisha3@amdocs.com</a></div>" >> $HTML_FILE
echo "<div class='footer'>Regards,<br>Abhishek Agrahari</div>" >> $HTML_FILE
echo "</body></html>" >> $HTML_FILE

# Send email
log "Sending email"
cat <<EOF | /usr/sbin/sendmail -t
To: $EMAIL_RECIP
From: $EMAIL_FROM
Subject: $EMAIL_SUBJECT
Content-Type: text/html

$(cat $HTML_FILE)
EOF

log "Script completed successfully"
