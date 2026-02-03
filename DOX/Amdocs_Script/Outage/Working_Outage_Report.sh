#!/bin/ksh

#############################################################################
# NAME   : Orion Outage Report Generator
# AUTHOR : Abhishek Agrahari
# DATE   : 05/30/2025
# DESCRIPTION: Generates a 24-hour outage impact report and emails it as HTML
#############################################################################

SUCCESS=0
FAILURE=1
#EMAIL_RECIP="abhisha3@amdocs.com"
EMAIL_RECIP="abhisha3@amdocs.com,Enna.Arora@amdocs.com,Nishant.Bhatia@amdocs.com,prateek.jain5@amdocs.com,mukul.bhasin@amdocs.com,Alon.Kugel@Amdocs.com,Shreyas.Kulkarni@amdocs.com"
EMAIL_FROM="noreplyreports@amdocs.com"
SCRIPT_NAME="orion_outage_report"
TS=$(date +%Y%m%d%H%M%S)
LOG_FILE=${SCRIPT_NAME}_${TS}.log
HTML_FILE="orion_outage_report.html"

DB_CONN="postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb"

function pull_data {
  psql "$DB_CONN" -H -c \
  "SELECT spoi.id, spoi.name, spoi.start_date, spoi.last_updated, spoi.status, spoi.objid, spoi.type, spoi.parent_project_id, spoi.path_to_root
   FROM ossdb01db.sc_project_order_instance spoi
   WHERE spoi.status IN ('BNOT STARTED','CDRELEASE IN PROGRESS','AHHOLD IN PROGRESS')
   AND spoi.last_updated >= NOW() - interval '1 day'
   AND spoi.last_updated <= now();" -o p.html
  (( $? != SUCCESS )) && return $FAILURE
  return $SUCCESS
}

function pull_data_summary {
  psql "$DB_CONN" -H -c \
  "SELECT spoi.status AS Activity_Status, COUNT(*) AS Activity_status_count
   FROM ossdb01db.sc_project_order_instance spoi
   WHERE spoi.status IN ('BNOT STARTED','CDRELEASE IN PROGRESS','AHHOLD IN PROGRESS')
   AND spoi.last_updated >= NOW() - interval '1 day'
   AND spoi.last_updated <= now()
   GROUP BY spoi.status;" -o summary.html
  (( $? != SUCCESS )) && return $FAILURE
  return $SUCCESS
}

function pull_data_activities {
  step=10
  for i in {0..9}; do
    start=$((i * step + 1))
    end=$((start + step - 1))
    output="part_$i.html"
    echo "Running query for part_id BETWEEN $start AND $end"
    psql "$DB_CONN" -H -c \
    "SELECT ord.entity_name AS \"Activty Name\",
           oai.spec_ver_id AS \"Spec Id\",
           aocd.interface AS Interface,
           SUM(CASE
                   WHEN oai.actual_start_date >= NOW() - INTERVAL '1 days'
                        AND oai.actual_start_date < NOW()
                   THEN 1 ELSE 0
               END) AS \"less than 24 hours\"
    FROM ossdb01db.oss_activity_instance oai,
         ossdb01ref.oss_ref_attribute ora,
         ossdb01ref.oss_ref_data ord,
         ossdb01db.activity_overview_custom_data aocd
    WHERE oai.part_id BETWEEN $start AND $end
      AND oai.last_update_date > NOW() - INTERVAL '1 days'
      AND oai.state IN ('In Progress', 'Rework In Progress')
      AND oai.is_latest_version = 1
      AND oai.implementation_type <> 'Manual'
      AND oai.spec_ver_id = ora.attribute_value
      AND ora.entity_id = ord.entity_id
      AND oai.spec_ver_id = aocd.spec_id
      AND oai.spec_ver_id NOT IN (
          'f1f62e0d-6f07-4c0c-be12-631e07b7448f','3936695f-90a1-4e79-8a60-1b460fcf26b4',
          '85a4f2c9-c720-4f30-bd84-408a36da97c2','20e2328d-f681-4c4a-bdad-43ad9da2b728',
          'bf25901d-eb35-48b8-b4ad-ba39d874cbc4','d30f36e7-c671-471b-aa70-bb5ccbe8939f',
          'b0403ef6-3198-4641-8d11-7630361473b9','4bd19612-5446-4f70-bb85-e05b8bcbc9da',
          '546d9598-8d49-4fb9-b2b7-f11ac62ac1c5','2316fc59-1289-4fbf-ba10-e933cdfd9941',
          '2f4a4d90-bccd-43e4-851f-e70073b1da6a','81c7f66d-a2fc-4d89-bc96-d83ebf70b11c',
          'b0012a40-d80f-4a1e-83ce-d78455d21fdc','b4b7b8c9-e275-409d-8657-0c5ffbb28e59',
          '2580eed6-e91b-497e-9504-dd289765eb03','22a7a5a0-fc32-4af0-a929-08aa860c3c4b',
          '0d409cea-5222-45f5-ae88-109c20919bfb','811131f6-8b6b-4548-a535-8708666d1dda',
          'b5bad4ff-7935-4053-afb5-fb1d25797a44','127ecdcc-b677-4132-a95b-c509cfaa7c60',
          'a4267bbb-c25a-4d93-a7c7-3d96c579b895','1aea0862-2530-43c8-9fb0-dc120166f7f4',
          '0c81c4e0-2681-476f-b7d1-bcf14b829265','fb5043db-c056-4529-be38-db0c1bae3f20',
          'e6880c45-1cbd-4d7a-8c4a-044e667ecda5','e3a7de55-7a84-499d-8cc1-9d227d7c357f',
          '330116f0-e475-4afa-b949-697ac94b0d52','02b9b6b8-44eb-4652-b137-de7d5530416f',
          '3f9849dd-5133-46f2-a789-80a21120554e','09d7e394-39b9-4ef0-b747-bc5eeda5d9fd',
          '7597cb49-d972-4e98-b3f1-84687d4360f5','1287e89f-056b-4c3c-a2a7-e200a012bc92',
          '24e86c2a-6cb5-4e0e-ab11-e00dd14da5e4','f2a616fd-ccb0-4b1f-b413-fc915802fa25',
          '8a112601-d9f2-4d33-ab00-19f4f483104b','88f0860f-e647-41cd-aaac-1930adea8a3c',
          '92286b75-55c8-4991-be47-c04c7b3d9780','fddff199-92dc-4862-b90e-6c2bf32efcda',
          'b9e64a57-b511-4b1c-8eb7-c3d7e9feff25','55c4d13b-19d2-45a9-b1b7-a1b9e874aaff',
          '54d3e8c0-4a06-41bc-b7cf-1749177e9ff1','ce922024-75d4-4af5-9b4e-2e8d6d79f3e2',
          '7277a8b5-9eef-4421-bf4b-06b8494e91c9','bb73d434-f14e-4349-b080-83f747900676',
          '6a0bd4cf-8b31-499b-b331-378beb30a2b9','60fa385f-6e81-43e2-b129-08d72aaa5fc7',
          '776d2d5b-c7fe-49d1-a071-fd4472964c1e'
      )
    GROUP BY ord.entity_name, oai.spec_ver_id, aocd.interface
    ORDER BY \"less than 24 hours\" DESC;" -o "$output"
    (( $? != SUCCESS )) && return $FAILURE
  done

  echo "<table>" > activities.html
  for file in part_*.html; do
    if [[ "$file" == "part_0.html" ]]; then
      grep -A 1000 "<table" "$file" | grep -B 1000 "</table" >> activities.html
    else
      grep "<tr>" "$file" | grep -v "<th>" >> activities.html
    fi
  done
  echo "</table>" >> activities.html
  return $SUCCESS
}

function css_only {
cat <<EOF
<style>
  body { font-family: Arial, sans-serif; padding: 20px; color: #333; }
  h2 { color: #004080; border-bottom: 2px solid #004080; padding-bottom: 5px; }
  h3 { color: #004080; margin-top: 30px; }
  table { width: 100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 20px; }
  th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
  th { background-color: #004080; color: white; }
  tr:nth-child(even) { background-color: #f9f9f9; }
  .note { font-style: italic; color: #555; margin-top: 40px; }
  .footer { margin-top: 40px; font-size: 0.9em; color: #666; }
</style>
EOF
}

function send_html_report {
  {
    echo "To: $EMAIL_RECIP"
    echo "From: $EMAIL_FROM"
    echo "Subject: Comcast OSS – Stuck Order Report"
    echo "Content-Type: text/html"
    echo ""
    echo "<html><head>"
    css_only
    echo "</head><body>"
    echo "<p>Hi Team,</p>"
    echo "<p>Please find below the Orion Outage Report for the past 24 hours.</p>"
    echo "<p>The first two tables highlight the impact at the project level, listing projects whose statuses have not changed as expected. These discrepancies indicate potential issues, assuming the system had been functioning correctly.</p>"
    echo "<p>The third table outlines activities that remain stuck in either the 'In Progress' or 'Rework In Progress' status. Some of these may be due to pending third-party callbacks.</p>"

    echo "<h2>Count of Projects which are stuck in 'NOT STARTED','RELEASE IN PROGRESS','HOLD IN PROGRESS'Status past 24 hours</h2>"
    cat summary.html

    echo "<h2>List of Stuck Projects in 'NOT STARTED','RELEASE IN PROGRESS'or 'HOLD IN PROGRESS' Status past 24 hours</h2>"
    cat p.html

    echo "<h2>Stuck Activities and their count whose status not changed from 'In Progress'or  'Rework In Progress' in Last 24 Hours</h2>"
    cat activities.html

    echo "<div class='note'>For any changes in the report: Please reach out to <a href='mailto:abhisha3@amdocs.com'>abhisha3@amdocs.com</a></div>"
    echo "<div class='footer'>Regards,<br>Abhishek Agrahari</div>"

    echo "</body></html>"
  } | /usr/sbin/sendmail -t
}

# Main execution
pull_data_summary || exit $FAILURE
pull_data || exit $FAILURE
pull_data_activities || exit $FAILURE

if [[ -f summary.html && -f p.html && -f activities.html ]]; then
  send_html_report
else
  echo "One or more HTML files are missing. Cannot generate final report." >> $LOG_FILE
  exit $FAILURE
fi

exit $SUCCESS
