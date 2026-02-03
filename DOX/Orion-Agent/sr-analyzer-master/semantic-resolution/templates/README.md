# 🎨 Templates Module

> **Jinja2 HTML Templates for Flask Application**

All HTML templates for the SR-Analyzer web interface.

---

## 📁 Structure

```
templates/
├── README.md
├── admin/                      # Admin portal templates
│   ├── admin_upload.html       # Main upload page
│   ├── admin_remove_sr.html    # SR removal page
│   └── today_upload.html       # Today's upload view
├── auth/                       # Authentication templates
│   ├── login_select.html       # Login type selection
│   ├── admin_login.html        # Admin login form
│   ├── user_login.html         # User login form
│   └── login_error.html        # Login error page
├── team/                       # Team management templates
│   └── skill_view.html         # Team skills matrix
├── user/                       # User portal templates
│   ├── feedback_main.html      # Main user interface (2979 lines)
│   └── my_srs.html             # User's assigned SRs
└── json_workaround/            # Known workaround templates
    ├── workaround_search.html  # Search interface
    └── workaround_detail.html  # Detail view
```

---

## 🎨 Key Templates

### User Portal (`user/`)

**`feedback_main.html`** (Main Interface)
- SR search box with autocomplete
- AI workaround display panel
- Similar SRs with similarity scores
- Feedback submission form
- Voting buttons (👍/👎)
- User availability management
- Known workaround integration

**`my_srs.html`**
- List of SRs assigned to user
- Status indicators
- Quick view/edit actions

### Admin Portal (`admin/`)

**`admin_upload.html`**
- Drag-and-drop file upload
- Progress bar with status
- Statistics dashboard
- Recent reports list

**`today_upload.html`**
- Today's processed files
- Quick actions (download, reprocess)

### Authentication (`auth/`)

**`login_select.html`**
- Portal selection (Admin/User)
- Azure AD login option

**`admin_login.html` / `user_login.html`**
- Username/password forms
- Error messages
- Remember me option

---

## 🌙 Theme & Styling

All templates use a consistent dark theme:
- **Background**: #1a1a2e, #16213e
- **Accent Colors**: Blue, Green
- **Typography**: Modern, clean fonts
- **Layout**: Responsive design

---

## 🔗 Related

- [app/README.md](../app/README.md) - Flask application
- [app/routes/README.md](../app/routes/README.md) - Route handlers

---

*Part of SR-Analyzer Templates Module*
