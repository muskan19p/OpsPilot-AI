"""
OpsPilot AI
Role Model

Defines user roles for Role-Based Access Control (RBAC).
"""

from sqlalchemy import Boolean
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.models.user import User
    
from backend.models.base import BaseModel


class Role(BaseModel):
    """
    User Role Model.
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
    # String Representation
    # ==========================================================

    def __repr__(self) -> str:
        return (
            f"<Role(id={self.id}, "
            f"name='{self.name}')>"
        )