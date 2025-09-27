#!/bin/bash

. ./common_functions_PLAB.sh

function pull_data {
  psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -H -c \
  "SELECT spoi.id AS projectid, spoi.version, oai.status, spoi.status, oai.id AS activity_id, spoi.name, oai2.last_update_date, oai.create_date
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
     AND oai.part_id BETWEEN 1 AND 33;" -o p.html
}

function pull_data2 {
  psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -H -c \
  "SELECT spoi.id AS projectid, spoi.version, oai.status, spoi.status, oai.id AS activity_id, spoi.name, oai2.last_update_date, oai.create_date
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
     AND oai.part_id BETWEEN 34 AND 66;" -o q.html
}

function pull_data3 {
  psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -H -c \
  "SELECT spoi.id AS projectid, spoi.version, oai.status, spoi.status, oai.id AS activity_id, spoi.name, oai2.last_update_date, oai.create_date
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
     AND oai.part_id BETWEEN 67 AND 99;" -o r.html
}

function send_html_special_delivery_static_message {
  typeset Recips=$1
  typeset Subject=$4
  typeset HtmlFile=$3
  typeset From=$2

  cat <<-EOF | /usr/sbin/sendmail -t
To: $Recips
From: $From
Content-type: text/html;
Subject: $Subject
$(css_only)
<hr>
<h4>This is a Amdocs generated report for all the pending User task impacting Billing. Please take follow-up with respective work queue or task owner.</h4>
$(cat $HtmlFile)
EOF
}

function exit_process {
  typeset ExitCode=$1

  case $ExitCode in
    0)
      send_html_special_delivery_static_message "$EMAIL_RECIP" "$EMAIL_FROM" "$HTML_FILE" "Report || Orion User Pending Task Impacting Billing || Rebill"
      ;;
    1)
      cat $LOG_FILE | mailx -s "FAILURE - $SCRIPT_NAME" "$ERR_RECIP"
      ;;
  esac

  cleanup
  exit $ExitCode
}

# Main execution
pull_data
pull_data2
pull_data3

cat q.html >> p.html
cat r.html >> p.html
cp p.html final_output.html

HTML_FILE="final_output.html"
EMAIL_RECIP="abhisha3@amdocs.com"
EMAIL_FROM="noreplyreports@amdocs.com"
ERR_RECIP="abhisha3@amdocs.com"
SCRIPT_NAME="split_query_script"

exit_process 0
