"""
OpsPilot AI
User Schemas

Pydantic schemas for user management.
"""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


# ==========================================================
# Base Schema
# ==========================================================

class UserBase(BaseModel):
    """
    Base user schema.
    """

    employee_id: str = Field(..., min_length=3, max_length=30)
    first_name: str = Field(..., min_length=2, max_length=100)
    last_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr

    phone: str | None = None
    job_title: str | None = None
    experience_years: int = 0

    skills: list[str] = Field(default_factory=list)

    bio: str | None = None
    avatar_url: str | None = None


# ==========================================================
# Create User
# ==========================================================

class UserCreate(UserBase):
    """
    Create new user.
    """

    password: str = Field(..., min_length=8, max_length=128)

    role_id: int
    department_id: int | None = None


# ==========================================================
# Update User
# ==========================================================

class UserUpdate(BaseModel):
    """
    Update user.
    """

    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    job_title: str | None = None
    experience_years: int | None = None

    skills: list[str] | None = None

    bio: str | None = None
    avatar_url: str | None = None

    department_id: int | None = None


# ==========================================================
# User Response
# ==========================================================

class UserResponse(UserBase):
    """
    User API response.
    """

    id: int

    role_id: int
    department_id: int | None

    manager_id: int | None

    is_active: bool
    is_verified: bool
    is_superuser: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


# ==========================================================
# User Profile
# ==========================================================

class UserProfile(UserResponse):
    """
    User profile response.
    """

    last_login: datetime | None


# ==========================================================
# Dashboard Card
# ==========================================================

class UserDashboard(BaseModel):
    """
    Dashboard summary.
    """

    total_tasks: int = 0
    completed_tasks: int = 0
    pending_tasks: int = 0

    meetings_today: int = 0

    productivity_score: float = 0.0


# ==========================================================
# User List
# ==========================================================

class UserListResponse(BaseModel):
    """
    List of users.
    """

    total: int
    users: list[UserResponse]