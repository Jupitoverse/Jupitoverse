# India STEM Database

Comprehensive database of Science, Technology & Innovation organizations in India, scraped from the official India Science and Technology Portal.

## Overview

This database contains detailed information about various STEM organizations across India, categorized by type, state, and sector.

## Data Statistics

- **Total Organizations**: 126
- **Science Centres**: 5
- **Categories**: 6
- **States Covered**: 16
- **Last Updated**: November 2, 2025

## Data Categories

### By Sector
1. **Private Sector - DSIR Registered**: 54 organizations
2. **Private Sector - CMIE Database & Multinational Companies**: 37 organizations
3. **Private Sector - Potential to undertake R&D**: 19 organizations
4. **Central Sector - Labs & Research Institutions**: 8 organizations
5. **Higher Education Sector**: 6 organizations
6. **State Sector - Government Institutions**: 2 organizations

### By State (Top 10)
1. Maharashtra: 35
2. Gujarat: 16
3. Karnataka: 15
4. Tamil Nadu: 11
5. Haryana: 10
6. Telangana: 9
7. Delhi: 5
8. Uttar Pradesh: 5
9. Andhra Pradesh: 5
10. West Bengal: 4

## Files Structure

```
STEM Database/
├── data/
│   ├── complete_data.json                    # All data in one file
│   ├── organizations.json                    # All organizations
│   ├── science_centres.json                  # Science centres
│   ├── categorized_by_category.json          # Organized by category
│   ├── categorized_by_state.json             # Organized by state
│   ├── categorized_by_type.json              # Organized by type
│   └── summary.json                          # Statistics summary
├── STEM_Database_Dashboard.html              # Interactive dashboard
├── comprehensive_scraper.py                  # Main scraper script
├── scrape_improved.py                        # Organization scraper
└── README.md                                 # This file
```

## Data Fields

Each organization entry contains:
- **name**: Organization name
- **url**: Official website
- **category**: Organization category/sector
- **state**: State location
- **city**: City/district
- **contact**: Contact information (when available)

## Usage

### View Dashboard
Simply open `STEM_Database_Dashboard.html` in any modern web browser to:
- Browse all organizations
- Filter by category or state
- Search organizations
- View statistics
- Access organization websites

### Access Raw Data
All data is available in JSON format in the `data/` folder:

```javascript
// Load complete data
fetch('data/complete_data.json')
  .then(response => response.json())
  .then(data => {
    console.log(data.organizations);
    console.log(data.science_centres);
  });
```

### Run Scraper
To update the database with latest data:

```bash
cd "C:\Users\abhisha3\Desktop\Projects\Jupitoverse\STEM Database"
python comprehensive_scraper.py
```

## Features

### Dashboard Features
- **Interactive Search**: Real-time search across all fields
- **Category View**: Browse organizations by sector
- **State View**: Browse organizations by location
- **Statistics**: Visual overview of database
- **Responsive Design**: Works on all devices
- **Direct Links**: Quick access to organization websites

### Data Features
- **Comprehensive**: Covers multiple sectors
- **Structured**: Well-organized JSON format
- **Categorized**: Multiple categorization methods
- **Updated**: Regular scraping capability
- **Accessible**: Easy to use and integrate

## Data Source

All data is scraped from the official India Science and Technology Portal:
- **Website**: https://www.indiascienceandtechnology.gov.in/
- **Section**: Organizations → State S&T Organizations → All S&T Institution
- **Method**: Automated web scraping with BeautifulSoup

## Technical Details

### Technologies Used
- **Python 3.x**: Scraping and data processing
- **BeautifulSoup4**: HTML parsing
- **Requests**: HTTP requests
- **HTML/CSS/JavaScript**: Dashboard interface

### Scraper Features
- SSL certificate handling
- Rate limiting (polite scraping)
- Error handling and logging
- Multiple categorization
- JSON export

## Integration

### For Jupitoverse Website
```html
<!-- Include in your HTML -->
<script src="data/complete_data.json"></script>

<!-- Display organizations -->
<div id="stem-organizations"></div>

<script>
fetch('data/organizations.json')
  .then(r => r.json())
  .then(orgs => {
    const html = orgs.map(org => `
      <div class="org-card">
        <h3>${org.name}</h3>
        <p>${org.category}</p>
        <a href="${org.url}">Visit</a>
      </div>
    `).join('');
    document.getElementById('stem-organizations').innerHTML = html;
  });
</script>
```

### For API/Backend
```python
import json

# Load data
with open('data/organizations.json', 'r', encoding='utf-8') as f:
    organizations = json.load(f)

# Filter by state
maharashtra_orgs = [org for org in organizations if org['state'] == 'Maharashtra']

# Filter by category
dsir_orgs = [org for org in organizations if 'DSIR' in org['category']]
```

## Future Enhancements

- [ ] Add more sections (research labs, universities, funding schemes)
- [ ] Include contact details and addresses
- [ ] Add organization descriptions
- [ ] Include research areas and specializations
- [ ] Add collaboration opportunities
- [ ] Include funding information
- [ ] Add news and updates
- [ ] Create API endpoints

## Contributing

To add more data or improve the scraper:
1. Modify `comprehensive_scraper.py`
2. Add new scraping methods
3. Update categorization logic
4. Run scraper to generate new data
5. Test dashboard with new data

## License

This database is compiled from publicly available information on the India Science and Technology Portal. Please refer to the original source for usage terms and conditions.

## Contact

For questions or suggestions:
- **Project**: Jupitoverse STEM Database
- **Location**: C:\Users\abhisha3\Desktop\Projects\Jupitoverse\STEM Database
- **Last Updated**: November 2, 2025

## Acknowledgments

- **Data Source**: India Science and Technology Portal (indiascienceandtechnology.gov.in)
- **Purpose**: Educational and research purposes
- **Part of**: Jupitoverse Project

---

**Note**: This database is regularly updated. Run the scraper periodically to get the latest information.





