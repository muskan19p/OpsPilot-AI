"""
OpsPilot AI
Authentication & Authorization

Provides:
- Current authenticated user
- Active user validation
- Role-Based Access Control (RBAC)
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.security import verify_token

# These imports will work after we create the files.
from backend.models.user import User
from backend.services.auth_service import AuthService

# ==========================================================
# OAuth2
# ==========================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)


# ==========================================================
# Current User
# ==========================================================

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Return authenticated user.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = verify_token(token)

    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")

    if user_id is None:
        raise credentials_exception

    user = AuthService.get_user_by_id(
        db=db,
        user_id=int(user_id),
    )

    if user is None:
        raise credentials_exception

    return user


# ==========================================================
# Active User
# ==========================================================

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Ensure account is active.
    """

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive account.",
        )

    return current_user


# ==========================================================
# Employee
# ==========================================================

def require_employee(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Employee or above.
    """

    allowed = {
        "employee",
        "manager",
        "admin",
    }

    if current_user.role.name.lower() not in allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Employee access required.",
        )

    return current_user


# ==========================================================
# Manager
# ==========================================================

def require_manager(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Manager or Admin.
    """

    allowed = {
        "manager",
        "admin",
    }

    if current_user.role.name.lower() not in allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager access required.",
        )

    return current_user


# ==========================================================
# Admin
# ==========================================================

def require_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Admin only.
    """

    if current_user.role.name.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required.",
        )

    return current_user