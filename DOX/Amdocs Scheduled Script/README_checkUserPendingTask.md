# Check User Pending Task - Script Conversion Documentation

## Overview
This document describes the conversion of the shell script (`checkUserPendingTask.py` - originally ksh) to a proper Python implementation (`checkUserPendingTask_converted.py`).

## Key Improvements

### 1. **Merged SQL Queries with Smart Batching**
   - **Original**: Three separate functions (`pull_data`, `pull_data2`, `pull_data3`) with different `part_id` ranges
   - **New**: Single unified function that iterates through `spec_ver_id` values one by one
   - **Benefit**: Prevents query timeout by processing smaller batches while maintaining comprehensive data collection

### 2. **Proper Logging System**
   - **Features**:
     - Logs to both console and file simultaneously
     - Timestamped log files for easy tracking
     - Automatic cleanup of logs older than 30 days
     - Detailed execution information at each step
   - **Location**: All logs stored in `LOGS/` directory

### 3. **Enhanced HTML Report Generation**
   - Professional styled HTML with:
     - Color-coded header and sections
     - Responsive table styling with hover effects
     - Record count summary
     - Automatic timestamp
   - Better readability and presentation

### 4. **Robust Error Handling**
   - Database connection failures handled gracefully
   - Email notification on errors
   - Proper exception logging
   - Script doesn't crash silently

### 5. **Execution Frequency Control**
   - Runs every 5th day of the month (configurable)
   - Sends notification email when execution is skipped
   - Prevents unnecessary processing and emails

### 6. **Code Structure**
   - Well-organized with clear sections
   - Comprehensive docstrings for all functions
   - Configuration separated at the top
   - Easy to maintain and modify

## Configuration

### Email Recipients
Edit the `EMAIL_CONFIG` dictionary to modify recipients:
```python
EMAIL_CONFIG = {
    'recipients': [
        'abhisha3@amdocs.com',
        # Add or remove recipients here
    ],
    'from': 'noreplyreports@amdocs.com',
    'error_recipients': ['abhisha3@amdocs.com']
}
```

### Database Configuration
Update `DB_CONFIG` if database credentials change:
```python
DB_CONFIG = {
    'database': 'prodossdb',
    'user': 'ossdb01uams',
    'password': 'Pr0d_ossdb01uams',
    'host': 'oso-pstgr-rd.orion.comcast.com',
    'port': '6432'
}
```

### Execution Frequency
Modify the frequency (currently every 5th day):
```python
EXECUTION_FREQUENCY = 5  # Change this value
```

### Log Retention
Change how long logs are kept:
```python
cleanup_old_logs(days_to_keep=30)  # Modify days_to_keep parameter
```

## SQL Query Optimization

### Original Approach (Shell Script)
The shell script split queries into three parts based on `part_id` ranges:
- **Function 1**: `part_id in (1-33)`
- **Function 2**: `part_id in (34-76)`
- **Function 3**: `part_id in (77-99)`

All three queries processed all `spec_ver_id` values, causing timeouts.

### New Approach (Python Script)
Iterates through each `spec_ver_id` individually with full `part_id` range batches:
```python
for spec_ver_id in spec_ver_ids:
    for part_id_start, part_id_end in [(1,33), (34,76), (77,99)]:
        # Execute query with specific spec_ver_id and part_id range
        # This prevents timeout by limiting query scope
```

**Benefits**:
- Smaller, faster queries
- No timeout issues
- Same comprehensive data coverage
- Better error isolation (if one fails, others continue)

## File Structure

```
Amdocs Scheduled Script/
├── checkUserPendingTask.py              # Original shell script (ksh)
├── checkUserPendingTask_converted.py    # New Python implementation
├── Outage_Report.py                     # Reference script
├── README_checkUserPendingTask.md       # This documentation
└── LOGS/                                # Log directory (auto-created)
    ├── checkUserPendingTask_YYYYMMDD_HHMMSS.log
    ├── checkUserPendingTask_YYYYMMDD_HHMMSS.html
    └── ... (older logs)
```

## Running the Script

### Prerequisites
```bash
pip install pandas psycopg2 openpyxl
```

### Execution
```bash
python checkUserPendingTask_converted.py
```

### Scheduling (Windows Task Scheduler)
1. Open Task Scheduler
2. Create New Task
3. Set Trigger: Daily at desired time
4. Set Action: Run Python script
   - Program: `python.exe` or `pythonw.exe`
   - Arguments: `C:\Path\To\checkUserPendingTask_converted.py`
5. Configure to run with highest privileges

### Scheduling (Linux/Unix Cron)
Add to crontab:
```bash
# Run daily at 2 AM
0 2 * * * /usr/bin/python3 /path/to/checkUserPendingTask_converted.py
```

## Output Files

### Log Files
- **Location**: `LOGS/checkUserPendingTask_YYYYMMDD_HHMMSS.log`
- **Content**: Detailed execution log with timestamps
- **Retention**: Automatically deleted after 30 days

### HTML Reports
- **Location**: `LOGS/checkUserPendingTask_YYYYMMDD_HHMMSS.html`
- **Content**: Formatted report with all pending tasks
- **Sent via email**: To configured recipients

## Email Notifications

### Success Email
- **Subject**: "Report || Orion User Pending Task Impacting Billing || Rebill - YYYY-MM-DD"
- **Content**: HTML report with all pending tasks
- **Recipients**: All configured recipients

### Skip Notification
- **Subject**: "INFO - Orion User Pending Task Report - Execution Skipped (Day N)"
- **Content**: Information about why execution was skipped
- **Recipients**: Error recipients only

### Error Notification
- **Subject**: "FAILURE - Orion User Pending Task Report"
- **Content**: Error details and timestamp
- **Recipients**: Error recipients

## Troubleshooting

### Database Connection Issues
1. Verify database credentials in `DB_CONFIG`
2. Check network connectivity to database host
3. Verify port accessibility
4. Check database user permissions

### Email Sending Issues
1. Verify SMTP server is accessible (`localhost`)
2. Check email server logs
3. Verify email addresses are correct
4. Test with a smaller recipient list

### No Data Returned
1. Check if tasks exist matching the criteria (30+ days old)
2. Verify `spec_ver_id` values are correct
3. Check database query permissions
4. Review log file for query errors

### Script Not Running on Schedule
1. Verify execution frequency setting
2. Check current day of month
3. Review scheduler configuration
4. Check script permissions

## Migration from Shell Script

### To migrate from the old shell script:

1. **Test the new script** in a non-production environment
2. **Update scheduler** to call the Python script instead
3. **Monitor first few executions** via log files
4. **Verify email reports** are being sent correctly
5. **Keep old script** as backup for a few cycles

### Differences to Note:

| Feature | Old (Shell) | New (Python) |
|---------|-------------|--------------|
| Query Strategy | 3 parallel queries | Sequential by spec_ver_id |
| Logging | Basic to $LOG_FILE | Comprehensive with rotation |
| HTML Generation | Simple concatenation | Professional styled output |
| Error Handling | Basic | Comprehensive with notifications |
| Cleanup | Manual move to LOGS/ | Automatic with old file removal |
| Email | sendmail command | SMTP with proper MIME types |

## Support

For issues or questions:
- **Developer**: abhisha3@amdocs.com
- **Co-Developer**: prateek.jain5@amdocs.com

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2024-10-19 | Complete Python conversion with improvements |
| 1.0 | 2024-11-12 | Original shell script version |



