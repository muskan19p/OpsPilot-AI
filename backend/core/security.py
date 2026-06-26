"""
OpsPilot AI
Security Utilities

Handles:
- Password Hashing
- Password Verification
- JWT Token Creation
- JWT Token Validation
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.core.config import settings

# ==========================================================
# Password Hashing
# ==========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# ==========================================================
# Password Functions
# ==========================================================


def hash_password(password: str) -> str:
    """
    Hash a plain password.
    """
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify password against its hash.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


# ==========================================================
# JWT Token
# ==========================================================


def create_access_token(
    subject: str,
    expires_delta: Optional[timedelta] = None,
    extra_data: Optional[dict[str, Any]] = None,
) -> str:
    """
    Create JWT access token.
    """

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    payload = {
        "sub": subject,
        "exp": expire,
    }

    if extra_data:
        payload.update(extra_data)

    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return encoded_jwt


# ==========================================================
# Decode JWT
# ==========================================================


def decode_access_token(token: str) -> dict:
    """
    Decode JWT token.

    Raises:
        JWTError
    """

    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )


# ==========================================================
# Validate JWT
# ==========================================================


def verify_token(token: str) -> Optional[dict]:
    """
    Verify JWT token.

    Returns payload if valid.
    Returns None if invalid.
    """

    try:
        payload = decode_access_token(token)
        return payload

    except JWTError:
        return None