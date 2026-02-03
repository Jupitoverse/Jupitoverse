# Orionverse - Requirements

**Version**: 3.2  
**Last Updated**: November 2025

---

## 📋 Python Dependencies

```
Flask==3.0.0
Flask-Cors==4.0.0
psycopg2-binary==2.9.9
pandas==2.1.0
SQLAlchemy==2.0.23
requests==2.31.0
python-dotenv==1.0.0
```

### Installation
```bash
pip install -r requirements.txt
```

---

## 🗄️ Database Requirements

### PostgreSQL
- **Version**: 10.x or higher
- **Required**: For production deployment
- **Tables**: 
  - Workaround system (7 tables)
  - User management
  - Activity logs

### JSON Data Files
- `backend/data/sr_data.json` - Service Request data
- `backend/data/defect_data.json` - Defect tracking data

---

## 🌐 Frontend Dependencies

### CDN Libraries (Auto-loaded)
- **Quill.js** (v1.3.6) - Rich text editor for workarounds
- **jQuery** (v3.7.0) - DOM manipulation
- **DataTables** (v1.13.6) - Table display and filtering

### Custom JavaScript Files
Located in `static/js/`:
- `main.js` - Main application logic & navigation
- `api.js` - API communication layer
- `auth.js` - Authentication handling
- `search.js` - Search functionality
- `bulk_handling.js` - Bulk operations tab switching
- `abbreviations.js` - Abbreviations page logic

### Custom CSS
- `static/css/style.css` - Main stylesheet (dark purple theme)

---

## 🖥️ System Requirements

### Development Environment
- **Python**: 3.8 or higher
- **Browser**: Chrome, Firefox, Edge (modern versions)
- **OS**: Windows 10+, Linux, macOS

### Network Deployment
- **Port**: 5001 (default)
- **Network Access**: Firewall configured for port 5001
- **Database Connection**: PostgreSQL accessible on network

### AVD (Azure Virtual Desktop) Deployment
- **Python**: Pre-installed or installable
- **Network**: Access to PostgreSQL database
- **Firewall**: Port 5001 open
- **VS Code**: For development (optional)

---

## 📁 Required Directory Structure

```
Orionverse/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── database.py         # Database connection
│   ├── data/
│   │   ├── sr_data.json
│   │   └── defect_data.json
│   └── routes/
│       ├── auth.py
│       ├── search.py
│       ├── bulk_handling.py
│       ├── billing.py
│       └── workarounds_enhanced.py
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── main.js
│       ├── api.js
│       ├── auth.js
│       ├── search.js
│       ├── bulk_handling.js
│       └── abbreviations.js
├── templates/
│   ├── home.html
│   ├── search_anything.html
│   ├── bulk_handling.html
│   ├── abbreviation.html
│   ├── welcome-kit.html
│   └── [other pages]
├── docs/                   # Documentation
├── scripts/                # Utility scripts
└── index.html             # Main entry point
```

---

## 🔐 Environment Variables (Optional)

Create `.env` file in root directory:

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=orionverse
DB_USER=your_username
DB_PASSWORD=your_password

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key

# API Configuration
API_BASE_URL=http://localhost:5001
```

---

## 🚀 Minimum Requirements for Running

### Local Development
1. Python 3.8+
2. Flask and dependencies installed
3. JSON data files present
4. Port 5001 available

### Network Deployment
1. All local requirements +
2. Network-accessible machine
3. Firewall configured
4. PostgreSQL database accessible
5. Database credentials configured

---

## 📦 Optional Components

### For Full Workaround System
- PostgreSQL database
- Database schema created (`backend/schema_workarounds_enhanced.sql`)
- User authentication configured

### For Search Functionality
- SR and Defect JSON data files populated
- Search indices built (automatic on first run)

### For Bulk Operations
- Backend routes configured
- Database connections established
- User permissions set

---

## 🔄 Upgrade Requirements

### From Version 2.x to 3.x
1. Update requirements.txt
2. Run `pip install -r requirements.txt --upgrade`
3. Create docs and scripts folders
4. Move files to new structure (see FILE_STRUCTURE.md)
5. Update any hardcoded paths
6. Restart Flask server

---

## ❓ Troubleshooting

### Missing Dependencies
```bash
pip install -r requirements.txt --force-reinstall
```

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5001
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5001 | xargs kill -9
```

### Database Connection Issues
1. Check PostgreSQL is running
2. Verify credentials in `database.py`
3. Test connection: `psql -h <host> -U <user> -d <database>`
4. Check firewall allows port 5432/6432

---

## 📞 Support

For issues:
1. Check `docs/PROJECT_CONTEXT.md` for complete project documentation
2. Review `docs/QUICK_START.md` for setup instructions
3. See `AVD_DEPLOYMENT_GUIDE.md` for AVD-specific setup
4. Contact Orion team for database credentials

---

**Last Review**: November 2025  
**Next Review**: Quarterly


