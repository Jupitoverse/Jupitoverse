// Enhanced Country Migration Data - Part 4 (Asia Pacific & Middle East)
// Japan, South Korea, Hong Kong, Saudi Arabia, Qatar, Kuwait, Bahrain, Oman

const ENHANCED_COUNTRY_DATA_4 = {

    // ==================== JAPAN ====================
    Japan: {
        basic_info: {
            official_name: 'Japan',
            capital: 'Tokyo',
            tech_hubs: 'Tokyo, Osaka, Fukuoka, Nagoya',
            currency: 'JPY (Japanese Yen)',
            exchange_rate: '1 JPY ≈ ₹0.56 (weak yen = good for Indians!)',
            timezone: 'GMT+9 (3.5hrs ahead of IST)',
            flight_time: '8-10 hours',
            language: 'Japanese (Limited English)',
            indian_population: '45,000+',
            visa_processing: '2-4 weeks',
            visa_cost: '¥3,000 (₹1,700)',
            tax_rate: '5-45% Progressive'
        },

        why_indians_migrate: [
            'Unique cultural experience',
            'Very safe country (#1 globally)',
            'Amazing technology and innovation',
            'Weak yen = great for savings',
            'HSP (Highly Skilled Professional) visa',
            'Japanese companies hiring globally',
            'Excellent public transport',
            'Clean and organized',
            'Work culture improving',
            'Anime, gaming, food culture'
        ],

        step_by_step_migration: [
            {step: 1, title: 'Get Job Offer', details: 'Apply via LinkedIn, TokyoDev, Japan Dev, Daijob. Need employer sponsorship.', duration: '2-6 months'},
            {step: 2, title: 'COE Application', details: 'Employer applies for Certificate of Eligibility at immigration.', duration: '1-3 months'},
            {step: 3, title: 'Visa Application', details: 'Submit COE at Japanese embassy in India.', duration: '1 week'},
            {step: 4, title: 'Fly to Japan', details: 'Enter within 3 months of visa issue.', duration: '1 day'},
            {step: 5, title: 'City Registration', details: 'Register at local ward office (Ku-yakusho).', duration: '1 day'},
            {step: 6, title: 'Residence Card', details: 'Get Zairyu Card at airport or immigration.', duration: '1 day'},
            {step: 7, title: 'Bank Account', details: 'Shinsei, Sony Bank, or post office. Need residence card.', duration: '1-2 weeks'},
            {step: 8, title: 'Phone SIM', details: 'Rakuten, LINEMO, ahamo. Need residence card.', duration: '1 day'},
            {step: 9, title: 'Health Insurance', details: 'Shakai Hoken through employer or National Health Insurance.', duration: 'Automatic'}
        ],

        essential_apps: {
            translation: ['Google Translate', 'DeepL', 'Papago'],
            transport: ['Suica/Pasmo', 'Google Maps', 'Yahoo Transit Japan', 'Japan Rail Pass'],
            food: ['UberEats Japan', 'Demae-can', 'Tabelog', 'Gurunavi'],
            housing: ['Suumo', 'Homes.co.jp', 'Real Estate Japan', 'GaijinPot Apartments'],
            social: ['Line', 'Discord', 'Meetup', 'Tokyo Internationals'],
            banking: ['PayPay', 'Wise', 'Shinsei Bank'],
            shopping: ['Amazon Japan', 'Rakuten', 'Yahoo Shopping']
        },

        essential_websites: {
            job_portals: ['tokyodev.com', 'japandev.com', 'daijob.com', 'gaijinpot.com', 'linkedin.com'],
            housing: ['suumo.jp', 'homes.co.jp', 'realestate.co.jp', 'gaijinpot.com/apartments'],
            community: ['reddit.com/r/japanlife', 'tokyocheapo.com', 'gaijinpot.com']
        },

        language_requirement: {
            for_work: 'N2-N1 for most jobs, some English-only positions exist',
            for_daily_life: 'N3 minimum recommended',
            tips: [
                'Start learning before arrival (JLPT prep)',
                'English-only jobs are limited but growing',
                'IT companies more English-friendly',
                'Learn Hiragana, Katakana at minimum'
            ]
        },

        top_hiring_companies: {
            english_friendly: ['Amazon Japan', 'Google Japan', 'Microsoft Japan', 'Mercari', 'Indeed Japan', 'Rakuten'],
            japanese_tech: ['Sony', 'Nintendo', 'LINE', 'CyberAgent', 'DeNA', 'GREE'],
            automotive: ['Toyota', 'Honda', 'Nissan', 'Denso'],
            consulting: ['McKinsey', 'BCG', 'Accenture Japan']
        },

        salaries: {
            'Junior Developer (0-2y)': {jpy: '¥4-5.5M/year', inr: '₹22-31 LPA'},
            'Mid Developer (3-5y)': {jpy: '¥6-8M/year', inr: '₹34-45 LPA'},
            'Senior Developer (5-8y)': {jpy: '¥8-12M/year', inr: '₹45-67 LPA'},
            'Tech Lead (8-12y)': {jpy: '¥12-18M/year', inr: '₹67-100 LPA'},
            'Note': 'Foreign tech companies pay 30-50% more than Japanese companies'
        },

        monthly_expenses: {
            tokyo: {
                rent: '¥100,000-180,000 (₹56,000-1,00,000)',
                food: '¥50,000-80,000 (₹28,000-45,000)',
                transport: '¥10,000-20,000 (₹5,600-11,200)',
                phone: '¥3,000-5,000',
                total: '¥180,000-300,000 (₹1,00,000-1,68,000)'
            }
        },

        initial_setup_cost: {
            visa: '¥3,000 (₹1,700)',
            flight: '₹40,000-70,000',
            key_money: '¥200,000-400,000 (non-refundable)',
            deposit: '¥100,000-200,000',
            first_month_rent: '¥100,000-180,000',
            furniture: '¥100,000-300,000',
            total: '₹5,00,000-10,00,000'
        },

        visa_types: [
            {name: 'Engineer/Humanities Visa', duration: '1-5 years', requirements: ['Job offer', 'Degree'], path_to_pr: '10 years'},
            {name: 'HSP (Highly Skilled Professional)', duration: '5 years', requirements: ['70+ points', 'Advanced degree', 'High salary'], path_to_pr: '1-3 years!'},
            {name: 'Startup Visa', duration: '6 months-1 year', requirements: ['Business plan', 'Funding'], path_to_pr: 'Via Business Manager visa'}
        ],

        hsp_points_system: {
            what: 'Points for education, experience, salary, Japanese ability',
            benefits: '80+ points = PR in 1 year, 70+ points = PR in 3 years',
            calculate: 'immi-moj.go.jp for calculator'
        },

        pros: ['Extremely safe', 'Excellent public transport', 'Clean environment', 'Unique culture', 'Weak yen = savings', 'HSP visa fast track to PR'],
        cons: ['Language barrier', 'Demanding work culture', 'Small apartments', 'Complex visa system', 'Cultural adjustment', 'Earthquakes'],

        weather: {
            summer: '25-35°C (humid)',
            winter: '0-10°C (Tokyo), colder up north',
            seasons: 'Beautiful cherry blossoms (spring), autumn foliage'
        },

        best_cities: [
            {name: 'Tokyo', why: 'Most jobs, highest salaries, most English-friendly'},
            {name: 'Osaka', why: 'Second largest, food city, more relaxed'},
            {name: 'Fukuoka', why: 'Startup hub, cheaper, international community'}
        ]
    },

    // ==================== SOUTH KOREA ====================
    SouthKorea: {
        basic_info: {
            official_name: 'Republic of Korea',
            capital: 'Seoul',
            tech_hubs: 'Seoul, Pangyo (Korean Silicon Valley)',
            currency: 'KRW (Korean Won)',
            exchange_rate: '1 KRW ≈ ₹0.063',
            timezone: 'GMT+9 (3.5hrs ahead of IST)',
            flight_time: '7-8 hours',
            language: 'Korean (English limited)',
            indian_population: '15,000+',
            visa_processing: '2-4 weeks',
            visa_cost: '₹5,000-7,000',
            tax_rate: '6-45%'
        },

        why_indians_migrate: [
            'Samsung, LG, Hyundai - tech giants',
            'K-culture boom (K-pop, K-drama)',
            'High salaries for senior roles',
            'Advanced technology country',
            'Fast internet, tech infrastructure',
            'Safe country',
            'Affordable food and transport',
            'Growing startup scene',
            'Government promoting foreign talent',
            'Close to India'
        ],

        top_hiring_companies: {
            tech: ['Samsung', 'LG', 'Naver', 'Kakao', 'Coupang'],
            global: ['Google Korea', 'Amazon Korea', 'Microsoft Korea'],
            gaming: ['Nexon', 'NCSoft', 'Krafton', 'Smilegate']
        },

        salaries: {
            'Junior Developer (0-2y)': {krw: '₩40-55M/year', inr: '₹25-35 LPA'},
            'Mid Developer (3-5y)': {krw: '₩60-85M/year', inr: '₹38-53 LPA'},
            'Senior Developer (5-8y)': {krw: '₩85-120M/year', inr: '₹53-75 LPA'},
            'Tech Lead': {krw: '₩110-160M/year', inr: '₹69-100 LPA'}
        },

        monthly_expenses: {
            seoul: {
                rent: '₩800,000-1,500,000 (₹50,000-94,000)',
                food: '₩400,000-600,000 (₹25,000-38,000)',
                transport: '₩50,000-100,000',
                total: '₩1,500,000-2,500,000 (₹94,000-1,56,000)'
            }
        },

        visa_types: [
            {name: 'E-7 (Professional)', duration: '1-3 years', requirements: ['Job offer', 'Degree', 'Experience'], path_to_pr: '5+ years'},
            {name: 'F-2-7 (Points)', duration: 'Quasi-resident', requirements: ['80+ points'], path_to_pr: 'Direct path'},
            {name: 'D-10 (Job Seeking)', duration: '2 years', requirements: ['Bachelor\'s', 'Looking for job'], path_to_pr: 'Via employment visa'}
        ],

        pros: ['Tech giants opportunities', 'Safe country', 'Advanced infrastructure', 'Good food', 'K-culture', 'Close to India'],
        cons: ['Korean language essential', 'Intense work culture', 'Difficult to integrate', 'Cold winters', 'Limited English outside tech']
    },

    // ==================== HONG KONG ====================
    HongKong: {
        basic_info: {
            official_name: 'Hong Kong Special Administrative Region',
            capital: 'Hong Kong (city-state)',
            currency: 'HKD (Hong Kong Dollar)',
            exchange_rate: '1 HKD ≈ ₹10.6',
            timezone: 'GMT+8 (2.5hrs ahead of IST)',
            flight_time: '6-7 hours',
            language: 'Cantonese, English, Mandarin',
            indian_population: '75,000+',
            visa_processing: '4-8 weeks',
            visa_cost: 'HKD 230 (₹2,400)',
            tax_rate: '2-17% (low!)'
        },

        why_indians_migrate: [
            'Very low taxes (max 17%)',
            'Financial hub of Asia',
            'English widely used',
            'Close to India (6 hours)',
            'Large Indian community',
            'High salaries',
            'International environment',
            'Gateway to China market',
            'No capital gains tax',
            'Banking and finance opportunities'
        ],

        top_hiring_companies: {
            banks: ['HSBC', 'Standard Chartered', 'JP Morgan', 'Goldman Sachs', 'Citi'],
            tech: ['Google', 'Microsoft', 'Alibaba', 'Tencent', 'ByteDance'],
            fintech: ['Wise', 'Revolut', 'Airwallex', 'FTX (was)']
        },

        salaries: {
            'Junior Developer (0-2y)': {hkd: 'HKD 25,000-35,000/mo', inr: '₹32-45 LPA'},
            'Mid Developer (3-5y)': {hkd: 'HKD 45,000-65,000/mo', inr: '₹57-82 LPA'},
            'Senior Developer (5-8y)': {hkd: 'HKD 70,000-100,000/mo', inr: '₹89-127 LPA'},
            'Tech Lead': {hkd: 'HKD 90,000-140,000/mo', inr: '₹114-178 LPA'}
        },

        monthly_expenses: {
            hk: {
                rent: 'HKD 15,000-30,000 (₹1,59,000-3,18,000)',
                food: 'HKD 5,000-10,000 (₹53,000-1,06,000)',
                transport: 'HKD 1,000-2,000',
                total: 'HKD 25,000-50,000 (₹2,65,000-5,30,000)'
            }
        },

        visa_types: [
            {name: 'Employment Visa', duration: '2 years', requirements: ['Job offer', 'Degree/Experience'], path_to_pr: '7 years'},
            {name: 'ASMTP (Top Talent)', duration: '2 years', requirements: ['₹3 Cr+ salary globally OR Top 100 university'], path_to_pr: '7 years'},
            {name: 'GEP (General Employment)', duration: '1 year', requirements: ['Employer sponsorship'], path_to_pr: '7 years'}
        ],

        pros: ['Low taxes', 'English environment', 'Close to India', 'High salaries', 'Financial hub', 'No capital gains'],
        cons: ['VERY expensive housing', 'Tiny apartments', 'Political uncertainty', 'Work-life balance poor', 'Competitive market']
    },

    // ==================== SAUDI ARABIA ====================
    SaudiArabia: {
        basic_info: {
            official_name: 'Kingdom of Saudi Arabia',
            capital: 'Riyadh',
            tech_hubs: 'Riyadh, Jeddah, NEOM',
            currency: 'SAR (Saudi Riyal)',
            exchange_rate: '1 SAR ≈ ₹22.1',
            timezone: 'GMT+3 (2.5hrs behind IST)',
            flight_time: '4-5 hours',
            language: 'Arabic, English in tech',
            indian_population: '2.5 Million+',
            visa_processing: '2-4 weeks',
            visa_cost: '₹10,000-25,000',
            tax_rate: '0% Income Tax'
        },

        why_indians_migrate: [
            '0% Income Tax - 100% take home',
            'Vision 2030 massive tech investment',
            'NEOM project - futuristic city with premium salaries',
            'Huge Indian community',
            'Close to India (4-5 hours)',
            'High savings potential (60-70%)',
            'Growing tech sector',
            'Premium Residency option',
            'Family-friendly lifestyle',
            'Good for building savings'
        ],

        vision_2030_opportunities: {
            neom: 'Futuristic city project - paying 50-100% premium',
            entertainment: 'Opening up - gaming, media, events',
            tech: 'Digital transformation initiatives',
            tourism: 'Red Sea project, AlUla'
        },

        step_by_step_migration: [
            {step: 1, title: 'Get Job Offer', details: 'Apply via LinkedIn, GulfTalent, Bayt, company websites.', duration: '1-3 months'},
            {step: 2, title: 'Document Attestation', details: 'Get degrees attested by MEA + Saudi Embassy.', duration: '2-4 weeks'},
            {step: 3, title: 'Visa Application', details: 'Employer applies through HRSD/Muqeem.', duration: '1-2 weeks'},
            {step: 4, title: 'Medical Test', details: 'GAMCA approved medical center in India.', duration: '1 week'},
            {step: 5, title: 'Fly to Saudi', details: 'Collect Iqama after arrival.', duration: '1 day'},
            {step: 6, title: 'Iqama (Residence ID)', details: 'Employer processes through Absher.', duration: '1-2 weeks'},
            {step: 7, title: 'Bank Account', details: 'Riyad Bank, Al Rajhi, SNB.', duration: '1 day'},
            {step: 8, title: 'SIM Card', details: 'STC, Mobily, Zain - need Iqama.', duration: '1 hour'}
        ],

        essential_apps: {
            government: ['Absher', 'Tawakkalna', 'Muqeem'],
            banking: ['Al Rajhi Bank', 'SNB', 'Riyad Bank'],
            transport: ['Uber Saudi', 'Careem', 'SAPTCO'],
            food: ['Hunger Station', 'Jahez', 'Talabat'],
            shopping: ['Noon', 'Amazon.sa', 'Namshi']
        },

        top_hiring_companies: {
            tech: ['Google', 'Oracle', 'SAP', 'Microsoft', 'Amazon'],
            neom: ['NEOM', 'Red Sea Development', 'Qiddiya'],
            saudi_companies: ['Saudi Aramco', 'STC', 'stc pay', 'Elm'],
            banks: ['Al Rajhi Bank', 'SNB', 'SABB', 'ANB']
        },

        salaries: {
            'Junior Developer (0-2y)': {sar: 'SAR 10,000-18,000/mo', inr: '₹27-48 LPA'},
            'Mid Developer (3-5y)': {sar: 'SAR 18,000-28,000/mo', inr: '₹48-74 LPA'},
            'Senior Developer (5-8y)': {sar: 'SAR 28,000-45,000/mo', inr: '₹74-119 LPA'},
            'Tech Lead (8-12y)': {sar: 'SAR 40,000-65,000/mo', inr: '₹106-172 LPA'},
            'NEOM Projects': {sar: 'SAR 50,000-100,000/mo', inr: '₹133-265 LPA'}
        },

        monthly_expenses: {
            riyadh: {
                rent: 'SAR 3,000-7,000 (₹66,000-1,55,000)',
                food: 'SAR 1,500-3,000 (₹33,000-66,000)',
                transport: 'SAR 800-1,500 (₹18,000-33,000)',
                utilities: 'SAR 500-1,000 (₹11,000-22,000)',
                total: 'SAR 6,000-13,000 (₹1,33,000-2,88,000)'
            }
        },

        savings_potential: {
            junior: '₹15-25 LPA (55-60% savings)',
            mid: '₹30-45 LPA (60-65% savings)',
            senior: '₹50-75 LPA (65-70% savings)',
            note: '0% tax + housing allowance = massive savings'
        },

        visa_types: [
            {name: 'Work Visa (Iqama)', duration: '1-2 years', requirements: ['Job offer', 'Attestations', 'Medical'], path_to_pr: 'Premium Residency option'},
            {name: 'Premium Residency', duration: 'Permanent or 1 year', requirements: ['Investment OR High salary'], path_to_pr: 'Closest to PR available'}
        ],

        culture_tips: [
            'Weekend is Friday-Saturday',
            'Ramadan affects work hours',
            'Alcohol prohibited',
            'Modest dressing appreciated',
            'Society is liberalizing rapidly under Vision 2030',
            'Women can drive and work freely now',
            'Entertainment options expanding'
        ],

        pros: ['0% income tax', 'High savings', 'Vision 2030 opportunities', 'Close to India', 'Large Indian community', 'Family-friendly'],
        cons: ['Extreme summer heat (50°C)', 'Conservative culture', 'Limited nightlife', 'Visa tied to employer', 'No citizenship pathway']
    },

    // ==================== QATAR ====================
    Qatar: {
        basic_info: {
            official_name: 'State of Qatar',
            capital: 'Doha',
            currency: 'QAR (Qatari Riyal)',
            exchange_rate: '1 QAR ≈ ₹22.8',
            timezone: 'GMT+3 (2.5hrs behind IST)',
            flight_time: '4 hours',
            language: 'Arabic, English widely used',
            indian_population: '700,000+',
            visa_processing: '2-4 weeks',
            visa_cost: '₹5,000-15,000',
            tax_rate: '0% Income Tax'
        },

        why_indians_migrate: [
            '0% Income Tax',
            'Post-FIFA World Cup infrastructure boom',
            'Close to India (4 hours)',
            'Large Indian community',
            'High savings potential',
            'Modern infrastructure',
            'Growing tech sector',
            'Safe country',
            'Tax-free remittances'
        ],

        top_hiring_companies: {
            tech: ['Microsoft Qatar', 'Oracle', 'SAP'],
            qatar_companies: ['Qatar Airways', 'Ooredoo', 'Qatar Energy', 'Qatar Foundation'],
            banks: ['QNB', 'Commercial Bank', 'Doha Bank'],
            construction: ['Qatar Rail', 'Ashghal']
        },

        salaries: {
            'Junior Developer (0-2y)': {qar: 'QAR 10,000-16,000/mo', inr: '₹27-44 LPA'},
            'Mid Developer (3-5y)': {qar: 'QAR 18,000-28,000/mo', inr: '₹49-76 LPA'},
            'Senior Developer (5-8y)': {qar: 'QAR 28,000-42,000/mo', inr: '₹76-115 LPA'},
            'Tech Lead': {qar: 'QAR 38,000-55,000/mo', inr: '₹104-150 LPA'}
        },

        monthly_expenses: {
            doha: {
                rent: 'QAR 4,000-8,000 (₹91,000-1,82,000)',
                food: 'QAR 1,500-3,000 (₹34,000-68,000)',
                transport: 'QAR 500-1,000',
                total: 'QAR 7,000-14,000 (₹1,60,000-3,19,000)'
            }
        },

        pros: ['0% tax', 'Modern infrastructure', 'Close to India', 'Safe', 'World Cup legacy', 'High savings'],
        cons: ['Small country', 'Extreme heat', 'Limited social life', 'No PR pathway', 'Expensive housing']
    },

    // ==================== KUWAIT ====================
    Kuwait: {
        basic_info: {
            official_name: 'State of Kuwait',
            capital: 'Kuwait City',
            currency: 'KWD (Kuwaiti Dinar - World\'s most valuable)',
            exchange_rate: '1 KWD ≈ ₹270',
            timezone: 'GMT+3 (2.5hrs behind IST)',
            flight_time: '4 hours',
            language: 'Arabic, English in tech',
            indian_population: '1 Million+',
            visa_processing: '2-4 weeks',
            tax_rate: '0% Income Tax'
        },

        why_indians_migrate: [
            '0% Income Tax',
            'Highest currency value in world',
            'Large Indian community (1M+)',
            'Close to India',
            'Oil wealth = good salaries',
            'Established Indian businesses'
        ],

        salaries: {
            'Junior Developer (0-2y)': {kwd: 'KWD 600-900/mo', inr: '₹19-29 LPA'},
            'Mid Developer (3-5y)': {kwd: 'KWD 1,000-1,500/mo', inr: '₹32-49 LPA'},
            'Senior Developer (5-8y)': {kwd: 'KWD 1,500-2,200/mo', inr: '₹49-71 LPA'}
        },

        pros: ['0% tax', 'Close to India', 'Strong currency', 'Large Indian community'],
        cons: ['Limited opportunities', 'Strict visa rules', 'No PR pathway', 'Hot climate']
    },

    // ==================== BAHRAIN ====================
    Bahrain: {
        basic_info: {
            official_name: 'Kingdom of Bahrain',
            capital: 'Manama',
            currency: 'BHD (Bahraini Dinar)',
            exchange_rate: '1 BHD ≈ ₹220',
            timezone: 'GMT+3 (2.5hrs behind IST)',
            flight_time: '4 hours',
            language: 'Arabic, English widely used',
            indian_population: '400,000+',
            visa_processing: '2-3 weeks',
            tax_rate: '0% Income Tax'
        },

        why_indians_migrate: [
            '0% Income Tax',
            'More liberal than other Gulf states',
            'Growing fintech hub',
            'Close to India',
            'Large Indian community',
            'Good work-life balance for Gulf',
            'Bahrain Fintech Bay initiatives',
            'Alcohol available'
        ],

        top_hiring_companies: {
            banks: ['Bank of Bahrain', 'Gulf International Bank', 'Ahli United'],
            fintech: ['Rain', 'Bahrain FinTech Bay startups'],
            telecom: ['Batelco', 'Zain', 'STC Bahrain']
        },

        salaries: {
            'Junior Developer (0-2y)': {bhd: 'BHD 600-1,000/mo', inr: '₹16-26 LPA'},
            'Mid Developer (3-5y)': {bhd: 'BHD 1,000-1,600/mo', inr: '₹26-42 LPA'},
            'Senior Developer (5-8y)': {bhd: 'BHD 1,500-2,500/mo', inr: '₹40-66 LPA'}
        },

        pros: ['0% tax', 'Liberal culture', 'Fintech hub', 'Alcohol available', 'Good quality of life'],
        cons: ['Smaller market', 'Lower salaries than UAE', 'Limited tech jobs', 'Small country']
    },

    // ==================== OMAN ====================
    Oman: {
        basic_info: {
            official_name: 'Sultanate of Oman',
            capital: 'Muscat',
            currency: 'OMR (Omani Rial)',
            exchange_rate: '1 OMR ≈ ₹216',
            timezone: 'GMT+4 (1.5hrs behind IST)',
            flight_time: '3-4 hours',
            language: 'Arabic, English in business',
            indian_population: '600,000+',
            visa_processing: '2-3 weeks',
            tax_rate: '0% Income Tax'
        },

        why_indians_migrate: [
            '0% Income Tax',
            'Most scenic Gulf country',
            'Relaxed pace of life',
            'Close to India (3 hours)',
            'Large Indian community',
            'Good work-life balance',
            'Beautiful beaches and mountains',
            'More affordable than UAE'
        ],

        top_hiring_companies: {
            oil_gas: ['PDO (Petroleum Development Oman)', 'OQ', 'OOCEP'],
            telecom: ['Omantel', 'Ooredoo Oman'],
            banks: ['Bank Muscat', 'Bank Dhofar', 'HSBC Oman']
        },

        salaries: {
            'Junior Developer (0-2y)': {omr: 'OMR 400-700/mo', inr: '₹10-18 LPA'},
            'Mid Developer (3-5y)': {omr: 'OMR 700-1,200/mo', inr: '₹18-31 LPA'},
            'Senior Developer (5-8y)': {omr: 'OMR 1,200-2,000/mo', inr: '₹31-52 LPA'}
        },

        pros: ['0% tax', 'Beautiful country', 'Relaxed lifestyle', 'Close to India', 'Affordable'],
        cons: ['Limited tech jobs', 'Lower salaries', 'Omanization rules', 'Small market']
    }
};

// Export
if (typeof window !== 'undefined') {
    window.ENHANCED_COUNTRY_DATA_4 = ENHANCED_COUNTRY_DATA_4;
}


