
#!/bin/ksh -x
#############################################################################
#NAME   :     To generate the report of pending user tasks
#DESCRIPTION: Pulls data from PostgreSQL in 3 parts, sends HTML email and Excel attachment
#############################################################################

. ./common_functions_PLAB.sh

SUCCESS=0
FAILURE=1

function check_count {
  count=(`psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -t -c "select date_part('day',now());"`)
  echo $count
}

function pull_data {
  psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -H -f query1.sql -o p.html
  (( $? != SUCCESS )) && return $FAILURE
  return $SUCCESS
}

function pull_data2 {
  psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -H -f query2.sql -o q.html
  (( $? != SUCCESS )) && return $FAILURE
  return $SUCCESS
}

function pull_data3 {
  psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -H -f query3.sql -o r.html
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
    echo "<h4>This is a Amdocs generated report for all the pending User task impacting Billing.</h4>"
    cat "$HtmlFile"
    echo "</body></html>"
  } | /usr/sbin/sendmail -t

  # Attach Excel file
  uuencode user_pending_tasks.xlsx user_pending_tasks.xlsx | mailx -s "$Subject" -r "$From" "$Recips"
}

function exit_process {
  typeset ExitCode=$1
  printf "\nEnd $(date)\n" >> $LOG_FILE

  case $ExitCode in
    $SUCCESS)
      send_html_special_delivery_static_message "$EMAIL_RECIP" "$EMAIL_FROM" "$HTML_FILE" "Report: Orion User Pending Task Impacting Billing"
      ;;
    $FAILURE)
      cat $LOG_FILE | mailx -s "FAILURE - $AREA $CLIENT $SCRIPT_NAME" "$ERR_RECIP"
      ;;
  esac
  cleanup
  exit $ExitCode
}

# Main
typeset -r LOG_FILE=${SCRIPT_NAME}_${TS}.log
typeset -r HTML_FILE=${SCRIPT_NAME}_${TS}.html
typeset -r TDATE=$(date --date="today" +"%m/%d/%Y")
typeset -r EMAIL_RECIP="abhisha3@amdocs.com"
typeset -r ERR_RECIP="abhisha3@amdocs.com"
typeset -r EMAIL_FROM="noreplyreports@amdocs.com"

count=$(check_count)
echo $count

if (( $count %6 == 0 ))
then
  printf "There are $count records today in database.\n" >> $LOG_FILE

  pull_data || exit_process $FAILURE
  pull_data2 || exit_process $FAILURE
  pull_data3 || exit_process $FAILURE

  cat q.html >> p.html
  cat r.html >> p.html
  cat p.html > "$HTML_FILE"

  # Generate Excel file
  python3 <<EOF
import pandas as pd

def safe_read(file):
    try:
        return pd.read_html(file)[0]
    except:
        return pd.DataFrame()

df1 = safe_read("p.html")
df2 = safe_read("q.html")
df3 = safe_read("r.html")

with pd.ExcelWriter("user_pending_tasks.xlsx", engine="openpyxl") as writer:
    df1.to_excel(writer, sheet_name="Part1", index=False)
    df2.to_excel(writer, sheet_name="Part2", index=False)
    df3.to_excel(writer, sheet_name="Part3", index=False)
EOF

  (( $? != SUCCESS )) && exit_process $FAILURE
else
  printf "There are $count records today for User Pending task\n" >> $LOG_FILE
  cat $LOG_FILE | mailx -r $EMAIL_FROM -s "$CUSTNAME $AREA - SOM" "$EMAIL_RECIP"
  cleanup
  exit 0
fi

exit_process $SUCCESS
