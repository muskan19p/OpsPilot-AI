"""
OpsPilot AI
Application Configuration

Centralized configuration management using Pydantic Settings.
All environment variables are loaded from the .env file.
"""

from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application Settings"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # =====================================================
    # Application
    # =====================================================

    APP_NAME: str = "OpsPilot AI"

    APP_VERSION: str = "1.0.0"

    APP_DESCRIPTION: str = (
        "Enterprise AI-Powered Business Operations Platform"
    )

    DEBUG: bool = True

    ENVIRONMENT: str = "development"

    # =====================================================
    # API
    # =====================================================

    API_PREFIX: str = "/api/v1"

    # =====================================================
    # Security
    # =====================================================

    SECRET_KEY: str = Field(...)

    ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # =====================================================
    # Database
    # =====================================================

    DATABASE_URL: str = Field(...)

    # =====================================================
    # Groq AI
    # =====================================================

    GROQ_API_KEY: str = Field(...)

    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # =====================================================
    # File Uploads
    # =====================================================

    MAX_UPLOAD_SIZE_MB: int = 20

    UPLOAD_FOLDER: str = "backend/uploads"

    GENERATED_REPORT_FOLDER: str = "generated_reports"

    # =====================================================
    # CORS
    # =====================================================

    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:8501",
        "http://localhost:3000",
        "http://127.0.0.1:8501",
        "http://127.0.0.1:3000",
    ]

    # =====================================================
    # Logging
    # =====================================================

    LOG_LEVEL: str = "INFO"

    # =====================================================
    # Email (Future)
    # =====================================================

    SMTP_SERVER: str = ""

    SMTP_PORT: int = 587

    SMTP_USERNAME: str = ""

    SMTP_PASSWORD: str = ""

    EMAIL_FROM: str = ""

    # =====================================================
    # Redis (Future)
    # =====================================================

    REDIS_URL: str = ""

    # =====================================================
    # Vector Database (Future)
    # =====================================================

    VECTOR_DB_PATH: str = "ai_models/vector_db"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache
def get_settings() -> Settings:
    """
    Returns cached application settings.
    """
    return Settings()


settings = get_settings()