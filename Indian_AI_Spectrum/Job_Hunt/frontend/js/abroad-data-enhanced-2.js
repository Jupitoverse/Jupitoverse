// Enhanced Country Migration Data - Part 2 (USA, UK, Australia, Singapore)
// Complete migration guide for Indian IT Professionals

const ENHANCED_COUNTRY_DATA_2 = {

    // ==================== USA ====================
    USA: {
        basic_info: {
            official_name: 'United States of America',
            capital: 'Washington D.C.',
            tech_hubs: 'San Francisco, Seattle, New York, Austin, Boston',
            currency: 'USD (US Dollar)',
            exchange_rate: '1 USD ≈ ₹83',
            timezone: 'GMT-5 to GMT-8 (varies by state)',
            flight_time: '15-20 hours from India',
            language: 'English',
            indian_population: '4.5 Million+ (2nd largest Asian group)',
            total_it_professionals: '1 Million+ Indians in tech',
            visa_processing: '6-18 months (H1B lottery based)',
            visa_cost: '$190 visa + $500 USCIS = ₹57,000+',
            tax_rate: '10-37% Federal + State (0-13%)'
        },

        why_indians_migrate: [
            'Highest tech salaries globally',
            'Silicon Valley - World tech capital',
            'Best career growth opportunities',
            'Top universities for kids',
            'Innovation and startup ecosystem',
            'Large established Indian community',
            'English speaking',
            'World-class infrastructure',
            'Diverse opportunities',
            'Path to Green Card (though long)'
        ],

        step_by_step_migration: [
            {step: 1, title: 'Get Job Offer', details: 'Need H1B sponsoring employer. Apply to companies that sponsor H1B.', duration: '3-12 months'},
            {step: 2, title: 'H1B Lottery', details: 'Employer files petition in March. Lottery in April. 30% selection rate.', duration: 'March-September'},
            {step: 3, title: 'H1B Approval', details: 'If selected, USCIS processes petition. Premium processing available.', duration: '2-6 months'},
            {step: 4, title: 'Visa Stamping', details: 'Interview at US Embassy in India. Book early, prepare well.', duration: '2-4 weeks'},
            {step: 5, title: 'Fly to USA', details: 'Enter before H1B activation date (Oct 1 for new H1Bs).', duration: '1 day'},
            {step: 6, title: 'Get SSN', details: 'Social Security Number - apply at SSA office after arrival.', duration: '1-2 weeks'},
            {step: 7, title: 'Bank Account', details: 'Chase, Bank of America, Wells Fargo. Need SSN/passport.', duration: '1 day'},
            {step: 8, title: 'Get SIM/Phone', details: 'T-Mobile, AT&T, Verizon. Need SSN for postpaid.', duration: '1 hour'},
            {step: 9, title: 'Find Housing', details: 'Zillow, Apartments.com, Craigslist. Credit history needed.', duration: '2-4 weeks'},
            {step: 10, title: 'DMV & License', details: 'Get state driver\'s license. Essential for ID.', duration: '1-2 weeks'}
        ],

        essential_apps: {
            government: ['USCIS App', 'CBP One', 'myE-Verify', 'IRS2Go'],
            banking: ['Chase', 'Bank of America', 'Wells Fargo', 'Zelle', 'Venmo', 'Cash App'],
            transport: ['Uber', 'Lyft', 'Google Maps', 'Apple Maps', 'Waze'],
            food_grocery: ['DoorDash', 'UberEats', 'Grubhub', 'Instacart', 'Amazon Fresh', 'Walmart'],
            housing: ['Zillow', 'Apartments.com', 'Realtor.com', 'Redfin', 'Craigslist'],
            shopping: ['Amazon', 'Target', 'Walmart', 'Costco', 'BestBuy'],
            social: ['LinkedIn', 'Meetup', 'Facebook Groups', 'Nextdoor']
        },

        essential_websites: {
            job_portals: ['linkedin.com', 'indeed.com', 'glassdoor.com', 'dice.com', 'hired.com', 'levels.fyi'],
            h1b_info: ['h1bdata.info', 'myvisajobs.com', 'trackitt.com'],
            government: ['uscis.gov', 'travel.state.gov', 'usa.gov'],
            housing: ['zillow.com', 'apartments.com', 'realtor.com', 'redfin.com'],
            salary: ['levels.fyi', 'glassdoor.com', 'blind (app)']
        },

        sim_cards: {
            providers: [
                {name: 'T-Mobile', monthly: '$50-85', note: 'Good coverage, flexible plans'},
                {name: 'Verizon', monthly: '$65-90', note: 'Best coverage, expensive'},
                {name: 'AT&T', monthly: '$55-85', note: 'Good coverage'},
                {name: 'Mint Mobile', monthly: '$15-30', note: 'Budget prepaid (T-Mobile network)'},
                {name: 'Google Fi', monthly: '$20-50', note: 'Flexible, good for international'}
            ],
            requirements: ['SSN for postpaid (or deposit)', 'Passport', 'Credit card']
        },

        cv_format: {
            style: 'American Resume format',
            length: '1-2 pages only',
            photo: 'NEVER include (discrimination concerns)',
            must_include: ['Summary/Objective', 'Skills section', 'Quantified achievements (metrics)', 'Education', 'Relevant certifications'],
            avoid: ['Photo', 'Date of birth', 'Gender', 'Marital status', 'Address (city/state only)', 'References'],
            tips: [
                'Quantify everything (increased X by 25%)',
                'Use action verbs',
                'ATS-friendly format',
                'Tailor for each job',
                'Include visa status briefly'
            ]
        },

        top_hiring_companies: {
            faang: ['Google', 'Meta', 'Apple', 'Amazon', 'Netflix', 'Microsoft'],
            big_tech: ['Salesforce', 'Adobe', 'Oracle', 'Uber', 'Airbnb', 'LinkedIn', 'Stripe', 'Coinbase'],
            unicorns: ['Figma', 'Notion', 'Databricks', 'Plaid', 'Rippling', 'Ramp'],
            consulting: ['Deloitte', 'Accenture', 'McKinsey', 'BCG', 'Bain'],
            finance: ['Goldman Sachs', 'JP Morgan', 'Morgan Stanley', 'Citadel', 'Two Sigma'],
            h1b_sponsors: ['Cognizant', 'Infosys', 'TCS', 'Wipro', 'Tech Mahindra', 'HCL']
        },

        salaries: {
            'Junior Developer (0-2y)': {usd: '$80,000-120,000', inr: '₹66-100 LPA'},
            'Mid Developer (3-5y)': {usd: '$130,000-180,000', inr: '₹108-150 LPA'},
            'Senior Developer (5-8y)': {usd: '$180,000-250,000', inr: '₹150-208 LPA'},
            'Staff Engineer (8-12y)': {usd: '$250,000-350,000', inr: '₹208-290 LPA'},
            'Principal/Architect': {usd: '$300,000-450,000', inr: '₹250-374 LPA'},
            'Engineering Manager': {usd: '$200,000-300,000', inr: '₹166-250 LPA'},
            'Director': {usd: '$300,000-500,000', inr: '₹250-415 LPA'},
            'note': 'FAANG pays 20-50% above these numbers'
        },

        monthly_expenses: {
            bay_area: {
                rent: '$2,500-4,500 (₹2,08,000-3,74,000)',
                food: '$600-1,000 (₹50,000-83,000)',
                transport: '$200-500 (₹17,000-42,000)',
                utilities: '$150-300 (₹12,500-25,000)',
                health: '$200-500 (₹17,000-42,000)',
                total: '$4,000-7,000 (₹3,32,000-5,81,000)'
            },
            other_cities: {
                rent: '$1,500-2,500 (₹1,25,000-2,08,000)',
                food: '$400-700',
                transport: '$150-400',
                total: '$2,500-4,500'
            }
        },

        initial_setup_cost: {
            visa_fees: '$700-1,000 (₹58,000-83,000)',
            flight: '₹70,000-1,20,000',
            first_month: '$5,000-10,000',
            security_deposit: '$3,000-6,000',
            car_if_needed: '$3,000-10,000',
            total: '₹15,00,000-30,00,000'
        },

        visa_types: [
            {name: 'H1B', duration: '3+3 years', requirements: ['Bachelor\'s degree', 'Job offer', 'Lottery selection'], path_to_pr: 'EB2/EB3 (10-15 years for Indians)'},
            {name: 'L1A/L1B', duration: '5-7 years', requirements: ['1 year with company abroad', 'Transfer to US office'], path_to_pr: 'EB1C for L1A (faster)'},
            {name: 'O1', duration: '3 years', requirements: ['Extraordinary ability', 'Awards/publications'], path_to_pr: 'EB1A (fastest for Indians)'}
        ],

        green_card_wait: {
            eb2_india: '10-15 years',
            eb3_india: '8-12 years',
            eb1: '1-2 years (if eligible)',
            note: 'India has massive backlog due to per-country limits'
        },

        pros: [
            'Highest tech salaries globally',
            'Best career growth',
            'Silicon Valley ecosystem',
            'Top universities',
            'Strong Indian community',
            'English speaking',
            'Innovation hub',
            'World-class companies'
        ],

        cons: [
            'H1B lottery is uncertain',
            'Green Card wait is 10-15 years',
            'Very expensive (Bay Area)',
            'Healthcare expensive if uninsured',
            'Visa tied to employer',
            'Far from India',
            'Gun violence concerns',
            'Work culture can be intense'
        ],

        best_cities: [
            {name: 'San Francisco Bay Area', why: 'Silicon Valley, highest salaries, most expensive'},
            {name: 'Seattle', why: 'Amazon, Microsoft HQ, no state income tax'},
            {name: 'New York', why: 'Finance + Tech, diverse, expensive'},
            {name: 'Austin', why: 'Growing tech hub, no state income tax, cheaper'},
            {name: 'Boston', why: 'Biotech, startups, universities'}
        ]
    },

    // ==================== UK ====================
    UK: {
        basic_info: {
            official_name: 'United Kingdom',
            capital: 'London',
            tech_hubs: 'London, Manchester, Cambridge, Edinburgh',
            currency: 'GBP (Pound Sterling)',
            exchange_rate: '1 GBP ≈ ₹105',
            timezone: 'GMT/GMT+1 (4.5-5.5hrs behind IST)',
            flight_time: '9-10 hours from India',
            language: 'English',
            indian_population: '1.8 Million+ (largest ethnic minority)',
            visa_processing: '3-8 weeks',
            visa_cost: '£719 (₹75,000) for Skilled Worker',
            tax_rate: '20-45% Progressive'
        },

        why_indians_migrate: [
            'English speaking - no language barrier',
            'Clear PR pathway (5 years)',
            'NHS - Free healthcare',
            'Historical ties with India',
            'Large Indian community',
            'Strong tech scene (London)',
            'Good work-life balance',
            'Excellent education',
            'Youth Mobility Scheme available',
            'Post-Brexit immigration is points-based'
        ],

        step_by_step_migration: [
            {step: 1, title: 'Get Job Offer', details: 'From licensed sponsor. Check register on gov.uk. Salary must meet threshold.', duration: '1-3 months'},
            {step: 2, title: 'Certificate of Sponsorship', details: 'Employer issues CoS. Contains unique reference for visa.', duration: '1-2 weeks'},
            {step: 3, title: 'Apply for Visa', details: 'Apply online at gov.uk. Pay IHS (£1,035/year). Submit biometrics at VFS.', duration: '3-8 weeks'},
            {step: 4, title: 'Travel to UK', details: 'BRP (Biometric Residence Permit) collected at post office.', duration: '1 day'},
            {step: 5, title: 'NI Number', details: 'National Insurance number - apply by phone or online.', duration: '2-8 weeks'},
            {step: 6, title: 'Bank Account', details: 'Monzo, Starling, or traditional banks. Need proof of address.', duration: '1 day to 2 weeks'},
            {step: 7, title: 'GP Registration', details: 'Register with local GP for NHS services.', duration: '1 week'},
            {step: 8, title: 'Find Housing', details: 'Rightmove, Zoopla, SpareRoom. Need employer reference.', duration: '2-4 weeks'}
        ],

        essential_apps: {
            government: ['NHS App', 'HMRC', 'gov.uk Verify', 'BRP App'],
            banking: ['Monzo', 'Starling', 'Revolut', 'Barclays', 'Lloyds', 'HSBC'],
            transport: ['Citymapper', 'TfL Oyster', 'Trainline', 'Uber UK'],
            food_grocery: ['Deliveroo', 'UberEats', 'JustEat', 'Tesco', 'Sainsbury\'s', 'Ocado'],
            housing: ['Rightmove', 'Zoopla', 'SpareRoom', 'OpenRent']
        },

        sim_cards: {
            providers: [
                {name: 'EE', monthly: '£15-40', note: 'Best coverage'},
                {name: 'Three', monthly: '£10-35', note: 'Good data plans'},
                {name: 'Vodafone', monthly: '£12-40', note: 'Good coverage'},
                {name: 'O2', monthly: '£12-35', note: 'Good coverage'},
                {name: 'Giffgaff', monthly: '£6-20', note: 'Budget, no contract'}
            ]
        },

        cv_format: {
            style: 'UK CV format',
            length: '2 pages',
            photo: 'Generally NOT included',
            must_include: ['Personal statement', 'Key skills', 'Work experience (reverse chronological)', 'Education', 'Right to work status'],
            tips: ['British English spelling', 'Mention visa type', 'Include UK references if available']
        },

        top_hiring_companies: {
            tech: ['Google', 'Amazon', 'Meta', 'Microsoft', 'Apple', 'Spotify', 'Monzo', 'Revolut'],
            fintech: ['Wise', 'Checkout.com', 'GoCardless', 'Starling', 'OakNorth'],
            banks: ['Barclays', 'HSBC', 'Lloyds', 'Goldman Sachs', 'JP Morgan'],
            consulting: ['Deloitte', 'PwC', 'KPMG', 'EY', 'Accenture', 'McKinsey']
        },

        salaries: {
            'Junior Developer (0-2y)': {gbp: '£35,000-50,000', inr: '₹37-53 LPA'},
            'Mid Developer (3-5y)': {gbp: '£55,000-75,000', inr: '₹58-79 LPA'},
            'Senior Developer (5-8y)': {gbp: '£75,000-100,000', inr: '₹79-105 LPA'},
            'Tech Lead (8-12y)': {gbp: '£95,000-130,000', inr: '₹100-137 LPA'},
            'Architect': {gbp: '£110,000-150,000', inr: '₹116-158 LPA'},
            'Engineering Manager': {gbp: '£100,000-140,000', inr: '₹105-147 LPA'}
        },

        monthly_expenses: {
            london: {
                rent: '£1,400-2,500 (₹1,47,000-2,63,000)',
                food: '£300-500 (₹31,500-52,500)',
                transport: '£150-250 (₹15,750-26,250)',
                council_tax: '£100-200 (₹10,500-21,000)',
                total: '£2,200-4,000 (₹2,31,000-4,20,000)'
            }
        },

        initial_setup_cost: {
            visa_fees: '£719 + IHS £1,035/year (₹1,85,000 for 3 years)',
            flight: '₹40,000-70,000',
            first_month_rent: '£2,000-3,000',
            deposit: '£2,000-4,000 (5-6 weeks rent)',
            total: '₹8,00,000-12,00,000'
        },

        pr_citizenship_path: {
            pr: '5 years on Skilled Worker visa = ILR (Indefinite Leave)',
            citizenship: '1 year after ILR = Can apply for British citizenship',
            total_time: '6 years to citizenship',
            dual_citizenship: 'Allowed - No need to renounce Indian passport'
        },

        pros: [
            'English speaking',
            '5 years to PR, 6 to citizenship',
            'Dual citizenship allowed',
            'NHS free healthcare',
            'Large Indian community',
            'Good work-life balance',
            'Strong labor laws',
            '28 days paid leave minimum'
        ],

        cons: [
            'High cost of living (London)',
            'Gloomy weather',
            'High taxes (40%+ effective)',
            'IHS fee is expensive',
            'Housing crisis',
            'Brexit uncertainties',
            'NHS wait times',
            'Lower salaries than US'
        ],

        best_cities: [
            {name: 'London', why: 'Most tech jobs, highest salaries, most expensive'},
            {name: 'Manchester', why: 'Growing tech hub, affordable, BBC, startups'},
            {name: 'Cambridge', why: 'Tech hub, ARM, universities, expensive'},
            {name: 'Edinburgh', why: 'Beautiful, growing fintech, cheaper'},
            {name: 'Birmingham', why: 'Affordable, growing tech scene'}
        ]
    },

    // ==================== AUSTRALIA ====================
    Australia: {
        basic_info: {
            official_name: 'Commonwealth of Australia',
            capital: 'Canberra',
            tech_hubs: 'Sydney, Melbourne, Brisbane',
            currency: 'AUD (Australian Dollar)',
            exchange_rate: '1 AUD ≈ ₹55',
            timezone: 'GMT+8 to GMT+11 (varies by state)',
            flight_time: '10-12 hours from India',
            language: 'English',
            indian_population: '900,000+ (fastest growing migrant group)',
            visa_processing: '3-12 months',
            visa_cost: 'AUD 4,640 (₹2,55,000) for skilled PR',
            tax_rate: '19-45% Progressive'
        },

        why_indians_migrate: [
            'Clear PR pathway (SkillSelect)',
            'High quality of life',
            'English speaking',
            'Similar timezone to India',
            'Excellent weather',
            'Multicultural society',
            'Strong economy',
            'Medicare - good healthcare',
            'Beautiful nature',
            'Growing tech sector'
        ],

        step_by_step_migration: [
            {step: 1, title: 'Skills Assessment', details: 'Get skills assessed by ACS (for IT). Takes 8-12 weeks.', duration: '2-3 months'},
            {step: 2, title: 'IELTS/PTE', details: 'Get 8+ in each band for maximum points.', duration: '2-3 months prep'},
            {step: 3, title: 'Submit EOI', details: 'Expression of Interest in SkillSelect. Calculate points.', duration: '1 day'},
            {step: 4, title: 'Wait for Invite', details: 'Need 65+ points for 189, 190 state nomination adds 5-15.', duration: '1-12 months'},
            {step: 5, title: 'Submit PR Application', details: 'After invitation, submit full application with docs.', duration: '3-12 months processing'},
            {step: 6, title: 'Medical & PCC', details: 'Health check and police clearance.', duration: '1-2 weeks'},
            {step: 7, title: 'PR Grant', details: 'Initial Entry Date given - must land before.', duration: '1 day'},
            {step: 8, title: 'Land in Australia', details: 'Complete landing, apply for Medicare, TFN.', duration: '1 day'},
            {step: 9, title: 'TFN & Bank Account', details: 'Tax File Number essential. Open CommBank, NAB, etc.', duration: '1 week'}
        ],

        essential_apps: {
            government: ['myGov', 'Medicare', 'myTax', 'Centrelink'],
            banking: ['CommBank', 'NAB', 'Westpac', 'ANZ', 'Up Bank'],
            transport: ['Opal (Sydney)', 'myki (Melbourne)', 'Uber', 'Ola Australia'],
            jobs: ['Seek', 'Indeed', 'LinkedIn', 'Jora'],
            housing: ['Domain', 'Realestate.com.au', 'Flatmates.com.au']
        },

        sim_cards: {
            providers: [
                {name: 'Telstra', monthly: 'AUD 55-90', note: 'Best coverage'},
                {name: 'Optus', monthly: 'AUD 35-70', note: 'Good value'},
                {name: 'Vodafone', monthly: 'AUD 30-60', note: 'Budget friendly'},
                {name: 'Amaysim', monthly: 'AUD 20-40', note: 'Prepaid'}
            ]
        },

        top_hiring_companies: {
            tech: ['Atlassian', 'Canva', 'Google', 'Amazon', 'Microsoft', 'Salesforce'],
            aussie_tech: ['Atlassian', 'Canva', 'Afterpay', 'SafetyCulture', 'Employment Hero'],
            banks: ['CommBank', 'NAB', 'Westpac', 'ANZ', 'Macquarie'],
            consulting: ['Deloitte', 'PwC', 'KPMG', 'EY', 'Accenture']
        },

        salaries: {
            'Junior Developer (0-2y)': {aud: 'AUD 70,000-90,000', inr: '₹38-50 LPA'},
            'Mid Developer (3-5y)': {aud: 'AUD 100,000-130,000', inr: '₹55-71 LPA'},
            'Senior Developer (5-8y)': {aud: 'AUD 140,000-180,000', inr: '₹77-99 LPA'},
            'Tech Lead (8-12y)': {aud: 'AUD 170,000-220,000', inr: '₹94-121 LPA'},
            'Architect': {aud: 'AUD 200,000-260,000', inr: '₹110-143 LPA'}
        },

        monthly_expenses: {
            sydney: {
                rent: 'AUD 2,000-3,500 (₹1,10,000-1,93,000)',
                food: 'AUD 500-800 (₹27,500-44,000)',
                transport: 'AUD 150-250 (₹8,250-13,750)',
                utilities: 'AUD 150-250 (₹8,250-13,750)',
                total: 'AUD 3,000-5,000 (₹1,65,000-2,75,000)'
            }
        },

        pr_citizenship_path: {
            pr: 'Skilled Independent (189): Direct PR | Skilled Nominated (190): State sponsorship',
            citizenship: '4 years PR = Can apply (1 year as PR minimum)',
            points_needed: '65 minimum, competitive: 80-90',
            dual_citizenship: 'Allowed with India'
        },

        pros: [
            'Clear PR pathway',
            'High quality of life',
            'Great weather',
            'English speaking',
            'Multicultural',
            'Dual citizenship allowed',
            'Medicare healthcare',
            'Similar timezone to India',
            'Strong economy'
        ],

        cons: [
            'Very expensive cities',
            'Far from India (flight)',
            'Competitive PR points',
            'High taxes',
            'Slow processing times',
            'Skills assessment mandatory',
            'Regional areas for some visas'
        ],

        best_cities: [
            {name: 'Sydney', why: 'Most jobs, highest salaries, most expensive'},
            {name: 'Melbourne', why: 'Liveable, cultural, slightly cheaper'},
            {name: 'Brisbane', why: 'Growing tech hub, affordable, good weather'},
            {name: 'Perth', why: 'Mining tech, affordable, isolated'}
        ]
    },

    // ==================== SINGAPORE ====================
    Singapore: {
        basic_info: {
            official_name: 'Republic of Singapore',
            capital: 'Singapore (city-state)',
            currency: 'SGD (Singapore Dollar)',
            exchange_rate: '1 SGD ≈ ₹62',
            timezone: 'GMT+8 (2.5hrs ahead of IST)',
            flight_time: '5-6 hours from India',
            language: 'English, Mandarin, Malay, Tamil',
            indian_population: '400,000+ (9% of population)',
            visa_processing: '2-4 weeks',
            visa_cost: 'SGD 105 (₹6,500)',
            tax_rate: '0-22% Progressive (very low)'
        },

        why_indians_migrate: [
            'Very low taxes (0-22%)',
            'English speaking',
            'Close to India (5 hours)',
            'Safe, clean city',
            'Strong tech hub (Asia Pacific HQ)',
            'Large Indian community',
            'Excellent infrastructure',
            'High quality of life',
            'PR possible after 2-3 years',
            'Gateway to Asia'
        ],

        step_by_step_migration: [
            {step: 1, title: 'Get Job Offer', details: 'Need employer to sponsor Employment Pass (EP). Min salary SGD 5,000+ for tech.', duration: '1-3 months'},
            {step: 2, title: 'EP Application', details: 'Employer applies via MOM. Self-Assessment Tool (SAT) check.', duration: '2-4 weeks'},
            {step: 3, title: 'Entry Approval', details: 'Get In-Principle Approval (IPA) letter.', duration: '1 week'},
            {step: 4, title: 'Fly to Singapore', details: 'Enter on IPA within 60 days.', duration: '1 day'},
            {step: 5, title: 'Collect EP Card', details: 'Employer schedules appointment at MOM.', duration: '1 week'},
            {step: 6, title: 'Open Bank Account', details: 'DBS, OCBC, UOB. Need EP card and passport.', duration: '1 day'},
            {step: 7, title: 'Get SIM Card', details: 'Singtel, Starhub, M1. Need EP card.', duration: '1 hour'},
            {step: 8, title: 'Find Housing', details: 'PropertyGuru, 99.co. Expect 2 months deposit.', duration: '1-2 weeks'}
        ],

        essential_apps: {
            government: ['Singpass', 'LifeSG', 'TraceTogether', 'MyTransport'],
            banking: ['DBS PayLah', 'OCBC Pay Anyone', 'GrabPay', 'Google Pay'],
            transport: ['Grab', 'Gojek', 'ComfortDelGro', 'SG BusLeh'],
            food: ['GrabFood', 'FoodPanda', 'Deliveroo', 'WhyQ'],
            housing: ['PropertyGuru', '99.co', 'Carousell']
        },

        sim_cards: {
            providers: [
                {name: 'Singtel', monthly: 'SGD 30-80', note: 'Best coverage'},
                {name: 'Starhub', monthly: 'SGD 28-70', note: 'Good plans'},
                {name: 'M1', monthly: 'SGD 25-60', note: 'Budget friendly'},
                {name: 'GOMO/Circles', monthly: 'SGD 20-40', note: 'Digital brands'}
            ]
        },

        top_hiring_companies: {
            tech: ['Google', 'Meta', 'Amazon', 'Microsoft', 'Apple', 'ByteDance'],
            apac_hq: ['Stripe', 'Shopify', 'Zoom', 'Twilio', 'Datadog'],
            local: ['Grab', 'Sea (Shopee)', 'Lazada', 'Carousell', 'PropertyGuru'],
            banks: ['DBS', 'OCBC', 'UOB', 'Standard Chartered', 'Citi'],
            mnc: ['PayPal', 'Visa', 'Mastercard', 'JP Morgan', 'Goldman Sachs']
        },

        salaries: {
            'Junior Developer (0-2y)': {sgd: 'SGD 4,500-6,500/mo', inr: '₹33-48 LPA'},
            'Mid Developer (3-5y)': {sgd: 'SGD 7,000-10,000/mo', inr: '₹52-74 LPA'},
            'Senior Developer (5-8y)': {sgd: 'SGD 10,000-15,000/mo', inr: '₹74-111 LPA'},
            'Tech Lead (8-12y)': {sgd: 'SGD 14,000-20,000/mo', inr: '₹104-148 LPA'},
            'Architect': {sgd: 'SGD 18,000-25,000/mo', inr: '₹133-185 LPA'}
        },

        monthly_expenses: {
            single: {
                rent: 'SGD 1,200-2,500 (₹74,400-1,55,000) - Room',
                food: 'SGD 500-800 (₹31,000-50,000)',
                transport: 'SGD 100-200 (₹6,200-12,400)',
                utilities: 'Included in rent usually',
                total: 'SGD 2,000-4,000 (₹1,24,000-2,48,000)'
            }
        },

        initial_setup_cost: {
            ep_fees: 'SGD 105 (₹6,500)',
            flight: '₹15,000-30,000',
            first_month: 'SGD 3,000-5,000',
            deposit: 'SGD 2,400-5,000 (2 months rent)',
            total: '₹5,00,000-8,00,000'
        },

        pr_citizenship_path: {
            pr: 'Apply after 6 months on EP (2-3 years realistic)',
            citizenship: '2 years after PR',
            note: 'PR approval is discretionary - not guaranteed',
            factors: 'Salary, education, time in SG, family ties, age'
        },

        taxes: {
            income_tax: '0% up to 20K, then 2-22%',
            effective_rate: '~15% for most tech salaries',
            no_capital_gains: 'No tax on investments',
            note: 'Much lower than US/UK/Australia'
        },

        pros: [
            'Very low taxes',
            'Close to India (5 hours)',
            'English widely used',
            'Extremely safe',
            'Clean, efficient city',
            'Large Indian community',
            'High salaries',
            'Gateway to APAC opportunities',
            'Excellent infrastructure',
            'Tamil is official language'
        ],

        cons: [
            'Very expensive housing',
            'Small country',
            'Hot and humid year-round',
            'PR not guaranteed',
            'Cost of living high',
            'Competitive job market now',
            'COE for cars expensive',
            'Limited nature/outdoor'
        ],

        weather: {
            year_round: '28-32°C, humid',
            rain: 'Frequent short showers',
            note: 'No seasons - tropical climate'
        },

        tips: [
            'Singpass is essential - get it ASAP',
            'Share apartment initially',
            'Hawker centers for cheap food',
            'MRT is excellent - no need for car',
            'Network in Indian tech community',
            'Apply PR after 2 years for best chances'
        ]
    }
};

// Export
if (typeof window !== 'undefined') {
    window.ENHANCED_COUNTRY_DATA_2 = ENHANCED_COUNTRY_DATA_2;
}


