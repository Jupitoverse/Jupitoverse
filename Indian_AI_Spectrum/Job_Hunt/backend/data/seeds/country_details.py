"""
Comprehensive Country Migration Data
Detailed guides for each country including visa, job portals, agencies, and more
"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import SessionLocal, init_db
from app.models.country import Country, CountryMigration
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def serialize_json_fields(data):
    """Convert dict/list fields to JSON strings for SQLite"""
    serialized = {}
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            serialized[key] = json.dumps(value)
        else:
            serialized[key] = value
    return serialized

# =============================================================================
# COMPREHENSIVE COUNTRY MIGRATION GUIDES
# =============================================================================

DETAILED_MIGRATION_GUIDES = [
    # =============================================================================
    # DUBAI / UAE
    # =============================================================================
    {
        "country_name": "United Arab Emirates (Dubai)",
        "visa_types": [
            {
                "name": "Employment Visa",
                "description": "Standard work visa sponsored by employer",
                "requirements": [
                    "Job offer from UAE company",
                    "Valid passport (6+ months)",
                    "Passport photos",
                    "Educational certificates (attested)",
                    "Medical fitness certificate",
                    "Emirates ID application"
                ],
                "processing_time": "2-4 weeks",
                "validity": "2-3 years (renewable)",
                "cost": "$300-500"
            },
            {
                "name": "Green Visa",
                "description": "Self-sponsored 5-year residency visa",
                "requirements": [
                    "Bachelor's degree or equivalent",
                    "Minimum salary AED 15,000/month",
                    "Valid employment contract",
                    "Health insurance"
                ],
                "processing_time": "2-3 weeks",
                "validity": "5 years",
                "cost": "$500-700"
            },
            {
                "name": "Golden Visa",
                "description": "10-year residency for exceptional talents",
                "requirements": [
                    "Specialized talents in AI, Big Data, etc.",
                    "OR Investment of AED 2M+",
                    "OR Salary AED 30,000+ with specialized degree"
                ],
                "processing_time": "1-2 months",
                "validity": "10 years",
                "cost": "$1000-1500"
            },
            {
                "name": "Freelance Visa",
                "description": "For remote workers and freelancers",
                "requirements": [
                    "Proof of freelance work/clients",
                    "Minimum income requirements",
                    "Valid passport"
                ],
                "processing_time": "2-3 weeks",
                "validity": "1-3 years",
                "cost": "$2000-3000/year"
            }
        ],
        "visa_process_steps": [
            "1. Get job offer from UAE employer",
            "2. Employer applies for work permit at Ministry of Labour",
            "3. Receive entry permit (within 2 weeks)",
            "4. Travel to UAE within 60 days",
            "5. Complete medical fitness test",
            "6. Apply for Emirates ID",
            "7. Visa stamped in passport",
            "8. Open bank account with Emirates ID"
        ],
        "visa_processing_time_weeks": 3,
        "visa_cost_usd": 500,
        "employer_sponsorship_required": True,
        "popular_job_portals": [
            {"name": "LinkedIn UAE", "url": "https://linkedin.com/jobs", "description": "Best for networking and professional jobs", "is_recommended": True},
            {"name": "Bayt.com", "url": "https://bayt.com", "description": "Largest job portal in Middle East", "is_recommended": True},
            {"name": "GulfTalent", "url": "https://gulftalent.com", "description": "Premium Gulf jobs", "is_recommended": True},
            {"name": "Naukri Gulf", "url": "https://naukrigulf.com", "description": "Indian-friendly portal for Gulf jobs", "is_recommended": True},
            {"name": "Indeed UAE", "url": "https://indeed.ae", "description": "Large job aggregator"},
            {"name": "Dubizzle Jobs", "url": "https://dubizzle.com/jobs", "description": "Local UAE classifieds"},
            {"name": "Monster Gulf", "url": "https://monstergulf.com", "description": "International job board"},
            {"name": "Jobs.ac.ae", "url": "https://jobs.ac.ae", "description": "Government jobs portal"},
            {"name": "Khaleej Times Jobs", "url": "https://khaleejtimes.com/jobs", "description": "Jobs from local newspaper"}
        ],
        "recruitment_agencies": [
            {"name": "Michael Page UAE", "url": "https://michaelpage.ae", "specialization": "Finance, Tech, Engineering", "free_for_candidates": True},
            {"name": "Robert Half UAE", "url": "https://roberthalf.ae", "specialization": "Finance, Tech", "free_for_candidates": True},
            {"name": "Hays UAE", "url": "https://hays.ae", "specialization": "All sectors", "free_for_candidates": True},
            {"name": "Charterhouse", "url": "https://charterhouse.ae", "specialization": "Finance, Banking", "free_for_candidates": True},
            {"name": "Adecco Middle East", "url": "https://adeccome.com", "specialization": "IT, Engineering", "free_for_candidates": True},
            {"name": "Manpower Middle East", "url": "https://manpowergroup.ae", "specialization": "IT, Manufacturing", "free_for_candidates": True},
            {"name": "Clarendon Parker", "url": "https://clarendonparker.com", "specialization": "Tech, Finance", "free_for_candidates": True},
            {"name": "Gulfstream HR", "url": "https://gulfstreamhr.com", "specialization": "All sectors", "free_for_candidates": True}
        ],
        "top_hiring_companies": [
            {"name": "Emirates NBD", "industry": "Banking", "careers_url": "https://emiratesnbd.com/en/careers"},
            {"name": "Careem", "industry": "Tech/Mobility", "careers_url": "https://careem.com/en-ae/careers"},
            {"name": "Noon", "industry": "E-commerce", "careers_url": "https://noon.com/careers"},
            {"name": "Talabat", "industry": "Food Delivery", "careers_url": "https://talabat.com/uae/careers"},
            {"name": "Aramex", "industry": "Logistics", "careers_url": "https://aramex.com/ae/en/careers"},
            {"name": "Majid Al Futtaim", "industry": "Retail/Tech", "careers_url": "https://majidalfuttaim.com/en/careers"},
            {"name": "Emirates Airlines", "industry": "Aviation", "careers_url": "https://emirates.com/careers"},
            {"name": "Dubai Holding", "industry": "Investment", "careers_url": "https://dubaiholding.com/en/careers"},
            {"name": "DEWA", "industry": "Utilities/Govt", "careers_url": "https://dewa.gov.ae/en/career"},
            {"name": "Etisalat", "industry": "Telecom", "careers_url": "https://etisalat.ae/en/careers.html"},
            {"name": "du (EITC)", "industry": "Telecom", "careers_url": "https://du.ae/about-us/careers"},
            {"name": "Mashreq Bank", "industry": "Banking", "careers_url": "https://mashreq.com/en/uae/personal/careers"},
            {"name": "ADNOC", "industry": "Oil & Gas", "careers_url": "https://adnoc.ae/careers"},
            {"name": "DP World", "industry": "Logistics", "careers_url": "https://dpworld.com/careers"},
            {"name": "G42", "industry": "AI/Tech", "careers_url": "https://g42.ai/careers"}
        ],
        "resume_format": "Standard international format, 2 pages max, no photo required (but common to include)",
        "resume_tips": [
            "Keep it concise - 2 pages maximum",
            "Include visa status if already in UAE",
            "Highlight GCC/Middle East experience",
            "Add nationality and languages",
            "Include notice period",
            "Mention current salary (common practice)",
            "No need for detailed personal info"
        ],
        "cover_letter_required": False,
        "documents_required": [
            "Valid passport (6+ months validity)",
            "Passport-size photographs (white background)",
            "Educational certificates (degree, transcripts)",
            "Attestation of documents (from home country and UAE embassy)",
            "Experience letters from previous employers",
            "Police clearance certificate",
            "Medical fitness certificate (done in UAE)",
            "Emirates ID application (done in UAE)"
        ],
        "document_attestation_required": True,
        "attestation_process": [
            "1. Notarize documents from local notary",
            "2. State-level attestation (e.g., SDM/Home Department)",
            "3. MEA (Ministry of External Affairs) attestation",
            "4. UAE Embassy attestation in India",
            "5. MOFA (Ministry of Foreign Affairs) attestation in UAE"
        ],
        "monthly_expenses_estimate": {
            "single_sharing": 3000,
            "single_studio": 5000,
            "single_1bhk": 7000,
            "family_2bhk": 10000,
            "breakdown": {
                "rent_studio": "AED 3000-5000/month",
                "rent_1bhk": "AED 5000-8000/month",
                "rent_2bhk": "AED 8000-12000/month",
                "utilities": "AED 500-800/month",
                "food_single": "AED 1500-2500/month",
                "transport_metro": "AED 300-500/month",
                "transport_car": "AED 1500-2500/month",
                "mobile_internet": "AED 300-500/month",
                "health_insurance": "Usually covered by employer"
            }
        },
        "initial_settlement_cost": 15000,
        "initial_costs_breakdown": {
            "flight": "$300-500",
            "security_deposit_rent": "AED 5000-15000 (1-3 months)",
            "agency_fee": "AED 2000-5000",
            "furnishing": "AED 3000-10000",
            "initial_groceries": "AED 1000-2000",
            "transport_setup": "AED 1000-2000"
        },
        "language_requirements": {
            "work": "English (Arabic is a plus)",
            "daily_life": "English widely spoken",
            "official": "Arabic (but English accepted)"
        },
        "work_culture": [
            "Work week: Sunday to Thursday (Friday-Saturday weekend)",
            "Working hours: 8-9 hours/day",
            "Ramadan: Reduced working hours",
            "Dress code: Business formal, modest",
            "Hierarchy respected in workplace",
            "Networking is crucial for career growth"
        ],
        "tax_info": {
            "income_tax": "0% - No income tax",
            "corporate_tax": "9% (from 2023, above AED 375,000 profit)",
            "vat": "5% on goods and services",
            "notes": "Tax-free salary is major attraction"
        },
        "pr_eligibility_years": 0,
        "pr_info": "UAE doesn't offer traditional PR. Golden Visa (10 years) is closest option.",
        "citizenship_eligibility_years": 0,
        "citizenship_info": "UAE citizenship extremely rare for expats. Naturalization possible after 30 years.",
        "healthcare_info": {
            "system": "Mandatory health insurance (employer provided)",
            "quality": "World-class private healthcare",
            "cost": "Insurance covers most expenses",
            "hospitals": ["Cleveland Clinic Abu Dhabi", "Mediclinic", "NMC Healthcare", "Aster DM Healthcare"]
        },
        "indian_community": {
            "population": "3.5+ million Indians",
            "percentage": "30% of UAE population",
            "areas": ["Karama", "Bur Dubai", "Deira", "Sharjah", "Al Ain"],
            "temples": ["Hindu Temple Bur Dubai", "BAPS Mandir Abu Dhabi"],
            "groceries": "Indian groceries widely available",
            "restaurants": "Extensive Indian food options"
        },
        "common_challenges": [
            "High cost of living in Dubai",
            "Rental costs require large upfront payment",
            "Job market competitive",
            "Summer heat (45°C+) challenging",
            "Limited long-term residency options",
            "Strict laws - respect local culture",
            "Dependent visa restrictions"
        ],
        "tips_for_indians": [
            "Network heavily on LinkedIn before applying",
            "Get documents attested before leaving India",
            "Negotiate salary package including housing allowance",
            "Consider Sharjah/Ajman for cheaper rent",
            "Join Indian community groups on Facebook/WhatsApp",
            "Keep emergency fund for 3-6 months",
            "Understand labor laws - notice periods etc.",
            "Don't pay recruitment agencies - it's illegal to charge candidates"
        ],
        "things_to_avoid": [
            "Don't pay agencies for job placement (illegal)",
            "Don't accept job without proper contract",
            "Don't overstay visa - heavy penalties",
            "Don't use VPN for illegal content",
            "Don't disrespect local customs/religion",
            "Don't bounce cheques - criminal offense"
        ],
        "salary_expectations": {
            "software_engineer_entry": "AED 8,000-15,000/month",
            "software_engineer_mid": "AED 15,000-30,000/month",
            "software_engineer_senior": "AED 30,000-50,000/month",
            "data_scientist": "AED 20,000-45,000/month",
            "devops_engineer": "AED 15,000-35,000/month",
            "product_manager": "AED 25,000-50,000/month",
            "note": "Salaries are TAX FREE"
        },
        "facebook_groups": [
            {"name": "Indians in Dubai", "url": "https://facebook.com/groups/indiansindubai"},
            {"name": "Jobs in Dubai for Indians", "url": "https://facebook.com/groups/jobsindubaiforindians"},
            {"name": "IT Professionals UAE", "url": "https://facebook.com/groups/itprofessionalsuae"},
            {"name": "Dubai Jobs", "url": "https://facebook.com/groups/dubaijobsgroup"}
        ],
        "whatsapp_telegram_groups": [
            {"name": "Dubai IT Jobs", "platform": "Telegram", "description": "IT job postings"},
            {"name": "Indians in UAE", "platform": "Telegram", "description": "Community group"}
        ],
        "youtube_channels": [
            {"name": "Dubai Life", "url": "https://youtube.com/@dubailife", "description": "Life in Dubai tips"},
            {"name": "Indian in Dubai", "url": "https://youtube.com/@indianindubai", "description": "Relocation guide"}
        ],
        "useful_websites": [
            {"name": "GDRFA Dubai", "url": "https://gdrfad.gov.ae", "description": "Visa and residency info"},
            {"name": "MOHRE", "url": "https://mohre.gov.ae", "description": "Ministry of Human Resources"},
            {"name": "ICA UAE", "url": "https://icp.gov.ae", "description": "Identity and citizenship"}
        ]
    },
    
    # =============================================================================
    # GERMANY (Enhanced)
    # =============================================================================
    {
        "country_name": "Germany",
        "visa_types": [
            {
                "name": "EU Blue Card",
                "description": "For highly qualified professionals with university degree",
                "requirements": [
                    "Recognized university degree",
                    "Job offer with minimum salary €58,400/year (€45,552 for shortage occupations like IT)",
                    "Valid passport",
                    "Health insurance",
                    "Proof of accommodation"
                ],
                "processing_time": "4-8 weeks",
                "validity": "4 years (max) or duration of contract + 3 months",
                "cost": "€75"
            },
            {
                "name": "Job Seeker Visa",
                "description": "6-month visa to search for job in Germany",
                "requirements": [
                    "Recognized university degree",
                    "Proof of financial means (€947/month for 6 months)",
                    "Health insurance for 6 months",
                    "CV and cover letter",
                    "Accommodation proof"
                ],
                "processing_time": "8-12 weeks",
                "validity": "6 months",
                "cost": "€75"
            },
            {
                "name": "Skilled Worker Visa",
                "description": "For qualified professionals without degree but with training",
                "requirements": [
                    "Recognized vocational qualification",
                    "Job offer in related field",
                    "German language skills (usually B1)"
                ],
                "processing_time": "4-8 weeks",
                "validity": "4 years",
                "cost": "€75"
            }
        ],
        "visa_process_steps": [
            "1. Get job offer from German employer",
            "2. Check if degree is recognized (anabin database)",
            "3. Get ZAB evaluation if needed",
            "4. Book appointment at German embassy/VFS",
            "5. Prepare all documents with translations",
            "6. Submit visa application",
            "7. Wait for approval (4-12 weeks)",
            "8. Collect visa and travel",
            "9. Register at local Bürgeramt within 2 weeks",
            "10. Apply for residence permit"
        ],
        "visa_processing_time_weeks": 8,
        "visa_cost_usd": 100,
        "employer_sponsorship_required": True,
        "popular_job_portals": [
            {"name": "LinkedIn Germany", "url": "https://linkedin.com/jobs", "description": "Best for professional networking", "is_recommended": True},
            {"name": "StepStone", "url": "https://stepstone.de", "description": "Major German job portal", "is_recommended": True},
            {"name": "Indeed Germany", "url": "https://indeed.de", "description": "Large job aggregator", "is_recommended": True},
            {"name": "Xing", "url": "https://xing.com", "description": "German professional network", "is_recommended": True},
            {"name": "Glassdoor Germany", "url": "https://glassdoor.de", "description": "Reviews + jobs"},
            {"name": "Monster Germany", "url": "https://monster.de", "description": "International job board"},
            {"name": "Arbeitsagentur", "url": "https://arbeitsagentur.de", "description": "Official government job portal"},
            {"name": "Make it in Germany", "url": "https://make-it-in-germany.com", "description": "Government portal for skilled workers"},
            {"name": "Honeypot", "url": "https://honeypot.io", "description": "Tech-focused job platform"},
            {"name": "Berlinstartupjobs", "url": "https://berlinstartupjobs.com", "description": "Startup jobs in Berlin"}
        ],
        "recruitment_agencies": [
            {"name": "Michael Page Germany", "url": "https://michaelpage.de", "specialization": "Finance, Tech, Engineering"},
            {"name": "Hays Germany", "url": "https://hays.de", "specialization": "IT, Engineering, Finance"},
            {"name": "Robert Half", "url": "https://roberthalf.de", "specialization": "Finance, Tech"},
            {"name": "Randstad Germany", "url": "https://randstad.de", "specialization": "IT, Engineering"},
            {"name": "Experis", "url": "https://experis.de", "specialization": "IT and Tech"},
            {"name": "Computer Futures", "url": "https://computerfutures.com/de", "specialization": "Tech only"}
        ],
        "top_hiring_companies": [
            {"name": "SAP", "industry": "Enterprise Software", "careers_url": "https://jobs.sap.com"},
            {"name": "Siemens", "industry": "Industrial/Tech", "careers_url": "https://siemens.com/careers"},
            {"name": "BMW", "industry": "Automotive", "careers_url": "https://bmwgroup.jobs"},
            {"name": "Bosch", "industry": "Automotive/IoT", "careers_url": "https://bosch.com/careers"},
            {"name": "Deutsche Bank", "industry": "Banking", "careers_url": "https://careers.db.com"},
            {"name": "Allianz", "industry": "Insurance", "careers_url": "https://careers.allianz.com"},
            {"name": "Delivery Hero", "industry": "Food Tech", "careers_url": "https://careers.deliveryhero.com"},
            {"name": "Zalando", "industry": "E-commerce", "careers_url": "https://jobs.zalando.com"},
            {"name": "N26", "industry": "FinTech", "careers_url": "https://n26.com/en/careers"},
            {"name": "AUTO1 Group", "industry": "Automotive", "careers_url": "https://auto1-group.com/careers"},
            {"name": "Personio", "industry": "HR Tech", "careers_url": "https://personio.com/careers"},
            {"name": "Celonis", "industry": "Process Mining", "careers_url": "https://celonis.com/careers"}
        ],
        "resume_format": "Europass or German-style CV with photo, personal details, and signature",
        "resume_tips": [
            "Include professional photo (mandatory in Germany)",
            "Add date of birth, nationality, marital status",
            "List education with grades",
            "Include German language proficiency level",
            "Mention hobbies and interests",
            "Sign and date the CV",
            "Keep it structured and chronological",
            "2-3 pages acceptable"
        ],
        "cover_letter_required": True,
        "documents_required": [
            "Valid passport (6+ months)",
            "Completed visa application form",
            "Biometric photos",
            "Original degree certificates",
            "Degree evaluation (ZAB/anabin)",
            "Job offer/employment contract",
            "Proof of accommodation",
            "Health insurance",
            "Proof of financial means",
            "CV in German/English",
            "Cover letter",
            "Blocked account (Sperrkonto) for job seeker visa"
        ],
        "monthly_expenses_estimate": {
            "single": 1500,
            "family": 3500,
            "breakdown": {
                "rent_shared": "€400-700/month",
                "rent_1bhk": "€800-1500/month (varies by city)",
                "utilities": "€150-250/month",
                "health_insurance": "€100-200/month (public)",
                "food": "€250-400/month",
                "transport": "€80-100/month (monthly pass)",
                "mobile": "€10-30/month"
            }
        },
        "initial_settlement_cost": 5000,
        "language_requirements": {
            "work": "English for IT (German preferred for others)",
            "daily_life": "German A1-B1 recommended",
            "official": "German"
        },
        "pr_eligibility_years": 4,
        "pr_requirements": [
            "33 months with Blue Card (21 months with B1 German)",
            "Mandatory pension contributions",
            "Sufficient living space",
            "German language B1",
            "No criminal record"
        ],
        "citizenship_eligibility_years": 8,
        "citizenship_requirements": [
            "8 years of legal residence (6 with integration course)",
            "German language B1",
            "Pass citizenship test",
            "Financial self-sufficiency",
            "Renounce previous citizenship (mostly)"
        ],
        "tax_info": {
            "income_tax": "14% - 45% (progressive)",
            "social_contributions": "~20% (pension, health, unemployment)",
            "church_tax": "8-9% (if registered)",
            "solidarity_surcharge": "5.5% (high earners only)"
        },
        "common_challenges": [
            "German bureaucracy (Bürokratie)",
            "Finding apartment is very difficult",
            "Cold weather and short winter days",
            "Language barrier in daily life",
            "Cultural adjustment",
            "Banking can be complex",
            "Sundays everything closed"
        ],
        "tips_for_indians": [
            "Start learning German NOW (even A1 helps)",
            "Open Blocked Account before visa application",
            "Join German courses at Goethe Institut",
            "Network on LinkedIn and Xing",
            "Consider cities beyond Berlin - Munich, Frankfurt",
            "Get anabin recognition checked early",
            "Join Indian community groups"
        ],
        "salary_expectations": {
            "software_engineer_entry": "€50,000-65,000/year",
            "software_engineer_mid": "€65,000-85,000/year",
            "software_engineer_senior": "€85,000-120,000/year",
            "data_scientist": "€55,000-90,000/year",
            "devops_engineer": "€55,000-85,000/year"
        },
        "facebook_groups": [
            {"name": "Indians in Germany", "url": "https://facebook.com/groups/indiansingermany"},
            {"name": "IT Jobs in Germany", "url": "https://facebook.com/groups/itjobsingermany"},
            {"name": "Indians in Berlin", "url": "https://facebook.com/groups/indiansinberlin"}
        ],
        "youtube_channels": [
            {"name": "Bharat in Germany", "url": "https://youtube.com/@bharatingermany"},
            {"name": "Nikhilesh Dhure", "url": "https://youtube.com/@nikhileshdhure"},
            {"name": "Simple Germany", "url": "https://youtube.com/@simplegermany"}
        ]
    },
    
    # =============================================================================
    # CANADA (Enhanced)
    # =============================================================================
    {
        "country_name": "Canada",
        "visa_types": [
            {
                "name": "Express Entry - Federal Skilled Worker",
                "description": "Points-based immigration for skilled workers",
                "requirements": [
                    "Minimum 67 points on selection grid",
                    "CLB 7 in English/French (IELTS 6 each)",
                    "Education Credential Assessment (ECA)",
                    "1+ year skilled work experience",
                    "Proof of funds"
                ],
                "processing_time": "6-12 months",
                "validity": "PR (Permanent Residence)",
                "cost": "CAD 2,500-3,500"
            },
            {
                "name": "Provincial Nominee Program (PNP)",
                "description": "Province-specific immigration pathways",
                "requirements": [
                    "Meet specific provincial criteria",
                    "May have lower CRS requirements",
                    "Some streams have job offer requirements"
                ],
                "processing_time": "12-18 months",
                "validity": "PR",
                "cost": "CAD 2,500-4,000"
            },
            {
                "name": "Work Permit (LMIA)",
                "description": "Employer-sponsored temporary work permit",
                "requirements": [
                    "Valid job offer with LMIA",
                    "Proof of qualifications",
                    "Medical exam"
                ],
                "processing_time": "2-4 months",
                "validity": "Depends on job offer",
                "cost": "CAD 155"
            },
            {
                "name": "Global Talent Stream",
                "description": "Fast-track work permit for tech workers",
                "requirements": [
                    "Job offer from GTS employer",
                    "In-demand tech occupation"
                ],
                "processing_time": "2 weeks",
                "validity": "Up to 3 years",
                "cost": "CAD 155"
            }
        ],
        "visa_process_steps": [
            "1. Check eligibility using CRS calculator",
            "2. Take IELTS/CELPIP exam (aim for 8+)",
            "3. Get ECA (Educational Credential Assessment) from WES",
            "4. Create Express Entry profile",
            "5. Improve CRS score (French, PNP nomination)",
            "6. Receive ITA (Invitation to Apply)",
            "7. Submit PR application with documents",
            "8. Complete medical examination",
            "9. Provide biometrics",
            "10. Receive COPR (Confirmation of PR)",
            "11. Land in Canada within validity"
        ],
        "visa_processing_time_weeks": 26,
        "visa_cost_usd": 1500,
        "employer_sponsorship_required": False,
        "popular_job_portals": [
            {"name": "LinkedIn Canada", "url": "https://linkedin.com/jobs", "description": "Best for professional networking", "is_recommended": True},
            {"name": "Indeed Canada", "url": "https://indeed.ca", "description": "Largest job aggregator", "is_recommended": True},
            {"name": "Glassdoor Canada", "url": "https://glassdoor.ca", "description": "Reviews + jobs", "is_recommended": True},
            {"name": "Job Bank", "url": "https://jobbank.gc.ca", "description": "Official government portal", "is_recommended": True},
            {"name": "Workopolis", "url": "https://workopolis.com", "description": "Canadian job board"},
            {"name": "Monster Canada", "url": "https://monster.ca", "description": "International job board"},
            {"name": "Eluta", "url": "https://eluta.ca", "description": "Top employer jobs"},
            {"name": "TechToronto", "url": "https://techto.org/jobs", "description": "Toronto tech jobs"},
            {"name": "AngelList", "url": "https://angel.co", "description": "Startup jobs"}
        ],
        "recruitment_agencies": [
            {"name": "Robert Half Canada", "url": "https://roberthalf.ca", "specialization": "Finance, Tech"},
            {"name": "Hays Canada", "url": "https://hays.ca", "specialization": "IT, Engineering"},
            {"name": "Randstad Canada", "url": "https://randstad.ca", "specialization": "IT, Admin"},
            {"name": "TEKsystems", "url": "https://teksystems.com/en-ca", "specialization": "IT staffing"},
            {"name": "Procom", "url": "https://procom.ca", "specialization": "Tech consulting"}
        ],
        "top_hiring_companies": [
            {"name": "Shopify", "industry": "E-commerce", "careers_url": "https://shopify.com/careers"},
            {"name": "Amazon Canada", "industry": "Tech/E-commerce", "careers_url": "https://amazon.jobs/en/locations/canada"},
            {"name": "Google Canada", "industry": "Tech", "careers_url": "https://careers.google.com"},
            {"name": "Microsoft Canada", "industry": "Tech", "careers_url": "https://careers.microsoft.com"},
            {"name": "RBC", "industry": "Banking", "careers_url": "https://jobs.rbc.com"},
            {"name": "TD Bank", "industry": "Banking", "careers_url": "https://jobs.td.com"},
            {"name": "Scotiabank", "industry": "Banking", "careers_url": "https://scotiabank.com/careers"},
            {"name": "Bell", "industry": "Telecom", "careers_url": "https://jobs.bell.ca"},
            {"name": "Rogers", "industry": "Telecom", "careers_url": "https://rogers.com/careers"},
            {"name": "Wealthsimple", "industry": "FinTech", "careers_url": "https://wealthsimple.com/en-ca/careers"},
            {"name": "Hootsuite", "industry": "SaaS", "careers_url": "https://hootsuite.com/careers"},
            {"name": "Clio", "industry": "LegalTech", "careers_url": "https://clio.com/careers"}
        ],
        "resume_format": "Canadian style - achievement-focused, no photo, no personal details",
        "resume_tips": [
            "NO photo required",
            "Remove date of birth, marital status",
            "Use Canadian spelling (colour, behaviour)",
            "Focus on achievements with metrics",
            "Include Canadian certifications if any",
            "Keep to 2 pages maximum",
            "Use ATS-friendly format"
        ],
        "cover_letter_required": True,
        "documents_required": [
            "Valid passport",
            "IELTS/CELPIP scores (CLB 7+)",
            "ECA report (WES recommended)",
            "Police Clearance Certificate",
            "Medical examination results",
            "Proof of funds (CAD 13,310+ for single)",
            "Reference letters from employers",
            "Photos as per specifications"
        ],
        "monthly_expenses_estimate": {
            "single": 2000,
            "family": 4500,
            "breakdown": {
                "rent_shared": "CAD 800-1200/month",
                "rent_1bhk": "CAD 1500-2500/month (Toronto/Vancouver)",
                "utilities": "CAD 100-200/month",
                "food": "CAD 400-600/month",
                "transport": "CAD 100-150/month (public transit)",
                "mobile": "CAD 50-80/month",
                "health_insurance": "Covered by provincial health"
            }
        },
        "initial_settlement_cost": 8000,
        "language_requirements": {
            "work": "English (French is bonus)",
            "daily_life": "English",
            "pr_requirement": "CLB 7 (IELTS 6 each band)"
        },
        "pr_eligibility_years": 0,
        "pr_info": "Express Entry provides direct PR - no waiting period",
        "citizenship_eligibility_years": 3,
        "citizenship_requirements": [
            "3 years (1095 days) physical presence",
            "File taxes for 3 years",
            "Pass citizenship test",
            "English/French CLB 4",
            "No criminal inadmissibility"
        ],
        "tax_info": {
            "federal_tax": "15% - 33% (progressive)",
            "provincial_tax": "5% - 21% (varies)",
            "total": "Approximately 25-50% depending on income and province"
        },
        "common_challenges": [
            "Extreme cold (-30°C in winter)",
            "High cost of living in Toronto/Vancouver",
            "Canadian experience requirement for some jobs",
            "Long waiting times for healthcare",
            "Getting first job can be challenging",
            "Credential recognition can be slow"
        ],
        "tips_for_indians": [
            "Take IELTS seriously - 8+ is competitive",
            "Start WES ECA 3-4 months before profile",
            "Consider PNP for extra 600 points",
            "Learn French for 50+ extra points",
            "Consider smaller cities (Calgary, Ottawa)",
            "Network on LinkedIn BEFORE moving",
            "Join Desi community groups",
            "Prepare for cold weather seriously"
        ],
        "salary_expectations": {
            "software_engineer_entry": "CAD 65,000-85,000/year",
            "software_engineer_mid": "CAD 90,000-130,000/year",
            "software_engineer_senior": "CAD 130,000-180,000/year",
            "data_scientist": "CAD 80,000-140,000/year",
            "devops_engineer": "CAD 80,000-130,000/year"
        },
        "facebook_groups": [
            {"name": "Indians in Canada", "url": "https://facebook.com/groups/indiansincanada"},
            {"name": "Express Entry Canada", "url": "https://facebook.com/groups/expressentry"},
            {"name": "Indians in Toronto", "url": "https://facebook.com/groups/indiansintoronto"},
            {"name": "IT Jobs in Canada", "url": "https://facebook.com/groups/itjobscanada"}
        ],
        "youtube_channels": [
            {"name": "Canada Immigration", "url": "https://youtube.com/@canadaimmigration"},
            {"name": "Desi to Videsi", "url": "https://youtube.com/@desividesi"},
            {"name": "Saurabh", "url": "https://youtube.com/@saurabhcanada"}
        ]
    },
    
    # =============================================================================
    # USA
    # =============================================================================
    {
        "country_name": "United States",
        "visa_types": [
            {
                "name": "H-1B Visa",
                "description": "Specialty occupation visa for skilled workers",
                "requirements": [
                    "Bachelor's degree or equivalent",
                    "Job offer in specialty occupation",
                    "Employer files petition with USCIS",
                    "Selected in lottery (April each year)"
                ],
                "processing_time": "3-6 months (after lottery selection)",
                "validity": "3 years (extendable to 6)",
                "cost": "$5,000-10,000 (employer pays)",
                "lottery": True
            },
            {
                "name": "L-1 Visa",
                "description": "Intracompany transferee visa",
                "requirements": [
                    "Worked for company abroad for 1+ years",
                    "Managerial/specialized knowledge role",
                    "Company has US presence"
                ],
                "processing_time": "2-4 months",
                "validity": "1-3 years initially",
                "cost": "$3,000-5,000"
            },
            {
                "name": "O-1 Visa",
                "description": "For individuals with extraordinary ability",
                "requirements": [
                    "Extraordinary ability in sciences, arts, business",
                    "National/international recognition",
                    "Extensive documentation"
                ],
                "processing_time": "2-4 months",
                "validity": "3 years",
                "cost": "$3,000-5,000"
            }
        ],
        "visa_process_steps": [
            "1. Find US employer willing to sponsor H-1B",
            "2. Employer files LCA (Labor Condition Application)",
            "3. Employer files H-1B petition in April",
            "4. Wait for lottery results (April)",
            "5. If selected, petition processed",
            "6. Attend visa interview at US embassy",
            "7. Receive visa stamp",
            "8. Enter US and start work (October 1)"
        ],
        "visa_processing_time_weeks": 20,
        "visa_cost_usd": 7000,
        "employer_sponsorship_required": True,
        "popular_job_portals": [
            {"name": "LinkedIn USA", "url": "https://linkedin.com/jobs", "description": "Best for networking", "is_recommended": True},
            {"name": "Indeed USA", "url": "https://indeed.com", "description": "Largest job board", "is_recommended": True},
            {"name": "Glassdoor", "url": "https://glassdoor.com", "description": "Reviews + Jobs", "is_recommended": True},
            {"name": "Levels.fyi", "url": "https://levels.fyi", "description": "Tech salary data", "is_recommended": True},
            {"name": "Dice", "url": "https://dice.com", "description": "Tech-focused jobs"},
            {"name": "BuiltIn", "url": "https://builtin.com", "description": "Startup jobs by city"},
            {"name": "AngelList", "url": "https://angel.co", "description": "Startup jobs"},
            {"name": "Hired", "url": "https://hired.com", "description": "Tech job marketplace"}
        ],
        "recruitment_agencies": [
            {"name": "Robert Half", "url": "https://roberthalf.com", "specialization": "Tech, Finance"},
            {"name": "TEKsystems", "url": "https://teksystems.com", "specialization": "IT Staffing"},
            {"name": "Insight Global", "url": "https://insightglobal.com", "specialization": "IT Consulting"},
            {"name": "Modis", "url": "https://modis.com", "specialization": "IT, Engineering"}
        ],
        "top_hiring_companies": [
            {"name": "Google", "industry": "Tech", "h1b_sponsor": True, "careers_url": "https://careers.google.com"},
            {"name": "Microsoft", "industry": "Tech", "h1b_sponsor": True, "careers_url": "https://careers.microsoft.com"},
            {"name": "Amazon", "industry": "Tech", "h1b_sponsor": True, "careers_url": "https://amazon.jobs"},
            {"name": "Meta", "industry": "Tech", "h1b_sponsor": True, "careers_url": "https://metacareers.com"},
            {"name": "Apple", "industry": "Tech", "h1b_sponsor": True, "careers_url": "https://jobs.apple.com"},
            {"name": "Netflix", "industry": "Entertainment", "h1b_sponsor": True, "careers_url": "https://jobs.netflix.com"},
            {"name": "Salesforce", "industry": "SaaS", "h1b_sponsor": True, "careers_url": "https://salesforce.com/careers"},
            {"name": "Adobe", "industry": "Software", "h1b_sponsor": True, "careers_url": "https://adobe.com/careers"},
            {"name": "Uber", "industry": "Mobility", "h1b_sponsor": True, "careers_url": "https://uber.com/careers"},
            {"name": "Airbnb", "industry": "Travel", "h1b_sponsor": True, "careers_url": "https://careers.airbnb.com"}
        ],
        "monthly_expenses_estimate": {
            "single_sf_bay": 4500,
            "single_other": 2500,
            "family": 6000,
            "breakdown": {
                "rent_bay_area": "$2500-4000/month",
                "rent_other": "$1200-2000/month",
                "utilities": "$100-200/month",
                "food": "$400-800/month",
                "health_insurance": "Usually employer covered",
                "transport": "$100-500/month"
            }
        },
        "initial_settlement_cost": 10000,
        "pr_eligibility_years": 5,
        "pr_info": "Green Card through employer sponsorship (EB-2, EB-3). India backlog is 10+ years.",
        "citizenship_eligibility_years": 5,
        "tax_info": {
            "federal_tax": "10% - 37% (progressive)",
            "state_tax": "0% - 13% (varies by state)",
            "social_security": "6.2%",
            "medicare": "1.45%"
        },
        "common_challenges": [
            "H-1B lottery uncertainty",
            "Green card backlog for Indians (10+ years)",
            "Employer dependency on H-1B",
            "Very high cost in Bay Area/NYC",
            "Healthcare can be expensive",
            "No guaranteed paid leave"
        ],
        "tips_for_indians": [
            "Apply to multiple companies for H-1B",
            "Consider L-1 if working for MNC",
            "Look for companies that sponsor",
            "Build US network through LinkedIn",
            "Consider MS in USA for OPT advantage",
            "Save aggressively for green card wait"
        ],
        "salary_expectations": {
            "software_engineer_entry": "$100,000-150,000/year",
            "software_engineer_mid": "$150,000-220,000/year",
            "software_engineer_senior": "$220,000-350,000/year (with stock)",
            "data_scientist": "$120,000-200,000/year",
            "note": "Bay Area/NYC 20-30% higher"
        }
    },
    
    # =============================================================================
    # AUSTRALIA
    # =============================================================================
    {
        "country_name": "Australia",
        "visa_types": [
            {
                "name": "Skilled Independent Visa (189)",
                "description": "Points-based permanent visa without sponsorship",
                "requirements": [
                    "65+ points on skills assessment",
                    "Occupation on skilled occupation list",
                    "Skills assessment from relevant body",
                    "IELTS 6 each (Competent English)",
                    "Age under 45"
                ],
                "processing_time": "6-12 months",
                "validity": "Permanent",
                "cost": "AUD 4,115"
            },
            {
                "name": "Skilled Nominated Visa (190)",
                "description": "State-nominated permanent visa",
                "requirements": [
                    "State nomination",
                    "60+ points (state adds 5)",
                    "Commitment to live in nominating state"
                ],
                "processing_time": "6-12 months",
                "validity": "Permanent",
                "cost": "AUD 4,115"
            },
            {
                "name": "Temporary Skill Shortage Visa (482)",
                "description": "Employer-sponsored temporary visa",
                "requirements": [
                    "Job offer from Australian employer",
                    "Skills assessment",
                    "2 years work experience"
                ],
                "processing_time": "1-4 months",
                "validity": "2-4 years",
                "cost": "AUD 1,290-2,645"
            }
        ],
        "visa_process_steps": [
            "1. Check occupation on skilled list",
            "2. Get skills assessment from relevant body (ACS for IT)",
            "3. Take IELTS/PTE exam",
            "4. Create SkillSelect account and submit EOI",
            "5. Wait for invitation to apply",
            "6. Submit visa application",
            "7. Complete medical and police checks",
            "8. Receive visa grant"
        ],
        "visa_processing_time_weeks": 30,
        "visa_cost_usd": 3000,
        "employer_sponsorship_required": False,
        "popular_job_portals": [
            {"name": "LinkedIn Australia", "url": "https://linkedin.com/jobs", "description": "Best for networking", "is_recommended": True},
            {"name": "Seek", "url": "https://seek.com.au", "description": "Australia's #1 job site", "is_recommended": True},
            {"name": "Indeed Australia", "url": "https://indeed.com.au", "description": "Large aggregator", "is_recommended": True},
            {"name": "Jora", "url": "https://jora.com", "description": "Job aggregator"},
            {"name": "CareerOne", "url": "https://careerone.com.au", "description": "Australian job board"},
            {"name": "GradConnection", "url": "https://gradconnection.com", "description": "Graduate jobs"}
        ],
        "recruitment_agencies": [
            {"name": "Hays Australia", "url": "https://hays.com.au", "specialization": "IT, Finance"},
            {"name": "Michael Page", "url": "https://michaelpage.com.au", "specialization": "Tech, Finance"},
            {"name": "Robert Half", "url": "https://roberthalf.com.au", "specialization": "Finance, Tech"},
            {"name": "Randstad", "url": "https://randstad.com.au", "specialization": "IT, Engineering"}
        ],
        "top_hiring_companies": [
            {"name": "Atlassian", "industry": "Software", "careers_url": "https://atlassian.com/company/careers"},
            {"name": "Canva", "industry": "Design Tech", "careers_url": "https://canva.com/careers"},
            {"name": "Afterpay", "industry": "FinTech", "careers_url": "https://afterpay.com/careers"},
            {"name": "REA Group", "industry": "PropTech", "careers_url": "https://rea-group.com/careers"},
            {"name": "CommBank", "industry": "Banking", "careers_url": "https://commbank.com.au/careers"},
            {"name": "Telstra", "industry": "Telecom", "careers_url": "https://careers.telstra.com"}
        ],
        "monthly_expenses_estimate": {
            "single_sydney": 3000,
            "single_other": 2000,
            "family": 5000
        },
        "initial_settlement_cost": 8000,
        "pr_eligibility_years": 0,
        "citizenship_eligibility_years": 4,
        "salary_expectations": {
            "software_engineer_entry": "AUD 70,000-90,000/year",
            "software_engineer_mid": "AUD 100,000-140,000/year",
            "software_engineer_senior": "AUD 150,000-200,000/year"
        }
    },
    
    # =============================================================================
    # SINGAPORE
    # =============================================================================
    {
        "country_name": "Singapore",
        "visa_types": [
            {
                "name": "Employment Pass (EP)",
                "description": "For professionals earning SGD 5,000+/month",
                "requirements": [
                    "Job offer from Singapore employer",
                    "Minimum salary SGD 5,000/month (higher for experienced)",
                    "Good educational qualifications",
                    "Pass COMPASS framework scoring"
                ],
                "processing_time": "2-8 weeks",
                "validity": "2 years (renewable)",
                "cost": "SGD 105"
            },
            {
                "name": "S Pass",
                "description": "For mid-skilled workers",
                "requirements": [
                    "Minimum salary SGD 3,000/month",
                    "Diploma or equivalent",
                    "Company quota requirements"
                ],
                "processing_time": "2-8 weeks",
                "validity": "2 years",
                "cost": "SGD 105"
            },
            {
                "name": "Tech.Pass",
                "description": "For top tech talent",
                "requirements": [
                    "SGD 20,000+ salary OR",
                    "Leadership role at top tech company OR",
                    "Key role in funded startup"
                ],
                "processing_time": "4-8 weeks",
                "validity": "2 years",
                "cost": "SGD 105"
            }
        ],
        "popular_job_portals": [
            {"name": "LinkedIn Singapore", "url": "https://linkedin.com/jobs", "is_recommended": True},
            {"name": "JobStreet", "url": "https://jobstreet.com.sg", "is_recommended": True},
            {"name": "Indeed Singapore", "url": "https://indeed.com.sg"},
            {"name": "MyCareersFuture", "url": "https://mycareersfuture.gov.sg", "description": "Government portal"},
            {"name": "NodeFlair", "url": "https://nodeflair.com", "description": "Tech jobs"}
        ],
        "top_hiring_companies": [
            {"name": "Google Singapore", "industry": "Tech"},
            {"name": "Meta Singapore", "industry": "Tech"},
            {"name": "Grab", "industry": "Mobility/FinTech"},
            {"name": "Sea Group", "industry": "Gaming/E-commerce"},
            {"name": "Shopee", "industry": "E-commerce"},
            {"name": "Lazada", "industry": "E-commerce"},
            {"name": "DBS Bank", "industry": "Banking"},
            {"name": "ByteDance", "industry": "Tech"}
        ],
        "monthly_expenses_estimate": {
            "single": 2500,
            "family": 5000
        },
        "pr_eligibility_years": 2,
        "salary_expectations": {
            "software_engineer_entry": "SGD 5,000-8,000/month",
            "software_engineer_mid": "SGD 8,000-14,000/month",
            "software_engineer_senior": "SGD 14,000-25,000/month"
        },
        "tips_for_indians": [
            "EP requires passing COMPASS framework",
            "Salary expectations rising - minimum SGD 5,000",
            "Competition is high from other nationalities",
            "Network through Singapore tech communities",
            "Consider larger companies for easier EP approval"
        ]
    },
    
    # =============================================================================
    # UK
    # =============================================================================
    {
        "country_name": "United Kingdom",
        "visa_types": [
            {
                "name": "Skilled Worker Visa",
                "description": "For workers with job offer from licensed sponsor",
                "requirements": [
                    "Job offer from licensed sponsor",
                    "Job at appropriate skill level (RQF 3+)",
                    "Minimum salary £26,200 or going rate",
                    "English proficiency (B1)",
                    "Certificate of Sponsorship"
                ],
                "processing_time": "3-8 weeks",
                "validity": "Up to 5 years",
                "cost": "£719-1,500"
            },
            {
                "name": "Global Talent Visa",
                "description": "For leaders/potential leaders in tech",
                "requirements": [
                    "Endorsement from Tech Nation",
                    "Evidence of exceptional talent/promise"
                ],
                "processing_time": "8 weeks",
                "validity": "5 years",
                "cost": "£623"
            },
            {
                "name": "High Potential Individual Visa",
                "description": "For recent graduates of top universities",
                "requirements": [
                    "Graduated from top global university in last 5 years",
                    "Not previously had UK visa"
                ],
                "processing_time": "3 weeks",
                "validity": "2 years (3 for PhD)",
                "cost": "£715"
            }
        ],
        "popular_job_portals": [
            {"name": "LinkedIn UK", "url": "https://linkedin.com/jobs", "is_recommended": True},
            {"name": "Indeed UK", "url": "https://indeed.co.uk", "is_recommended": True},
            {"name": "Reed", "url": "https://reed.co.uk", "is_recommended": True},
            {"name": "Totaljobs", "url": "https://totaljobs.com"},
            {"name": "CWJobs", "url": "https://cwjobs.co.uk", "description": "IT Jobs"},
            {"name": "Adzuna", "url": "https://adzuna.co.uk"}
        ],
        "top_hiring_companies": [
            {"name": "Google UK", "industry": "Tech"},
            {"name": "Amazon UK", "industry": "Tech/E-commerce"},
            {"name": "Meta UK", "industry": "Tech"},
            {"name": "Revolut", "industry": "FinTech"},
            {"name": "Monzo", "industry": "FinTech"},
            {"name": "Deliveroo", "industry": "Food Tech"},
            {"name": "Wise", "industry": "FinTech"},
            {"name": "Barclays", "industry": "Banking"},
            {"name": "HSBC", "industry": "Banking"}
        ],
        "monthly_expenses_estimate": {
            "single_london": 2500,
            "single_other": 1500,
            "family": 4000
        },
        "pr_eligibility_years": 5,
        "citizenship_eligibility_years": 6,
        "salary_expectations": {
            "software_engineer_entry": "£35,000-55,000/year",
            "software_engineer_mid": "£55,000-85,000/year",
            "software_engineer_senior": "£85,000-130,000/year"
        }
    }
]


def seed_detailed_country_data():
    """Seed detailed country migration data"""
    logger.info("🌍 Adding detailed country migration data...")
    
    init_db()
    db = SessionLocal()
    
    try:
        for guide_data in DETAILED_MIGRATION_GUIDES:
            country_name = guide_data.get("country_name")
            
            # Serialize JSON fields for SQLite
            serialized_data = serialize_json_fields(guide_data)
            
            # Check if exists
            existing = db.query(CountryMigration).filter(
                CountryMigration.country_name == country_name
            ).first()
            
            if existing:
                # Update existing
                for key, value in serialized_data.items():
                    setattr(existing, key, value)
                logger.info(f"📝 Updated: {country_name}")
            else:
                # Create new
                guide = CountryMigration(**serialized_data)
                db.add(guide)
                logger.info(f"➕ Added: {country_name}")
        
        db.commit()
        logger.info(f"✅ Processed {len(DETAILED_MIGRATION_GUIDES)} country guides!")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_detailed_country_data()

