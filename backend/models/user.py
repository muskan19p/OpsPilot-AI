"""
OpsPilot AI
User Model

Enterprise User model for authentication,
employee management, and role-based access control.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import JSON
from sqlalchemy import String
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from backend.models.base import BaseModel

if TYPE_CHECKING:
    from backend.models.department import Department
    from backend.models.role import Role


class User(BaseModel):
    """
    User model.

    Represents every employee, manager,
    and administrator in OpsPilot AI.
    """

    __tablename__ = "users"

    # ==========================================================
    # Employee Information
    # ==========================================================

    employee_id: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
        index=True,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    # ==========================================================
    # Authentication
    # ==========================================================

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ==========================================================
    # Professional Information
    # ==========================================================

    job_title: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )

    experience_years: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    skills: Mapped[list | None] = mapped_column(
        JSON,
        nullable=True,
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    avatar_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # ==========================================================
    # Foreign Keys
    # ==========================================================

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
        index=True,
    )

    department_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id"),
        nullable=True,
        index=True,
    )

    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=True,
        index=True,
    )
    
        # ==========================================================
    # Relationships
    # ==========================================================

    role: Mapped["Role"] = relationship(
        back_populates="users",
        lazy="joined",
    )

    department: Mapped["Department | None"] = relationship(
        back_populates="users",
        lazy="joined",
    )

    # ==========================================================
    # Self Referencing Relationship
    # ==========================================================

    manager: Mapped["User | None"] = relationship(
        "User",
        remote_side="User.id",
        back_populates="subordinates",
        foreign_keys=[manager_id],
    )

    subordinates: Mapped[list["User"]] = relationship(
        "User",
        back_populates="manager",
        foreign_keys="User.manager_id",
        cascade="save-update",
    )

    # ==========================================================
    # Future Relationships
    # ==========================================================
    
    
        # ==========================================================
    # Properties
    # ==========================================================

    @property
    def full_name(self) -> str:
        """
        Return user's full name.
        """
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def initials(self) -> str:
        """
        Return user initials.

        Example:
            Muskan Sharma -> MS
        """
        first = self.first_name[:1] if self.first_name else ""
        last = self.last_name[:1] if self.last_name else ""

        return f"{first}{last}".upper()

    @property
    def is_manager(self) -> bool:
        """
        Check whether the user manages
        at least one employee.
        """
        return len(self.subordinates) > 0

    # ==========================================================
    # Utility Methods
    # ==========================================================

    def to_dict(self) -> dict:
        """
        Convert user object to dictionary.
        Useful for APIs and debugging.
        """

        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "job_title": self.job_title,
            "experience_years": self.experience_years,
            "skills": self.skills,
            "bio": self.bio,
            "avatar_url": self.avatar_url,
            "role_id": self.role_id,
            "department_id": self.department_id,
            "manager_id": self.manager_id,
            "is_active": self.is_active,
            "is_verified": self.is_verified,
            "is_superuser": self.is_superuser,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_login": (
                self.last_login.isoformat()
                if self.last_login
                else None
            ),
        }

    # ==========================================================
    # Representation
    # ==========================================================

    def __repr__(self) -> str:
        return (
            f"<User("
            f"id={self.id}, "
            f"employee_id='{self.employee_id}', "
            f"email='{self.email}'"
            f")>"
        )