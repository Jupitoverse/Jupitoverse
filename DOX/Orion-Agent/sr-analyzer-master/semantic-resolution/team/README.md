# 👥 Team Module

> **Team Skills Database with ML Learning**

Manages team member skills, specializations, workload capacity, and availability.

---

## 📁 Structure

```
team/
├── __init__.py
├── README.md
└── people_skills_database.py    # PeopleSkillsDatabase (1948 lines)
```

---

## 🚀 Quick Start

```python
from team.people_skills_database import PeopleSkillsDatabase

db = PeopleSkillsDatabase("data/database/people_skills.db")

# Load from Excel
db.load_people_from_excel("People.xlsx")

# Get team configuration
config = db.get_team_configuration()

# Get top experts for an application
experts = db.get_top_experts("SOM_MM", top_n=3)

# Get all active members
members = db.get_all_people()
```

---

## 📦 `people_skills_database.py`

### Class: `PeopleSkillsDatabase`

**Lines:** 1948  
**Features:** Skills management, availability tracking, ML learning

### Key Methods

| Method | Description |
|--------|-------------|
| `load_people_from_excel()` | Load team from Excel |
| `get_team_configuration()` | Get all skills config |
| `get_top_experts(app)` | Get experts for app |
| `get_all_people()` | Get all active members |
| `set_member_availability()` | Set availability |
| `get_member_availability()` | Get availability |
| `record_assignment()` | Record for ML learning |
| `get_member_by_email()` | Lookup by email |

---

## 🗄️ Database Schema

### `team_members` Table

```sql
CREATE TABLE team_members (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    employee_id TEXT UNIQUE,
    email TEXT,
    status TEXT DEFAULT 'active',
    created_date DATETIME,
    updated_date DATETIME
);
```

### `skills` Table

```sql
CREATE TABLE skills (
    id INTEGER PRIMARY KEY,
    member_id INTEGER,
    application TEXT,           -- SOM_MM, SQO_MM, etc.
    skill_level REAL,           -- 1.0 to 5.0
    specializations TEXT,       -- JSON array
    max_load INTEGER DEFAULT 10,
    confidence_score REAL DEFAULT 0.5
);
```

### `assignment_history` Table

```sql
CREATE TABLE assignment_history (
    id INTEGER PRIMARY KEY,
    member_id INTEGER,
    sr_id TEXT,
    application TEXT,
    complexity_score REAL,
    success_rate REAL,
    resolution_time_hours REAL
);
```

### `availability_history` Table

```sql
CREATE TABLE availability_history (
    id INTEGER PRIMARY KEY,
    member_id INTEGER,
    availability_percent INTEGER,
    availability_type TEXT,
    reason TEXT,
    start_date DATETIME,
    end_date DATETIME
);
```

---

## 📊 Skill Levels

| Level | Label | Assignment Priority |
|-------|-------|---------------------|
| 4.5-5.0 | Expert | P1/P2 SRs, Complex issues |
| 3.5-4.4 | Advanced | Standard complex SRs |
| 2.5-3.4 | Intermediate | Regular SRs |
| 1.0-2.4 | Fresher | Simple SRs, with mentoring |

---

## 📁 People.xlsx Format

```
| Team Member    | App     | Skill Level | Max Load | Specialization    | Email              |
|----------------|---------|-------------|----------|-------------------|-------------------|
| Praveer Dubey  | SOM_MM  | 4.5/5       | 12       | Java/Backend      | praveerd@amdocs   |
| Prateek Jain   | SOM_MM  | 4.0/5       | 10       | EVC/Bandwidth     | prateek.jain5@... |
| Smitesh Kadia  | SQO_MM  | 3.5/5       | 10       | Quotes/Pricing    | smitesh.kadia@... |
```

---

## 🔄 Availability Management

```python
# Set availability
db.set_member_availability(
    member_name="John Smith",
    availability_percent=50,
    availability_type="half_day",
    reason="Training",
    end_date="2026-01-25"
)

# Get availability
avail = db.get_member_availability("John Smith")
# {'availability_percent': 50, 'availability_type': 'half_day', ...}
```

---

## 🧠 ML Learning

The system tracks assignment history to learn:
- Which members handle certain SR types well
- Resolution time patterns
- Success rates by application area
- Keyword associations

---

## 🔗 Related

- [RAG/README.md](../RAG/README.md) - Uses skills for assignment
- [app/routes/team.py](../app/routes/team.py) - Team management UI
- [templates/team/README.md](../templates/team/README.md) - Team templates

---

*Part of SR-Analyzer Team Module*
