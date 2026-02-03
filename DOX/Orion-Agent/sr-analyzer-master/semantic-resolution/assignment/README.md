# 📋 Assignment Module

> **SR Assignment Logic and Daily Data Management**

Handles SR assignment and daily upload management.

---

## 📁 Structure

```
assignment/
├── __init__.py
├── README.md
├── daily_data_manager.py        # Daily upload management
└── priority_age_calculator.py   # Business day calculations
```

---

## 📦 `daily_data_manager.py`

### Class: `DailyDataManager`

Manages daily SR uploads and integration.

```python
from assignment.daily_data_manager import DailyDataManager

manager = DailyDataManager()

# Process daily upload
results = manager.process_daily_upload("report.xlsx", analyzer)

# Merge to historical
manager.merge_daily_data()
```

---

## 📦 `priority_age_calculator.py`

### Class: `PriorityAgeCalculator`

Calculates SR age in business days.

```python
from assignment.priority_age_calculator import PriorityAgeCalculator

calc = PriorityAgeCalculator()

# Calculate business day age
age = calc.calculate_business_day_age("2026-01-15")
print(f"Age: {age} business days")

# Check if priority met
is_met = calc.is_sla_met("P2", age)
```

### SLA Targets

| Priority | Target (Business Days) |
|----------|------------------------|
| P1 | 1 day |
| P2 | 3 days |
| P3 | 5 days |
| P4 | 10 days |

---

## 🔗 Related

- [admin/README.md](../admin/README.md) - Uses assignment
- [team/README.md](../team/README.md) - Skills database

---

*Part of SR-Analyzer Assignment Module*
