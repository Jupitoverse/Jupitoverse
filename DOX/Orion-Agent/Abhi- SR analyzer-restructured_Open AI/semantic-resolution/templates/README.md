# 🎨 Templates Module

> **Jinja2 HTML Templates for Web Interface**

This folder contains all HTML templates for the Flask web application, organized by functional area.

---

## 📁 Structure

```
templates/
├── README.md
├── admin/                    # Admin portal templates
│   ├── dashboard.html        # Admin home page
│   ├── upload.html           # File upload page
│   └── reports.html          # Reports viewing page
│
├── auth/                     # Authentication templates
│   ├── login.html            # Login page
│   ├── logout.html           # Logout confirmation
│   └── session.html          # Session info page
│
├── feedback/                 # Feedback collection templates
│   ├── base.html             # Base template
│   ├── search.html           # SR search page
│   ├── detail.html           # SR detail view
│   ├── submit.html           # Feedback submission
│   ├── success.html          # Success message
│   ├── error.html            # Error page
│   ├── list.html             # Feedback list
│   └── history.html          # Feedback history
│
├── team/                     # Team management templates
│   └── skill_view.html       # Team skills matrix
│
└── user/                     # User portal templates
    └── feedback_main.html    # Main feedback interface
```

---

## 🎯 Template Organization

### Base Templates
Each section has a base template that defines common layout:

```html
<!-- feedback/base.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}SR Feedback{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
</head>
<body>
    <nav>{% include 'nav.html' %}</nav>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>{% include 'footer.html' %}</footer>
</body>
</html>
```

### Child Templates
Child templates extend the base:

```html
<!-- feedback/search.html -->
{% extends "feedback/base.html" %}

{% block title %}Search SRs{% endblock %}

{% block content %}
<h1>Search Service Requests</h1>
<form method="GET" action="{{ url_for('user.search') }}">
    <input type="text" name="sr_id" placeholder="Enter SR ID...">
    <button type="submit">Search</button>
</form>
{% endblock %}
```

---

## 📋 Template Descriptions

### Admin Templates

| Template | Purpose |
|----------|---------|
| `dashboard.html` | Admin home with stats and quick actions |
| `upload.html` | Excel file upload form with progress bar |
| `reports.html` | List of generated reports with download links |

### Auth Templates

| Template | Purpose |
|----------|---------|
| `login.html` | Login form with username/password |
| `logout.html` | Logout confirmation page |
| `session.html` | Current session information |

### Feedback Templates

| Template | Purpose |
|----------|---------|
| `base.html` | Common layout for feedback pages |
| `search.html` | SR search form |
| `detail.html` | SR details with workaround display |
| `submit.html` | Feedback submission form |
| `success.html` | Success message after submission |
| `error.html` | Error display page |
| `list.html` | List all feedback entries |
| `history.html` | Feedback history for an SR |

### Team Templates

| Template | Purpose |
|----------|---------|
| `skill_view.html` | Team skills matrix with availability |

### User Templates

| Template | Purpose |
|----------|---------|
| `feedback_main.html` | Main user interface for feedback |

---

## 🎨 Template Variables

Common variables available in templates:

```python
# Passed from Flask routes
sr_id           # Service Request ID
sr_data         # SR details dictionary
workaround      # AI-generated workaround
feedback_list   # List of user feedback
stats           # Statistics dictionary
error_message   # Error message if any
success_message # Success message if any

# Flask built-ins
url_for()       # Generate URLs
request         # Current request object
session         # User session
g               # Request-global storage
```

---

## 🔧 Example Templates

### Search Page
```html
<!-- feedback/search.html -->
{% extends "feedback/base.html" %}

{% block content %}
<div class="search-container">
    <h1>🔍 Search Service Requests</h1>
    
    <form method="GET" action="{{ url_for('user.search') }}" class="search-form">
        <input type="text" 
               name="sr_id" 
               placeholder="Enter SR ID (e.g., CAS123456)"
               value="{{ request.args.get('sr_id', '') }}"
               required>
        <button type="submit">Search</button>
    </form>
    
    {% if results %}
    <div class="results">
        <h2>Search Results</h2>
        {% for sr in results %}
        <div class="sr-card">
            <h3>{{ sr.sr_id }}</h3>
            <p>{{ sr.description[:200] }}...</p>
            <a href="{{ url_for('user.feedback', sr_id=sr.sr_id) }}">
                View Details
            </a>
        </div>
        {% endfor %}
    </div>
    {% endif %}
</div>
{% endblock %}
```

### Feedback Form
```html
<!-- user/feedback_main.html -->
{% extends "feedback/base.html" %}

{% block content %}
<div class="feedback-container">
    <h1>📝 SR: {{ sr_id }}</h1>
    
    <!-- SR Details -->
    <section class="sr-details">
        <h2>Description</h2>
        <p>{{ sr_data.description }}</p>
        
        <h2>AI Workaround</h2>
        <div class="workaround">
            {{ sr_data.ai_workaround | safe }}
        </div>
    </section>
    
    <!-- Voting -->
    <section class="voting">
        <h3>Was this workaround helpful?</h3>
        <form method="POST" action="{{ url_for('api.vote') }}">
            <input type="hidden" name="sr_id" value="{{ sr_id }}">
            <button type="submit" name="vote" value="up">👍 Yes</button>
            <button type="submit" name="vote" value="down">👎 No</button>
        </form>
    </section>
    
    <!-- Correction Form -->
    <section class="correction">
        <h3>Submit Correction</h3>
        <form method="POST" action="{{ url_for('user.feedback', sr_id=sr_id) }}">
            <textarea name="corrected_workaround" 
                      rows="10" 
                      placeholder="Enter your corrected workaround..."></textarea>
            
            <label>Rating (optional):</label>
            <select name="rating">
                <option value="">-</option>
                <option value="1">1 ⭐</option>
                <option value="2">2 ⭐⭐</option>
                <option value="3">3 ⭐⭐⭐</option>
                <option value="4">4 ⭐⭐⭐⭐</option>
                <option value="5">5 ⭐⭐⭐⭐⭐</option>
            </select>
            
            <button type="submit">Submit Feedback</button>
        </form>
    </section>
</div>
{% endblock %}
```

### Admin Upload
```html
<!-- admin/upload.html -->
{% extends "admin/base.html" %}

{% block content %}
<div class="upload-container">
    <h1>📤 Upload SR Report</h1>
    
    <form method="POST" 
          action="{{ url_for('admin.upload') }}" 
          enctype="multipart/form-data"
          id="upload-form">
        
        <div class="file-input">
            <input type="file" 
                   name="file" 
                   accept=".xls,.xlsx"
                   required>
            <p>Supported formats: .xls, .xlsx (max 16MB)</p>
        </div>
        
        <button type="submit">Upload & Process</button>
    </form>
    
    <div id="progress" style="display: none;">
        <div class="progress-bar">
            <div class="progress-fill" id="progress-fill"></div>
        </div>
        <p id="progress-message">Processing...</p>
    </div>
</div>

<script>
document.getElementById('upload-form').addEventListener('submit', function() {
    document.getElementById('progress').style.display = 'block';
});
</script>
{% endblock %}
```

---

## 🎨 Styling

Templates reference CSS files in `static/css/`:
- `main.css` - Global styles
- `admin.css` - Admin portal styles
- `feedback.css` - Feedback form styles

---

## 🔗 Related Modules

- [App](../app/README.md) - Flask routes that render templates
- [Config](../config/README.md) - Template configuration

---

*Part of SR-Analyzer Templates Module*
