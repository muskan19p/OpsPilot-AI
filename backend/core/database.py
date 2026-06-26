"""
OpsPilot AI
Database Configuration

Creates:
- SQLAlchemy Engine
- Session Factory
- Declarative Base
- Database Dependency
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

from backend.core.config import settings

# ==========================================================
# Database Engine
# ==========================================================

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=settings.DEBUG,
)

# ==========================================================
# Session Factory
# ==========================================================

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ==========================================================
# Base Model
# ==========================================================

Base = declarative_base()

# ==========================================================
# Dependency
# ==========================================================


def get_db():
    """
    FastAPI dependency.

    Example:
        db: Session = Depends(get_db)
    """

    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# ==========================================================
# Utility
# ==========================================================


def create_tables():
    """
    Create all database tables.

    Used only during development.
    Alembic will handle migrations in production.
    """
    Base.metadata.create_all(bind=engine)