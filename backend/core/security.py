"""
OpsPilot AI
Security Utilities

Provides password hashing, password verification,
JWT token creation, and token decoding utilities.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from pwdlib import PasswordHash

from backend.core.config import settings

# ==========================================================
# Password Hasher
# ==========================================================

password_hash = PasswordHash.recommended()


# ==========================================================
# Password Utilities
# ==========================================================

def hash_password(password: str) -> str:
    """
    Hash a plain text password.
    """
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    """
    return password_hash.verify(password, hashed_password)


# ==========================================================
# JWT Utilities
# ==========================================================

def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create a JWT access token.
    """

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    expire = datetime.now(timezone.utc) + expires_delta

    payload: dict[str, Any] = {
        "sub": subject,
        "exp": expire,
        "type": "access",
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode a JWT access token.
    """

    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )