"""
OpsPilot AI
User Repository

Handles all database operations related to users.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models.user import User


class UserRepository:
    """
    Repository for User model.
    """

    def __init__(self, db: Session):
        self.db = db

    # ==========================================================
    # Create
    # ==========================================================

    def create(self, user: User) -> User:
        """
        Create a new user.
        """
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    # ==========================================================
    # Read
    # ==========================================================

    def get_by_id(self, user_id: int) -> User | None:
        """
        Get user by ID.
        """
        stmt = select(User).where(User.id == user_id)
        return self.db.scalar(stmt)

    def get_by_email(self, email: str) -> User | None:
        """
        Get user by email.
        """
        stmt = select(User).where(User.email == email)
        return self.db.scalar(stmt)

    def get_by_employee_id(self, employee_id: str) -> User | None:
        """
        Get user by employee ID.
        """
        stmt = select(User).where(
            User.employee_id == employee_id
        )
        return self.db.scalar(stmt)

    def get_all(self) -> list[User]:
        """
        Return all users.
        """
        stmt = select(User).order_by(User.first_name)
        return list(self.db.scalars(stmt).all())

    # ==========================================================
    # Update
    # ==========================================================

    def update(self, user: User) -> User:
        """
        Update an existing user.
        """
        self.db.commit()
        self.db.refresh(user)
        return user

    # ==========================================================
    # Delete
    # ==========================================================

    def delete(self, user: User) -> None:
        """
        Delete user.
        """
        self.db.delete(user)
        self.db.commit()

    # ==========================================================
    # Utility
    # ==========================================================

    def email_exists(self, email: str) -> bool:
        """
        Check whether email already exists.
        """
        return self.get_by_email(email) is not None

    def employee_id_exists(self, employee_id: str) -> bool:
        """
        Check whether employee ID already exists.
        """
        return (
            self.get_by_employee_id(employee_id)
            is not None
        )