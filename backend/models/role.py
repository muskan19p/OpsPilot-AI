"""
OpsPilot AI
Role Model

Defines user roles used for Role-Based Access Control (RBAC).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from backend.models.base import BaseModel

if TYPE_CHECKING:
    from backend.models.user import User


class Role(BaseModel):
    """
    Role model.

    Examples:
        - Admin
        - Manager
        - Employee
    """

    __tablename__ = "roles"

    # ==========================================================
    # Basic Information
    # ==========================================================

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    display_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # ==========================================================
    # Relationships
    # ==========================================================

    users: Mapped[list["User"]] = relationship(
        back_populates="role",
        lazy="selectin",
    )

    # ==========================================================
    # Representation
    # ==========================================================

    def __repr__(self) -> str:
        return (
            f"<Role(id={self.id}, "
            f"name='{self.name}')>"
        )