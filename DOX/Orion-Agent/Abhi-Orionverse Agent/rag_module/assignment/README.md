# 📋 Assignment Module

> **SR Assignment Logic and Daily Data Management**

This module handles the intelligent assignment of Service Requests to team members, including daily upload management and business day calculations.

---

## 📁 Structure

```
assignment/
├── __init__.py
├── README.md
├── daily_data_manager.py          # Daily upload management
└── priority_age_calculator.py     # Business day age calculation
```

---

## 📦 Key Components

### 1. `daily_data_manager.py` - DailyDataManager

Manages daily SR uploads and integration into the historical knowledge base.

**Key Class: `DailyDataManager`**

```python
from assignment.daily_data_manager import DailyDataManager

manager = DailyDataManager()

# Process daily upload
indexed_results = manager.process_daily_upload(excel_file, analyzer)

# Get SR by ID
sr = manager.get_sr_by_id("CAS123456")

# Get staging statistics
stats = manager.get_staging_stats()
```

**Key Methods:**

| Method | Description |
|--------|-------------|
| `process_daily_upload(excel_file, analyzer)` | Process uploaded Excel and stage SRs |
| `get_sr_by_id(sr_id)` | Retrieve SR from staging data |
| `get_all_staging_srs()` | Get all SRs in staging |
| `merge_daily_data()` | Merge staging data into historical index |
| `get_staging_stats()` | Get staging data statistics |

**Staging Data Structure:**
```python
staging_data = {
    'srs': [],              # List of analyzed SRs
    'last_updated': None,   # ISO timestamp
    'upload_count': 0       # Number of uploads today
}
```

**Processing Flow:**
```
1. Read Excel file
2. Convert to SR records
3. Analyze with AIEnhancedServiceRequestAnalyzer
4. Index by SR ID
5. Add to staging
6. Move processed file to processed/ folder
```

**Directory Structure:**
```
daily_uploads/
├── (uploaded files placed here)
└── processed/
    └── (moved after processing with timestamp)
```

---

### 2. `priority_age_calculator.py` - PriorityAgeCalculator

Calculates SR age in business days (excluding weekends and holidays).

**Key Class: `PriorityAgeCalculator`**

```python
from assignment.priority_age_calculator import PriorityAgeCalculator

calculator = PriorityAgeCalculator()

# Calculate business days
business_days = calculator.calculate_business_days("2026-01-01")
print(f"SR is {business_days} business days old")

# Get formatted age string
age_str, days = calculator.get_formatted_age("2026-01-01")
print(f"Age: {age_str}")  # "5 business days"
```

**Key Methods:**

| Method | Description |
|--------|-------------|
| `calculate_business_days(submit_date)` | Calculate business days since date |
| `get_formatted_age(submit_date)` | Get human-readable age string |
| `is_business_day(date)` | Check if date is a business day |
| `add_business_days(date, days)` | Add business days to a date |

**Business Day Rules:**
- Excludes weekends (Saturday, Sunday)
- Excludes configured holidays
- Handles various date formats

**Date Format Support:**
```python
# Supported formats:
calculator.calculate_business_days("2026-01-01")           # ISO string
calculator.calculate_business_days("01/01/2026")           # US format
calculator.calculate_business_days(datetime(2026, 1, 1))   # datetime object
calculator.calculate_business_days(pd.Timestamp(...))      # pandas Timestamp
```

**Holiday Configuration:**
```python
# Default holidays (can be customized)
holidays = [
    "2026-01-01",  # New Year's Day
    "2026-07-04",  # Independence Day
    "2026-12-25",  # Christmas
    # ... more holidays
]
```

---

## 📊 Assignment Strategy

The assignment module works with the RAG pipeline's LLM #5 to assign SRs:

### Priority-Based Assignment

| Priority | Strategy |
|----------|----------|
| P1 | Assign to top expert (skill ≥ 4.5) |
| P2 | Assign to advanced member (skill ≥ 4.0) |
| P3 | Standard assignment with load balancing |
| P4 | Prefer junior members (save experts) |

### Load Balancing

```python
# Effective load calculation
effective_max_load = max_load * (availability / 100)

# Example:
# max_load = 10, availability = 50%
# effective_max_load = 5
```

### Equal Distribution

```python
# Everyone gets at least one SR before anyone gets a second
daily_assignments = {}  # {member_name: count}

# Sort by current load
candidates.sort(key=lambda x: daily_assignments.get(x, 0))
```

---

## 🔄 Daily Merge Process

The `merge_daily_data()` method runs as a nightly job:

```
1. Load staging data (today's uploads)
2. Load historical index
3. Get existing SR IDs
4. Convert staging SRs to historical format
5. Skip duplicates (already in history)
6. Add new records to historical data
7. Update index metadata
8. Create backup of old index
9. Save updated index
10. Clear staging data
```

**Historical Record Format:**
```python
{
    'sr_id': 'CAS123456',
    'description': '...',
    'searchable_text': '...',
    'priority': 'P2',
    'assigned_group': 'SOM_MM',
    'status': 'Resolved',
    'outcome': {
        'has_workaround': True,
        'workaround_text': '...',
        'resolution_type': 'Daily Upload'
    },
    'source_file': 'daily_upload',
    'resolution': '...',
    'created_date': '2026-01-07T10:30:00',
    'success_flag': True,
    'application': 'SOM_MM',
    'functional_area': 'DCP',
    'keywords': [],
    'phase1_workaround': {}
}
```

---

## 📈 Usage Example

```python
from assignment.daily_data_manager import DailyDataManager
from assignment.priority_age_calculator import PriorityAgeCalculator
from analyzers.batch_sr_analyser import AIEnhancedServiceRequestAnalyzer

# Initialize components
manager = DailyDataManager()
calculator = PriorityAgeCalculator()
analyzer = AIEnhancedServiceRequestAnalyzer()

# Process daily upload
results = manager.process_daily_upload("uploads/today.xlsx", analyzer)
print(f"Processed {len(results)} SRs")

# Get staging stats
stats = manager.get_staging_stats()
print(f"Staging: {stats['sr_count']} SRs")

# Calculate age for each SR
for sr_id, sr_data in results.items():
    age_str, days = calculator.get_formatted_age(sr_data.get('Created Date'))
    print(f"{sr_id}: {age_str}")

# Nightly merge (run as scheduled job)
new_count = manager.merge_daily_data()
print(f"Merged {new_count} new SRs to history")
```

---

## ⚙️ Configuration

### File Paths
```python
staging_path = 'data/vectorstore/staging_sr_data.pkl'
historical_path = 'data/vectorstore/historical_sr_index.pkl'
daily_uploads_dir = 'daily_uploads'
processed_dir = 'daily_uploads/processed'
```

### Auto-Created Directories
```python
os.makedirs('daily_uploads', exist_ok=True)
os.makedirs('daily_uploads/processed', exist_ok=True)
os.makedirs('data/vectorstore', exist_ok=True)
```

---

## 🔗 Related Modules

- [Team](../team/README.md) - Skills database for assignment
- [RAG Pipeline](../RAG/README.md) - LLM-based assignment
- [Admin](../admin/README.md) - Upload processing

---

*Part of SR-Analyzer Assignment Module*
