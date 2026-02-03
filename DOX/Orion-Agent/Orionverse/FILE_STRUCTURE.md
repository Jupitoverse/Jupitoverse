# Orionverse - File Structure Guide

**Version**: 3.2  
**Last Updated**: November 2025

---

## 📁 Directory Structure Overview

```
Orionverse/
├── 📄 index.html                    # Main entry point - loads all pages
├── 📄 README.md                     # Project overview
├── 📄 REQUIREMENTS.md               # Dependencies and system requirements
├── 📄 requirements.txt              # Python dependencies
├── 📄 PROMPT_HISTORY.md             # All prompts and changes log
├── 📄 FILE_STRUCTURE.md             # This file
├── 📄 AVD_DEPLOYMENT_GUIDE.md       # AVD deployment instructions
│
├── 📂 backend/                      # Flask backend application
│   ├── 📄 app.py                    # Main Flask app (entry point)
│   ├── 📄 database.py               # Database connection & queries
│   ├── 📄 schema_workarounds_enhanced.sql  # Database schema
│   ├── 📄 debug_search.py           # Search debugging utilities
│   ├── 📄 test_backend_live.py      # Backend testing script
│   │
│   ├── 📂 routes/                   # API endpoints
│   │   ├── 📄 __init__.py           # Routes package initializer
│   │   ├── 📄 auth.py               # Authentication routes
│   │   ├── 📄 search.py             # Search API endpoints
│   │   ├── 📄 bulk_handling.py      # Bulk operations API
│   │   ├── 📄 billing.py            # Billing routes
│   │   ├── 📄 workarounds_enhanced.py  # Enhanced workaround system
│   │   └── 📄 workarounds.py        # Basic workaround routes (legacy)
│   │
│   └── 📂 data/                     # JSON data storage
│       ├── 📄 sr_data.json          # Service Request data
│       └── 📄 defect_data.json      # Defect tracking data
│
├── 📂 static/                       # Frontend static files
│   ├── 📂 css/
│   │   └── 📄 style.css             # Main stylesheet (dark theme)
│   │
│   └── 📂 js/                       # JavaScript files
│       ├── 📄 main.js               # Navigation & page loading
│       ├── 📄 api.js                # API communication layer
│       ├── 📄 auth.js               # Authentication logic
│       ├── 📄 search.js             # Search functionality
│       ├── 📄 bulk_handling.js      # Bulk operations tab switching
│       ├── 📄 bulk_handling_tabs.js # Alternative tab handler (backup)
│       └── 📄 abbreviations.js      # Abbreviations page logic
│
├── 📂 templates/                    # HTML page templates
│   ├── 📄 home.html                 # Home page with quick links
│   ├── 📄 search_anything.html      # Search engine (primary feature)
│   ├── 📄 bulk_handling.html        # Bulk operations (6 tabs)
│   ├── 📄 abbreviation.html         # Abbreviations & acronyms
│   ├── 📄 welcome-kit.html          # New joiner access guide
│   ├── 📄 billing.html              # Billing information
│   ├── 📄 training.html             # Training resources
│   ├── 📄 release.html              # Release management
│   ├── 📄 database.html             # Database management
│   ├── 📄 assignments.html          # Assignment tracking
│   ├── 📄 events.html               # Events calendar
│   └── 📄 imp-links.html            # Important links
│
├── 📂 docs/                         # Documentation files
│   ├── 📄 PROJECT_CONTEXT.md        # Complete project history & context
│   ├── 📄 ARCHITECTURE.md           # System architecture
│   ├── 📄 DEVELOPER_GUIDE.md        # Developer documentation
│   ├── 📄 QUICK_START.md            # Quick start guide
│   ├── 📄 CHANGELOG.md              # Version history
│   │
│   ├── 📄 SEARCH_ENGINE_GUIDE.md    # Search functionality docs
│   ├── 📄 SEARCH_UI_UPDATES.md      # Search UI changes
│   │
│   ├── 📄 BULK_HANDLING_GUIDE.md    # Bulk operations guide
│   ├── 📄 BULK_HANDLING_UI_SPEC.md  # Bulk handling UI specs
│   ├── 📄 BULK_HANDLING_SUMMARY.txt # Bulk handling summary
│   │
│   ├── 📄 WORKAROUND_SETUP_GUIDE.md # Workaround system setup
│   ├── 📄 WORKAROUND_FEATURES_SUMMARY.md  # Workaround features
│   ├── 📄 QUICK_START_WORKAROUNDS.md  # Workaround quick start
│   ├── 📄 IMAGE_SUPPORT_GUIDE.md    # Image support in workarounds
│   │
│   ├── 📄 NETWORK_DEPLOYMENT_GUIDE.md  # Network deployment
│   ├── 📄 QUICK_NETWORK_SETUP.md    # Quick network setup
│   ├── 📄 DEPLOYMENT_CHECKLIST.md   # Deployment checklist
│   ├── 📄 DEPLOYMENT_SUMMARY.txt    # Deployment summary
│   ├── 📄 README_AVD_DEPLOYMENT.md  # AVD deployment overview
│   ├── 📄 SETUP_COMPLETE.md         # Setup completion guide
│   │
│   └── 📄 QUICK_REFERENCE.md        # Quick reference card
│
└── 📂 scripts/                      # Utility scripts
    ├── 📄 START_BACKEND.bat         # Start local backend (Windows)
    ├── 📄 START_NETWORK_BACKEND.bat # Start network backend (Windows)
    ├── 📄 setup_avd.ps1             # Automated AVD setup (PowerShell)
    ├── 📄 test_network_access.ps1   # Network diagnostics (PowerShell)
    ├── 📄 convert_excel.py          # Excel to JSON converter
    └── 📄 test_api.html             # API testing page
```

---

## 📄 Key Files Explained

### **Root Level Files**

| File | Purpose |
|------|---------|
| `index.html` | Main HTML entry point. Loads all JavaScript and routes to different pages |
| `README.md` | Project overview, features, and basic usage |
| `REQUIREMENTS.md` | System requirements, dependencies, and installation instructions |
| `requirements.txt` | Python package dependencies (used by pip) |
| `PROMPT_HISTORY.md` | Complete history of all prompts and changes made |
| `FILE_STRUCTURE.md` | This file - explains project structure |
| `AVD_DEPLOYMENT_GUIDE.md` | Step-by-step AVD deployment guide |

---

### **Backend Files**

#### **`backend/app.py`**
- **Purpose**: Main Flask application entry point
- **What it does**: 
  - Creates Flask app
  - Registers all blueprints (routes)
  - Configures CORS
  - Starts web server on port 5001
  - Network deployment configuration

#### **`backend/database.py`**
- **Purpose**: Database connection and queries
- **What it does**:
  - PostgreSQL connection management
  - User authentication queries
  - Workaround CRUD operations
  - Data retrieval functions

#### **`backend/routes/`**
All API endpoint handlers:

| File | API Prefix | Purpose |
|------|------------|---------|
| `auth.py` | `/api/auth` | User login, logout, session management |
| `search.py` | `/api/search` | Search across SR, Defects, Workarounds |
| `bulk_handling.py` | `/api/bulk-handling` | Bulk operations (6 types) |
| `billing.py` | `/api/billing` | Billing information retrieval |
| `workarounds_enhanced.py` | `/api/workarounds` | Full workaround system with comments, likes, shares |
| `workarounds.py` | - | Legacy workaround routes (backup) |

---

### **Frontend Files**

#### **`static/js/main.js`**
- **Purpose**: Main application controller
- **What it does**:
  - Navigation management
  - Page routing (hash-based)
  - Loads HTML templates dynamically
  - Fires `pageLoaded` events
  - Navigation bar generation

#### **`static/js/api.js`**
- **Purpose**: API communication layer
- **What it does**:
  - Dynamic API URL detection (local vs network)
  - Fetch wrapper functions
  - Error handling
  - Request/response logging

#### **`static/js/search.js`**
- **Purpose**: Search functionality
- **What it does**:
  - Search form handling
  - Filter management
  - Results display
  - Pagination

#### **`static/js/bulk_handling.js`**
- **Purpose**: Bulk operations tab switching
- **What it does**:
  - Internal tab switching (6 tabs)
  - Line counters for text inputs
  - Event delegation
  - Multiple initialization strategies

#### **`static/js/abbreviations.js`**
- **Purpose**: Abbreviations page logic
- **What it does**:
  - Loads 100+ abbreviations
  - Real-time search filtering
  - Card generation

#### **`static/css/style.css`**
- **Purpose**: Main stylesheet
- **What it does**:
  - Dark purple theme
  - Component styling
  - Responsive design
  - Animations and transitions

---

### **Template Files**

All HTML files in `templates/` are page fragments loaded by `index.html`:

| File | Tab Name | Purpose |
|------|----------|---------|
| `home.html` | Home | Landing page with quick links |
| `search_anything.html` | Search Anything | Primary search feature |
| `bulk_handling.html` | Bulk Handling | 6 bulk operation tabs |
| `abbreviation.html` | Abbreviation | Abbreviations & acronyms (120+) |
| `welcome-kit.html` | Welcome Kit | New joiner guide (apps + DB creds) |
| `billing.html` | Billing | Billing dashboards |
| `training.html` | Training | Training materials |
| `release.html` | Release | Release management |
| `database.html` | DataBase | Database tools |
| `assignments.html` | Assignments | Assignment tracking |
| `events.html` | Events | Events calendar |
| `imp-links.html` | Imp Links | Important links |

---

## 🔄 Data Flow

### Page Load Flow
```
1. User opens index.html
2. index.html loads all JS files (main.js, api.js, etc.)
3. main.js reads hash (e.g., #search-anything)
4. main.js fetches templates/search_anything.html
5. Inserts HTML into <main> element
6. Fires pageLoaded event with pageId
7. Specific JS (e.g., search.js) initializes
```

### API Call Flow
```
1. User action (e.g., search submit)
2. Frontend JS calls function from api.js
3. api.js sends fetch request to Flask backend
4. Backend route handler processes request
5. database.py queries PostgreSQL or JSON files
6. Backend returns JSON response
7. Frontend JS updates UI with results
```

### Tab Switching Flow (Bulk Handling)
```
1. User clicks tab button (e.g., "Bulk Force Complete")
2. bulk_handling.js detects click event
3. Removes 'active' class from all tabs
4. Adds 'active' class to clicked tab
5. Corresponding content div becomes visible
6. Line counter initializes for that tab's textarea
```

---

## 🚀 Startup Sequence

### Local Development
```
1. Run scripts/START_BACKEND.bat
2. Flask starts on localhost:5001
3. Open browser to http://localhost:5001
4. index.html loads
5. Application ready
```

### Network Deployment
```
1. Run scripts/START_NETWORK_BACKEND.bat
2. Flask starts on 0.0.0.0:5001 (all interfaces)
3. Open browser to http://<machine-ip>:5001
4. Firewall allows port 5001
5. Application accessible on network
```

---

## 🔧 Modification Guide

### To Add a New Page
1. Create `templates/new_page.html`
2. Add entry to `NAV_CONFIG.links` in `static/js/main.js`
3. Optionally create `static/js/new_page.js` for page-specific logic
4. Add script tag in `index.html` if needed

### To Add a New API Endpoint
1. Add route function in appropriate `backend/routes/*.py` file
2. Or create new routes file and register blueprint in `app.py`
3. Update API documentation in `docs/`

### To Modify Styling
1. Edit `static/css/style.css`
2. Or add `<style>` tag in specific template file
3. Follow dark purple theme (primary: #8b5cf6)

---

## 📦 Deployment Files

| File | Purpose | When to Use |
|------|---------|-------------|
| `AVD_DEPLOYMENT_GUIDE.md` | Full AVD deployment guide | Deploying to AVD |
| `scripts/setup_avd.ps1` | Automated AVD setup | First-time AVD setup |
| `scripts/START_NETWORK_BACKEND.bat` | Start network server | Network deployment |
| `scripts/test_network_access.ps1` | Network diagnostics | Troubleshooting network issues |
| `requirements.txt` | Python dependencies | Any deployment |

---

## 📚 Documentation Files

All in `docs/` folder:

| Category | Files |
|----------|-------|
| **Project Overview** | PROJECT_CONTEXT.md, README.md, ARCHITECTURE.md |
| **Getting Started** | QUICK_START.md, DEVELOPER_GUIDE.md, QUICK_REFERENCE.md |
| **Features** | SEARCH_ENGINE_GUIDE.md, BULK_HANDLING_GUIDE.md, WORKAROUND_SETUP_GUIDE.md |
| **Deployment** | NETWORK_DEPLOYMENT_GUIDE.md, AVD_DEPLOYMENT_GUIDE.md, DEPLOYMENT_CHECKLIST.md |
| **History** | CHANGELOG.md, PROMPT_HISTORY.md |

---

## 🗑️ Files You Can Ignore

- `backend/__pycache__/` - Python compiled files (auto-generated)
- `backend/routes/__pycache__/` - Python compiled files (auto-generated)
- `static/js/bulk_handling_tabs.js` - Backup file (not used)
- `backend/routes/workarounds.py` - Legacy file (use workarounds_enhanced.py)

---

## 💡 Tips

1. **Finding Files**: Use Ctrl+P in VS Code to quickly find files
2. **Search in Files**: Use Ctrl+Shift+F to search across all files
3. **Documentation**: Always check `docs/PROJECT_CONTEXT.md` first
4. **Deployment**: Use `AVD_DEPLOYMENT_GUIDE.md` for step-by-step deployment
5. **Troubleshooting**: Check console logs (F12 in browser) and Flask logs

---

**Last Updated**: November 2025  
**Maintainer**: Orion Team


