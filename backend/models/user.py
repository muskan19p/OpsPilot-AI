"""
OpsPilot AI
User Model

Enterprise User Model
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Text
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.role import Role
    from backend.models.department import Department
    
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from backend.models.base import BaseModel


class User(BaseModel):

    __tablename__ = "users"

    # =====================================================
    # Employee Information
    # =====================================================

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

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # =====================================================
    # Profile
    # =====================================================

    profile_image: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    bio: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    job_title: Mapped[str | None] = mapped_column(
        String(120),
        nullable=True,
    )

    experience: Mapped[int] = mapped_column(
        default=0,
    )

    skills: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # =====================================================
    # Foreign Keys
    # =====================================================

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False,
    )

    department_id: Mapped[int | None] = mapped_column(
        ForeignKey("departments.id"),
    )

    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
    )

    # =====================================================
    # Account
    # =====================================================

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    last_login: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # =====================================================
    # Relationships
    # =====================================================

    role: Mapped["Role"] = relationship(
    back_populates="users",
    lazy="joined",
)
    department: Mapped["Department"] = relationship(
    back_populates="users",
    lazy="joined",
)
    

    manager: Mapped["User"] = relationship(
        "User",
        remote_side="User.id",
        back_populates="subordinates",
    )

    subordinates: Mapped[list["User"]] = relationship(
        "User",
        back_populates="manager",
    )

    # Future Relationships

    meetings = relationship(
        "Meeting",
        back_populates="user",
    )

    tasks = relationship(
        "Task",
        back_populates="user",
    )

    tickets = relationship(
        "Ticket",
        back_populates="user",
    )

    notifications = relationship(
        "Notification",
        back_populates="user",
    )

    activities = relationship(
        "Activity",
        back_populates="user",
    )

    # =====================================================
    # Properties
    # =====================================================

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    # =====================================================
    # Representation
    # =====================================================

    def __repr__(self) -> str:

        return (
            f"<User(id={self.id}, "
            f"employee_id='{self.employee_id}', "
            f"email='{self.email}')>"
        )