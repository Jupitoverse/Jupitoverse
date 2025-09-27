#still giving less records

#!/bin/ksh -x

# Constants
NTH_DAY=1
EMAIL_RECIP="abhisha3@amdocs.com"
EMAIL_FROM="noreplyreports@amdocs.com"
EMAIL_SUBJECT="Report || Orion User Pending Task Impacting Billing"
CONN_STR="postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb"
SCRIPT_NAME="user_pending_task"
TS=$(date '+%Y%m%d_%H%M%S')
LOG_FILE="${SCRIPT_NAME}_${TS}.log"
HTML_FILE="${SCRIPT_NAME}_${TS}.html"
SUCCESS=0
FAILURE=1

log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

run_query() {
    typeset part_ids="$1"
    typeset output="$2"
    log "Running query for part_id IN $part_ids"
    psql "$CONN_STR" -H -c "
SELECT spoi.id AS projectid, oas.value AS customer_id, oas2.value AS site_id,
       oas4.value AS projectOwnerName, oas5.value AS siteName, oas6.value AS PTD,
       o1.entity_name, spoi.name, oai.last_update_date, oai.create_date,
       oai.status, spoi.status, oai.id AS activity_id
FROM ossdb01db.sc_project_order_instance spoi,
     ossdb01db.oss_activity_instance oai,
     ossdb01ref.oss_ref_data o1,
     ossdb01ref.oss_ref_attribute o2,
     ossdb01db.oss_attribute_store oas,
     ossdb01db.oss_attribute_store oas2,
     ossdb01db.oss_attribute_store oas4,
     ossdb01db.oss_attribute_store oas5,
     ossdb01db.oss_attribute_store oas6
WHERE oai.part_id IN $part_ids
  AND oai.implementation_type = 'Manual'
  AND oai.spec_ver_id IN ('5bf0536f-4798-4674-b811-f0c40cd9f967','800f1e6c-a19d-4851-8c33-caf6df02e7fb','e7cd1c8f-f778-4e6d-aa2b-43240bce64d4','234487e7-7dfa-4f09-a7db-6de805f7ff23','234487e7-7dfa-4f09-a7db-6de805f7ff23','6e9c8fb9-078e-4711-baee-cd31a4dfed61','1e1f81de-aea5-4f1c-a621-8daed5a11842','93d43aae-8e7b-4950-a358-1c302bb948a6','f8dec3e6-143b-49db-b0a3-3f2362ffc20a','fa571a98-8774-45a5-9f43-d7f557385333')
  AND oai.state IN ('In Progress', 'Rework In Progress')
  AND oai.last_update_date < current_date - interval '30' day
  AND spoi.plan_id = oai.plan_id
  AND spoi.manager IS DISTINCT FROM 'ProductionSanity'
  AND oai.is_latest_version = 1
  AND spoi.is_latest_version = 1
  AND spoi.name NOT LIKE '%MM_PROD_TEST%'
  AND spoi.status NOT LIKE 'FCANCELLED'
  AND o2.attribute_value = oai.spec_ver_id
  AND o1.entity_id = o2.entity_id
  AND oas.parent_id = spoi.objid AND oas.code = 'customerID'
  AND oas2.parent_id = spoi.objid AND oas2.code = 'siteId'
  AND oas4.parent_id = spoi.objid AND oas4.code = 'projectOwnerName'
  AND oas5.parent_id = spoi.objid AND oas5.code = 'siteName'
  AND oas6.parent_id = spoi.objid AND oas6.code = 'DMD_PTD';" -o "$output"
    if [[ $? -ne 0 ]]; then
        log "Query failed for part_id IN $part_ids"
        return $FAILURE
    fi
    return $SUCCESS
}

merge_html() {
    echo "<html><head><style>
        body { font-family: Arial, sans-serif; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; color: #333; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        tr:hover { background-color: #f1f1f1; }
        .footer { margin-top: 30px; font-style: italic; }
    </style></head><body>" > "$HTML_FILE"
    echo "<p>Hi Team,</p>" >> "$HTML_FILE"
    echo "<p>Please find user pending record:</p>" >> "$HTML_FILE"
    echo "<table>" >> "$HTML_FILE"
    for file in part_*.html; do
        if [[ "$file" == "part_0.html" ]]; then
            grep -A 1000 "<table" "$file" | grep -B 1000 "</table" >> "$HTML_FILE"
        else
            grep "<tr>" "$file" | grep -v "<th>" >> "$HTML_FILE"
        fi
    done
    echo "</table>" >> "$HTML_FILE"
    echo "<div class='footer'>Thanks,<br>Abhishek Agrahari</div>" >> "$HTML_FILE"
    echo "</body></html>" >> "$HTML_FILE"
}

send_email() {
    log "Sending email to $EMAIL_RECIP"
    cat <<EOF | /usr/sbin/sendmail -t
To: $EMAIL_RECIP
From: $EMAIL_FROM
Subject: $EMAIL_SUBJECT
Content-Type: text/html

$(cat "$HTML_FILE")
EOF
}

cleanup() {
    log "Cleaning up temporary files"
    mv "$LOG_FILE" LOGS/ 2>/dev/null
    mv "$HTML_FILE" LOGS/ 2>/dev/null
}

main() {
    day=$(date +%d)
    log "Today is day $day of the month"
    if (( day % NTH_DAY == 0 )); then
        log "Running report as today is a multiple of $NTH_DAY"
        run_query "(1,2,3,4,5,6,7,8,9,10)" part_0.html || exit $FAILURE
        run_query "(11,12,13,14,15,16,17,18,19,20)" part_1.html || exit $FAILURE
        run_query "(21,22,23,24,25,26,27,28,29,30)" part_2.html || exit $FAILURE
        run_query "(31,32,33,34,35,36,37,38,39,40)" part_3.html || exit $FAILURE
        run_query "(41,42,43,44,45,46,47,48,49,50)" part_4.html || exit $FAILURE
        run_query "(51,52,53,54,55,56,57,58,59,60)" part_5.html || exit $FAILURE
        run_query "(61,62,63,64,65,66,67,68,69,70)" part_6.html || exit $FAILURE
        run_query "(71,72,73,74,75,76,77,78,79,80)" part_7.html || exit $FAILURE
        run_query "(81,82,83,84,85,86,87,88,89,90)" part_8.html || exit $FAILURE
        run_query "(91,92,93,94,95,96,97,98,99,100)" part_9.html || exit $FAILURE
        merge_html
        send_email
    else
        log "Skipping report generation. Today is not a multiple of $NTH_DAY."
    fi
    cleanup
    exit $SUCCESS
}

main