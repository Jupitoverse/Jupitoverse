"""
Authentication API Routes
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import re

from app.models.database import get_db
from app.models.user import User, UserProfile, SubscriptionPlan, UserRole
from app.core.security import (
    get_password_hash, verify_password, 
    create_access_token, create_refresh_token, decode_token,
    generate_referral_code, generate_verification_code
)
from app.core.dependencies import get_current_user

router = APIRouter()


# Pydantic Schemas
class UserSignUp(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    referral_code: Optional[str] = None
    
    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


class VerifyEmail(BaseModel):
    email: EmailStr
    code: str


class CompanyVerification(BaseModel):
    company_email: str  # company domain email


@router.post("/signup", response_model=TokenResponse)
async def signup(user_data: UserSignUp, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if email exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check referral code
    referrer = None
    if user_data.referral_code:
        referrer = db.query(User).filter(User.referral_code == user_data.referral_code).first()
        if not referrer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid referral code"
            )
    
    # Create user
    user = User(
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        full_name=user_data.full_name,
        referral_code=generate_referral_code(),
        referred_by=referrer.id if referrer else None,
        subscription_plan=SubscriptionPlan.FREE,
        role=UserRole.USER,
        is_active=True,
        is_verified=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create empty profile
    profile = UserProfile(user_id=user.id)
    db.add(profile)
    
    # Update referrer's count
    if referrer:
        referrer.total_referrals = (referrer.total_referrals or 0) + 1
    
    db.commit()
    
    # Generate tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "subscription_plan": user.subscription_plan.value,
            "is_verified": user.is_verified,
            "is_verified_employee": user.is_verified_employee,
            "referral_code": user.referral_code
        }
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login with email and password"""
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Generate tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "subscription_plan": user.subscription_plan.value,
            "role": user.role.value,
            "is_verified": user.is_verified,
            "is_verified_employee": user.is_verified_employee,
            "referral_code": user.referral_code,
            "avatar_url": user.avatar_url
        }
    )


@router.post("/refresh")
async def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Refresh access token"""
    payload = decode_token(request.refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == int(user_id)).first()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "username": current_user.username,
        "avatar_url": current_user.avatar_url,
        "bio": current_user.bio,
        "subscription_plan": current_user.subscription_plan.value,
        "subscription_active": current_user.subscription_active,
        "role": current_user.role.value,
        "is_verified": current_user.is_verified,
        "is_verified_employee": current_user.is_verified_employee,
        "verified_company_email": current_user.verified_company_email,
        "current_company_name": current_user.current_company_name,
        "current_title": current_user.current_title,
        "linkedin_url": current_user.linkedin_url,
        "github_url": current_user.github_url,
        "referral_code": current_user.referral_code,
        "referral_earnings": current_user.referral_earnings,
        "total_referrals": current_user.total_referrals,
        "created_at": current_user.created_at
    }


@router.post("/verify-company-email")
async def verify_company_email(
    data: CompanyVerification,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Start company email verification process"""
    # Check if email is corporate (not gmail, yahoo, etc.)
    personal_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'icloud.com']
    domain = data.company_email.split('@')[-1].lower()
    
    if domain in personal_domains:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please use your company email address"
        )
    
    # Generate verification code
    code = generate_verification_code()
    
    # Store verification info
    current_user.verified_company_email = data.company_email
    current_user.verification_code = code
    current_user.verification_expires = datetime.utcnow() + timedelta(hours=24)
    db.commit()
    
    # In production, send email here
    # For now, return the code for testing
    return {
        "message": f"Verification code sent to {data.company_email}",
        "code_for_testing": code  # Remove in production
    }


@router.post("/confirm-company-verification")
async def confirm_company_verification(
    data: VerifyEmail,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Confirm company email verification"""
    if current_user.verified_company_email != data.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email mismatch"
        )
    
    if current_user.verification_code != data.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code"
        )
    
    if current_user.verification_expires < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification code expired"
        )
    
    # Mark as verified employee
    current_user.is_verified_employee = True
    current_user.verification_code = None
    db.commit()
    
    return {"message": "Company email verified successfully! You now have a verified badge."}


@router.post("/change-password")
async def change_password(
    data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password"""
    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    current_user.password_hash = get_password_hash(data.new_password)
    db.commit()
    
    return {"message": "Password changed successfully"}


@router.get("/referral-stats")
async def get_referral_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's referral statistics"""
    return {
        "referral_code": current_user.referral_code,
        "total_referrals": current_user.total_referrals or 0,
        "referral_earnings": current_user.referral_earnings or 0,
        "earnings_per_referral": 146,
        "referral_link": f"https://jobhunt.indianaispectrum.com/signup?ref={current_user.referral_code}"
    }


