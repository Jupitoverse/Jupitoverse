# ONI-SQO-Bulk Console

A lightweight web application for SQO, ONI API operations and Bulk Handling.

## 🚀 Quick Start

### Local Development
```bash
# Double-click the batch file:
START_APP.bat
```
Or manually:
```bash
# Terminal 1 - Backend
cd backend
py -3.11 app.py

# Terminal 2 - Frontend
py -3.11 -m http.server 8080
```

### Network/Remote Deployment
```bash
# Double-click:
START_NETWORK.bat
```
This will:
- Start backend on `0.0.0.0:5001` (accessible from network)
- Start frontend on `0.0.0.0:8080` (accessible from network)
- Display your local IP for sharing

## 📋 Features

### ⚡ SQO Tab
- Billing Manual Call
- Submit to Delivery
- Set Product Status
- Send to Fulfillment
- Quote Alignment

### 🔮 ONI Tab
- Search by Customer ID
- Search by External Service ID
- Search by Product ID
- Search by Site ID
- Custom GraphQL Query

### 📦 Bulk Tab
- Create batch tasks
- Execute tasks
- View results
- Export data

## 🔧 Configuration

### Backend Port
Edit `backend/app.py`:
```python
CONFIG = {
    'host': '0.0.0.0',  # Listen on all interfaces
    'port': 5001,       # Change port here
    'debug': False,     # Set to False for production
}
```

### API Credentials
Edit `backend/routes/sqo_api.py` and `oni_api.py` to update:
- API URLs
- Client credentials
- Authentication tokens

## 📁 Project Structure
```
ONI-SQO-Bulk/
├── backend/
│   ├── app.py              # Flask application
│   └── routes/
│       ├── sqo_api.py      # SQO endpoints
│       ├── oni_api.py      # ONI endpoints
│       └── bulk_handling.py # Bulk operations
├── static/
│   ├── css/style.css       # Styles
│   └── js/
│       ├── main.js         # Navigation
│       └── api_console.js  # API modules
├── templates/
│   ├── sqo.html            # SQO tab
│   ├── oni.html            # ONI tab
│   └── bulk.html           # Bulk tab
├── index.html              # Main entry
├── requirements.txt        # Python deps
├── START_APP.bat           # Local startup
└── START_NETWORK.bat       # Network startup
```

## 🌐 Remote Desktop / Server Deployment

1. **Copy the entire `ONI-SQO-Bulk` folder** to the remote machine

2. **Install Python 3.11+** if not installed

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the network startup script:**
   ```bash
   START_NETWORK.bat
   ```

5. **Access from any machine** using the displayed IP:
   ```
   http://<SERVER_IP>:8080
   ```

## 🔒 Firewall Configuration

If accessing from other machines, ensure these ports are open:
- **5001** - Backend API
- **8080** - Frontend UI

### Windows Firewall
```powershell
# Run as Administrator
netsh advfirewall firewall add rule name="ONI-SQO-Bulk Backend" dir=in action=allow protocol=tcp localport=5001
netsh advfirewall firewall add rule name="ONI-SQO-Bulk Frontend" dir=in action=allow protocol=tcp localport=8080
```

## 📞 Support

For issues or questions, contact the Orion Team.

---
© 2026 Amdocs Orion Team
