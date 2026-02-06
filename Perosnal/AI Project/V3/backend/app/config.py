from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Default: SQLite (no Docker). Set DATABASE_URL for PostgreSQL.
    database_url: str = "sqlite:///./annotation.db"
    secret_key: str = "demo-secret-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24 hours

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
