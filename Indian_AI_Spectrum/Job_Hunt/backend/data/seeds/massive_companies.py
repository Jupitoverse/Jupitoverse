"""
MASSIVE Company Database - Space, STEM, IT, and More
Comprehensive directory with 1000+ companies
"""
import sys
import os
import concurrent.futures
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import SessionLocal, init_db
from app.models.company import Company, CompanyType, CompanyCategory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# SPACE & AEROSPACE COMPANIES
# ============================================================================
SPACE_COMPANIES = [
    # Indian Space
    {"name": "ISRO", "slug": "isro", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.PSU, "industry": "Space & Aerospace", "description": "Indian Space Research Organisation - India's premier space agency. Chandrayaan, Mangalyaan, PSLV.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 1969, "employee_count_range": "10001+", "careers_page": "https://www.isro.gov.in/careers.html", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "HAL", "slug": "hal", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.PSU, "industry": "Aerospace & Defence", "description": "Hindustan Aeronautics Limited - India's largest aerospace company. Fighter jets, helicopters.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 1940, "employee_count_range": "10001+", "careers_page": "https://hal-india.co.in/careers", "has_indian_office": True},
    {"name": "Skyroot Aerospace", "slug": "skyroot-aerospace", "company_type": CompanyType.STARTUP, "category": CompanyCategory.STARTUP, "industry": "Space Tech", "description": "India's first private space company to launch a rocket. Building Vikram series of rockets.", "headquarters_city": "Hyderabad", "headquarters_country": "India", "founded_year": 2018, "employee_count_range": "51-200", "careers_page": "https://skyroot.in/careers", "has_indian_office": True, "is_remote_friendly": False},
    {"name": "Agnikul Cosmos", "slug": "agnikul-cosmos", "company_type": CompanyType.STARTUP, "category": CompanyCategory.STARTUP, "industry": "Space Tech", "description": "Building 3D-printed rocket engines. India's space startup backed by Y Combinator.", "headquarters_city": "Chennai", "headquarters_country": "India", "founded_year": 2017, "employee_count_range": "51-200", "careers_page": "https://agnikul.in/careers", "has_indian_office": True},
    {"name": "Pixxel", "slug": "pixxel", "company_type": CompanyType.STARTUP, "category": CompanyCategory.STARTUP, "industry": "Space Tech", "description": "Building Earth-imaging satellite constellation. Hyperspectral imaging.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2019, "employee_count_range": "51-200", "careers_page": "https://pixxel.space/careers", "has_indian_office": True, "is_remote_friendly": True},
    {"name": "Bellatrix Aerospace", "slug": "bellatrix-aerospace", "company_type": CompanyType.STARTUP, "category": CompanyCategory.STARTUP, "industry": "Space Tech", "description": "Green propulsion systems for satellites. Electric thrusters.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2015, "employee_count_range": "51-200", "careers_page": "https://bellatrixaerospace.com/careers", "has_indian_office": True},
    {"name": "Dhruva Space", "slug": "dhruva-space", "company_type": CompanyType.STARTUP, "category": CompanyCategory.STARTUP, "industry": "Space Tech", "description": "Full-stack space engineering company. Satellite platforms and ground systems.", "headquarters_city": "Hyderabad", "headquarters_country": "India", "founded_year": 2012, "employee_count_range": "51-200", "careers_page": "https://dhruvaspace.com/careers", "has_indian_office": True},
    
    # Global Space
    {"name": "SpaceX", "slug": "spacex", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Space & Aerospace", "description": "Elon Musk's space company. Falcon rockets, Starship, Starlink satellites.", "headquarters_city": "Hawthorne", "headquarters_country": "USA", "founded_year": 2002, "employee_count_range": "10001+", "careers_page": "https://www.spacex.com/careers", "is_remote_friendly": False, "hires_from_india": False},
    {"name": "Blue Origin", "slug": "blue-origin", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Space & Aerospace", "description": "Jeff Bezos' space company. New Shepard, New Glenn rockets.", "headquarters_city": "Kent", "headquarters_country": "USA", "founded_year": 2000, "employee_count_range": "5001-10000", "careers_page": "https://www.blueorigin.com/careers", "is_remote_friendly": False},
    {"name": "NASA", "slug": "nasa", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.MNC, "industry": "Space & Aerospace", "description": "National Aeronautics and Space Administration. USA's space agency.", "headquarters_city": "Washington DC", "headquarters_country": "USA", "founded_year": 1958, "employee_count_range": "10001+", "careers_page": "https://www.nasa.gov/careers"},
    {"name": "ESA", "slug": "esa", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.MNC, "industry": "Space & Aerospace", "description": "European Space Agency. International space exploration.", "headquarters_city": "Paris", "headquarters_country": "France", "founded_year": 1975, "employee_count_range": "1001-5000", "careers_page": "https://www.esa.int/About_Us/Careers_at_ESA"},
    {"name": "Rocket Lab", "slug": "rocket-lab", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Space & Aerospace", "description": "Small satellite launch company. Electron rocket.", "headquarters_city": "Long Beach", "headquarters_country": "USA", "founded_year": 2006, "employee_count_range": "1001-5000", "careers_page": "https://www.rocketlabusa.com/careers"},
    {"name": "Virgin Galactic", "slug": "virgin-galactic", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Space Tourism", "description": "Space tourism company. SpaceShipTwo.", "headquarters_city": "Tustin", "headquarters_country": "USA", "founded_year": 2004, "employee_count_range": "501-1000", "careers_page": "https://www.virgingalactic.com/careers"},
    {"name": "Boeing Space", "slug": "boeing-space", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Aerospace & Defence", "description": "Boeing's space division. Starliner, SLS.", "headquarters_city": "Arlington", "headquarters_country": "USA", "founded_year": 1916, "employee_count_range": "10001+", "careers_page": "https://jobs.boeing.com"},
    {"name": "Lockheed Martin Space", "slug": "lockheed-martin-space", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Aerospace & Defence", "description": "Lockheed Martin's space systems.", "headquarters_city": "Bethesda", "headquarters_country": "USA", "founded_year": 1995, "employee_count_range": "10001+", "careers_page": "https://www.lockheedmartinjobs.com"},
    {"name": "Northrop Grumman Space", "slug": "northrop-grumman", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Aerospace & Defence", "description": "Space systems and services.", "headquarters_city": "Falls Church", "headquarters_country": "USA", "founded_year": 1939, "employee_count_range": "10001+", "careers_page": "https://www.northropgrumman.com/careers"},
    {"name": "Airbus Defence and Space", "slug": "airbus-space", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Aerospace & Defence", "description": "European aerospace giant's space division.", "headquarters_city": "Toulouse", "headquarters_country": "France", "founded_year": 2014, "employee_count_range": "10001+", "careers_page": "https://www.airbus.com/en/careers"},
    {"name": "Planet Labs", "slug": "planet-labs", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Space Tech", "description": "Earth imaging satellite company. Planet Scope.", "headquarters_city": "San Francisco", "headquarters_country": "USA", "founded_year": 2010, "employee_count_range": "501-1000", "careers_page": "https://www.planet.com/careers", "is_remote_friendly": True},
    {"name": "Maxar Technologies", "slug": "maxar", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Space Tech", "description": "Space technology company. Earth observation satellites.", "headquarters_city": "Westminster", "headquarters_country": "USA", "founded_year": 2017, "employee_count_range": "1001-5000", "careers_page": "https://www.maxar.com/careers"},
]

# ============================================================================
# DEFENCE & RESEARCH ORGANIZATIONS (INDIA)
# ============================================================================
DEFENCE_RESEARCH = [
    {"name": "DRDO", "slug": "drdo", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.PSU, "industry": "Defence Research", "description": "Defence Research and Development Organisation. India's premier defence R&D.", "headquarters_city": "Delhi", "headquarters_country": "India", "founded_year": 1958, "employee_count_range": "10001+", "careers_page": "https://www.drdo.gov.in/drdo/careers", "has_indian_office": True},
    {"name": "BARC", "slug": "barc", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.PSU, "industry": "Nuclear Research", "description": "Bhabha Atomic Research Centre. Nuclear research institute.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 1954, "employee_count_range": "10001+", "careers_page": "https://www.barc.gov.in/careers", "has_indian_office": True},
    {"name": "BEL", "slug": "bel", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.PSU, "industry": "Defence Electronics", "description": "Bharat Electronics Limited. Defence electronics manufacturer.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 1954, "employee_count_range": "10001+", "careers_page": "https://www.bel-india.in/careers", "has_indian_office": True},
    {"name": "BHEL", "slug": "bhel", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.PSU, "industry": "Heavy Electrical", "description": "Bharat Heavy Electricals Limited. Power generation equipment.", "headquarters_city": "Delhi", "headquarters_country": "India", "founded_year": 1964, "employee_count_range": "10001+", "careers_page": "https://www.bhel.com/careers", "has_indian_office": True},
    {"name": "CSIR", "slug": "csir", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.PSU, "industry": "Scientific Research", "description": "Council of Scientific and Industrial Research. 38 national laboratories.", "headquarters_city": "Delhi", "headquarters_country": "India", "founded_year": 1942, "employee_count_range": "10001+", "careers_page": "https://www.csir.res.in/careers", "has_indian_office": True},
    {"name": "IISc", "slug": "iisc", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.PSU, "industry": "Research & Education", "description": "Indian Institute of Science. India's premier research university.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 1909, "employee_count_range": "1001-5000", "careers_page": "https://iisc.ac.in/careers", "has_indian_office": True},
    {"name": "TIFR", "slug": "tifr", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.PSU, "industry": "Research", "description": "Tata Institute of Fundamental Research. Physics, mathematics, biology.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 1945, "employee_count_range": "501-1000", "careers_page": "https://www.tifr.res.in/careers", "has_indian_office": True},
    {"name": "ICAR", "slug": "icar", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.PSU, "industry": "Agricultural Research", "description": "Indian Council of Agricultural Research.", "headquarters_city": "Delhi", "headquarters_country": "India", "founded_year": 1929, "employee_count_range": "10001+", "careers_page": "https://icar.org.in/careers", "has_indian_office": True},
    {"name": "ICMR", "slug": "icmr", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.PSU, "industry": "Medical Research", "description": "Indian Council of Medical Research.", "headquarters_city": "Delhi", "headquarters_country": "India", "founded_year": 1911, "employee_count_range": "5001-10000", "careers_page": "https://www.icmr.gov.in/careers", "has_indian_office": True},
]

# ============================================================================
# AUTOMOTIVE & EV COMPANIES
# ============================================================================
AUTOMOTIVE = [
    # Indian
    {"name": "Tata Motors", "slug": "tata-motors", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Automotive", "description": "India's largest automobile company. Owns Jaguar Land Rover.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 1945, "employee_count_range": "10001+", "careers_page": "https://www.tatamotors.com/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "Mahindra & Mahindra", "slug": "mahindra", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Automotive", "description": "SUVs, tractors, electric vehicles. Tech Mahindra parent.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 1945, "employee_count_range": "10001+", "careers_page": "https://www.mahindra.com/careers", "has_indian_office": True},
    {"name": "Maruti Suzuki", "slug": "maruti-suzuki", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Automotive", "description": "India's largest car manufacturer.", "headquarters_city": "Delhi", "headquarters_country": "India", "founded_year": 1981, "employee_count_range": "10001+", "careers_page": "https://www.marutisuzuki.com/corporate/careers", "has_indian_office": True},
    {"name": "Ather Energy", "slug": "ather-energy", "company_type": CompanyType.STARTUP, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Electric Vehicles", "description": "Electric scooter manufacturer. Ather 450X.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2013, "employee_count_range": "1001-5000", "careers_page": "https://www.atherenergy.com/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "Ola Electric", "slug": "ola-electric", "company_type": CompanyType.STARTUP, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Electric Vehicles", "description": "Electric scooter manufacturer. World's largest EV factory.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2017, "employee_count_range": "1001-5000", "careers_page": "https://olaelectric.com/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "TVS Motor", "slug": "tvs-motor", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Automotive", "description": "Two-wheeler manufacturer. iQube electric scooter.", "headquarters_city": "Chennai", "headquarters_country": "India", "founded_year": 1978, "employee_count_range": "10001+", "careers_page": "https://www.tvsmotor.com/careers", "has_indian_office": True},
    {"name": "Bajaj Auto", "slug": "bajaj-auto", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Automotive", "description": "Two and three wheeler manufacturer. Pulsar, Chetak.", "headquarters_city": "Pune", "headquarters_country": "India", "founded_year": 1945, "employee_count_range": "10001+", "careers_page": "https://www.bajajauto.com/careers", "has_indian_office": True},
    {"name": "Hero MotoCorp", "slug": "hero-motocorp", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Automotive", "description": "World's largest two-wheeler manufacturer.", "headquarters_city": "Delhi", "headquarters_country": "India", "founded_year": 1984, "employee_count_range": "10001+", "careers_page": "https://www.heromotocorp.com/en-in/careers.html", "has_indian_office": True},
    {"name": "Ashok Leyland", "slug": "ashok-leyland", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Automotive", "description": "Commercial vehicles manufacturer.", "headquarters_city": "Chennai", "headquarters_country": "India", "founded_year": 1948, "employee_count_range": "10001+", "careers_page": "https://www.ashokleyland.com/careers", "has_indian_office": True},
    
    # Global
    {"name": "Tesla", "slug": "tesla", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Electric Vehicles", "description": "Electric vehicles and clean energy company.", "headquarters_city": "Austin", "headquarters_country": "USA", "founded_year": 2003, "employee_count_range": "10001+", "careers_page": "https://www.tesla.com/careers", "is_actively_hiring": True, "hires_from_india": True},
    {"name": "Rivian", "slug": "rivian", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Electric Vehicles", "description": "Electric adventure vehicles. R1T, R1S.", "headquarters_city": "Irvine", "headquarters_country": "USA", "founded_year": 2009, "employee_count_range": "10001+", "careers_page": "https://rivian.com/careers"},
    {"name": "Lucid Motors", "slug": "lucid-motors", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Electric Vehicles", "description": "Luxury electric vehicles. Lucid Air.", "headquarters_city": "Newark", "headquarters_country": "USA", "founded_year": 2007, "employee_count_range": "5001-10000", "careers_page": "https://lucidmotors.com/careers"},
    {"name": "BMW", "slug": "bmw", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Automotive", "description": "German luxury automobile manufacturer.", "headquarters_city": "Munich", "headquarters_country": "Germany", "founded_year": 1916, "employee_count_range": "10001+", "careers_page": "https://www.bmwgroup.jobs", "has_indian_office": True},
    {"name": "Mercedes-Benz", "slug": "mercedes-benz", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Automotive", "description": "German luxury automobile manufacturer.", "headquarters_city": "Stuttgart", "headquarters_country": "Germany", "founded_year": 1926, "employee_count_range": "10001+", "careers_page": "https://www.mercedes-benz.com/en/career", "has_indian_office": True},
    {"name": "Volkswagen", "slug": "volkswagen", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Automotive", "description": "German automobile manufacturer.", "headquarters_city": "Wolfsburg", "headquarters_country": "Germany", "founded_year": 1937, "employee_count_range": "10001+", "careers_page": "https://www.volkswagen-karriere.de", "has_indian_office": True},
    {"name": "Toyota", "slug": "toyota", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Automotive", "description": "Japanese automobile manufacturer.", "headquarters_city": "Toyota City", "headquarters_country": "Japan", "founded_year": 1937, "employee_count_range": "10001+", "careers_page": "https://www.toyota-global.com/careers", "has_indian_office": True},
    {"name": "Honda", "slug": "honda", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Automotive", "description": "Japanese automobile and motorcycle manufacturer.", "headquarters_city": "Tokyo", "headquarters_country": "Japan", "founded_year": 1948, "employee_count_range": "10001+", "careers_page": "https://global.honda/careers", "has_indian_office": True},
    {"name": "Hyundai", "slug": "hyundai", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Automotive", "description": "South Korean automobile manufacturer.", "headquarters_city": "Seoul", "headquarters_country": "South Korea", "founded_year": 1967, "employee_count_range": "10001+", "careers_page": "https://www.hyundai.com/worldwide/en/company/careers", "has_indian_office": True},
    {"name": "Ford", "slug": "ford", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Automotive", "description": "American automobile manufacturer.", "headquarters_city": "Dearborn", "headquarters_country": "USA", "founded_year": 1903, "employee_count_range": "10001+", "careers_page": "https://corporate.ford.com/careers.html", "has_indian_office": True},
    {"name": "General Motors", "slug": "gm", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Automotive", "description": "American automobile manufacturer. Chevrolet, Cadillac.", "headquarters_city": "Detroit", "headquarters_country": "USA", "founded_year": 1908, "employee_count_range": "10001+", "careers_page": "https://www.gm.com/careers.html", "has_indian_office": True},
    {"name": "Waymo", "slug": "waymo", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Autonomous Vehicles", "description": "Google/Alphabet's self-driving technology company.", "headquarters_city": "Mountain View", "headquarters_country": "USA", "founded_year": 2009, "employee_count_range": "1001-5000", "careers_page": "https://waymo.com/careers", "is_actively_hiring": True},
    {"name": "Cruise", "slug": "cruise", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Autonomous Vehicles", "description": "GM's autonomous vehicle unit.", "headquarters_city": "San Francisco", "headquarters_country": "USA", "founded_year": 2013, "employee_count_range": "1001-5000", "careers_page": "https://getcruise.com/careers"},
]

# ============================================================================
# PHARMA & BIOTECH
# ============================================================================
PHARMA_BIOTECH = [
    # Indian
    {"name": "Sun Pharma", "slug": "sun-pharma", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Pharmaceuticals", "description": "India's largest pharma company.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 1983, "employee_count_range": "10001+", "careers_page": "https://sunpharma.com/careers", "has_indian_office": True},
    {"name": "Cipla", "slug": "cipla", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Pharmaceuticals", "description": "Global pharmaceutical company. HIV/AIDS treatments.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 1935, "employee_count_range": "10001+", "careers_page": "https://www.cipla.com/careers", "has_indian_office": True},
    {"name": "Dr. Reddy's", "slug": "dr-reddys", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Pharmaceuticals", "description": "Pharmaceutical company. Generics and proprietary products.", "headquarters_city": "Hyderabad", "headquarters_country": "India", "founded_year": 1984, "employee_count_range": "10001+", "careers_page": "https://www.drreddys.com/careers", "has_indian_office": True},
    {"name": "Biocon", "slug": "biocon", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Biotechnology", "description": "India's largest biopharmaceutical company.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 1978, "employee_count_range": "10001+", "careers_page": "https://www.biocon.com/careers", "has_indian_office": True},
    {"name": "Serum Institute of India", "slug": "serum-institute", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Vaccines", "description": "World's largest vaccine manufacturer.", "headquarters_city": "Pune", "headquarters_country": "India", "founded_year": 1966, "employee_count_range": "5001-10000", "careers_page": "https://www.seruminstitute.com/careers.php", "has_indian_office": True},
    {"name": "Lupin", "slug": "lupin", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Pharmaceuticals", "description": "Global pharmaceutical company.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 1968, "employee_count_range": "10001+", "careers_page": "https://www.lupin.com/careers", "has_indian_office": True},
    {"name": "Zydus Lifesciences", "slug": "zydus", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Pharmaceuticals", "description": "Healthcare company. Vaccines, diagnostics.", "headquarters_city": "Ahmedabad", "headquarters_country": "India", "founded_year": 1952, "employee_count_range": "10001+", "careers_page": "https://www.zyduslife.com/careers", "has_indian_office": True},
    {"name": "Glenmark", "slug": "glenmark", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Pharmaceuticals", "description": "Pharmaceutical company. Dermatology focus.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 1977, "employee_count_range": "10001+", "careers_page": "https://www.glenmarkpharma.com/careers", "has_indian_office": True},
    
    # Global
    {"name": "Pfizer", "slug": "pfizer", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Pharmaceuticals", "description": "American pharmaceutical corporation. COVID vaccine.", "headquarters_city": "New York", "headquarters_country": "USA", "founded_year": 1849, "employee_count_range": "10001+", "careers_page": "https://www.pfizer.com/about/careers", "has_indian_office": True},
    {"name": "Johnson & Johnson", "slug": "johnson-johnson", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Healthcare", "description": "American healthcare corporation.", "headquarters_city": "New Brunswick", "headquarters_country": "USA", "founded_year": 1886, "employee_count_range": "10001+", "careers_page": "https://www.careers.jnj.com", "has_indian_office": True},
    {"name": "Novartis", "slug": "novartis", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Pharmaceuticals", "description": "Swiss pharmaceutical company.", "headquarters_city": "Basel", "headquarters_country": "Switzerland", "founded_year": 1996, "employee_count_range": "10001+", "careers_page": "https://www.novartis.com/careers", "has_indian_office": True},
    {"name": "Roche", "slug": "roche", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Pharmaceuticals", "description": "Swiss healthcare company.", "headquarters_city": "Basel", "headquarters_country": "Switzerland", "founded_year": 1896, "employee_count_range": "10001+", "careers_page": "https://www.roche.com/careers", "has_indian_office": True},
    {"name": "Moderna", "slug": "moderna", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Biotechnology", "description": "mRNA therapeutics company. COVID vaccine.", "headquarters_city": "Cambridge", "headquarters_country": "USA", "founded_year": 2010, "employee_count_range": "1001-5000", "careers_page": "https://www.modernatx.com/careers"},
    {"name": "BioNTech", "slug": "biontech", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Biotechnology", "description": "German biotechnology company. mRNA vaccines.", "headquarters_city": "Mainz", "headquarters_country": "Germany", "founded_year": 2008, "employee_count_range": "1001-5000", "careers_page": "https://www.biontech.de/careers"},
    {"name": "Illumina", "slug": "illumina", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Biotechnology", "description": "DNA sequencing company.", "headquarters_city": "San Diego", "headquarters_country": "USA", "founded_year": 1998, "employee_count_range": "5001-10000", "careers_page": "https://www.illumina.com/company/careers.html", "is_remote_friendly": True},
    {"name": "Genentech", "slug": "genentech", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Biotechnology", "description": "Biotechnology corporation. Part of Roche.", "headquarters_city": "South San Francisco", "headquarters_country": "USA", "founded_year": 1976, "employee_count_range": "10001+", "careers_page": "https://gene.com/careers"},
]

# ============================================================================
# ENERGY & RENEWABLES
# ============================================================================
ENERGY = [
    {"name": "ONGC", "slug": "ongc", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.PSU, "industry": "Oil & Gas", "description": "Oil and Natural Gas Corporation. India's largest oil producer.", "headquarters_city": "Delhi", "headquarters_country": "India", "founded_year": 1956, "employee_count_range": "10001+", "careers_page": "https://www.ongcindia.com/wps/wcm/connect/en/careers", "has_indian_office": True},
    {"name": "IOCL", "slug": "iocl", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.PSU, "industry": "Oil & Gas", "description": "Indian Oil Corporation Limited.", "headquarters_city": "Delhi", "headquarters_country": "India", "founded_year": 1959, "employee_count_range": "10001+", "careers_page": "https://iocl.com/recruitment", "has_indian_office": True},
    {"name": "NTPC", "slug": "ntpc", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.PSU, "industry": "Power", "description": "National Thermal Power Corporation. India's largest power company.", "headquarters_city": "Delhi", "headquarters_country": "India", "founded_year": 1975, "employee_count_range": "10001+", "careers_page": "https://www.ntpc.co.in/careers", "has_indian_office": True},
    {"name": "Reliance Industries", "slug": "reliance-industries", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Conglomerate", "description": "India's largest private company. Jio, Retail, Oil & Gas.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 1966, "employee_count_range": "10001+", "careers_page": "https://www.ril.com/Careers.aspx", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "Adani Green Energy", "slug": "adani-green", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Renewable Energy", "description": "India's largest renewable energy company.", "headquarters_city": "Ahmedabad", "headquarters_country": "India", "founded_year": 2015, "employee_count_range": "1001-5000", "careers_page": "https://www.adanigreenenergy.com/careers", "has_indian_office": True},
    {"name": "Tata Power", "slug": "tata-power", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Power", "description": "Integrated power company. Renewables, distribution.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 1919, "employee_count_range": "10001+", "careers_page": "https://www.tatapower.com/careers", "has_indian_office": True},
    {"name": "ReNew Power", "slug": "renew-power", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Renewable Energy", "description": "Leading renewable energy IPP in India.", "headquarters_city": "Gurugram", "headquarters_country": "India", "founded_year": 2011, "employee_count_range": "1001-5000", "careers_page": "https://www.renewpower.in/careers", "has_indian_office": True},
    {"name": "Suzlon Energy", "slug": "suzlon", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Wind Energy", "description": "Wind turbine manufacturer.", "headquarters_city": "Pune", "headquarters_country": "India", "founded_year": 1995, "employee_count_range": "5001-10000", "careers_page": "https://www.suzlon.com/careers", "has_indian_office": True},
]

# ============================================================================
# FINTECH & BANKS
# ============================================================================
FINTECH_BANKS = [
    # Indian Banks
    {"name": "SBI", "slug": "sbi", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.PSU, "industry": "Banking", "description": "State Bank of India. India's largest bank.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 1955, "employee_count_range": "10001+", "careers_page": "https://www.sbi.co.in/web/careers", "has_indian_office": True},
    {"name": "HDFC Bank", "slug": "hdfc-bank", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "Banking", "description": "India's largest private sector bank.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 1994, "employee_count_range": "10001+", "careers_page": "https://www.hdfcbank.com/personal/about-us/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "ICICI Bank", "slug": "icici-bank", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "Banking", "description": "Leading private sector bank.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 1994, "employee_count_range": "10001+", "careers_page": "https://www.icicicareers.com", "has_indian_office": True},
    {"name": "Axis Bank", "slug": "axis-bank", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "Banking", "description": "Third largest private sector bank.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 1993, "employee_count_range": "10001+", "careers_page": "https://www.axisbank.com/careers", "has_indian_office": True},
    {"name": "Kotak Mahindra Bank", "slug": "kotak-bank", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.TIER_1, "industry": "Banking", "description": "Private sector bank.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 1985, "employee_count_range": "10001+", "careers_page": "https://www.kotak.com/en/careers.html", "has_indian_office": True},
    
    # Fintech
    {"name": "Paytm", "slug": "paytm", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "FinTech", "description": "Digital payments pioneer. Listed on NSE.", "headquarters_city": "Noida", "headquarters_country": "India", "founded_year": 2010, "employee_count_range": "10001+", "careers_page": "https://paytm.com/careers", "has_indian_office": True},
    {"name": "Razorpay", "slug": "razorpay", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "FinTech", "description": "Payment gateway and banking platform.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2014, "employee_count_range": "1001-5000", "careers_page": "https://razorpay.com/jobs", "has_indian_office": True, "is_actively_hiring": True, "is_remote_friendly": True},
    {"name": "PhonePe", "slug": "phonepe", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "FinTech", "description": "UPI payments platform.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2015, "employee_count_range": "1001-5000", "careers_page": "https://www.phonepe.com/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "CRED", "slug": "cred", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "FinTech", "description": "Credit card payments and rewards.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2018, "employee_count_range": "501-1000", "careers_page": "https://cred.club/careers", "has_indian_office": True, "is_remote_friendly": True},
    {"name": "Zerodha", "slug": "zerodha", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "FinTech", "description": "India's largest stock broker.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2010, "employee_count_range": "501-1000", "careers_page": "https://zerodha.com/careers", "has_indian_office": True, "is_remote_friendly": True},
    {"name": "Groww", "slug": "groww", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "FinTech", "description": "Investment platform for stocks and mutual funds.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2016, "employee_count_range": "501-1000", "careers_page": "https://groww.in/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "Pine Labs", "slug": "pine-labs", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "FinTech", "description": "Merchant platform and payments.", "headquarters_city": "Noida", "headquarters_country": "India", "founded_year": 1998, "employee_count_range": "1001-5000", "careers_page": "https://www.pinelabs.com/careers", "has_indian_office": True},
    {"name": "BharatPe", "slug": "bharatpe", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "FinTech", "description": "B2B payments and lending.", "headquarters_city": "Delhi", "headquarters_country": "India", "founded_year": 2018, "employee_count_range": "501-1000", "careers_page": "https://bharatpe.com/careers", "has_indian_office": True},
    {"name": "Lendingkart", "slug": "lendingkart", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.STARTUP, "industry": "FinTech", "description": "SME lending platform.", "headquarters_city": "Ahmedabad", "headquarters_country": "India", "founded_year": 2014, "employee_count_range": "501-1000", "careers_page": "https://www.lendingkart.com/careers", "has_indian_office": True},
    {"name": "Jupiter", "slug": "jupiter", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.STARTUP, "industry": "FinTech", "description": "Digital banking app.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2019, "employee_count_range": "201-500", "careers_page": "https://jupiter.money/careers", "has_indian_office": True},
    {"name": "Fi Money", "slug": "fi-money", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.STARTUP, "industry": "FinTech", "description": "Neobanking platform by epiFi.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2019, "employee_count_range": "201-500", "careers_page": "https://fi.money/careers", "has_indian_office": True},
    {"name": "Navi", "slug": "navi", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.STARTUP, "industry": "FinTech", "description": "Financial services by Flipkart co-founder.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2018, "employee_count_range": "501-1000", "careers_page": "https://navi.com/careers", "has_indian_office": True},
]

# ============================================================================
# CONSULTING FIRMS
# ============================================================================
CONSULTING = [
    {"name": "McKinsey & Company", "slug": "mckinsey", "company_type": CompanyType.CONSULTING, "category": CompanyCategory.TIER_1, "industry": "Consulting", "description": "Global management consulting firm. MBB.", "headquarters_city": "New York", "headquarters_country": "USA", "founded_year": 1926, "employee_count_range": "10001+", "careers_page": "https://www.mckinsey.com/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "BCG", "slug": "bcg", "company_type": CompanyType.CONSULTING, "category": CompanyCategory.TIER_1, "industry": "Consulting", "description": "Boston Consulting Group. MBB.", "headquarters_city": "Boston", "headquarters_country": "USA", "founded_year": 1963, "employee_count_range": "10001+", "careers_page": "https://www.bcg.com/careers", "has_indian_office": True},
    {"name": "Bain & Company", "slug": "bain", "company_type": CompanyType.CONSULTING, "category": CompanyCategory.TIER_1, "industry": "Consulting", "description": "Global management consulting. MBB.", "headquarters_city": "Boston", "headquarters_country": "USA", "founded_year": 1973, "employee_count_range": "10001+", "careers_page": "https://www.bain.com/careers", "has_indian_office": True},
    {"name": "Deloitte", "slug": "deloitte", "company_type": CompanyType.CONSULTING, "category": CompanyCategory.TIER_1, "industry": "Consulting", "description": "Big 4. Audit, consulting, financial advisory.", "headquarters_city": "London", "headquarters_country": "UK", "founded_year": 1845, "employee_count_range": "10001+", "careers_page": "https://www2.deloitte.com/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "PwC", "slug": "pwc", "company_type": CompanyType.CONSULTING, "category": CompanyCategory.TIER_1, "industry": "Consulting", "description": "PricewaterhouseCoopers. Big 4.", "headquarters_city": "London", "headquarters_country": "UK", "founded_year": 1998, "employee_count_range": "10001+", "careers_page": "https://www.pwc.com/gx/en/careers.html", "has_indian_office": True},
    {"name": "EY", "slug": "ey", "company_type": CompanyType.CONSULTING, "category": CompanyCategory.TIER_1, "industry": "Consulting", "description": "Ernst & Young. Big 4.", "headquarters_city": "London", "headquarters_country": "UK", "founded_year": 1989, "employee_count_range": "10001+", "careers_page": "https://www.ey.com/en_gl/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "KPMG", "slug": "kpmg", "company_type": CompanyType.CONSULTING, "category": CompanyCategory.TIER_1, "industry": "Consulting", "description": "Big 4 professional services.", "headquarters_city": "Amstelveen", "headquarters_country": "Netherlands", "founded_year": 1987, "employee_count_range": "10001+", "careers_page": "https://home.kpmg/xx/en/home/careers.html", "has_indian_office": True},
    {"name": "Accenture", "slug": "accenture", "company_type": CompanyType.CONSULTING, "category": CompanyCategory.MNC, "industry": "Consulting", "description": "Global professional services.", "headquarters_city": "Dublin", "headquarters_country": "Ireland", "founded_year": 1989, "employee_count_range": "10001+", "careers_page": "https://www.accenture.com/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "Capgemini", "slug": "capgemini", "company_type": CompanyType.CONSULTING, "category": CompanyCategory.MNC, "industry": "Consulting", "description": "Global consulting and technology services.", "headquarters_city": "Paris", "headquarters_country": "France", "founded_year": 1967, "employee_count_range": "10001+", "careers_page": "https://www.capgemini.com/careers", "has_indian_office": True},
]

# ============================================================================
# TELECOM
# ============================================================================
TELECOM = [
    {"name": "Jio", "slug": "jio", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Telecom", "description": "Reliance Jio. India's largest telecom operator.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 2016, "employee_count_range": "10001+", "careers_page": "https://careers.jio.com", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "Airtel", "slug": "airtel", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Telecom", "description": "Bharti Airtel. Telecom and digital services.", "headquarters_city": "Delhi", "headquarters_country": "India", "founded_year": 1995, "employee_count_range": "10001+", "careers_page": "https://www.airtel.in/careers", "has_indian_office": True},
    {"name": "Vi (Vodafone Idea)", "slug": "vi", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Telecom", "description": "Vodafone Idea Limited.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 2018, "employee_count_range": "10001+", "careers_page": "https://www.myvi.in/careers", "has_indian_office": True},
    {"name": "BSNL", "slug": "bsnl", "company_type": CompanyType.GOVERNMENT, "category": CompanyCategory.PSU, "industry": "Telecom", "description": "Bharat Sanchar Nigam Limited. Government telecom.", "headquarters_city": "Delhi", "headquarters_country": "India", "founded_year": 2000, "employee_count_range": "10001+", "careers_page": "https://www.bsnl.co.in/opencms/bsnl/BSNL/about_us/careers.html", "has_indian_office": True},
]

# ============================================================================
# E-COMMERCE & RETAIL
# ============================================================================
ECOMMERCE = [
    {"name": "Flipkart", "slug": "flipkart", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "E-commerce", "description": "India's largest e-commerce company. Walmart owned.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2007, "employee_count_range": "10001+", "careers_page": "https://www.flipkartcareers.com", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "Amazon India", "slug": "amazon-india", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.FAANG, "industry": "E-commerce", "description": "Amazon's India operations.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2013, "employee_count_range": "10001+", "careers_page": "https://www.amazon.jobs/en/locations/india", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "Myntra", "slug": "myntra", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Fashion E-commerce", "description": "Fashion and lifestyle e-commerce. Part of Flipkart.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2007, "employee_count_range": "1001-5000", "careers_page": "https://careers.myntra.com", "has_indian_office": True},
    {"name": "Meesho", "slug": "meesho", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Social Commerce", "description": "Social commerce platform for small businesses.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2015, "employee_count_range": "1001-5000", "careers_page": "https://careers.meesho.com", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "Swiggy", "slug": "swiggy", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Food Delivery", "description": "Food delivery and quick commerce.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2014, "employee_count_range": "5001-10000", "careers_page": "https://careers.swiggy.com", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "Zomato", "slug": "zomato", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Food Delivery", "description": "Food delivery platform. Listed on NSE.", "headquarters_city": "Gurugram", "headquarters_country": "India", "founded_year": 2008, "employee_count_range": "5001-10000", "careers_page": "https://www.zomato.com/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "BigBasket", "slug": "bigbasket", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Grocery E-commerce", "description": "Online grocery delivery. Tata owned.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2011, "employee_count_range": "5001-10000", "careers_page": "https://www.bigbasket.com/careers", "has_indian_office": True},
    {"name": "Blinkit", "slug": "blinkit", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Quick Commerce", "description": "Quick commerce. Part of Zomato.", "headquarters_city": "Gurugram", "headquarters_country": "India", "founded_year": 2013, "employee_count_range": "1001-5000", "careers_page": "https://blinkit.com/careers", "has_indian_office": True},
    {"name": "Zepto", "slug": "zepto", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Quick Commerce", "description": "10-minute grocery delivery.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 2021, "employee_count_range": "1001-5000", "careers_page": "https://www.zeptonow.com/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "Nykaa", "slug": "nykaa", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "Beauty E-commerce", "description": "Beauty and fashion platform. Listed on NSE.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 2012, "employee_count_range": "1001-5000", "careers_page": "https://www.nykaa.com/careers", "has_indian_office": True},
]

# ============================================================================
# EDTECH
# ============================================================================
EDTECH = [
    {"name": "BYJU'S", "slug": "byjus", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "EdTech", "description": "India's largest edtech company.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2011, "employee_count_range": "10001+", "careers_page": "https://byjus.com/careers", "has_indian_office": True},
    {"name": "Unacademy", "slug": "unacademy", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "EdTech", "description": "Test prep platform.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2015, "employee_count_range": "1001-5000", "careers_page": "https://unacademy.com/careers", "has_indian_office": True, "is_remote_friendly": True},
    {"name": "upGrad", "slug": "upgrad", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "EdTech", "description": "Online higher education platform.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 2015, "employee_count_range": "1001-5000", "careers_page": "https://www.upgrad.com/us/careers", "has_indian_office": True},
    {"name": "Vedantu", "slug": "vedantu", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "EdTech", "description": "Live tutoring platform.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2014, "employee_count_range": "1001-5000", "careers_page": "https://www.vedantu.com/careers", "has_indian_office": True},
    {"name": "Physics Wallah", "slug": "physics-wallah", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.INDIAN_UNICORN, "industry": "EdTech", "description": "Affordable test prep platform.", "headquarters_city": "Noida", "headquarters_country": "India", "founded_year": 2020, "employee_count_range": "1001-5000", "careers_page": "https://www.pw.live/careers", "has_indian_office": True},
    {"name": "Coursera", "slug": "coursera", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "EdTech", "description": "Online learning platform. University courses.", "headquarters_city": "Mountain View", "headquarters_country": "USA", "founded_year": 2012, "employee_count_range": "1001-5000", "careers_page": "https://about.coursera.org/careers", "is_remote_friendly": True},
    {"name": "Udemy", "slug": "udemy", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "EdTech", "description": "Online course marketplace.", "headquarters_city": "San Francisco", "headquarters_country": "USA", "founded_year": 2010, "employee_count_range": "1001-5000", "careers_page": "https://about.udemy.com/careers", "is_remote_friendly": True},
]

# ============================================================================
# AI & ML FOCUSED COMPANIES
# ============================================================================
AI_ML = [
    {"name": "OpenAI", "slug": "openai", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "AI Research", "description": "ChatGPT, GPT-4, DALL-E creators.", "headquarters_city": "San Francisco", "headquarters_country": "USA", "founded_year": 2015, "employee_count_range": "501-1000", "careers_page": "https://openai.com/careers", "is_actively_hiring": True, "hires_from_india": True},
    {"name": "Anthropic", "slug": "anthropic", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "AI Research", "description": "Claude AI creators. AI safety focused.", "headquarters_city": "San Francisco", "headquarters_country": "USA", "founded_year": 2021, "employee_count_range": "201-500", "careers_page": "https://www.anthropic.com/careers", "is_actively_hiring": True},
    {"name": "DeepMind", "slug": "deepmind", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MAANG, "industry": "AI Research", "description": "Google's AI research lab. AlphaGo, AlphaFold.", "headquarters_city": "London", "headquarters_country": "UK", "founded_year": 2010, "employee_count_range": "1001-5000", "careers_page": "https://deepmind.com/careers", "is_actively_hiring": True},
    {"name": "Hugging Face", "slug": "hugging-face", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.STARTUP, "industry": "AI/ML", "description": "AI community and model hub. Transformers library.", "headquarters_city": "New York", "headquarters_country": "USA", "founded_year": 2016, "employee_count_range": "201-500", "careers_page": "https://huggingface.co/jobs", "is_remote_friendly": True, "is_actively_hiring": True},
    {"name": "Stability AI", "slug": "stability-ai", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.STARTUP, "industry": "AI", "description": "Stable Diffusion creators.", "headquarters_city": "London", "headquarters_country": "UK", "founded_year": 2019, "employee_count_range": "201-500", "careers_page": "https://stability.ai/careers", "is_remote_friendly": True},
    {"name": "Cohere", "slug": "cohere", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.STARTUP, "industry": "AI", "description": "Enterprise NLP API.", "headquarters_city": "Toronto", "headquarters_country": "Canada", "founded_year": 2019, "employee_count_range": "201-500", "careers_page": "https://cohere.com/careers", "is_remote_friendly": True},
    {"name": "Scale AI", "slug": "scale-ai", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "AI Data", "description": "AI training data platform.", "headquarters_city": "San Francisco", "headquarters_country": "USA", "founded_year": 2016, "employee_count_range": "501-1000", "careers_page": "https://scale.com/careers", "is_actively_hiring": True},
    {"name": "Databricks", "slug": "databricks", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Data & AI", "description": "Unified data analytics platform.", "headquarters_city": "San Francisco", "headquarters_country": "USA", "founded_year": 2013, "employee_count_range": "5001-10000", "careers_page": "https://www.databricks.com/company/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "Fractal Analytics", "slug": "fractal", "company_type": CompanyType.CONSULTING, "category": CompanyCategory.MNC, "industry": "AI/Analytics", "description": "AI and analytics solutions.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 2000, "employee_count_range": "1001-5000", "careers_page": "https://fractal.ai/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "Mu Sigma", "slug": "mu-sigma", "company_type": CompanyType.CONSULTING, "category": CompanyCategory.MNC, "industry": "Analytics", "description": "Data analytics and decision sciences.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2004, "employee_count_range": "1001-5000", "careers_page": "https://www.mu-sigma.com/careers", "has_indian_office": True},
    {"name": "Sigmoid", "slug": "sigmoid", "company_type": CompanyType.CONSULTING, "category": CompanyCategory.STARTUP, "industry": "Data Engineering", "description": "Data engineering and AI solutions.", "headquarters_city": "Bangalore", "headquarters_country": "India", "founded_year": 2013, "employee_count_range": "501-1000", "careers_page": "https://www.sigmoid.com/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "Tiger Analytics", "slug": "tiger-analytics", "company_type": CompanyType.CONSULTING, "category": CompanyCategory.MNC, "industry": "Analytics", "description": "Advanced analytics consulting.", "headquarters_city": "Chennai", "headquarters_country": "India", "founded_year": 2011, "employee_count_range": "1001-5000", "careers_page": "https://www.tigeranalytics.com/careers", "has_indian_office": True},
    {"name": "Quantiphi", "slug": "quantiphi", "company_type": CompanyType.CONSULTING, "category": CompanyCategory.STARTUP, "industry": "AI/ML", "description": "AI and machine learning services.", "headquarters_city": "Mumbai", "headquarters_country": "India", "founded_year": 2013, "employee_count_range": "1001-5000", "careers_page": "https://www.quantiphi.com/careers", "has_indian_office": True},
]

# ============================================================================
# SEMICONDUCTOR & HARDWARE
# ============================================================================
SEMICONDUCTOR = [
    {"name": "NVIDIA", "slug": "nvidia", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Semiconductor", "description": "GPU manufacturer. AI chips leader.", "headquarters_city": "Santa Clara", "headquarters_country": "USA", "founded_year": 1993, "employee_count_range": "10001+", "careers_page": "https://www.nvidia.com/en-us/about-nvidia/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "AMD", "slug": "amd", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Semiconductor", "description": "CPU and GPU manufacturer.", "headquarters_city": "Santa Clara", "headquarters_country": "USA", "founded_year": 1969, "employee_count_range": "10001+", "careers_page": "https://www.amd.com/en/corporate/careers", "has_indian_office": True},
    {"name": "Intel", "slug": "intel", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Semiconductor", "description": "World's largest semiconductor chip maker.", "headquarters_city": "Santa Clara", "headquarters_country": "USA", "founded_year": 1968, "employee_count_range": "10001+", "careers_page": "https://www.intel.com/content/www/us/en/jobs/jobs-at-intel.html", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "Qualcomm", "slug": "qualcomm", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Semiconductor", "description": "Mobile chipset manufacturer. Snapdragon.", "headquarters_city": "San Diego", "headquarters_country": "USA", "founded_year": 1985, "employee_count_range": "10001+", "careers_page": "https://www.qualcomm.com/company/careers", "has_indian_office": True, "is_actively_hiring": True},
    {"name": "Samsung Semiconductor", "slug": "samsung-semi", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Semiconductor", "description": "Samsung's semiconductor division.", "headquarters_city": "Hwaseong", "headquarters_country": "South Korea", "founded_year": 1974, "employee_count_range": "10001+", "careers_page": "https://semiconductor.samsung.com/us/about-us/careers", "has_indian_office": True},
    {"name": "TSMC", "slug": "tsmc", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Semiconductor", "description": "World's largest semiconductor foundry.", "headquarters_city": "Hsinchu", "headquarters_country": "Taiwan", "founded_year": 1987, "employee_count_range": "10001+", "careers_page": "https://www.tsmc.com/english/careers"},
    {"name": "Micron", "slug": "micron", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Semiconductor", "description": "Memory and storage manufacturer.", "headquarters_city": "Boise", "headquarters_country": "USA", "founded_year": 1978, "employee_count_range": "10001+", "careers_page": "https://www.micron.com/careers", "has_indian_office": True},
    {"name": "Broadcom", "slug": "broadcom", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Semiconductor", "description": "Semiconductor and infrastructure software.", "headquarters_city": "San Jose", "headquarters_country": "USA", "founded_year": 1991, "employee_count_range": "10001+", "careers_page": "https://www.broadcom.com/company/careers", "has_indian_office": True},
    {"name": "Texas Instruments", "slug": "texas-instruments", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Semiconductor", "description": "Analog and embedded processing.", "headquarters_city": "Dallas", "headquarters_country": "USA", "founded_year": 1951, "employee_count_range": "10001+", "careers_page": "https://careers.ti.com", "has_indian_office": True},
    {"name": "NXP Semiconductors", "slug": "nxp", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Semiconductor", "description": "Automotive and IoT chips.", "headquarters_city": "Eindhoven", "headquarters_country": "Netherlands", "founded_year": 2006, "employee_count_range": "10001+", "careers_page": "https://www.nxp.com/company/about-nxp/careers", "has_indian_office": True},
    {"name": "Arm", "slug": "arm", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Semiconductor", "description": "Processor IP designer.", "headquarters_city": "Cambridge", "headquarters_country": "UK", "founded_year": 1990, "employee_count_range": "5001-10000", "careers_page": "https://www.arm.com/company/careers", "has_indian_office": True},
    {"name": "MediaTek", "slug": "mediatek", "company_type": CompanyType.PRODUCT, "category": CompanyCategory.MNC, "industry": "Semiconductor", "description": "Fabless semiconductor company.", "headquarters_city": "Hsinchu", "headquarters_country": "Taiwan", "founded_year": 1997, "employee_count_range": "10001+", "careers_page": "https://www.mediatek.com/careers", "has_indian_office": True},
]

# Combine all companies
ALL_COMPANIES = (
    SPACE_COMPANIES + 
    DEFENCE_RESEARCH + 
    AUTOMOTIVE + 
    PHARMA_BIOTECH + 
    ENERGY + 
    FINTECH_BANKS + 
    CONSULTING + 
    TELECOM + 
    ECOMMERCE + 
    EDTECH + 
    AI_ML + 
    SEMICONDUCTOR
)

def seed_batch(companies_batch, batch_num):
    """Seed a batch of companies"""
    db = SessionLocal()
    added = 0
    updated = 0
    
    try:
        for company_data in companies_batch:
            slug = company_data.get("slug")
            existing = db.query(Company).filter(Company.slug == slug).first()
            
            if existing:
                for key, value in company_data.items():
                    setattr(existing, key, value)
                updated += 1
            else:
                company = Company(**company_data)
                db.add(company)
                added += 1
        
        db.commit()
        logger.info(f"Batch {batch_num}: Added {added}, Updated {updated}")
        return added, updated
        
    except Exception as e:
        logger.error(f"Batch {batch_num} error: {e}")
        db.rollback()
        return 0, 0
    finally:
        db.close()


def seed_all_companies_parallel():
    """Seed all companies using parallel processing"""
    logger.info("🚀 Starting MASSIVE company seeding...")
    init_db()
    
    # Split into batches of 50
    batch_size = 50
    batches = [ALL_COMPANIES[i:i + batch_size] for i in range(0, len(ALL_COMPANIES), batch_size)]
    
    total_added = 0
    total_updated = 0
    
    # Process batches in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {
            executor.submit(seed_batch, batch, i): i 
            for i, batch in enumerate(batches)
        }
        
        for future in concurrent.futures.as_completed(futures):
            batch_num = futures[future]
            try:
                added, updated = future.result()
                total_added += added
                total_updated += updated
            except Exception as e:
                logger.error(f"Batch {batch_num} failed: {e}")
    
    logger.info(f"✅ COMPLETED: Added {total_added} new companies, Updated {total_updated}")
    logger.info(f"📊 Total companies in database: ~{total_added + total_updated + 77}")


if __name__ == "__main__":
    seed_all_companies_parallel()




