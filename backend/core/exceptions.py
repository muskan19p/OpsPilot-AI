"""
OpsPilot AI
Custom Exceptions

Defines custom application exceptions.
"""

from __future__ import annotations


class OpsPilotException(Exception):
    """
    Base exception class.
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class AuthenticationError(OpsPilotException):
    """Raised when authentication fails."""
    pass


class AuthorizationError(OpsPilotException):
    """Raised when authorization fails."""
    pass


class DuplicateResourceError(OpsPilotException):
    """Raised when a duplicate resource exists."""
    pass


class ResourceNotFoundError(OpsPilotException):
    """Raised when a resource cannot be found."""
    pass


class ValidationError(OpsPilotException):
    """Raised when validation fails."""
    pass