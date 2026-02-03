# ✅ Orionverse AVD Deployment Checklist

## 📦 Before Zipping (Local Machine)

- [ ] All code changes saved
- [ ] Backend tested locally (`python backend/app.py`)
- [ ] Frontend tested (search, workarounds working)
- [ ] `requirements.txt` exists and is up to date
- [ ] Database credentials verified in `backend/database.py`
- [ ] All documentation files included
- [ ] No temporary/cache files (clean up `__pycache__`, `.pyc` files)

**Create ZIP:**
```powershell
cd C:\Users\abhisha3\Desktop\Projects\Orion
Compress-Archive -Path "Orionverse" -DestinationPath "Orionverse.zip"
```

---

## 🚚 Transfer to AVD

- [ ] ZIP file copied to AVD machine (OneDrive, network share, USB)
- [ ] Extracted to desired location (e.g., `C:\Projects\Orionverse`)
- [ ] All files present after extraction

**Extract:**
```powershell
Expand-Archive -Path "Orionverse.zip" -DestinationPath "C:\Projects\"
```

---

## 🔧 Setup on AVD Machine

### **Required Software:**

- [ ] **Python 3.11+** installed
  - Check: `python --version`
  - Download: https://www.python.org/downloads/
  - ⚠️ Check "Add Python to PATH" during installation

- [ ] **pip** working
  - Check: `pip --version`
  - Upgrade: `python -m pip install --upgrade pip`

- [ ] **VS Code** installed (optional but recommended)
  - Download: https://code.visualstudio.com/

- [ ] **PostgreSQL client** (optional, for database testing)
  - Download: https://www.postgresql.org/download/

### **Python Dependencies:**

- [ ] Navigate to project: `cd C:\Projects\Orionverse`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Verify installations:
  ```powershell
  pip list
  # Should show: Flask, Flask-CORS, psycopg2-binary, pandas, SQLAlchemy, etc.
  ```

**Or run automated setup:**
```powershell
.\setup_avd.ps1
```

---

## 🔌 Network & Database

- [ ] **Connected to Comcast network/VPN**
  - Check: VPN client connected
  - Verify: Can access internal resources

- [ ] **Database connection working**
  - Test: 
    ```powershell
    cd backend
    python -c "import database; conn = database.get_db_connection(); print('✅ Connected' if conn else '❌ Failed')"
    ```
  - Or ping: `Test-NetConnection -ComputerName oso-pstgr-rd.orion.comcast.com -Port 6432`

- [ ] **Database schema setup** (first time only)
  - Run: `psql -h oso-pstgr-rd.orion.comcast.com -p 6432 -U ossdb01uams -d prodossdb < backend/schema_workarounds_enhanced.sql`
  - Verify: Tables created (`workarounds`, `workaround_comments`, etc.)

---

## 🔥 Firewall Configuration

- [ ] **Windows Firewall rule created**
  - Run as Administrator:
    ```powershell
    New-NetFirewallRule -DisplayName "Flask Backend 5001" -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow
    ```
  - Or use GUI: Windows Defender Firewall → Advanced Settings → Inbound Rules → New Rule

- [ ] **Port 5001 accessible**
  - Test: `Test-NetConnection -ComputerName localhost -Port 5001`

---

## 🚀 Start Backend

- [ ] **Backend starts successfully**
  - Option 1: `.\START_NETWORK_BACKEND.bat`
  - Option 2: `cd backend ; python app.py`

- [ ] **Expected output shows:**
  ```
  * Running on http://0.0.0.0:5001
  * Running on http://YOUR_IP:5001
  ```

- [ ] **No error messages in console**

---

## 🧪 Testing

### **API Tests:**

- [ ] **Test local access:**
  ```powershell
  curl http://localhost:5001/api/search/all
  ```
  - Should return JSON with SR/defect/workaround data

- [ ] **Test network access:**
  ```powershell
  curl http://YOUR_IP:5001/api/search/all
  ```

- [ ] **Test in browser:**
  - Open: `http://localhost:5001/api/search/all`
  - Should show JSON response

### **Frontend Tests:**

- [ ] **Open index.html** in browser
- [ ] **Check console** (F12) for API URL:
  ```
  🌐 API Base URL: http://YOUR_IP:5001
  ```
- [ ] **Test search functionality:**
  - Search Anything tab works
  - Can search by SR number, customer ID, defect name
  - Results display correctly

- [ ] **Test workaround features:**
  - Can view workarounds
  - Can add new workaround
  - Can add comments
  - Can like/unlike
  - Can bookmark/share

### **Run Diagnostic Script:**

- [ ] **Execute test script:**
  ```powershell
  .\test_network_access.ps1
  ```

- [ ] **All checks pass:**
  - ✅ IP address found
  - ✅ Python installed
  - ✅ Backend running
  - ✅ Port 5001 open
  - ✅ Firewall configured
  - ✅ API responding

---

## 📂 VS Code Setup

- [ ] **Open project in VS Code:**
  ```powershell
  cd C:\Projects\Orionverse
  code .
  ```

- [ ] **Recommended extensions installed:**
  - Python (Microsoft)
  - Pylance
  - Flask Snippets
  - PostgreSQL
  - Thunder Client (for API testing)

- [ ] **Python interpreter selected:**
  - Press: `Ctrl+Shift+P`
  - Type: "Python: Select Interpreter"
  - Choose: Python 3.11+

---

## 🔒 Security Verification

- [ ] **Debug mode** appropriate for environment:
  - Development: `debug=True` (OK)
  - Production: `debug=False` (REQUIRED)

- [ ] **Database credentials** not hardcoded (use `.env` file):
  - Create `.env` file with credentials
  - Update `database.py` to use `python-dotenv`
  - Add `.env` to `.gitignore`

- [ ] **Firewall** only allows necessary ports
- [ ] **CORS** configured appropriately
- [ ] **No sensitive data** in logs

---

## 📊 Verification Commands

**Run these to verify everything:**

```powershell
# 1. Check Python
python --version

# 2. Check installed packages
pip list | findstr "Flask psycopg2 pandas"

# 3. Check backend process
Get-Process | Where-Object {$_.ProcessName -like "*python*"}

# 4. Check port
Test-NetConnection -ComputerName localhost -Port 5001

# 5. Check firewall
Get-NetFirewallRule -DisplayName "*Flask*"

# 6. Test API
curl http://localhost:5001/api/search/all

# 7. Check IP
ipconfig | findstr IPv4
```

---

## 🆘 Troubleshooting Reference

### **Python not found:**
- Add to PATH: System Properties → Environment Variables
- Reinstall Python with "Add to PATH" checked

### **pip install fails:**
- Upgrade pip: `python -m pip install --upgrade pip`
- Install Visual C++ Build Tools (for psycopg2)

### **Database connection fails:**
- Check VPN/network connection
- Test connectivity: `Test-NetConnection -ComputerName oso-pstgr-rd.orion.comcast.com -Port 6432`
- Verify credentials in `backend/database.py`

### **Port 5001 in use:**
- Find process: `netstat -ano | findstr :5001`
- Kill process: `taskkill /PID <pid> /F`

### **Backend crashes:**
- Check console for error messages
- Verify all dependencies installed
- Check Python version (3.8+)

### **API not responding:**
- Verify backend is running
- Check firewall rules
- Test port: `Test-NetConnection -ComputerName localhost -Port 5001`

---

## 📋 Files to Verify After Extraction

```
✅ backend/
   ✅ app.py
   ✅ database.py
   ✅ routes/ (auth.py, billing.py, search.py, workarounds.py, workarounds_enhanced.py)
   ✅ data/ (sr_data.json, defect_data.json, wa_data.json)
   ✅ schema_workarounds_enhanced.sql

✅ templates/
   ✅ *.html files

✅ static/
   ✅ css/style.css
   ✅ js/api.js and other JS files

✅ Root files:
   ✅ index.html
   ✅ requirements.txt
   ✅ START_NETWORK_BACKEND.bat
   ✅ setup_avd.ps1
   ✅ test_network_access.ps1
   ✅ DEPLOYMENT_CHECKLIST.md (this file)
   ✅ AVD_DEPLOYMENT_GUIDE.md
   ✅ NETWORK_DEPLOYMENT_GUIDE.md
   ✅ Other documentation
```

---

## 🎯 Success Criteria

### **Setup is successful when:**

✅ Backend starts without errors
✅ Shows "Running on http://0.0.0.0:5001"
✅ Shows network IP in output
✅ Can access: `http://localhost:5001/api/search/all`
✅ Browser shows: `🌐 API Base URL: http://YOUR_IP:5001`
✅ Search functionality works
✅ Workaround features work
✅ Database queries return data
✅ No errors in browser console (F12)
✅ Team can access via network IP

---

## 📞 Quick Reference Commands

```powershell
# Setup
.\setup_avd.ps1

# Start backend
.\START_NETWORK_BACKEND.bat

# Test everything
.\test_network_access.ps1

# Manual start
cd backend
python app.py

# Test API
curl http://localhost:5001/api/search/all

# Open VS Code
code .

# Get IP
ipconfig | findstr IPv4

# Check process
Get-Process | Where-Object {$_.ProcessName -like "*python*"}

# Test port
Test-NetConnection -ComputerName localhost -Port 5001
```

---

## 🎉 Deployment Complete!

When all items are checked:

1. ✅ ZIP created and transferred
2. ✅ Extracted on AVD machine
3. ✅ Python and dependencies installed
4. ✅ Database connection verified
5. ✅ Firewall configured
6. ✅ Backend started successfully
7. ✅ API responding correctly
8. ✅ Frontend working
9. ✅ All tests passing

**You're ready to use Orionverse on AVD!** 🚀

---

## 📚 Documentation

- **This checklist** - Deployment steps
- **AVD_DEPLOYMENT_GUIDE.md** - Complete deployment guide
- **NETWORK_DEPLOYMENT_GUIDE.md** - Network configuration details
- **QUICK_NETWORK_SETUP.md** - Quick reference
- **WORKAROUND_SETUP_GUIDE.md** - Workaround system setup
- **SETUP_COMPLETE.md** - Network setup summary

---

**Total Time: ~15-20 minutes** ⏱️

**Difficulty: Easy** ✨ (with automated scripts)

**Support: Run** `.\test_network_access.ps1` **for diagnostics** 🔧





