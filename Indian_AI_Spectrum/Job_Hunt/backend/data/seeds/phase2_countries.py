"""
Phase 2: Complete Country Migration Data
Adding detailed migration guides for Germany, Canada, US, Australia, UK, Singapore
"""
import sys
import os
import json
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import SessionLocal, init_db
from app.models.country import Country, CountryMigration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COUNTRY_DATA = [
    # GERMANY
    {
        "country_name": "Germany",
        "visa_types": json.dumps([
            {"name": "EU Blue Card", "description": "For highly qualified professionals with job offer and degree", "requirements": ["Recognized university degree", "Job offer with min €58,400 salary (or €45,552 for shortage occupations)", "Valid passport"], "processing_time": "4-8 weeks", "validity": "4 years", "cost": "€75-100"},
            {"name": "Job Seeker Visa", "description": "6-month visa to search for jobs in Germany", "requirements": ["University degree", "Proof of funds (€947/month)", "Health insurance", "Accommodation proof"], "processing_time": "4-12 weeks", "validity": "6 months", "cost": "€75"},
            {"name": "Work Visa", "description": "Standard work visa for skilled workers", "requirements": ["Job offer from German employer", "Recognized qualifications", "Valid passport"], "processing_time": "4-8 weeks", "validity": "1-4 years", "cost": "€75"},
            {"name": "Freelancer Visa", "description": "For self-employed/freelance workers", "requirements": ["Business plan", "Client contracts", "Proof of funds", "Health insurance"], "processing_time": "4-12 weeks", "validity": "1-3 years", "cost": "€100"}
        ]),
        "visa_process_steps": json.dumps([
            "1. Secure job offer from German employer",
            "2. Gather documents (degree certificates, passport, photos)",
            "3. Book visa appointment at German Embassy/VFS",
            "4. Submit application and biometrics",
            "5. Wait for processing (4-12 weeks)",
            "6. Collect visa and travel to Germany",
            "7. Register at local Bürgeramt within 2 weeks",
            "8. Apply for residence permit at Ausländerbehörde"
        ]),
        "visa_processing_time_weeks": 8,
        "visa_cost_usd": 85,
        "employer_sponsorship_required": True,
        "popular_job_portals": json.dumps([
            {"name": "LinkedIn Germany", "url": "https://linkedin.com/jobs", "description": "Best for tech and professional roles", "is_recommended": True},
            {"name": "StepStone", "url": "https://stepstone.de", "description": "Germany's largest job portal", "is_recommended": True},
            {"name": "Indeed Germany", "url": "https://de.indeed.com", "description": "Global job search engine"},
            {"name": "XING", "url": "https://xing.com", "description": "German professional network like LinkedIn"},
            {"name": "Glassdoor Germany", "url": "https://glassdoor.de", "description": "Jobs with company reviews"},
            {"name": "Monster Germany", "url": "https://monster.de", "description": "Large job board"},
            {"name": "Make it in Germany", "url": "https://make-it-in-germany.com", "description": "Official government portal", "is_recommended": True},
            {"name": "Honeypot", "url": "https://honeypot.io", "description": "Tech-focused, companies apply to you", "is_recommended": True},
            {"name": "Berlin Startup Jobs", "url": "https://berlinstartupjobs.com", "description": "Berlin startup ecosystem"}
        ]),
        "recruitment_agencies": json.dumps([
            {"name": "Hays Germany", "url": "https://hays.de", "specialization": "IT, Engineering, Finance", "free_for_candidates": True},
            {"name": "Michael Page Germany", "url": "https://michaelpage.de", "specialization": "Finance, Tech, Engineering", "free_for_candidates": True},
            {"name": "Robert Half", "url": "https://roberthalf.de", "specialization": "Finance, IT", "free_for_candidates": True},
            {"name": "Randstad Germany", "url": "https://randstad.de", "specialization": "Various sectors", "free_for_candidates": True}
        ]),
        "top_hiring_companies": json.dumps([
            {"name": "SAP", "industry": "Enterprise Software", "careers_url": "https://sap.com/careers"},
            {"name": "Siemens", "industry": "Industrial/Tech", "careers_url": "https://siemens.com/careers"},
            {"name": "BMW", "industry": "Automotive", "careers_url": "https://bmwgroup.jobs"},
            {"name": "Bosch", "industry": "Engineering", "careers_url": "https://bosch.com/careers"},
            {"name": "Deutsche Bank", "industry": "Banking", "careers_url": "https://db.com/careers"},
            {"name": "Zalando", "industry": "E-commerce/Tech", "careers_url": "https://jobs.zalando.com"},
            {"name": "Delivery Hero", "industry": "Food Tech", "careers_url": "https://careers.deliveryhero.com"},
            {"name": "N26", "industry": "FinTech", "careers_url": "https://n26.com/careers"},
            {"name": "Auto1 Group", "industry": "Auto Tech", "careers_url": "https://auto1-group.com/careers"},
            {"name": "HelloFresh", "industry": "Food Tech", "careers_url": "https://hellofresh.com/careers"}
        ]),
        "salary_expectations": json.dumps({
            "software_engineer_entry": "€45,000-55,000/year",
            "software_engineer_mid": "€55,000-75,000/year",
            "software_engineer_senior": "€75,000-100,000/year",
            "data_scientist": "€55,000-85,000/year",
            "devops_engineer": "€55,000-80,000/year",
            "product_manager": "€60,000-90,000/year",
            "note": "Salaries are before tax. Germany has progressive tax (14-45%)"
        }),
        "monthly_expenses_estimate": json.dumps({
            "single_shared": 1200, "single_studio": 1800, "single_1bhk": 2200, "family_2bhk": 3000,
            "breakdown": {
                "rent_shared": "€500-800/month",
                "rent_studio": "€800-1200/month",
                "rent_1bhk": "€1000-1500/month",
                "utilities": "€150-250/month",
                "groceries": "€200-350/month",
                "transport": "€80-100/month (monthly pass)",
                "health_insurance": "€80-400/month",
                "internet_mobile": "€40-60/month"
            }
        }),
        "initial_settlement_cost": 5000,
        "tips_for_indians": json.dumps([
            "Learn basic German (A1-A2) before arriving - it helps immensely",
            "Open a blocked account (Sperrkonto) for visa processing",
            "Get your degrees assessed by Anabin or get equivalency certificate",
            "Register your address (Anmeldung) within 14 days of arrival",
            "Indian degrees in STEM are generally well-recognized",
            "Join Indian community groups in your city for support",
            "Berlin and Munich have largest Indian communities",
            "German work culture values punctuality - be on time",
            "Health insurance is mandatory - choose between public and private"
        ]),
        "common_challenges": json.dumps([
            "German language barrier - especially for non-tech roles",
            "Finding housing in major cities is very competitive",
            "Bureaucracy (Behörden) can be slow and frustrating",
            "Weather can be challenging - long, dark winters",
            "Bank account opening can be difficult initially",
            "Making German friends takes time and effort"
        ]),
        "things_to_avoid": json.dumps([
            "Don't ignore learning German - it limits opportunities",
            "Don't underestimate housing costs and competition",
            "Don't work without proper visa/permit",
            "Don't skip health insurance - it's mandatory and expensive if caught",
            "Don't expect quick administrative processes"
        ]),
        "pr_eligibility_years": 4,
        "citizenship_eligibility_years": 8,
        "income_tax_rate": "14% - 45% progressive",
        "tax_treaties_with_india": True,
        "work_culture": "Strong work-life balance. 28-30 days vacation. 40-hour work weeks. Unions are powerful. Direct communication style.",
        "last_updated": datetime.now()
    },
    
    # CANADA
    {
        "country_name": "Canada",
        "visa_types": json.dumps([
            {"name": "Express Entry", "description": "Points-based PR immigration system", "requirements": ["Skilled work experience", "Language test (IELTS/CELPIP)", "Education credential assessment (ECA)", "Points score above cutoff"], "processing_time": "6 months", "validity": "Permanent Resident", "cost": "$2,300 CAD"},
            {"name": "Provincial Nominee Program (PNP)", "description": "Province-specific immigration", "requirements": ["Job offer in province (sometimes)", "Meet provincial criteria", "Express Entry profile (usually)"], "processing_time": "6-18 months", "validity": "Permanent Resident", "cost": "$2,300+ CAD"},
            {"name": "Work Permit (LMIA)", "description": "Employer-sponsored work permit", "requirements": ["Job offer with positive LMIA", "Valid passport", "Proof of funds"], "processing_time": "2-4 months", "validity": "1-3 years", "cost": "$155 CAD"},
            {"name": "Global Talent Stream", "description": "Fast-track for tech workers", "requirements": ["Job in eligible occupation", "Employer in GTS program", "Skilled worker qualifications"], "processing_time": "2 weeks", "validity": "2-3 years", "cost": "$155 CAD"}
        ]),
        "visa_process_steps": json.dumps([
            "1. Check eligibility and CRS score using online calculator",
            "2. Take IELTS/CELPIP language test",
            "3. Get Education Credential Assessment (ECA) from WES",
            "4. Create Express Entry profile",
            "5. Receive ITA (Invitation to Apply) if score is above cutoff",
            "6. Submit complete application with documents",
            "7. Complete medical exam and biometrics",
            "8. Wait for COPR (Confirmation of Permanent Residence)",
            "9. Land in Canada and activate PR"
        ]),
        "visa_processing_time_weeks": 24,
        "visa_cost_usd": 1700,
        "employer_sponsorship_required": False,
        "popular_job_portals": json.dumps([
            {"name": "LinkedIn Canada", "url": "https://linkedin.com/jobs", "description": "Best for professional jobs", "is_recommended": True},
            {"name": "Indeed Canada", "url": "https://ca.indeed.com", "description": "Largest job aggregator", "is_recommended": True},
            {"name": "Job Bank", "url": "https://jobbank.gc.ca", "description": "Official Canadian government job portal", "is_recommended": True},
            {"name": "Glassdoor Canada", "url": "https://glassdoor.ca", "description": "Jobs with reviews"},
            {"name": "Workopolis", "url": "https://workopolis.com", "description": "Canadian job board"},
            {"name": "Monster Canada", "url": "https://monster.ca", "description": "Large job board"},
            {"name": "Tech Jobs Canada", "url": "https://techjobscanada.com", "description": "Tech-focused job board"}
        ]),
        "recruitment_agencies": json.dumps([
            {"name": "Randstad Canada", "url": "https://randstad.ca", "specialization": "Various sectors", "free_for_candidates": True},
            {"name": "Robert Half Canada", "url": "https://roberthalf.ca", "specialization": "Finance, IT, Admin", "free_for_candidates": True},
            {"name": "Hays Canada", "url": "https://hays.ca", "specialization": "IT, Engineering", "free_for_candidates": True}
        ]),
        "top_hiring_companies": json.dumps([
            {"name": "Shopify", "industry": "E-commerce/Tech", "careers_url": "https://shopify.com/careers"},
            {"name": "Amazon Canada", "industry": "Tech/E-commerce", "careers_url": "https://amazon.jobs"},
            {"name": "Google Canada", "industry": "Tech", "careers_url": "https://careers.google.com"},
            {"name": "Microsoft Canada", "industry": "Tech", "careers_url": "https://careers.microsoft.com"},
            {"name": "RBC", "industry": "Banking", "careers_url": "https://jobs.rbc.com"},
            {"name": "TD Bank", "industry": "Banking", "careers_url": "https://jobs.td.com"},
            {"name": "Deloitte Canada", "industry": "Consulting", "careers_url": "https://www2.deloitte.com/ca/en/careers.html"},
            {"name": "Telus", "industry": "Telecom", "careers_url": "https://www.telus.com/en/careers"},
            {"name": "Wealthsimple", "industry": "FinTech", "careers_url": "https://www.wealthsimple.com/en-ca/careers"}
        ]),
        "salary_expectations": json.dumps({
            "software_engineer_entry": "$60,000-80,000 CAD/year",
            "software_engineer_mid": "$80,000-120,000 CAD/year",
            "software_engineer_senior": "$120,000-180,000 CAD/year",
            "data_scientist": "$80,000-130,000 CAD/year",
            "devops_engineer": "$80,000-130,000 CAD/year",
            "product_manager": "$90,000-150,000 CAD/year",
            "note": "Toronto and Vancouver pay higher. Federal + Provincial tax applies."
        }),
        "monthly_expenses_estimate": json.dumps({
            "single_toronto": 2500, "single_vancouver": 2600, "single_other": 1800, "family": 4500,
            "breakdown": {
                "rent_1bhk_toronto": "$1,800-2,500/month",
                "rent_1bhk_vancouver": "$1,900-2,600/month",
                "rent_1bhk_other_cities": "$1,200-1,800/month",
                "utilities": "$100-200/month",
                "groceries": "$300-500/month",
                "transport": "$100-150/month (transit pass)",
                "phone_internet": "$100-150/month",
                "health_basics": "Free (provincial healthcare)"
            }
        }),
        "initial_settlement_cost": 8000,
        "tips_for_indians": json.dumps([
            "Take IELTS Academic - aim for 8+ bands for maximum CRS points",
            "Get ECA done from WES - takes 2-3 months",
            "Consider applying to less competitive provinces (Atlantic, Manitoba)",
            "Canadian experience is valued - consider studying in Canada if young",
            "Join Desi communities on Facebook/WhatsApp for housing and job tips",
            "Apply to multiple provinces for PNP if eligible",
            "Toronto, Vancouver, and Brampton have large Indian communities",
            "Get reference letters from all previous employers before leaving India"
        ]),
        "common_challenges": json.dumps([
            "High living costs in Toronto and Vancouver",
            "First job in Canada can be hard without Canadian experience",
            "Weather is extremely cold in winter (-20°C to -40°C)",
            "Driver's license takes time to convert",
            "Initial months can be financially challenging"
        ]),
        "things_to_avoid": json.dumps([
            "Don't rely only on Express Entry - explore all pathways",
            "Don't underestimate living costs in major cities",
            "Don't apply to fake colleges (diploma mills)",
            "Don't work without proper work authorization",
            "Don't ignore French language learning for extra points"
        ]),
        "pr_eligibility_years": 0,
        "citizenship_eligibility_years": 3,
        "income_tax_rate": "15% - 33% federal + provincial",
        "tax_treaties_with_india": True,
        "work_culture": "Relaxed work culture. Multicultural environment. 2-3 weeks vacation. Strong employee rights. Friendly and polite communication.",
        "last_updated": datetime.now()
    },
    
    # UNITED STATES
    {
        "country_name": "United States",
        "visa_types": json.dumps([
            {"name": "H-1B Visa", "description": "Specialty occupation visa for skilled workers", "requirements": ["Bachelor's degree or equivalent", "Job offer from US employer", "Specialty occupation role", "Employer sponsorship"], "processing_time": "3-6 months (Premium: 15 days)", "validity": "3 years (extendable to 6)", "cost": "$2,500-5,000 (employer pays)"},
            {"name": "L-1 Visa", "description": "Intra-company transfer visa", "requirements": ["1 year with company abroad", "Manager/Executive (L-1A) or Specialized Knowledge (L-1B)", "US affiliate/subsidiary"], "processing_time": "1-3 months", "validity": "1-3 years", "cost": "$2,000-4,000"},
            {"name": "O-1 Visa", "description": "For individuals with extraordinary ability", "requirements": ["Extraordinary ability in field", "Evidence of achievements", "US employer/agent sponsor"], "processing_time": "2-3 months (Premium: 15 days)", "validity": "3 years", "cost": "$1,500-3,000"},
            {"name": "EB-2/EB-3 Green Card", "description": "Employment-based permanent residence", "requirements": ["PERM labor certification", "Employer sponsorship", "Priority date current (long wait for Indians)"], "processing_time": "5-15+ years for Indians", "validity": "Permanent", "cost": "$5,000-10,000+"}
        ]),
        "visa_process_steps": json.dumps([
            "1. Get job offer from US employer willing to sponsor H-1B",
            "2. Employer files H-1B petition in April lottery",
            "3. If selected in lottery, USCIS processes petition",
            "4. Once approved, schedule visa interview at US Embassy",
            "5. Attend visa interview with all documents",
            "6. If approved, receive visa stamp",
            "7. Enter US before visa expiry, start work",
            "8. For Green Card: Employer starts PERM, then I-140, then I-485/consular processing"
        ]),
        "visa_processing_time_weeks": 16,
        "visa_cost_usd": 3500,
        "employer_sponsorship_required": True,
        "popular_job_portals": json.dumps([
            {"name": "LinkedIn", "url": "https://linkedin.com/jobs", "description": "Best for tech and professional jobs", "is_recommended": True},
            {"name": "Indeed", "url": "https://indeed.com", "description": "Largest job aggregator", "is_recommended": True},
            {"name": "Glassdoor", "url": "https://glassdoor.com", "description": "Jobs with salary and review data", "is_recommended": True},
            {"name": "Dice", "url": "https://dice.com", "description": "Tech-focused job board"},
            {"name": "AngelList/Wellfound", "url": "https://wellfound.com", "description": "Startup jobs"},
            {"name": "Hired", "url": "https://hired.com", "description": "Tech jobs, companies apply to you"},
            {"name": "Levels.fyi", "url": "https://levels.fyi/jobs", "description": "Tech jobs with compensation data", "is_recommended": True},
            {"name": "Blind", "url": "https://teamblind.com", "description": "Anonymous job discussions and referrals"}
        ]),
        "recruitment_agencies": json.dumps([
            {"name": "TEKsystems", "url": "https://teksystems.com", "specialization": "IT staffing", "free_for_candidates": True},
            {"name": "Robert Half", "url": "https://roberthalf.com", "specialization": "Finance, IT, Admin", "free_for_candidates": True},
            {"name": "Dice (Direct)", "url": "https://dice.com", "specialization": "Tech roles", "free_for_candidates": True}
        ]),
        "top_hiring_companies": json.dumps([
            {"name": "Google", "industry": "Tech", "careers_url": "https://careers.google.com"},
            {"name": "Meta", "industry": "Tech", "careers_url": "https://metacareers.com"},
            {"name": "Amazon", "industry": "Tech/E-commerce", "careers_url": "https://amazon.jobs"},
            {"name": "Apple", "industry": "Tech", "careers_url": "https://apple.com/careers"},
            {"name": "Microsoft", "industry": "Tech", "careers_url": "https://careers.microsoft.com"},
            {"name": "Netflix", "industry": "Entertainment/Tech", "careers_url": "https://jobs.netflix.com"},
            {"name": "Salesforce", "industry": "Enterprise Software", "careers_url": "https://salesforce.com/careers"},
            {"name": "Uber", "industry": "Tech/Mobility", "careers_url": "https://uber.com/careers"},
            {"name": "Stripe", "industry": "FinTech", "careers_url": "https://stripe.com/jobs"},
            {"name": "Airbnb", "industry": "Tech/Travel", "careers_url": "https://careers.airbnb.com"}
        ]),
        "salary_expectations": json.dumps({
            "software_engineer_entry": "$100,000-150,000/year",
            "software_engineer_mid": "$150,000-250,000/year",
            "software_engineer_senior": "$250,000-400,000/year",
            "data_scientist": "$120,000-200,000/year",
            "devops_engineer": "$120,000-200,000/year",
            "product_manager": "$150,000-300,000/year",
            "note": "Bay Area and NYC pay highest. Total comp includes stock/bonus."
        }),
        "monthly_expenses_estimate": json.dumps({
            "single_bay_area": 4500, "single_nyc": 4000, "single_seattle": 3000, "single_other": 2500,
            "breakdown": {
                "rent_1bhk_bay_area": "$2,500-4,000/month",
                "rent_1bhk_nyc": "$2,500-3,500/month",
                "rent_1bhk_seattle": "$1,800-2,500/month",
                "utilities": "$100-200/month",
                "groceries": "$400-600/month",
                "health_insurance": "$200-500/month (employer usually covers)",
                "transport": "$100-300/month",
                "phone_internet": "$100-150/month"
            }
        }),
        "initial_settlement_cost": 10000,
        "tips_for_indians": json.dumps([
            "Apply to companies known to sponsor H-1B (check myvisajobs.com)",
            "H-1B lottery is in April - start job search by January",
            "Get referrals from Indians in target companies via LinkedIn/Blind",
            "Prepare extensively for FAANG-style interviews (LeetCode, System Design)",
            "Consider MS in US for easier path to job and H-1B",
            "Bay Area, Seattle, NYC have largest Indian tech communities",
            "Keep all I-20, I-797 documents safe - you'll need them",
            "Start Green Card process early - wait is 50+ years for Indians",
            "Network actively in Indian tech communities"
        ]),
        "common_challenges": json.dumps([
            "H-1B lottery is random - only 30% selection rate",
            "Tied to employer - changing jobs requires transfer",
            "Green Card backlog for Indians is 50-80+ years",
            "At-will employment - can be fired anytime",
            "Healthcare is expensive without employer coverage",
            "Political uncertainty around immigration policy"
        ]),
        "things_to_avoid": json.dumps([
            "Don't work for body shops with bad reputation",
            "Don't overstay visa - it bars future entry",
            "Don't work without proper authorization",
            "Don't ignore the Green Card process timeline",
            "Don't rely on a single H-1B application"
        ]),
        "pr_eligibility_years": 50,
        "citizenship_eligibility_years": 55,
        "income_tax_rate": "10% - 37% federal + state (0-13%)",
        "tax_treaties_with_india": True,
        "work_culture": "Fast-paced, results-oriented. 2-4 weeks vacation (less used). At-will employment. Direct feedback culture. Long working hours common in tech.",
        "last_updated": datetime.now()
    },
    
    # AUSTRALIA
    {
        "country_name": "Australia",
        "visa_types": json.dumps([
            {"name": "Skilled Independent (189)", "description": "Points-based PR without sponsorship", "requirements": ["Occupation on skilled list", "Skills assessment", "65+ points", "Age under 45", "IELTS 6+ each"], "processing_time": "6-12 months", "validity": "Permanent", "cost": "AUD 4,640"},
            {"name": "Skilled Nominated (190)", "description": "State-sponsored PR visa", "requirements": ["State nomination", "Occupation on state list", "60+ points (+ 5 state points)", "Skills assessment"], "processing_time": "6-12 months", "validity": "Permanent", "cost": "AUD 4,640"},
            {"name": "Skilled Work Regional (491)", "description": "Regional area provisional visa", "requirements": ["State/family sponsorship", "Occupation on regional list", "65+ points"], "processing_time": "6-12 months", "validity": "5 years (pathway to 191 PR)", "cost": "AUD 4,640"},
            {"name": "TSS (482) Visa", "description": "Employer-sponsored temporary work visa", "requirements": ["Job offer in nominated occupation", "Skills assessment", "2 years experience", "Employer sponsorship"], "processing_time": "1-4 months", "validity": "2-4 years", "cost": "AUD 1,455-2,770"}
        ]),
        "visa_process_steps": json.dumps([
            "1. Check if occupation is on skilled occupation list",
            "2. Get skills assessment from relevant authority (ACS for IT)",
            "3. Take IELTS/PTE and get required score",
            "4. Submit Expression of Interest (EOI) in SkillSelect",
            "5. Wait for invitation (ITA) based on points",
            "6. Lodge visa application with documents",
            "7. Complete health exams and police clearances",
            "8. Wait for visa grant",
            "9. Make initial entry and activate visa"
        ]),
        "visa_processing_time_weeks": 40,
        "visa_cost_usd": 3000,
        "employer_sponsorship_required": False,
        "popular_job_portals": json.dumps([
            {"name": "Seek", "url": "https://seek.com.au", "description": "Australia's largest job board", "is_recommended": True},
            {"name": "LinkedIn Australia", "url": "https://linkedin.com/jobs", "description": "Professional networking and jobs", "is_recommended": True},
            {"name": "Indeed Australia", "url": "https://au.indeed.com", "description": "Job aggregator"},
            {"name": "Jora", "url": "https://jora.com", "description": "Job search engine"},
            {"name": "CareerOne", "url": "https://careerone.com.au", "description": "Australian job portal"},
            {"name": "GradConnection", "url": "https://gradconnection.com", "description": "Graduate and entry-level jobs"}
        ]),
        "recruitment_agencies": json.dumps([
            {"name": "Hays Australia", "url": "https://hays.com.au", "specialization": "IT, Engineering, Finance", "free_for_candidates": True},
            {"name": "Robert Half", "url": "https://roberthalf.com.au", "specialization": "Finance, IT", "free_for_candidates": True},
            {"name": "Randstad Australia", "url": "https://randstad.com.au", "specialization": "Various sectors", "free_for_candidates": True},
            {"name": "Michael Page", "url": "https://michaelpage.com.au", "specialization": "Professional roles", "free_for_candidates": True}
        ]),
        "top_hiring_companies": json.dumps([
            {"name": "Atlassian", "industry": "Tech", "careers_url": "https://atlassian.com/careers"},
            {"name": "Canva", "industry": "Tech/Design", "careers_url": "https://canva.com/careers"},
            {"name": "REA Group", "industry": "PropTech", "careers_url": "https://rea-group.com/careers"},
            {"name": "Xero", "industry": "FinTech", "careers_url": "https://xero.com/careers"},
            {"name": "Commonwealth Bank", "industry": "Banking", "careers_url": "https://commbank.com.au/careers"},
            {"name": "NAB", "industry": "Banking", "careers_url": "https://nab.com.au/careers"},
            {"name": "Telstra", "industry": "Telecom", "careers_url": "https://telstra.com.au/careers"},
            {"name": "Afterpay", "industry": "FinTech", "careers_url": "https://afterpay.com/careers"}
        ]),
        "salary_expectations": json.dumps({
            "software_engineer_entry": "AUD 70,000-90,000/year",
            "software_engineer_mid": "AUD 100,000-140,000/year",
            "software_engineer_senior": "AUD 150,000-200,000/year",
            "data_scientist": "AUD 100,000-150,000/year",
            "devops_engineer": "AUD 110,000-160,000/year",
            "product_manager": "AUD 120,000-180,000/year",
            "note": "Sydney and Melbourne pay highest. Super (retirement) is 11% on top."
        }),
        "monthly_expenses_estimate": json.dumps({
            "single_sydney": 3500, "single_melbourne": 3000, "single_other": 2500,
            "breakdown": {
                "rent_1bhk_sydney": "AUD 2,000-3,000/month",
                "rent_1bhk_melbourne": "AUD 1,600-2,400/month",
                "utilities": "AUD 150-250/month",
                "groceries": "AUD 400-600/month",
                "transport": "AUD 150-200/month",
                "phone_internet": "AUD 80-120/month",
                "health_insurance": "Required for visa"
            }
        }),
        "initial_settlement_cost": 7000,
        "tips_for_indians": json.dumps([
            "Take PTE - it's faster and easier than IELTS for most",
            "Get ACS assessment early - it takes 8-12 weeks",
            "Apply for 190/491 to multiple states for better chances",
            "Adelaide, Perth, Brisbane are easier for 190 nomination",
            "Indian IT degrees are well-recognized in Australia",
            "Join Indian community groups for job referrals and tips",
            "Sydney and Melbourne have largest Indian populations",
            "Consider regional areas for faster PR pathway (491→191)"
        ]),
        "common_challenges": json.dumps([
            "Points requirement keeps increasing",
            "Some occupations have long backlogs",
            "High cost of living in Sydney/Melbourne",
            "Job market can be competitive for new migrants",
            "Adjustment to Australian work culture"
        ]),
        "things_to_avoid": json.dumps([
            "Don't apply without skills assessment",
            "Don't overstate experience in skills assessment",
            "Don't ignore regional opportunities",
            "Don't delay English test preparation",
            "Don't come without sufficient savings"
        ]),
        "pr_eligibility_years": 0,
        "citizenship_eligibility_years": 4,
        "income_tax_rate": "0% - 45% progressive",
        "tax_treaties_with_india": True,
        "work_culture": "Good work-life balance. 4 weeks annual leave. Casual dress code. Flat hierarchy. Friday drinks culture.",
        "last_updated": datetime.now()
    }
]


def seed_countries():
    """Seed country migration data"""
    logger.info("🌍 Seeding Phase 2: Country Migration Data...")
    init_db()
    db = SessionLocal()
    
    added = 0
    updated = 0
    
    try:
        for country_data in COUNTRY_DATA:
            country_name = country_data.get("country_name")
            existing = db.query(CountryMigration).filter(
                CountryMigration.country_name == country_name
            ).first()
            
            if existing:
                for key, value in country_data.items():
                    setattr(existing, key, value)
                updated += 1
                logger.info(f"Updated: {country_name}")
            else:
                guide = CountryMigration(**country_data)
                db.add(guide)
                added += 1
                logger.info(f"Added: {country_name}")
        
        db.commit()
        logger.info(f"✅ Phase 2 Countries: Added {added}, Updated {updated}")
        
        total = db.query(CountryMigration).count()
        logger.info(f"📊 Total migration guides: {total}")
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_countries()


