from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Using SQLite for local development (no PostgreSQL needed)
db_url = "sqlite:///./products.db"
engine = create_engine(db_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
