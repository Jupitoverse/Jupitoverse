// Enhanced Country Migration Data - Part 1 (Gulf Countries + Europe)
// Complete migration guide for Indian IT Professionals
// Last Updated: January 2025

const ENHANCED_COUNTRY_DATA_1 = {

    // ==================== UAE / DUBAI (MOST DETAILED) ====================
    UAE: {
        basic_info: {
            official_name: 'United Arab Emirates',
            capital: 'Abu Dhabi',
            tech_hub: 'Dubai',
            currency: 'AED (Emirati Dirham)',
            exchange_rate: '1 AED ≈ ₹22.5',
            timezone: 'GMT+4 (1.5hrs ahead of IST)',
            flight_time: '3-4 hours from Mumbai/Delhi',
            language: 'Arabic (Official), English (Business)',
            indian_population: '3.5 Million+ (35% of total population)',
            total_it_professionals: '500,000+ Indians in IT sector',
            visa_processing: '2-4 weeks',
            visa_cost: '₹15,000-30,000',
            tax_rate: '0% Income Tax'
        },

        why_indians_migrate: [
            '0% Income Tax - Take home 100% salary',
            'Only 3-4 hours from India',
            'Massive Indian community (35% population)',
            'High demand for IT professionals',
            'Tax-free remittances to India',
            'Modern lifestyle and infrastructure',
            'English widely spoken at workplace',
            'Easy to visit family frequently',
            'Indian food, culture everywhere',
            'Golden Visa for long-term stay'
        ],

        step_by_step_migration: [
            {step: 1, title: 'Get a Job Offer', details: 'Apply through LinkedIn, Indeed, GulfTalent, Bayt. Most companies require candidates to have offer before visa.', duration: '1-3 months'},
            {step: 2, title: 'Document Attestation', details: 'Get degree certificates attested from MEA (India) and UAE Embassy. Cost: ₹3,000-8,000', duration: '2-4 weeks'},
            {step: 3, title: 'Entry Permit', details: 'Employer applies for entry permit. You receive it via email.', duration: '1 week'},
            {step: 4, title: 'Travel to UAE', details: 'Enter UAE on entry permit within 60 days.', duration: '1 day'},
            {step: 5, title: 'Medical Test', details: 'Complete medical test at approved center (SEHA). Cost: AED 250-350', duration: '1-2 days'},
            {step: 6, title: 'Emirates ID', details: 'Apply for Emirates ID at typing center. Biometric capture required.', duration: '2-3 days'},
            {step: 7, title: 'Visa Stamping', details: 'Passport submitted for visa stamping. Get residency visa.', duration: '3-5 days'},
            {step: 8, title: 'Bank Account', details: 'Open salary account with Emirates NBD, ADCB, or Mashreq.', duration: '1 day'},
            {step: 9, title: 'Get SIM Card', details: 'Etisalat or Du - need Emirates ID and passport copy.', duration: '1 hour'},
            {step: 10, title: 'Find Housing', details: 'Use Dubizzle, Bayut, Property Finder. Negotiate rent and cheques.', duration: '1-2 weeks'}
        ],

        essential_apps: {
            government: ['UAE Pass (Digital ID)', 'MOHRE (Labor Ministry)', 'ICA Smart (Immigration)', 'Dubai Now (City Services)'],
            banking: ['Emirates NBD', 'ADCB Mobile', 'Mashreq Neo', 'FAB Mobile'],
            transport: ['RTA Dubai (Metro/Bus)', 'Careem', 'Uber UAE', 'Salik (Toll)'],
            food_grocery: ['Talabat', 'Deliveroo', 'Noon Food', 'Instashop', 'Lulu Online'],
            housing: ['Dubizzle', 'Bayut', 'Property Finder', 'JustProperty'],
            social: ['WhatsApp (widely used)', 'BOTIM (VoIP calls)', 'Teams/Zoom'],
            shopping: ['Noon', 'Amazon.ae', 'Namshi', 'Carrefour'],
            utility: ['DEWA (Electricity)', 'Etisalat App', 'Du App', 'ENBD Pay']
        },

        essential_websites: {
            job_portals: ['linkedin.com/jobs', 'indeed.ae', 'gulftalent.com', 'bayt.com', 'naukrigulf.com', 'monster.com.ae'],
            government: ['mohre.gov.ae', 'u.ae', 'icp.gov.ae', 'med.gov.ae'],
            housing: ['dubizzle.com', 'bayut.com', 'propertyfinder.ae'],
            community: ['expatwoman.com', 'dubai-online.com', 'reddit.com/r/dubai'],
            news: ['khaleejtimes.com', 'gulfnews.com']
        },

        sim_cards: {
            providers: [
                {name: 'Etisalat', monthly: 'AED 75-200', note: 'Largest network, best coverage'},
                {name: 'Du', monthly: 'AED 65-175', note: 'Competitive pricing, good deals'},
                {name: 'Virgin Mobile UAE', monthly: 'AED 50-150', note: 'Budget friendly, app-based'}
            ],
            requirements: ['Passport copy', 'Emirates ID (or entry permit initially)', 'Address proof'],
            tip: 'Get postpaid once you have Emirates ID - better plans and coverage'
        },

        cv_format: {
            style: 'Europass or Modern format',
            length: '2 pages maximum',
            photo: 'Required - Professional headshot',
            must_include: ['Full name and nationality', 'UAE contact number (if available)', 'LinkedIn URL', 'Visa status (if already in UAE)', 'Notice period'],
            avoid: ['Date of birth (optional)', 'Religion', 'Marital status', 'Salary expectations in CV'],
            tips: [
                'Use ATS-friendly format',
                'Highlight international experience',
                'Mention GCC experience if any',
                'Include technology stack prominently',
                'Add certifications (AWS, Azure, etc.)'
            ]
        },

        top_hiring_companies: {
            tech_giants: ['Microsoft', 'Google', 'Amazon AWS', 'Meta', 'Oracle', 'SAP'],
            mnc_it: ['Accenture', 'IBM', 'TCS', 'Infosys', 'Wipro', 'Cognizant', 'Capgemini', 'DXC'],
            banks: ['Emirates NBD', 'FAB', 'ADCB', 'Mashreq', 'DIB', 'Standard Chartered'],
            telecom: ['Etisalat', 'Du', 'e& Group'],
            startups: ['Careem', 'Noon', 'Fetchr', 'Property Finder', 'Dubizzle'],
            government: ['Dubai Municipality', 'DEWA', 'Dubai Police', 'RTA'],
            free_zones: ['DIFC', 'Dubai Internet City', 'Dubai Silicon Oasis', 'DMCC', 'Jebel Ali']
        },

        salaries: {
            'Junior Developer (0-2y)': {aed: 'AED 8,000-15,000/mo', inr: '₹8-15 LPA'},
            'Mid Developer (3-5y)': {aed: 'AED 15,000-25,000/mo', inr: '₹15-25 LPA'},
            'Senior Developer (5-8y)': {aed: 'AED 25,000-40,000/mo', inr: '₹25-40 LPA'},
            'Tech Lead (8-12y)': {aed: 'AED 35,000-55,000/mo', inr: '₹35-55 LPA'},
            'Architect (10+y)': {aed: 'AED 45,000-70,000/mo', inr: '₹45-70 LPA'},
            'Engineering Manager': {aed: 'AED 40,000-65,000/mo', inr: '₹40-65 LPA'},
            'Director/VP': {aed: 'AED 60,000-1,00,000/mo', inr: '₹60-100 LPA'}
        },

        in_demand_skills: ['Python', 'Java', 'Cloud (AWS/Azure/GCP)', 'DevOps', 'React/Angular', 'Data Engineering', 'AI/ML', 'Cybersecurity', 'SAP', 'Salesforce', 'Mobile Development'],

        monthly_expenses: {
            single: {
                rent: '₹60,000-1,20,000 (Sharing: ₹25,000-40,000)',
                food: '₹15,000-25,000',
                transport: '₹8,000-15,000',
                utilities: '₹5,000-10,000',
                phone_internet: '₹3,000-5,000',
                entertainment: '₹10,000-20,000',
                total: '₹1,00,000-2,00,000'
            },
            family: {
                rent: '₹1,20,000-2,50,000',
                food: '₹30,000-50,000',
                transport: '₹15,000-25,000',
                utilities: '₹10,000-15,000',
                school_fees: '₹40,000-1,50,000',
                total: '₹2,50,000-5,00,000'
            }
        },

        initial_setup_cost: {
            visa_medical: '₹20,000-35,000',
            flight_one_way: '₹15,000-30,000',
            first_month_rent: '₹60,000-1,50,000',
            security_deposit: '₹60,000-1,50,000 (1 month)',
            furniture_basics: '₹50,000-1,50,000',
            emergency_fund: '₹1,00,000',
            total_single: '₹3,00,000-6,00,000',
            total_family: '₹6,00,000-12,00,000'
        },

        savings_potential: {
            junior: '₹3-5 LPA (40-50% savings)',
            mid: '₹8-12 LPA (50-55% savings)',
            senior: '₹15-25 LPA (55-60% savings)',
            lead: '₹25-40 LPA (60-65% savings)',
            note: '0% tax means significantly higher take-home than countries with 30-40% tax'
        },

        visa_types: [
            {name: 'Employment Visa', duration: '2-3 years', requirements: ['Job offer', 'Medical test', 'Employer sponsorship'], path_to_pr: 'No direct PR'},
            {name: 'Golden Visa', duration: '5-10 years', requirements: ['₹2.5 Cr+ income OR Specialized talent OR Investors'], path_to_pr: 'Long-term residency'},
            {name: 'Green Visa', duration: '5 years', requirements: ['Self-sponsored, skilled workers'], path_to_pr: 'Freelance work allowed'},
            {name: 'Freelance Visa', duration: '1-3 years', requirements: ['Freelancer permit from free zone'], path_to_pr: 'Work independently'}
        ],

        housing_tips: [
            'Negotiate - everything is negotiable in Dubai',
            'Ask for multiple cheques (4-12) instead of 1-2',
            'Check DEWA connection before signing',
            'Studios in Deira/Bur Dubai are cheapest',
            'Marina, JLT, Sports City popular for IT professionals',
            'Use Dubizzle for direct landlord listings',
            'Avoid agents with high commission (5%+)',
            'Check commute time to office before finalizing'
        ],

        agencies_recruiters: [
            {name: 'Robert Half', type: 'Premium', website: 'roberthalf.ae'},
            {name: 'Michael Page', type: 'Premium', website: 'michaelpage.ae'},
            {name: 'Hays', type: 'Premium', website: 'hays.ae'},
            {name: 'BAC Middle East', type: 'Mid-level', website: 'bacme.com'},
            {name: 'Charterhouse', type: 'All levels', website: 'charterhouse.ae'},
            {name: 'Adecco', type: 'All levels', website: 'adecco.ae'}
        ],

        interview_process: [
            'Phone screening (30 min)',
            'Technical assessment (online)',
            'Technical interview (1-2 rounds)',
            'HR interview',
            'Offer negotiation'
        ],

        email_templates: {
            job_application: `Subject: Application for [Position] - [Your Name] - [X] Years Experience

Dear Hiring Manager,

I am writing to express my interest in the [Position] role at [Company]. With [X] years of experience in [Technologies], I am confident I would be a valuable addition to your team.

Key highlights:
• [Achievement 1]
• [Achievement 2]
• [Relevant skill/certification]

I am currently based in India and ready to relocate to UAE immediately upon offer. I hold valid documents for attestation and can complete visa formalities promptly.

Looking forward to discussing this opportunity.

Best regards,
[Name]
[LinkedIn URL]
[Phone]`,
            
            follow_up: `Subject: Following up - [Position] Application - [Your Name]

Dear [Hiring Manager Name],

I hope this email finds you well. I wanted to follow up on my application for the [Position] role submitted on [Date].

I remain very interested in this opportunity and would welcome the chance to discuss how my experience in [Key Skill] can benefit [Company].

Please let me know if you need any additional information.

Best regards,
[Name]`
        },

        pros: [
            '0% Income Tax - Massive savings',
            '3-4 hours from India - Easy family visits',
            '35% Indian population - Feel at home',
            'English workplace - No language barrier',
            'Golden Visa option for 10 years',
            'Modern infrastructure',
            'Safe for families',
            'Tax-free remittances',
            'Indian food everywhere',
            'Strong career growth'
        ],

        cons: [
            'Expensive housing in prime areas',
            'No citizenship pathway',
            'Hot summers (40-50°C)',
            'Visa tied to employer',
            'Cost of living rising',
            'Traffic congestion',
            'Limited outdoor life in summer',
            'School fees expensive'
        ],

        lifestyle: {
            work_hours: '9 AM - 6 PM (some companies 8-5)',
            weekend: 'Saturday-Sunday (shifted from Friday-Saturday in 2022)',
            dress_code: 'Business casual to formal',
            social: 'Malls, beaches, restaurants, desert safaris',
            indian_community: 'Very active - temples, festivals, cricket clubs, cultural associations',
            food: 'Abundant Indian restaurants from street food to fine dining'
        },

        tips_for_success: [
            'Network actively - LinkedIn is huge here',
            'Learn basic Arabic phrases (not required but appreciated)',
            'Start savings from Day 1 - 0% tax is powerful',
            'Build emergency fund of 3 months expenses',
            'Explore free zones for better benefits',
            'Negotiate housing allowance in package',
            'Join Indian IT professional groups',
            'Consider Dubai vs Abu Dhabi based on role',
            'Upskill continuously - market is competitive'
        ],

        weather: {
            summer: '40-50°C (April-September) - Very hot',
            winter: '15-25°C (October-March) - Pleasant',
            humidity: 'High in coastal areas',
            best_time: 'November to March'
        },

        best_cities: [
            {name: 'Dubai', pop: '3.5M', why: 'Tech hub - DIFC, Internet City, Silicon Oasis. Most IT opportunities.'},
            {name: 'Abu Dhabi', pop: '1.5M', why: 'Government sector, oil companies, slightly lower cost.'},
            {name: 'Sharjah', pop: '1.4M', why: 'Affordable rent, more conservative, commute to Dubai common.'}
        ]
    },

    // ==================== GERMANY (MOST DETAILED) ====================
    Germany: {
        basic_info: {
            official_name: 'Federal Republic of Germany',
            capital: 'Berlin',
            tech_hubs: 'Berlin, Munich, Frankfurt, Hamburg',
            currency: 'EUR (Euro)',
            exchange_rate: '1 EUR ≈ ₹90',
            timezone: 'GMT+1/+2 (3.5-4.5hrs behind IST)',
            flight_time: '8-9 hours from India',
            language: 'German (English in tech)',
            indian_population: '200,000+ (IT professionals: 50,000+)',
            visa_processing: '4-8 weeks',
            visa_cost: '₹6,000-10,000 (€75)',
            tax_rate: '14-45% Progressive'
        },

        why_indians_migrate: [
            'Clear PR pathway - after 21 months!',
            'Free world-class healthcare',
            'Free education for children',
            'Strong tech ecosystem',
            'Work-life balance culture',
            'EU Blue Card - fast track immigration',
            'High quality of life',
            'Safe country',
            'Strong labor laws protecting employees',
            'Path to EU citizenship'
        ],

        step_by_step_migration: [
            {step: 1, title: 'Get Job Offer', details: 'Apply via LinkedIn, StepStone, Indeed Germany. Salary must meet Blue Card threshold (€45,300 for IT).', duration: '2-4 months'},
            {step: 2, title: 'University Degree Recognition', details: 'Get degree recognized via anabin database. Most Indian degrees are recognized.', duration: '1-2 weeks'},
            {step: 3, title: 'Apply for Visa', details: 'Apply at German Embassy/VFS for EU Blue Card. Need job offer, degree, health insurance.', duration: '4-8 weeks'},
            {step: 4, title: 'Fly to Germany', details: 'Arrive in Germany within 90 days of visa issuance.', duration: '1 day'},
            {step: 5, title: 'City Registration (Anmeldung)', details: 'Register address at Bürgeramt within 14 days. Essential for everything.', duration: '1 day'},
            {step: 6, title: 'Open Bank Account', details: 'N26, DKB, or traditional bank. Need passport and registration certificate.', duration: '1-2 days'},
            {step: 7, title: 'Get Health Insurance', details: 'Public (TK, AOK) or Private. Mandatory for visa.', duration: '1 day'},
            {step: 8, title: 'Apply for Blue Card', details: 'At Ausländerbehörde (immigration office). Convert visa to residence permit.', duration: '2-4 weeks'},
            {step: 9, title: 'Get SIM Card', details: 'Telekom, Vodafone, O2 - need passport and German address.', duration: '1 hour'},
            {step: 10, title: 'Find Permanent Housing', details: 'Use Immobilienscout24, WG-Gesucht. Expect to share initially.', duration: '2-4 weeks'}
        ],

        essential_apps: {
            government: ['AusweisApp2 (Digital ID)', 'ELSTER (Tax)', 'Termin Buchen (Appointments)'],
            banking: ['N26', 'DKB', 'Sparkasse', 'ING'],
            transport: ['DB Navigator (Trains)', 'BVG (Berlin)', 'MVV (Munich)', 'Uber/FREE NOW'],
            food_grocery: ['Lieferando', 'Wolt', 'REWE', 'Gorillas', 'Flink'],
            housing: ['Immobilienscout24', 'WG-Gesucht', 'Immowelt', 'eBay Kleinanzeigen'],
            social: ['Meetup', 'Internations', 'LinkedIn', 'Xing'],
            language: ['Duolingo', 'Babbel', 'DW Learn German'],
            utility: ['Clark (Insurance)', 'Check24', 'Meine Stadtwerke']
        },

        essential_websites: {
            job_portals: ['linkedin.com/jobs', 'stepstone.de', 'indeed.de', 'xing.com', 'glassdoor.de', 'honeypot.io', 'germantechjobs.de'],
            government: ['make-it-in-germany.com', 'auswaertiges-amt.de', 'bamf.de'],
            housing: ['immobilienscout24.de', 'wg-gesucht.de', 'immowelt.de'],
            community: ['reddit.com/r/germany', 'toytowngermany.com', 'internations.org'],
            tax: ['lohnsteuer-kompakt.de', 'smartsteuer.de']
        },

        sim_cards: {
            providers: [
                {name: 'Telekom (T-Mobile)', monthly: '€20-40', note: 'Best network coverage'},
                {name: 'Vodafone', monthly: '€15-35', note: 'Good coverage, competitive'},
                {name: 'O2', monthly: '€10-30', note: 'Budget friendly'},
                {name: 'Aldi Talk', monthly: '€8-15', note: 'Prepaid, cheapest option'}
            ],
            requirements: ['Passport', 'German address (Anmeldung)', 'German bank account for postpaid'],
            tip: 'Start with Aldi Talk prepaid, switch to postpaid after settling'
        },

        cv_format: {
            style: 'German CV (Lebenslauf) or Europass',
            length: '1-2 pages maximum',
            photo: 'Required - Professional headshot (this is German standard)',
            must_include: ['Personal details (name, address, DOB)', 'Photo (top right)', 'Education with grades', 'Work experience (detailed)', 'Languages with levels', 'IT skills'],
            avoid: ['Salary expectations', 'References (auf Anfrage)'],
            tips: [
                'German CV format different from US/UK',
                'Include Arbeitszeugnisse (reference letters) from past employers',
                'Highlight German language skills (even A1)',
                'Mention willingness to learn German',
                'Use European date format (DD.MM.YYYY)'
            ]
        },

        top_hiring_companies: {
            tech_giants: ['Google', 'Amazon', 'Microsoft', 'Apple', 'Meta', 'SAP', 'Zalando'],
            german_tech: ['SAP', 'Siemens', 'Bosch', 'Continental', 'Deutsche Telekom', 'Infineon'],
            startups: ['N26', 'Zalando', 'HelloFresh', 'Trade Republic', 'Personio', 'Celonis', 'FlixBus'],
            automotive: ['BMW', 'Mercedes-Benz', 'Volkswagen', 'Audi', 'Porsche', 'Daimler'],
            consulting: ['BCG', 'McKinsey', 'Bain', 'Roland Berger', 'Accenture', 'Deloitte'],
            banks: ['Deutsche Bank', 'Commerzbank', 'DZ Bank', 'ING Germany']
        },

        salaries: {
            'Junior Developer (0-2y)': {eur: '€45,000-55,000/year', inr: '₹40-50 LPA'},
            'Mid Developer (3-5y)': {eur: '€55,000-70,000/year', inr: '₹50-63 LPA'},
            'Senior Developer (5-8y)': {eur: '€70,000-90,000/year', inr: '₹63-81 LPA'},
            'Tech Lead (8-12y)': {eur: '€85,000-110,000/year', inr: '₹76-99 LPA'},
            'Architect (10+y)': {eur: '€100,000-130,000/year', inr: '₹90-117 LPA'},
            'Engineering Manager': {eur: '€95,000-130,000/year', inr: '₹85-117 LPA'}
        },

        taxes_explained: {
            income_tax: '14-45% progressive (42% kicks in at €58k)',
            solidarity_surcharge: '5.5% of income tax (for higher earners)',
            church_tax: '8-9% of income tax (optional - can opt out)',
            social_security: '~20% (pension, health, unemployment, care)',
            net_salary: 'Expect ~55-60% take-home after all deductions',
            note: 'Use brutto-netto-rechner.info to calculate exact take-home'
        },

        monthly_expenses: {
            single: {
                rent: '€800-1,500 (₹72,000-1,35,000)',
                food: '€300-500 (₹27,000-45,000)',
                transport: '€50-100 (₹4,500-9,000)',
                health_insurance: 'Included in salary deduction',
                phone_internet: '€30-50 (₹2,700-4,500)',
                entertainment: '€100-200 (₹9,000-18,000)',
                total: '€1,300-2,500 (₹1,17,000-2,25,000)'
            }
        },

        initial_setup_cost: {
            visa_fees: '€75 (₹6,750)',
            flight_one_way: '₹40,000-70,000',
            blocked_account: '€11,208 (₹10,00,000) - Required for visa',
            first_month_rent: '€1,000-1,500',
            security_deposit: '€2,000-4,500 (3 months cold rent)',
            furniture: '€1,000-3,000',
            total: '₹12,00,000-18,00,000'
        },

        savings_potential: {
            junior: '₹5-10 LPA (20-25% after expenses)',
            mid: '₹12-18 LPA (25-30%)',
            senior: '₹20-30 LPA (30-35%)',
            note: 'Lower than UAE due to taxes but includes healthcare, pension, unemployment insurance'
        },

        visa_types: [
            {name: 'EU Blue Card', duration: '4 years', requirements: ['Job offer €45,300+', 'University degree', 'Health insurance'], path_to_pr: '21 months with B1 German, 33 months otherwise'},
            {name: 'Job Seeker Visa', duration: '6 months', requirements: ['Degree', 'Funds for stay', 'No work allowed'], path_to_pr: 'Find job and convert to Blue Card'},
            {name: 'Work Permit (§18b)', duration: '4 years', requirements: ['Job offer', 'Degree'], path_to_pr: '4 years'}
        ],

        pr_citizenship_path: {
            pr: '21-33 months on Blue Card',
            citizenship: '6-8 years (5 years for spouses of Germans)',
            requirements_pr: ['B1 German', 'Sufficient income', 'Pension contributions', 'No criminal record'],
            requirements_citizenship: ['8 years residence', 'B1 German', 'Livelihood secured', 'Renounce Indian citizenship']
        },

        pros: [
            'Clear PR pathway in 21 months',
            'Free healthcare',
            'Free university education',
            'Strong worker protections',
            '30 days paid vacation',
            'Work-life balance',
            'EU freedom of movement',
            'Path to EU citizenship',
            'Excellent public transport',
            'Safe for families'
        ],

        cons: [
            'High taxes (40%+ effective)',
            'German language needed for daily life',
            'Bureaucracy is slow',
            'Housing crisis in major cities',
            'Cold, gray winters',
            'Cultural adjustment',
            'Lower net salary than UAE/Singapore',
            'Must renounce Indian citizenship for German passport'
        ],

        tips_for_success: [
            'Start learning German NOW (A1 before arrival)',
            'Use Blocked Account (Sperrkonto) for visa',
            'Register address within 14 days (Anmeldung)',
            'Open N26 account online even before arriving',
            'Join German tech Slack/Discord communities',
            'Housing is HARD - start searching early',
            'Learn German workplace culture (direct, punctual)',
            'Use tax advisors (Steuerberater) for filing'
        ],

        weather: {
            summer: '20-30°C (June-August)',
            winter: '-5 to 5°C (December-February) - Cold and gray',
            spring_autumn: '10-20°C - Pleasant',
            note: 'Winter can be depressing - plan for it'
        },

        best_cities: [
            {name: 'Berlin', pop: '3.6M', avg_salary: '€65K', why: 'Startup capital, English-friendly, cheaper rent'},
            {name: 'Munich', pop: '1.5M', avg_salary: '€75K', why: 'Highest salaries, BMW/Siemens, expensive'},
            {name: 'Frankfurt', pop: '750K', avg_salary: '€70K', why: 'Banking hub, central location'},
            {name: 'Hamburg', pop: '1.9M', avg_salary: '€62K', why: 'Port city, startups, good quality of life'}
        ]
    },

    // ==================== CANADA ====================
    Canada: {
        basic_info: {
            official_name: 'Canada',
            capital: 'Ottawa',
            tech_hubs: 'Toronto, Vancouver, Montreal, Calgary',
            currency: 'CAD (Canadian Dollar)',
            exchange_rate: '1 CAD ≈ ₹62',
            timezone: 'GMT-5 to GMT-8 (varies by province)',
            flight_time: '14-18 hours from India',
            language: 'English, French (Quebec)',
            indian_population: '1.8 Million+ (Fastest growing)',
            visa_processing: '3-12 months (varies by program)',
            visa_cost: 'CAD 1,325 (₹82,000) for PR',
            tax_rate: '15-33% Federal + Provincial'
        },

        why_indians_migrate: [
            'Clear PR and Citizenship pathway',
            'Multicultural society - very welcoming',
            'Free healthcare (after PR)',
            'High quality of life',
            'Excellent education for children',
            'Work opportunities for spouse',
            'Express Entry is point-based and fair',
            'Large Indian community',
            'Safe country',
            'OCI allows easy India visits'
        ],

        step_by_step_migration: [
            {step: 1, title: 'Get IELTS Score', details: 'Target CLB 9+ (L8.5, R7, W7, S7). Higher = more points.', duration: '2-3 months prep'},
            {step: 2, title: 'Get ECA (Education Assessment)', details: 'Get degree assessed by WES or other agency.', duration: '4-8 weeks'},
            {step: 3, title: 'Create Express Entry Profile', details: 'Calculate CRS score. Need 470+ for recent draws.', duration: '1 day'},
            {step: 4, title: 'Wait for ITA or Apply PNP', details: 'If CRS < 470, apply Provincial Nominee Program (+600 points).', duration: '1-6 months'},
            {step: 5, title: 'Submit PR Application', details: 'After ITA, submit docs, police clearance, medicals.', duration: '6-12 months processing'},
            {step: 6, title: 'Land in Canada', details: 'Complete landing formalities, get PR card.', duration: '1 day'},
            {step: 7, title: 'Get SIN Number', details: 'Social Insurance Number - needed for work.', duration: '1 day'},
            {step: 8, title: 'Open Bank Account', details: 'TD, RBC, Scotiabank, or online banks.', duration: '1 day'},
            {step: 9, title: 'Get Health Card', details: 'Provincial health card (OHIP in Ontario).', duration: '2-3 months wait'},
            {step: 10, title: 'Start Job Search', details: 'LinkedIn, Indeed, company websites. Network actively.', duration: '1-6 months'}
        ],

        essential_apps: {
            government: ['Canada.ca', 'GCKey', 'IRCC Portal', 'ArriveCAN'],
            banking: ['TD EasyWeb', 'RBC Mobile', 'Scotiabank', 'CIBC', 'Simplii'],
            transport: ['Uber', 'Lyft', 'Transit App', 'TTC (Toronto)', 'TransLink (Vancouver)'],
            food_grocery: ['UberEats', 'DoorDash', 'SkipTheDishes', 'Instacart', 'Walmart'],
            housing: ['Realtor.ca', 'Rentals.ca', 'Kijiji', 'Facebook Marketplace', 'Zumper'],
            jobs: ['LinkedIn', 'Indeed', 'Glassdoor', 'Monster.ca', 'Workopolis']
        },

        sim_cards: {
            providers: [
                {name: 'Rogers', monthly: 'CAD 50-90', note: 'Best coverage'},
                {name: 'Bell', monthly: 'CAD 50-85', note: 'Good network'},
                {name: 'Telus', monthly: 'CAD 45-80', note: 'Competitive'},
                {name: 'Fido/Koodo/Virgin', monthly: 'CAD 35-60', note: 'Budget brands'},
                {name: 'Chatr/Lucky Mobile', monthly: 'CAD 25-45', note: 'Cheapest prepaid'}
            ]
        },

        cv_format: {
            style: 'North American format',
            length: '2 pages',
            photo: 'NOT required (avoid discrimination)',
            must_include: ['Professional summary', 'Skills section', 'Quantified achievements', 'Education', 'Canadian certifications if any'],
            avoid: ['Photo', 'Date of birth', 'Marital status', 'Religion', 'References on CV']
        },

        top_hiring_companies: {
            tech_giants: ['Amazon', 'Microsoft', 'Google', 'Meta', 'Apple', 'Shopify'],
            canadian_tech: ['Shopify', 'Hootsuite', 'Wealthsimple', 'Clio', 'Lightspeed', 'ApplyBoard'],
            banks: ['RBC', 'TD Bank', 'Scotiabank', 'BMO', 'CIBC'],
            consulting: ['Deloitte', 'KPMG', 'PwC', 'EY', 'Accenture'],
            telecom: ['Rogers', 'Bell', 'Telus']
        },

        salaries: {
            'Junior Developer (0-2y)': {cad: 'CAD 55,000-75,000', inr: '₹34-46 LPA'},
            'Mid Developer (3-5y)': {cad: 'CAD 80,000-110,000', inr: '₹50-68 LPA'},
            'Senior Developer (5-8y)': {cad: 'CAD 110,000-150,000', inr: '₹68-93 LPA'},
            'Tech Lead (8-12y)': {cad: 'CAD 140,000-180,000', inr: '₹87-112 LPA'},
            'Staff Engineer': {cad: 'CAD 160,000-220,000', inr: '₹99-136 LPA'}
        },

        monthly_expenses: {
            single: {
                rent: 'CAD 1,500-2,500 (₹93,000-1,55,000)',
                food: 'CAD 400-600 (₹25,000-37,000)',
                transport: 'CAD 100-200 (₹6,200-12,400)',
                phone: 'CAD 50-80 (₹3,100-5,000)',
                utilities: 'CAD 100-200 (₹6,200-12,400)',
                total: 'CAD 2,500-4,000 (₹1,55,000-2,48,000)'
            }
        },

        initial_setup_cost: {
            pr_fees: 'CAD 2,500 (₹1,55,000)',
            flight: '₹60,000-1,00,000',
            settlement_fund_show: 'CAD 13,310 (₹8,25,000) - Must show',
            first_month: 'CAD 4,000-6,000',
            total: '₹15,00,000-20,00,000'
        },

        pr_citizenship_path: {
            pr: 'Express Entry: 6-12 months | PNP: 12-18 months',
            citizenship: '3 years as PR (1,095 days in 5 years)',
            express_entry_points: 'Need CRS 470+ (varies)',
            pnp_advantage: '+600 points guaranteed'
        },

        pros: [
            'Clear PR and Citizenship path',
            'Multicultural, welcoming society',
            'Free healthcare after PR',
            'Excellent education',
            'Safe, clean environment',
            'Large Indian community',
            'No need to renounce Indian citizenship (OCI)',
            'Spouse can work',
            'Express Entry is transparent'
        ],

        cons: [
            'Extreme winters (-20 to -40°C)',
            'High cost of living',
            'Housing crisis in Toronto/Vancouver',
            'Healthcare wait times',
            'Far from India (15+ hours)',
            'Initial job search can be tough',
            '"Canadian experience" barrier',
            'High taxes (40%+ effective)'
        ],

        weather: {
            summer: '20-30°C (short, June-August)',
            winter: '-10 to -40°C (long, November-March)',
            note: 'First winter is challenging - prepare well'
        },

        best_cities: [
            {name: 'Toronto', pop: '6.2M', why: 'Most jobs, diverse, expensive'},
            {name: 'Vancouver', pop: '2.5M', why: 'Mild weather, beautiful, expensive'},
            {name: 'Montreal', pop: '4.1M', why: 'Affordable, need French for some jobs'},
            {name: 'Calgary', pop: '1.4M', why: 'Oil/Gas, growing tech, affordable'},
            {name: 'Ottawa', pop: '1M', why: 'Government jobs, balanced'}
        ]
    }
};

// Export
if (typeof window !== 'undefined') {
    window.ENHANCED_COUNTRY_DATA_1 = ENHANCED_COUNTRY_DATA_1;
}


