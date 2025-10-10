# 🚀 Orionverse Hub - Developer Quick Reference

**Quick start guide for developers working on Orionverse Hub**

---

## 🏃 Quick Start (5 minutes)

### 1. Clone & Setup
```bash
cd C:\Users\YOUR_USERNAME\Desktop\Projects\Orion\Orionverse

# Install dependencies
pip install -r requirements.txt
```

### 2. Start Backend
```bash
cd backend
python app.py
```
✅ Backend running at `http://127.0.0.1:5001`

### 3. Open Frontend
- **Option A**: Open `index.html` directly in browser
- **Option B**: Run local server:
  ```bash
  python -m http.server 8000
  # Navigate to http://localhost:8000
  ```

---

## 📁 Project Structure (Quick Overview)

```
Orionverse/
├── index.html                    ← Entry point (load once)
│
├── backend/
│   ├── app.py                    ← Backend entry, register blueprints here
│   ├── database.py               ← All database functions
│   │
│   ├── routes/                   ← Feature modules
│   │   ├── auth.py               ← /api/auth/*
│   │   ├── workarounds.py        ← /api/workarounds/*
│   │   ├── search.py             ← /api/search/*
│   │   └── billing.py            ← /api/billing/*
│   │
│   └── data/
│       ├── sr_data.json          ← Pre-processed data
│       └── defect_data.json      ← Pre-processed data
│
├── static/
│   ├── css/style.css             ← All styling
│   │
│   └── js/
│       ├── main.js               ← Router (handles navigation)
│       ├── api.js                ← All API calls
│       ├── auth.js               ← Login/signup UI
│       └── search.js             ← Search page logic
│
└── templates/                    ← HTML fragments (not full pages)
    ├── home.html
    ├── search_anything.html
    └── ... (other pages)
```

---

## 🎯 Common Tasks

### ✅ Add a New Page

**1. Create HTML template**
```bash
# Create file: templates/mypage.html
```
```html
<div class="page" id="mypage-page">
    <h1>My New Page</h1>
    <p>Content goes here...</p>
</div>
```

**2. Register in navigation** (`static/js/main.js`)
```javascript
const NAV_CONFIG = {
    links: [
        // ... existing links ...
        { id: 'mypage', text: 'My Page', file: 'templates/mypage.html' }
    ]
};
```

**3. (Optional) Add page-specific logic** (`static/js/mypage.js`)
```javascript
const MyPage = {
    init() {
        document.addEventListener('pageLoaded', (e) => {
            if (e.detail.pageId === 'mypage') {
                this.setupPage();
            }
        });
    },
    
    setupPage() {
        console.log('My Page loaded!');
        // Your logic here
    }
};

// Don't forget to call init() and add script tag to index.html
MyPage.init();
```

**4. Add script tag to index.html** (if you created a JS file)
```html
<script src="static/js/mypage.js"></script>
```

✅ **Done!** Navigate to `#mypage` to see your page.

---

### ✅ Add a New API Endpoint

**1. Create route in backend** (`backend/routes/myfeature.py`)
```python
from flask import Blueprint, jsonify, request

myfeature_bp = Blueprint('myfeature', __name__)

@myfeature_bp.route('/data', methods=['GET'])
def get_data():
    # Your logic here
    return jsonify({"message": "Hello from API!"})

@myfeature_bp.route('/create', methods=['POST'])
def create_item():
    data = request.get_json()
    # Process data
    return jsonify({"status": "success", "id": 123}), 201
```

**2. Register blueprint** (`backend/app.py`)
```python
from routes.myfeature import myfeature_bp

def create_app():
    # ... existing code ...
    app.register_blueprint(myfeature_bp, url_prefix='/api/myfeature')
    return app
```

**3. Add API function** (`static/js/api.js`)
```javascript
const API = {
    // ... existing functions ...
    
    getMyFeatureData: () => fetchAPI('/api/myfeature/data'),
    
    createMyFeatureItem: (itemData) => {
        return fetchAPI('/api/myfeature/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(itemData)
        });
    }
};
```

**4. Call from frontend**
```javascript
// Somewhere in your page logic
async function loadData() {
    try {
        const data = await API.getMyFeatureData();
        console.log(data);
    } catch (error) {
        console.error('Failed to load data:', error);
    }
}
```

✅ **Done!** Your API is ready to use.

---

### ✅ Add a Database Table

**1. Create table in PostgreSQL**
```sql
CREATE TABLE my_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**2. Add helper functions** (`backend/database.py`)
```python
def get_all_items():
    """Fetch all items from my_table"""
    conn = get_db_connection()
    if not conn: return []
    
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute('SELECT * FROM my_table ORDER BY created_at DESC;')
    items = cur.fetchall()
    cur.close()
    conn.close()
    return items

def create_item(name, description):
    """Insert new item into my_table"""
    conn = get_db_connection()
    if not conn: return None
    
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO my_table (name, description) VALUES (%s, %s) RETURNING id;',
        (name, description)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return new_id
```

**3. Use in your route**
```python
import database

@myfeature_bp.route('/items', methods=['GET'])
def get_items():
    items = database.get_all_items()
    return jsonify(items)
```

✅ **Done!** Database operations ready.

---

### ✅ Add Styling

**Global styles** → `static/css/style.css`
```css
.my-custom-class {
    background-color: var(--primary-color);
    padding: 20px;
    border-radius: 8px;
}
```

**Page-specific styles** → Add to `style.css` with page ID selector
```css
#mypage-page {
    /* Styles only for My Page */
}

#mypage-page .special-button {
    background-color: red;
}
```

---

## 🔧 Development Tools

### Backend Debugging
```python
# Add to any route for debugging
print(f"DEBUG: Data received: {data}")

# Pretty print JSON
import json
print(json.dumps(data, indent=2))
```

### Frontend Debugging
```javascript
// Console logging
console.log('Value:', value);
console.table(arrayData);    // Pretty table for arrays
console.dir(object);         // Detailed object inspection

// Breakpoints in browser DevTools
debugger;  // Pause execution here
```

### Database Debugging
```python
# In database.py, add this to see SQL queries
cur.execute(query)
print(f"SQL: {cur.query.decode('utf-8')}")
```

---

## 📋 Checklist for New Features

**Before you start:**
- [ ] Read ARCHITECTURE.md for understanding
- [ ] Check if similar feature exists
- [ ] Create feature branch: `git checkout -b feature/myfeature`

**Backend checklist:**
- [ ] Create blueprint in `backend/routes/`
- [ ] Register blueprint in `app.py`
- [ ] Add database functions if needed
- [ ] Test API with Postman/cURL
- [ ] Add error handling

**Frontend checklist:**
- [ ] Create HTML template in `templates/`
- [ ] Add to NAV_CONFIG in `main.js`
- [ ] Add API functions in `api.js`
- [ ] Create feature JS file if complex
- [ ] Add styling in `style.css`
- [ ] Test in browser

**Before committing:**
- [ ] Test thoroughly
- [ ] Remove console.log() statements
- [ ] Check for linter errors
- [ ] Write meaningful commit message
- [ ] Update CHANGELOG.md

---

## 🐛 Common Issues & Solutions

### Issue: "CORS error in console"
**Solution**: 
1. Check backend is running (`http://127.0.0.1:5001`)
2. Verify `CORS(app)` is in `backend/app.py`
3. Check `API_BASE_URL` in `static/js/api.js`

---

### Issue: "Page shows empty content"
**Solution**:
1. Check browser console for errors
2. Verify template file path in NAV_CONFIG
3. Check template file exists
4. Verify HTML structure (should NOT have `<html>` tags)

---

### Issue: "Database connection failed"
**Solution**:
1. Verify credentials in `backend/database.py`
2. Check if PostgreSQL is running
3. Test connection:
   ```python
   import psycopg2
   conn = psycopg2.connect(database="prodossdb", user="...", password="...", host="...", port="6432")
   print("✅ Connected!")
   ```

---

### Issue: "API endpoint not found (404)"
**Solution**:
1. Check blueprint is registered in `app.py`
2. Verify route decorator: `@blueprint_name.route('/path')`
3. Check API_BASE_URL + endpoint path matches
4. Restart Flask server after changes

---

### Issue: "Changes not reflecting"
**Solution**:
1. **Backend**: Restart Flask server
2. **Frontend**: Hard refresh browser (Ctrl+Shift+R)
3. Check browser cache (Ctrl+Shift+Delete)
4. Check if editing correct file

---

## 📚 Key Concepts

### 1. Single-Page Application (SPA)
- Page loads **once**
- Navigation changes URL hash (`#page`)
- Content updates **without** page reload
- Fast, smooth user experience

### 2. Flask Blueprints
- Modular way to organize routes
- Each feature is independent
- Register with URL prefix: `/api/feature`

### 3. API-First Design
- Backend only returns JSON (no HTML)
- Frontend makes HTTP requests
- Complete separation of concerns

### 4. Hash-Based Routing
- URL: `http://localhost:8000#home`
- Hash changes trigger navigation
- Handled by `main.js`

---

## 🎨 UI Components

### Modal
```javascript
// Show modal
document.getElementById('modal-container').innerHTML = `
    <div class="modal-overlay visible">
        <div class="modal-content">
            <h2>Modal Title</h2>
            <p>Content here</p>
        </div>
    </div>
`;
```

### Loading Spinner
```html
<div class="loading-spinner">Loading...</div>
```

### Error Message
```html
<div class="error-message">Error: Something went wrong</div>
```

### Success Message
```html
<div class="success-message">✅ Success!</div>
```

---

## 🧪 Testing Endpoints

### Using cURL
```bash
# GET request
curl http://127.0.0.1:5001/api/workarounds/

# POST request with JSON
curl -X POST http://127.0.0.1:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# PUT request
curl -X PUT http://127.0.0.1:5001/api/workarounds/1 \
  -H "Content-Type: application/json" \
  -d '{"category":"Updated","issue":"New issue","description":"New desc"}'

# DELETE request
curl -X DELETE http://127.0.0.1:5001/api/workarounds/1
```

### Using Python
```python
import requests

# GET
response = requests.get('http://127.0.0.1:5001/api/workarounds/')
print(response.json())

# POST
response = requests.post(
    'http://127.0.0.1:5001/api/auth/login',
    json={'email': 'test@example.com', 'password': 'password123'}
)
print(response.json())
```

---

## 📝 Commit Message Format

```
type(scope): subject

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance

Examples:
feat(search): add advanced filter options
fix(auth): resolve login timeout issue
docs(readme): update installation steps
```

---

## 🔐 Security Best Practices

1. **Never commit**:
   - Passwords
   - API keys
   - Database credentials
   - `.env` files

2. **Always use**:
   - Parameterized queries (`%s` placeholders)
   - Password hashing (werkzeug)
   - Input validation
   - Error handling

3. **Before production**:
   - Move credentials to `.env`
   - Implement JWT authentication
   - Restrict CORS origins
   - Add rate limiting

---

## 📞 Getting Help

1. **Check documentation**:
   - ARCHITECTURE.md (detailed technical docs)
   - README.md (project overview)
   - This file (quick reference)

2. **Search existing code**:
   - Look for similar features
   - Check how others implemented it

3. **Ask the team**:
   - Create GitHub issue
   - Ask in team chat
   - Contact maintainer

---

## 🎓 Learning Resources

### Flask
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Blueprints](https://flask.palletsprojects.com/en/2.3.x/blueprints/)

### JavaScript
- [MDN Web Docs](https://developer.mozilla.org/en-US/)
- [JavaScript.info](https://javascript.info/)

### PostgreSQL
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)

---

## 💡 Pro Tips

1. **Use browser DevTools**: F12 → Network tab to see API calls
2. **Console is your friend**: Log everything when debugging
3. **Git commit often**: Small, frequent commits are better
4. **Test as you build**: Don't wait until the end
5. **Read existing code**: Learn from what's already there
6. **Comment complex logic**: Your future self will thank you
7. **Use meaningful names**: `getUserData()` not `func1()`
8. **Keep functions small**: Max 50 lines
9. **DRY principle**: Don't Repeat Yourself
10. **Ask for help early**: Don't struggle for hours

---

## 🚀 Next Steps

1. Read ARCHITECTURE.md for deep understanding
2. Explore existing code
3. Try adding a simple page
4. Create a test API endpoint
5. Build your first feature!

---

**Happy Coding! 🎉**

*For detailed architecture information, see [ARCHITECTURE.md](ARCHITECTURE.md)*

