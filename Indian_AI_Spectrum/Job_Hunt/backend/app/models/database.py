"""
Database Configuration and Session Management
Supports both SQLite (development) and PostgreSQL (production)
"""
import os
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Database URL Configuration
# Priority: Environment variable > PostgreSQL > SQLite
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "job_hunt.db")

# Default to SQLite for easy development, use PostgreSQL in production
DEFAULT_SQLITE_URL = f"sqlite:///{DB_PATH}"
DEFAULT_POSTGRES_URL = "postgresql://careerlaunch_user:password@localhost:5432/careerlaunch"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_SQLITE_URL)

# Engine configuration based on database type
def get_engine():
    """Create database engine with appropriate settings"""
    if "sqlite" in DATABASE_URL:
        # SQLite configuration
        return create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=os.getenv("SQL_ECHO", "false").lower() == "true"
        )
    elif "postgresql" in DATABASE_URL or "postgres" in DATABASE_URL:
        # PostgreSQL configuration
        return create_engine(
            DATABASE_URL,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            echo=os.getenv("SQL_ECHO", "false").lower() == "true"
        )
    else:
        # Generic fallback
        return create_engine(
            DATABASE_URL,
            echo=os.getenv("SQL_ECHO", "false").lower() == "true"
        )

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    from . import company, job, user, resource, country, referral, review, agency, profile, content
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL}")def drop_all_tables():
    """Drop all tables (use with caution!)"""
    Base.metadata.drop_all(bind=engine)
    print("⚠️ All tables dropped!")def get_database_info():
    """Get database connection info"""
    return {
        "url": DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else DATABASE_URL,
        "type": "postgresql" if "postgres" in DATABASE_URL else "sqlite",
        "tables": list(Base.metadata.tables.keys())
    }