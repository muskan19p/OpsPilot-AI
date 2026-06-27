"""
OpsPilot AI
Authentication Router

Authentication APIs.
"""

from __future__ import annotations

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.dependencies import get_current_active_user
from backend.core.exceptions import (
    AuthenticationError,
    DuplicateResourceError,
)

from backend.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    AuthResponse,
)

from backend.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


# ==========================================================
# Register
# ==========================================================

@router.post(
    "/register",
    response_model=AuthResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):

    service = AuthService(db)

    try:
        return service.register(request)

    except DuplicateResourceError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )


# ==========================================================
# Login
# ==========================================================

@router.post(
    "/login",
    response_model=AuthResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):

    service = AuthService(db)

    try:
        return service.login(request)

    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )
        
        # ==========================================================
# Current User
# ==========================================================

@router.get(
    "/me",
)
def me(
    current_user=Depends(get_current_active_user),
):
    """
    Return currently authenticated user.
    """

    return current_user


# ==========================================================
# Change Password
# ==========================================================

@router.post(
    "/change-password",
)
def change_password(
    request: ChangePasswordRequest,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    Change user password.
    """

    service = AuthService(db)

    try:

        service.change_password(
            current_user,
            request.current_password,
            request.new_password,
        )

        return {
            "success": True,
            "message": "Password changed successfully.",
        }

    except AuthenticationError as e:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )


# ==========================================================
# Forgot Password
# ==========================================================

@router.post(
    "/forgot-password",
)
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db),
):
    """
    Forgot password endpoint.
    """

    service = AuthService(db)

    try:

        service.forgot_password(
            request.email,
        )

        return {
            "success": True,
            "message": "Password reset link generated.",
        }

    except AuthenticationError as e:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )


# ==========================================================
# Reset Password
# ==========================================================

@router.post(
    "/reset-password",
)
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db),
):
    """
    Reset password endpoint.
    """

    service = AuthService(db)

    try:

        service.reset_password(
            request.token,
            request.new_password,
        )

        return {
            "success": True,
            "message": "Password reset successfully.",
        }

    except AuthenticationError as e:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
        )