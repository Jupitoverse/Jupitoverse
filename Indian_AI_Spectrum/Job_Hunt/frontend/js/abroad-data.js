// Comprehensive Country Data for Indian IT Professionals Migrating Abroad
// Last Updated: January 2025

const COMPREHENSIVE_COUNTRY_DATA = {

    // ==================== UAE / DUBAI ====================
    UAE: {
        visa_processing: '2-4 weeks',
        visa_cost: '₹15,000-30,000',
        tax_rate: '0% Income Tax',
        language: 'Arabic (English widely used)',
        weather: 'Desert climate - Hot summers (40-50°C), mild winters (15-25°C)',
        indian_population: '3.5 Million+',
        currency: 'AED (1 AED ≈ ₹22.5)',
        timezone: 'GMT+4 (1.5hrs ahead of IST)',
        flight_time: '3-4 hours from major Indian cities',
        
        pros: [
            '0% Income Tax - Keep 100% of your salary',
            'Very close to India - 3hr flight, easy to visit family',
            'Large Indian community (35% of Dubai population)',
            'Tax-free savings - Build wealth faster',
            'Modern infrastructure and lifestyle',
            'Golden Visa (10-year) for skilled professionals',
            'No restrictions on sending money to India',
            'High demand for IT professionals',
            'English widely spoken in workplace',
            'Indian food, culture readily available'
        ],
        cons: [
            'Expensive housing in prime areas',
            'No permanent residency (visa tied to employment)',
            'Hot weather for 6-7 months',
            'Alcohol restrictions and cultural norms',
            'Limited workers rights compared to Western countries',
            'Healthcare can be expensive without employer coverage',
            'Job security depends on visa status',
            'Limited outdoor activities in summer'
        ],
        
        best_cities: [
            {name: 'Dubai', why: 'Tech hub, DIFC, Internet City - Most opportunities'},
            {name: 'Abu Dhabi', why: 'Government jobs, more relaxed pace'},
            {name: 'Sharjah', why: 'Cheaper housing, conservative culture'}
        ],
        
        lifestyle: {
            work_hours: '9 AM - 6 PM (Sunday-Thursday typically)',
            weekend: 'Friday-Saturday (changed from Friday-Saturday to Saturday-Sunday in some companies)',
            dress_code: 'Business casual, modest dressing appreciated',
            social_life: 'Active expat community, malls, beaches, restaurants',
            indian_community: 'Very strong - temples, cultural events, cricket clubs',
            food: 'Abundant Indian restaurants, grocery stores with Indian products'
        },
        
        expenses: {
            rent: {s: '₹60,000-1,20,000', f: '₹1,00,000-2,00,000'},
            food: {s: '₹20,000-30,000', f: '₹35,000-50,000'},
            transport: {s: '₹15,000-25,000', f: '₹20,000-35,000'},
            utilities: {s: '₹8,000-15,000', f: '₹12,000-20,000'},
            healthcare: {s: '₹3,000-8,000', f: '₹8,000-15,000'},
            entertainment: {s: '₹15,000-25,000', f: '₹25,000-40,000'},
            total: {s: '₹1,20,000-2,20,000', f: '₹2,00,000-3,60,000'}
        },
        
        initial: {
            visa: '₹15,000-30,000',
            flight: '₹15,000-30,000',
            deposit: '₹2,00,000-4,00,000 (2-3 months rent)',
            furniture: '₹50,000-1,50,000',
            emergency: '₹1,00,000',
            total: '₹4,00,000-7,00,000'
        },
        
        salaries: {
            'Junior Developer (0-2y)': '₹8-12 LPA (AED 35-50K)',
            'Mid Developer (3-5y)': '₹15-25 LPA (AED 65-110K)',
            'Senior Developer (5-8y)': '₹25-40 LPA (AED 110-175K)',
            'Tech Lead (8-12y)': '₹35-55 LPA (AED 150-240K)',
            'Architect/Principal (12+y)': '₹50-80 LPA (AED 220-350K)',
            'Engineering Manager': '₹45-70 LPA (AED 200-300K)'
        },
        
        savings_potential: {
            junior: '₹4-6 LPA (50% savings)',
            mid: '₹8-12 LPA (50-55% savings)',
            senior: '₹15-25 LPA (55-60% savings)',
            lead: '₹25-35 LPA (60% savings)'
        },
        
        taxes: {
            income_tax: '0%',
            vat: '5% on goods/services',
            property_tax: '0%',
            capital_gains: '0%',
            notes: 'UAE has no personal income tax. 5% VAT since 2018.'
        },
        
        visas: [
            {n: 'Employment Visa', d: 'Standard work visa sponsored by employer', t: '2-4 weeks', r: ['Job offer', 'Medical test', 'Emirates ID', 'Employer sponsorship']},
            {n: 'Golden Visa (10 years)', d: 'Long-term residency for skilled professionals', t: '2-4 weeks', r: ['Salary AED 30K+/month OR', 'PhD degree OR', 'Specialized talent in tech/science']},
            {n: 'Green Visa (5 years)', d: 'Self-sponsored residency', t: '4-6 weeks', r: ['Salary AED 15K+/month', 'Bachelor degree', 'Skilled worker category']}
        ],
        
        agencies: [
            {n: 'Michael Page', s: 'Executive & Tech recruitment', w: 'https://michaelpage.ae', verified: true},
            {n: 'Robert Half', s: 'IT & Finance recruitment', w: 'https://roberthalf.ae', verified: true},
            {n: 'Hays', s: 'Tech & Engineering', w: 'https://hays.ae', verified: true},
            {n: 'Bayt.com', s: 'Largest Middle East job portal', w: 'https://bayt.com', verified: true},
            {n: 'GulfTalent', s: 'Regional tech recruitment', w: 'https://gulftalent.com', verified: true}
        ],
        
        portals: [
            {n: 'LinkedIn UAE', u: 'https://linkedin.com/jobs', d: 'Best for tech jobs & networking'},
            {n: 'Bayt.com', u: 'https://bayt.com', d: 'Largest Middle East job site - Top rated'},
            {n: 'GulfTalent', u: 'https://gulftalent.com', d: 'Premium Gulf jobs with extensive database'},
            {n: 'Indeed UAE', u: 'https://ae.indeed.com', d: 'Wide range of jobs across industries'},
            {n: 'Naukri Gulf', u: 'https://naukrigulf.com', d: 'Indian-focused portal for Gulf jobs'},
            {n: 'Dubizzle Jobs', u: 'https://dubizzle.com/jobs', d: 'Local job listings in UAE'},
            {n: 'Dubaijobs.net', u: 'https://dubaijobs.net', d: 'Niche portal specifically for Dubai openings'},
            {n: 'Gulfjobcareers.com', u: 'https://gulfjobcareers.com', d: 'Jobs from Gulf region companies'},
            {n: 'Careerjet.ae', u: 'https://careerjet.ae', d: 'Job search engine aggregating multiple sources'}
        ],
        
        recruiter_emails: [
            'info@mackenziejones.com', 'info@sawaeed.ae', 'clientmiddleeast@hays.com',
            'info@receptionistpa.com', 'jobs@reachgroup.ae', 'info@nathanhr.com',
            'sparkmos@spark.ae', 'info@uhrs.ae', 'info@inspireselection.com',
            'info@sundusrecruitment.com', 'jobs@alvakil.net', 'info@derbygroup.ae',
            'adeccoa.e.info@adecco.com', 'submit@bacme.com', 'contact@nadiaglobal.com',
            'info@almansoorgroup.com', 'recruit@bacme.com', 'cv@xpertsjobs.com',
            'employers@jvi-global.com', 'adminmumbai@alvakil.net',
            'talascend.marketing@talascend.com', 'info@cig.ae', 'cv@sundusrecruitment.com',
            'enquiry@al-thawiya.com', 'info@akrs.ae', 'horizongroup@horizon.ae',
            'info@tascoutsourcing.com', 'request@tascoutsourcing.com',
            'recruitment@innovationuae.com', 'info@manpower-me.com', 'info@admsuae.com',
            'lobo@lobomanagement.com', 'clientmiddleeast@michaelpage.ae',
            'dxbjobs@tascoutsourcing.com', 'info@executivesolutionsme.com',
            'info@alnahiya.com', 'gaile@expertsrecruitment.com', 'mike@kershawleonard.net',
            'jobseekers@jvi-global.com', 'info@asrs.ae', 'corporate.communications@randstad.com',
            'cv@pactemployment.ae'
        ],
        
        tips: [
            'Negotiate housing allowance separately - it\'s common in UAE',
            'Join WhatsApp groups for Indian professionals in Dubai',
            'Get Emirates ID immediately - needed for everything',
            'Open a UAE bank account (Emirates NBD, ADCB popular among Indians)',
            'Consider Sharjah for cheaper housing if working in Dubai',
            'Summer months (June-Aug) have fewer opportunities',
            'Ramadan period has different work hours',
            'Build LinkedIn network with UAE-based recruiters',
            'Health insurance is mandatory - ensure employer provides',
            'Save aggressively - no tax is a huge advantage'
        ],
        
        interview: [
            'Video interviews are common for international hiring',
            'Expect 3-4 rounds: HR screening, Technical, Manager, Final',
            'Salary negotiation is expected - start 20% higher',
            'Ask about visa process, relocation support, housing allowance',
            'Research company reviews on Glassdoor UAE',
            'Prepare for behavioral questions (STAR method)'
        ],
        
        network: [
            'Dubai Tech Community (Meetup.com)',
            'Indian Professionals Network UAE (LinkedIn)',
            'TiE Dubai - Entrepreneurship network',
            'Google Developer Group Dubai',
            'AWS User Group Dubai'
        ]
    },

    // ==================== GERMANY ====================
    Germany: {
        visa_processing: '6-12 weeks',
        visa_cost: '₹7,000-10,000 (€75)',
        tax_rate: '14-45% Progressive',
        language: 'German (English in tech companies)',
        weather: 'Temperate - Cold winters (0°C), mild summers (20-25°C)',
        indian_population: '200,000+',
        currency: 'EUR (1 EUR ≈ ₹90)',
        timezone: 'GMT+1 (4.5hrs behind IST)',
        flight_time: '8-9 hours',
        
        pros: [
            'EU Blue Card - Fast track to permanent residency',
            'Free/Cheap university education for kids',
            'Excellent public healthcare (included in taxes)',
            'Strong job security and worker rights',
            '30+ vacation days mandated by law',
            'EU access - work anywhere in Schengen',
            'High quality of life',
            'Excellent public transport',
            'Path to citizenship in 8 years (6 with German proficiency)',
            'Strong economy and stable job market'
        ],
        cons: [
            'High taxes (42% for high earners)',
            'German language helpful for daily life',
            'Bureaucracy can be slow and frustrating',
            'Cold, grey winters (Seasonal depression common)',
            'Finding housing in cities like Munich, Berlin is very hard',
            'Sunday shops closed (Blue laws)',
            'Cultural adjustment - Germans are reserved initially',
            'Healthcare system has long wait times for specialists'
        ],
        
        best_cities: [
            {name: 'Berlin', why: 'Startup hub, diverse, affordable (for Germany), English-friendly'},
            {name: 'Munich', why: 'Highest salaries, BMW, Siemens, Allianz, but very expensive'},
            {name: 'Frankfurt', why: 'Finance & consulting hub, international'},
            {name: 'Hamburg', why: 'Growing tech scene, port city'},
            {name: 'Düsseldorf', why: 'Japanese/Asian community, consulting'}
        ],
        
        lifestyle: {
            work_hours: '8 AM - 5 PM (Work-life balance is sacred)',
            weekend: 'Saturday-Sunday (Shops closed Sunday)',
            dress_code: 'Smart casual to casual in tech',
            social_life: 'Beer gardens, parks, cultural events',
            indian_community: 'Growing - temples in major cities, Diwali celebrations',
            food: 'Indian restaurants available, Aldi/Lidl have some Indian products'
        },
        
        expenses: {
            rent: {s: '₹50,000-1,00,000', f: '₹80,000-1,60,000'},
            food: {s: '₹25,000-35,000', f: '₹40,000-60,000'},
            transport: {s: '₹8,000-12,000', f: '₹12,000-18,000'},
            utilities: {s: '₹15,000-25,000', f: '₹25,000-35,000'},
            healthcare: {s: 'Included in taxes', f: 'Included in taxes'},
            entertainment: {s: '₹15,000-25,000', f: '₹25,000-40,000'},
            total: {s: '₹1,15,000-2,00,000', f: '₹1,80,000-3,20,000'}
        },
        
        initial: {
            visa: '₹15,000-25,000 (including blocked account)',
            flight: '₹40,000-70,000',
            deposit: '₹1,50,000-3,00,000 (3 months rent)',
            blocked_account: '₹10,00,000 (€11,208 required)',
            furniture: '₹80,000-1,50,000',
            total: '₹13,00,000-16,00,000'
        },
        
        salaries: {
            'Junior Developer (0-2y)': '₹35-50 LPA (€40-55K)',
            'Mid Developer (3-5y)': '₹55-75 LPA (€60-85K)',
            'Senior Developer (5-8y)': '₹70-95 LPA (€78-105K)',
            'Tech Lead (8-12y)': '₹85-1.2 Cr (€95-130K)',
            'Architect/Principal (12+y)': '₹1-1.5 Cr (€110-165K)',
            'Engineering Manager': '₹90-1.3 Cr (€100-140K)'
        },
        
        savings_potential: {
            junior: '₹8-12 LPA (25-30% after tax)',
            mid: '₹15-22 LPA (28-32% after tax)',
            senior: '₹22-30 LPA (30-35% after tax)',
            lead: '₹30-40 LPA (32-38% after tax)'
        },
        
        taxes: {
            income_tax: '14% (€10K) to 45% (€277K+)',
            solidarity_surcharge: '5.5% on income tax',
            church_tax: '8-9% if registered (optional)',
            social_security: '~20% (pension, health, unemployment)',
            notes: 'Total deductions ~40-45%. But includes healthcare, pension, unemployment insurance.'
        },
        
        visas: [
            {n: 'EU Blue Card', d: 'For qualified professionals - best option', t: '6-12 weeks', r: ['Job offer €45K+ (€41K for shortage occupations like IT)', 'Recognized degree', 'Valid passport', 'Health insurance']},
            {n: 'Work Visa (Skilled)', d: 'For skilled workers', t: '8-12 weeks', r: ['Job offer', 'Recognized qualification', '6 months blocked account proof']},
            {n: 'Job Seeker Visa', d: '6 months to find job in Germany', t: '4-8 weeks', r: ['Degree', 'Blocked account (€11,208)', 'No job offer needed']}
        ],
        
        agencies: [
            {n: 'Honeypot', s: 'Tech-only platform, companies apply to you', w: 'https://honeypot.io', verified: true},
            {n: 'Talent.io', s: 'Tech recruitment, salary transparency', w: 'https://talent.io', verified: true},
            {n: 'Berlin Startup Jobs', s: 'Startup focused', w: 'https://berlinstartupjobs.com', verified: true},
            {n: 'Relocate.me', s: 'Visa sponsorship focus', w: 'https://relocate.me', verified: true}
        ],
        
        companies_with_relocation: [
            {n: 'Zalando', s: 'E-commerce/Tech', relocation: true},
            {n: 'Delivery Hero', s: 'Food Tech', relocation: true},
            {n: 'N26', s: 'Fintech', relocation: true},
            {n: 'AUTO1 Group', s: 'Automotive/Tech', relocation: true},
            {n: 'FlixBus', s: 'Mobility/Travel', relocation: true},
            {n: 'Celonis', s: 'Process Mining/Tech', relocation: true},
            {n: 'HelloFresh', s: 'Food Tech', relocation: true},
            {n: 'GetYourGuide', s: 'Travel Tech', relocation: true},
            {n: 'Forto', s: 'Logistics/Tech', relocation: true},
            {n: 'Billie', s: 'Fintech', relocation: true},
            {n: 'Wolt', s: 'Food Delivery', relocation: true},
            {n: 'Babbel', s: 'EdTech', relocation: true},
            {n: 'SumUp', s: 'Fintech', relocation: true},
            {n: 'Omio', s: 'Travel Tech', relocation: true},
            {n: 'Adjust', s: 'AdTech', relocation: true},
            {n: 'ResearchGate', s: 'Tech/Academia', relocation: true},
            {n: 'Ada Health', s: 'Health Tech', relocation: true},
            {n: 'Raisin', s: 'Fintech', relocation: true},
            {n: 'Blinkist', s: 'EdTech', relocation: true},
            {n: 'SoundCloud', s: 'Music Tech', relocation: true},
            {n: 'SAP', s: 'Enterprise Tech', relocation: true},
            {n: 'Siemens', s: 'Engineering', relocation: true},
            {n: 'Bosch', s: 'Engineering/Tech', relocation: true},
            {n: 'Infarm', s: 'AgriTech', relocation: true},
            {n: 'Scout24', s: 'Tech/Marketplace', relocation: true},
            {n: 'Personio', s: 'HR Tech', relocation: true},
            {n: 'Trade Republic', s: 'Fintech', relocation: true},
            {n: 'Bayer', s: 'Pharma', relocation: 'sometimes'},
            {n: 'Roche', s: 'Pharma', relocation: 'sometimes'},
            {n: 'Fresenius', s: 'Healthcare', relocation: 'sometimes'}
        ],
        
        portals: [
            {n: 'LinkedIn Germany', u: 'https://linkedin.com/jobs/germany', d: 'Best for tech'},
            {n: 'StepStone', u: 'https://stepstone.de', d: 'Largest German job portal'},
            {n: 'Xing', u: 'https://xing.com', d: 'German LinkedIn alternative'},
            {n: 'Indeed Germany', u: 'https://de.indeed.com', d: 'Wide range'},
            {n: 'Glassdoor Germany', u: 'https://glassdoor.de', d: 'Reviews + jobs'},
            {n: 'Stack Overflow Jobs', u: 'https://stackoverflow.com/jobs', d: 'Developer focused'}
        ],
        
        tips: [
            'Learn basic German (A1/A2) before moving - helps daily life immensely',
            'Apply for Anmeldung (address registration) within 14 days of arrival',
            'Open a blocked account (Sperrkonto) for visa - Expatrio, Fintiba are popular',
            'Get Schufa (credit score) early - needed for renting apartments',
            'Join WG (shared apartments) initially - easier than finding solo apartment',
            'Deutsche Bahn (train) has Bahncard 25/50 for discounts',
            'Tax filing is complex - use services like Taxfix or hire Steuerberater',
            'Join English-speaking meetups in Berlin, Munich',
            'Amazon Germany delivers most things you need'
        ],
        
        interview: [
            'Technical interviews similar to US but less LeetCode-heavy',
            'Cultural fit is important - be prepared for behavioral questions',
            'Work-life balance is valued - don\'t oversell overtime willingness',
            'Salary ranges are often listed (transparency laws)',
            'Ask about visa sponsorship, relocation package',
            'Remote work policies vary - clarify early'
        ],
        
        network: [
            'Berlin Tech Meetup',
            'Indians in Germany (Facebook/LinkedIn)',
            'Google Developer Group Germany',
            'AWS User Group Berlin/Munich',
            'TiE Germany - Entrepreneurship'
        ]
    },

    // ==================== CANADA ====================
    Canada: {
        visa_processing: '6-12 weeks (Express Entry)',
        visa_cost: '₹1,50,000-2,50,000 (CAD 2000-3000)',
        tax_rate: '15-33% Federal + Provincial',
        language: 'English & French',
        weather: 'Cold winters (-20°C), mild summers (25°C)',
        indian_population: '1.8 Million+',
        currency: 'CAD (1 CAD ≈ ₹62)',
        timezone: 'GMT-5 to GMT-8',
        flight_time: '14-18 hours',
        
        pros: [
            'Clear PR pathway through Express Entry',
            'Free healthcare for PR/Citizens',
            'Welcoming multicultural society',
            'Large Indian community',
            'Good work-life balance',
            'Quality education system',
            'Path to citizenship in 3 years of PR',
            'Close to US market for business',
            'Safe, clean cities',
            'Family-friendly immigration policies'
        ],
        cons: [
            'Very cold winters (especially inland)',
            'High cost of living (Toronto, Vancouver)',
            'Lower salaries than US',
            'Housing crisis in major cities',
            'Long wait times for healthcare',
            'Credential recognition can be slow',
            'Job market competitive in some sectors',
            'Remote from India (long flights)'
        ],
        
        best_cities: [
            {name: 'Toronto', why: 'Largest tech hub, most jobs, most expensive'},
            {name: 'Vancouver', why: 'Beautiful, mild weather, expensive'},
            {name: 'Calgary', why: 'Lower cost, growing tech, colder'},
            {name: 'Ottawa', why: 'Government jobs, Shopify HQ'},
            {name: 'Montreal', why: 'Affordable, AI hub (requires French)'}
        ],
        
        lifestyle: {
            work_hours: '9 AM - 5 PM (Good work-life balance)',
            weekend: 'Saturday-Sunday',
            dress_code: 'Casual to smart casual',
            social_life: 'Outdoor activities, multicultural events',
            indian_community: 'Huge - Brampton is 50%+ South Asian',
            food: 'Excellent Indian food scene, desi groceries everywhere'
        },
        
        expenses: {
            rent: {s: '₹80,000-1,50,000', f: '₹1,20,000-2,50,000'},
            food: {s: '₹30,000-45,000', f: '₹50,000-75,000'},
            transport: {s: '₹10,000-20,000', f: '₹15,000-30,000'},
            utilities: {s: '₹12,000-20,000', f: '₹20,000-35,000'},
            healthcare: {s: 'Free with PR', f: 'Free with PR'},
            entertainment: {s: '₹20,000-35,000', f: '₹35,000-55,000'},
            total: {s: '₹1,50,000-2,70,000', f: '₹2,40,000-4,50,000'}
        },
        
        initial: {
            visa: '₹1,50,000-2,50,000 (application fees)',
            flight: '₹60,000-1,00,000',
            deposit: '₹2,50,000-4,00,000 (first+last month rent)',
            proof_of_funds: '₹15,00,000-25,00,000 (required for PR)',
            settlement: '₹2,00,000-3,00,000',
            total: '₹22,00,000-35,00,000'
        },
        
        salaries: {
            'Junior Developer (0-2y)': '₹40-55 LPA (CAD 55-75K)',
            'Mid Developer (3-5y)': '₹55-80 LPA (CAD 75-110K)',
            'Senior Developer (5-8y)': '₹75-1.1 Cr (CAD 100-150K)',
            'Tech Lead (8-12y)': '₹90-1.3 Cr (CAD 120-175K)',
            'Architect/Principal (12+y)': '₹1.1-1.6 Cr (CAD 150-220K)',
            'Engineering Manager': '₹1-1.5 Cr (CAD 140-200K)'
        },
        
        savings_potential: {
            junior: '₹8-12 LPA (22-25% after tax)',
            mid: '₹12-20 LPA (25-28% after tax)',
            senior: '₹20-30 LPA (28-32% after tax)',
            lead: '₹30-45 LPA (30-35% after tax)'
        },
        
        taxes: {
            income_tax: '15% to 33% Federal + 5-25% Provincial',
            capital_gains: '50% of gains taxable',
            cpp: 'Canada Pension Plan ~5.95%',
            ei: 'Employment Insurance ~1.58%',
            notes: 'Ontario total tax ~35-45% for tech salaries. RRSP/TFSA help reduce taxes.'
        },
        
        visas: [
            {n: 'Express Entry (PR)', d: 'Points-based permanent residency', t: '6-12 months', r: ['CRS score 460+', 'IELTS 7+', 'Education credential assessment', 'Proof of funds']},
            {n: 'Provincial Nominee (PNP)', d: 'Province-specific immigration', t: '12-18 months', r: ['Provincial criteria', 'Job offer (some streams)', 'Lower CRS acceptable']},
            {n: 'Work Permit (LMIA)', d: 'Employer-sponsored work permit', t: '2-4 months', r: ['Job offer', 'LMIA approval', 'Employer sponsorship']}
        ],
        
        agencies: [
            {n: 'Randstad Canada', s: 'General tech recruitment', w: 'https://randstad.ca', verified: true},
            {n: 'Robert Half Canada', s: 'IT & Finance', w: 'https://roberthalf.ca', verified: true},
            {n: 'Hays Canada', s: 'Tech recruitment', w: 'https://hays.ca', verified: true}
        ],
        
        portals: [
            {n: 'LinkedIn Canada', u: 'https://linkedin.com/jobs/canada', d: 'Best for tech'},
            {n: 'Indeed Canada', u: 'https://ca.indeed.com', d: 'Wide range'},
            {n: 'Glassdoor Canada', u: 'https://glassdoor.ca', d: 'Reviews + salary'},
            {n: 'Job Bank', u: 'https://jobbank.gc.ca', d: 'Government portal'},
            {n: 'Workopolis', u: 'https://workopolis.com', d: 'Canadian jobs'}
        ],
        
        tips: [
            'Apply for Express Entry - fastest PR route',
            'Get IELTS score of 8+ for better CRS points',
            'WES evaluation for educational credentials takes 2-3 months',
            'Join LinkedIn communities for Canada immigration',
            'Consider PNP if Express Entry score is low',
            'Open Canadian bank account online before arrival (RBC, TD)',
            'Get SIN number immediately after landing',
            'Buy winter gear before winter - it\'s serious cold',
            'RRSP and TFSA are excellent tax-saving tools'
        ],
        
        interview: [
            'Less LeetCode focus than US companies',
            'Behavioral questions are very important',
            'Cultural fit matters a lot',
            'Work-life balance discussions are welcomed',
            'Remote work is common post-COVID',
            'Be prepared to discuss visa status upfront'
        ],
        
        network: [
            'Toronto Tech Community',
            'Indians in Canada (Facebook groups)',
            'Tech Toronto Meetup',
            'Vancouver Tech Community',
            'TiE Toronto'
        ]
    },

    // ==================== AUSTRALIA ====================
    Australia: {
        visa_processing: '4-12 weeks',
        visa_cost: '₹3,00,000-5,00,000 (AUD 4000-6000)',
        tax_rate: '19-45% Progressive',
        language: 'English',
        weather: 'Varied - Hot summers (35°C), mild winters (10-15°C)',
        indian_population: '800,000+',
        currency: 'AUD (1 AUD ≈ ₹55)',
        timezone: 'GMT+8 to GMT+11 (2.5-5.5hrs ahead of IST)',
        flight_time: '10-12 hours',
        
        pros: [
            'High salaries with good work-life balance',
            'Clear PR pathway through points system',
            'Beautiful weather and outdoor lifestyle',
            'Strong economy and job market',
            'Multicultural society',
            'Excellent healthcare (Medicare)',
            'High quality of life',
            'Close timezone to India',
            'Large Indian community',
            'English-speaking country'
        ],
        cons: [
            'Very expensive visa fees',
            'High cost of living in Sydney/Melbourne',
            'Far from India (but closer than US/Europe)',
            'Housing affordability crisis',
            'PR processing times have increased',
            'Limited public transport outside major cities',
            'Skilled occupation list changes frequently',
            'Wildlife concerns (snakes, spiders)'
        ],
        
        best_cities: [
            {name: 'Sydney', why: 'Most jobs, highest salaries, most expensive'},
            {name: 'Melbourne', why: 'Cultural hub, slightly cheaper, tech growing'},
            {name: 'Brisbane', why: 'Growing fast, better weather, affordable'},
            {name: 'Perth', why: 'Mining tech, isolated but good lifestyle'},
            {name: 'Adelaide', why: 'Affordable, extra PR points for regional'}
        ],
        
        lifestyle: {
            work_hours: '9 AM - 5 PM (Work-life balance prioritized)',
            weekend: 'Saturday-Sunday',
            dress_code: 'Casual to smart casual',
            social_life: 'Beaches, outdoor activities, BBQs',
            indian_community: 'Large - especially in Sydney, Melbourne',
            food: 'Great Indian restaurants, Coles/Woolworths have Indian sections'
        },
        
        expenses: {
            rent: {s: '₹90,000-1,80,000', f: '₹1,50,000-2,80,000'},
            food: {s: '₹30,000-50,000', f: '₹55,000-85,000'},
            transport: {s: '₹12,000-22,000', f: '₹20,000-35,000'},
            utilities: {s: '₹10,000-18,000', f: '₹18,000-28,000'},
            healthcare: {s: '₹8,000-15,000 (private)', f: '₹15,000-25,000'},
            entertainment: {s: '₹20,000-35,000', f: '₹35,000-55,000'},
            total: {s: '₹1,70,000-3,20,000', f: '₹2,90,000-5,00,000'}
        },
        
        initial: {
            visa: '₹3,00,000-5,00,000',
            flight: '₹50,000-80,000',
            deposit: '₹3,00,000-5,00,000 (4 weeks rent + bond)',
            health_insurance: '₹50,000-80,000 (first year)',
            settlement: '₹2,00,000-3,00,000',
            total: '₹9,00,000-14,00,000'
        },
        
        salaries: {
            'Junior Developer (0-2y)': '₹45-60 LPA (AUD 65-85K)',
            'Mid Developer (3-5y)': '₹65-90 LPA (AUD 90-125K)',
            'Senior Developer (5-8y)': '₹85-1.2 Cr (AUD 120-170K)',
            'Tech Lead (8-12y)': '₹1-1.4 Cr (AUD 140-200K)',
            'Architect/Principal (12+y)': '₹1.2-1.8 Cr (AUD 170-250K)',
            'Engineering Manager': '₹1.1-1.6 Cr (AUD 160-230K)'
        },
        
        savings_potential: {
            junior: '₹8-15 LPA (20-25%)',
            mid: '₹15-25 LPA (25-30%)',
            senior: '₹25-40 LPA (30-35%)',
            lead: '₹35-50 LPA (35-40%)'
        },
        
        taxes: {
            income_tax: '19% (AUD 18K) to 45% (AUD 180K+)',
            medicare_levy: '2% on income',
            superannuation: '11% employer contribution (pension)',
            notes: 'Total tax ~30-38% for tech salaries. Super is on top of salary.'
        },
        
        visas: [
            {n: 'Skilled Independent (189)', d: 'Points-based, no sponsorship needed', t: '6-12 months', r: ['65+ points', 'Skill assessment', 'IELTS 6+', 'Under 45 years']},
            {n: 'Skilled Nominated (190)', d: 'State-nominated PR', t: '6-12 months', r: ['65+ points (with nomination)', 'State nomination', 'Commitment to state']},
            {n: 'TSS 482 (Work Visa)', d: 'Employer sponsored temporary', t: '1-4 months', r: ['Job offer', 'Employer sponsorship', '2 years experience']}
        ],
        
        agencies: [
            {n: 'Hays Australia', s: 'Largest tech recruiter', w: 'https://hays.com.au', verified: true},
            {n: 'Robert Half', s: 'IT recruitment', w: 'https://roberthalf.com.au', verified: true},
            {n: 'Talent', s: 'Tech focused', w: 'https://talent.com.au', verified: true}
        ],
        
        portals: [
            {n: 'Seek', u: 'https://seek.com.au', d: 'Largest Australian job portal'},
            {n: 'LinkedIn Australia', u: 'https://linkedin.com/jobs/australia', d: 'Tech jobs'},
            {n: 'Indeed Australia', u: 'https://au.indeed.com', d: 'Wide range'},
            {n: 'Glassdoor Australia', u: 'https://glassdoor.com.au', d: 'Reviews + salary'}
        ],
        
        tips: [
            'Get skill assessment from ACS (Australian Computer Society) early',
            'IELTS/PTE score matters a lot for points',
            'Consider regional areas for extra 5-15 points',
            'Check Skilled Occupation List before applying',
            'Medicare enrollment immediately after PR',
            'Open bank account with NAB/CommBank/Westpac',
            'Get TFN (Tax File Number) immediately',
            'Superannuation is like forced savings - grows over time',
            'Sydney/Melbourne are very competitive, consider other cities'
        ],
        
        interview: [
            'Mix of technical and behavioral',
            'Work-life balance is valued - discuss openly',
            'Cultural fit important for Australian companies',
            'Visa sponsorship less common than before',
            'Remote work available for many roles',
            'Salary negotiation expected'
        ],
        
        network: [
            'Sydney Tech Meetup',
            'Melbourne AWS User Group',
            'Indians in Australia (Facebook)',
            'Australian Computer Society',
            'Product Hunt Sydney'
        ]
    },

    // ==================== SINGAPORE ====================
    Singapore: {
        visa_processing: '3-8 weeks',
        visa_cost: '₹20,000-40,000',
        tax_rate: '0-22% Progressive',
        language: 'English, Mandarin, Malay, Tamil',
        weather: 'Tropical - Hot and humid year-round (28-32°C)',
        indian_population: '650,000+ (9% of population)',
        currency: 'SGD (1 SGD ≈ ₹62)',
        timezone: 'GMT+8 (2.5hrs ahead of IST)',
        flight_time: '5-6 hours',
        
        pros: [
            'Very low taxes (max 22%)',
            'Extremely safe city (lowest crime)',
            'Close to India - 5hr flight',
            'Large Indian community (9%)',
            'World-class infrastructure',
            'English is primary language',
            'Clean, efficient city',
            'Great food (including Indian)',
            'Hub for Asian business',
            'Excellent healthcare'
        ],
        cons: [
            'Very expensive housing',
            'Small country - can feel limiting',
            'Hot and humid all year',
            'Competitive work culture',
            'EP (work pass) requirements have tightened',
            'Car ownership extremely expensive',
            'PR more difficult to obtain',
            'Strict laws and regulations',
            'No clear PR timeline'
        ],
        
        best_cities: [
            {name: 'Singapore', why: 'City-state - entire country is the city!'},
            {name: 'Central Region', why: 'CBD, Marina Bay - premium but convenient'},
            {name: 'East Coast', why: 'Indian enclave, Little India nearby'},
            {name: 'West Region', why: 'More affordable, good for families'}
        ],
        
        lifestyle: {
            work_hours: '9 AM - 6 PM (Can be longer in some companies)',
            weekend: 'Saturday-Sunday',
            dress_code: 'Smart casual to business casual',
            social_life: 'Food culture, malls, nearby travel to SEA',
            indian_community: 'Very strong - Little India, temples, cultural events',
            food: 'Amazing Indian food, vegetarian options widely available'
        },
        
        expenses: {
            rent: {s: '₹1,20,000-2,50,000', f: '₹2,00,000-4,00,000'},
            food: {s: '₹25,000-40,000', f: '₹45,000-70,000'},
            transport: {s: '₹8,000-15,000', f: '₹12,000-22,000'},
            utilities: {s: '₹8,000-15,000', f: '₹15,000-25,000'},
            healthcare: {s: '₹5,000-12,000', f: '₹12,000-25,000'},
            entertainment: {s: '₹20,000-35,000', f: '₹35,000-55,000'},
            total: {s: '₹1,85,000-3,65,000', f: '₹3,20,000-6,00,000'}
        },
        
        initial: {
            visa: '₹20,000-40,000',
            flight: '₹20,000-35,000',
            deposit: '₹4,00,000-8,00,000 (2-3 months rent)',
            agent_fee: '₹1,00,000-2,00,000',
            furniture: '₹1,00,000-2,00,000',
            total: '₹6,50,000-12,00,000'
        },
        
        salaries: {
            'Junior Developer (0-2y)': '₹40-55 LPA (SGD 48-66K)',
            'Mid Developer (3-5y)': '₹60-85 LPA (SGD 72-102K)',
            'Senior Developer (5-8y)': '₹80-1.2 Cr (SGD 96-144K)',
            'Tech Lead (8-12y)': '₹1-1.5 Cr (SGD 120-180K)',
            'Architect/Principal (12+y)': '₹1.3-2 Cr (SGD 156-240K)',
            'Engineering Manager': '₹1.1-1.7 Cr (SGD 132-204K)'
        },
        
        savings_potential: {
            junior: '₹10-18 LPA (28-35%)',
            mid: '₹18-30 LPA (32-38%)',
            senior: '₹30-45 LPA (38-42%)',
            lead: '₹45-65 LPA (40-45%)'
        },
        
        taxes: {
            income_tax: '0% (first SGD 20K) to 22% (SGD 320K+)',
            cpf: 'Central Provident Fund - 20% employee + 17% employer (citizens/PR)',
            gst: '9% on goods/services',
            notes: 'Very low taxes. EP holders don\'t contribute to CPF. Effective rate ~15-18% for most tech salaries.'
        },
        
        visas: [
            {n: 'Employment Pass (EP)', d: 'For professionals earning SGD 5000+/month', t: '3-8 weeks', r: ['Job offer SGD 5000+', 'Recognized degree', 'Relevant experience', 'COMPASS framework score']},
            {n: 'S Pass', d: 'For mid-skilled workers SGD 3150+', t: '3-4 weeks', r: ['Job offer SGD 3150+', 'Diploma/degree', 'Employer quota available']},
            {n: 'Tech.Pass', d: 'For tech leaders/founders', t: '4-8 weeks', r: ['SGD 20K+ salary OR', 'Leadership at major tech company OR', 'Significant tech achievements']}
        ],
        
        agencies: [
            {n: 'Michael Page Singapore', s: 'Tech & Finance recruitment', w: 'https://michaelpage.com.sg', verified: true},
            {n: 'Robert Walters', s: 'Tech recruitment', w: 'https://robertwalters.com.sg', verified: true},
            {n: 'Hays Singapore', s: 'Technology recruitment', w: 'https://hays.com.sg', verified: true}
        ],
        
        portals: [
            {n: 'LinkedIn Singapore', u: 'https://linkedin.com/jobs/singapore', d: 'Best for tech'},
            {n: 'JobStreet', u: 'https://jobstreet.com.sg', d: 'Popular local portal'},
            {n: 'Indeed Singapore', u: 'https://sg.indeed.com', d: 'Wide range'},
            {n: 'NodeFlair', u: 'https://nodeflair.com', d: 'Tech-focused, salary data'}
        ],
        
        tips: [
            'EP minimum salary increased to SGD 5000 in 2023 - budget accordingly',
            'COMPASS framework now affects EP approval - check points calculator',
            'Find accommodation BEFORE arriving - very competitive',
            'MRT (metro) is excellent - you don\'t need a car',
            'Little India for groceries, restaurants, community',
            'DBS/POSB/OCBC are popular banks',
            'SingPass is essential for government services',
            'Weekend trips to Malaysia, Indonesia, Thailand are cheap',
            'Join Singapore Indians Facebook groups'
        ],
        
        interview: [
            'Technical interviews are rigorous',
            'LeetCode practice recommended',
            'System design important for senior roles',
            'Fast hiring process (1-2 weeks)',
            'Multiple rounds: HR, Technical, Manager',
            'Salary negotiation is expected'
        ],
        
        network: [
            'Singapore Tech Meetup',
            'Google Developer Group Singapore',
            'AWS User Group Singapore',
            'Indians in Singapore (Facebook)',
            'Junior Developers Singapore'
        ]
    },

    // ==================== UK ====================
    UK: {
        visa_processing: '3-8 weeks',
        visa_cost: '₹50,000-1,00,000',
        tax_rate: '20-45% Progressive',
        language: 'English',
        weather: 'Mild, rainy. Cool summers (18-22°C), cold winters (2-8°C)',
        indian_population: '1.5 Million+',
        currency: 'GBP (1 GBP ≈ ₹105)',
        timezone: 'GMT (5.5hrs behind IST)',
        flight_time: '8-10 hours',
        
        pros: [
            'English speaking - easy transition',
            'NHS healthcare (free with taxes)',
            'Strong Indian community',
            'Global financial hub',
            'Rich history and culture',
            'Good work-life balance',
            'Path to settlement (ILR) in 5 years',
            'Gateway to Europe (despite Brexit)',
            'Established tech ecosystem',
            'Premier League, British culture!'
        ],
        cons: [
            'High taxes (40%+ for higher earners)',
            'Very expensive (especially London)',
            'Brexit complications',
            'Grey, rainy weather',
            'NHS wait times can be long',
            'Housing crisis in London',
            'Cost of living crisis ongoing',
            'Visa costs have increased'
        ],
        
        best_cities: [
            {name: 'London', why: 'Most opportunities, highest salaries, very expensive'},
            {name: 'Manchester', why: 'Growing tech hub, BBC, cheaper'},
            {name: 'Edinburgh', why: 'Financial services, beautiful city'},
            {name: 'Birmingham', why: 'Second largest, growing tech scene'},
            {name: 'Bristol', why: 'Tech startups, quality of life'}
        ],
        
        lifestyle: {
            work_hours: '9 AM - 5:30 PM',
            weekend: 'Saturday-Sunday',
            dress_code: 'Business casual to casual',
            social_life: 'Pubs, cultural events, football',
            indian_community: 'Massive - especially in Leicester, London, Birmingham',
            food: 'British Indian food is its own cuisine! Amazing variety'
        },
        
        expenses: {
            rent: {s: '₹80,000-2,00,000 (London)', f: '₹1,50,000-3,50,000'},
            food: {s: '₹25,000-40,000', f: '₹45,000-70,000'},
            transport: {s: '₹15,000-30,000', f: '₹25,000-45,000'},
            utilities: {s: '₹12,000-22,000', f: '₹22,000-35,000'},
            healthcare: {s: 'NHS (tax funded)', f: 'NHS (tax funded)'},
            entertainment: {s: '₹20,000-35,000', f: '₹35,000-55,000'},
            total: {s: '₹1,50,000-3,30,000', f: '₹2,75,000-5,55,000'}
        },
        
        initial: {
            visa: '₹60,000-1,00,000 (including IHS)',
            flight: '₹45,000-75,000',
            deposit: '₹2,50,000-5,00,000 (5-6 weeks rent)',
            ihs_surcharge: '₹50,000-70,000 (Immigration Health Surcharge)',
            settlement: '₹1,50,000-2,50,000',
            total: '₹5,50,000-9,00,000'
        },
        
        salaries: {
            'Junior Developer (0-2y)': '₹35-50 LPA (£30-42K)',
            'Mid Developer (3-5y)': '₹55-80 LPA (£48-70K)',
            'Senior Developer (5-8y)': '₹75-1.15 Cr (£65-100K)',
            'Tech Lead (8-12y)': '₹95-1.4 Cr (£82-120K)',
            'Architect/Principal (12+y)': '₹1.2-1.8 Cr (£100-155K)',
            'Engineering Manager': '₹1-1.5 Cr (£90-130K)'
        },
        
        savings_potential: {
            junior: '₹5-10 LPA (15-22%)',
            mid: '₹12-20 LPA (22-28%)',
            senior: '₹20-35 LPA (28-32%)',
            lead: '₹30-45 LPA (30-35%)'
        },
        
        taxes: {
            income_tax: '20% (£12.5K-50K), 40% (£50K-125K), 45% (£125K+)',
            national_insurance: '12% on earnings above £12,570',
            council_tax: '£1,500-3,000/year depending on property',
            notes: 'Total tax ~35-45% for tech salaries. Personal allowance reduces to 0 at £125K+'
        },
        
        visas: [
            {n: 'Skilled Worker Visa', d: 'Employer-sponsored work visa', t: '3-8 weeks', r: ['Job offer at RQF 3+', 'Salary £26K+ (or going rate)', 'Certificate of Sponsorship', 'English proficiency']},
            {n: 'Global Talent Visa', d: 'For exceptional talent in tech', t: '4-8 weeks', r: ['Endorsement from Tech Nation', 'OR exceptional promise/talent', 'No job offer needed']},
            {n: 'Scale-up Visa', d: 'For scale-up company hires', t: '3-8 weeks', r: ['Job at qualifying scale-up', 'Salary £33,000+', '6 months then unrestricted work']}
        ],
        
        agencies: [
            {n: 'Hays UK', s: 'Largest tech recruiter', w: 'https://hays.co.uk', verified: true},
            {n: 'Robert Half UK', s: 'IT & Finance', w: 'https://roberthalf.co.uk', verified: true},
            {n: 'Michael Page', s: 'Tech recruitment', w: 'https://michaelpage.co.uk', verified: true}
        ],
        
        portals: [
            {n: 'LinkedIn UK', u: 'https://linkedin.com/jobs/uk', d: 'Best for tech'},
            {n: 'Indeed UK', u: 'https://indeed.co.uk', d: 'Wide range'},
            {n: 'Reed', u: 'https://reed.co.uk', d: 'UK focused'},
            {n: 'Glassdoor UK', u: 'https://glassdoor.co.uk', d: 'Reviews + salary'},
            {n: 'Otta', u: 'https://otta.com', d: 'Startup focused'}
        ],
        
        tips: [
            'Immigration Health Surcharge (IHS) is expensive but mandatory',
            'London salaries are 20-30% higher but cost of living makes up for it',
            'Consider Manchester, Bristol for better value',
            'Get National Insurance number immediately',
            'Open bank account with Monzo/Starling (no address needed initially)',
            'Council Tax is significant - budget for it',
            'Join Skilled Worker visa WhatsApp groups',
            'BRP card collection within 10 days of arrival',
            'Oyster card for London transport'
        ],
        
        interview: [
            'Technical interviews are thorough',
            'LeetCode practice helpful',
            'System design for senior roles',
            'Cultural fit questions common',
            'Visa sponsorship willingness varies',
            'Salary negotiation expected'
        ],
        
        network: [
            'London Tech Network',
            'Indians in UK (Facebook)',
            'AWS User Group London',
            'London DevOps Meetup',
            'Tech London Advocates'
        ]
    },

    // ==================== USA ====================
    USA: {
        visa_processing: '2-12 months',
        visa_cost: '₹2,00,000-4,00,000',
        tax_rate: '10-37% Federal + State',
        language: 'English',
        weather: 'Varies greatly by region',
        indian_population: '4.5 Million+',
        currency: 'USD (1 USD ≈ ₹83)',
        timezone: 'GMT-5 to GMT-8',
        flight_time: '15-20 hours',
        
        pros: [
            'Highest salaries in the world for tech',
            'Silicon Valley - heart of tech innovation',
            'Largest Indian diaspora community',
            'Career growth opportunities unmatched',
            'Top tech companies headquartered here',
            'Diverse culture and opportunities',
            'World-class universities',
            'English speaking',
            'Strong startup ecosystem',
            'Latest tech exposure'
        ],
        cons: [
            'H1B lottery system (25% chance)',
            'Green card wait of 50-100+ years for Indians',
            'No universal healthcare',
            'High cost in Bay Area, NYC',
            'Political visa policies uncertainty',
            'Work-life balance can be poor',
            'At-will employment (less job security)',
            'Gun violence concerns in some areas'
        ],
        
        best_cities: [
            {name: 'San Francisco Bay Area', why: 'Tech capital - highest salaries & opportunities'},
            {name: 'Seattle', why: 'Amazon, Microsoft - no state income tax'},
            {name: 'New York', why: 'Finance + tech, diverse'},
            {name: 'Austin', why: 'Growing tech hub, no state income tax'},
            {name: 'Boston', why: 'Biotech, universities, established'}
        ],
        
        lifestyle: {
            work_hours: 'Varies - can be intense in tech',
            weekend: 'Saturday-Sunday',
            dress_code: 'Very casual in tech',
            social_life: 'Varies by city - very diverse options',
            indian_community: 'Massive - established communities in most cities',
            food: 'Excellent Indian food in major cities'
        },
        
        expenses: {
            rent: {s: '₹1,50,000-4,00,000 (Bay Area)', f: '₹3,00,000-6,00,000'},
            food: {s: '₹40,000-70,000', f: '₹70,000-1,20,000'},
            transport: {s: '₹25,000-50,000', f: '₹40,000-80,000'},
            healthcare: {s: '₹20,000-40,000', f: '₹40,000-80,000'},
            utilities: {s: '₹15,000-30,000', f: '₹25,000-45,000'},
            entertainment: {s: '₹25,000-50,000', f: '₹45,000-80,000'},
            total: {s: '₹2,75,000-6,50,000', f: '₹5,00,000-10,00,000'}
        },
        
        initial: {
            visa: '₹2,00,000-4,00,000 (attorney + fees)',
            flight: '₹70,000-1,20,000',
            deposit: '₹4,00,000-8,00,000 (first+last+security)',
            ssn_setup: '₹50,000-1,00,000',
            car: '₹5,00,000-15,00,000 (needed in most cities)',
            total: '₹12,00,000-30,00,000'
        },
        
        salaries: {
            'Junior Developer (0-2y)': '₹80-1.2 Cr ($95-145K)',
            'Mid Developer (3-5y)': '₹1.2-1.8 Cr ($145-220K)',
            'Senior Developer (5-8y)': '₹1.6-2.5 Cr ($195-300K)',
            'Staff/Tech Lead (8-12y)': '₹2.2-3.5 Cr ($265-420K)',
            'Principal/Architect (12+y)': '₹3-5 Cr ($360-600K)',
            'Engineering Manager': '₹2.5-4 Cr ($300-480K)'
        },
        
        savings_potential: {
            junior: '₹25-40 LPA (30-35%)',
            mid: '₹40-65 LPA (35-40%)',
            senior: '₹60-1 Cr (40-45%)',
            lead: '₹90-1.5 Cr (45-50%)'
        },
        
        taxes: {
            income_tax: '10% to 37% Federal',
            state_tax: '0% (TX, WA, FL) to 13.3% (CA)',
            social_security: '6.2% on first $168,600',
            medicare: '1.45% (additional 0.9% above $200K)',
            notes: 'CA total: ~40-45%, TX/WA: ~30-35%. RSUs/stocks taxed as ordinary income.'
        },
        
        visas: [
            {n: 'H1B', d: 'Most common work visa - lottery based', t: '3-6 months', r: ['Bachelor\'s degree', 'Job offer in specialty occupation', 'Selected in lottery (25% odds)', 'Employer sponsorship']},
            {n: 'L1', d: 'Intracompany transfer', t: '2-3 months', r: ['1 year with same company abroad', 'Transfer to US office', 'Manager/Executive OR specialized knowledge']},
            {n: 'O1', d: 'Extraordinary ability', t: '2-4 months', r: ['Extraordinary achievements', 'Awards/recognition/patents', 'Expert endorsements']}
        ],
        
        agencies: [
            {n: 'Robert Half', s: 'Tech recruitment', w: 'https://roberthalf.com', verified: true},
            {n: 'Hired', s: 'Tech talent marketplace', w: 'https://hired.com', verified: true},
            {n: 'Dice', s: 'Tech focused', w: 'https://dice.com', verified: true}
        ],
        
        portals: [
            {n: 'LinkedIn', u: 'https://linkedin.com/jobs', d: 'Essential for US tech'},
            {n: 'levels.fyi', u: 'https://levels.fyi', d: 'Salary data + jobs'},
            {n: 'Glassdoor', u: 'https://glassdoor.com', d: 'Reviews + salary'},
            {n: 'Indeed', u: 'https://indeed.com', d: 'Wide range'},
            {n: 'Blind', u: 'https://teamblind.com', d: 'Insider info (anonymous)'}
        ],
        
        tips: [
            'H1B lottery opens in March each year - apply early',
            'Consider L1 if your company has US presence',
            'Masters in US improves H1B odds (20% extra cap)',
            'Start Green Card process immediately after joining',
            'Texas, Washington have no state income tax',
            'Bay Area salaries are 30-50% higher than national average',
            'Build US credit history immediately',
            'Join Blind for honest company insights',
            'Negotiate heavily - TC can vary widely for same role'
        ],
        
        interview: [
            'LeetCode is essential - practice 200+ problems',
            'System Design crucial for senior roles',
            'Behavioral rounds (STAR method)',
            'Multiple rounds: Phone screen → Technical → Onsite',
            'Team matching rounds at some companies',
            'Negotiate hard - first offer is rarely final'
        ],
        
        network: [
            'TiE Silicon Valley',
            'IndUS Entrepreneurs',
            'AAPI in Tech',
            'Women in Tech communities',
            'SF Bay Area Tech groups'
        ]
    },

    // ==================== NETHERLANDS ====================
    Netherlands: {
        visa_processing: '4-8 weeks',
        visa_cost: '₹25,000-40,000',
        tax_rate: '36.93-49.5%',
        language: 'Dutch (English widely spoken)',
        weather: 'Temperate - Mild summers (20°C), cold winters (2-6°C)',
        indian_population: '50,000+',
        currency: 'EUR (1 EUR ≈ ₹90)',
        timezone: 'GMT+1 (4.5hrs behind IST)',
        flight_time: '8-9 hours',
        
        pros: [
            '30% Tax Ruling - massive tax benefit for 5 years',
            'English widely spoken in workplace and daily life',
            'EU access - work anywhere in Schengen',
            'Great work-life balance',
            'Bicycle-friendly cities',
            'Progressive, open society',
            'High quality of life',
            'Good public transport',
            'Tech hub with many multinationals',
            'Direct flights to India'
        ],
        cons: [
            'Housing crisis - very hard to find apartments',
            'High base tax rate (without 30% ruling)',
            'Rainy, grey weather',
            'Small country - limited cities',
            'Dutch bureaucracy can be slow',
            'Language barrier for some daily activities',
            'Expensive compared to Eastern Europe'
        ],
        
        best_cities: [
            {name: 'Amsterdam', why: 'Tech hub, most opportunities, very expensive'},
            {name: 'Eindhoven', why: 'ASML, Philips, High Tech Campus, more affordable'},
            {name: 'Rotterdam', why: 'Second largest, port city, cheaper'},
            {name: 'The Hague', why: 'Government, international orgs'},
            {name: 'Utrecht', why: 'Growing tech scene, central location'}
        ],
        
        lifestyle: {
            work_hours: '9 AM - 5 PM (Work-life balance is excellent)',
            weekend: 'Saturday-Sunday',
            dress_code: 'Very casual',
            social_life: 'Cafes, cycling, canal-side activities',
            indian_community: 'Growing - temples in major cities',
            food: 'Indian restaurants available, some grocery stores'
        },
        
        expenses: {
            rent: {s: '₹80,000-1,80,000', f: '₹1,20,000-2,50,000'},
            food: {s: '₹25,000-40,000', f: '₹45,000-70,000'},
            transport: {s: '₹6,000-12,000', f: '₹10,000-18,000'},
            utilities: {s: '₹12,000-22,000', f: '₹20,000-35,000'},
            healthcare: {s: '₹10,000-15,000', f: '₹20,000-30,000'},
            entertainment: {s: '₹18,000-30,000', f: '₹30,000-50,000'},
            total: {s: '₹1,50,000-3,00,000', f: '₹2,45,000-4,50,000'}
        },
        
        initial: {
            visa: '₹25,000-40,000',
            flight: '₹45,000-70,000',
            deposit: '₹2,50,000-5,00,000 (2-3 months rent)',
            furniture: '₹80,000-1,50,000',
            registration: '₹15,000-25,000',
            total: '₹4,15,000-7,85,000'
        },
        
        salaries: {
            'Junior Developer (0-2y)': '₹35-50 LPA (€38-55K)',
            'Mid Developer (3-5y)': '₹55-75 LPA (€60-83K)',
            'Senior Developer (5-8y)': '₹70-1 Cr (€78-110K)',
            'Tech Lead (8-12y)': '₹85-1.2 Cr (€95-130K)',
            'Architect/Principal (12+y)': '₹1-1.5 Cr (€110-165K)',
            'Engineering Manager': '₹90-1.3 Cr (€100-145K)'
        },
        
        savings_potential: {
            junior: '₹15-22 LPA (with 30% ruling: 45%)',
            mid: '₹25-35 LPA (with 30% ruling: 48%)',
            senior: '₹35-50 LPA (with 30% ruling: 50%)',
            lead: '₹45-60 LPA (with 30% ruling: 52%)'
        },
        
        taxes: {
            income_tax: '36.93% (up to €73K), 49.5% (above)',
            thirty_percent_ruling: '30% of salary tax-free for 5 years!',
            social_security: 'Included in income tax',
            notes: 'With 30% ruling, effective tax ~25-30%. One of the best tax benefits for expats globally.'
        },
        
        visas: [
            {n: 'Highly Skilled Migrant', d: 'Most common for tech workers', t: '2-4 weeks', r: ['Job offer from recognized sponsor', 'Salary €46K+ (or €36K if under 30)', 'Degree not strictly required']},
            {n: 'EU Blue Card', d: 'Alternative to HSM visa', t: '4-8 weeks', r: ['Job offer €60K+', 'Recognized degree', 'EU-wide benefits']},
            {n: 'Orientation Visa', d: 'Search for work after graduation', t: '2-4 weeks', r: ['Graduated from top 200 university in past 3 years']}
        ],
        
        agencies: [
            {n: 'Undutchables', s: 'Expat-focused recruitment', w: 'https://undutchables.nl', verified: true},
            {n: 'Hays Netherlands', s: 'Tech recruitment', w: 'https://hays.nl', verified: true},
            {n: 'Adams', s: 'IT recruitment', w: 'https://adams.nl', verified: true}
        ],
        
        portals: [
            {n: 'LinkedIn NL', u: 'https://linkedin.com/jobs/netherlands', d: 'Best for tech'},
            {n: 'Indeed NL', u: 'https://indeed.nl', d: 'Wide range'},
            {n: 'Glassdoor NL', u: 'https://glassdoor.nl', d: 'Reviews + salary'},
            {n: 'Together Abroad', u: 'https://togetherabroad.nl', d: 'Expat-focused'}
        ],
        
        tips: [
            '30% Ruling is a game-changer - ensure eligibility',
            'Start apartment search months in advance',
            'Get BSN number immediately - needed for everything',
            'Buy a bicycle - essential Dutch experience',
            'Learn basic Dutch - appreciated by locals',
            'Join expat Facebook groups for housing leads',
            'DigiD is like Aadhaar - needed for government services',
            'Open ING/ABN AMRO bank account',
            'Amsterdam South/East preferred by Indians'
        ],
        
        interview: [
            'Technical interviews are thorough but less LeetCode-heavy',
            'Cultural fit is very important',
            'Direct communication style expected',
            'Work-life balance discussions are normal',
            'Salary negotiation expected',
            'Ask about 30% ruling eligibility'
        ],
        
        network: [
            'Amsterdam Tech Meetup',
            'Indians in Netherlands (Facebook)',
            'AWS User Group Amsterdam',
            'Python Amsterdam',
            'Dutch Startup Association'
        ]
    },

    // ==================== NEW ZEALAND ====================
    NewZealand: {
        visa_processing: '4-8 weeks',
        visa_cost: '₹30,000-50,000',
        tax_rate: '10.5-39% Progressive',
        language: 'English',
        weather: 'Temperate - Mild all year (10-25°C)',
        indian_population: '250,000+ (5% of population)',
        currency: 'NZD (1 NZD ≈ ₹51)',
        timezone: 'GMT+12 (6.5hrs ahead of IST)',
        flight_time: '13-15 hours',
        
        pros: [
            'Best work-life balance in the world',
            'Fast track to PR (2 years)',
            'Beautiful natural environment',
            'Very safe country',
            'Good healthcare system',
            'Friendly, welcoming culture',
            'English speaking',
            'Quality of life focused',
            'Easy citizenship after PR',
            'Close to Australia'
        ],
        cons: [
            'Lower salaries than Australia/US',
            'Remote location - far from everywhere',
            'Small job market',
            'High cost of living',
            'Limited career growth options',
            'Housing affordability crisis',
            'Earthquakes in some areas',
            'Limited public transport outside Auckland'
        ],
        
        best_cities: [
            {name: 'Auckland', why: 'Largest city, most jobs, diverse'},
            {name: 'Wellington', why: 'Capital, government & tech jobs'},
            {name: 'Christchurch', why: 'Growing tech, cheaper, South Island'}
        ],
        
        expenses: {
            rent: {s: '₹70,000-1,30,000', f: '₹1,10,000-2,00,000'},
            food: {s: '₹25,000-40,000', f: '₹45,000-70,000'},
            transport: {s: '₹10,000-20,000', f: '₹15,000-30,000'},
            utilities: {s: '₹10,000-18,000', f: '₹18,000-28,000'},
            healthcare: {s: '₹0-8,000', f: '₹0-15,000'},
            total: {s: '₹1,15,000-2,15,000', f: '₹1,90,000-3,45,000'}
        },
        
        salaries: {
            'Junior Developer (0-2y)': '₹35-45 LPA (NZD 55-70K)',
            'Mid Developer (3-5y)': '₹50-70 LPA (NZD 80-110K)',
            'Senior Developer (5-8y)': '₹65-90 LPA (NZD 105-145K)',
            'Tech Lead (8-12y)': '₹80-1.1 Cr (NZD 130-175K)',
            'Engineering Manager': '₹75-1 Cr (NZD 120-160K)'
        },
        
        visas: [
            {n: 'Accredited Employer Work Visa', d: 'For roles with accredited employers', t: '4-8 weeks', r: ['Job offer from accredited employer', 'Meet median wage threshold', 'Relevant experience']},
            {n: 'Skilled Migrant Category', d: 'Points-based resident visa', t: '3-6 months', r: ['160+ points', 'Job or job offer', 'Skills on shortage lists', 'Age under 56']}
        ],
        
        tips: [
            'Green List occupations have faster PR pathway',
            'Auckland has most jobs but most expensive',
            'Consider Wellington or Christchurch for better value',
            'Join Skilled Migrant pool even before arriving',
            'Summer is December-February (opposite seasons!)',
            'Kiwi work culture is very relaxed'
        ]
    },

    // ==================== SWITZERLAND ====================
    Switzerland: {
        visa_processing: '6-12 weeks',
        visa_cost: '₹15,000-30,000',
        tax_rate: '0-11.5% Federal + Canton',
        language: 'German, French, Italian, English',
        weather: 'Alpine - Cold winters, mild summers',
        indian_population: '20,000+',
        currency: 'CHF (1 CHF ≈ ₹95)',
        timezone: 'GMT+1 (4.5hrs behind IST)',
        flight_time: '8-9 hours',
        
        pros: [
            'Highest salaries in Europe',
            'Low taxes compared to other EU countries',
            'Neutral, stable country',
            'Excellent quality of life',
            'Beautiful Alpine scenery',
            'Strong banking sector',
            'Central European location',
            'Efficient public transport'
        ],
        cons: [
            'Extremely expensive everything',
            'Not in EU (but has agreements)',
            'Strict quota system for non-EU',
            'Difficult to integrate socially',
            'PR takes 10 years',
            'Need to learn local language',
            'Smaller job market than Germany/UK'
        ],
        
        best_cities: [
            {name: 'Zurich', why: 'Financial hub, most tech jobs'},
            {name: 'Geneva', why: 'International orgs, UN'},
            {name: 'Basel', why: 'Pharma companies'},
            {name: 'Bern', why: 'Capital, government jobs'}
        ],
        
        expenses: {
            rent: {s: '₹1,50,000-2,80,000', f: '₹2,50,000-4,50,000'},
            food: {s: '₹50,000-80,000', f: '₹90,000-1,40,000'},
            transport: {s: '₹12,000-20,000', f: '₹20,000-35,000'},
            healthcare: {s: '₹25,000-40,000', f: '₹50,000-80,000'},
            total: {s: '₹2,40,000-4,20,000', f: '₹4,10,000-7,00,000'}
        },
        
        salaries: {
            'Junior Developer (0-2y)': '₹60-85 LPA (CHF 65-90K)',
            'Mid Developer (3-5y)': '₹90-1.3 Cr (CHF 95-135K)',
            'Senior Developer (5-8y)': '₹1.2-1.7 Cr (CHF 125-180K)',
            'Tech Lead (8-12y)': '₹1.5-2.2 Cr (CHF 160-230K)',
            'Engineering Manager': '₹1.4-2 Cr (CHF 150-210K)'
        },
        
        tips: [
            'Switzerland is NOT in EU - separate visa process',
            'Learn German (Zurich) or French (Geneva)',
            'Healthcare is mandatory and expensive',
            'Zurich has most tech opportunities',
            'Build network before applying',
            'Consider cross-border work from France/Germany'
        ]
    },

    // ==================== SWEDEN ====================
    Sweden: {
        visa_processing: '4-8 weeks',
        visa_cost: '₹15,000-25,000',
        tax_rate: '32-52% (including municipal)',
        language: 'Swedish (English widely spoken)',
        weather: 'Cold - Very cold winters (-10°C), mild summers (20°C)',
        indian_population: '30,000+',
        currency: 'SEK (1 SEK ≈ ₹7.8)',
        timezone: 'GMT+1 (4.5hrs behind IST)',
        flight_time: '8-9 hours',
        
        pros: [
            'Innovation hub (Spotify, Klarna, IKEA)',
            'Excellent work-life balance',
            'Very high quality of life',
            'Parental leave is among best globally',
            'Free education and healthcare',
            'EU access',
            'English widely spoken',
            'Progressive society'
        ],
        cons: [
            'Very high taxes',
            'Cold, dark winters (seasonal depression)',
            'Housing shortage in Stockholm',
            'Swedish needed for permanent stay',
            'Reserved culture initially',
            'Smaller job market'
        ],
        
        best_cities: [
            {name: 'Stockholm', why: 'Tech hub, Spotify HQ'},
            {name: 'Gothenburg', why: 'Volvo, automotive tech'},
            {name: 'Malmö', why: 'Growing tech, close to Copenhagen'}
        ],
        
        salaries: {
            'Junior Developer (0-2y)': '₹30-45 LPA (SEK 35-50K/mo)',
            'Mid Developer (3-5y)': '₹45-65 LPA (SEK 50-75K/mo)',
            'Senior Developer (5-8y)': '₹60-90 LPA (SEK 70-100K/mo)',
            'Tech Lead (8-12y)': '₹75-1.1 Cr (SEK 85-120K/mo)',
            'Engineering Manager': '₹70-1 Cr (SEK 80-115K/mo)'
        },
        
        tips: [
            'Fika (coffee break) is a sacred Swedish tradition',
            'Learn basic Swedish - helps with integration',
            'Personal number (personnummer) essential for everything',
            'Stockholm has most tech jobs',
            'Join tech meetups - Swedes open up there',
            'Winters are tough - prepare mentally'
        ]
    },

    // ==================== IRELAND ====================
    Ireland: {
        visa_processing: '6-12 weeks',
        visa_cost: '₹25,000-40,000',
        tax_rate: '20-40%',
        language: 'English, Irish',
        weather: 'Mild, rainy - Similar to UK',
        indian_population: '50,000+',
        currency: 'EUR (1 EUR ≈ ₹90)',
        timezone: 'GMT (5.5hrs behind IST)',
        flight_time: '9-10 hours',
        
        pros: [
            'EU headquarters of Google, Meta, Apple, LinkedIn',
            'English speaking in EU',
            'Fast growing tech sector',
            'Friendly culture',
            'EU access',
            'Good salaries',
            'Path to citizenship in 5 years',
            'Strong Indian community'
        ],
        cons: [
            'Housing crisis is severe',
            'High rent in Dublin',
            'Rainy weather most of the year',
            'Small country, limited cities',
            'High cost of living',
            'Limited public transport outside Dublin'
        ],
        
        best_cities: [
            {name: 'Dublin', why: 'Tech hub, all major companies, expensive'},
            {name: 'Cork', why: 'Apple, second largest city, cheaper'},
            {name: 'Galway', why: 'Tech growing, west coast'}
        ],
        
        salaries: {
            'Junior Developer (0-2y)': '₹35-50 LPA (€40-55K)',
            'Mid Developer (3-5y)': '₹55-80 LPA (€60-90K)',
            'Senior Developer (5-8y)': '₹75-1.1 Cr (€85-120K)',
            'Tech Lead (8-12y)': '₹90-1.4 Cr (€100-155K)',
            'Engineering Manager': '₹85-1.3 Cr (€95-140K)'
        },
        
        tips: [
            'Dublin is like a small tech city - most companies in walking distance',
            'Start housing search 2-3 months before arrival',
            'Critical Skills Permit gives fastest path to residency',
            'Irish tech scene is very networked - attend meetups',
            'Cork is increasingly popular alternative to Dublin',
            'PPS number (like PAN) needed for everything'
        ]
    },

    // ==================== JAPAN ====================
    Japan: {
        visa_processing: '4-8 weeks',
        visa_cost: '₹5,000-15,000',
        tax_rate: '5-45% Progressive',
        language: 'Japanese (JLPT N2/N3 preferred)',
        weather: 'Four seasons - Hot summers, cold winters',
        indian_population: '45,000+',
        currency: 'JPY (1 JPY ≈ ₹0.56)',
        timezone: 'GMT+9 (3.5hrs ahead of IST)',
        flight_time: '8-10 hours',
        monthly_expense_single: '₹1.3-1.5 LPA (modest lifestyle including rent, utilities, transport, food)',
        
        pros: [
            'Unique cultural experience',
            'Extremely safe country',
            'Excellent public transport',
            'Tech innovation hub - Japan is actively hiring foreign talent',
            'Low crime rate',
            'High quality products/services',
            'Anime, gaming, culture',
            'Beautiful four seasons',
            'Workforce shortage = More opportunities for foreigners'
        ],
        cons: [
            'Japanese language essential for most jobs (JLPT N2/N3)',
            'Work culture can be intense',
            'Small apartments, expensive cities',
            'PR takes 10 years',
            'Cultural adjustment significant',
            'Earthquakes and natural disasters',
            'Limited English in daily life'
        ],
        
        best_cities: [
            {name: 'Tokyo', why: 'Largest tech hub, most opportunities'},
            {name: 'Osaka', why: 'Second largest, more affordable'},
            {name: 'Fukuoka', why: 'Startup hub, cheaper, foreigner-friendly'}
        ],
        
        salaries: {
            'Junior Developer (0-2y)': '₹28-40 LPA (¥4-5.5M)',
            'Mid Developer (3-5y)': '₹40-60 LPA (¥5.5-8M)',
            'Senior Developer (5-8y)': '₹55-85 LPA (¥7.5-11M)',
            'Tech Lead (8-12y)': '₹70-1.1 Cr (¥9.5-15M)',
            'Engineering Manager': '₹65-1 Cr (¥9-14M)'
        },
        
        portals: [
            {n: 'Daijob', u: 'https://www.daijob.com/en/', d: 'Best for Multilingual/Bilingual IT & Business roles (est. 1998)'},
            {n: 'Japan Dev', u: 'https://japan-dev.com/', d: 'Curated engineering roles with salary info, English-friendly teams'},
            {n: 'Yaaay', u: 'https://yaaay.jp/', d: 'Tech-focused for foreign engineers, includes Scout feature'},
            {n: 'GaijinPot Jobs', u: 'https://jobs.gaijinpot.com/', d: 'Large portal covering IT, teaching, service roles'},
            {n: 'Jobs in Japan', u: 'https://jobsinjapan.com/', d: 'Wide range with visa sponsorship filters'},
            {n: 'Mintoku Work', u: 'https://mintoku.com/en/work', d: 'Focuses on foreign residents with housing & visa support'},
            {n: 'Guidable Jobs', u: 'https://jobs.guidable.co/en/', d: 'Specializes in nursing and caregiving jobs'},
            {n: 'EPIC JAPAN JOBS', u: 'https://www.epicjapanjobs.com/', d: 'Healthcare and skilled roles for foreigners'}
        ],
        
        tips: [
            'Learn Japanese - at least N3/N2 level for most jobs',
            'Filter by Visa Support, English OK, or Foreign nationals welcome',
            'Prepare English resume AND Japanese-style resume (rirekisho)',
            'Some English-only positions exist but limited',
            'Work culture is changing but still demanding',
            'Tokyo is expensive but has most opportunities (₹1.3-1.5L/month needed)',
            'Join tech meetups - good for networking',
            'Gaijin (foreigner) friendly companies exist - target them',
            'Clarify visa sponsorship, relocation, training in writing',
            'Avoid paying recruitment agents upfront'
        ]
    },

    // ==================== QATAR ====================
    Qatar: {
        visa_processing: '2-4 weeks',
        visa_cost: '₹5,000-15,000',
        tax_rate: '0% Income Tax',
        language: 'Arabic, English widely used',
        weather: 'Desert - Very hot summers (45°C+), mild winters',
        indian_population: '700,000+',
        currency: 'QAR (1 QAR ≈ ₹22.8)',
        timezone: 'GMT+3 (2.5hrs behind IST)',
        flight_time: '4 hours',
        
        pros: [
            '0% Income Tax',
            'Growing economy (post FIFA World Cup)',
            'Large Indian community',
            'Close to India',
            'Modern infrastructure',
            'High savings potential',
            'Safe country',
            'Tax-free remittances'
        ],
        cons: [
            'Extreme summer heat',
            'Limited social life options',
            'Alcohol restrictions',
            'No PR pathway',
            'Visa tied to employer',
            'Small country',
            'Conservative culture'
        ],
        
        best_cities: [
            {name: 'Doha', why: 'Capital city - all jobs here'}
        ],
        
        salaries: {
            'Junior Developer (0-2y)': '₹7-11 LPA (QAR 8-13K/mo)',
            'Mid Developer (3-5y)': '₹12-20 LPA (QAR 14-23K/mo)',
            'Senior Developer (5-8y)': '₹18-30 LPA (QAR 20-35K/mo)',
            'Tech Lead (8-12y)': '₹25-40 LPA (QAR 30-48K/mo)',
            'Engineering Manager': '₹22-35 LPA (QAR 26-42K/mo)'
        },
        
        tips: [
            'Similar to UAE but smaller market',
            'World Cup infrastructure boosted tech sector',
            'Negotiate housing allowance',
            'Join Indian community groups',
            'Save aggressively - no tax advantage is huge',
            'Consider it as stepping stone'
        ]
    },

    // ==================== SAUDI ARABIA ====================
    SaudiArabia: {
        visa_processing: '2-4 weeks',
        visa_cost: '₹10,000-25,000',
        tax_rate: '0% Income Tax',
        language: 'Arabic, English in tech',
        weather: 'Desert - Extreme summers (50°C), mild winters',
        indian_population: '2.5 Million+',
        currency: 'SAR (1 SAR ≈ ₹22.1)',
        timezone: 'GMT+3 (2.5hrs behind IST)',
        flight_time: '4-5 hours',
        
        pros: [
            '0% Income Tax',
            'Vision 2030 creating massive tech investment',
            'Huge Indian community',
            'Close to India',
            'High savings potential',
            'NEOM and other mega projects',
            'Premium Residency option (like Golden Visa)',
            'Growing tech sector'
        ],
        cons: [
            'Extreme summer heat',
            'Conservative culture',
            'Alcohol prohibited',
            'Social restrictions (improving)',
            'Visa tied to employer (Kafala system reforming)',
            'Gender segregation (reducing)',
            'Weekend is Friday-Saturday'
        ],
        
        best_cities: [
            {name: 'Riyadh', why: 'Capital, most tech opportunities'},
            {name: 'Jeddah', why: 'More liberal, coastal city'},
            {name: 'NEOM', why: 'Futuristic city project - high paying'}
        ],
        
        salaries: {
            'Junior Developer (0-2y)': '₹8-13 LPA (SAR 9-15K/mo)',
            'Mid Developer (3-5y)': '₹14-22 LPA (SAR 16-26K/mo)',
            'Senior Developer (5-8y)': '₹20-35 LPA (SAR 24-42K/mo)',
            'Tech Lead (8-12y)': '₹30-50 LPA (SAR 36-60K/mo)',
            'Engineering Manager': '₹28-45 LPA (SAR 33-54K/mo)'
        },
        
        tips: [
            'Vision 2030 is creating massive opportunities',
            'NEOM project paying premium salaries',
            'Culture is liberalizing rapidly',
            'Women can drive and work freely now',
            'Entertainment sector opening up',
            'Save 60-70% of salary easily',
            'Consider Premium Residency for long-term stay'
        ]
    }
};

// Export for use in abroad.html and country-detail.html
if (typeof window !== 'undefined') {
    window.COMPREHENSIVE_COUNTRY_DATA = COMPREHENSIVE_COUNTRY_DATA;
    window.COUNTRY_DATA = COMPREHENSIVE_COUNTRY_DATA;  // Alias for compatibility
}
