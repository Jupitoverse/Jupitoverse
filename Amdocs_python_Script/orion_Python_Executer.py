#!/bin/ksh

#############################################################################
# NAME   : Orion Python Script Executor
# AUTHOR : Abhishek Agrahari
# DATE   : 05/30/2025
# DESCRIPTION: Simple script executor with individual scheduling per script
#############################################################################

#!/bin/bash

#############################################################################
# CONFIGURATION - MODIFY THESE VARIABLES AS NEEDED
#############################################################################

# Delay between scripts (in minutes)
DELAY_MINUTES=5

# Script 1 Configuration
SCRIPT1_ENABLED="true"                    # true/false
SCRIPT1_SCHEDULE="5"                      # For DATE: number (5 = 5,10,15,20,25,30) | For DAY: MON,TUE,WED,THU,FRI,SAT,SUN
SCRIPT1_PATH="/fs_ogs/operogs/scriptbin/ogs_monitors/Jupitoverse/outage_Report.py"

# Script 2 Configuration  
SCRIPT2_ENABLED="false"                   # true/false
SCRIPT2_SCHEDULE="MON"                    # For DATE: number (1 = 1,11,21,31) | For DAY: MON,TUE,WED,THU,FRI,SAT,SUN
SCRIPT2_PATH="/fs_ogs/operogs/scriptbin/ogs_monitors/Jupitoverse/script2.py"

# Script 3 Configuration
SCRIPT3_ENABLED="false"                   # true/false
SCRIPT3_SCHEDULE="15"                     # For DATE: number (15 = 15,30) | For DAY: MON,TUE,WED,THU,FRI,SAT,SUN
SCRIPT3_PATH="/fs_ogs/operogs/scriptbin/ogs_monitors/Jupitoverse/script3.py"

# Script 4 Configuration
SCRIPT4_ENABLED="false"                   # true/false
SCRIPT4_SCHEDULE="FRI"                    # For DATE: number | For DAY: MON,TUE,WED,THU,FRI,SAT,SUN
SCRIPT4_PATH="/fs_ogs/operogs/scriptbin/ogs_monitors/Jupitoverse/script4.py"

# Script 5 Configuration
SCRIPT5_ENABLED="false"                   # true/false
SCRIPT5_SCHEDULE="1"                      # For DATE: number (1 = 1,11,21,31) | For DAY: MON,TUE,WED,THU,FRI,SAT,SUN
SCRIPT5_PATH="/fs_ogs/operogs/scriptbin/ogs_monitors/Jupitoverse/script5.py"

#############################################################################
# EXECUTION LOGIC - DO NOT MODIFY BELOW THIS LINE
#############################################################################

# Get current date and day
CURRENT_DATE=$(date +%d | sed 's/^0*//')  # Remove leading zeros
CURRENT_DAY=$(date +%a | tr '[:lower:]' '[:upper:]')

echo "============================================================"
echo "Orion Python Script Executor Started: $(date)"
echo "Current Date: $CURRENT_DATE | Current Day: $CURRENT_DAY"
echo "============================================================"

# Function to check if script should run
should_run() {
    local schedule="$1"
    
    # Check if it's a number (DATE mode) or text (DAY mode)
    if [[ "$schedule" =~ ^[0-9]+$ ]]; then
        # DATE mode: check if current date is divisible by schedule value
        if [ $((CURRENT_DATE % schedule)) -eq 0 ]; then
            return 0  # Should run
        fi
    else
        # DAY mode: check if current day matches
        if [ "$CURRENT_DAY" = "$schedule" ]; then
            return 0  # Should run
        fi
    fi
    return 1  # Should not run
}

# Function to run a script
run_script() {
    local enabled="$1"
    local schedule="$2"
    local path="$3"
    local script_name="$4"
    
    if [ "$enabled" != "true" ]; then
        echo "[$script_name] SKIPPED - Disabled"
        return 0
    fi
    
    if ! should_run "$schedule"; then
        echo "[$script_name] SKIPPED - Not scheduled (Schedule: $schedule)"
        return 0
    fi
    
    if [ ! -f "$path" ]; then
        echo "[$script_name] ERROR - File not found: $path"
        return 1
    fi
    
    echo "[$script_name] RUNNING - $path"
    echo "  Start: $(date)"
    
    python3 "$path"
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "  End: $(date) - SUCCESS"
    else
        echo "  End: $(date) - FAILED (Exit code: $exit_code)"
    fi
    echo "------------------------------------------------------------"
    
    return $exit_code
}

# Execute all scripts
TOTAL_EXECUTED=0
TOTAL_ERRORS=0

# Script 1
run_script "$SCRIPT1_ENABLED" "$SCRIPT1_SCHEDULE" "$SCRIPT1_PATH" "SCRIPT1"
if [ $? -eq 0 ] && [ "$SCRIPT1_ENABLED" = "true" ] && should_run "$SCRIPT1_SCHEDULE"; then
    TOTAL_EXECUTED=$((TOTAL_EXECUTED + 1))
elif [ $? -ne 0 ]; then
    TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
    TOTAL_EXECUTED=$((TOTAL_EXECUTED + 1))
fi

# Wait and continue with remaining scripts
sleep $((DELAY_MINUTES * 60))

# Script 2
run_script "$SCRIPT2_ENABLED" "$SCRIPT2_SCHEDULE" "$SCRIPT2_PATH" "SCRIPT2"
if [ $? -eq 0 ] && [ "$SCRIPT2_ENABLED" = "true" ] && should_run "$SCRIPT2_SCHEDULE"; then
    TOTAL_EXECUTED=$((TOTAL_EXECUTED + 1))
elif [ $? -ne 0 ]; then
    TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
    TOTAL_EXECUTED=$((TOTAL_EXECUTED + 1))
fi

sleep $((DELAY_MINUTES * 60))

# Script 3
run_script "$SCRIPT3_ENABLED" "$SCRIPT3_SCHEDULE" "$SCRIPT3_PATH" "SCRIPT3"
if [ $? -eq 0 ] && [ "$SCRIPT3_ENABLED" = "true" ] && should_run "$SCRIPT3_SCHEDULE"; then
    TOTAL_EXECUTED=$((TOTAL_EXECUTED + 1))
elif [ $? -ne 0 ]; then
    TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
    TOTAL_EXECUTED=$((TOTAL_EXECUTED + 1))
fi

sleep $((DELAY_MINUTES * 60))

# Script 4
run_script "$SCRIPT4_ENABLED" "$SCRIPT4_SCHEDULE" "$SCRIPT4_PATH" "SCRIPT4"
if [ $? -eq 0 ] && [ "$SCRIPT4_ENABLED" = "true" ] && should_run "$SCRIPT4_SCHEDULE"; then
    TOTAL_EXECUTED=$((TOTAL_EXECUTED + 1))
elif [ $? -ne 0 ]; then
    TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
    TOTAL_EXECUTED=$((TOTAL_EXECUTED + 1))
fi

sleep $((DELAY_MINUTES * 60))

# Script 5
run_script "$SCRIPT5_ENABLED" "$SCRIPT5_SCHEDULE" "$SCRIPT5_PATH" "SCRIPT5"
if [ $? -eq 0 ] && [ "$SCRIPT5_ENABLED" = "true" ] && should_run "$SCRIPT5_SCHEDULE"; then
    TOTAL_EXECUTED=$((TOTAL_EXECUTED + 1))
elif [ $? -ne 0 ]; then
    TOTAL_ERRORS=$((TOTAL_ERRORS + 1))
    TOTAL_EXECUTED=$((TOTAL_EXECUTED + 1))
fi

# Final Summary
echo "============================================================"
echo "EXECUTION COMPLETED: $(date)"
echo "Scripts Executed: $TOTAL_EXECUTED"
echo "Errors: $TOTAL_ERRORS"
if [ $TOTAL_ERRORS -eq 0 ]; then
    echo "Status: SUCCESS"
    exit 0
else
    echo "Status: COMPLETED WITH ERRORS"
    exit 1
fi
