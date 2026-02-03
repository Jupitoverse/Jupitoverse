#!/bin/ksh -x
#############################################################################
#NAME   :      To Check the Pending User task which is impacting billing and hence Rebill
#AUTHOR :      Abhishek Agrahari && Prateek Jain
#DATE   :      12/11/2024 
#DESCRIPTION:  Check User Pending Task which are impacting Billing 
#CASE   :
#############################################################################
. ./common_functions_PLAB.sh

#############################################################################
# function  : pull_data
# parameters: none
# purpose   : overview if files have been sent or not
#############################################################################


#"postgresql://${DB_USER}:${DB_PASS}@${DB_SERVER}:${DB_PORT}/${DB_INSTANCE}

#A: defines which date the query should be executed check_count

function check_count
{
#CONN_STR = "postgresql://ossdb01uams:ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb"
count=(`psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -t -c "select date_part('day',now());"`)

echo $count
}

#A: it fetches data from SQL Query pull_data

function pull_data
{
#CONN_STR = "postgresql://ossdb01uams:ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb"
typeset SqlOut
SqlOut=(`psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -H -c "select spoi.id as projectid,oas.value as customer_id ,oas2.value as site_id ,oas4.value as projectOwnerName,oas5.value as siteName ,oas6.value as PTD,o1.entity_name,spoi.name,oai.last_update_date,oai.create_date,oai.status ,spoi.status,oai.id as activity_id from ossdb01db.sc_project_order_instance spoi,ossdb01db.oss_activity_instance oai,ossdb01ref.oss_ref_data o1,ossdb01ref.oss_ref_attribute o2,ossdb01db.oss_attribute_store oas,ossdb01db.oss_attribute_store oas2 ,ossdb01db.oss_attribute_store oas4 ,ossdb01db.oss_attribute_store oas5,ossdb01db.oss_attribute_store oas6 where oai.part_id in(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33) and oai.implementation_type = 'Manual' and oai.spec_ver_id in('5bf0536f-4798-4674-b811-f0c40cd9f967','800f1e6c-a19d-4851-8c33-caf6df02e7fb','e7cd1c8f-f778-4e6d-aa2b-43240bce64d4','234487e7-7dfa-4f09-a7db-6de805f7ff23','234487e7-7dfa-4f09-a7db-6de805f7ff23','6e9c8fb9-078e-4711-baee-cd31a4dfed61','1e1f81de-aea5-4f1c-a621-8daed5a11842','93d43aae-8e7b-4950-a358-1c302bb948a6','f8dec3e6-143b-49db-b0a3-3f2362ffc20a','fa571a98-8774-45a5-9f43-d7f557385333') and oai.state in ('In Progress', 'Rework In Progress')and oai.last_update_date < current_date - interval '30' day and spoi.plan_id = oai.plan_id and spoi.manager is distinct from'ProductionSanity' and oai.is_latest_version = 1 and spoi.is_latest_version = 1 and spoi.name not like '%MM_PROD_TEST%'and spoi.status not like 'FCANCELLED' and o2.attribute_value = oai.spec_ver_id and o1.entity_id = o2.entity_id and oas.parent_id = spoi.objid and oas2.parent_id = spoi.objid and oas4.parent_id = spoi.objid and oas5.parent_id = spoi.objid and oas6.parent_id = spoi.objid and oas.code like 'customerID' and oas2.code like 'siteId' and oas4.code like 'projectOwnerName' and oas5.code like 'siteName' and oas6.code like 'DMD_PTD';" -o p.html`)



echo $SUCCESS
echo $FAILURE
if (( $? != SUCCESS ))
then
echi 'errrorrrr1'
cat <<-EOF >> $LOG_FILE
Error in function $0 at line $LINENO
$SqlOut
EOF

return $FAILURE
fi

echo 'sql part completed'


return $SUCCESS
}


function pull_data2
{
#CONN_STR = "postgresql://ossdb01uams:ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb"
typeset SqlOut
SqlOut=(`psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -H -c "select spoi.id as projectid,oas.value as customer_id ,oas2.value as site_id ,oas4.value as projectOwnerName,oas5.value as siteName ,oas6.value as PTD,o1.entity_name,spoi.name,oai.last_update_date,oai.create_date,oai.status ,spoi.status,oai.id as activity_id from ossdb01db.sc_project_order_instance spoi,ossdb01db.oss_activity_instance oai,ossdb01ref.oss_ref_data o1,ossdb01ref.oss_ref_attribute o2,ossdb01db.oss_attribute_store oas,ossdb01db.oss_attribute_store oas2 ,ossdb01db.oss_attribute_store oas4 ,ossdb01db.oss_attribute_store oas5,ossdb01db.oss_attribute_store oas6 where oai.part_id in(34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76) and oai.implementation_type = 'Manual' and oai.spec_ver_id in('5bf0536f-4798-4674-b811-f0c40cd9f967','800f1e6c-a19d-4851-8c33-caf6df02e7fb','e7cd1c8f-f778-4e6d-aa2b-43240bce64d4','234487e7-7dfa-4f09-a7db-6de805f7ff23','234487e7-7dfa-4f09-a7db-6de805f7ff23','6e9c8fb9-078e-4711-baee-cd31a4dfed61','1e1f81de-aea5-4f1c-a621-8daed5a11842','93d43aae-8e7b-4950-a358-1c302bb948a6','f8dec3e6-143b-49db-b0a3-3f2362ffc20a','fa571a98-8774-45a5-9f43-d7f557385333') and oai.state in ('In Progress', 'Rework In Progress')and oai.last_update_date < current_date - interval '30' day and spoi.plan_id = oai.plan_id and spoi.manager is distinct from'ProductionSanity' and oai.is_latest_version = 1 and spoi.is_latest_version = 1 and spoi.name not like '%MM_PROD_TEST%'and spoi.status not like 'FCANCELLED' and o2.attribute_value = oai.spec_ver_id and o1.entity_id = o2.entity_id and oas.parent_id = spoi.objid and oas2.parent_id = spoi.objid and oas4.parent_id = spoi.objid and oas5.parent_id = spoi.objid and oas6.parent_id = spoi.objid and oas.code like 'customerID' and oas2.code like 'siteId' and oas4.code like 'projectOwnerName' and oas5.code like 'siteName' and oas6.code like 'DMD_PTD';" -o q.html`)



echo $SUCCESS
echo $FAILURE
if (( $? != SUCCESS ))
then
echi 'errrorrrr1'
cat <<-EOF >> $LOG_FILE
Error in function $0 at line $LINENO
$SqlOut
EOF

return $FAILURE
fi

echo 'sql part completed'


return $SUCCESS
}

function pull_data3
{
#CONN_STR = "postgresql://ossdb01uams:ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb"
typeset SqlOut
SqlOut=(`psql "postgresql://ossdb01uams:Pr0d_ossdb01uams@oso-pstgr-rd.orion.comcast.com:6432/prodossdb" -H -c "select spoi.id as projectid,oas.value as customer_id ,oas2.value as site_id ,oas4.value as projectOwnerName,oas5.value as siteName ,oas6.value as PTD,o1.entity_name,spoi.name,oai.last_update_date,oai.create_date,oai.status ,spoi.status,oai.id as activity_id from ossdb01db.sc_project_order_instance spoi,ossdb01db.oss_activity_instance oai,ossdb01ref.oss_ref_data o1,ossdb01ref.oss_ref_attribute o2,ossdb01db.oss_attribute_store oas,ossdb01db.oss_attribute_store oas2 ,ossdb01db.oss_attribute_store oas4 ,ossdb01db.oss_attribute_store oas5,ossdb01db.oss_attribute_store oas6 where oai.part_id in(77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99)and oai.implementation_type = 'Manual' and oai.spec_ver_id in('5bf0536f-4798-4674-b811-f0c40cd9f967','800f1e6c-a19d-4851-8c33-caf6df02e7fb','e7cd1c8f-f778-4e6d-aa2b-43240bce64d4','234487e7-7dfa-4f09-a7db-6de805f7ff23','234487e7-7dfa-4f09-a7db-6de805f7ff23','6e9c8fb9-078e-4711-baee-cd31a4dfed61','1e1f81de-aea5-4f1c-a621-8daed5a11842','93d43aae-8e7b-4950-a358-1c302bb948a6','f8dec3e6-143b-49db-b0a3-3f2362ffc20a','fa571a98-8774-45a5-9f43-d7f557385333','800f1e6c-a19d-4851-8c33-caf6df02e7fb') and oai.state in ('In Progress', 'Rework In Progress')and oai.last_update_date < current_date - interval '30' day and spoi.plan_id = oai.plan_id and spoi.manager is distinct from'ProductionSanity' and oai.is_latest_version = 1 and spoi.is_latest_version = 1 and spoi.name not like '%MM_PROD_TEST%'and spoi.status not like 'FCANCELLED' and o2.attribute_value = oai.spec_ver_id and o1.entity_id = o2.entity_id and oas.parent_id = spoi.objid and oas2.parent_id = spoi.objid and oas4.parent_id = spoi.objid and oas5.parent_id = spoi.objid and oas6.parent_id = spoi.objid and oas.code like 'customerID' and oas2.code like 'siteId' and oas4.code like 'projectOwnerName' and oas5.code like 'siteName' and oas6.code like 'DMD_PTD';" -o r.html`)



echo $SUCCESS
echo $FAILURE
if (( $? != SUCCESS ))
then
echi 'errrorrrr1'
cat <<-EOF >> $LOG_FILE
Error in function $0 at line $LINENO
$SqlOut
EOF

return $FAILURE
fi

echo 'sql part completed'


return $SUCCESS
}

#############################################################################
# function  : cleanup 
# parameters: none 
# purpose   : Cleanup temp files. 
#############################################################################

#A: Cleanup old logs file

function cleanup
{

mv $LOG_FILE LOGS/ 2>/dev/null
mv $HTML_FILE LOGS/ 
return $SUCCESS

}
#############################################################################
# function  : send_html_email
# parameters: 1. Email recips
#             2. Subject
#             3. html file
# purpose   : Send html email via sendmail.
#############################################################################

#A: TO send email

function send_html_special_delivery_static_message
{
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
<h4>This is a Amdocs generated report for all the pending User task impacting Billing.Please take follow-up with respective work queue or task owner.</h4>
$(cat $HtmlFile)




EOF

return $SUCCESS

}
#############################################################################
# function  : exit_process 
# parameters: 1. Exit code. 
# purpose   : Send email with log file. 
#############################################################################
#A: sabse pahle ye chalega fir Mail wala : We are calling mail function here only
function exit_process  
{
typeset ExitCode=$1

printf "\nEnd $(date)\n" >> $LOG_FILE

case $ExitCode in

	$SUCCESS)
        send_html_special_delivery_static_message "$EMAIL_RECIP" "$EMAIL_FROM" "$HTML_FILE" "Comcast OSS Report ||User Pending Task Impacting Billing || Rebill"
		;;

	$FAILURE) 
    echo 'erorrr'
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
#EMAIL_RECIP="abhisha3@amdocs.com"
EMAIL_RECIP="abhisha3@amdocs.com,prateek.jain5@amdocs.com,anarghaarsha_alexander@comcast.com,chandradeepthi_doruvupalagiri@comcast.com,venkataraghavendrakalyan_ankem@comcast.com,sonalika_sapra2@comcast.com,joseph_thottukadavil@cable.comcast.com,Nishant.Bhatia@amdocs.com,Enna.Arora@amdocs.com,RAJIVKUM@amdocs.com,mukul.bhasin@amdocs.com,daleszandro_jasper@cable.comcast.com,Natasha.Deshpande@amdocs.com"
ERR_RECIP="abhisha3@amdocs.com"
EMAIL_FROM="noreplyreports@amdocs.com"
typeset -r APPLICATION="OSO"
 

 ##################
 
 

count=$(check_count)
#count=1
	echo $count

	if (( $count %11==0))  #frequency of receiving the alert mail
        then
        	printf " in yes There are "$count" records today in database."  >> $LOG_FILE
          pull_data
          pull_data2
          pull_data3          
          
          cat q.html >> p.html
          cat r.html >> p.html
          cat  p.html > "$HTML_FILE"     #name given to fuile where we are storing output 
          #cat te.html seq.html > "$HTML_FILE"
          #cat f.html | echo $text_disp > "$HTML_FILE" 
         
        	 (( $? != SUCCESS )) && exit_process $FAILURE
        else
        	printf "There are "$count" records today for User Pending task" >> $HTML_FILE
		printf "There are "$count" records today for User Pending task" >> $LOG_FILE
	
    cat $LOG_FILE | mailx -r $EMAIL_FROM -s "$CUSTNAME $AREA - SOM" "$EMAIL_RECIP"
    cleanup
        	exit 0
       fi #if ko close krte hai aise 


exit_process $SUCCESS
