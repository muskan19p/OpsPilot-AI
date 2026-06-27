"""
OpsPilot AI
Authentication Schemas

Pydantic schemas for authentication and authorization.
"""

from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import Field


# ==========================================================
# Login
# ==========================================================

class LoginRequest(BaseModel):
    """
    User login request.
    """

    email: EmailStr
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )


# ==========================================================
# Register
# ==========================================================

class RegisterRequest(BaseModel):
    """
    User registration request.
    """

    employee_id: str = Field(
        ...,
        min_length=3,
        max_length=30,
    )

    first_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    last_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
    )

    email: EmailStr

    phone: str | None = None

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

    role_id: int

    department_id: int | None = None


# ==========================================================
# JWT Token
# ==========================================================

class Token(BaseModel):
    """
    JWT access token response.
    """

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    JWT payload.
    """

    sub: str
    exp: int


# ==========================================================
# Password Management
# ==========================================================

class ChangePasswordRequest(BaseModel):
    """
    Change password request.
    """

    current_password: str

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )


class ForgotPasswordRequest(BaseModel):
    """
    Forgot password request.
    """

    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """
    Reset password request.
    """

    token: str

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )


# ==========================================================
# Authentication Response
# ==========================================================

class AuthResponse(BaseModel):
    """
    Authentication response.
    """

    success: bool
    message: str
    access_token: str | None = None
    token_type: str = "bearer"


# ==========================================================
# Current User
# ==========================================================

class CurrentUser(BaseModel):
    """
    Current authenticated user.
    """

    id: int
    employee_id: str
    first_name: str
    last_name: str
    email: EmailStr
    role: str

    model_config = ConfigDict(
        from_attributes=True,
    )