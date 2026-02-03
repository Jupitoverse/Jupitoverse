# 📋 Orionverse Hub - Quick Reference Card

**One-page overview for developers**

---

## 🚀 Start Development (30 seconds)

```bash
# Terminal 1: Backend
cd backend && python app.py

# Terminal 2: Frontend (optional)
python -m http.server 8000

# Or just open index.html in browser
```

**Backend**: `http://127.0.0.1:5001`  
**Frontend**: Open `index.html` or `http://localhost:8000`

---

## 📁 File Structure

```
Orionverse/
├── index.html              ← Main entry (load once)
├── backend/
│   ├── app.py              ← Register blueprints here
│   ├── database.py         ← All DB functions
│   └── routes/             ← Feature modules
│       ├── auth.py         ← /api/auth/*
│       ├── workarounds.py  ← /api/workarounds/*
│       ├── search.py       ← /api/search/*
│       └── billing.py      ← /api/billing/*
├── static/
│   ├── css/style.css       ← All styling
│   └── js/
│       ├── main.js         ← Router (navigation)
│       ├── api.js          ← All API calls
│       ├── auth.js         ← Login/signup UI
│       └── search.js       ← Search logic
└── templates/              ← HTML fragments
```

---

## 🎯 Common Tasks

### Add New Page
1. Create `templates/mypage.html`
2. Add to `NAV_CONFIG` in `main.js`:
   ```javascript
   { id: 'mypage', text: 'My Page', file: 'templates/mypage.html' }
   ```
3. Done! Navigate to `#mypage`

### Add API Endpoint
1. Create route in `backend/routes/myfeature.py`:
   ```python
   @myfeature_bp.route('/data', methods=['GET'])
   def get_data():
       return jsonify({"data": "value"})
   ```
2. Register in `backend/app.py`:
   ```python
   from routes.myfeature import myfeature_bp
   app.register_blueprint(myfeature_bp, url_prefix='/api/myfeature')
   ```
3. Add to `static/js/api.js`:
   ```javascript
   getMyData: () => fetchAPI('/api/myfeature/data')
   ```

### Add Database Function
1. Add to `backend/database.py`:
   ```python
   def get_items():
       conn = get_db_connection()
       # ... query logic
       return results
   ```
2. Use in your route:
   ```python
   import database
   data = database.get_items()
   ```

---

## 🔧 Architecture at a Glance

```
USER BROWSER
    ↓
[index.html] ← Loads once
    ↓
[main.js] ← Handles navigation (#home, #search-anything)
    ↓
[Templates] ← Loads HTML fragments
    ↓
[api.js] ← Makes HTTP requests
    ↓
BACKEND (Flask)
    ↓
[app.py] → Routes to blueprints
    ↓
[routes/*.py] → Business logic
    ↓
[database.py] → DB operations
    ↓
PostgreSQL / Oracle / JSON Files
```

---

## 🌐 API Endpoints Quick List

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/auth/signup` | POST | Create user |
| `/api/auth/login` | POST | Authenticate |
| `/api/workarounds/` | GET | List all |
| `/api/workarounds/` | POST | Create |
| `/api/workarounds/<id>` | PUT | Update |
| `/api/workarounds/<id>` | DELETE | Delete |
| `/api/search/all` | GET | Initial load (top 10) |
| `/api/search/filter` | POST | Filtered search |
| `/api/billing/data/<site_id>` | GET | Billing data |

**Base URL**: `http://127.0.0.1:5001`

---

## 🗄️ Database Quick Reference

### Tables

**users**
- id, fullname, email, password_hash, role, status, created_at

**workarounds**
- id, category, issue, description, created_by, created_date, views, likes

### Key Functions (database.py)
```python
# Users
create_user(fullname, email, password)
find_user_by_email(email)
get_all_users()
update_user_status(user_id, status)

# Workarounds
update_workaround(id, data)
delete_workaround(id)
get_workaround_by_id(id)

# Utility
test_connection()
```

---

## 🎨 Frontend Pattern

### Page Module Template
```javascript
const MyFeature = {
    init() {
        document.addEventListener('pageLoaded', (e) => {
            if (e.detail.pageId === 'myfeature') {
                this.setupPage();
            }
        });
    },
    
    async setupPage() {
        // Load data
        const data = await API.getMyData();
        
        // Render UI
        this.renderData(data);
        
        // Set up event listeners
        document.getElementById('btn').addEventListener('click', this.handleClick);
    },
    
    renderData(data) {
        // Update DOM
    }
};

MyFeature.init();
```

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| CORS error | Check backend running, verify `API_BASE_URL` |
| Page empty | Check console, verify template path in NAV_CONFIG |
| API 404 | Verify blueprint registered in app.py |
| DB error | Check credentials, test with `python database.py` |
| Changes not showing | Hard refresh (Ctrl+Shift+R) or restart Flask |

---

## 🔐 Security Checklist (Before Production)

- [ ] Move DB credentials to `.env` file
- [ ] Implement JWT authentication
- [ ] Add input validation
- [ ] Restrict CORS to specific origins
- [ ] Enable HTTPS
- [ ] Add rate limiting
- [ ] Implement logging
- [ ] Add error monitoring

---

## 📝 Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes and commit
git add .
git commit -m "feat(module): description"

# Push to GitHub
git push origin feature/my-feature

# Merge to main (after review)
git checkout main
git merge feature/my-feature
git push origin main
```

**Commit Types**: feat, fix, docs, style, refactor, test, chore

---

## 🧪 Testing

```bash
# Test backend endpoint
curl http://127.0.0.1:5001/api/workarounds/

# Test database connection
cd backend && python database.py

# Test in browser
F12 → Console → Check for errors
F12 → Network → See API calls
```

---

## 📚 Documentation

- **ARCHITECTURE.md** - Complete technical documentation
- **DEVELOPER_GUIDE.md** - Detailed developer guide with examples
- **README.md** - Project overview and setup
- **CHANGELOG.md** - Version history
- **This file** - Quick reference card

---

## 💡 Key Concepts

**SPA (Single-Page Application)**
- Page loads once, content updates dynamically
- Fast navigation without page reloads

**Flask Blueprints**
- Modular route organization
- Each feature is independent

**API-First Design**
- Backend only returns JSON
- Frontend handles all UI

**Hash-Based Routing**
- URLs like `#home`, `#search-anything`
- Handled by `main.js`

---

## 🎯 Best Practices

✅ **DO**
- Use parameterized queries (`%s`)
- Hash passwords
- Add error handling
- Write descriptive commit messages
- Test before committing
- Comment complex logic

❌ **DON'T**
- Commit credentials
- Use string formatting in SQL
- Store plain passwords
- Skip error handling
- Leave console.log() in production
- Make massive commits

---

## 🔗 Important Links

- **GitHub**: `https://github.com/Jupitoverse/Dox`
- **Backend**: `http://127.0.0.1:5001`
- **Frontend**: `file:///path/to/index.html` or `http://localhost:8000`

---

## 📞 Getting Help

1. Check documentation (ARCHITECTURE.md, DEVELOPER_GUIDE.md)
2. Search existing code for examples
3. Check browser console for errors
4. Test API with cURL or Postman
5. Create GitHub issue or ask team

---

**Print this page and keep it on your desk!** 📄

*Last Updated: October 10, 2025*

