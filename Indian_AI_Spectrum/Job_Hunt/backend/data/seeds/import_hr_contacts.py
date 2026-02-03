"""
Import HR Contacts from PDF and Excel files
"""
import sys
import os
import logging
import pdfplumber
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import SessionLocal, init_db
from app.models.hr_contact import HRContact, HRContactVisibility

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def determine_seniority(title: str) -> str:
    """Determine seniority level from title"""
    title_lower = title.lower() if title else ""
    
    if any(x in title_lower for x in ['chief', 'cxo', 'ceo', 'cto', 'cfo', 'chro', 'cpo']):
        return "C-Level"
    elif any(x in title_lower for x in ['vp', 'vice president']):
        return "VP"
    elif any(x in title_lower for x in ['director', 'head']):
        return "Director/Head"
    elif any(x in title_lower for x in ['manager', 'lead', 'senior']):
        return "Manager/Lead"
    elif any(x in title_lower for x in ['associate', 'executive', 'officer']):
        return "Associate"
    else:
        return "Other"


def import_from_pdf(pdf_path: str, db):
    """Import HR contacts from PDF"""
    logger.info(f"📄 Importing from PDF: {pdf_path}")
    
    added = 0
    updated = 0
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            
            for table in tables:
                for row in table:
                    # Skip header row
                    if row and row[0] and (row[0] == 'SNo' or row[0].isdigit() == False and row[0] != '1'):
                        continue
                    
                    try:
                        # Expected format: [SNo, Name, Email, Title, Company]
                        if len(row) >= 5:
                            sno, name, email, title, company = row[0], row[1], row[2], row[3], row[4]
                            
                            if not email or '@' not in str(email):
                                continue
                            
                            # Check if exists
                            existing = db.query(HRContact).filter(
                                HRContact.email == email.strip()
                            ).first()
                            
                            if existing:
                                # Update
                                existing.name = name.strip() if name else existing.name
                                existing.title = title.strip() if title else existing.title
                                existing.company_name = company.strip() if company else existing.company_name
                                existing.seniority_level = determine_seniority(title)
                                updated += 1
                            else:
                                # Create new
                                contact = HRContact(
                                    name=name.strip() if name else "Unknown",
                                    email=email.strip(),
                                    title=title.strip() if title else None,
                                    company_name=company.strip() if company else None,
                                    seniority_level=determine_seniority(title),
                                    visibility=HRContactVisibility.PRO,  # Default to Pro only
                                    source="pdf_import",
                                    is_active=True
                                )
                                db.add(contact)
                                added += 1
                    
                    except Exception as e:
                        logger.warning(f"Error processing row: {row}, Error: {e}")
                        continue
            
            if (page_num + 1) % 10 == 0:
                logger.info(f"  Processed {page_num + 1} pages...")
                db.commit()
    
    db.commit()
    logger.info(f"✅ PDF Import: Added {added}, Updated {updated}")
    return added, updated


def import_from_excel(excel_path: str, db):
    """Import HR contacts from Excel"""
    logger.info(f"📊 Importing from Excel: {excel_path}")
    
    added = 0
    updated = 0
    
    try:
        df = pd.read_excel(excel_path)
        
        # Try to identify columns
        columns = df.columns.tolist()
        logger.info(f"Excel columns: {columns}")
        
        # Map columns (adjust based on actual file structure)
        # Assuming structure similar to PDF: SNo, Name, Email, Title, Company
        name_col = None
        email_col = None
        title_col = None
        company_col = None
        
        # Try to auto-detect columns
        for i, col in enumerate(columns):
            col_lower = str(col).lower()
            first_value = str(df.iloc[0, i]).lower() if len(df) > 0 else ""
            
            if 'name' in col_lower or (i == 1 and '@' not in first_value):
                name_col = i
            elif 'email' in col_lower or '@' in first_value:
                email_col = i
            elif 'title' in col_lower or 'position' in col_lower or 'role' in col_lower:
                title_col = i
            elif 'company' in col_lower or 'organization' in col_lower:
                company_col = i
        
        # Fallback to positional if not found
        if email_col is None and len(columns) >= 3:
            name_col, email_col, title_col, company_col = 1, 2, 3, 4
        
        logger.info(f"Detected columns - Name: {name_col}, Email: {email_col}, Title: {title_col}, Company: {company_col}")
        
        for idx, row in df.iterrows():
            try:
                email = str(row.iloc[email_col]).strip() if email_col is not None and pd.notna(row.iloc[email_col]) else None
                
                if not email or '@' not in email:
                    continue
                
                name = str(row.iloc[name_col]).strip() if name_col is not None and pd.notna(row.iloc[name_col]) else "Unknown"
                title = str(row.iloc[title_col]).strip() if title_col is not None and pd.notna(row.iloc[title_col]) else None
                company = str(row.iloc[company_col]).strip() if company_col is not None and pd.notna(row.iloc[company_col]) else None
                
                # Clean up 'nan' strings
                if name == 'nan':
                    name = "Unknown"
                if title == 'nan':
                    title = None
                if company == 'nan':
                    company = None
                
                # Check if exists
                existing = db.query(HRContact).filter(HRContact.email == email).first()
                
                if existing:
                    existing.name = name if name != "Unknown" else existing.name
                    existing.title = title or existing.title
                    existing.company_name = company or existing.company_name
                    existing.seniority_level = determine_seniority(title)
                    updated += 1
                else:
                    contact = HRContact(
                        name=name,
                        email=email,
                        title=title,
                        company_name=company,
                        seniority_level=determine_seniority(title),
                        visibility=HRContactVisibility.PRO,
                        source="excel_import",
                        is_active=True
                    )
                    db.add(contact)
                    added += 1
                
                if (idx + 1) % 500 == 0:
                    logger.info(f"  Processed {idx + 1} rows...")
                    db.commit()
            
            except Exception as e:
                logger.warning(f"Error processing row {idx}: {e}")
                continue
        
        db.commit()
        logger.info(f"✅ Excel Import: Added {added}, Updated {updated}")
        
    except Exception as e:
        logger.error(f"Error reading Excel: {e}")
    
    return added, updated


def set_visibility_distribution(db):
    """Set visibility distribution: 10% free, 40% premium, 50% pro"""
    logger.info("🔧 Setting visibility distribution...")
    
    total = db.query(HRContact).filter(HRContact.is_active == True).count()
    
    free_count = int(total * 0.10)  # 10% for free users
    premium_count = int(total * 0.40)  # 40% for premium users (includes free)
    # Remaining 50% for pro users
    
    all_contacts = db.query(HRContact).filter(
        HRContact.is_active == True
    ).order_by(HRContact.id).all()
    
    for i, contact in enumerate(all_contacts):
        if i < free_count:
            contact.visibility = HRContactVisibility.ALL
        elif i < premium_count:
            contact.visibility = HRContactVisibility.PREMIUM
        else:
            contact.visibility = HRContactVisibility.PRO
    
    db.commit()
    
    logger.info(f"✅ Visibility set: Free={free_count}, Premium={premium_count-free_count}, Pro={total-premium_count}")


def main():
    logger.info("🚀 Starting HR Contact Import...")
    
    init_db()
    db = SessionLocal()
    
    try:
        # Paths to data files
        base_path = r"C:\Users\abhisha3\Desktop\Projects\Indian_AI_Spectrum\Job_Hunt\My Data"
        pdf_path = os.path.join(base_path, "CompanyWise HR contact.pdf")
        excel_path = os.path.join(base_path, "hr list.xlsx")
        
        total_added = 0
        total_updated = 0
        
        # Import from PDF
        if os.path.exists(pdf_path):
            added, updated = import_from_pdf(pdf_path, db)
            total_added += added
            total_updated += updated
        else:
            logger.warning(f"PDF not found: {pdf_path}")
        
        # Import from Excel
        if os.path.exists(excel_path):
            added, updated = import_from_excel(excel_path, db)
            total_added += added
            total_updated += updated
        else:
            logger.warning(f"Excel not found: {excel_path}")
        
        # Set visibility distribution
        set_visibility_distribution(db)
        
        # Final stats
        total = db.query(HRContact).count()
        active = db.query(HRContact).filter(HRContact.is_active == True).count()
        
        logger.info(f"""
        ========================================
        📊 HR CONTACT IMPORT COMPLETE
        ========================================
        Total Added: {total_added}
        Total Updated: {total_updated}
        Total in Database: {total}
        Active Contacts: {active}
        ========================================
        """)
        
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()


