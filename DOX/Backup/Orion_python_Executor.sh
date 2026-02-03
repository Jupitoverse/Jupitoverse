#!/bin/ksh

#############################################################################
# NAME   : Orion Outage Report Generator
# AUTHOR : Abhishek Agrahari
# DATE   : 05/30/2025
# DESCRIPTION: Generates a 24-hour outage impact report and emails it as HTML
#############################################################################

#!/bin/bash

# Shell script to execute multiple Python scripts

# Define paths to Python scripts
SCRIPT1="/fs_ogs/operogs/scriptbin/ogs_monitors/Jupitoverse/outage_Report.py"
#SCRIPT2="/fs_ogs/operogs/scriptbin/ogs_monitors/Jupitoverse/another_script.py"
#SCRIPT3="/fs_ogs/operogs/scriptbin/ogs_monitors/Jupitoverse/third_script.py"

# Execute each script
echo "Executing: $SCRIPT1"
python3 "$SCRIPT1"

#echo "Executing: $SCRIPT2"
#python3 "$SCRIPT2"

#echo "Executing: $SCRIPT3"
#python3 "$SCRIPT3"

# Log execution time
echo "All scripts executed at: $(date)"


exit $SUCCESS
