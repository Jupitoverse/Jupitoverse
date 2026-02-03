#!/bin/bash

. ./common_functions_PLAB.sh

function pull_data {
  psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -H -c "
    SELECT spoi.id AS projectid, spoi.version, oai.status, spoi.status, oai.id AS activity_id, spoi.name, oai2.last_update_date, oai.create_date
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
  psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -H -c "
    SELECT spoi.id AS projectid, spoi.version, oai.status, spoi.status, oai.id AS activity_id, spoi.name, oai2.last_update_date, oai.create_date
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
  psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -H -c "
    SELECT spoi.id AS projectid, spoi.version, oai.status, spoi.status, oai.id AS activity_id, spoi.name, oai2.last_update_date, oai.create_date
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

function merge_html {
  echo "<p>Hi Team,</p>" > final_output.html
  echo "<p>Please find below the orders where RELEASE PONR flag was not released.</p>" >> final_output.html

  # Extract header from p.html
  grep -m 1 "<table" p.html > header.tmp
  grep "<tr>" p.html | head -1 >> header.tmp
  echo "</table>" >> header.tmp

  # Extract all rows from p.html, q.html, r.html (excluding headers)
  grep "<tr>" p.html | tail -n +2 > rows.tmp
  grep "<tr>" q.html | tail -n +2 >> rows.tmp
  grep "<tr>" r.html | tail -n +2 >> rows.tmp

  # Combine into one table
  echo "<table border='1'>" >> final_output.html
  grep "<tr>" p.html | head -1 >> final_output.html
  cat rows.tmp >> final_output.html
  echo "</table>" >> final_output.html

  echo "<div class='note'>For any changes in the report: Please reach out to <a href='mailto:abhisha3@amdocs.com'>abhisha3@amdocs.com</a></div>" >> final_output.html
  echo "<div class='footer'>Regards,<br>Abhishek Agrahari</div>" >> final_output.html

  rm -f header.tmp rows.tmp
}

function send_report {
  cat <<-EOF | /usr/sbin/sendmail -t
To: abhisha3@amdocs.com
From: noreplyreports@amdocs.com
Content-type: text/html;
Subject: Report || Orion User Pending Task Impacting Billing || Rebill
$(cat final_output.html)
EOF
}

# Run all parts
pull_data
pull_data2
pull_data3
merge_html
send_report
