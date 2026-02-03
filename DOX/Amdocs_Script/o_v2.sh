
#!/bin/ksh

# Configuration
SUCCESS=0
FAILURE=1
EMAIL_RECIP="abhisha3@amdocs.com"
EMAIL_FROM="noreplyreports@amdocs.com"
SCRIPT_NAME="orion_outage_report"
TS=$(date +%Y%m%d%H%M%S)
LOG_FILE=${SCRIPT_NAME}_${TS}.log
HTML_FILE="orion_outage_report.html"
EXCEL_FILE="Orion_Outage_Report.xlsx"
DB_CONN="postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb"

# Time intervals
INTERVALS=("1 day" "30 days" "1 year" "3 years")
TAGS=("1d" "30d" "1y" "3y")

# Queries
QUERIES=(
"SELECT spoi.id, spoi.name, spoi.start_date, spoi.last_updated, spoi.status FROM ossdb01db.sc_project_order_instance spoi WHERE spoi.status IN ('BNOT STARTED','CDRELEASE IN PROGRESS','AHHOLD IN PROGRESS') AND spoi.last_updated >= NOW() - interval '__INTERVAL__';"
"SELECT spoi.status AS Activity_Status, COUNT(*) AS Activity_status_count FROM ossdb01db.sc_project_order_instance spoi WHERE spoi.status IN ('BNOT STARTED','CDRELEASE IN PROGRESS','AHHOLD IN PROGRESS') AND spoi.last_updated >= NOW() - interval '__INTERVAL__' GROUP BY spoi.status;"
"SELECT ord.entity_name, oai.spec_ver_id, COUNT(*) AS activity_count FROM ossdb01db.oss_activity_instance oai, ossdb01ref.oss_ref_attribute ora, ossdb01ref.oss_ref_data ord WHERE oai.part_id BETWEEN 1 AND 99 AND oai.last_update_date >= NOW() - interval '__INTERVAL__' AND oai.state IN ('In Progress', 'Rework In Progress') AND oai.is_latest_version = 1 AND oai.implementation_type <> 'Manual' AND oai.spec_ver_id = ora.attribute_value AND ora.entity_id = ord.entity_id GROUP BY ord.entity_name, oai.spec_ver_id;"
)

# Function to run a query
run_query() {
  query="$1"
  interval="$2"
  tag="$3"
  qid="$4"
  output_file="query${qid}_${tag}.html"
  final_query=$(echo "$query" | sed "s/__INTERVAL__/$interval/g")
  echo "Running Query $qid for $interval..."
  psql "$DB_CONN" -H -c "$final_query" -o "$output_file"
  return $?
}

# Run all queries for all intervals
qid=1
for query in "${QUERIES[@]}"; do
  i=0
  for interval in "${INTERVALS[@]}"; do
    run_query "$query" "$interval" "${TAGS[$i]}" "$qid" || echo "Query $qid failed for interval $interval" >> $LOG_FILE
    i=$((i+1))
  done
  qid=$((qid+1))
done

# Generate HTML + Excel using Python
python3 <<EOF
import pandas as pd
from pathlib import Path

query_names = ['Query1', 'Query2', 'Query3']
intervals = ['1d', '30d', '1y', '3y']
html_files = {q: {i: f"query{q[-1]}_{i}.html" for i in intervals} for q in query_names}

def read_html_table(file_path):
    try:
        return pd.read_html(file_path)[0]
    except:
        return pd.DataFrame()

# Excel
with pd.ExcelWriter("$EXCEL_FILE", engine='openpyxl') as writer:
    for query, files in html_files.items():
        for interval, file_path in files.items():
            df = read_html_table(file_path)
            sheet_name = f"{query}_{interval}"[:31]
            df.to_excel(writer, sheet_name=sheet_name, index=False)

# HTML
html = """
<html>
<head>
<style>
body { font-family: Arial, sans-serif; padding: 20px; }
h2 { color: #004080; }
table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
th { background-color: #004080; color: white; }
tr:nth-child(even) { background-color: #f2f2f2; }
.note { font-style: italic; color: #555; margin-bottom: 20px; }
</style>
</head>
<body>
<h2>Orion Outage Report</h2>
"""

for query, files in html_files.items():
    html += f"<h3>{query}</h3><table><tr><th>Interval</th><th>Record Count</th><th>Note</th></tr>"
    for interval, file_path in files.items():
        df = read_html_table(file_path)
        count = len(df)
        if count == 0:
            note = "✅ No outages — system is stable."
        elif count > 100:
            note = "⚠️ High number of records. Please investigate."
        else:
            note = "🔍 Some records found. Please review."
        html += f"<tr><td>{interval}</td><td>{count}</td><td>{note}</td></tr>"
    html += "</table>"

html += "</body></html>"

with open("$HTML_FILE", "w") as f:
    f.write(html)
EOF

# Send email with HTML body and Excel attachment
cat "$HTML_FILE" | mailx -a "$EXCEL_FILE" -s "Orion Outage Report" -r "$EMAIL_FROM" "$EMAIL_RECIP"

echo "Report sent successfully."
