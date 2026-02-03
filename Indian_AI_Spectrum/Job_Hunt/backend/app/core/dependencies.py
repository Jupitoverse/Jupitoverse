"""
FastAPI Dependencies for authentication and authorization
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from app.models.database import get_db
from app.models.user import User, UserRole, SubscriptionPlan
from app.core.security import decode_token

# HTTP Bearer token scheme
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = credentials.credentials
    payload = decode_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    return user


async def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """Get the current user if authenticated, otherwise None"""
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Ensure user is active"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_premium_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Ensure user has Premium or higher subscription"""
    if current_user.subscription_plan not in [SubscriptionPlan.PREMIUM, SubscriptionPlan.PRO]:
        if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Premium subscription required"
            )
    return current_user


async def get_pro_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Ensure user has Pro subscription"""
    if current_user.subscription_plan != SubscriptionPlan.PRO:
        if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Pro subscription required"
            )
    return current_user


async def get_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Ensure user is an admin"""
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


async def get_super_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Ensure user is a super admin"""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin access required"
        )
    return current_user


def check_hr_contact_access(user: User, visibility: str) -> bool:
    """Check if user can access HR contact based on visibility"""
    if user.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        return True
    
    if visibility == "hidden":
        return False
    elif visibility == "pro":
        return user.subscription_plan == SubscriptionPlan.PRO
    elif visibility == "premium":
        return user.subscription_plan in [SubscriptionPlan.PREMIUM, SubscriptionPlan.PRO]
    else:  # "all"
        return True


