"""
Users API Routes - User profiles and preferences
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.user import User, UserProfile

router = APIRouter()

@router.get("/me")
async def get_current_user():
    """Get current user - placeholder for auth"""
    # TODO: Implement authentication
    return {"message": "Authentication not implemented yet"}

@router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID (public profile)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Return only public info
    return {
        "id": user.id,
        "username": user.username,
        "full_name": user.full_name,
        "avatar_url": user.avatar_url,
        "current_title": user.current_title,
        "linkedin_url": user.linkedin_url,
        "github_url": user.github_url,
        "portfolio_url": user.portfolio_url
    }

@router.get("/{user_id}/profile")
async def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """Get user profile"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

# TODO: Add POST, PUT endpoints for creating and updating users/profiles
# These would require authentication




