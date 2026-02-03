"""
Comprehensive Country Migration Guides
Detailed information for all major destinations
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import SessionLocal, init_db
from app.models.country import CountryMigration
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COMPREHENSIVE_MIGRATION_GUIDES = [
    # ==================== UAE / DUBAI ====================
    {
        "country_name": "United Arab Emirates",
        "visa_types": [
            {
                "name": "Employment Visa",
                "description": "Standard work visa sponsored by employer",
                "requirements": ["Job offer from UAE company", "Valid passport (6+ months)", "Educational certificates attested", "Medical fitness certificate", "Emirates ID application"],
                "processing_time": "2-4 weeks",
                "validity": "2-3 years (renewable)"
            },
            {
                "name": "Green Visa",
                "description": "Self-sponsored 5-year visa for skilled workers",
                "requirements": ["Bachelor's degree or equivalent", "Current job in skill level 1-3", "Salary AED 15,000+ per month", "Valid employment contract"],
                "processing_time": "2-3 weeks",
                "validity": "5 years"
            },
            {
                "name": "Golden Visa",
                "description": "10-year residency for exceptional talents",
                "requirements": ["Specialized talents in AI, Big Data, etc.", "Salary AED 30,000+ OR PhD degree", "Endorsement from relevant ministry"],
                "processing_time": "2-4 weeks",
                "validity": "10 years"
            },
            {
                "name": "Freelance/Self-Employment Visa",
                "description": "For freelancers and consultants",
                "requirements": ["Freelance permit from free zone", "Portfolio/work samples", "Bank statement"],
                "processing_time": "1-2 weeks",
                "validity": "1-3 years"
            }
        ],
        "visa_process_steps": [
            "1. Get job offer from UAE employer",
            "2. Employer applies for employment permit",
            "3. Receive entry permit (pink visa)",
            "4. Travel to UAE within 60 days",
            "5. Complete medical fitness test",
            "6. Apply for Emirates ID",
            "7. Stamp visa in passport (residence visa)",
            "8. Open bank account",
            "9. Apply for UAE driving license (if needed)"
        ],
        "visa_processing_time_weeks": 3,
        "visa_cost_usd": 500,
        "employer_sponsorship_required": True,
        "popular_job_portals": [
            {"name": "LinkedIn UAE", "url": "https://linkedin.com/jobs", "description": "Best for professional/tech roles", "tips": "Set location to Dubai/UAE, connect with recruiters"},
            {"name": "Bayt", "url": "https://bayt.com", "description": "Largest job portal in Middle East", "tips": "Upload CV, apply to multiple jobs daily"},
            {"name": "GulfTalent", "url": "https://gulftalent.com", "description": "Premium Gulf jobs", "tips": "Good for senior positions"},
            {"name": "Naukrigulf", "url": "https://naukrigulf.com", "description": "Popular among Indians", "tips": "Sister site of Naukri.com"},
            {"name": "Indeed UAE", "url": "https://ae.indeed.com", "description": "Job aggregator", "tips": "Set up job alerts"},
            {"name": "Dubizzle Jobs", "url": "https://dubizzle.com/jobs", "description": "Local classifieds with jobs", "tips": "Good for direct employer listings"},
            {"name": "Monster Gulf", "url": "https://monstergulf.com", "description": "International job site", "tips": "Apply to multiple jobs"}
        ],
        "recruitment_agencies": [
            {"name": "Robert Half UAE", "url": "https://roberthalf.ae", "specialization": "Finance, Tech", "free_for_candidates": True},
            {"name": "Michael Page UAE", "url": "https://michaelpage.ae", "specialization": "All sectors", "free_for_candidates": True},
            {"name": "Hays UAE", "url": "https://hays.ae", "specialization": "IT, Engineering", "free_for_candidates": True},
            {"name": "Charterhouse", "url": "https://charterhouse.ae", "specialization": "Banking, Finance", "free_for_candidates": True},
            {"name": "Adecco Middle East", "url": "https://adeccome.com", "specialization": "All sectors", "free_for_candidates": True},
            {"name": "Talent360", "url": "https://talent-360.me", "specialization": "Tech, Digital", "free_for_candidates": True}
        ],
        "companies_hiring_indians": [
            {"name": "Emirates NBD", "industry": "Banking", "roles": "Software Engineers, Data Analysts"},
            {"name": "Mashreq Bank", "industry": "Banking", "roles": "Developers, DevOps"},
            {"name": "Careem", "industry": "Tech/Mobility", "roles": "Full Stack, Backend, ML"},
            {"name": "Noon", "industry": "E-commerce", "roles": "Engineers, Data Scientists"},
            {"name": "Talabat", "industry": "Food Tech", "roles": "Backend, Mobile, Data"},
            {"name": "Amazon UAE", "industry": "Tech/E-commerce", "roles": "SDEs, TPMs"},
            {"name": "Microsoft UAE", "industry": "Tech", "roles": "Cloud, Support, Engineering"},
            {"name": "IBM UAE", "industry": "IT Services", "roles": "Consultants, Architects"},
            {"name": "Oracle UAE", "industry": "Tech", "roles": "Cloud Engineers, Developers"},
            {"name": "du (EITC)", "industry": "Telecom", "roles": "Network, Software Engineers"},
            {"name": "Etisalat", "industry": "Telecom", "roles": "IT, Network Engineers"},
            {"name": "Majid Al Futtaim", "industry": "Retail/Tech", "roles": "Digital, E-commerce"},
            {"name": "ENBD", "industry": "Banking", "roles": "FinTech, Developers"},
            {"name": "First Abu Dhabi Bank", "industry": "Banking", "roles": "Tech, Data"}
        ],
        "resume_format": "Standard international CV format, 1-2 pages, no photo required but accepted",
        "resume_tips": [
            "Keep it concise - 1-2 pages max",
            "Include nationality and visa status",
            "Mention notice period",
            "Add expected salary range (optional)",
            "Highlight UAE/GCC experience if any",
            "Include LinkedIn profile URL",
            "List certifications prominently"
        ],
        "cover_letter_required": False,
        "documents_required": [
            "Valid passport (6+ months validity)",
            "Passport-size photos (white background)",
            "Educational certificates (attested by UAE embassy)",
            "Experience letters from previous employers",
            "Police clearance certificate (PCC)",
            "Medical fitness certificate (done in UAE)",
            "Proof of accommodation (tenancy contract)"
        ],
        "document_attestation_required": True,
        "monthly_expenses_estimate": {
            "single": {"rent": 4000, "food": 1500, "transport": 500, "utilities": 500, "misc": 1000, "total_aed": 7500, "total_usd": 2000},
            "family": {"rent": 8000, "food": 3000, "transport": 1000, "utilities": 800, "school": 3000, "misc": 2000, "total_aed": 17800, "total_usd": 4800}
        },
        "initial_settlement_cost": 8000,
        "relocation_checklist": [
            "Get documents attested before leaving India",
            "Book initial accommodation (hotel/Airbnb for 2 weeks)",
            "Carry original certificates",
            "Get international driving permit",
            "Inform bank about international travel",
            "Get health insurance (temporary)",
            "Research areas to live based on workplace",
            "Join WhatsApp groups for accommodation"
        ],
        "initial_accommodation_tips": "Stay in hotel/Airbnb for first 2 weeks. Use Dubizzle, Bayut for apartment hunting. Popular areas: Business Bay, JLT, Discovery Gardens (budget), Downtown (premium).",
        "banking_guide": "Open account at Emirates NBD, Mashreq, or ADCB. Requires Emirates ID, passport, employment letter, salary certificate. Takes 1-2 weeks. Get debit card for daily use.",
        "mobile_sim_guide": "Get prepaid SIM from du or Etisalat at airport. Postpaid requires Emirates ID. Plans start from AED 75/month. Data is expensive compared to India.",
        "language_requirements": {"work": "English (Arabic is a plus but not required for tech)", "daily_life": "English widely spoken"},
        "pr_eligibility_years": 10,
        "pr_requirements": ["Golden Visa for 10-year residency", "No permanent residency like Western countries", "Visa tied to employment/sponsor"],
        "citizenship_eligibility_years": None,
        "citizenship_requirements": ["UAE citizenship rarely granted", "30+ years residence", "Arabic fluency", "Special contributions to UAE"],
        "income_tax_rate": "0% personal income tax",
        "tax_treaties_with_india": True,
        "tax_tips": [
            "No personal income tax in UAE",
            "5% VAT on goods and services",
            "You may need to file taxes in India if staying <182 days",
            "Corporate tax 9% (introduced 2023) doesn't affect employees"
        ],
        "healthcare_system": "Private healthcare, insurance mandatory through employer. Good quality hospitals. Popular: Aster, NMC, Mediclinic. Emergency care available 24/7.",
        "education_system": "Private schools (expensive). Popular curricula: CBSE (Indian), British, American, IB. School fees: AED 15,000 - 80,000 per year.",
        "indian_community": "Largest expat community. 3.5 million+ Indians. Strong community networks. Many Indian restaurants, grocery stores, temples, cultural events.",
        "indian_groceries_availability": "Excellent - Lulu Hypermarket, Carrefour, Indian grocery stores everywhere. All Indian brands available.",
        "common_challenges": [
            "High rent costs (30-40% of salary)",
            "Hot climate (40-50°C in summer)",
            "Limited public transport (improving with Metro)",
            "Visa tied to employer (changing)",
            "No permanent residency path",
            "Expensive healthcare without insurance"
        ],
        "tips_for_indians": [
            "Negotiate housing allowance in salary",
            "Ask for annual air ticket to India",
            "Start apartment hunting immediately after arrival",
            "Get attestation done in India before leaving",
            "Join Facebook/WhatsApp groups for accommodation",
            "Keep 3 months expenses as emergency fund",
            "Don't resign before finding new job (visa issues)"
        ],
        "things_to_avoid": [
            "Don't share fake documents",
            "Avoid salary discussions with colleagues (cultural)",
            "Don't badmouth employer publicly",
            "Avoid bounced cheques (criminal offense)",
            "Don't overstay visa",
            "Avoid public display of affection"
        ],
        "interview_process": [
            "Usually 2-4 rounds",
            "HR screening call",
            "Technical rounds (coding/system design)",
            "Manager/Team lead round",
            "HR final round (salary discussion)",
            "Some companies do case studies/presentations"
        ],
        "salary_negotiation_tips": [
            "Research market rates on Bayt, GulfTalent",
            "Ask for housing allowance (AED 5,000-15,000/month)",
            "Request annual air tickets for family",
            "Education allowance for kids",
            "Medical insurance for family",
            "Annual bonus (1-3 months typical)"
        ],
        "facebook_groups": [
            {"name": "Indians in Dubai", "url": "https://facebook.com/groups/indiansindubai"},
            {"name": "Jobs in UAE", "url": "https://facebook.com/groups/jobsinuae"},
            {"name": "Dubai IT Professionals", "url": "https://facebook.com/groups/dubaiitprofessionals"},
            {"name": "Room/Flat for Rent Dubai", "url": "https://facebook.com/groups/roomsindubai"}
        ],
        "whatsapp_telegram_groups": [
            {"name": "Dubai Jobs WhatsApp", "description": "Job postings shared daily"},
            {"name": "UAE Indians Telegram", "description": "Community discussions"}
        ],
        "youtube_channels": [
            {"name": "Dubai OFW", "url": "https://youtube.com/@DubaiOFW", "description": "Life in Dubai"},
            {"name": "Syed Waqar", "url": "https://youtube.com/@syedwaqar", "description": "Dubai jobs guide"},
            {"name": "Dubai Life", "url": "https://youtube.com/@dubailife", "description": "Living in Dubai"}
        ],
        "useful_websites": [
            {"name": "MOHRE", "url": "https://mohre.gov.ae", "description": "Ministry of Human Resources - Official employment info"},
            {"name": "ICA", "url": "https://ica.gov.ae", "description": "Federal Authority for Identity - Visa info"},
            {"name": "Dubai Economy", "url": "https://dubaided.gov.ae", "description": "Business setup info"}
        ],
        "current_demand_sectors": ["FinTech", "AI/ML", "Cloud Computing", "Cybersecurity", "E-commerce", "Healthcare Tech", "PropTech"],
        "success_stories": [
            {"title": "From TCS India to Careem Dubai", "summary": "5 LPA to 40 LPA in 2 years"},
            {"title": "Backend Developer to Tech Lead at Noon", "summary": "Career growth in UAE startup"}
        ]
    },
    
    # ==================== GERMANY (Enhanced) ====================
    {
        "country_name": "Germany",
        "visa_types": [
            {
                "name": "EU Blue Card",
                "description": "For highly qualified professionals - most popular for IT",
                "requirements": ["University degree (recognized in Germany)", "Job offer with minimum €58,400 salary (€45,552 for STEM shortage occupations)", "Health insurance", "Valid passport"],
                "processing_time": "4-8 weeks",
                "validity": "4 years (leads to PR)"
            },
            {
                "name": "Job Seeker Visa",
                "description": "6 months to search for job in Germany",
                "requirements": ["University degree", "Proof of funds (€947/month blocked account)", "Health insurance", "CV and motivation letter", "No job offer needed"],
                "processing_time": "8-12 weeks",
                "validity": "6 months"
            },
            {
                "name": "ICT (Intra-Company Transfer)",
                "description": "For transfers within same company",
                "requirements": ["Working for company 6+ months", "Transfer to German branch", "Manager/Specialist role"],
                "processing_time": "4-6 weeks",
                "validity": "3 years"
            },
            {
                "name": "Skilled Worker Visa",
                "description": "For vocational training holders",
                "requirements": ["Recognized vocational qualification", "Job offer", "German language skills often required"],
                "processing_time": "6-10 weeks",
                "validity": "4 years"
            }
        ],
        "visa_process_steps": [
            "1. Get job offer from German employer",
            "2. Open blocked account (Sperrkonto) with €11,364",
            "3. Get health insurance (public: TK, AOK or private)",
            "4. Get degree evaluated at anabin.kmk.org",
            "5. Book VFS/Embassy appointment (book early - 2-3 months wait)",
            "6. Gather all documents (original + copies + translations)",
            "7. Attend visa interview",
            "8. Wait for visa processing (4-8 weeks)",
            "9. Receive visa and book flights",
            "10. Register at Bürgeramt within 2 weeks of arrival (Anmeldung)",
            "11. Apply for residence permit (Aufenthaltstitel)"
        ],
        "visa_processing_time_weeks": 8,
        "visa_cost_usd": 100,
        "employer_sponsorship_required": True,
        "popular_job_portals": [
            {"name": "LinkedIn Germany", "url": "https://linkedin.com/jobs", "description": "Best for English-speaking tech roles", "tips": "Filter by 'English' in job description"},
            {"name": "StepStone", "url": "https://stepstone.de", "description": "Major German job portal", "tips": "Many jobs in German only"},
            {"name": "Indeed Germany", "url": "https://de.indeed.com", "description": "Job aggregator", "tips": "Search 'English' + your skill"},
            {"name": "Xing", "url": "https://xing.com", "description": "German LinkedIn equivalent", "tips": "Good for local networking"},
            {"name": "Stack Overflow Jobs", "url": "https://stackoverflow.com/jobs", "description": "Developer-focused", "tips": "Filter by Germany"},
            {"name": "Berlin Startup Jobs", "url": "https://berlinstartupjobs.com", "description": "Startup ecosystem jobs", "tips": "Mostly English-speaking"},
            {"name": "Glassdoor Germany", "url": "https://glassdoor.de", "description": "Jobs + company reviews", "tips": "Research salaries"},
            {"name": "Make it in Germany", "url": "https://make-it-in-germany.com", "description": "Official government portal", "tips": "Job listings + visa info"},
            {"name": "Relocate.me", "url": "https://relocate.me", "description": "Visa sponsorship jobs", "tips": "Companies willing to sponsor"}
        ],
        "recruitment_agencies": [
            {"name": "Michael Page Germany", "url": "https://michaelpage.de", "specialization": "IT, Finance", "free_for_candidates": True},
            {"name": "Hays Germany", "url": "https://hays.de", "specialization": "IT, Engineering", "free_for_candidates": True},
            {"name": "Robert Half Germany", "url": "https://roberthalf.de", "specialization": "Finance, IT", "free_for_candidates": True},
            {"name": "Computer Futures", "url": "https://computerfutures.com/de", "specialization": "IT only", "free_for_candidates": True},
            {"name": "Randstad Germany", "url": "https://randstad.de", "specialization": "All sectors", "free_for_candidates": True}
        ],
        "companies_hiring_indians": [
            {"name": "SAP", "industry": "Enterprise Software", "roles": "Developers, Consultants", "locations": "Walldorf, Berlin"},
            {"name": "Siemens", "industry": "Industrial Tech", "roles": "Engineers, Developers", "locations": "Munich, Berlin"},
            {"name": "BMW", "industry": "Automotive", "roles": "Software Engineers", "locations": "Munich"},
            {"name": "Mercedes-Benz", "industry": "Automotive", "roles": "IT, Engineering", "locations": "Stuttgart"},
            {"name": "Zalando", "industry": "E-commerce", "roles": "Full Stack, Data", "locations": "Berlin"},
            {"name": "Delivery Hero", "industry": "Food Tech", "roles": "Backend, Mobile", "locations": "Berlin"},
            {"name": "N26", "industry": "FinTech", "roles": "Engineers, Data", "locations": "Berlin"},
            {"name": "Deutsche Bank", "industry": "Banking", "roles": "IT, Risk", "locations": "Frankfurt"},
            {"name": "Booking.com", "industry": "Travel Tech", "roles": "Developers", "locations": "Berlin"},
            {"name": "Amazon Germany", "industry": "Tech", "roles": "SDEs, TPMs", "locations": "Berlin, Munich"},
            {"name": "Google Germany", "industry": "Tech", "roles": "Engineers", "locations": "Munich, Berlin"},
            {"name": "Microsoft Germany", "industry": "Tech", "roles": "Cloud, Support", "locations": "Munich"}
        ],
        "resume_format": "German-style CV (Lebenslauf) with photo, date of birth, or Europass format",
        "resume_tips": [
            "Include professional photo (business attire)",
            "Add date of birth and nationality",
            "Keep it 1-2 pages",
            "Include German language level (A1, B1, etc.)",
            "List education in reverse chronological order",
            "Certifications are valued highly",
            "Mention visa status/work permit"
        ],
        "cover_letter_required": True,
        "documents_required": [
            "Valid passport (6+ months validity)",
            "Biometric photos (35x45mm)",
            "University degree (original + certified translation)",
            "Degree evaluation from anabin or ZAB",
            "Job offer letter/employment contract",
            "Proof of blocked account (€11,364)",
            "Health insurance certificate",
            "Rental agreement or proof of accommodation",
            "CV in English/German",
            "Cover letter",
            "Previous employment certificates"
        ],
        "monthly_expenses_estimate": {
            "single": {"rent": 800, "health_insurance": 100, "food": 300, "transport": 80, "utilities": 150, "misc": 200, "total_eur": 1630, "total_usd": 1800},
            "family": {"rent": 1400, "health_insurance": 200, "food": 600, "transport": 150, "utilities": 200, "childcare": 400, "misc": 350, "total_eur": 3300, "total_usd": 3600}
        },
        "initial_settlement_cost": 5000,
        "language_requirements": {"work": "English for most tech jobs (B2 German helpful)", "integration": "A1 German for residence permit extension", "pr": "B1 German required"},
        "pr_eligibility_years": 4,
        "pr_requirements": ["21 months with Blue Card (if B1 German) or 33 months", "Pension contributions", "Basic German (A1 or B1)", "Stable income"],
        "citizenship_eligibility_years": 8,
        "citizenship_requirements": ["8 years residence (6 with integration course)", "B1 German", "Pass citizenship test", "Renounce Indian citizenship (dual not allowed)"],
        "income_tax_rate": "14% - 45% progressive (42% above €58k)",
        "tax_treaties_with_india": True,
        "common_challenges": [
            "German bureaucracy (lots of paperwork)",
            "Finding apartment is very difficult",
            "German language barrier in daily life",
            "Cold winters (especially for South Indians)",
            "Everything closed on Sundays",
            "Slow internet compared to expectations",
            "Bank appointments take weeks"
        ],
        "tips_for_indians": [
            "Start German on Duolingo before moving",
            "Open blocked account 2 months before visa appointment",
            "Book VFS appointment early (slots fill fast)",
            "Get WG (shared apartment) initially",
            "Apply for Anmeldung appointment before arriving",
            "Get liability insurance (Haftpflichtversicherung)",
            "Church tax - declare 'no religion' if applicable"
        ],
        "facebook_groups": [
            {"name": "Indians in Germany", "url": "https://facebook.com/groups/indiansingermany"},
            {"name": "IT Jobs Germany", "url": "https://facebook.com/groups/itjobsgermany"},
            {"name": "Berlin Indians", "url": "https://facebook.com/groups/berlinindians"},
            {"name": "WG Gesucht Berlin", "url": "https://facebook.com/groups/wggesuchtberlin"}
        ],
        "youtube_channels": [
            {"name": "Bharat in Germany", "url": "https://youtube.com/@bharatingermany", "description": "Visa process, life in Germany"},
            {"name": "Nikhilesh Dhure", "url": "https://youtube.com/@nikhileshdhure", "description": "Jobs, visa, tips"},
            {"name": "Simple Germany", "url": "https://youtube.com/@simplegermany", "description": "Official info channel"}
        ]
    },
    
    # ==================== CANADA (Enhanced) ====================
    {
        "country_name": "Canada",
        "visa_types": [
            {
                "name": "Express Entry - Federal Skilled Worker",
                "description": "Points-based immigration for skilled workers",
                "requirements": ["67+ points on FSW grid", "1+ year skilled work experience", "IELTS CLB 7+", "Education credential assessment (ECA)"],
                "processing_time": "6 months",
                "validity": "Permanent Residence"
            },
            {
                "name": "Provincial Nominee Program (PNP)",
                "description": "Province-specific immigration",
                "requirements": ["Nomination from province", "Meet provincial criteria", "Job offer may be required"],
                "processing_time": "12-18 months",
                "validity": "Permanent Residence"
            },
            {
                "name": "Work Permit (LMIA)",
                "description": "Temporary work permit with employer sponsorship",
                "requirements": ["Positive LMIA from employer", "Job offer", "Relevant qualifications"],
                "processing_time": "2-4 months",
                "validity": "Tied to job duration"
            },
            {
                "name": "Global Talent Stream",
                "description": "Fast-track for tech workers",
                "requirements": ["Job in eligible tech occupation", "Employer is GTS-designated"],
                "processing_time": "2 weeks",
                "validity": "2-3 years"
            },
            {
                "name": "Start-up Visa",
                "description": "For entrepreneurs with innovative business",
                "requirements": ["Support from designated organization", "Meet language requirements", "Sufficient funds"],
                "processing_time": "12-16 months",
                "validity": "Permanent Residence"
            }
        ],
        "visa_process_steps": [
            "1. Take IELTS/CELPIP and score CLB 7+ (aim for 8+)",
            "2. Get Educational Credential Assessment (WES recommended)",
            "3. Create Express Entry profile",
            "4. Calculate CRS score",
            "5. Get provincial nomination if needed (600 points boost)",
            "6. Wait for Invitation to Apply (ITA)",
            "7. Submit complete PR application within 60 days",
            "8. Complete medical exam",
            "9. Provide biometrics",
            "10. Wait for background check",
            "11. Receive Confirmation of Permanent Residence (COPR)",
            "12. Land in Canada and get PR card"
        ],
        "visa_processing_time_weeks": 26,
        "visa_cost_usd": 2000,
        "employer_sponsorship_required": False,
        "popular_job_portals": [
            {"name": "LinkedIn Canada", "url": "https://linkedin.com/jobs", "description": "Best for networking and jobs", "tips": "Connect with recruiters, use 'Open to Work'"},
            {"name": "Indeed Canada", "url": "https://indeed.ca", "description": "Largest job aggregator", "tips": "Set up multiple job alerts"},
            {"name": "Job Bank", "url": "https://jobbank.gc.ca", "description": "Official government portal", "tips": "Shows LMIA-approved jobs"},
            {"name": "Glassdoor Canada", "url": "https://glassdoor.ca", "description": "Jobs + salary research", "tips": "Research company reviews"},
            {"name": "Workopolis", "url": "https://workopolis.com", "description": "Canadian job board", "tips": "Good for entry-level"},
            {"name": "Monster Canada", "url": "https://monster.ca", "description": "Large job board", "tips": "Upload resume for visibility"},
            {"name": "Tech Jobs Canada", "url": "https://techjobscanada.com", "description": "Tech-focused jobs", "tips": "Startup listings"},
            {"name": "AngelList", "url": "https://angel.co/jobs", "description": "Startup jobs", "tips": "Filter by Canada + Visa sponsor"}
        ],
        "recruitment_agencies": [
            {"name": "Robert Half Canada", "url": "https://roberthalf.ca", "specialization": "IT, Finance", "free_for_candidates": True},
            {"name": "Hays Canada", "url": "https://hays.ca", "specialization": "IT, Engineering", "free_for_candidates": True},
            {"name": "Randstad Canada", "url": "https://randstad.ca", "specialization": "All sectors", "free_for_candidates": True},
            {"name": "TEKsystems Canada", "url": "https://teksystems.ca", "specialization": "IT only", "free_for_candidates": True},
            {"name": "Procom", "url": "https://procom.ca", "specialization": "IT, Engineering", "free_for_candidates": True}
        ],
        "companies_hiring_indians": [
            {"name": "Amazon Canada", "industry": "Tech", "roles": "SDEs, Data Engineers", "locations": "Vancouver, Toronto"},
            {"name": "Google Canada", "industry": "Tech", "roles": "Engineers", "locations": "Toronto, Waterloo, Montreal"},
            {"name": "Microsoft Canada", "industry": "Tech", "roles": "All tech roles", "locations": "Vancouver"},
            {"name": "Shopify", "industry": "E-commerce", "roles": "Full Stack, Backend", "locations": "Ottawa, Toronto (Remote)"},
            {"name": "RBC", "industry": "Banking", "roles": "Developers, Data", "locations": "Toronto"},
            {"name": "TD Bank", "industry": "Banking", "roles": "IT, Risk", "locations": "Toronto"},
            {"name": "Scotiabank", "industry": "Banking", "roles": "Digital Banking", "locations": "Toronto"},
            {"name": "Uber Canada", "industry": "Mobility", "roles": "Engineers", "locations": "Toronto"},
            {"name": "Wealthsimple", "industry": "FinTech", "roles": "Engineers", "locations": "Toronto"},
            {"name": "Clio", "industry": "LegalTech", "roles": "Engineers", "locations": "Vancouver, Calgary"},
            {"name": "Hootsuite", "industry": "SaaS", "roles": "Developers", "locations": "Vancouver"},
            {"name": "OpenText", "industry": "Enterprise Software", "roles": "Developers", "locations": "Waterloo"}
        ],
        "resume_format": "Canadian-style: No photo, no personal info, achievement-focused",
        "resume_tips": [
            "NO photo - discrimination laws",
            "NO date of birth, marital status",
            "Use Canadian spelling (honour, colour)",
            "Focus on achievements with metrics",
            "2 pages maximum",
            "Include Canadian address if available",
            "ATS-friendly format"
        ],
        "documents_required": [
            "Valid passport",
            "IELTS/CELPIP score report",
            "ECA report (WES/IQAS)",
            "Police clearance certificates (all countries lived 6+ months)",
            "Medical exam results",
            "Proof of funds (CAD 13,757 single, CAD 17,127 couple)",
            "Reference letters from employers",
            "Education transcripts and certificates"
        ],
        "monthly_expenses_estimate": {
            "single_toronto": {"rent": 2200, "food": 600, "transport": 150, "utilities": 150, "phone_internet": 100, "misc": 300, "total_cad": 3500, "total_usd": 2600},
            "family_toronto": {"rent": 3000, "food": 1000, "transport": 300, "utilities": 200, "childcare": 1500, "misc": 500, "total_cad": 6500, "total_usd": 4800},
            "single_calgary": {"rent": 1400, "food": 500, "transport": 100, "utilities": 150, "misc": 300, "total_cad": 2450, "total_usd": 1800}
        },
        "initial_settlement_cost": 8000,
        "language_requirements": {"express_entry": "CLB 7+ (IELTS 6.0 each)", "provincial": "Varies", "citizenship": "CLB 4"},
        "pr_eligibility_years": 0,
        "citizenship_eligibility_years": 3,
        "citizenship_requirements": ["PR for 3 years (1095 days in 5 years)", "CLB 4 English/French", "Pass citizenship test", "File taxes for 3 years", "No criminality"],
        "income_tax_rate": "Federal 15%-33% + Provincial 5%-25%",
        "tax_treaties_with_india": True,
        "common_challenges": [
            "Canadian work experience catch-22",
            "Extreme cold (-30°C in winter)",
            "High cost of living (Toronto, Vancouver)",
            "Long PR processing times",
            "Recognition of foreign credentials",
            "Initial unemployment period"
        ],
        "tips_for_indians": [
            "Start IELTS preparation 6 months early - aim for 8+",
            "Apply for ECA immediately after deciding",
            "Consider smaller cities (Calgary, Ottawa) for lower CRS cutoffs",
            "Get Canadian certifications (PMP, AWS) for extra points",
            "Network heavily on LinkedIn before landing",
            "Keep 6 months living expenses as backup",
            "Consider doing Masters for extra 30 CRS points"
        ],
        "facebook_groups": [
            {"name": "Indians in Canada", "url": "https://facebook.com/groups/indiansincanada"},
            {"name": "Express Entry Canada", "url": "https://facebook.com/groups/expressentry"},
            {"name": "Toronto Indians", "url": "https://facebook.com/groups/torontoindians"},
            {"name": "Canada Immigration Forum", "url": "https://facebook.com/groups/canadaimmigration"}
        ],
        "youtube_channels": [
            {"name": "ImmigrationTeddy", "url": "https://youtube.com/@immigrationteddy", "description": "PR process updates"},
            {"name": "Canadian Immigrant", "url": "https://youtube.com/@canadianimmigrant", "description": "Settlement tips"},
            {"name": "Desi in Canada", "url": "https://youtube.com/@desiincanada", "description": "Indian perspective"}
        ]
    },

    # ==================== AUSTRALIA ====================
    {
        "country_name": "Australia",
        "visa_types": [
            {
                "name": "Subclass 189 - Skilled Independent",
                "description": "Points-tested PR visa, no sponsorship needed",
                "requirements": ["Occupation on skilled list", "Skills assessment", "65+ points", "IELTS 6+ each", "Under 45 years"],
                "processing_time": "6-12 months",
                "validity": "Permanent"
            },
            {
                "name": "Subclass 190 - Skilled Nominated",
                "description": "State-nominated PR visa",
                "requirements": ["State nomination", "65+ points (190 gives 5 points)", "Occupation on state list"],
                "processing_time": "6-9 months",
                "validity": "Permanent"
            },
            {
                "name": "Subclass 491 - Skilled Regional",
                "description": "Regional area provisional visa",
                "requirements": ["Regional nomination", "65+ points", "Live/work in regional area"],
                "processing_time": "6-12 months",
                "validity": "5 years (PR pathway)"
            },
            {
                "name": "Subclass 482 - TSS (Temporary Skill Shortage)",
                "description": "Employer-sponsored temporary visa",
                "requirements": ["Job offer from approved sponsor", "Skills assessment", "2+ years experience"],
                "processing_time": "2-4 months",
                "validity": "2-4 years"
            }
        ],
        "visa_process_steps": [
            "1. Check if occupation is on skilled list",
            "2. Get skills assessment (ACS for IT)",
            "3. Take IELTS/PTE (aim for 8+ each)",
            "4. Submit Expression of Interest (EOI)",
            "5. Get state nomination (for 190/491)",
            "6. Receive invitation to apply",
            "7. Lodge visa application",
            "8. Complete health checks and police clearance",
            "9. Wait for visa grant",
            "10. Land in Australia before first entry date"
        ],
        "visa_processing_time_weeks": 35,
        "visa_cost_usd": 3000,
        "popular_job_portals": [
            {"name": "Seek", "url": "https://seek.com.au", "description": "#1 job site in Australia"},
            {"name": "LinkedIn Australia", "url": "https://linkedin.com/jobs", "description": "Professional network"},
            {"name": "Indeed Australia", "url": "https://indeed.com.au", "description": "Job aggregator"},
            {"name": "Jora", "url": "https://jora.com", "description": "Aggregator by Seek"},
            {"name": "CareerOne", "url": "https://careerone.com.au", "description": "Australian job board"},
            {"name": "GradConnection", "url": "https://gradconnection.com", "description": "Graduate jobs"}
        ],
        "companies_hiring_indians": [
            {"name": "Atlassian", "industry": "Tech", "roles": "Engineers", "locations": "Sydney"},
            {"name": "Canva", "industry": "Design Tech", "roles": "All roles", "locations": "Sydney"},
            {"name": "Commonwealth Bank", "industry": "Banking", "roles": "Tech, Data", "locations": "Sydney"},
            {"name": "NAB", "industry": "Banking", "roles": "Digital", "locations": "Melbourne"},
            {"name": "Telstra", "industry": "Telecom", "roles": "Tech", "locations": "Melbourne, Sydney"},
            {"name": "REA Group", "industry": "PropTech", "roles": "Engineers", "locations": "Melbourne"},
            {"name": "Afterpay", "industry": "FinTech", "roles": "Engineers", "locations": "Melbourne"},
            {"name": "Amazon Australia", "industry": "Tech", "roles": "SDEs", "locations": "Sydney"},
            {"name": "Google Australia", "industry": "Tech", "roles": "Engineers", "locations": "Sydney"}
        ],
        "monthly_expenses_estimate": {
            "single_sydney": {"rent": 2000, "food": 600, "transport": 200, "utilities": 150, "misc": 400, "total_aud": 3350, "total_usd": 2200},
            "single_melbourne": {"rent": 1700, "food": 550, "transport": 180, "utilities": 140, "misc": 350, "total_aud": 2920, "total_usd": 1900}
        },
        "initial_settlement_cost": 6000,
        "pr_eligibility_years": 0,
        "citizenship_eligibility_years": 4,
        "income_tax_rate": "19% - 45% progressive",
        "common_challenges": [
            "High cost of living (Sydney, Melbourne)",
            "Distance from India (long flights)",
            "Skilled occupation list changes frequently",
            "High points required for invitation",
            "Regional visas require living in regional areas"
        ],
        "tips_for_indians": [
            "Get ACS assessment early (takes 2-3 months)",
            "Aim for PTE 79+ each (superior English = 20 points)",
            "Consider regional areas for lower cutoffs",
            "Apply for multiple states simultaneously",
            "Keep checking occupation ceilings"
        ]
    },

    # ==================== SINGAPORE ====================
    {
        "country_name": "Singapore",
        "visa_types": [
            {
                "name": "Employment Pass (EP)",
                "description": "For professionals, managers, executives",
                "requirements": ["Job offer from SG company", "Salary SGD 5,000+ (higher for experienced)", "Recognized qualifications"],
                "processing_time": "3-8 weeks",
                "validity": "1-2 years (renewable)"
            },
            {
                "name": "S Pass",
                "description": "For mid-skilled workers",
                "requirements": ["Salary SGD 3,000+", "Relevant qualifications", "Subject to quota"],
                "processing_time": "3-8 weeks",
                "validity": "2 years"
            },
            {
                "name": "Tech.Pass",
                "description": "For established tech entrepreneurs/leaders",
                "requirements": ["Salary SGD 20,000+ OR equity in tech company", "5+ years experience", "Leadership in tech company"],
                "processing_time": "4-8 weeks",
                "validity": "2 years"
            },
            {
                "name": "ONE Pass",
                "description": "For top talent in any field",
                "requirements": ["Salary SGD 30,000+ per month", "Outstanding achievements in field"],
                "processing_time": "4-8 weeks",
                "validity": "5 years"
            }
        ],
        "visa_process_steps": [
            "1. Get job offer from Singapore employer",
            "2. Employer applies for EP via MOM",
            "3. Check COMPASS points (new framework)",
            "4. Wait for In-Principle Approval (IPA)",
            "5. Enter Singapore with IPA letter",
            "6. Complete medical exam if required",
            "7. Collect EP card",
            "8. Apply for dependent passes if needed"
        ],
        "visa_processing_time_weeks": 6,
        "visa_cost_usd": 200,
        "employer_sponsorship_required": True,
        "popular_job_portals": [
            {"name": "LinkedIn Singapore", "url": "https://linkedin.com/jobs", "description": "Best for tech jobs"},
            {"name": "JobStreet", "url": "https://jobstreet.com.sg", "description": "Local job portal"},
            {"name": "Indeed Singapore", "url": "https://sg.indeed.com", "description": "Job aggregator"},
            {"name": "MyCareersFuture", "url": "https://mycareersfuture.gov.sg", "description": "Government portal"},
            {"name": "Glints", "url": "https://glints.com", "description": "Startup jobs"},
            {"name": "NodeFlair", "url": "https://nodeflair.com", "description": "Tech jobs + salary data"}
        ],
        "companies_hiring_indians": [
            {"name": "Google Singapore", "industry": "Tech", "roles": "Engineers, PMs"},
            {"name": "Meta Singapore", "industry": "Tech", "roles": "Engineers"},
            {"name": "Amazon Singapore", "industry": "Tech", "roles": "SDEs, Data"},
            {"name": "ByteDance/TikTok", "industry": "Tech", "roles": "Engineers"},
            {"name": "Grab", "industry": "SuperApp", "roles": "All tech roles"},
            {"name": "Sea/Shopee", "industry": "E-commerce", "roles": "Engineers"},
            {"name": "DBS Bank", "industry": "Banking", "roles": "Tech, Data"},
            {"name": "OCBC", "industry": "Banking", "roles": "Digital"},
            {"name": "Stripe Singapore", "industry": "FinTech", "roles": "Engineers"},
            {"name": "Wise", "industry": "FinTech", "roles": "Engineers"}
        ],
        "monthly_expenses_estimate": {
            "single": {"rent": 2000, "food": 800, "transport": 150, "utilities": 100, "misc": 400, "total_sgd": 3450, "total_usd": 2550}
        },
        "initial_settlement_cost": 5000,
        "pr_eligibility_years": 2,
        "pr_requirements": ["EP holder for 2+ years", "Stable employment", "Integration into society"],
        "citizenship_eligibility_years": 2,
        "income_tax_rate": "0% - 22% progressive (very low)",
        "common_challenges": [
            "Very high rent costs",
            "EP approval getting stricter",
            "COMPASS framework points required",
            "Small country, limited opportunities",
            "PR approval unpredictable"
        ],
        "tips_for_indians": [
            "Salary is key - negotiate higher for EP approval",
            "Apply through big companies first",
            "COMPASS framework favors diversity - check points",
            "Living in HDB areas is cheaper",
            "SingPass needed for everything"
        ]
    },

    # ==================== UK ====================
    {
        "country_name": "United Kingdom",
        "visa_types": [
            {
                "name": "Skilled Worker Visa",
                "description": "Main work visa (replaced Tier 2)",
                "requirements": ["Job offer from licensed sponsor", "Salary £26,200+ (or going rate)", "English B1", "70 points required"],
                "processing_time": "3-8 weeks",
                "validity": "5 years"
            },
            {
                "name": "Global Talent Visa",
                "description": "For leaders in tech, science, arts",
                "requirements": ["Endorsement from Tech Nation", "Proven track record", "No job offer needed"],
                "processing_time": "3-8 weeks",
                "validity": "5 years"
            },
            {
                "name": "High Potential Individual (HPI)",
                "description": "For recent graduates from top universities",
                "requirements": ["Degree from global top 50 university", "Graduated within 5 years"],
                "processing_time": "3 weeks",
                "validity": "2-3 years"
            },
            {
                "name": "Scale-up Visa",
                "description": "For fast-growing companies",
                "requirements": ["Job at qualifying scale-up", "Salary £33,000+"],
                "processing_time": "3 weeks",
                "validity": "2 years"
            }
        ],
        "visa_process_steps": [
            "1. Get job offer from licensed sponsor",
            "2. Employer issues Certificate of Sponsorship (CoS)",
            "3. Apply online via gov.uk",
            "4. Pay visa fee + Immigration Health Surcharge",
            "5. Book biometrics appointment",
            "6. Provide documents",
            "7. Wait for decision",
            "8. Collect BRP card in UK"
        ],
        "visa_processing_time_weeks": 5,
        "visa_cost_usd": 1500,
        "employer_sponsorship_required": True,
        "popular_job_portals": [
            {"name": "LinkedIn UK", "url": "https://linkedin.com/jobs", "description": "Best for tech"},
            {"name": "Indeed UK", "url": "https://indeed.co.uk", "description": "Job aggregator"},
            {"name": "Reed", "url": "https://reed.co.uk", "description": "Large UK job board"},
            {"name": "Totaljobs", "url": "https://totaljobs.com", "description": "UK job board"},
            {"name": "Glassdoor UK", "url": "https://glassdoor.co.uk", "description": "Jobs + reviews"},
            {"name": "Otta", "url": "https://otta.com", "description": "Curated tech jobs"},
            {"name": "Hackajob", "url": "https://hackajob.co", "description": "Tech assessment jobs"}
        ],
        "companies_hiring_indians": [
            {"name": "Google UK", "industry": "Tech", "roles": "Engineers"},
            {"name": "Meta UK", "industry": "Tech", "roles": "Engineers"},
            {"name": "Amazon UK", "industry": "Tech/Retail", "roles": "SDEs"},
            {"name": "Microsoft UK", "industry": "Tech", "roles": "Engineers"},
            {"name": "Revolut", "industry": "FinTech", "roles": "All roles"},
            {"name": "Monzo", "industry": "FinTech", "roles": "Engineers"},
            {"name": "Deliveroo", "industry": "Food Tech", "roles": "Engineers"},
            {"name": "JP Morgan UK", "industry": "Banking", "roles": "Tech"},
            {"name": "Goldman Sachs UK", "industry": "Banking", "roles": "Tech"}
        ],
        "monthly_expenses_estimate": {
            "single_london": {"rent": 1800, "food": 500, "transport": 200, "utilities": 150, "misc": 400, "total_gbp": 3050, "total_usd": 3800}
        },
        "initial_settlement_cost": 6000,
        "pr_eligibility_years": 5,
        "citizenship_eligibility_years": 6,
        "income_tax_rate": "20% - 45% progressive",
        "common_challenges": [
            "High cost of living in London",
            "NHS wait times",
            "Immigration Health Surcharge expensive",
            "Sponsor license requirement limits options",
            "Weather (grey, rainy)"
        ],
        "tips_for_indians": [
            "Apply to companies with sponsor license",
            "Budget for IHS (£1,035/year)",
            "Consider cities outside London (cheaper)",
            "Global Talent visa if you qualify (more freedom)",
            "Build UK professional network early"
        ]
    },

    # ==================== NETHERLANDS ====================
    {
        "country_name": "Netherlands",
        "visa_types": [
            {
                "name": "Highly Skilled Migrant Visa (Kennismigrant)",
                "description": "For skilled professionals - most common for IT",
                "requirements": ["Job offer from recognized sponsor", "Salary €5,008/month (under 30: €3,672)", "Relevant qualifications"],
                "processing_time": "2-4 weeks",
                "validity": "5 years"
            },
            {
                "name": "EU Blue Card (Netherlands)",
                "description": "EU-wide work permit",
                "requirements": ["Higher education degree", "Salary €5,867+/month", "Job contract 1+ year"],
                "processing_time": "3-6 weeks",
                "validity": "4 years"
            },
            {
                "name": "Orientation Year Visa (Zoekjaar)",
                "description": "Job search visa for graduates",
                "requirements": ["Graduated from top 200 university within 3 years", "Sufficient funds"],
                "processing_time": "2-4 weeks",
                "validity": "1 year"
            }
        ],
        "visa_process_steps": [
            "1. Get job offer from recognized sponsor",
            "2. Employer applies for work permit at IND",
            "3. Receive positive decision",
            "4. Apply for MVV (entry visa) at embassy",
            "5. Travel to Netherlands",
            "6. Register at municipality (BSN)",
            "7. Collect residence permit"
        ],
        "visa_processing_time_weeks": 4,
        "visa_cost_usd": 350,
        "employer_sponsorship_required": True,
        "popular_job_portals": [
            {"name": "LinkedIn Netherlands", "url": "https://linkedin.com/jobs", "description": "Best for tech"},
            {"name": "Indeed NL", "url": "https://indeed.nl", "description": "Job aggregator"},
            {"name": "Glassdoor NL", "url": "https://glassdoor.nl", "description": "Jobs + reviews"},
            {"name": "IamExpat Jobs", "url": "https://iamexpat.nl/career/jobs-netherlands", "description": "Expat-focused"},
            {"name": "Together Abroad", "url": "https://togetherabroad.nl", "description": "International jobs"},
            {"name": "Honeypot", "url": "https://honeypot.io", "description": "Tech jobs Europe"}
        ],
        "companies_hiring_indians": [
            {"name": "Booking.com", "industry": "Travel Tech", "roles": "All tech"},
            {"name": "Uber NL", "industry": "Tech", "roles": "Engineers"},
            {"name": "Adyen", "industry": "FinTech", "roles": "Engineers"},
            {"name": "Elastic", "industry": "Tech", "roles": "Engineers"},
            {"name": "TomTom", "industry": "Maps/Tech", "roles": "Engineers"},
            {"name": "Philips", "industry": "HealthTech", "roles": "Engineers"},
            {"name": "ING Bank", "industry": "Banking", "roles": "Tech"},
            {"name": "ABN AMRO", "industry": "Banking", "roles": "Tech"},
            {"name": "ASML", "industry": "Semiconductor", "roles": "Engineers"}
        ],
        "monthly_expenses_estimate": {
            "single_amsterdam": {"rent": 1800, "food": 400, "transport": 100, "utilities": 150, "insurance": 130, "misc": 300, "total_eur": 2880, "total_usd": 3100}
        },
        "initial_settlement_cost": 5000,
        "pr_eligibility_years": 5,
        "citizenship_eligibility_years": 5,
        "income_tax_rate": "37% - 50% (but 30% ruling saves taxes)",
        "tax_tips": [
            "30% ruling: 30% of salary is tax-free for 5 years!",
            "Highly skilled migrants eligible",
            "Significant tax savings",
            "Apply within 4 months of starting job"
        ],
        "common_challenges": [
            "Finding housing is extremely difficult",
            "High rent in Amsterdam",
            "Weather is grey and rainy",
            "Dutch language helpful for daily life",
            "Bureaucracy can be slow"
        ],
        "tips_for_indians": [
            "Apply for 30% ruling immediately",
            "Start housing search before moving",
            "Consider cities outside Amsterdam (Rotterdam, Eindhoven)",
            "Many jobs don't require Dutch",
            "Get DigiD for government services"
        ]
    }
]


def seed_country_guides():
    """Seed comprehensive country migration guides"""
    logger.info("🌍 Seeding comprehensive country migration guides...")
    
    init_db()
    db = SessionLocal()
    
    try:
        # Remove existing guides to update with comprehensive ones
        db.query(CountryMigration).delete()
        db.commit()
        logger.info("Cleared old migration guides")
        
        for guide_data in COMPREHENSIVE_MIGRATION_GUIDES:
            guide = CountryMigration(**guide_data)
            db.add(guide)
        
        db.commit()
        logger.info(f"✅ Seeded {len(COMPREHENSIVE_MIGRATION_GUIDES)} comprehensive migration guides")
        
    except Exception as e:
        logger.error(f"❌ Error seeding guides: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_country_guides()

