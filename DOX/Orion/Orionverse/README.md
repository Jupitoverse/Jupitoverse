# 🌌 Orionverse Hub

**Orionverse Hub** is a centralized web application serving as the single source of truth for team resources, documentation, tools, and automation workflows within the Orion ecosystem.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Setup & Installation](#setup--installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
- [Development](#development)
- [Security Notes](#security-notes)
- [Contributing](#contributing)

---

## ✨ Features

### Core Modules

| Module | Description |
|--------|-------------|
| 🏠 **Home** | Quick links dashboard for easy navigation |
| 🔎 **Search Anything** | Multi-source search across SR data, Defects, and Workarounds |
| ⚡ **Bulk Handling** | Bulk operations (Retry, Force Complete, Re-execute, Resolve Error, Stuck Activity, Flag Release) |
| 💳 **Billing** | Billing dashboards and data analysis tools |
| 🎓 **Training** | Onboarding materials and knowledge transfer documents |
| 🤖 **Automation** | Automated workflow tools and scripts |
| 🚀 **Release** | Release schedules, deployment steps, and PONR tracking |
| 👋 **Welcome Kit** | Team onboarding resources, applications list, and DB credentials |
| 💻 **Applications** | Links and documentation for common applications |
| 🔤 **Abbreviations** | Glossary of 120+ terms and acronyms with search |
| 👥 **Teams** | Team directory and contact information |
| 🔗 **Important Links** | Curated collection of essential URLs |
| 🗄️ **Database** | Database schemas, queries, and tools |
| 📅 **Events** | Event calendar and schedules |
| 📝 **Assignments** | Task and assignment tracking |

### Technical Features

- **Multi-source Search**: Search across PostgreSQL database and JSON data sources simultaneously
- **Bulk Operations**: 6 powerful bulk handling operations with confirmation popups
- **Workaround System**: Collaborative workaround management with comments, likes, and sharing
- **SPA Architecture**: Single-page application with hash-based routing for smooth navigation
- **RESTful API**: Flask backend with modular blueprint architecture
- **Authentication System**: User management with login/signup functionality
- **Real-time Data**: Dynamic content loading from multiple data sources
- **Network Deployment**: Ready for AVD deployment with automated setup scripts

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         Frontend (Vanilla JS)           │
│  ┌──────────────────────────────────┐   │
│  │  index.html (SPA Shell)          │   │
│  │  ├── main.js (Router)            │   │
│  │  ├── auth.js (Authentication)    │   │
│  │  ├── search.js (Search Logic)    │   │
│  │  └── api.js (HTTP Client)        │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
                    ↕ HTTP/REST
┌─────────────────────────────────────────┐
│         Backend (Flask)                 │
│  ┌──────────────────────────────────┐   │
│  │  app.py (Application Factory)    │   │
│  │  ├── routes/auth.py              │   │
│  │  ├── routes/search.py            │   │
│  │  ├── routes/billing.py           │   │
│  │  └── routes/workarounds.py       │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────┐
│         Data Layer                      │
│  ├── PostgreSQL (Workarounds, Users)   │
│  └── JSON Files (SR Data, Defects)     │
└─────────────────────────────────────────┘
```

**Tech Stack:**
- **Backend**: Python 3.x, Flask, Flask-CORS
- **Database**: PostgreSQL (via psycopg2)
- **Frontend**: Vanilla JavaScript (ES6+), HTML5, CSS3
- **Additional**: jQuery DataTables, Quill.js (Rich Text Editor)

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.7+
- PostgreSQL database access
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Projects/Orion/Orionverse
   ```

2. **Set up Python virtual environment** (Recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask flask-cors psycopg2-binary
   ```

4. **Configure database connection**
   - Edit `backend/database.py` with your credentials
   - **⚠️ For production**: Use environment variables instead of hardcoded credentials

5. **Generate JSON data** (if SR/Defect Excel files exist)
   ```bash
   python convert_excel.py
   ```

6. **Run the application**
   ```bash
   cd backend
   python app.py
   ```

7. **Access the application**
   - Open your browser and navigate to: `http://localhost:5001`
   - Open `index.html` directly or serve via a local web server

---

## 📁 Project Structure

**For detailed file structure documentation, see [FILE_STRUCTURE.md](FILE_STRUCTURE.md)**

```
Orionverse/
│
├── 📄 index.html                    # Main SPA entry point
├── 📄 README.md                     # This file
├── 📄 REQUIREMENTS.md               # Dependencies & requirements
├── 📄 requirements.txt              # Python packages
├── 📄 FILE_STRUCTURE.md             # Detailed file guide
├── 📄 PROMPT_HISTORY.md             # Complete project history
├── 📄 AVD_DEPLOYMENT_GUIDE.md       # AVD deployment guide
│
├── 📂 backend/                      # Flask backend
│   ├── app.py                       # Main application
│   ├── database.py                  # Database layer
│   ├── routes/                      # API endpoints
│   │   ├── auth.py                  # Authentication
│   │   ├── search.py                # Search API
│   │   ├── bulk_handling.py         # Bulk operations
│   │   ├── billing.py               # Billing
│   │   └── workarounds_enhanced.py  # Workarounds
│   └── data/                        # JSON data
│       ├── sr_data.json
│       └── defect_data.json
│
├── 📂 static/                       # Frontend assets
│   ├── css/
│   │   └── style.css                # Main stylesheet
│   └── js/
│       ├── main.js                  # Router & navigation
│       ├── api.js                   # API client
│       ├── auth.js                  # Authentication
│       ├── search.js                # Search logic
│       ├── bulk_handling.js         # Tab switching
│       └── abbreviations.js         # Abbreviations page
│
├── 📂 templates/                    # HTML templates
│   ├── home.html
│   ├── search_anything.html
│   ├── bulk_handling.html          # NEW
│   ├── abbreviation.html           # NEW
│   ├── welcome-kit.html            # NEW
│   ├── billing.html
│   ├── training.html
│   ├── release.html
│   ├── database.html
│   └── [other pages]
│
├── 📂 docs/                         # 📚 Documentation
│   ├── PROJECT_CONTEXT.md           # Complete history
│   ├── ARCHITECTURE.md
│   ├── DEVELOPER_GUIDE.md
│   ├── BULK_HANDLING_GUIDE.md
│   ├── WORKAROUND_SETUP_GUIDE.md
│   ├── NETWORK_DEPLOYMENT_GUIDE.md
│   └── [20+ other docs]
│
└── 📂 scripts/                      # ⚙️ Utilities
    ├── START_BACKEND.bat
    ├── START_NETWORK_BACKEND.bat
    ├── setup_avd.ps1
    ├── test_network_access.ps1
    └── convert_excel.py
```

---

## 🎯 Usage

### Starting the Backend Server

**Quick Start:**
```bash
# Use pre-built script (Windows)
scripts\START_BACKEND.bat

# OR manually:
cd backend
python app.py
```

The Flask server will start on `http://localhost:5001`

**For network deployment**, see [AVD_DEPLOYMENT_GUIDE.md](AVD_DEPLOYMENT_GUIDE.md)

### Accessing the Frontend

Open `index.html` in a web browser, or use a local server:

```bash
# Using Python's built-in server (from Orionverse root)
python -m http.server 8000

# Then navigate to: http://localhost:8000
```

### Navigation

- Use the top navigation bar to switch between modules
- The app uses hash-based routing (e.g., `#home`, `#search-anything`, `#billing`)
- All navigation happens client-side without page reloads

---

## 🛠️ Development

### Adding a New Module

1. **Create template file**: Add `templates/your-module.html`
2. **Register route**: Update `NAV_CONFIG` in `static/js/main.js`
3. **Add backend route** (if needed): Create `backend/routes/your-module.py`
4. **Register blueprint**: Add to `backend/app.py`

### Database Schema

#### Workarounds Table
```sql
CREATE TABLE workarounds (
    id SERIAL PRIMARY KEY,
    category VARCHAR(255),
    issue TEXT,
    description TEXT,
    created_by VARCHAR(255),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### API Endpoints

#### Search
- `GET /api/search/all` - Fetch top 10 records from all sources
- `POST /api/search/filter` - Filter data with search parameters

#### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/login` - User login

#### Workarounds
- `GET /api/workarounds/` - List all workarounds
- `POST /api/workarounds/` - Create new workaround
- `PUT /api/workarounds/<id>` - Update workaround
- `DELETE /api/workarounds/<id>` - Delete workaround

---

## 🔒 Security Notes

**⚠️ IMPORTANT**: This application currently contains security vulnerabilities that should be addressed before production deployment:

1. **Hardcoded Database Credentials**: 
   - Current: Credentials in `backend/database.py`
   - Fix: Move to environment variables using `python-dotenv`

2. **No Password Hashing**: 
   - Implement `bcrypt` or similar for password storage

3. **No Authentication Middleware**: 
   - Add JWT or session-based authentication

4. **CORS Wide Open**: 
   - Restrict CORS to specific origins in production

5. **No Input Validation**: 
   - Add input sanitization and validation

### Recommended Security Improvements

```bash
# Install security packages
pip install python-dotenv bcrypt flask-jwt-extended

# Create .env file (add to .gitignore)
DB_HOST=your-host
DB_NAME=your-db
DB_USER=your-user
DB_PASSWORD=your-password
SECRET_KEY=your-secret-key
```

---

## 🤝 Contributing

### Commit Message Convention

```
type(scope): subject

Examples:
feat(search): add advanced filtering options
fix(billing): resolve data loading issue
docs(readme): update installation steps
refactor(auth): improve error handling
```

### Branching Strategy

- `main` - Production-ready code
- `develop` - Development branch
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Urgent production fixes

### Before Committing

1. Test your changes locally
2. Ensure no sensitive data is committed
3. Update documentation if needed
4. Run linting (if configured)

---

## 📝 License

Internal company project - Not for public distribution

---

## 👥 Team

Maintained by the Orion Operations Team

---

## 📞 Support

For issues, questions, or feature requests, please contact the team or create an issue in the repository.

---

**Last Updated**: November 4, 2025  
**Version**: 3.2

