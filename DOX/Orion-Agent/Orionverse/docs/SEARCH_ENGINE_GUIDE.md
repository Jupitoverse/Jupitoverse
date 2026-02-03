# 🔍 Orionverse OSO Search Engine - User Guide

**Version**: 1.0.0  
**Last Updated**: October 10, 2025  
**Author**: Orion DOX Team

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Features](#features)
4. [Search Filters](#search-filters)
5. [Data Sources](#data-sources)
6. [Workaround Management](#workaround-management)
7. [Export & Download](#export--download)
8. [Tips & Tricks](#tips--tricks)
9. [Troubleshooting](#troubleshooting)

---

## Overview

The **Orionverse OSO Search Engine** is a comprehensive, production-ready search tool designed for Amdocs and Comcast support teams. It allows you to search across **35,000+ Service Requests**, **2,500+ Defects**, and your team's **Workaround Inventory** simultaneously.

### Key Statistics
- 📋 **35,000+ Service Requests** from SR sheet
- 🐛 **2,500+ Defects** from Defect sheet
- 💡 **Unlimited Workarounds** in PostgreSQL database

### Team Coverage
- **DOX Teams**: OSO, AMIL, OT, DMAAS, SQO, ABP, ADH
- **NON-DOX Teams**: ELOC, OMW, Polaris, CLIPS, CAMP, SNP, CSP

---

## Quick Start

### Starting the Application

1. **Start Backend Server**:
   ```bash
   cd C:\Users\abhisha3\Desktop\Projects\Orion\Orionverse\backend
   python app.py
   ```
   ✅ Backend will run on `http://127.0.0.1:5001`

2. **Open Frontend**:
   - Open `C:\Users\abhisha3\Desktop\Projects\Orion\Orionverse\index.html` in your browser
   - Or serve via local server:
     ```bash
     python -m http.server 8000
     # Navigate to http://localhost:8000
     ```

3. **Navigate to Search Engine**:
   - Click on **"Search Anything"** in the top navigation
   - You're ready to search! 🎉

---

## Features

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| **Multi-Source Search** | Search across SRs, Defects, and Workarounds simultaneously |
| **5 Filter Types** | Customer ID, OSite ID, SR ID, Defect ID, Free Text |
| **Real-time Filtering** | Instant results from 37,500+ records |
| **Tab Navigation** | Switch between Workarounds, SRs, and Defects |
| **DataTables Integration** | Sortable, searchable, paginated tables |
| **Export Functionality** | Download results as CSV/Excel |
| **Workaround CRUD** | Create, Read, Update, Delete workarounds |
| **Rich Text Editor** | Quill.js for formatting solutions with images |
| **Responsive Design** | Works on desktop, tablet, and mobile |

### 🎯 Advanced Features

- **Statistics Dashboard**: Real-time count of records
- **Like & View Tracking**: Track popular workarounds
- **PDF Download**: Export workarounds as HTML documents
- **Bulk Export**: Download all workarounds at once
- **Search Highlighting**: Results highlight in tables
- **Empty State Handling**: Friendly messages when no results
- **Loading Indicators**: Visual feedback during searches
- **Error Handling**: Graceful error messages

---

## Search Filters

### 1. 🔎 Search Anything (Free Text)

**What it does**: Searches across all text fields in all data sources.

**Where it searches**:
- **SR Data**: DETAILS, UPDATE_DETAILS columns
- **Defect Data**: Name, Description columns
- **Workarounds**: Category, Issue, Description, Created By

**Example searches**:
```
"billing issue"
"OSite_623385_1"
"fallout"
"order stuck"
```

**Use cases**:
- Finding any mention of a keyword
- Broad searches when you don't know exact IDs
- Discovering related issues

---

### 2. 👤 Customer ID

**What it does**: Searches for specific customer identifiers.

**Format**: Typically starts with `13` (e.g., `130382820`)

**Where it searches**:
- **SR Data**: CUSTOMER_ID column (exact/partial match)
- **Defect Data**: Name, Description columns (mentioned anywhere)

**Example searches**:
```
130382820
13038
"Customer ID: 130382820"
```

**Use cases**:
- Finding all tickets for a specific customer
- Tracking customer history
- Customer-specific issues

---

### 3. 📍 OSite ID

**What it does**: Searches for site identifiers.

**Format**: `OSite_%_1` where `%` is a 5-6 digit number (e.g., `OSite_623385_1`)

**Where it searches**:
- **SR Data**: DETAILS, UPDATE_DETAILS columns
- **Defect Data**: Name, Description columns

**Example searches**:
```
OSite_623385_1
osite_623385_1 (case-insensitive)
623385
```

**Use cases**:
- Site-specific issues
- Location-based troubleshooting
- Multi-site customer tracking

---

### 4. 📄 SR ID (Service Request ID)

**What it does**: Searches for specific service request numbers.

**Format**: Alphanumeric (e.g., `CAS2570812`)

**Where it searches**:
- **SR Data**: SR_ID column (exact/partial match)
- **Defect Data**: Name, Description columns (mentioned anywhere)

**Example searches**:
```
CAS2570812
SR019577586
CAS
```

**Use cases**:
- Looking up specific tickets
- Finding related defects for an SR
- Tracking SR progress

---

### 5. 🆔 Defect ID

**What it does**: Searches for specific defect numbers.

**Format**: Numeric (e.g., `2860119`)

**Where it searches**:
- **SR Data**: DETAILS, UPDATE_DETAILS columns
- **Defect Data**: ID column (exact match)

**Example searches**:
```
2860119
2860
```

**Use cases**:
- Finding specific defects
- Tracking defect mentions in SRs
- Linking SRs to defects

---

## Data Sources

### 📋 Service Request (SR) Data

**Source**: `C:\Users\abhisha3\Desktop\OSO Automation\OSO Search Engine\Abhi_SE_V1.xlsx` → Sheet "SR"  
**Records**: 35,000+  
**Format**: JSON (`backend/data/sr_data.json`)

**Columns**:
- `SR_ID` - Unique service request identifier
- `CUSTOMER_ID` - Customer identifier
- `CUSTOMER_NAME` - Customer name
- `DETAILS` - Detailed description of the issue
- `UPDATE_DETAILS` - Updates and resolution details
- `RCA` - Root Cause Analysis
- `LBGUPS_Subcategory` - Issue category
- `Create_Date` - Creation date
- `Day_of_Restored` - Resolution date
- `Close_Date` - Closure date

**Features in Interface**:
- Sortable by any column
- Paginated (10, 25, 50, 100 records per page)
- In-table search
- Export to CSV
- View full details button

---

### 🐛 Defect Data

**Source**: `C:\Users\abhisha3\Desktop\OSO Automation\OSO Search Engine\Abhi_SE_V1.xlsx` → Sheet "Defect"  
**Records**: 2,500+  
**Format**: JSON (`backend/data/defect_data.json`)

**Columns**:
- `ID` - Unique defect identifier
- `Name` - Defect title/name
- `Description` - Detailed defect description
- `Phase` - Development phase
- `Release` - Release version

**Features in Interface**:
- Sortable by any column
- Paginated (10, 25, 50, 100 records per page)
- In-table search
- Export to CSV
- View full details button

---

### 💡 Workaround Inventory

**Source**: PostgreSQL database (`prodossdb.workarounds` table)  
**Records**: Dynamic (grows with team contributions)  
**Format**: Live database

**Fields**:
- `id` - Auto-increment ID
- `category` - Issue category (Billing, OSS, CRM, etc.)
- `issue` - Issue title
- `description` - Solution description (rich text with images)
- `created_by` - Author name
- `created_date` - Creation timestamp
- `views` - View count
- `likes` - Like count

**Features in Interface**:
- Card-based view
- Create new workarounds
- Edit existing workarounds
- Delete workarounds
- Like workarounds
- Track views
- Download as HTML/PDF
- Rich text with images, code blocks, formatting

---

## Workaround Management

### Creating a New Workaround

1. Click **"➕ New Workaround"** button
2. Fill in the form:
   - **Category**: e.g., "Billing", "OSS", "Provisioning"
   - **Issue Title**: Short, descriptive title
   - **Description**: Detailed solution using the rich text editor
3. Use the toolbar to:
   - Add headings, bold, italic, underline
   - Insert images (paste or upload)
   - Add code blocks
   - Create lists
   - Add links
4. Click **"Create Workaround"**

**Example Workaround**:
```
Category: Billing
Issue: Order Stuck in Fallout Manager

Description:
When an order is stuck, follow these steps:
1. Check the fallout manager first
2. Query ORDER_STATUS table using Customer ID
3. If no fallout found, manual kickstart required:
   - Go to Workflow Manager
   - Search order by ID
   - Click "Restart Workflow"
```

---

### Editing a Workaround

1. Click **"✏️ Edit"** on any workaround card
2. Make your changes
3. Click **"Update Workaround"**

---

### Deleting a Workaround

1. Click **"🗑️ Delete"** on any workaround card
2. Confirm deletion
3. Workaround is permanently removed

⚠️ **Note**: Deletion is permanent and cannot be undone!

---

### Viewing Full Workaround

1. Click **"📖 Read More"** on any workaround card
2. View full details in modal
3. Automatically increments view count

---

### Liking a Workaround

1. Click **"👍"** button on any workaround card
2. Like count increases by 1
3. Helps identify popular solutions

---

### Downloading Workarounds

**Single Download**:
1. Click **"📥 PDF"** on any workaround card
2. Downloads as HTML file (can be printed to PDF)

**Bulk Download**:
1. Click **"📥 Download All"** in Workaround section header
2. Downloads all visible workarounds

---

## Export & Download

### Exporting SR Data

1. Navigate to **Service Requests** tab
2. Click **"📥 Export to Excel"**
3. CSV file downloads with current results
4. Open in Excel, Google Sheets, etc.

**Filename Format**: `SR_Data_YYYY-MM-DD.csv`

---

### Exporting Defect Data

1. Navigate to **Defects** tab
2. Click **"📥 Export to Excel"**
3. CSV file downloads with current results

**Filename Format**: `Defect_Data_YYYY-MM-DD.csv`

---

### Exporting All Results

1. Click **"📥 Export Results"** in search filters section
2. Downloads both SR and Defect data as separate CSV files

---

## Tips & Tricks

### 🚀 Pro Tips

1. **Combine Filters**: Use multiple filters together for precise results
   ```
   Customer ID: 130382820
   + Search Anything: "billing"
   = All billing issues for customer 130382820
   ```

2. **Partial Matches**: Don't need exact IDs
   ```
   Instead of: OSite_623385_1
   Use: 623385
   ```

3. **Case Insensitive**: All searches work regardless of case
   ```
   "BILLING" = "billing" = "Billing"
   ```

4. **Quick Clear**: Click **"🔄 Clear Filters"** to reset all filters

5. **Tab Navigation**: Use keyboard shortcuts
   - `Alt + 1`: Workarounds tab
   - `Alt + 2`: SRs tab
   - `Alt + 3`: Defects tab

6. **DataTables Search**: Use the "Search in results" box in tables for additional filtering

7. **Sort Tables**: Click column headers to sort ascending/descending

8. **Page Size**: Adjust number of rows per page (10, 25, 50, 100)

---

### 🎯 Common Use Cases

#### Finding Customer Issues
```
Filter: Customer ID = 130382820
Result: All SRs and defects for this customer
```

#### Tracking Site Problems
```
Filter: OSite ID = OSite_623385_1
Result: All tickets for this specific site
```

#### Defect Research
```
Filter: Defect ID = 2860119
Result: Exact defect + all SRs mentioning it
```

#### Keyword Discovery
```
Filter: Search Anything = "fallout manager"
Result: All mentions across all sources
```

#### Complex Search
```
Filter: Customer ID = 130382820
      + Search Anything = "provisioning"
      + OSite ID = 623385
Result: Provisioning issues for customer at site
```

---

## Troubleshooting

### ❌ No Results Found

**Problem**: Search returns 0 results

**Solutions**:
1. Check spelling and case (though search is case-insensitive)
2. Try partial matches instead of exact IDs
3. Use "Search Anything" for broader results
4. Clear all filters and try again
5. Check if data source has the information

---

### ⚠️ Backend Not Running

**Problem**: "Failed to load data. Please ensure backend is running."

**Solutions**:
1. Start backend server:
   ```bash
   cd backend
   python app.py
   ```
2. Verify backend URL in `static/js/api.js`:
   ```javascript
   const API_BASE_URL = 'http://127.0.0.1:5001';
   ```
3. Check console for errors (F12 → Console)

---

### 🐌 Slow Performance

**Problem**: Search takes too long

**Solutions**:
1. Be more specific with filters
2. Use exact IDs when possible
3. Avoid very broad "Search Anything" queries
4. Close other browser tabs
5. Clear browser cache

---

### 📊 DataTables Not Loading

**Problem**: Tables show "Loading..." forever

**Solutions**:
1. Check browser console for errors (F12)
2. Verify backend is running
3. Hard refresh browser (Ctrl + Shift + R)
4. Check network tab in DevTools

---

### 💾 Database Connection Failed

**Problem**: Workarounds not loading

**Solutions**:
1. Check `backend/database.py` credentials
2. Verify PostgreSQL server is accessible:
   ```bash
   ping oso-pstgr-rd.orion.comcast.com
   ```
3. Check database logs
4. Test connection:
   ```bash
   cd backend
   python database.py
   ```

---

## Advanced Features

### 🔍 Regular Expressions

While not directly supported in UI, you can modify `backend/routes/search.py` to use regex:

```python
import re
pattern = re.compile(r'OSite_\d+_1', re.IGNORECASE)
filtered = [r for r in data if pattern.search(r.get('DETAILS', ''))]
```

---

### 📈 Analytics

Track usage with backend logs:
```bash
cd backend
tail -f nohup.out
```

See:
- Search patterns
- Popular filters
- Error rates

---

### 🎨 Customization

**Change Theme**: Edit `static/css/style.css`
```css
:root {
    --bg-primary: #0a0a12;  /* Dark background */
    --accent-primary: #8B5CF6;  /* Purple accent */
}
```

**Add Columns**: Edit DataTables initialization in `static/js/search.js`
```javascript
columns: [
    { data: 'SR_ID', title: 'SR ID' },
    { data: 'NEW_COLUMN', title: 'New Column' },  // Add here
]
```

---

## Performance Metrics

### Expected Performance

| Operation | Records | Time |
|-----------|---------|------|
| Initial Load | Top 10 each | < 1s |
| Filter (Customer ID) | ~100 results | < 2s |
| Filter (Search Anything) | ~500 results | < 3s |
| Export to CSV | 1,000 records | < 5s |
| DataTable Sort | Any | < 500ms |

### Optimization Tips

1. **Use Exact IDs**: Faster than text searches
2. **Limit Results**: More specific filters = faster
3. **Export Strategically**: Export only what you need
4. **Cache Results**: Backend caches JSON data in memory

---

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Enter` | Execute search (when in filter input) |
| `Esc` | Close modal |
| `Ctrl + F` | Focus DataTable search |
| `Tab` | Navigate between filters |

---

## Browser Compatibility

✅ **Supported**:
- Chrome 90+
- Firefox 88+
- Edge 90+
- Safari 14+

❌ **Not Supported**:
- Internet Explorer (any version)

---

## Data Refresh

### Updating Source Data

When SR or Defect Excel files are updated:

1. Replace files at:
   ```
   C:\Users\abhisha3\Desktop\OSO Automation\OSO Search Engine\Abhi_SE_V1.xlsx
   ```

2. Regenerate JSON:
   ```bash
   cd Orion/Orionverse
   python convert_excel.py
   ```

3. Restart backend:
   ```bash
   cd backend
   python app.py
   ```

---

## Security Notes

⚠️ **Current Implementation**:
- Database credentials hardcoded
- No authentication required
- All data publicly accessible

✅ **Recommended for Production**:
1. Move credentials to `.env` file
2. Implement JWT authentication
3. Add role-based access control
4. Enable HTTPS
5. Add input validation
6. Implement rate limiting

---

## Support & Contact

For issues, questions, or feature requests:
- **GitHub**: https://github.com/Jupitoverse/Dox
- **Team**: Orion DOX Operations Team
- **Documentation**: See ARCHITECTURE.md, DEVELOPER_GUIDE.md

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-10-10 | Initial release with full search functionality |

---

## License

Internal Amdocs/Comcast project - Not for public distribution

---

**Happy Searching! 🚀**

*For detailed technical documentation, see [ARCHITECTURE.md](ARCHITECTURE.md)*

