# India STEM Database - Quick Start Guide

## What is This?

A comprehensive database of **126 Science, Technology & Innovation organizations** across India, extracted from the official India Science and Technology Portal.

## Quick Access

### 1. View Dashboard (Recommended)
```
Open: STEM_Database_Dashboard.html
```
- Beautiful interactive interface
- Search functionality
- Browse by category/state
- Direct links to websites

### 2. Access Raw Data
```
Location: data/ folder
Main File: data/complete_data.json
```

## What's Inside?

### Organizations (126)
- Private Sector (DSIR Registered): 54
- Private Sector (CMIE & MNCs): 37
- Private Sector (R&D Potential): 19
- Central Labs & Research: 8
- Higher Education: 6
- State Government: 2

### Coverage
- **States**: 16 (Maharashtra, Gujarat, Karnataka, Tamil Nadu, etc.)
- **Cities**: 50+ cities across India
- **Sectors**: Government, Private, Education, Research

### Data Fields
Each organization includes:
- Name
- Official Website URL
- Category/Sector
- State
- City/District
- Contact Info (when available)

## How to Use

### Option 1: Dashboard (Easy)
1. Open `STEM_Database_Dashboard.html` in browser
2. Browse or search organizations
3. Click "Visit Website" to access organization sites

### Option 2: JSON Data (For Developers)
```javascript
// Load data
fetch('data/organizations.json')
  .then(r => r.json())
  .then(orgs => {
    console.log(`${orgs.length} organizations loaded`);
    // Use the data
  });
```

### Option 3: Python (For Analysis)
```python
import json

with open('data/organizations.json', 'r', encoding='utf-8') as f:
    orgs = json.load(f)

# Filter by state
maharashtra = [o for o in orgs if o['state'] == 'Maharashtra']
print(f"Maharashtra has {len(maharashtra)} organizations")
```

## File Structure

```
STEM Database/
├── STEM_Database_Dashboard.html    ← Open this!
├── README.md                        ← Full documentation
├── QUICK_START.md                   ← This file
├── PROJECT_COMPLETE.md              ← Project summary
│
├── data/                            ← All data here
│   ├── complete_data.json          ← Everything
│   ├── organizations.json          ← All orgs
│   ├── categorized_by_category.json
│   ├── categorized_by_state.json
│   └── summary.json
│
└── comprehensive_scraper.py         ← Update data
```

## Top Organizations by State

1. **Maharashtra**: 35 organizations
   - Includes major research labs and private companies
   
2. **Gujarat**: 16 organizations
   - Strong private sector presence
   
3. **Karnataka**: 15 organizations
   - Tech and research focused
   
4. **Tamil Nadu**: 11 organizations
   - Manufacturing and R&D
   
5. **Haryana**: 10 organizations
   - Industrial R&D centers

## Search Examples

In the dashboard, try searching for:
- **"Pharmaceuticals"** - Find pharma companies
- **"Gujarat"** - All Gujarat organizations
- **"DSIR"** - DSIR registered companies
- **"Research"** - Research institutions
- **"Bangalore"** - Bangalore-based orgs

## Update Data

To get latest data from the website:
```bash
python comprehensive_scraper.py
```
This will:
- Scrape latest organizations
- Update all JSON files
- Refresh statistics

## Integration

### Add to Website
```html
<div id="stem-orgs"></div>

<script>
fetch('data/organizations.json')
  .then(r => r.json())
  .then(orgs => {
    const html = orgs.map(o => `
      <div class="org">
        <h3>${o.name}</h3>
        <p>${o.category} | ${o.state}</p>
        <a href="${o.url}">Visit</a>
      </div>
    `).join('');
    document.getElementById('stem-orgs').innerHTML = html;
  });
</script>
```

### Use in Research
- Export to Excel/CSV
- Analyze by state/category
- Create visualizations
- Generate reports

## Features

✅ **126 Organizations** - Comprehensive coverage  
✅ **Real-time Search** - Find anything instantly  
✅ **Category Filters** - Browse by sector  
✅ **State Filters** - Browse by location  
✅ **Direct Links** - Access websites directly  
✅ **Responsive** - Works on mobile/tablet  
✅ **Beautiful UI** - Modern dark theme  
✅ **JSON Format** - Easy to integrate  

## Support

- **Documentation**: See README.md
- **Project Info**: See PROJECT_COMPLETE.md
- **Data Source**: indiascienceandtechnology.gov.in

## Quick Stats

```
Total Items:        131
Organizations:      126
Science Centres:    5
Categories:         6
States:             16
Files Created:      25
Data Files:         12
```

## Next Steps

1. ✅ Open `STEM_Database_Dashboard.html`
2. ✅ Explore the data
3. ✅ Use search to find organizations
4. ✅ Click links to visit websites
5. ✅ Integrate into your project

---

**Ready to use!** Open the dashboard and start exploring India's STEM ecosystem! 🚀





