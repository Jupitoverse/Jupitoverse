# 🔐 Auth Templates

> **Authentication HTML Templates**

---

## 📁 Structure

```
auth/
├── README.md
├── login_select.html       # Login type selection
├── admin_login.html        # Admin login form
├── user_login.html         # User login form
└── login_error.html        # Login error page
```

---

## 📄 Templates

### `login_select.html`

Portal selection page:
- **Admin Portal** button → `/admin/login`
- **User Portal** button → `/user/login`
- Azure AD SSO option (if configured)

### `admin_login.html`

Admin login form:
- Username field
- Password field
- Remember me checkbox
- Error message display
- Default credentials hint: `admin` / `admin123`

### `user_login.html`

User login form:
- Email field
- Azure AD integration button
- Local login option
- Error message display

### `login_error.html`

Login error page:
- Error message display
- Back to login button
- Help text

---

## 🔐 Authentication Flow

```
User visits /
    │
    ▼
login_select.html
    │
    ├── Admin → admin_login.html → /admin
    │
    └── User → user_login.html → /user
                    │
                    └── Azure AD SSO → /user
```

---

## 🔗 Related

- [templates/README.md](../README.md) - Templates module
- [app/routes/auth.py](../../app/routes/auth.py) - Auth routes

---

*Part of SR-Analyzer Templates Module*
