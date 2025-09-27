#!/bin/ksh -x
#############################################################################
#NAME   :     To generate the report of impact of any Outage
#To Check the stuck Projects
#To check the stuck activities
#To check the orders where RELEASE_PONR flag not released by system on time

#AUTHOR :      Abhishek Agrahari
#DATE   :      05/30/2025
#DESCRIPTION:   To generate the report of impact of any Outage
#CASE   :
#############################################################################

. ./common_functions_PLAB.sh

SUCCESS=0
FAILURE=1

function check_count {
  count=(`psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -t -c "select date_part('day',now());"`)
  echo $count
}

function pull_data {
  psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -H -c"select spoi.id,spoi.name,spoi.start_date,spoi.last_updated,spoi.status,spoi.objid,spoi.type,spoi.parent_project_id,spoi.path_to_root from ossdb01db.sc_project_order_instance spoi where spoi.status in('BNOT STARTED','CDRELEASE IN PROGRESS','AHHOLD IN PROGRESS') and spoi.last_updated >= NOW()-interval '1 day' and spoi.last_updated <= now();" -o p.html
  (( $? != SUCCESS )) && return $FAILURE
  return $SUCCESS
}

function pull_data_summary {
  psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -H -c"select spoi.status as Activity_Status, count(*) as Activity_status_count from ossdb01db.sc_project_order_instance spoi where spoi.status in ('BNOT STARTED','CDRELEASE IN PROGRESS','AHHOLD IN PROGRESS') and spoi.last_updated >= NOW()-interval '1 day' and spoi.last_updated <= now() group by spoi.status;" -o summary.html
  (( $? != SUCCESS )) && return $FAILURE
  return $SUCCESS
}

function pull_data_activities {
  psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -H -c"select ord.entity_name, oai.spec_ver_id, sum(case when oai.actual_start_date >= now() - interval '1 day' and oai.actual_start_date < now() then 1 else 0 end) as \"last 24 hours\" from ossdb01db.oss_activity_instance oai, ossdb01ref.oss_ref_attribute ora, ossdb01ref.oss_ref_data ord where oai.part_id between 1 and 99 and oai.last_update_date > now() - interval '1 days' and oai.state in ('In Progress', 'Rework In Progress') and oai.is_latest_version = 1 and oai.implementation_type <> 'Manual' and oai.spec_ver_id = ora.attribute_value and ora.entity_id = ord.entity_id and oai.spec_ver_id not in ('20e2328d-f681-4c4a-bdad-43ad9da2b728','bf25901d-eb35-48b8-b4ad-ba39d874cbc4') group by ord.entity_name, oai.spec_ver_id;" -o activities.html
  (( $? != SUCCESS )) && return $FAILURE
  return $SUCCESS
}

function css_only {
cat <<EOF
<style>
  body { font-family: Arial, sans-serif; }
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  th, td {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
  }
  th {
    background-color: #004080;
    color: white;
  }
  tr:nth-child(even) {
    background-color: #f2f2f2;
  }
  h4 {
    color: #004080;
  }
</style>
EOF
}

function cleanup {
  mv $LOG_FILE LOGS/ 2>/dev/null
  [[ -f $HTML_FILE ]] && mv $HTML_FILE LOGS/
  return $SUCCESS
}

function send_html_special_delivery_static_message {
  typeset Recips=$1
  typeset Subject=$4
  typeset HtmlFile=$3
  typeset From=$2

  {
    echo "To: $Recips"
    echo "From: $From"
    echo "Subject: $Subject"
    echo "Content-Type: text/html"
    echo ""
    echo "<html><head>"
    css_only
    echo "</head><body>"
    echo "<h4>This is an Orion outage impact report for last 24 hours which checks for the stuck projects and activity</h4>"
    echo "<h4>Summary of Activity Status which remained same in last 24 hours</h4>"
    cat summary.html
    echo "<h4>Stuck Projects and Orders</h4>"
    cat p.html
    echo "<h4>Stuck Activities and their respective Count in last 24 hours</h4>"
    cat activities.html
    echo "</body></html>"
  } | /usr/sbin/sendmail -t

  return $SUCCESS
}

function exit_process {
  typeset ExitCode=$1
  printf "\nEnd $(date)\n" >> $LOG_FILE

  case $ExitCode in
    $SUCCESS)
      send_html_special_delivery_static_message "$EMAIL_RECIP" "$EMAIL_FROM" "$HTML_FILE" "Environment Impact Report: Stuck Activities and Projects"
      ;;
    $FAILURE)
      cat $LOG_FILE | mailx -s "FAILURE - $AREA $CLIENT $SCRIPT_NAME" "$ERR_RECIP"
      ;;
  esac
  cleanup
  exit $ExitCode
}

#main()
typeset -r LOG_FILE=${SCRIPT_NAME}_${TS}.log
typeset -r HTML_FILE=${SCRIPT_NAME}_${TS}.html
typeset -r HTML_FILE_COUNT=${SCRIPT_NAME}_COUNT_${TS}.html
typeset -r TDATE=$(date --date="today" +"%m/%d/%Y")
typeset -r HDATE=$(date --date="today" +"%H")
typeset -r TRANSDATE=$(date | awk '{print $3}')
typeset -r TDAY=$(date --date="today" +"%d")
typeset -r CDATE=$(date +%a)
typeset -r CSS=$(cat trans_billing_midmarket_css.dat)

text_disp="information present at the end"
#EMAIL_RECIP="abhisha3@amdocs.com,prateek.jain5@amdocs.com,Nishant.Bhatia@amdocs.com"
EMAIL_RECIP="abhisha3@amdocs.com"
ERR_RECIP="abhisha3@amdocs.com"
EMAIL_FROM="noreplyreports@amdocs.com"
typeset -r APPLICATION="OSO"

count=$(check_count)
echo $count

if (( $count %1==0 ))
then
  printf " There are "$count" records today in database."  >> $LOG_FILE
  pull_data_summary || exit_process $FAILURE
  pull_data || exit_process $FAILURE
  pull_data_activities || exit_process $FAILURE

  if [[ -f summary.html && -f p.html && -f activities.html ]]; then
    cat summary.html p.html activities.html > "$HTML_FILE"
  else
    echo "One or more HTML files are missing. Cannot generate final report." >> $LOG_FILE
    exit_process $FAILURE
  fi
else
  cat $LOG_FILE | mailx -r $EMAIL_FROM -s "$CUSTNAME $AREA - SOM" "$EMAIL_RECIP"
  cleanup
  exit 0
fi

exit_process $SUCCESS
