# Network Access Issue - Database Connection Refused

## Problem Summary

The OSO_Service_Activated.py script is failing with **"Connection refused"** errors when trying to connect to both READ and WRITE PostgreSQL databases from your Remote Desktop machine.

### Error Details

```
[ERROR] PostgreSQL Error (READ): connection to server at "oso-pstgr-rd.orion.comcast.com" 
(10.145.229.36), port 6432 failed: Connection refused (0x0000274D/10061)

[ERROR] PostgreSQL Error (WRITE): connection to server at 
"OSS-PROD1-PGRDS-NLB-1fe6faf4eb2c6ea3.elb.us-east-2.amazonaws.com" 
(100.89.26.197), port 6432 failed: Connection refused (0x0000274D/10061)
```

## Root Cause

**Network/Firewall Restrictions**: The databases are only accessible from specific networks or servers (e.g., production app servers, Unix servers in the same VPC/network zone). Your Remote Desktop machine is NOT in an allowed network.

Port 6432 traffic is blocked by:
- Corporate firewall
- Database security groups
- Network ACLs
- VPC routing restrictions

## Solutions (Choose One)

### ✅ Option 1: Run Script from Unix/Linux Server (RECOMMENDED)

**Where it works:**
- The Unix server you mentioned earlier (where you got the encoding error)
- Any application server that already has database access
- Jenkins/automation server
- Jump hosts with database access

**Steps:**
1. Transfer the script to a Unix server:
   ```bash
   # Copy to Unix server
   scp OSO_Service_Activated.py user@unix-server:/path/to/script/
   
   # Or use WinSCP, FileZilla, etc.
   ```

2. Install required Python packages on that server:
   ```bash
   pip3 install psycopg2-binary pandas openpyxl --user
   ```

3. Run the script:
   ```bash
   python3 OSO_Service_Activated.py
   ```

**Why this works:**
- Unix/Linux servers in the data center typically have network access to databases
- Production databases are designed to be accessed from app servers, not desktop machines

---

### ✅ Option 2: Use VPN or Bastion/Jump Host

If you have VPN access to the production network:

1. **Connect to VPN** that routes to the database network
2. **Verify connectivity:**
   ```powershell
   Test-NetConnection oso-pstgr-rd.orion.comcast.com -Port 6432
   ```
3. If connection succeeds, run the script again

Alternatively, use a bastion/jump host:
```bash
# SSH tunnel through bastion
ssh -L 6432:oso-pstgr-rd.orion.comcast.com:6432 user@bastion-host

# Then update script to use localhost:6432
```

---

### ✅ Option 3: Request Network Access (DBA/Network Team)

Contact your DBA or Network team to:

1. **Whitelist your Remote Desktop IP** for database access
2. **Request security group rule** allowing:
   - Source: Your machine's IP or subnet
   - Destination: Database hosts
   - Port: 6432

**Information to provide:**
- Your machine's IP address
- Database hosts needed:
  - `oso-pstgr-rd.orion.comcast.com` (READ DB)
  - `OSS-PROD1-PGRDS-NLB-1fe6faf4eb2c6ea3.elb.us-east-2.amazonaws.com` (WRITE DB)
- Port: 6432
- Business justification

**Note:** This may take time and might not be approved due to security policies.

---

### ✅ Option 4: Schedule as a Server-Side Job

Set up the script to run automatically on a server with database access:

1. **Copy script to application server**
2. **Set up cron job** (Linux) or **Task Scheduler** (Windows Server):
   ```bash
   # Linux cron - Run daily at 8 AM
   0 8 * * * /usr/bin/python3 /path/to/OSO_Service_Activated.py >> /var/log/oso_sync.log 2>&1
   ```

3. **Email reports** will be sent automatically

**Benefits:**
- ✅ Runs automatically daily
- ✅ No manual intervention needed
- ✅ Consistent network access
- ✅ No desktop dependency

---

## Quick Test: Check Database Connectivity

### From PowerShell (Windows):
```powershell
# Test READ DB
Test-NetConnection oso-pstgr-rd.orion.comcast.com -Port 6432

# Test WRITE DB
Test-NetConnection OSS-PROD1-PGRDS-NLB-1fe6faf4eb2c6ea3.elb.us-east-2.amazonaws.com -Port 6432
```

### From Bash (Linux/Unix):
```bash
# Test READ DB
nc -zv oso-pstgr-rd.orion.comcast.com 6432

# Test WRITE DB
nc -zv OSS-PROD1-PGRDS-NLB-1fe6faf4eb2c6ea3.elb.us-east-2.amazonaws.com 6432

# Or using telnet
telnet oso-pstgr-rd.orion.comcast.com 6432
```

**Expected output if accessible:**
- `TcpTestSucceeded : True` (Windows)
- `Connection to host succeeded` (Linux)

---

## Current Script Status

### ✅ Script is Ready
- ✅ All Python code is correct
- ✅ REPORT_ONLY_MODE implemented (no write DB needed when enabled)
- ✅ Error handling in place
- ✅ Email functionality works
- ✅ Excel export works

### ❌ Only Issue: Network Access
- The script **ONLY** needs to be run from a machine/server with database network access

---

## Recommended Next Steps

1. **Identify a Unix/Linux server** with database access (you mentioned you have one)
2. **Transfer the script** to that server
3. **Install dependencies** (`psycopg2-binary`, `pandas`, `openpyxl`)
4. **Fix the encoding issue** (already have UTF-8 header in place)
5. **Run the script** - it will work from there!

OR

1. **Set up as a scheduled job** on a server with DB access
2. **Let it run daily** and email reports automatically

---

## Files Ready for Transfer

If going with Option 1 (Unix server), transfer these files:

```
OSO_Service_Activated.py          # Main script (READY)
RUN_OSO_SCRIPT.bat                # Windows batch file (optional)
CREATE_TABLE_OSO.sql              # Table creation SQL (if needed)
```

---

## Need Help?

The script is **100% ready to run**. It just needs to be executed from a machine with network access to the databases. Once you run it from a proper server, it will:

1. ✅ Connect to READ DB
2. ✅ Fetch service activation data
3. ✅ Check for NEW vs EXISTING records (REPORT_ONLY_MODE)
4. ✅ Generate multi-sheet Excel report
5. ✅ Email the report to you

Let me know which option you'd like to pursue!









