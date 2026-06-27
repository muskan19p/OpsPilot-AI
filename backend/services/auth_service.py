"""
OpsPilot AI
Authentication Service

Contains business logic for user authentication.
"""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy.orm import Session
from torch.multiprocessing import AuthenticationError
from backend.core.exceptions import (
    AuthenticationError,
    DuplicateResourceError,
)

from backend.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from backend.models.user import User
from backend.repositories.user_repository import UserRepository
from backend.schemas.auth import (
    AuthResponse,
    LoginRequest,
    RegisterRequest,
)


class AuthService:
    """
    Handles authentication business logic.
    """

    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)

    # ==========================================================
    # Register
    # ==========================================================

    def register(
        self,
        request: RegisterRequest,
    ) -> AuthResponse:
        """
        Register a new user.
        """

        if self.user_repository.email_exists(request.email):
            raise DuplicateResourceError(
                 "Email already exists." 
                )

        if self.user_repository.employee_id_exists(
            request.employee_id
        ):
            raise DuplicateResourceError(
    "Employee ID already exists."
)

        user = User(
            employee_id=request.employee_id,
            first_name=request.first_name,
            last_name=request.last_name,
            email=request.email,
            phone=request.phone,
            hashed_password=hash_password(request.password),
            role_id=request.role_id,
            department_id=request.department_id,
        )

        self.user_repository.create(user)

        token = create_access_token(
            subject=user.email,
        )

        return AuthResponse(
            success=True,
            message="Registration successful.",
            access_token=token,
        )

    # ==========================================================
    # Login
    # ==========================================================

    def login(
        self,
        request: LoginRequest,
    ) -> AuthResponse:
        """
        Authenticate a user.
        """

        user = self.user_repository.get_by_email(
            request.email,
        )

        if user is None:
            raise AuthenticationError(
    "Invalid email or password."
         )

        if not verify_password(
            request.password,
            user.hashed_password,
        ):
            raise AuthenticationError(
                "Invalid email or password."
            )

        if not user.is_active:
            raise AuthenticationError(
                "User account is inactive."
            )

        user.last_login = datetime.now(
            timezone.utc,
        )

        self.user_repository.update(user)

        token = create_access_token(
            subject=user.email,
        )

        return AuthResponse(
            success=True,
            message="Login successful.",
            access_token=token,
        )
        
        from backend.core.exceptions import (
    AuthenticationError,
    DuplicateResourceError,
)


    # ==========================================================
    # Get Current User
    # ==========================================================

    def get_current_user(self, email: str) -> User:
        """
        Get authenticated user by email.
        """

        user = self.user_repository.get_by_email(email)

        if user is None:
            raise AuthenticationError(
                "User not found."
            )

        if not user.is_active:
            raise AuthenticationError(
                "User account is inactive."
            )

        return user

    # ==========================================================
    # Change Password
    # ==========================================================

    def change_password(
        self,
        user: User,
        current_password: str,
        new_password: str,
    ) -> bool:
        """
        Change user password.
        """

        if not verify_password(
            current_password,
            user.hashed_password,
        ):
            raise AuthenticationError(
                "Current password is incorrect."
            )

        user.hashed_password = hash_password(
            new_password,
        )

        self.user_repository.update(user)

        return True

    # ==========================================================
    # Forgot Password
    # ==========================================================

    def forgot_password(
        self,
        email: str,
    ) -> bool:
        """
        Initiate forgot password workflow.

        Email sending will be implemented later.
        """

        user = self.user_repository.get_by_email(email)

        if user is None:
            raise AuthenticationError(
                "No account found with this email."
            )

        # Future:
        # Generate reset token
        # Store token
        # Send email

        return True

    # ==========================================================
    # Reset Password
    # ==========================================================

    def reset_password(
        self,
        email: str,
        new_password: str,
    ) -> bool:
        """
        Reset user password.

        Token verification will be added later.
        """

        user = self.user_repository.get_by_email(email)

        if user is None:
            raise AuthenticationError(
                "User not found."
            )

        user.hashed_password = hash_password(
            new_password,
        )

        self.user_repository.update(user)

        return True