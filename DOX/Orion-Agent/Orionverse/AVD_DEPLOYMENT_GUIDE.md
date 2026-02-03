# 🖥️ AVD Machine Deployment Guide

## 📋 Overview

This guide walks you through deploying Orionverse on an AVD (Azure Virtual Desktop) machine with database connectivity.

---

## 📦 What to Transfer

### **Create ZIP File on Local Machine:**

**Option 1 - Right-click:**
```
1. Navigate to: C:\Users\abhisha3\Desktop\Projects\Orion\Orionverse
2. Right-click folder → Send to → Compressed (zipped) folder
3. Name it: Orionverse.zip
```

**Option 2 - PowerShell:**
```powershell
cd C:\Users\abhisha3\Desktop\Projects\Orion
Compress-Archive -Path "Orionverse" -DestinationPath "Orionverse.zip"
```

**ZIP will include:**
- ✅ Backend code (`backend/`)
- ✅ Frontend code (`templates/`, `static/`)
- ✅ Database schemas (`schema_workarounds_enhanced.sql`)
- ✅ Dependencies list (`requirements.txt`)
- ✅ Configuration files
- ✅ Documentation

---

## 🚀 Setup on AVD Machine

### **Step 1: Transfer ZIP File**

**Copy Orionverse.zip to AVD machine via:**
- OneDrive/SharePoint
- Network share
- Email (if size permits)
- USB drive
- Remote Desktop copy-paste

**Recommended location on AVD:**
```
C:\Projects\Orionverse
```

---

### **Step 2: Extract ZIP File**

```powershell
# Navigate to desired location
cd C:\Projects

# Extract ZIP
Expand-Archive -Path "Orionverse.zip" -DestinationPath "."

# Verify extraction
cd Orionverse
dir
```

---

### **Step 3: Install Python (if not already installed)**

**Check if Python exists:**
```powershell
python --version
```

**If not installed:**

1. Download Python 3.11+ from: https://www.python.org/downloads/
2. **Important:** Check "Add Python to PATH" during installation
3. Verify installation:
   ```powershell
   python --version
   pip --version
   ```

**Or use Windows Store:**
```powershell
# Install from Microsoft Store
python3
# This will open Microsoft Store if not installed
```

---

### **Step 4: Install Python Dependencies**

**Open PowerShell/Terminal in Orionverse folder:**

```powershell
cd C:\Projects\Orionverse

# Upgrade pip first
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

**This will install:**
- ✅ Flask (web framework)
- ✅ Flask-CORS (API access)
- ✅ psycopg2 (PostgreSQL driver)
- ✅ pandas (data processing)
- ✅ SQLAlchemy (database ORM)
- ✅ requests (HTTP client)
- ✅ python-dotenv (environment variables)

**Expected output:**
```
Successfully installed Flask-3.0.0 Flask-CORS-4.0.0 psycopg2-binary-2.9.9 ...
```

---

### **Step 5: Verify Installation**

```powershell
# Check installed packages
pip list

# Should show:
# Flask              3.0.0
# Flask-CORS         4.0.0
# psycopg2-binary    2.9.9
# pandas             2.1.4
# SQLAlchemy         2.0.23
# ...
```

---

### **Step 6: Configure Database Connection**

**Edit:** `backend/database.py`

**Verify these settings:**
```python
def get_db_connection():
    try:
        conn = psycopg2.connect(
            database='prodossdb',
            user='ossdb01uams',
            password='Pr0d_ossdb01uams',
            host='oso-pstgr-rd.orion.comcast.com',
            port='6432'
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ DATABASE CONNECTION FAILED: {e}")
        return None
```

**Test database connection:**
```powershell
cd backend
python -c "import database; conn = database.get_db_connection(); print('✅ Connected!' if conn else '❌ Failed')"
```

---

### **Step 7: Setup Database Schema (First Time Only)**

**Connect to PostgreSQL:**
```bash
psql -h oso-pstgr-rd.orion.comcast.com -p 6432 -U ossdb01uams -d prodossdb
```

**Run schema setup:**
```sql
-- In psql prompt
\i C:/Projects/Orionverse/backend/schema_workarounds_enhanced.sql

-- Verify tables created
\dt

-- Should show:
-- workarounds
-- workaround_comments
-- workaround_likes
-- workaround_shares
-- workaround_activity_log
-- workaround_tags
-- workaround_user_preferences
```

**Or run from PowerShell:**
```powershell
Get-Content "backend\schema_workarounds_enhanced.sql" | psql -h oso-pstgr-rd.orion.comcast.com -p 6432 -U ossdb01uams -d prodossdb
```

---

### **Step 8: Configure Firewall (if needed)**

```powershell
# Run as Administrator
New-NetFirewallRule -DisplayName "Flask Backend 5001" -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow
```

---

### **Step 9: Start Backend**

**Option 1 - Use startup script:**
```powershell
.\START_NETWORK_BACKEND.bat
```

**Option 2 - Manual:**
```powershell
cd backend
python app.py
```

**Expected output:**
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://0.0.0.0:5001
* Running on http://10.x.x.x:5001  ← AVD IP
```

---

### **Step 10: Test Everything**

**Run diagnostics:**
```powershell
cd C:\Projects\Orionverse
powershell -ExecutionPolicy Bypass -File .\test_network_access.ps1
```

**Manual tests:**
```powershell
# Test API
curl http://localhost:5001/api/search/all

# Or in browser
http://localhost:5001/api/search/all
```

---

### **Step 11: Open in VS Code**

```powershell
# Open project in VS Code
cd C:\Projects\Orionverse
code .
```

**Recommended VS Code Extensions:**
- Python (Microsoft)
- Pylance
- Flask Snippets
- PostgreSQL (Chris Kolkman)
- Thunder Client (for API testing)

---

## 📊 Complete Folder Structure

After extraction, you should have:

```
C:\Projects\Orionverse\
├── backend\
│   ├── app.py                          # Main Flask app
│   ├── database.py                     # Database connection
│   ├── routes\
│   │   ├── auth.py
│   │   ├── billing.py
│   │   ├── search.py
│   │   ├── workarounds.py
│   │   └── workarounds_enhanced.py     # New collaborative features
│   ├── schema_workarounds_enhanced.sql # Database schema
│   └── data\
│       ├── sr_data.json                # SR search data
│       ├── defect_data.json            # Defect data
│       └── wa_data.json                # Workaround data
├── templates\
│   └── *.html                          # Frontend templates
├── static\
│   ├── css\
│   │   └── style.css
│   └── js\
│       ├── api.js                      # API configuration
│       └── *.js                        # Other scripts
├── index.html                          # Main entry point
├── requirements.txt                    # Python dependencies
├── START_NETWORK_BACKEND.bat           # Startup script
├── test_network_access.ps1             # Diagnostic script
└── Documentation\
    ├── NETWORK_DEPLOYMENT_GUIDE.md
    ├── QUICK_NETWORK_SETUP.md
    ├── WORKAROUND_SETUP_GUIDE.md
    └── AVD_DEPLOYMENT_GUIDE.md         # This file
```

---

## ✅ Pre-Deployment Checklist

Before zipping on local machine:

- [ ] Backend tested locally
- [ ] All files saved
- [ ] requirements.txt exists
- [ ] Documentation included
- [ ] Database credentials verified
- [ ] No sensitive data in code (use .env if needed)

---

## 🔧 AVD Machine Checklist

After extraction:

- [ ] Python 3.11+ installed
- [ ] pip updated: `python -m pip install --upgrade pip`
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Database connection tested
- [ ] Firewall configured (port 5001)
- [ ] Backend starts successfully
- [ ] API responds: `http://localhost:5001/api/search/all`
- [ ] VS Code opened with project

---

## 🐛 Troubleshooting

### **Issue: Python not found**

**Solution:**
```powershell
# Add Python to PATH manually
# System Properties → Environment Variables → Path → Add:
C:\Users\YourUser\AppData\Local\Programs\Python\Python311
C:\Users\YourUser\AppData\Local\Programs\Python\Python311\Scripts
```

### **Issue: pip install fails**

**Solution:**
```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Try installing individually
pip install Flask
pip install Flask-CORS
pip install psycopg2-binary
pip install pandas
pip install SQLAlchemy
pip install python-dotenv
```

### **Issue: psycopg2 installation error**

**Solution:**
```powershell
# Use binary version (already in requirements.txt)
pip install psycopg2-binary

# If still fails, install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
```

### **Issue: Database connection fails**

**Check:**
1. Are you on Comcast network/VPN?
2. Can you ping the DB server?
   ```powershell
   Test-NetConnection -ComputerName oso-pstgr-rd.orion.comcast.com -Port 6432
   ```
3. Are credentials correct in `backend/database.py`?
4. Is PostgreSQL client installed? (optional, for psql command)

### **Issue: Port 5001 in use**

**Solution:**
```powershell
# Find process using port
netstat -ano | findstr :5001

# Kill process
taskkill /PID <process_id> /F

# Or change port in backend/app.py
```

### **Issue: Import errors**

**Solution:**
```powershell
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall

# Or create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 🎯 Using Virtual Environment (Recommended)

**Benefits:**
- Isolated dependencies
- No conflicts with system packages
- Clean uninstall (just delete folder)

**Setup:**
```powershell
cd C:\Projects\Orionverse

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run backend
cd backend
python app.py
```

**Deactivate:**
```powershell
deactivate
```

---

## 🔒 Security Considerations

### **1. Database Credentials**

**Option A - Use .env file (Recommended):**

Create `.env` file:
```env
DB_NAME=prodossdb
DB_USER=ossdb01uams
DB_PASSWORD=Pr0d_ossdb01uams
DB_HOST=oso-pstgr-rd.orion.comcast.com
DB_PORT=6432
```

Update `database.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT')
    )
    return conn
```

**⚠️ Important:** Add `.env` to `.gitignore`!

---

### **2. Production Mode**

For production deployment, change in `app.py`:
```python
app.run(
    host='0.0.0.0',
    port=5001,
    debug=False,  # ✅ Disable debug mode
    threaded=True
)
```

---

## 📊 System Requirements

### **Minimum:**
- Windows 10/11 or Windows Server
- Python 3.8+
- 2GB RAM
- 500MB free disk space
- Network access to PostgreSQL server

### **Recommended:**
- Windows 11 or Windows Server 2019+
- Python 3.11+
- 4GB RAM
- 1GB free disk space
- VS Code with Python extension
- PostgreSQL client tools (optional)

---

## 🚀 Quick Setup Script

**Create:** `setup_avd.ps1`

```powershell
# Orionverse AVD Quick Setup Script
Write-Host "🚀 Orionverse AVD Setup" -ForegroundColor Cyan
Write-Host ""

# 1. Check Python
Write-Host "[1/6] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Python not found. Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# 2. Upgrade pip
Write-Host "[2/6] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "  ✓ pip upgraded" -ForegroundColor Green

# 3. Install dependencies
Write-Host "[3/6] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "  ✓ Dependencies installed" -ForegroundColor Green

# 4. Test database connection
Write-Host "[4/6] Testing database connection..." -ForegroundColor Yellow
$testResult = python -c "import database; conn = database.get_db_connection(); print('OK' if conn else 'FAIL')" 2>&1
if ($testResult -like "*OK*") {
    Write-Host "  ✓ Database connected" -ForegroundColor Green
} else {
    Write-Host "  ✗ Database connection failed" -ForegroundColor Red
    Write-Host "  Ensure you're on Comcast network/VPN" -ForegroundColor Yellow
}

# 5. Configure firewall
Write-Host "[5/6] Configuring firewall..." -ForegroundColor Yellow
$rule = Get-NetFirewallRule -DisplayName "Flask Backend 5001" -ErrorAction SilentlyContinue
if (!$rule) {
    try {
        New-NetFirewallRule -DisplayName "Flask Backend 5001" -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow -ErrorAction Stop
        Write-Host "  ✓ Firewall rule created" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠ Run as Administrator to create firewall rule" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ✓ Firewall rule exists" -ForegroundColor Green
}

# 6. Get IP
Write-Host "[6/6] Getting IP address..." -ForegroundColor Yellow
$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*"} | Select-Object -First 1).IPAddress
Write-Host "  ✓ IP: $ip" -ForegroundColor Green

Write-Host ""
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Start backend: .\START_NETWORK_BACKEND.bat" -ForegroundColor Cyan
Write-Host "  2. Access at: http://$ip:5001" -ForegroundColor Cyan
Write-Host "  3. Open VS Code: code ." -ForegroundColor Cyan
Write-Host ""
```

---

## 📞 Support Commands

### **Check Installation:**
```powershell
python --version
pip list
python -c "import flask; print(flask.__version__)"
```

### **Test Backend:**
```powershell
cd backend
python -c "import app; print('✅ Backend OK')"
```

### **Check Port:**
```powershell
Test-NetConnection -ComputerName localhost -Port 5001
```

### **View Logs:**
```powershell
# Backend logs are shown in terminal where it's running
# Check for errors
```

---

## 🎉 You're Ready!

After completing all steps:

1. ✅ ZIP file created on local machine
2. ✅ Transferred to AVD machine
3. ✅ Extracted to `C:\Projects\Orionverse`
4. ✅ Python and dependencies installed
5. ✅ Database connection verified
6. ✅ Backend started successfully
7. ✅ Opened in VS Code

**Start using:**
```powershell
cd C:\Projects\Orionverse
.\START_NETWORK_BACKEND.bat
```

**Access at:**
```
http://localhost:5001
http://YOUR_AVD_IP:5001
```

---

## 💡 Tips

- **Use virtual environment** for cleaner setup
- **Run diagnostic script** if issues occur
- **Check network connectivity** to database
- **Keep dependencies updated**: `pip install -r requirements.txt --upgrade`
- **Use VS Code** for easier development
- **Test API endpoints** with Thunder Client or Postman

---

**Everything you need is now documented! Just zip, transfer, extract, and run!** 🚀✨






