#!/bin/ksh -x
#############################################################################
#NAME   :      checkBiWeeklySyncBillRun
#AUTHOR :      Sonali C
#DATE   :      03/31/2021 
#DESCRIPTION:  checkBiWeeklySyncBillRun
#CASE   :
#HISTORY:
#       CHANGED BY: DATE: CHANGE MADE
#----------------------------------------------------------------------------
#----------------------------------------------------------------------------
#############################################################################
. common_functions

#############################################################################
# function  : pull_data
# parameters: none
# purpose   : overview if files have been sent or not
#############################################################################


###Price Mismatch & Pending Fulfilment 

CONN_CPQ=CMMSEL/CMM4SEL@CMMCPQ1
CONN_OMS=CMMOMS/cmm_4c0nn@cmmoms1
CONN_ABP=CMMAPPC/cmm_4c0nn@CMMCM1

export ORACLE_BIN32=/oravl01/oracle/12.1.0/bin
export ORACLE_BIN64=/oravl01/oracle/12.1.0/bin
export ORACLE_HOME=/oravl01/oracle/12.1.0
export ORACLE_HOME_32=/oravl01/oracle/12.1.0
export ORACLE_HOME_BEFORE_TWA=/oravl01/oracle/12.1.0
export ORACLE_LIB32=/oravl01/oracle/12.1.0/lib
export ORACLE_LIB64=/oravl01/oracle/12.1.0/lib



#####ABP pull to get the last bill run date#####

function check_lastbillrundate
{
BDATE=$(sqlplus -s $CONN_STR_ABP <<END
       set pagesize 0 feedback off verify off heading off echo off;
select TO_CHAR(run_date ,'YYYYMMDD') from bl1_cycle_control where cycle_code='${CYCLE}' and  trunc(run_date)>=trunc(sysdate-30)
and run_date is not null;
exit;
END
)
echo $BDATE
}

####ABP pull to get the cycle sequence#####
function check_cycle_seq
{
CSEQ=$(sqlplus -s $CONN_STR_ABP <<END
       set pagesize 0 feedback off verify off heading off echo off;
select LTRIM(RTRIM(CYCLE_INSTANCE)) from bl1_cycle_control where cycle_code='${CYCLE}' and TO_CHAR(start_date ,'YYYYMMDD')='${BDATE}'
and status <> 'CN';

exit;
END
)
echo $CSEQ
}

##to find sysdate-1
function check_previous_day
{
PREVIOUS_DATE=$(sqlplus -s $CONN_STR_ABP <<END
       set pagesize 0 feedback off verify off heading off echo off;
select to_char(sysdate-1,'MM/DD/YYYY') from dual;

exit;
END
)
echo $PREVIOUS_DATE
}

function check_logical_date
{
LOGICAL_DAY=$(sqlplus -s $CONN_STR_ABP <<END
       set pagesize 0 feedback off verify off heading off echo off;
select to_char(logical_date,'DD') from logical_date where expiration_date is null and LOGICAL_DATE_TYPE='B';

exit;
END
)
echo $LOGICAL_DAY
}

function check_logical_month
{
LOGICAL_MONTH=$(sqlplus -s $CONN_STR_ABP <<END
       set pagesize 0 feedback off verify off heading off echo off;
select to_char(logical_date,'MM') from logical_date where expiration_date is null and LOGICAL_DATE_TYPE='B';

exit;
END
)
echo $LOGICAL_MONTH
}

function check_logical_date_year
{
LOGICAL_YEAR=$(sqlplus -s $CONN_STR_ABP <<END
       set pagesize 0 feedback off verify off heading off echo off;
select to_char(logical_date,'YY') from logical_date where expiration_date is null and LOGICAL_DATE_TYPE='B';

exit;
END
)
echo $LOGICAL_YEAR
}


function last_date_of_cycle
{
LAST_DATE=$(sqlplus -s $CONN_STR_ABP <<END
       set pagesize 0 feedback off verify off heading off echo off;
select to_char(to_date('${BILL_DATE}','DD-MM-YY')-1,'YYYYMMDD') from dual;

exit;
END
)
echo $LAST_DATE
}


echo "Function Started" >> $LOG_FILE
#####ABP#####
function pull_data_ABP

{

typeset SqlOut
SqlOut=$(sqlplus -s $CONN_STR_ABP << EOF
$DEF_SQL_OFF_WH
set serveroutput on
set wrap on
set tab off
set trimspool on
set pagesize 50000


--whenever sqlerror exit sql.sqlcode;

alter session set nls_date_format = 'DD-MON-YY HH24:MI:SS';

--ABP SYNC
drop table temp_rebill_data;

create table temp_rebill_data as select to_date('${BILL_DATE}','DD-MM-YY')-a.start_date as diff,b.customer_id,a.start_date, a.end_date,a.issue_date,c.subscriber_no,c.prim_resource_val as service_id, c.l9_site_name, c.l9_site_id, c.SYS_CREATION_DATE,c.SYS_UPDATE_DATE,b.l9_legal_name as customer_name from bl1_technical_mark a,customer b, subscriber c where status='PN' and a.entity_id=b.customer_id and a.entity_id=c.customer_id and ((to_char(a.issue_date,'MM/DD/YYYY')=to_char(c.sys_update_date,'MM/DD/YYYY')) or (to_char(a.issue_date,'MM/DD/YYYY')=to_char(c.sys_creation_date,'MM/DD/YYYY'))) and bill_cycle='${CYCLE}' and to_date('${BILL_DATE}','DD-MM-YY')-start_date>32 order by diff desc;

drop table temp_rebill_data_imm;
create table temp_rebill_data_imm as select a.* ,b.ATTR1VALUE, b.memo_system_text from  temp_rebill_data a, mo1_memo b where a.subscriber_no=b.entity_id and trunc(a.issue_date)=trunc(b.memo_date) and ATTR1VALUE in ('OMS','ABPBatchUser') order by l9_site_id;
drop table rebill_data_imm_1;
CREATE TABLE rebill_data_imm_1 AS SELECT diff, customer_id, start_date, end_date, issue_date, subscriber_no,        service_id, l9_site_id, l9_site_name, customer_name, attr1value,        XMLAGG(XMLELEMENT(E, memo_system_text||chr(10))).GetClobVal()|| chr(10) AS activities FROM temp_rebill_data_imm GROUP BY diff, customer_id, start_date, end_date, issue_date, subscriber_no,          service_id, l9_site_id, l9_site_name, customer_name, attr1value          order by diff desc;

drop table REBILL_DATA_IMM_2;
create table REBILL_DATA_IMM_2 as
select a.*, 
case 
when  a.activities like '%Subscriber Activated%' then 'Subscriber Activated'
when a.activities like '%Subscriber canceled%' then 'Subscriber ceased'
else 'Update Parameter'
end as activity,
case 
when  a.activities like '%Subscriber Activated%' then (select init_act_date from subscriber where subscriber_no=a.subscriber_no)
when a.activities like '%Subscriber canceled%' then (select sub_status_date from subscriber where subscriber_no=a.subscriber_no)
else (select backdating_date from bl1_backdate_requests where entity_id=a.subscriber_no and trunc(sys_creation_date)=trunc(a.issue_date))
end as billing_date,
case
when  a.activities like '%Subscriber Activated%' then 'NB call came on '||a.issue_Date||' to activate the '||a.service_id||' subscriber with the date of '||(select init_act_date from subscriber where subscriber_no=a.subscriber_no)
when  a.activities like '%Subscriber canceled%' then 'NB call came on '||a.issue_Date||' to cease the '||a.service_id||' subscriber with the date of '||(select sub_status_date from subscriber where subscriber_no=a.subscriber_no)
else 'UpdateParameter call came on '||a.issue_Date||' to update parameters of '||a.service_id||' subscriber with the date of '||(select backdating_date from bl1_backdate_requests where entity_id=a.subscriber_no and trunc(sys_creation_date)=trunc(a.issue_date))
end as billing_comments
from rebill_data_imm_1 a;
drop table REBILL_DATA_IMM_3;
create table REBILL_DATA_IMM_3 as
select a.* from REBILL_DATA_IMM_2 a where trunc(issue_date)-trunc(billing_date) >45 and billing_date is not null ;
drop table temp_rebill_data_final;
create table temp_rebill_data_final as select diff,customer_id, start_date,end_date ,issue_date,listagg(subscriber_no,' ') within group (order by subscriber_no) as subscriber_num, listagg(service_id,' ') within group(order by subscriber_no) as service_id ,l9_site_id,l9_site_name,customer_name ,attr1value, listagg(BILLING_COMMENTS,chr(10)) within group(order by subscriber_no) as BILLING_COMMENTS from REBILL_DATA_IMM_3 group by customer_id, diff,start_date,end_date,l9_site_id,l9_site_name ,issue_date,customer_name, attr1value order by diff desc;

---------------------------------
SET MARKUP HTML ON SPOOL ON PREFORMAT OFF ENTMAP ON -
HEAD "<TITLE>Report</TITLE> -
<STYLE type='text/css'> -
<!-- BODY {background: WHITE;} -
td {text-align: left; align:left;} -
th {text-align: left; align:left;} -
table { -
  width: 0%; align: left; -
}--> -
</STYLE>" -
BODY "TEXT='BLACK'" -
TABLE ""

spool $HTML_FILE_5
select * from temp_rebill_data_final order by issue_date;
spool off;

set markup html off

spool checkbiweeklysyncraw.txt;


--select 'ABP_SYNC',',',count(*) from abp_sync_data;
select 'REBILL',',',count(*) from temp_rebill_data_final;
------select 'Base_Promo_Mismatch',',',count(*) from base_and_promo_mismatch_data;
------select 'CM_INV_Mismatch_NRR',',',count(*) from cancel_cm_active_inv;
---select 'Over_Promotion',',',count(*) from over_promotion_data;
spool off;


exit

EOF)

if (( $? != SUCCESS ))
then
cat <<-EOF>> $LOG_FILE
Error in function $0 at line $LINENO
$SqlOut
EOF

return $FAILURE
fi

echo 'sql part completed'
echo "SQL Completed" >> $LOG_FILE

return $SUCCESS


}

#############################################################################
# function  : cleanup 
# parameters: none 
# purpose   : Cleanup temp files. 
#############################################################################
function cleanup
{
#mv $HTML_FILE LOGS/ 2>/dev/null
mv $LOG_FILE LOGS/ 2>/dev/null
mv $HTML_FILE_1 LOGS/ 2>/dev/null
mv $HTML_FILE_2 LOGS/ 2>/dev/null
mv $HTML_FILE_3 LOGS/ 2>/dev/null
mv $HTML_FILE_0 LOGS/ 2>/dev/null
mv $HTML_FILE_4 LOGS/ 2>/dev/null
mv $HTML_FILE_5 LOGS/ 2>/dev/null
mv $HTML_FILE_7 LOGS/ 2>/dev/null
mv $HTML_FILE_8 LOGS/ 2>/dev/null
mv $HTML_FILE_9 LOGS/ 2>/dev/null
mv $HTML_FILE_10 LOGS/ 2>/dev/null

rm -f $HTML_FILE
rm -f checkbiweeklysyncraw.txt 
rm -f checkbiweeklysync.txt
return $SUCCESS
}

#######################
#####Prepare report####
#######################
get_report(){
HTML_FILE=report_${TS}.html
cat  checkbiweeklysyncraw.txt| sed -e "s/-,//" -e "s/[- ]//g" | grep -v "^$" | grep -v "COUNT" > checkbiweeklysync.txt
echo "<p>" 

echo "<head>"  >> $HTML_FILE
echo "<style>"  >> $HTML_FILE
echo "td {text-align: left; border: 1px solid #dddddd;}"  >> $HTML_FILE
echo "th {text-align: left; border: 1px solid #dddddd;}"  >> $HTML_FILE
echo "table {text-align: left; width:0%;  border-collapse: collapse;}"  >> $HTML_FILE
echo "</style>" >> $HTML_FILE
echo "</head>" >> $HTML_FILE


#echo "<h3><a name=Totals><span style='mso-fareast-font-family:"Times New Roman"'>Report
#Summary:</span></a><span style='mso-fareast-font-family:"Times New Roman"'></span></h3>" >> $HTML_FILE
#echo "<table>"    >> $HTML_FILE
#echo "<tr>" >> $HTML_FILE
#echo "<th scope=\"col\">"    >> $HTML_FILE
#echo "SCRIPT_NAME"    >> $HTML_FILE
#GS/ 2>/dev/null

#echo "</th>"  >> $HTML_FILE
#echo "<th scope=\"col\">"    >> $HTML_FILE
#echo "COUNT"    >> $HTML_FILE
#echo "</th>"    >> $HTML_FILE
#echo "</tr>"    >> $HTML_FILE


#for line in `cat checkbiweeklysync.txt`
#do
#scr_name=`echo $line | cut -d ',' -f 1`
#cnt=`echo $line | cut -d ',' -f 2`
#echo "<tr text-align=\"left\"> <td text-align=\"left\"> <a href=\"#${scr_name}\">$scr_name</a> </td> <td text-align=\"left\"> ${cnt} </td> </tr>"  >> $HTML_FILE
#done
#echo "</table>" >> $HTML_FILE

#echo "<br/> <br/>" >> $HTML_FILE

for line in `cat checkbiweeklysync.txt`
do
scr_name=`echo $line | cut -d ',' -f 1`
echo "<br\\><br\\> <h3><font color=darkred><a name=\"${scr_name}\">$scr_name</a></font></h3>(<a href="#Totals">back</a>) " >> $HTML_FILE
scr_html_filen=`ls -tr ${scr_name}*.html | tail -1`
if [ ! -z $scr_html_filen ]
then
 grep -v "<p>" ${scr_html_filen} >> $HTML_FILE
fi
done
echo "</p>" >> $HTML_FILE


}


function send_html_email
{
typeset Recips=$1
#typeset Subject=$4
typeset Subject="Rebill Analysis $MONTH $CYCLE"
typeset HtmlFile=$3
typeset From=$EMAIL_FROM

cat <<-EOF | /usr/sbin/sendmail -t
To: $Recips
From: $From
Content-type: text/html;
Subject: $Subject

$(css_only)
$(cat $HtmlFile)
EOF

return $SUCCESS

}


#############################################################################
# function  : exit_process 
# parameters: 1. Exit code. 
# purpose   : Send email with log file. 
#############################################################################
function exit_process
{
typeset ExitCode=$1

printf "\nEnd $(date)\n" >> $LOG_FILE

case $ExitCode in

	$SUCCESS)
		send_html_email "$EMAIL_RECIP" "$EMAIL_FROM" "$HTML_FILE" "$CUSTNAME $AREA -Rebill analysis" 
		;;

	$FAILURE) 

		cat $LOG_FILE | mailx -s "FAILURE - $AREA $CLIENT $SCRIPT_NAME" "$ERR_RECIP"
		;;
esac

cleanup
exit $ExitCode

}

#############################################################################
# function  : main 
# parameters: none 
# purpose   : Setup globals, call functions. 
#############################################################################
# main()
typeset -r LOG_FILE=${SCRIPT_NAME}_${TS}.log
echo "1"
#typeset -r HTML_FILE_0=Price_mismatch${TS}.html
#typeset -r HTML_FILE_1=Offer_Missing_NRC${TS}.html
#typeset -r HTML_FILE_2=EBILL${TS}.html
#typeset -r HTML_FILE_3=Subscriber_Missing${TS}.html
echo "2" >> $LOG_FILE
#typeset -r HTML_FILE_4=ABP_SYNC${TS}.html
echo "3" >> $LOG_FILE
typeset -r HTML_FILE_5=REBILL${TS}.html
#typeset -r HTML_FILE_6=Offer_Missing_MRC${TS}.html
#typeset -r HTML_FILE_7=NRC_price_mismatch${TS}.html
#typeset -r HTML_FILE_8=Base_Promo_Mismatch${TS}.html
#typeset -r HTML_FILE_9=CM_INV_Mismatch_NRR${TS}.html
#typeset -r HTML_FILE_10=Over_Promotion${TS}.html
typeset -r CONN_STR=CMMSEL/CMM4SEL@CMMCPQ1
typeset -r CONN_STR_ABP=CMMAPPC/Cmm_4c0nn@cmmcm1
typeset -r CONN_STR_ODO=CMMSOMAFFC/Cmm_4c0nn@CMMSOM1
typeset -r CONN_STR_EP=CMMEPC/Cmm_4c0nn@CMMEP1
typeset -r CONN_STR_USG1=CMMUSG1C/cmm_4c0nn@CMMUSG1
typeset -r TDATE=$(date --date="today" +"%y%m%d")
typeset -r HDATE=$(date --date="today" +"%H")
typeset -r TRANSDATE=$(date | awk '{print $3}')
typeset -r TDAY=$(date --date="today" +"%d")
#typeset TDAY='20'
typeset NMONTH=$(date --date="today" +"%m")
typeset NYEAR=$(date --date="today" +"%y")
typeset NDAY=$(date --date="today" +"%d")
typeset NYEAR_4=$(date --date="today" +"%Y")
typeset -r CDATE=$(date +%a)

echo "4" >> $LOG_FILE
#CDATE=Mon
#typeset -r TRANSDAY='22'
#typeset -r EOMMDAY='01'
typeset -r CSS=$(cat trans_billing_midmarket_css_m.dat)
EMAIL_RECIP="anishaji@amdocs.com Abhishek.Bajpai@amdocs.com"
#"pratibha.porwal@amdocs.com anishaji@amdocs.com Abhishek.Bajpai@amdocs.com Chanda.Kapdoskar@amdocs.com sirish.katragadda@amdocs.com sandeep.singh@amdocs.com Saurabh.Mehta1@amdocs.com "
#EMAIL_RECIP="sadhana.kumari@amdocs.com"
ERR_RECIP="pratibha.porwal@amdocs.com anishaji@amdocs.com"
EMAIL_FROM="noreplyreports@amdocs.com"
echo "5" $LOG_FILE
printf "Start $(date)\n\n" >> $LOG_FILE
#typeset -r TODAY=$(date --date="today" +"%d")
echo $TDAY
echo "MAIL Recipients : $EMAIL_RECIP " 
#############DEBUG
echo $TDATE
#CYCLE=$1
TDATE_N="$NMONTH/$NDAY/$NYEAR_4";
TDATE_NEW="$NYEAR_4$NMONTH$NDAY";

#touch logs/CM_Billing_RC_OC_mismatch_recon.run.$$

check_logical_date
echo "After Logical Date" >> $LOG_FILE
#runCPQ
#runOMS
#runABP

########checking for days to run########

if (($TDAY==2 ||$TDAY==3 || $TDAY==4 || $TDAY==5 || $TDAY ==6 || $TDAY==7 || $TDAY == 8 || $TDAY == 9 ||$TDAY == 10 || $TDAY == 11 || $TDAY == 12 || $TDAY == 13 || $TDAY == 14 || $TDAY==15||$TDAY==16||$TDAY==17||$TDAY==18||$TDAY==19||$TDAY==20||$TDAY==21||$TDAY == 22 || $TDAY == 23 ||$TDAY == 24 || $TDAY == 25 || $TDAY == 26 || $TDAY == 27 || $TDAY == 28 || $TDAY == 29 || $TDAY == 30 || $TDAY == 31|| $TDAY == 1 ))
then

	if (( $TDAY==2|| $TDAY ==3 || $TDAY==4||$TDAY==5|| $TDAY == 6 || $TDAY==7 || $TDAY == 8 || $TDAY == 9 ||$TDAY == 10 || $TDAY == 11 || $TDAY == 12 || $TDAY == 13 || $TDAY == 14 ||$TDAY==1))
	then
		CYCLE=115
                NDAY=15
		#LDAY=14
		#LMONTH=$NMONTH
		#LYEAR=$NYEAR_4
		BILL_DATE="$NDAY-$NMONTH-$NYEAR"
		BILL_DATE_N="$NMONTH/$NDAY/$NYEAR_4"
		#LAST_DATE="$LYEAR$LMONTH$LDAY"
		echo $CYCLE>> $LOG_FILE
		echo $BILL_DATE>>$LOG_FILE
		echo $LAST_DATE>>$LOG_FILE
		echo $NYEAR_4>>$LOG_FILE 

	else
		CYCLE=101
		NDAY=01
		if(($NMONTH==12)) then
		NMONTH=01
		NYEAR=$((NYEAR+1))
		NYEAR_4=$((NYEAR_4+1))
		else
		NMONTH=$((NMONTH+1))
		fi
		printf -v NMONTH "%02d" $NMONTH
		printf -v NYEAR "%02d" $NYEAR
		BILL_DATE="$NDAY-$NMONTH-$NYEAR"
		BILL_DATE_N="$NMONTH/$NDAY/$NYEAR_4"
		
		#to find last date ofupcoming bill run
		#if(($NMONTH==01)) then
		#	LMONTH=12
		#	LYEAR=$((NYEAR_4-1))
		#else
		#	LMONTH=$((NMONTH-1))
		#	LYEAR=$NYEAR_4 
		#fi
		

		#if(($NMONTH==01 || $NMONTH==03 || $NMONTH==05 || $NMONTH==07 || $NMONTH==08 || $NMONTH==10 ||$NMONTH==12 )) then

		#LDAY=31  #last day of current cycle
		#elif (($NMONTH==02)) then
		#LDAY=28
		#	if(($NYEAR%4==0 && $NYEAR%100!=0)) then
		#		LDAY=29
		#	elif (($NYEAR%4==0 && $NYEAR%400==0)) then
		#		LDAY=29
		#	else LDAY=28
		#	fi
		#

		#else
		#LDArY=30
		#fi
		#printf -v LDAY "%02d" $LDAY
		#printf -v LMONTH "%02d" $LMONTH
		#printf -v LYEAR "%02d" $LYEAR
		#LAST_DATE="$LYEAR$LMONTH$LDAY"
		echo $CYCLE>> $LOG_FILE
		echo $BILL_DATE>> $LOG_FILE
		#echo $LAST_DATE>>$LOG_FILE

	fi
	last_date_of_cycle
	echo $LAST_DATE>>$LOG_FILE
        echo " Today is " $TDAY "of month" , script will run.>> $LOG_FILE
        #pull_data_CPQ
	#(( $? != SUCCESS )) && exit_process $FAILURE
	check_lastbillrundate
	(( $? != SUCCESS )) && exit_process $FAILURE
	check_previous_day
        (( $? != SUCCESS )) && exit_process $FAILURE
	#check_upcoming_bill_run_date
	#(( $? != SUCCESS )) && exit_process $FAILURE
	pull_data_ABP
	echo "Calling Pull_data" >> $LOG_FILE
	(( $? != SUCCESS )) && exit_process $FAILURE
	echo "After Pull_data" >> $LOG_FILE
	#echo $BILL_DATE>> $LOG_FILE
	#pull_data_ODO
	#(( $? != SUCCESS )) && exit_process $FAILURE
	check_cycle_seq
	(( $? != SUCCESS )) && exit_process $FAILURE
	#pull_data_EP
	#(( $? != SUCCESS )) && exit_process $FAILURE
	#pull_data_USG1
	#(( $? != SUCCESS )) && exit_process $FAILURE
	get_report
else
        echo "Runs on all days" >>$LOG_FILE
        cleanup
        exit 0
fi


exit_process $SUCCESS
                     
