# 🏗️ Orionverse Hub - Technical Architecture

**Last Updated**: October 10, 2025  
**Version**: 1.0.0

---

## Table of Contents

1. [Overview](#overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Backend Architecture](#backend-architecture)
4. [Frontend Architecture](#frontend-architecture)
5. [Data Flow](#data-flow)
6. [Database Schema](#database-schema)
7. [API Endpoints](#api-endpoints)
8. [Security Considerations](#security-considerations)
9. [Development Guidelines](#development-guidelines)

---

## Overview

**Orionverse Hub** is a centralized web portal for Amdocs & Comcast support teams to search across multiple data sources and manage a knowledge base.

### Core Principles

1. **Separation of Concerns**: Backend and frontend are completely independent
2. **API-First Design**: Backend is purely an API server (no HTML rendering)
3. **Modular Architecture**: Each feature is a self-contained module
4. **Single-Page Application**: Frontend loads once, all navigation is client-side
5. **Multi-Source Data**: Aggregates data from PostgreSQL, Oracle, and JSON files

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3.x | Core language |
| | Flask | Web framework |
| | Flask-CORS | Cross-origin resource sharing |
| | psycopg2 | PostgreSQL adapter |
| | SQLAlchemy | Oracle database ORM |
| **Frontend** | HTML5/CSS3 | Structure and styling |
| | Vanilla JavaScript (ES6+) | Application logic |
| | jQuery | DOM manipulation (DataTables) |
| | DataTables | Table rendering and search |
| | Quill.js | Rich text editor |
| **Database** | PostgreSQL | Users, workarounds, billing data |
| | Oracle | Legacy billing system |
| **Data Files** | JSON | Pre-processed SR and defect data |

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USER BROWSER                          │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Frontend (SPA)                            │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │  index.html (Shell)                              │  │  │
│  │  │  ├─ Navigation Bar                               │  │  │
│  │  │  ├─ Content Area (dynamic)                       │  │  │
│  │  │  └─ Modal Containers                             │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  │                                                          │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │  JavaScript Modules                              │  │  │
│  │  │  ├─ main.js     (Router & Controller)           │  │  │
│  │  │  ├─ api.js      (HTTP Client)                    │  │  │
│  │  │  ├─ auth.js     (Authentication)                 │  │  │
│  │  │  └─ search.js   (Search Logic)                   │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↕
                    HTTP REST API (JSON)
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                   Backend API Server                         │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  app.py (Application Factory)                         │  │
│  │  ├─ Flask App Initialization                          │  │
│  │  ├─ CORS Configuration                                │  │
│  │  └─ Blueprint Registration                            │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  routes/ (Feature Blueprints)                         │  │
│  │  ├─ auth.py         → /api/auth/*                     │  │
│  │  ├─ workarounds.py  → /api/workarounds/*              │  │
│  │  ├─ search.py       → /api/search/*                   │  │
│  │  └─ billing.py      → /api/billing/*                  │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  database.py (Data Access Layer)                      │  │
│  │  ├─ get_db_connection()                               │  │
│  │  ├─ User Management Functions                         │  │
│  │  └─ Workaround CRUD Functions                         │  │
│  └────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                      Data Layer                              │
│  ┌────────────────┐  ┌────────────────┐  ┌──────────────┐   │
│  │  PostgreSQL    │  │  Oracle DB     │  │  JSON Files  │   │
│  │  ─────────────│  │  ─────────────│  │  ───────────│   │
│  │  • Users       │  │  • Billing     │  │  • sr_data   │   │
│  │  • Workarounds │  │    Data        │  │  • defects   │   │
│  │  • Billing Log │  │                │  │              │   │
│  └────────────────┘  └────────────────┘  └──────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## Backend Architecture

### Design Pattern: Flask Application Factory

The backend uses the **Application Factory Pattern** for maximum flexibility, testability, and scalability.

### File Structure and Responsibilities

```
backend/
├── app.py                  # Application Factory (Entry Point)
├── database.py             # Data Access Layer
├── routes/                 # Feature Modules (Blueprints)
│   ├── __init__.py
│   ├── auth.py            # Authentication & User Management
│   ├── workarounds.py     # Knowledge Base CRUD
│   ├── search.py          # Multi-Source Search Engine
│   └── billing.py         # Billing Tool Integration
└── data/                   # Static Data Sources
    ├── sr_data.json       # Service Request Data
    └── defect_data.json   # Defect Tracking Data
```

---

### 1. app.py - The Application Factory

**Role**: Main hub and switchboard for the entire backend.

**Responsibilities**:
- Initialize Flask application
- Configure CORS for frontend communication
- Register all feature blueprints
- Start the development server

**Key Principle**: This file should remain SIMPLE. It only initializes and connects modules.

```python
# Conceptual Structure
def create_app():
    1. Create Flask instance
    2. Apply CORS configuration
    3. Register all blueprints with URL prefixes
    4. Return configured app
```

**Why This Pattern?**
- Easy to test (can create multiple app instances)
- Clean separation of concerns
- Easy to add new features (just register new blueprints)
- Configuration flexibility (dev/staging/prod)

---

### 2. routes/ - Feature Blueprints

**Role**: The "departments" of your application. Each file handles one major feature.

#### Blueprint Pattern Benefits:
- **Modularity**: Each feature is self-contained
- **Scalability**: Add new features without touching existing code
- **Team Collaboration**: Different developers can work on different blueprints
- **Clear URL Structure**: `/api/feature/action`

---

#### A. auth.py - Authentication & User Management

**URL Prefix**: `/api/auth`

**Responsibilities**:
- User registration (signup)
- User authentication (login)
- Password verification
- Session management (frontend handles storage)

**Endpoints**:
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/login` - Authenticate user

**Data Flow**:
```
Frontend → POST /api/auth/login
         ↓
auth.py receives request
         ↓
Calls database.find_user_by_email()
         ↓
Verifies password with werkzeug.security
         ↓
Returns user object (without password) as JSON
```

**Security Notes**:
- Passwords are hashed using `werkzeug.security.generate_password_hash()`
- User status must be 'approved' to login
- Plain passwords are NEVER stored or returned

---

#### B. workarounds.py - Knowledge Base Management

**URL Prefix**: `/api/workarounds`

**Responsibilities**:
- CRUD operations for team workarounds
- View/like tracking
- Sorting by creation date

**Endpoints**:
- `GET /api/workarounds/` - List all workarounds
- `POST /api/workarounds/` - Create new workaround
- `PUT /api/workarounds/<id>` - Update existing workaround
- `DELETE /api/workarounds/<id>` - Delete workaround
- `POST /api/workarounds/<id>/view` - Increment view count
- `POST /api/workarounds/<id>/like` - Increment like count

**Database Integration**:
- Direct connection via `database.get_db_connection()`
- Uses `psycopg2.extras.RealDictCursor` for dict-like results
- All queries return/accept JSON

---

#### C. search.py - Multi-Source Search Engine

**URL Prefix**: `/api/search`

**Responsibilities**:
- Aggregate data from PostgreSQL, JSON files, and potentially Oracle
- Provide initial data load (top 10 records)
- Execute complex, multi-criteria searches
- Return unified results in consistent format

**Endpoints**:
- `GET /api/search/all` - Fetch top 10 from each source (initial load)
- `POST /api/search/filter` - Execute filtered search across all sources

**Data Sources**:
1. **PostgreSQL** (workarounds table)
2. **JSON Files** (sr_data.json, defect_data.json)
3. **Future**: Oracle billing database

**Search Algorithm**:
```
1. Load filters from request body
2. Apply filters to sr_data.json → filtered_sr
3. Apply filters to defect_data.json → filtered_defect
4. Query PostgreSQL with filters → filtered_workarounds
5. Combine all results
6. Return unified JSON response
```

**Performance Optimization**:
- JSON files loaded once at startup (not on every request)
- Initial load returns only 10 records to reduce payload
- Full search executes only when user submits filters

---

#### D. billing.py - Billing Tool Integration

**URL Prefix**: `/api/billing`

**Responsibilities**:
- Connect to Oracle database for billing data
- Connect to PostgreSQL for billing flag tracking
- Execute complex SQL queries
- Return formatted results

**Endpoints**:
- `GET /api/billing/data/<site_id>` - Fetch billing data for specific site

**Database Connections**:
1. **PostgreSQL**: Read-only connection for OSS data
2. **Oracle**: Billing system queries

**Future Enhancements**:
- Automated rebill analysis
- PONR (Point of No Return) tracking
- Billing flag management

---

### 3. database.py - Data Access Layer

**Role**: The ONLY file that should directly interact with PostgreSQL.

**Why Centralize Database Logic?**
- **Security**: Credentials in one place
- **Maintainability**: Change connection logic once, affects everywhere
- **Testability**: Easy to mock for testing
- **Consistency**: All queries use same connection pattern

**Key Functions**:

```python
get_db_connection()
    → Returns psycopg2 connection object
    → Handles connection errors gracefully
    → Returns None if connection fails

create_user(fullname, email, password)
    → Hashes password
    → Inserts new user with 'pending' status
    → Returns user dict or None if email exists

find_user_by_email(email)
    → Returns user dict or None
    → Used for login authentication

update_workaround(id, data)
    → Updates existing workaround
    → Returns True/False for success

delete_workaround(id)
    → Deletes workaround by ID
    → Returns True/False for success
```

**Connection Pattern**:
```python
# Standard pattern used throughout
conn = get_db_connection()
if not conn: return error_response

cur = conn.cursor(cursor_factory=RealDictCursor)
cur.execute("SQL QUERY", parameters)
result = cur.fetchall()
cur.close()
conn.close()
return result
```

---

### 4. data/ - Static JSON Data

**Purpose**: Pre-processed data files for high-speed searches.

**Why JSON instead of live database queries?**
- **Performance**: JSON reads are 10-100x faster than complex DB queries
- **Reduced Load**: No database connection overhead
- **Excel Integration**: Easy conversion from Excel via `convert_excel.py`
- **Caching**: Data loaded once at server startup

**Files**:
- `sr_data.json` - Service Request historical data
- `defect_data.json` - Defect tracking data

**Regeneration**: Run `convert_excel.py` when source Excel files are updated.

---

## Frontend Architecture

### Design Pattern: Single-Page Application (SPA)

The frontend is a **Single-Page Application** where navigation happens WITHOUT page reloads.

### File Structure and Responsibilities

```
frontend/
├── index.html              # Shell (loaded once)
├── templates/              # HTML Fragments
│   ├── home.html
│   ├── search_anything.html
│   ├── billing.html
│   ├── training.html
│   ├── release.html
│   ├── welcome-kit.html
│   ├── database.html
│   ├── imp-links.html
│   ├── events.html
│   └── assignments.html
├── static/
│   ├── css/
│   │   └── style.css      # Global styles
│   └── js/
│       ├── main.js        # Router & Controller
│       ├── api.js         # HTTP Client
│       ├── auth.js        # Authentication UI
│       └── search.js      # Search Module
```

---

### 1. index.html - The Application Shell

**Role**: The only "real" HTML page. Loads once and never reloads.

**Structure**:
```html
<!DOCTYPE html>
<html>
<head>
    <!-- CSS and external libraries -->
</head>
<body>
    <header>
        <nav id="main-nav">
            <!-- Navigation populated by main.js -->
        </nav>
        <div id="user-actions-container">
            <!-- Login/User info populated by auth.js -->
        </div>
    </header>

    <main id="app-content">
        <!-- Dynamic content injected here by main.js -->
    </main>

    <div id="auth-modal-container"></div>
    <div id="workaround-modal-container"></div>

    <!-- JavaScript modules loaded in specific order -->
    <script src="static/js/api.js"></script>
    <script src="static/js/auth.js"></script>
    <script src="static/js/search.js"></script>
    <script src="static/js/main.js"></script>
</body>
</html>
```

**Key Principles**:
- Acts as a "stage" - the structure never changes
- All content is dynamically injected
- Scripts loaded in dependency order (api → auth → features → main)

---

### 2. templates/*.html - HTML Fragments

**Role**: Partial HTML snippets that get injected into `#app-content`.

**Key Characteristics**:
- **NOT** complete HTML documents
- No `<html>`, `<head>`, or `<body>` tags
- Start directly with content (`<div>`, `<h1>`, etc.)
- Can contain embedded JavaScript event handlers

**Example**: `templates/home.html`
```html
<div class="page" id="home-page">
    <h1>Welcome to Orionverse</h1>
    <div class="quick-links-grid">
        <!-- Content -->
    </div>
</div>
```

---

### 3. static/js/main.js - Router & Controller

**Role**: The "brain" of the frontend. Orchestrates everything.

**Responsibilities**:
1. Define navigation configuration (NAV_CONFIG)
2. Handle hash-based routing (`#home`, `#search-anything`)
3. Load appropriate HTML templates
4. Update navigation bar to show active page
5. Initialize other modules (Auth, SearchAnything)
6. Dispatch page load events

**Navigation Flow**:
```
User clicks "Search Anything"
         ↓
URL changes to #search-anything
         ↓
'hashchange' event fires
         ↓
handleNavigation() executes
         ↓
Finds matching page in NAV_CONFIG
         ↓
loadPage() fetches templates/search_anything.html
         ↓
Injects HTML into #app-content
         ↓
Dispatches 'pageLoaded' event
         ↓
search.js listens and initializes
```

**Key Configuration**:
```javascript
const NAV_CONFIG = {
    links: [
        { id: 'home', text: 'Home', file: 'templates/home.html' },
        { id: 'search-anything', text: 'Search Anything', file: 'templates/search_anything.html' },
        // ... more pages
    ]
};
```

**Adding a New Page**:
1. Create `templates/new-page.html`
2. Add entry to NAV_CONFIG
3. Done! Routing is automatic.

---

### 4. static/js/api.js - HTTP Client

**Role**: The ONLY file that makes HTTP requests to the backend.

**Responsibilities**:
- Define backend URL (`API_BASE_URL`)
- Provide clean, reusable functions for each endpoint
- Handle errors gracefully
- Parse JSON responses
- Throw errors for non-200 responses

**Pattern**:
```javascript
const API = {
    login: (email, password) => {
        return fetchAPI('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
    },
    
    getWorkarounds: () => fetchAPI('/api/workarounds/'),
    
    // ... more endpoints
};
```

**Benefits**:
- All API endpoints documented in one place
- Easy to update if backend changes
- Consistent error handling
- No fetch() calls scattered throughout code

---

### 5. static/js/auth.js - Authentication Module

**Role**: Manage user session and authentication UI.

**Responsibilities**:
- Display login/signup modal
- Handle form submissions
- Store user info in sessionStorage
- Show "Welcome, [Name]" or "Sign In" button
- Handle logout

**Key Functions**:
```javascript
Auth.init()           // Check for existing session on load
Auth.render()         // Update UI based on login status
Auth.showModal()      // Display login/signup form
Auth.handleLogin()    // Process login form
Auth.handleSignup()   // Process signup form
Auth.logout()         // Clear session
```

**Session Storage**:
- Uses `sessionStorage` (cleared when browser closes)
- Stores: `{ fullname, email, role }`
- Does NOT store password or sensitive data

---

### 6. static/js/search.js - Search Feature Module

**Role**: Complex logic specific to the "Search Anything" page.

**Responsibilities**:
- Listen for 'pageLoaded' event with id='search-anything'
- Fetch initial data from backend
- Render data tables and cards
- Handle search form submission
- Manage add/edit workaround modal
- Execute filters and update display

**Initialization Pattern**:
```javascript
const SearchAnything = {
    init() {
        document.addEventListener('pageLoaded', (e) => {
            if (e.detail.pageId === 'search-anything') {
                this.setupPage();
            }
        });
    },
    
    async setupPage() {
        // Load data, set up event listeners, etc.
    }
};
```

**Why This Pattern?**
- Code only runs when needed
- Doesn't conflict with other pages
- Easy to add more feature modules

---

### 7. static/css/style.css - Global Styles

**Role**: Define the visual appearance of the entire application.

**Organization**:
```css
/* 1. CSS Variables (colors, spacing) */
:root { --primary-color: #007bff; }

/* 2. Reset and Base Styles */
* { box-sizing: border-box; }

/* 3. Layout */
.app-header { ... }
.app-content { ... }

/* 4. Components */
.modal-overlay { ... }
.quick-link-card { ... }

/* 5. Page-Specific Styles */
#search-anything { ... }

/* 6. Responsive Design */
@media (max-width: 768px) { ... }
```

---

## Data Flow

### Example Flow: User Login

```
1. USER ACTION
   └─→ User clicks "Sign In" button

2. FRONTEND (auth.js)
   └─→ Auth.showModal(true) displays login form
   └─→ User enters email/password
   └─→ User submits form
   └─→ Auth.handleLogin() is called

3. API LAYER (api.js)
   └─→ API.login(email, password)
   └─→ POST http://127.0.0.1:5001/api/auth/login
   └─→ Headers: { 'Content-Type': 'application/json' }
   └─→ Body: { "email": "...", "password": "..." }

4. BACKEND (routes/auth.py)
   └─→ @auth_bp.route('/login') receives request
   └─→ Extracts email and password from JSON
   └─→ Calls database.find_user_by_email(email)

5. DATABASE LAYER (database.py)
   └─→ get_db_connection() establishes connection
   └─→ SELECT * FROM users WHERE email = %s
   └─→ Returns user dict or None

6. BACKEND (routes/auth.py continued)
   └─→ Verifies password with check_password_hash()
   └─→ Checks user status == 'approved'
   └─→ Returns JSON: { "user": { "fullname": "...", "email": "...", "role": "..." }}

7. FRONTEND (auth.js continued)
   └─→ Receives user data
   └─→ Stores in sessionStorage
   └─→ Sets Auth.currentUser
   └─→ Calls Auth.render()
   └─→ Updates UI to show "Welcome, [Name]"
   └─→ Hides modal
```

---

### Example Flow: Multi-Source Search

```
1. USER ACTION
   └─→ Navigates to #search-anything

2. FRONTEND (main.js)
   └─→ Loads templates/search_anything.html
   └─→ Dispatches 'pageLoaded' event

3. FRONTEND (search.js)
   └─→ Listens for event
   └─→ Calls SearchAnything.setupPage()
   └─→ Calls API.getAllSearchData()

4. API LAYER (api.js)
   └─→ GET http://127.0.0.1:5001/api/search/all

5. BACKEND (routes/search.py)
   └─→ @search_bp.route('/all') executes
   └─→ Reads sr_data[:10] from JSON file
   └─→ Reads defect_data[:10] from JSON file
   └─→ Queries PostgreSQL: SELECT * FROM workarounds LIMIT 10
   └─→ Combines data: { sr_data: [...], defect_data: [...], wa_data: [...] }
   └─→ Returns JSON

6. FRONTEND (search.js continued)
   └─→ Receives data
   └─→ Calls displaySRData(), displayDefectData(), displayWAData()
   └─→ User sees tables populated

7. USER ACTION
   └─→ User enters search term "billing issue"
   └─→ User clicks "Search" button

8. FRONTEND (search.js)
   └─→ Collects form data
   └─→ Calls API.filterAllData({ search_anything: "billing issue" })

9. API LAYER (api.js)
   └─→ POST http://127.0.0.1:5001/api/search/filter
   └─→ Body: { "search_anything": "billing issue" }

10. BACKEND (routes/search.py)
    └─→ @search_bp.route('/filter') executes
    └─→ Filters sr_data (all matching rows)
    └─→ Filters defect_data (all matching rows)
    └─→ Queries PostgreSQL with ILIKE for "billing issue"
    └─→ Returns all matching results

11. FRONTEND (search.js)
    └─→ Receives filtered data
    └─→ Re-renders all tables with new data
    └─→ User sees only matching results
```

---

## Database Schema

### PostgreSQL Tables

#### 1. users

**Purpose**: Store user accounts with role-based access.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user',
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Fields**:
- `id`: Auto-incrementing primary key
- `fullname`: User's display name
- `email`: Unique identifier for login
- `password_hash`: bcrypt/werkzeug hashed password
- `role`: 'admin' or 'user' (for future RBAC)
- `status`: 'pending', 'approved', or 'rejected'
- `created_at`: Account creation timestamp

---

#### 2. workarounds

**Purpose**: Team knowledge base of solutions and workarounds.

```sql
CREATE TABLE workarounds (
    id SERIAL PRIMARY KEY,
    category VARCHAR(255),
    issue TEXT NOT NULL,
    description TEXT NOT NULL,
    created_by VARCHAR(255),
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0
);
```

**Fields**:
- `id`: Auto-incrementing primary key
- `category`: Issue category (Billing, CRM, OSS, etc.)
- `issue`: Short issue description
- `description`: Detailed solution (supports rich text)
- `created_by`: User who created the workaround
- `views`: Number of times viewed
- `likes`: Number of likes received
- `created_date`: Creation timestamp

---

#### 3. billing_flag_tracking

**Purpose**: Track billing flag changes and PONR events.

```sql
CREATE TABLE billing_flag_tracking (
    id SERIAL PRIMARY KEY,
    site_id VARCHAR(50) NOT NULL,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_date TIMESTAMP,
    reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

### Oracle Database (Legacy Billing System)

**Access**: Read-only connection via SQLAlchemy  
**Purpose**: Query production billing data  
**Tables**: Various (depends on schema)

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/api/auth/signup` | Create new user account | `{ fullname, email, password }` | `{ fullname, email, role, status }` |
| POST | `/api/auth/login` | Authenticate user | `{ email, password }` | `{ user: { fullname, email, role } }` |

---

### Workarounds (Knowledge Base)

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/api/workarounds/` | List all workarounds | - | `[{ id, category, issue, ... }]` |
| POST | `/api/workarounds/` | Create workaround | `{ category, issue, description, created_by }` | `{ status: 'success', id }` |
| PUT | `/api/workarounds/<id>` | Update workaround | `{ category, issue, description }` | `{ status: 'success' }` |
| DELETE | `/api/workarounds/<id>` | Delete workaround | - | `{ status: 'success' }` |
| POST | `/api/workarounds/<id>/view` | Increment views | - | `{ status: 'success' }` |
| POST | `/api/workarounds/<id>/like` | Increment likes | - | `{ status: 'success' }` |

---

### Search

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/api/search/all` | Get top 10 from each source | - | `{ sr_data: [], defect_data: [], wa_data: [] }` |
| POST | `/api/search/filter` | Execute filtered search | `{ search_anything, customer_id, ... }` | `{ sr_data: [], defect_data: [], wa_data: [] }` |

---

### Billing

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/api/billing/data/<site_id>` | Get billing data for site | - | `{ ... billing details ... }` |

---

## Security Considerations

### Current Issues (Must Fix Before Production)

#### ⚠️ 1. Hardcoded Database Credentials
**Problem**: Credentials in `database.py` are plain text  
**Solution**: Use environment variables with `python-dotenv`

```python
# Current (BAD)
conn = psycopg2.connect(
    database="prodossdb",
    user='ossdb01uams',
    password='Pr0d_ossdb01uams',
    # ...
)

# Fixed (GOOD)
import os
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    # ...
)
```

---

#### ⚠️ 2. No Input Validation
**Problem**: User input not sanitized  
**Solution**: Add input validation library

```bash
pip install marshmallow
```

---

#### ⚠️ 3. CORS Wide Open
**Problem**: `CORS(app)` allows all origins  
**Solution**: Restrict to specific domains

```python
# Current (BAD)
CORS(app)

# Fixed (GOOD)
CORS(app, origins=[
    "http://localhost:5001",
    "https://yourdomain.com"
])
```

---

#### ⚠️ 4. No Authentication Middleware
**Problem**: No token-based auth, relies on sessionStorage  
**Solution**: Implement JWT

```bash
pip install flask-jwt-extended
```

---

#### ⚠️ 5. SQL Injection Risk
**Status**: Currently safe (using parameterized queries)  
**Note**: Always use `%s` placeholders, never string formatting

```python
# SAFE
cur.execute("SELECT * FROM users WHERE email = %s", (email,))

# UNSAFE (DON'T DO THIS!)
cur.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

---

## Development Guidelines

### Adding a New Feature

1. **Create Backend Blueprint** (`backend/routes/newfeature.py`):
   ```python
   from flask import Blueprint, jsonify
   
   newfeature_bp = Blueprint('newfeature', __name__)
   
   @newfeature_bp.route('/data', methods=['GET'])
   def get_data():
       return jsonify({"message": "Feature data"})
   ```

2. **Register Blueprint** in `backend/app.py`:
   ```python
   from routes.newfeature import newfeature_bp
   
   app.register_blueprint(newfeature_bp, url_prefix='/api/newfeature')
   ```

3. **Add API Function** in `static/js/api.js`:
   ```javascript
   API.getNewFeatureData = () => fetchAPI('/api/newfeature/data');
   ```

4. **Create Template** (`templates/newfeature.html`):
   ```html
   <div class="page" id="newfeature-page">
       <h1>New Feature</h1>
       <!-- Content -->
   </div>
   ```

5. **Register Route** in `static/js/main.js`:
   ```javascript
   const NAV_CONFIG = {
       links: [
           // ... existing links
           { id: 'newfeature', text: 'New Feature', file: 'templates/newfeature.html' }
       ]
   };
   ```

6. **Create Feature Module** (optional) (`static/js/newfeature.js`):
   ```javascript
   const NewFeature = {
       init() {
           document.addEventListener('pageLoaded', (e) => {
               if (e.detail.pageId === 'newfeature') {
                   this.setupPage();
               }
           });
       },
       setupPage() {
           // Feature-specific logic
       }
   };
   ```

---

### Testing Workflow

1. **Start Backend**:
   ```bash
   cd backend
   python app.py
   ```

2. **Serve Frontend** (option 1 - direct):
   - Open `index.html` directly in browser

3. **Serve Frontend** (option 2 - local server):
   ```bash
   python -m http.server 8000
   # Navigate to http://localhost:8000
   ```

4. **Test API Endpoints** (Postman/cURL):
   ```bash
   curl -X POST http://127.0.0.1:5001/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"password123"}'
   ```

---

### Git Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes
git add .
git commit -m "feat(module): description"

# Push to GitHub
git push origin feature/new-feature

# Merge to main (after review)
git checkout main
git merge feature/new-feature
git push origin main
```

---

### Code Style

**Python (Backend)**:
- Follow PEP 8
- Use descriptive function names
- Add docstrings to all functions
- Keep functions under 50 lines

**JavaScript (Frontend)**:
- Use ES6+ syntax
- Use `const` and `let` (not `var`)
- Use arrow functions
- Add comments for complex logic

**General**:
- DRY (Don't Repeat Yourself)
- Single Responsibility Principle
- Clear, descriptive naming

---

## Future Enhancements

### Short-term
- [ ] Implement JWT authentication
- [ ] Add input validation with marshmallow
- [ ] Move credentials to environment variables
- [ ] Add unit tests (pytest)
- [ ] Implement error logging

### Medium-term
- [ ] Add user roles and permissions (RBAC)
- [ ] Implement search history
- [ ] Add export to Excel functionality
- [ ] Create admin dashboard
- [ ] Add email notifications

### Long-term
- [ ] Microservices architecture
- [ ] GraphQL API option
- [ ] Real-time updates with WebSockets
- [ ] Mobile app (React Native)
- [ ] AI-powered search suggestions

---

## Troubleshooting

### Backend won't start
```bash
# Check if port 5001 is in use
netstat -ano | findstr :5001

# Try different port
python app.py --port 5002
```

### Frontend can't connect to backend
1. Check `API_BASE_URL` in `static/js/api.js`
2. Verify CORS is enabled
3. Check browser console for errors
4. Verify backend is running (`http://127.0.0.1:5001`)

### Database connection fails
1. Verify credentials in `database.py`
2. Check if PostgreSQL is running
3. Verify network connectivity
4. Check firewall settings

---

## Glossary

- **SPA**: Single-Page Application
- **Blueprint**: Flask's way of organizing routes
- **CORS**: Cross-Origin Resource Sharing
- **CRUD**: Create, Read, Update, Delete
- **JWT**: JSON Web Token
- **RBAC**: Role-Based Access Control
- **API**: Application Programming Interface
- **JSON**: JavaScript Object Notation
- **PONR**: Point of No Return (billing term)

---

**Document Maintained By**: Orion Operations Team  
**For Questions**: Contact the development team or create an issue in the repository

