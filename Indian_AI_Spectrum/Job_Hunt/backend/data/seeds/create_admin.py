"""
Create Admin User
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.database import SessionLocal, init_db
from app.models.user import User, UserRole, SubscriptionPlan
from app.core.security import get_password_hash, generate_referral_code

def create_admin():
    """Create admin user"""
    init_db()
    db = SessionLocal()
    
    try:
        # Check if admin exists
        admin = db.query(User).filter(User.role == UserRole.SUPER_ADMIN).first()
        if admin:
            print(f"Admin already exists: {admin.email}")
            return
        
        # Create admin user
        admin = User(
            email="admin@indianaispectrum.com",
            password_hash=get_password_hash("Admin@123"),
            full_name="Admin User",
            username="admin",
            role=UserRole.SUPER_ADMIN,
            subscription_plan=SubscriptionPlan.PRO,
            subscription_active=True,
            referral_code=generate_referral_code(),
            is_active=True,
            is_verified=True
        )
        db.add(admin)
        db.commit()
        
        print("[OK] Admin user created!")
        print("Email: admin@indianaispectrum.com")
        print("Password: Admin@123")
        print("[!] Please change the password after first login!")
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
