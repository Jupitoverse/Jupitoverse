#!/bin/ksh -x
#############################################################################
#NAME   :      ORION QARM automation
#AUTHOR :      Arpan
#DATE   :     
#DESCRIPTION: 
#CASE   :
#HISTORY:
#       Created BY:Arpan  DATE:20/09/2022 CHANGE MADE
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#############################################################################
. ./common_functions_PLAB.sh






#############################################################################
# function  : cleanup 
# parameters: none 
# purpose   : Cleanup temp files. 
#############################################################################
function cleanup
{
mv $LOG_FILE OSOInspectorLogsDir/ 2>/dev/null
mv $HTML_FILE_Top10 OSOInspectorLogsDir/
mv $HTML_FILE_Top5 OSOInspectorLogsDir/
mv $CSV_FILE OSOInspectorLogsDir/

return $SUCCESS
}


function Initialcleanup
{

mv $HTML_FILE_Top10 OSOInspectorLogsDir/
mv $HTML_FILE_Top5 OSOInspectorLogsDir/
mv $CSV_FILE OSOInspectorLogsDir/

return $SUCCESS
}


#############################################################################
# function  : pull_data
# parameters: none
# purpose   : overview if files have been sent or not
#############################################################################


function CSV_AllActivityFailures_60Days
{
echo 'Query for alert is  == ': "$QUERY_STRING_AllinCSV"
typeset SqlOut
psql $CONN_STR -A -F"," -c "$QUERY_STRING_AllinCSV" -o $CSV_FILE

echo 'sql part completed for CSV'
return $SUCCESS
}


function HTMLReport_Top10
{
echo 'Query for alert is  == ': "$QUERY_STRING_Top10"


echo """
    <html>
    <head>
   
   <style>
   
   h3 {font-family:verdana;color:#7d3456;}
    h4 {font-family:verdana;color:SlateGray;background-color:powderblue;}
     h5 {font-family:verdana;color:MidnightBlue;}
      h6 {font-family:verdana;color:MidnightBlue;}
   
   table, th,td {
     border: 1px solid black;
     border-collapse: collapse;
   }
   th {
     background-color: #454545;
     color: white;
   }
   tr:nth-child(even) {
      background-color: #f2f2f2;
    }
   
   </style>
   
   </head>""" > $HTML_FILE_Top10
   
psql $CONN_STR -H -c "$QUERY_STRING_Top10" \o  >> $HTML_FILE_Top10

echo $HTML_FILE_Top10
echo 'sql part completed for HTML'

return $SUCCESS

}

function HTMLReport_Top5
{
echo 'Query for alert is  == ': "$QUERY_STRING_Top5"


echo """
    <html>
    <head>
   
   <style>
   
   h3 {font-family:verdana;color:#4d3456;}
    h4 {font-family:verdana;color:SlateGray;background-color:powderblue;}
     h5 {font-family:verdana;color:MidnightBlue;}
      h6 {font-family:verdana;color:MidnightBlue;}
   
   table, th,td {
     border: 1px solid black;
     border-collapse: collapse;
   }
   th {
     background-color: #254545;
     color: white;
   }
   tr:nth-child(even) {
      background-color: #g2g2g2;
    }
   
   </style>
   
   </head>""" > $HTML_FILE_Top5
   
psql $CONN_STR -H -c "$QUERY_STRING_Top5" \o  >> $HTML_FILE_Top5

echo $HTML_FILE_Top5
echo 'sql part completed for HTML'

return $SUCCESS

}

function email_individual_reportHTML
{







cat <<-EOF | /usr/sbin/sendmail -t 
To: $EMAIL_RECIP
From: $EMAIL_FROM
Content-type: text/html;
attachment: $CSV_FILE
Subject: Top offenders Report for $ENV - $ADOPTER - $APPLICATION - For $TDATE - with errors from last 2 months (60 Days)
$(cat $HTML_FILE_Top10)
</br>
 <hr>
 
 <h5>All failed entries can be accessed on OSO PROD database, Table : DNDAM_ACTIVITY_FAILURES_3M. These can be used in day to day jobs to find how many failures for a particual error or on activity.</h5>
 
 <h5>Report for Top 10 offenders has been loaded on OSO PROD database, Table : TEMP_ACT_FAILURE_TOP10_3M </h5>

 <h5>Error, Activity and Project Type which are ignored are maintained on OSO PROD database, Table : DNDAM_ACT_AREA_MAPPING, Filter by : IGNORABLE as YES </h5>
 
 <h5>Sample Queries that can be used : </h5>
 
 <table>
 <tr>  <i>   <h6>
select * from DNDAM_Activity_Failures_3M; 
</h6> </i> </tr> 

 <tr>  <i>   <h6>
select * from DNDAM_Activity_Failures_3M where activity_name  like 'Update with Request Status' and description  like '%Man%'; 

</h6> </i> </tr> 

 <tr>  <i>   <h6>
select * from DNDAM_Activity_Failures_3M where  type in ('Equipment_Modify','Equipment_(Provide)','Equipment_Disconnect') ;
</h6> </i> </tr> 

 <tr>  <i>   <h6>
select distinct f.*, xl.request,xl.response from DNDAM_Activity_Failures_3M f 
left join x_logging xl on f.activity_id = xl.sub_key_value where 
1=1
and f.activity_name like '%Create Agreement%' 
and description like  '%Mandatory attribute is missing%'
and xl.request like '%Enterprise%'; 
</h6> </i> </tr> 
 </table>
<footer>
  <h7><p>For Information/Doubts Contact Prateek/Divyesh</p><h7>
  <h7><p><a href="mailto:jprateek@amdocs.com">jprateek@amdocs.com</a></p><h7>
</footer>

EOF










echo 'mail sent success'

#cat $LOG_FILE | mailx -s "FAILURE - $AREA $CLIENT $SCRIPT_NAME" "$ERR_RECIP"
#cleanup

return $SUCCESS


cleanup
}


#############################################################################
# function  : main 
# parameters: none 
# purpose   : Setup globals, call functions. 
#############################################################################
# main()

typeset -r ADOPTER='ORION'
typeset -r ENV='PROD'
typeset -r TDATE=$(date --date="today" +"%m/%d/%Y")
typeset -r TDATE2=$(date --date="today" +"%m-%d-%Y")
typeset -r APPLICATION='OSO'
typeset -r EMAIL_FROM='inspector@orion.amdocs.com'
typeset -r EMAIL_RECIP='prateek.jain5@amdocs.com,ComcastOssOneOperations@amdocs.com,ICMComcastMMIncubationTeam@amdocs.com'

 
typeset hdrtxt='Sample Mail Variable' 

echo "=============RICO [Richard Koch Principle based utility- " $ENV " - " $ADOPTER " For " $TDATE" ] Starting ============" 

Initialcleanup



HTML_FILE_Top10="OSOInspector_ActivityFailures_60days_Top10.html"
HTML_FILE_Top5="OSOInspector_ActivityFailures_60days_Top5.html"
CSV_FILE="ActivityFailures_60Days_OSO_$TDATE2.csv"

Initialcleanup

typeset -r CONN_STR=$(awk '{ if(/^RWOSO/) { print $2 } }' ogs_db_connect.dat)

set +f
GLOBIGNORE=*



MAIN_QUERY_DROPI="drop table if exists DNDAM_Activity_Failures_3MI"

MAIN_QUERY_CREATEI="create table DNDAM_Activity_Failures_3MI as with act_data as (select ord.entity_name, ora.attribute_value, ord.payload  from ossdb01ref.oss_ref_data ord,  ossdb01ref.OSS_REF_ATTRIBUTE ora where ord.entity_id = ora .entity_id and ora.attribute_name  = 'versionID') select oai.id activity_id,oai.plan_id plan,ad.entity_name activity_name, oai.spec_ver_id ,oai.operation , oai.last_update_date, State,  oai.error_id,er.code ,er.description,poi.Id project_id,poi.type,poi.name, poi.objid poiobjid,poi.status projStatus from ossdb01db.OSS_ACTIVITY_INSTANCE oai left join ossdb01db.OSS_ERROR er on  er.ID = oai.error_id join act_data ad on oai.spec_ver_id =ad.attribute_value join  ossdb01db.SC_PROJECT_ORDER_INSTANCE poi on poi.Plan_id = oai.plan_id and poi.status not in ('FCANCELLED','DCOMPLETED','ECANCEL IN PROGRESS') and poi.manager is distinct from 'ProductionSanity' and upper(name) not like '%_TEST%' where   oai.state = 'In Error' and poi.is_latest_version = 1 and oai.last_update_date >now () - interval '60 DAYS' order by er.code,er.description, poi.type;"


MAIN_QUERY_DROP="drop table if exists DNDAM_Activity_Failures_3M"

MAIN_QUERY_CREATE="create table DNDAM_Activity_Failures_3M as Select ts.*, oas.value as CID, da.customer_name as CNAME from DNDAM_Activity_Failures_3MI ts left join oss_attribute_store oas  on ts.poiobjid = oas.parent_id and oas.code = 'customerID' left join DD_AGREEMENT da on da.customer_id = oas.value and da.is_latest=1 where (upper(customer_name) not like '%_TEST%' and upper(customer_name) not like '%_PROD%');"

DROP_TOP5="drop table if exists temp_Act_Failure_Top5" 

CREATE_TOP5="create table temp_Act_Failure_Top5 as (select count(*), Activity_name,Spec_ver_id, code as Error_code, type as Project_Type from DNDAM_Activity_Failures_3M group by Activity_name,code, type,Spec_ver_id order by count(*) desc limit 5 )"


DROP_TOP10="drop table if exists temp_Act_Failure_Top10" 

CREATE_TOP10="create table temp_Act_Failure_Top10 as (select count(*),mt.Activity_name,mt.Spec_ver_id, mt.code as Error_code, mt.type as Project_Type from DNDAM_Activity_Failures_3M mt where NOT exists (Select 1 from dndam_act_area_mapping et where mt.activity_name=et.activity_name and mt.code =et.failure_code and mt.type =et.profile_type and et.ignorable='YES') group by Activity_name,code, type,Spec_ver_id order by count(*) desc limit 10);"


GRANT_QUERY1="GRANT ALL on ossdb01db.DNDAM_Activity_Failures_3M to ossdb01uams"
GRANT_QUERY2="GRANT ALL on ossdb01db.temp_Act_Failure_Top5 to ossdb01uams"
GRANT_QUERY3="GRANT ALL on ossdb01db.temp_Act_Failure_Top10 to ossdb01uams"
GRANT_QUERY4="GRANT ALL on ossdb01db.dndam_act_area_mapping to ossdb01uams"
#Execution

psql $CONN_STR -At -c "$MAIN_QUERY_DROPI" 

sleep 3

psql $CONN_STR -At -c "$MAIN_QUERY_CREATEI" 

echo 'Completed Intermediate Module'
psql $CONN_STR -At -c "$MAIN_QUERY_DROP" 

sleep 3

psql $CONN_STR -At -c "$MAIN_QUERY_CREATE" 

psql $CONN_STR -At -c "$GRANT_QUERY1" 


echo 'Completed First Module'

psql $CONN_STR -At -c "$DROP_TOP5" 

sleep 3

psql $CONN_STR -At -c "$CREATE_TOP5" 

echo 'Completed Second Module'

psql $CONN_STR -At -c "$DROP_TOP10" 

sleep 3

psql $CONN_STR -At -c "$CREATE_TOP10"

psql $CONN_STR -At -c "$GRANT_QUERY2" 
psql $CONN_STR -At -c "$GRANT_QUERY3" 
psql $CONN_STR -At -c "$GRANT_QUERY4" 

#Reports
 
QUERY_STRING_Top10="Select * from temp_Act_Failure_Top10"
QUERY_STRING_Top5="Select * from temp_Act_Failure_Top5"
QUERY_STRING_AllinCSV="Select * from DNDAM_Activity_Failures_3M"


CSV_AllActivityFailures_60Days

HTMLReport_Top10

HTMLReport_Top5

email_individual_reportHTML


echo 'Completed Report Creations'

