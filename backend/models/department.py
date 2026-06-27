"""
OpsPilot AI
Department Model

Stores organization departments.
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


class Department(BaseModel):
    """
    Department model.

    Examples:
        - Engineering
        - Human Resources
        - Finance
        - Marketing
        - Sales
    """

    __tablename__ = "departments"

    # ==========================================================
    # Basic Information
    # ==========================================================

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    code: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
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
        back_populates="department",
        lazy="selectin",
    )

    # ==========================================================
    # Representation
    # ==========================================================

    def __repr__(self) -> str:
        return (
            f"<Department(id={self.id}, "
            f"name='{self.name}', "
            f"code='{self.code}')>"
        )