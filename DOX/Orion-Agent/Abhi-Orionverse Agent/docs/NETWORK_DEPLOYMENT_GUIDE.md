# 🌐 Network Deployment Guide - Orionverse

## 📋 Overview

This guide helps you deploy Orionverse on a network where database connection is possible (e.g., Comcast internal network, VPN, or remote server).

---

## 🎯 Deployment Options

### **Option 1: Run on Network-Connected Machine** (Recommended)
- Run backend on machine with DB access
- Access from other machines via network IP
- Best for team collaboration

### **Option 2: VPN + Local Machine**
- Connect to VPN with DB access
- Run locally, share via network
- Good for testing

### **Option 3: Deploy to Server**
- Deploy to shared server (Linux/Windows)
- Always accessible to team
- Production-ready

---

## 🚀 Quick Start - Run on Network

### **Step 1: Find Your Machine's IP Address**

#### **On Windows:**
```powershell
# Open PowerShell
ipconfig

# Look for:
# IPv4 Address: 192.168.x.x  (Local network)
# or
# IPv4 Address: 10.x.x.x     (Corporate network)
```

#### **On Linux/Mac:**
```bash
ifconfig
# or
ip addr show
```

**Example Output:**
```
IPv4 Address: 192.168.1.100
```

---

### **Step 2: Update Flask Backend to Listen on All Interfaces**

**Edit:** `backend/app.py`

**Change this:**
```python
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5001)  # Only accessible from localhost
```

**To this:**
```python
if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',  # ✅ Listen on all network interfaces
        port=5001,
        debug=True
    )
```

**What this does:**
- `host='0.0.0.0'` - Makes Flask accessible from ANY network interface
- `port=5001` - Uses port 5001 (change if needed)
- Accessible via: `http://YOUR_IP:5001`

---

### **Step 3: Update Frontend API Configuration**

**Edit:** `static/js/api.js`

**Change this:**
```javascript
const API_BASE_URL = 'http://127.0.0.1:5001'; // ❌ Only works locally
```

**To this (Option A - Use Your IP):**
```javascript
const API_BASE_URL = 'http://192.168.1.100:5001'; // ✅ Replace with your IP
```

**Or (Option B - Use Hostname):**
```javascript
const API_BASE_URL = 'http://YOUR-MACHINE-NAME:5001'; // ✅ Use computer name
```

**Or (Option C - Dynamic Detection - Best!):**
```javascript
// Automatically detects the host
const API_BASE_URL = `http://${window.location.hostname}:5001`;
```

---

### **Step 4: Configure Windows Firewall**

#### **Allow Port 5001 Through Firewall:**

```powershell
# Open PowerShell as Administrator
New-NetFirewallRule -DisplayName "Flask Backend 5001" -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow
```

**Or use GUI:**
1. Open **Windows Defender Firewall**
2. Click **Advanced Settings**
3. Click **Inbound Rules** → **New Rule**
4. Select **Port** → Next
5. Enter **5001** → Next
6. Select **Allow the connection** → Next
7. Check all profiles → Next
8. Name: **Flask Orionverse Backend** → Finish

---

### **Step 5: Restart Backend**

```bash
cd C:\Users\abhisha3\Desktop\Projects\Orion\Orionverse\backend
python app.py
```

**You should see:**
```
* Running on http://0.0.0.0:5001
* Running on http://192.168.1.100:5001  # ✅ Your network IP
```

---

### **Step 6: Access from Other Machines**

**From any machine on the same network:**

**Open browser and navigate to:**
```
http://192.168.1.100:5001         # Backend API
http://192.168.1.100/Orionverse   # Frontend (if hosted)
```

**Or just open:** `index.html` on your machine and it will connect to the backend!

---

## 🔧 Complete Configuration Files

### **1. Updated `backend/app.py`**

```python
# backend/app.py
from flask import Flask
from flask_cors import CORS

# Import all blueprints
from routes.auth import auth_bp
from routes.billing import billing_bp
from routes.search import search_bp
from routes.workarounds import workarounds_bp

def create_app():
    """Application factory pattern for Flask app creation"""
    app = Flask(__name__)
    
    # Enable CORS for all domains (for development)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register all blueprints with the main app
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(billing_bp, url_prefix='/api/billing')
    app.register_blueprint(search_bp, url_prefix='/api/search')
    app.register_blueprint(workarounds_bp, url_prefix='/api/workarounds')

    return app

if __name__ == '__main__':
    app = create_app()
    
    # Network deployment configuration
    app.run(
        host='0.0.0.0',        # ✅ Listen on all interfaces
        port=5001,             # Port number
        debug=True,            # Enable debug mode
        threaded=True          # Handle multiple requests
    )
```

---

### **2. Updated `static/js/api.js`**

**Option A - Manual IP (Simple):**
```javascript
// static/js/api.js
const API_BASE_URL = 'http://192.168.1.100:5001'; // ✅ Your machine IP
```

**Option B - Dynamic (Smart):**
```javascript
// static/js/api.js
// Automatically detect if running locally or on network
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:5001'
    : `http://${window.location.hostname}:5001`;

console.log('API Base URL:', API_BASE_URL); // Debug output
```

**Option C - Environment-based (Professional):**
```javascript
// static/js/api.js
const config = {
    development: 'http://127.0.0.1:5001',
    production: 'http://192.168.1.100:5001',
    // Add more environments as needed
};

const API_BASE_URL = config[process.env.NODE_ENV || 'development'];
```

---

## 🐧 Deploy to Linux Server (Production)

### **Step 1: Install Dependencies**

```bash
# SSH into your Linux server
ssh user@server-ip

# Install Python and dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql-client

# Create project directory
mkdir -p /opt/orionverse
cd /opt/orionverse
```

### **Step 2: Upload Project Files**

```powershell
# From your Windows machine
scp -r C:\Users\abhisha3\Desktop\Projects\Orion\Orionverse user@server-ip:/opt/orionverse/
```

### **Step 3: Setup Virtual Environment**

```bash
cd /opt/orionverse
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **Step 4: Create Systemd Service**

```bash
sudo nano /etc/systemd/system/orionverse.service
```

```ini
[Unit]
Description=Orionverse Flask Backend
After=network.target

[Service]
User=your-username
WorkingDirectory=/opt/orionverse/backend
Environment="PATH=/opt/orionverse/venv/bin"
ExecStart=/opt/orionverse/venv/bin/python app.py

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### **Step 5: Start Service**

```bash
sudo systemctl daemon-reload
sudo systemctl start orionverse
sudo systemctl enable orionverse
sudo systemctl status orionverse
```

---

## 🌐 Deploy with Nginx (Reverse Proxy)

### **Why Use Nginx?**
- Better performance
- SSL/HTTPS support
- Load balancing
- Professional setup

### **Install Nginx:**

```bash
sudo apt install nginx
```

### **Configure Nginx:**

```bash
sudo nano /etc/nginx/sites-available/orionverse
```

```nginx
server {
    listen 80;
    server_name your-server-name.com;

    # Frontend (Static files)
    location / {
        root /opt/orionverse;
        index index.html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static assets
    location /static/ {
        root /opt/orionverse;
        expires 30d;
    }
}
```

### **Enable Site:**

```bash
sudo ln -s /etc/nginx/sites-available/orionverse /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### **Update Frontend:**

```javascript
// static/js/api.js
const API_BASE_URL = '/api'; // ✅ Nginx will proxy to backend
```

---

## 🔒 Security Considerations

### **1. Change Debug Mode in Production**

```python
# backend/app.py
if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=5001,
        debug=False,  # ✅ Disable debug in production!
        threaded=True
    )
```

### **2. Add Authentication**

```python
# backend/app.py
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

users = {
    "admin": "your-password-here"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    return None

# Protect routes
@app.route('/api/protected')
@auth.login_required
def protected_route():
    return jsonify({'message': 'Authenticated!'})
```

### **3. Use Environment Variables**

```python
# backend/database.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    try:
        conn = psycopg2.connect(
            database=os.getenv('DB_NAME', 'prodossdb'),
            user=os.getenv('DB_USER', 'ossdb01uams'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST', 'oso-pstgr-rd.orion.comcast.com'),
            port=os.getenv('DB_PORT', '6432')
        )
        return conn
    except psycopg2.OperationalError as e:
        print(f"❌ DATABASE CONNECTION FAILED: {e}")
        return None
```

### **4. Create `.env` File**

```bash
# .env (DO NOT COMMIT TO GIT!)
DB_NAME=prodossdb
DB_USER=ossdb01uams
DB_PASSWORD=Pr0d_ossdb01uams
DB_HOST=oso-pstgr-rd.orion.comcast.com
DB_PORT=6432
FLASK_SECRET_KEY=your-secret-key-here
```

---

## 🧪 Testing Network Access

### **Test from Local Machine:**

```bash
# Test backend
curl http://192.168.1.100:5001/api/search/all

# Test with browser
http://192.168.1.100:5001/api/search/all
```

### **Test from Another Machine:**

```bash
# Replace with your IP
curl http://192.168.1.100:5001/api/search/all
```

### **Test Frontend:**

1. Open `index.html` on another machine
2. Check browser console (F12)
3. Should see: "API Base URL: http://192.168.1.100:5001"
4. Try searching - should work!

---

## 🐛 Troubleshooting

### **Issue: "Connection Refused"**

**Solutions:**
```powershell
# 1. Check if backend is running
Get-Process | Where-Object {$_.ProcessName -like "*python*"}

# 2. Check if port is open
Test-NetConnection -ComputerName localhost -Port 5001

# 3. Check firewall
Get-NetFirewallRule -DisplayName "Flask*"
```

### **Issue: "CORS Error"**

**Solution:** Update CORS configuration:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### **Issue: "Can't access from other machines"**

**Checklist:**
- [ ] Backend running with `host='0.0.0.0'`
- [ ] Firewall allows port 5001
- [ ] Correct IP address in frontend
- [ ] Both machines on same network
- [ ] No VPN blocking connections

### **Issue: "Database connection failed"**

**Solution:**
- Ensure you're on network with DB access (VPN, internal network)
- Test DB connection:
```bash
psql -h oso-pstgr-rd.orion.comcast.com -p 6432 -U ossdb01uams -d prodossdb
```

---

## 📝 Quick Setup Checklist

### **Backend Setup:**
- [ ] Update `app.py`: Add `host='0.0.0.0'`
- [ ] Configure firewall: Allow port 5001
- [ ] Start backend: `python app.py`
- [ ] Verify: See your IP in startup message

### **Frontend Setup:**
- [ ] Update `api.js`: Set correct IP/hostname
- [ ] Test: Open in browser
- [ ] Check console: Verify API URL
- [ ] Test search: Verify backend connection

### **Network Setup:**
- [ ] Get your IP: `ipconfig` or `ifconfig`
- [ ] Test locally: `curl http://localhost:5001/api/search/all`
- [ ] Test network: `curl http://YOUR_IP:5001/api/search/all`
- [ ] Share with team: Send them `http://YOUR_IP/index.html`

---

## 🎯 Recommended Setup for Your Case

**Best approach for Comcast network:**

1. **VPN/Network Connection:** Connect to Comcast internal network
2. **Run Backend:** Start Flask with `host='0.0.0.0'`
3. **Update Frontend:** Use dynamic API URL detection
4. **Share Access:** Team accesses via your machine IP
5. **Optional:** Deploy to shared server for permanent access

---

## 📊 Deployment Comparison

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Local Network** | Easy setup | Requires your machine running | Small teams |
| **Linux Server** | Always available | Requires server access | Production |
| **Docker** | Portable | Additional complexity | Scalability |
| **Cloud (AWS/Azure)** | Highly available | Costs money | Public access |

---

## 🚀 Next Steps

1. **Update `app.py`** with `host='0.0.0.0'`
2. **Configure firewall** to allow port 5001
3. **Update `api.js`** with your machine IP
4. **Restart backend** and test
5. **Share URL** with your team!

---

## 📞 Support Commands

### **Check Backend Status:**
```powershell
Get-Process | Where-Object {$_.ProcessName -like "*python*"}
Test-NetConnection -ComputerName localhost -Port 5001
```

### **Check Network Configuration:**
```powershell
ipconfig
Get-NetFirewallRule -DisplayName "Flask*" | Select-Object DisplayName, Enabled
```

### **View Backend Logs:**
```bash
# Backend will show logs in terminal where it's running
# Check for errors, connection attempts, API calls
```

---

**Ready to deploy? Follow the steps above and your Orionverse will be accessible across your network!** 🌐✨





