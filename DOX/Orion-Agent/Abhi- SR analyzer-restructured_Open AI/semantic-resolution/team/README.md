# 👥 Team Module

> **Team Skills Database with ML Learning Capabilities**

This module manages team member skills, specializations, workload capacity, and availability tracking with machine learning-based skill evolution.

---

## 📁 Structure

```
team/
├── __init__.py
├── README.md
└── people_skills_database.py    # Main: PeopleSkillsDatabase class
```

---

## 🔧 Key Class: `PeopleSkillsDatabase`

The central class for managing team skills and assignments.

```python
from team.people_skills_database import PeopleSkillsDatabase

db = PeopleSkillsDatabase(db_path="data/database/people_skills.db")

# Load from Excel
db.load_people_from_excel("People.xlsx")

# Get team configuration
config = db.get_team_configuration()

# Get top experts
experts = db.get_top_experts("SOM_MM", top_n=3)
```

---

## 📊 Database Schema

### `team_members` Table
```sql
CREATE TABLE team_members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    employee_id TEXT UNIQUE,
    status TEXT DEFAULT 'active',
    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_date DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

### `skills` Table
```sql
CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    application TEXT NOT NULL,           -- SOM_MM, SQO_MM, etc.
    skill_level REAL NOT NULL,           -- 1.0 to 5.0
    specializations TEXT,                -- JSON array
    max_load INTEGER NOT NULL DEFAULT 10,
    min_load INTEGER DEFAULT 0,
    confidence_score REAL DEFAULT 0.5,   -- ML confidence
    last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES team_members (id),
    UNIQUE(member_id, application)
)
```

### `assignment_history` Table
```sql
CREATE TABLE assignment_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER,
    sr_id TEXT,
    application TEXT,
    area TEXT,
    assigned_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    complexity_score REAL,
    success_rate REAL,                   -- 0.0 to 1.0
    resolution_time_hours REAL,
    feedback_score REAL,                 -- Customer feedback
    keywords TEXT,                       -- JSON array
    FOREIGN KEY (member_id) REFERENCES team_members (id)
)
```

### `skill_evolution` Table
```sql
CREATE TABLE skill_evolution (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER,
    application TEXT,
    old_skill_level REAL,
    new_skill_level REAL,
    change_reason TEXT,
    ml_confidence REAL,
    updated_by TEXT,                     -- 'ML', 'USER', 'ADMIN'
    update_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES team_members (id)
)
```

### `availability_history` Table
```sql
CREATE TABLE availability_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    availability_percent INTEGER NOT NULL,  -- 0-100
    availability_type TEXT DEFAULT 'full_day',
    reason TEXT,
    start_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    end_date DATETIME,                      -- NULL = indefinite
    updated_by TEXT DEFAULT 'ADMIN',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES team_members (id)
)
```

---

## 📋 Key Methods

### Loading Data

```python
def load_people_from_excel(self, excel_path: str = "People.xlsx") -> bool:
    """
    Load team data from Excel file.
    
    Features:
    - Auto-detects new columns and updates schema
    - Handles deletions (removes DB records not in Excel)
    - Cleans duplicate entries
    - Parses skill levels (e.g., "3/5" → 3.0)
    
    Excel Format:
    | Team Member | App    | Skill Level | Max Load | Specialization       |
    |-------------|--------|-------------|----------|----------------------|
    | John Smith  | SOM_MM | 4.5/5       | 12       | Java/Provisioning    |
    """
```

### Querying Data

```python
def get_team_configuration(self) -> Dict[str, Any]:
    """
    Get all active team members with their skills.
    
    Returns:
        {
            'John Smith': {
                'status': 'active',
                'applications': {
                    'SOM_MM': {
                        'skill_level': 4.5,
                        'max_load': 12,
                        'specializations': ['Java', 'Provisioning']
                    }
                }
            }
        }
    """

def get_top_experts(self, application: str, top_n: int = 3) -> List[int]:
    """
    Get top N experts by skill level for an application.
    Used for P1/P2 priority SRs.
    
    Returns member IDs sorted by skill level (highest first).
    Only includes members with skill_level >= 4.0.
    """

def get_all_member_names(self) -> List[str]:
    """Get list of all active team member names."""

def get_all_people(self) -> List[Dict[str, Any]]:
    """
    Get all active members with availability and skills.
    
    Returns:
        [
            {
                'name': 'John Smith',
                'status': 'active',
                'current_availability': 100,
                'skill_level': 'Expert',
                'application': 'SOM_MM',
                'applications': ['SOM_MM', 'SQO_MM']
            }
        ]
    """
```

### Availability Management

```python
def set_member_availability(
    self,
    member_name: str,
    availability_percent: int,    # 0-100
    availability_type: str = 'full_day',  # full_day, half_day, unavailable
    reason: str = '',
    end_date: str = None          # ISO format, None = permanent
) -> bool:
    """Set availability for a team member."""

def get_member_availability(self, member_name: str) -> Dict[str, Any]:
    """
    Get current availability for a member.
    
    Returns:
        {
            'availability_percent': 50,
            'availability_type': 'half_day',
            'reason': 'Training',
            'end_date': '2026-01-15'
        }
    """

def get_all_members_availability(self) -> List[Dict[str, Any]]:
    """Get availability for all active members."""
```

### Assignment Tracking

```python
def record_assignment(
    self,
    member_name: str,
    assignment_data: Dict[str, Any]
) -> bool:
    """
    Record an assignment for ML learning.
    
    assignment_data:
        {
            'sr_id': 'CAS123456',
            'application': 'SOM_MM',
            'area': 'Provisioning',
            'complexity_score': 0.7,
            'success_rate': 0.9,
            'resolution_time_hours': 2.5,
            'feedback_score': 0.85,
            'keywords': ['EVC', 'Bandwidth']
        }
    """
```

### Configuration Updates

```python
def update_member_config_via_chat(
    self,
    member_name: str,
    updates: Dict[str, Any],
    changed_by: str = "CHATBOT"
) -> bool:
    """
    Update member configuration via chatbot commands.
    
    Supported updates:
    - skill_level: Update skill level for an application
    - max_load: Update maximum workload
    - add_specialization: Add new specialization
    
    Also updates People.xlsx to maintain consistency.
    """
```

### Skill Evolution

```python
def get_skill_evolution_report(
    self,
    member_name: str = None,
    days: int = 30
) -> Dict[str, Any]:
    """
    Get skill evolution report for analysis.
    
    Returns:
        {
            'total_changes': 15,
            'changes': [...],
            'summary': {
                'ml_updates': 10,
                'user_updates': 5,
                'avg_confidence': 0.85
            }
        }
    """
```

---

## 📊 Skill Levels

| Level | Label | Description |
|-------|-------|-------------|
| 4.5+ | Expert | Senior specialist, handles P1/P2 |
| 3.5-4.4 | Advanced | Experienced, can handle complex SRs |
| 2.5-3.4 | Intermediate | Standard skill level |
| 1.0-2.4 | Fresher | Junior, handles simpler SRs |

---

## 📁 People.xlsx Format

```
| Team Member    | App     | Skill Level | Max Load | Min Load | Specialization            |
|----------------|---------|-------------|----------|----------|---------------------------|
| Praveer Dubey  | SOM_MM  | 4.5/5       | 12       | 2        | Java/Provisioning/Backend |
| Prateek Jain   | SOM_MM  | 4.0/5       | 10       | 2        | EVC/Bandwidth/Orders      |
| Smitesh Kadia  | SQO_MM  | 3.5/5       | 10       | 1        | Quotes/Pricing            |
```

---

## 🔄 Automatic Schema Updates

When loading from Excel, the system:

1. **Detects new columns** in Excel not in database
2. **Adds columns** to `skills` table automatically
3. **Removes obsolete records** not in Excel
4. **Cleans duplicates** keeping latest entry
5. **Updates People.xlsx** when changes made via chatbot

---

## 🧠 ML Learning

The system tracks assignment history to learn:

- Which members handle certain SR types well
- Resolution time patterns
- Success rates by area
- Keyword associations

This data can be used to improve assignment recommendations over time.

---

## 📈 Usage Example

```python
from team.people_skills_database import PeopleSkillsDatabase

# Initialize
db = PeopleSkillsDatabase("data/database/people_skills.db")

# Load team from Excel
db.load_people_from_excel("People.xlsx")

# Get experts for SOM_MM application
experts = db.get_top_experts("SOM_MM", top_n=3)
print(f"Top experts: {experts}")

# Set member availability
db.set_member_availability(
    member_name="John Smith",
    availability_percent=50,
    availability_type="half_day",
    reason="Training",
    end_date="2026-01-15"
)

# Record an assignment
db.record_assignment("John Smith", {
    'sr_id': 'CAS123456',
    'application': 'SOM_MM',
    'complexity_score': 0.7,
    'success_rate': 1.0
})

# Get skill evolution report
report = db.get_skill_evolution_report(days=30)
print(f"Skill changes: {report['total_changes']}")
```

---

## 🔗 Related Modules

- [RAG Pipeline](../RAG/README.md) - Uses skills for assignment
- [Admin](../admin/README.md) - Team management UI
- [App](../app/README.md) - Team routes

---

*Part of SR-Analyzer Team Module*
