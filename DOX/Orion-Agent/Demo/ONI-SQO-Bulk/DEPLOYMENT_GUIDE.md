# ONI-SQO-Bulk Console - Deployment Guide

## 📋 Table of Contents
1. [Option 1: Remote Desktop Deployment](#option-1-remote-desktop-deployment)
2. [Option 2: Amdocs Server Deployment](#option-2-amdocs-server-deployment)
3. [Option 3: Network Sharing (Quick Demo)](#option-3-network-sharing-quick-demo)
4. [Troubleshooting](#troubleshooting)

---

## Option 1: Remote Desktop Deployment

### Step 1: Copy Project to Remote Desktop

**Method A: Using Shared Drive**
```
1. Zip the entire ONI-SQO-Bulk folder
2. Copy to a shared drive accessible from Remote Desktop
3. On Remote Desktop, extract to: C:\Apps\ONI-SQO-Bulk
```

**Method B: Using RDP File Copy**
```
1. Connect to Remote Desktop
2. Enable "Local Resources" > "Clipboard" in RDP settings
3. Copy-paste the folder directly
```

**Method C: Using Git (Recommended)**
```bash
# On Remote Desktop, open PowerShell
cd C:\Apps
git clone <your-repo-url> ONI-SQO-Bulk
```

### Step 2: Install Python on Remote Desktop

```powershell
# Check if Python is installed
python --version

# If not installed, download from:
# https://www.python.org/downloads/
# OR use winget:
winget install Python.Python.3.11
```

### Step 3: Install Dependencies

```powershell
cd C:\Apps\ONI-SQO-Bulk
pip install -r requirements.txt
```

### Step 4: Configure Firewall (Run as Administrator)

```powershell
# Allow Backend (Port 5003)
netsh advfirewall firewall add rule name="ONI-SQO-Bulk Backend" dir=in action=allow protocol=tcp localport=5003

# Allow Frontend (Port 8080)
netsh advfirewall firewall add rule name="ONI-SQO-Bulk Frontend" dir=in action=allow protocol=tcp localport=8080
```

### Step 5: Start the Application

```powershell
# Option A: Double-click START_NETWORK.bat

# Option B: Manual start
# Terminal 1 - Backend
cd C:\Apps\ONI-SQO-Bulk\backend
python app.py

# Terminal 2 - Frontend
cd C:\Apps\ONI-SQO-Bulk
python -m http.server 8080 --bind 0.0.0.0
```

### Step 6: Access the Application

```
From Remote Desktop itself:
  http://localhost:8080

From your local machine (through RDP):
  http://<REMOTE_DESKTOP_IP>:8080
```

---

## Option 2: Amdocs Server Deployment

### Prerequisites
- SSH access to Amdocs server
- Python 3.8+ installed on server
- Ports 5003 and 8080 available

### Step 1: Transfer Files to Server

**Method A: Using SCP**
```bash
# From your local machine (Git Bash or PowerShell)
scp -r C:\Users\abhisha3\Desktop\Projects\DOX\Orion-Agent\Demo\ONI-SQO-Bulk user@amdocs-server:/opt/apps/
```

**Method B: Using SFTP**
```bash
sftp user@amdocs-server
put -r ONI-SQO-Bulk /opt/apps/
```

**Method C: Using Git on Server**
```bash
ssh user@amdocs-server
cd /opt/apps
git clone <your-repo-url> ONI-SQO-Bulk
```

### Step 2: Setup on Linux Server

```bash
# SSH into the server
ssh user@amdocs-server

# Navigate to app directory
cd /opt/apps/ONI-SQO-Bulk

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure for Production

**Create systemd service for Backend:**
```bash
sudo nano /etc/systemd/system/oni-sqo-backend.service
```

```ini
[Unit]
Description=ONI-SQO-Bulk Backend API
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/apps/ONI-SQO-Bulk/backend
Environment="PATH=/opt/apps/ONI-SQO-Bulk/venv/bin"
ExecStart=/opt/apps/ONI-SQO-Bulk/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Create systemd service for Frontend:**
```bash
sudo nano /etc/systemd/system/oni-sqo-frontend.service
```

```ini
[Unit]
Description=ONI-SQO-Bulk Frontend
After=network.target

[Service]
Type=simple
User=appuser
WorkingDirectory=/opt/apps/ONI-SQO-Bulk
ExecStart=/opt/apps/ONI-SQO-Bulk/venv/bin/python -m http.server 8080 --bind 0.0.0.0
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Step 4: Start Services

```bash
# Reload systemd
sudo systemctl daemon-reload

# Start services
sudo systemctl start oni-sqo-backend
sudo systemctl start oni-sqo-frontend

# Enable auto-start on boot
sudo systemctl enable oni-sqo-backend
sudo systemctl enable oni-sqo-frontend

# Check status
sudo systemctl status oni-sqo-backend
sudo systemctl status oni-sqo-frontend
```

### Step 5: Configure Nginx (Optional - Production)

```bash
sudo nano /etc/nginx/sites-available/oni-sqo-bulk
```

```nginx
server {
    listen 80;
    server_name oni-sqo.amdocs.com;  # Your domain

    # Frontend
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:5003;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/oni-sqo-bulk /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 6: Open Firewall Ports

```bash
# CentOS/RHEL
sudo firewall-cmd --permanent --add-port=5003/tcp
sudo firewall-cmd --permanent --add-port=8080/tcp
sudo firewall-cmd --reload

# Ubuntu
sudo ufw allow 5003/tcp
sudo ufw allow 8080/tcp
```

### Step 7: Access the Application

```
http://<AMDOCS_SERVER_IP>:8080
```

---

## Option 3: Network Sharing (Quick Demo)

**Fastest way to share with team members on the same network:**

### Step 1: Find Your IP Address

```powershell
# Run this on your machine
ipconfig | findstr "IPv4"
```

### Step 2: Start with Network Binding

```powershell
# Double-click START_NETWORK.bat
# OR manually:

# Terminal 1 - Backend
cd C:\Users\abhisha3\Desktop\Projects\DOX\Orion-Agent\Demo\ONI-SQO-Bulk\backend
python app.py

# Terminal 2 - Frontend (bind to all interfaces)
cd C:\Users\abhisha3\Desktop\Projects\DOX\Orion-Agent\Demo\ONI-SQO-Bulk
python -m http.server 8080 --bind 0.0.0.0
```

### Step 3: Allow Through Windows Firewall

```powershell
# Run as Administrator
netsh advfirewall firewall add rule name="ONI-SQO Demo" dir=in action=allow protocol=tcp localport=5003
netsh advfirewall firewall add rule name="ONI-SQO Demo Frontend" dir=in action=allow protocol=tcp localport=8080
```

### Step 4: Share URL with Team

```
Your team can access:
http://<YOUR_IP>:8080

Example: http://10.161.45.123:8080
```

---

## Quick Reference Commands

### Windows (PowerShell)

```powershell
# Start Backend
cd backend; python app.py

# Start Frontend
python -m http.server 8080 --bind 0.0.0.0

# Check what's running on ports
netstat -ano | findstr ":5003 :8080"

# Kill process on port
$proc = Get-NetTCPConnection -LocalPort 5003 | Select -ExpandProperty OwningProcess; Stop-Process -Id $proc

# Get your IP
(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -notlike "*Loopback*"}).IPAddress
```

### Linux (Bash)

```bash
# Start Backend (background)
cd backend && nohup python app.py > backend.log 2>&1 &

# Start Frontend (background)
nohup python -m http.server 8080 --bind 0.0.0.0 > frontend.log 2>&1 &

# Check processes
ps aux | grep python

# Check ports
netstat -tlnp | grep -E "5003|8080"

# Kill process on port
fuser -k 5003/tcp

# Get your IP
hostname -I | awk '{print $1}'
```

---

## Troubleshooting

### Issue: "Connection Refused" or "Cannot Connect"

**Cause:** Firewall blocking ports

**Solution:**
```powershell
# Windows - Allow ports
netsh advfirewall firewall add rule name="App" dir=in action=allow protocol=tcp localport=5003
netsh advfirewall firewall add rule name="App" dir=in action=allow protocol=tcp localport=8080

# Temporarily disable firewall (testing only!)
netsh advfirewall set allprofiles state off
```

### Issue: "Address already in use"

**Cause:** Port already occupied

**Solution:**
```powershell
# Find and kill process on port
netstat -ano | findstr :5003
taskkill /F /PID <PID_NUMBER>
```

### Issue: API calls fail with CORS error

**Cause:** Frontend and Backend on different origins

**Solution:** Already handled in code. If still failing:
```python
# In backend/app.py, ensure CORS is configured:
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### Issue: Python not found on Remote Desktop

**Solution:**
```powershell
# Install Python
winget install Python.Python.3.11

# Or download manually from python.org
# Make sure to check "Add to PATH" during installation
```

### Issue: Cannot access from outside network

**Cause:** NAT/Router blocking external access

**Solution:**
1. Use VPN to connect to the same network
2. Configure port forwarding on router (if allowed)
3. Deploy on a server with public IP

---

## Environment Variables (Optional)

Create `.env` file for custom configuration:

```env
# Backend
FLASK_HOST=0.0.0.0
FLASK_PORT=5003
FLASK_DEBUG=false

# API Endpoints (update for your environment)
SQO_API_URL=https://xsqo-intg2.np.xtify.io
ONI_API_URL=https://dxhub-api-itg2.comcast.com

# Frontend
FRONTEND_PORT=8080
```

---

## Security Recommendations for Production

1. **Use HTTPS** - Configure SSL certificates
2. **Restrict CORS** - Change `"origins": "*"` to specific domains
3. **Add Authentication** - Implement login for the portal
4. **Use Environment Variables** - Don't hardcode credentials
5. **Enable Logging** - Configure proper logging for debugging
6. **Rate Limiting** - Prevent API abuse
7. **Regular Updates** - Keep dependencies updated

---

## Contact

For issues or questions, contact the Orion Team.

---
© 2026 Amdocs Orion Team
