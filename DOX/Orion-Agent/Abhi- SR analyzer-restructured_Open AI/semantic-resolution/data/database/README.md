# 🗄️ Database Module

> **SQLite Databases for Application Data**

This folder contains SQLite databases for various application functions.

---

## 📁 Structure

```
database/
├── README.md
├── abbreviation.db           # Abbreviation/acronym mappings
├── people_skills.db          # Team member skills & availability
├── sr_tracking.db            # SR processing tracking
├── workaround_feedback.db    # User feedback storage
├── llm_usage_stats.json      # LLM API usage statistics
└── database_creation/        # Database creation scripts
    └── create_database.py
```

---

## 📊 Database Schemas

### `people_skills.db`
**Purpose**: Team member skills, availability, and assignment tracking

```sql
-- Team members table
CREATE TABLE team_members (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    employee_id TEXT,
    email TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Skills table
CREATE TABLE skills (
    id INTEGER PRIMARY KEY,
    member_id INTEGER REFERENCES team_members(id),
    application TEXT,              -- SOM_MM, SQO_MM, etc.
    skill_level REAL,              -- 1.0 to 5.0
    max_load INTEGER,              -- Max daily SRs
    specializations TEXT,          -- JSON array
    current_load INTEGER DEFAULT 0,
    UNIQUE(member_id, application)
);

-- Assignment history
CREATE TABLE assignment_history (
    id INTEGER PRIMARY KEY,
    member_id INTEGER,
    sr_id TEXT,
    assigned_at TIMESTAMP,
    complexity_score INTEGER,
    resolution_time_hours REAL,
    success_rate REAL
);

-- Availability history
CREATE TABLE availability_history (
    id INTEGER PRIMARY KEY,
    member_id INTEGER,
    availability_percent INTEGER,  -- 0-100
    reason TEXT,
    effective_date DATE,
    recorded_at TIMESTAMP
);
```

### `sr_tracking.db`
**Purpose**: Track SR processing status and history

```sql
CREATE TABLE sr_processing (
    id INTEGER PRIMARY KEY,
    sr_id TEXT UNIQUE,
    status TEXT,                   -- pending, processed, error
    processed_at TIMESTAMP,
    source TEXT,                   -- email, upload, api
    output_file TEXT,
    error_message TEXT
);

CREATE TABLE processing_batches (
    id INTEGER PRIMARY KEY,
    batch_id TEXT,
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    total_srs INTEGER,
    successful INTEGER,
    failed INTEGER
);
```

### `abbreviation.db`
**Purpose**: Map abbreviations to full forms

```sql
CREATE TABLE abbreviations (
    id INTEGER PRIMARY KEY,
    abbreviation TEXT,
    full_form TEXT,
    category TEXT,
    source TEXT
);

CREATE VIRTUAL TABLE abbrev_fts USING fts5(
    abbreviation, full_form, category
);
```

### `workaround_feedback.db`
**Purpose**: Store user feedback on workarounds (legacy)

```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY,
    sr_id TEXT,
    user_email TEXT,
    original_workaround TEXT,
    corrected_workaround TEXT,
    feedback_type TEXT,           -- correction, approval, rejection
    submitted_at TIMESTAMP
);
```

---

## 📋 LLM Usage Statistics

`llm_usage_stats.json` tracks API usage:

```json
{
    "last_run": {
        "timestamp": "2026-01-07T10:30:00",
        "total_calls": 125,
        "input_tokens": 250000,
        "output_tokens": 75000,
        "total_cost": 0.4567,
        "calls_by_type": {
            "workaround_finder": 25,
            "java_detection": 25,
            "activity_extraction": 20,
            "resolution_generation": 25,
            "skill_assignment": 25
        }
    },
    "cumulative": {
        "total_calls": 15000,
        "total_cost": 45.67
    }
}
```

---

## 🔧 Database Operations

### Connect to Database

```python
import sqlite3

conn = sqlite3.connect("data/database/people_skills.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Query team members
cursor.execute("""
    SELECT tm.name, s.application, s.skill_level
    FROM team_members tm
    JOIN skills s ON tm.id = s.member_id
    WHERE tm.status = 'active'
""")

for row in cursor.fetchall():
    print(f"{row['name']}: {row['application']} ({row['skill_level']}/5)")
```

### Update Skill Level

```python
cursor.execute("""
    UPDATE skills
    SET skill_level = ?, updated_at = datetime('now')
    WHERE member_id = ? AND application = ?
""", (4.5, member_id, 'SOM_MM'))
conn.commit()
```

---

## 📦 Creation Scripts

### `database_creation/create_database.py`

Creates/initializes all database tables.

```python
python database_creation/create_database.py

# Creates all tables if not exist
# Upgrades schema if needed
```

---

## ⚠️ Backup

Databases should be backed up regularly:

```python
import shutil
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy(
    "data/database/people_skills.db",
    f"data/backup/people_skills_{timestamp}.db"
)
```

---

## 🔗 Related

- [Data/README.md](../README.md) - Data module overview
- [Team/README.md](../../team/README.md) - Team management

---

*Part of SR-Analyzer Data Module*
