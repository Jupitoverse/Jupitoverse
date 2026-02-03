# Orionverse Project - Complete Context & Instructions

**Last Updated**: November 2, 2025  
**Project Location**: `C:\Users\abhisha3\Desktop\Projects\Orion\Orionverse`

---

## Project Overview

**Orionverse Hub** is a comprehensive internal portal for Amdocs Orion team that provides:
- Centralized search across SR Details, Defect Names, and Workarounds
- Workaround management with collaborative features
- Billing information and tracking
- Training resources and documentation
- Release management tools
- Important links and resources

---

## Previous Work Summary

### Phase 1: Initial Setup & Search Engine
**What was done**:
- Created Flask backend with PostgreSQL database
- Implemented search functionality across multiple data sources
- Built responsive frontend with dark theme
- Added SR data, defect data, and workaround search

**Key Features**:
- Real-time search across SR Details, UPDATE_DETAILS
- Defect name and description search
- Workaround search across all fields
- Advanced filters (Customer ID, Site pattern, etc.)

### Phase 2: UI Improvements
**User Request**: "Removed texted below field in Advance Search filter and keep 'Search Anything' field in center and little highlighted"

**What was done**:
- Removed help text (`<small class="filter-help">`) from all search input fields
- Centered the "Search Anything" input field
- Added prominent styling with purple gradient background
- Added glow effect and animations for primary search
- Made it visually distinct from other search boxes

**Files Modified**:
- `templates/search_anything.html` - Removed help text, wrapped primary search
- `static/css/style.css` - Added `.sa-primary-search` and `.sa-filter-group.primary` styles

### Phase 3: Enhanced Workaround System
**User Request**: "Here anyone should be able to save it, fetch it based on search engine and other options like adding comment, like sharing mode, etc"

**What was done**:
- Created comprehensive workaround management system
- Added collaborative features: comments, likes, shares, tags
- Implemented activity logging and analytics
- Added user preferences and bookmarks

**Database Schema Created** (`schema_workarounds_enhanced.sql`):
1. **workarounds** - Main workaround storage
2. **workaround_comments** - Threaded comments with parent/child support
3. **workaround_likes** - Per-user like tracking
4. **workaround_shares** - Bookmark/share functionality
5. **workaround_activity_log** - Activity tracking
6. **workaround_tags** - Tag management
7. **workaround_user_preferences** - User settings

**API Endpoints Created** (`routes/workarounds_enhanced.py`):
- `GET /api/workarounds` - List with filtering, pagination, sorting
- `GET /api/workarounds/<id>` - Get single workaround
- `POST /api/workarounds` - Create new workaround
- `PUT /api/workarounds/<id>` - Update workaround
- `DELETE /api/workarounds/<id>` - Delete workaround
- `POST /api/workarounds/<id>/comments` - Add comment
- `GET /api/workarounds/<id>/comments` - Get comments (threaded)
- `POST /api/workarounds/<id>/like` - Like/unlike
- `GET /api/workarounds/<id>/likes` - Get like count
- `POST /api/workarounds/<id>/share` - Share/bookmark
- `GET /api/workarounds/<id>/analytics` - Get analytics
- `GET /api/workarounds/tags` - Get all tags
- Plus more endpoints for activity logs, user preferences, etc.

**Features**:
- ✅ Threaded comments with reply support
- ✅ Per-user like tracking (no duplicate likes)
- ✅ Share/bookmark functionality
- ✅ Tag management with auto-complete
- ✅ Activity logging for all actions
- ✅ Analytics (views, likes, shares, comments)
- ✅ User preferences
- ✅ Full CRUD operations
- ✅ Advanced filtering and sorting
- ✅ Pagination support

### Phase 4: Image Support Confirmation
**User Question**: "Please confirm if i would be able to add images in description of Add Workaround details"

**Answer**: YES! ✅ Image support is available through Quill.js rich text editor

**Image Support Methods**:
1. **Upload from Computer** - Click image icon in toolbar
2. **Drag & Drop** - Drag images directly into editor
3. **Copy & Paste** - Paste images from clipboard
4. **URL Embedding** - Insert images via URL

**Implementation**:
- Quill.js already integrated in the frontend
- Supports multiple image formats (JPEG, PNG, GIF, WebP)
- Images stored as base64 in description field
- No additional backend changes needed

### Phase 5: Network Deployment Setup
**User Request**: "now i have run this on other network where db connection is possible. guide me for that"

**What was done**:
- Created comprehensive network deployment guide
- Modified Flask app to listen on all network interfaces (`host='0.0.0.0'`)
- Updated frontend API to dynamically detect local vs network access
- Created automation scripts for AVD deployment
- Added firewall configuration
- Created testing scripts

**Files Created/Modified**:
1. **backend/app.py** - Changed to `host='0.0.0.0'` for network access
2. **static/js/api.js** - Dynamic API URL detection
3. **START_NETWORK_BACKEND.bat** - Quick network startup script
4. **test_network_access.ps1** - Network diagnostics
5. **setup_avd.ps1** - Automated AVD setup
6. **NETWORK_DEPLOYMENT_GUIDE.md** - Complete deployment guide
7. **AVD_DEPLOYMENT_GUIDE.md** - AVD-specific instructions
8. **DEPLOYMENT_CHECKLIST.md** - Step-by-step checklist

**Network Configuration**:
```python
# Backend (app.py)
app.run(
    host='0.0.0.0',        # Listen on all interfaces
    port=5001,
    debug=True,
    threaded=True
)
```

```javascript
// Frontend (api.js)
const API_BASE_URL = window.location.hostname === '' || 
                     window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:5001'
    : `http://${window.location.hostname}:5001`;
```

**Deployment Steps**:
1. Copy project to AVD machine
2. Install Python dependencies (`pip install -r requirements.txt`)
3. Configure PostgreSQL connection
4. Configure firewall (allow port 5001)
5. Run `START_NETWORK_BACKEND.bat`
6. Access from other machines: `http://YOUR_MACHINE_IP:5001`

---

## Current Project Structure

```
Orionverse/
├── backend/
│   ├── app.py                          # Main Flask application
│   ├── database.py                     # Database connection & queries
│   ├── routes/
│   │   ├── auth.py                     # Authentication routes
│   │   ├── search.py                   # Search functionality
│   │   ├── billing.py                  # Billing routes
│   │   ├── workarounds.py              # Basic workaround routes (OLD)
│   │   └── workarounds_enhanced.py     # Enhanced workaround system (NEW)
│   ├── data/
│   │   ├── sr_data.json                # SR database
│   │   └── defect_data.json            # Defect database
│   └── schema_workarounds_enhanced.sql # Database schema
│
├── static/
│   ├── css/
│   │   └── style.css                   # Main stylesheet
│   └── js/
│       ├── api.js                      # API communication (network-aware)
│       ├── auth.js                     # Authentication logic
│       ├── main.js                     # Main application logic
│       └── search.js                   # Search functionality
│
├── templates/
│   ├── home.html                       # Landing page
│   ├── search_anything.html            # Search page (PRIMARY FEATURE)
│   ├── billing.html                    # Billing information
│   ├── database.html                   # Database management
│   ├── assignments.html                # Assignment tracking
│   ├── release.html                    # Release management
│   ├── training.html                   # Training resources
│   ├── events.html                     # Events calendar
│   ├── imp-links.html                  # Important links
│   └── welcome-kit.html                # Welcome kit
│
├── Documentation/
│   ├── README.md                       # Main documentation
│   ├── ARCHITECTURE.md                 # System architecture
│   ├── DEVELOPER_GUIDE.md              # Developer guide
│   ├── QUICK_START.md                  # Quick start guide
│   ├── SEARCH_ENGINE_GUIDE.md          # Search functionality
│   ├── WORKAROUND_SETUP_GUIDE.md       # Workaround system setup
│   ├── WORKAROUND_FEATURES_SUMMARY.md  # Workaround features
│   ├── IMAGE_SUPPORT_GUIDE.md          # Image support in workarounds
│   ├── SEARCH_UI_UPDATES.md            # UI update history
│   ├── NETWORK_DEPLOYMENT_GUIDE.md     # Network deployment
│   ├── AVD_DEPLOYMENT_GUIDE.md         # AVD deployment
│   ├── DEPLOYMENT_CHECKLIST.md         # Deployment checklist
│   ├── QUICK_NETWORK_SETUP.md          # Quick network setup
│   ├── CHANGELOG.md                    # Change history
│   └── PROJECT_CONTEXT.md              # This file
│
├── Scripts/
│   ├── START_BACKEND.bat               # Local backend startup
│   ├── START_NETWORK_BACKEND.bat       # Network backend startup
│   ├── setup_avd.ps1                   # AVD setup automation
│   ├── test_network_access.ps1         # Network testing
│   └── convert_excel.py                # Excel data conversion
│
└── requirements.txt                     # Python dependencies
```

---

## Technology Stack

### Backend
- **Python 3.x** - Programming language
- **Flask** - Web framework
- **Flask-CORS** - Cross-origin resource sharing
- **psycopg2-binary** - PostgreSQL adapter
- **pandas** - Data manipulation
- **SQLAlchemy** - ORM (optional)

### Frontend
- **HTML5/CSS3** - Structure and styling
- **Vanilla JavaScript** - No frameworks
- **Quill.js** - Rich text editor with image support
- **jQuery DataTables** - Table display (optional)

### Database
- **PostgreSQL** - Primary database
- **JSON files** - SR and Defect data storage

### Deployment
- **Gunicorn** - WSGI server (production)
- **Nginx** - Reverse proxy (production)
- **Windows** - Development environment

---

## Key Features

### 1. Search Anything (PRIMARY FEATURE)
**Location**: `templates/search_anything.html`

**Capabilities**:
- Search across SR Details, UPDATE_DETAILS
- Search Defect Names and Descriptions
- Search Workarounds (all fields)
- Advanced filters:
  - Customer ID search
  - Site pattern (e.g., OSite_%_1)
  - Category filters
  - Date range filters

**UI Highlights**:
- Primary search field centered and highlighted
- Purple gradient background with glow effect
- No cluttering help text
- Real-time search results
- Responsive design

### 2. Enhanced Workaround Management
**Location**: `routes/workarounds_enhanced.py`

**Features**:
- **CRUD Operations**: Create, Read, Update, Delete workarounds
- **Collaborative**: Comments (threaded), Likes, Shares
- **Organization**: Tags, Categories, Search
- **Analytics**: Views, Engagement metrics
- **User Management**: Preferences, Activity logs
- **Rich Content**: Image support via Quill.js

**Database Tables**: 7 tables for complete functionality

### 3. Billing Management
**Location**: `templates/billing.html`

**Features**:
- Billing information display
- Cost tracking
- Invoice management

### 4. Training Resources
**Location**: `templates/training.html`

**Features**:
- Training materials
- Documentation links
- Video tutorials

### 5. Release Management
**Location**: `templates/release.html`

**Features**:
- Release planning
- Version tracking
- Deployment schedules

### 6. Bulk Handling Operations (NEW)
**Location**: `templates/bulk_handling.html`

**Features**:
- **Bulk Retry**: Retry failed orders or activities in bulk
- **Bulk Force Complete**: Force complete stuck or pending orders
- **Bulk Re-execute**: Re-execute orders or workflows from a specific step
- **Bulk Resolve Error**: Resolve errors in bulk for failed orders
- **Complete Stuck Activity**: Complete activities stuck in processing state

**Capabilities**:
- Input validation for IDs (Order IDs, SR IDs, Customer IDs, OSite IDs, Activity IDs)
- Multiple input formats (comma-separated or line-separated)
- Real-time execution status and results
- Detailed success/failure reporting
- Age-based and status-based activity search
- Priority-based execution
- Custom step re-execution
- Error type filtering and resolution actions

**Backend API**: `/api/bulk-handling/*`

---

## Database Schema

### Workaround System Tables

#### 1. workarounds
```sql
- id (SERIAL PRIMARY KEY)
- title (VARCHAR(500) NOT NULL)
- description (TEXT)
- category (VARCHAR(100))
- tags (TEXT[])
- created_by (VARCHAR(100))
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- status (VARCHAR(50))
- visibility (VARCHAR(50))
- view_count (INTEGER)
```

#### 2. workaround_comments
```sql
- id (SERIAL PRIMARY KEY)
- workaround_id (INTEGER REFERENCES workarounds)
- parent_comment_id (INTEGER) -- For threading
- user_id (VARCHAR(100))
- comment_text (TEXT)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- is_deleted (BOOLEAN)
```

#### 3. workaround_likes
```sql
- id (SERIAL PRIMARY KEY)
- workaround_id (INTEGER REFERENCES workarounds)
- user_id (VARCHAR(100))
- created_at (TIMESTAMP)
- UNIQUE(workaround_id, user_id) -- Prevent duplicate likes
```

#### 4. workaround_shares
```sql
- id (SERIAL PRIMARY KEY)
- workaround_id (INTEGER REFERENCES workarounds)
- user_id (VARCHAR(100))
- share_type (VARCHAR(50)) -- 'bookmark', 'share', 'export'
- created_at (TIMESTAMP)
```

#### 5. workaround_activity_log
```sql
- id (SERIAL PRIMARY KEY)
- workaround_id (INTEGER REFERENCES workarounds)
- user_id (VARCHAR(100))
- action_type (VARCHAR(50))
- action_details (JSONB)
- created_at (TIMESTAMP)
```

#### 6. workaround_tags
```sql
- id (SERIAL PRIMARY KEY)
- tag_name (VARCHAR(100) UNIQUE)
- usage_count (INTEGER)
- created_at (TIMESTAMP)
```

#### 7. workaround_user_preferences
```sql
- id (SERIAL PRIMARY KEY)
- user_id (VARCHAR(100) UNIQUE)
- preferences (JSONB)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
```

---

## API Endpoints Reference

### Search API
```
GET  /api/search/filter?q=<query>&customer_id=<id>&site_pattern=<pattern>
```

### Workaround API (Enhanced)
```
GET    /api/workarounds                    # List all (with filters)
GET    /api/workarounds/<id>               # Get single
POST   /api/workarounds                    # Create new
PUT    /api/workarounds/<id>               # Update
DELETE /api/workarounds/<id>               # Delete

POST   /api/workarounds/<id>/comments      # Add comment
GET    /api/workarounds/<id>/comments      # Get comments (threaded)
PUT    /api/workarounds/comments/<id>      # Update comment
DELETE /api/workarounds/comments/<id>      # Delete comment

POST   /api/workarounds/<id>/like          # Like/unlike
GET    /api/workarounds/<id>/likes         # Get like count
GET    /api/workarounds/<id>/user-liked    # Check if user liked

POST   /api/workarounds/<id>/share         # Share/bookmark
GET    /api/workarounds/<id>/shares        # Get share count

GET    /api/workarounds/<id>/analytics     # Get analytics
GET    /api/workarounds/<id>/activity      # Get activity log

GET    /api/workarounds/tags               # Get all tags
POST   /api/workarounds/tags               # Create tag
DELETE /api/workarounds/tags/<id>          # Delete tag

GET    /api/workarounds/user/preferences   # Get user preferences
PUT    /api/workarounds/user/preferences   # Update preferences
```

### Query Parameters
```
?search=<text>          # Search in title/description
?category=<cat>         # Filter by category
?tags=<tag1,tag2>       # Filter by tags
?created_by=<user>      # Filter by creator
?status=<status>        # Filter by status
?sort_by=<field>        # Sort field
?sort_order=<asc|desc>  # Sort order
?page=<num>             # Page number
?per_page=<num>         # Items per page
```

---

## Configuration

### Backend Configuration (app.py)
```python
# Local Development
app.run(host='127.0.0.1', port=5001, debug=True)

# Network Deployment
app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
```

### Frontend Configuration (api.js)
```javascript
// Dynamic API URL (works for both local and network)
const API_BASE_URL = window.location.hostname === '' || 
                     window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1'
    ? 'http://127.0.0.1:5001'
    : `http://${window.location.hostname}:5001`;
```

### Database Configuration (database.py)
```python
# PostgreSQL Connection
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'orionverse',
    'user': 'your_username',
    'password': 'your_password'
}
```

---

## Deployment Instructions

### Local Development
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start backend
START_BACKEND.bat
# Or: python backend/app.py

# 3. Open browser
http://localhost:5001
```

### Network Deployment (AVD)
```bash
# 1. Copy project to AVD machine
# 2. Run automated setup
.\setup_avd.ps1

# 3. Start network backend
START_NETWORK_BACKEND.bat

# 4. Configure firewall
New-NetFirewallRule -DisplayName "Orionverse Backend" -Direction Inbound -LocalPort 5001 -Protocol TCP -Action Allow

# 5. Access from other machines
http://<YOUR_MACHINE_IP>:5001
```

### Production Deployment
```bash
# 1. Install Gunicorn
pip install gunicorn

# 2. Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 backend.app:app

# 3. Configure Nginx (reverse proxy)
# See NETWORK_DEPLOYMENT_GUIDE.md
```

---

## User Instructions & Preferences

### Design Preferences
1. **Search UI**: Primary search field should be centered and highlighted
2. **No Clutter**: Remove help text from input fields
3. **Visual Hierarchy**: Make important elements stand out
4. **Dark Theme**: Maintain dark purple/blue theme throughout
5. **Responsive**: Must work on all devices

### Feature Priorities
1. **Search Functionality** - Most important feature
2. **Workaround Management** - Collaborative features essential
3. **User Experience** - Clean, intuitive interface
4. **Performance** - Fast search and data retrieval
5. **Network Access** - Must work across network

### Development Guidelines
1. **Keep it Simple**: Don't over-engineer
2. **Document Everything**: Update this file with changes
3. **Test Thoroughly**: Test both local and network access
4. **Maintain Consistency**: Follow existing patterns
5. **User-Centric**: Always consider user workflow

---

## Common Tasks

### Adding a New Feature
1. Update backend routes if needed
2. Modify database schema if needed
3. Update frontend templates/JS
4. Update API.js if new endpoints
5. Test locally and on network
6. Update documentation
7. Update this PROJECT_CONTEXT.md

### Modifying Search
1. Edit `backend/routes/search.py` for backend logic
2. Edit `templates/search_anything.html` for UI
3. Edit `static/js/search.js` for frontend logic
4. Edit `static/css/style.css` for styling
5. Test with various search queries

### Updating Workaround System
1. Modify `backend/routes/workarounds_enhanced.py`
2. Update database schema if needed
3. Update frontend to use new endpoints
4. Test all CRUD operations
5. Update WORKAROUND_SETUP_GUIDE.md

### Deploying to New Environment
1. Follow DEPLOYMENT_CHECKLIST.md
2. Run setup_avd.ps1 for automation
3. Configure database connection
4. Test network access
5. Configure firewall
6. Verify all features work

---

## Troubleshooting

### Search Not Working
**Check**:
1. Backend is running (`START_BACKEND.bat`)
2. Database connection is configured
3. sr_data.json and defect_data.json exist
4. API endpoint is accessible
5. Browser console for errors

**Solution**: Run `backend/test_backend_live.py` to diagnose

### Network Access Issues
**Check**:
1. Flask app is running with `host='0.0.0.0'`
2. Firewall allows port 5001
3. Correct IP address is being used
4. api.js is using correct API_BASE_URL

**Solution**: Run `test_network_access.ps1` for diagnostics

### Workaround Features Not Working
**Check**:
1. Database schema is created (run schema_workarounds_enhanced.sql)
2. PostgreSQL is running
3. workarounds_enhanced.py is being used (not workarounds.py)
4. User authentication is working

**Solution**: Check WORKAROUND_SETUP_GUIDE.md

### Image Upload Not Working
**Check**:
1. Quill.js is loaded in template
2. Image toolbar button is visible
3. Browser console for errors
4. Description field accepts base64 data

**Solution**: See IMAGE_SUPPORT_GUIDE.md

---

## Future Enhancements (Ideas)

### Short-term
- [ ] Add user authentication with Active Directory
- [ ] Implement role-based access control
- [ ] Add email notifications for workaround updates
- [ ] Create mobile-responsive views
- [ ] Add export functionality (PDF, Excel)

### Medium-term
- [ ] Integrate with Jira for ticket tracking
- [ ] Add real-time collaboration (WebSockets)
- [ ] Implement full-text search with Elasticsearch
- [ ] Add dashboard with analytics
- [ ] Create REST API documentation (Swagger)

### Long-term
- [ ] Machine learning for search relevance
- [ ] Automated workaround suggestions
- [ ] Integration with other Amdocs tools
- [ ] Mobile app (React Native)
- [ ] Advanced reporting and analytics

---

## Important Notes

### Critical Files
- **app.py** - Main application entry point
- **database.py** - Database connection logic
- **search_anything.html** - Primary user interface
- **style.css** - All styling (don't break the theme!)
- **api.js** - Network-aware API communication

### Don't Modify
- **workarounds.py** - Keep for reference, use workarounds_enhanced.py
- **Backend port** - Always use 5001
- **Database schema** - Don't change without updating all references

### Always Update
- **PROJECT_CONTEXT.md** - This file (after any changes)
- **CHANGELOG.md** - Document all changes
- **README.md** - Keep user documentation current

---

## Quick Commands Reference

```bash
# Start local backend
START_BACKEND.bat

# Start network backend
START_NETWORK_BACKEND.bat

# Test network access
.\test_network_access.ps1

# Setup AVD environment
.\setup_avd.ps1

# Install dependencies
pip install -r requirements.txt

# Run database schema
psql -U username -d orionverse -f backend/schema_workarounds_enhanced.sql

# Test API
curl http://localhost:5001/api/search/filter?q=test
```

---

## Contact & Support

**Project Owner**: Amdocs Orion Team  
**Development**: Internal Team  
**Location**: C:\Users\abhisha3\Desktop\Projects\Orion\Orionverse

For questions or issues:
1. Check documentation in project folder
2. Review this PROJECT_CONTEXT.md
3. Check TROUBLESHOOTING section
4. Review recent CHANGELOG.md entries

---

## Version History

**v1.0** - Initial release with search functionality  
**v1.1** - UI improvements (centered search, removed help text)  
**v2.0** - Enhanced workaround system with collaboration  
**v2.1** - Image support confirmation and documentation  
**v3.0** - Network deployment support and AVD setup  
**v3.1** - Complete documentation and context file  
**v3.2** - Bulk Handling operations added (current)

---

## Resume Working Checklist

When resuming work on this project:

1. ✅ Read this PROJECT_CONTEXT.md file completely
2. ✅ Check CHANGELOG.md for recent changes
3. ✅ Review any open issues or TODOs
4. ✅ Verify backend is running (START_BACKEND.bat)
5. ✅ Test search functionality
6. ✅ Check database connection
7. ✅ Review user's latest requirements
8. ✅ Update this file with any new changes

---

**END OF PROJECT CONTEXT**

*This file should be updated whenever significant changes are made to the project.*

