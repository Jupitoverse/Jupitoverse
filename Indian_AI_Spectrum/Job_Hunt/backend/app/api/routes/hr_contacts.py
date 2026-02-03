"""
HR Contacts API Routes - Premium/Pro Feature
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from pydantic import BaseModel
from app.models.database import get_db
from app.models.hr_contact import HRContact, HRContactVisibility
from app.models.user import User, SubscriptionPlan, UserRole
from app.core.dependencies import get_current_user, get_current_user_optional, get_pro_user, get_admin_user

router = APIRouter()


class HRContactUpdate(BaseModel):
    visibility: Optional[str] = None
    is_active: Optional[bool] = None


class BulkVisibilityUpdate(BaseModel):
    contact_ids: list[int]
    visibility: str
    

def filter_contacts_by_subscription(user, query):
    """Filter HR contacts based on user's subscription"""
    if user is None:
        # Not logged in - show only 'all' visibility
        return query.filter(HRContact.visibility == HRContactVisibility.ALL)
    
    if user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        return query
    
    if user.subscription_plan == SubscriptionPlan.PRO:
        return query.filter(HRContact.visibility != HRContactVisibility.HIDDEN)
    elif user.subscription_plan == SubscriptionPlan.PREMIUM:
        return query.filter(
            HRContact.visibility.in_([HRContactVisibility.ALL, HRContactVisibility.PREMIUM])
        )
    else:
        return query.filter(HRContact.visibility == HRContactVisibility.ALL)


@router.get("/")
async def get_hr_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    company: Optional[str] = None,
    title: Optional[str] = None,
    search: Optional[str] = None
):
    """
    Get HR contacts based on user's subscription level.
    - Free users: See limited contacts (visibility='all')
    - Premium users (₹499): See more contacts (visibility='all', 'premium')
    - Pro users (₹999): See all contacts except hidden
    - Admin: See everything
    """
    query = db.query(HRContact).filter(HRContact.is_active == True)
    
    # Apply subscription-based filtering
    query = filter_contacts_by_subscription(current_user, query)
    
    # Apply search filters
    if company:
        query = query.filter(HRContact.company_name.ilike(f"%{company}%"))
    if title:
        query = query.filter(HRContact.title.ilike(f"%{title}%"))
    if search:
        query = query.filter(
            (HRContact.name.ilike(f"%{search}%")) |
            (HRContact.company_name.ilike(f"%{search}%")) |
            (HRContact.title.ilike(f"%{search}%"))
        )
    
    total = query.count()
    contacts = query.order_by(HRContact.company_name).offset(skip).limit(limit).all()
    
    # Determine what user can see
    can_see_email = current_user is not None and (
        current_user.subscription_plan in [SubscriptionPlan.PREMIUM, SubscriptionPlan.PRO] or
        current_user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]
    )
    
    # Format response
    result = []
    for contact in contacts:
        contact_data = {
            "id": contact.id,
            "name": contact.name,
            "title": contact.title,
            "company_name": contact.company_name,
            "seniority_level": contact.seniority_level,
        }
        
        # Only show email for paid users
        if can_see_email:
            contact_data["email"] = contact.email
            contact_data["linkedin_url"] = contact.linkedin_url
            contact_data["phone"] = contact.phone
        else:
            # Mask email for free users
            email_parts = contact.email.split('@') if contact.email else ['***', '***']
            contact_data["email"] = f"{email_parts[0][:3]}***@{email_parts[1]}" if len(email_parts) > 1 else "***@***.com"
            contact_data["upgrade_message"] = "Upgrade to Premium or Pro to see full contact details"
        
        result.append(contact_data)
    
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "subscription": current_user.subscription_plan.value if current_user else "guest",
        "can_see_full_details": can_see_email,
        "contacts": result
    }


@router.get("/stats")
async def get_hr_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    """Get HR contacts statistics"""
    total = db.query(HRContact).filter(HRContact.is_active == True).count()
    
    # Count by visibility
    by_visibility = db.query(
        HRContact.visibility, func.count(HRContact.id)
    ).filter(HRContact.is_active == True).group_by(HRContact.visibility).all()
    
    # Count by company
    top_companies = db.query(
        HRContact.company_name, func.count(HRContact.id)
    ).filter(HRContact.is_active == True).group_by(
        HRContact.company_name
    ).order_by(func.count(HRContact.id).desc()).limit(10).all()
    
    return {
        "total_contacts": total,
        "your_subscription": current_user.subscription_plan.value if current_user else "guest",
        "accessible_count": filter_contacts_by_subscription(
            current_user, 
            db.query(HRContact).filter(HRContact.is_active == True)
        ).count(),
        "top_companies": [{"company": c[0], "count": c[1]} for c in top_companies]
    }


@router.get("/companies")
async def get_companies_with_contacts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional),
    skip: int = 0,
    limit: int = 50
):
    """Get list of companies that have HR contacts"""
    query = db.query(
        HRContact.company_name,
        func.count(HRContact.id).label('contact_count')
    ).filter(HRContact.is_active == True)
    
    query = filter_contacts_by_subscription(current_user, query)
    
    companies = query.group_by(HRContact.company_name).order_by(
        func.count(HRContact.id).desc()
    ).offset(skip).limit(limit).all()
    
    return [{"company": c[0], "contact_count": c[1]} for c in companies]


# Admin Routes
@router.get("/admin/all")
async def admin_get_all_contacts(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user),
    skip: int = 0,
    limit: int = 100,
    visibility: Optional[str] = None
):
    """Admin: Get all HR contacts with full details"""
    query = db.query(HRContact)
    
    if visibility:
        query = query.filter(HRContact.visibility == visibility)
    
    total = query.count()
    contacts = query.offset(skip).limit(limit).all()
    
    return {
        "total": total,
        "contacts": contacts
    }


@router.put("/admin/{contact_id}")
async def admin_update_contact(
    contact_id: int,
    update_data: HRContactUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """Admin: Update HR contact visibility or status"""
    contact = db.query(HRContact).filter(HRContact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    if update_data.visibility:
        contact.visibility = HRContactVisibility(update_data.visibility)
    if update_data.is_active is not None:
        contact.is_active = update_data.is_active
    
    db.commit()
    return {"message": "Contact updated", "contact_id": contact_id}


@router.post("/admin/bulk-visibility")
async def admin_bulk_update_visibility(
    data: BulkVisibilityUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """Admin: Update visibility for multiple contacts"""
    visibility = HRContactVisibility(data.visibility)
    
    updated = db.query(HRContact).filter(
        HRContact.id.in_(data.contact_ids)
    ).update({"visibility": visibility}, synchronize_session=False)
    
    db.commit()
    return {"message": f"Updated {updated} contacts", "visibility": data.visibility}


@router.post("/admin/set-visibility-percentage")
async def admin_set_visibility_percentage(
    pro_percentage: int = Query(100, ge=0, le=100),
    premium_percentage: int = Query(50, ge=0, le=100),
    free_percentage: int = Query(10, ge=0, le=100),
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    """
    Admin: Set what percentage of contacts each plan can see.
    Example: Pro=100%, Premium=50%, Free=10%
    """
    total_contacts = db.query(HRContact).filter(HRContact.is_active == True).count()
    
    # Calculate counts
    pro_count = int(total_contacts * pro_percentage / 100)
    premium_count = int(total_contacts * premium_percentage / 100)
    free_count = int(total_contacts * free_percentage / 100)
    
    # Get all active contacts ordered by ID
    all_contacts = db.query(HRContact).filter(
        HRContact.is_active == True
    ).order_by(HRContact.id).all()
    
    # Assign visibility
    for i, contact in enumerate(all_contacts):
        if i < free_count:
            contact.visibility = HRContactVisibility.ALL
        elif i < premium_count:
            contact.visibility = HRContactVisibility.PREMIUM
        elif i < pro_count:
            contact.visibility = HRContactVisibility.PRO
        else:
            contact.visibility = HRContactVisibility.HIDDEN
    
    db.commit()
    
    return {
        "message": "Visibility updated",
        "total_contacts": total_contacts,
        "free_can_see": free_count,
        "premium_can_see": premium_count,
        "pro_can_see": pro_count
    }

