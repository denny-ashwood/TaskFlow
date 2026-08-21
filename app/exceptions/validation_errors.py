"""
Validation-related exceptions.
"""

from app.exceptions import ValidationError


class EmptyTitleError(ValidationError):
    """Raised when task title is empty."""
    pass


class TitleTooLongError(ValidationError):
    """Raised when task title exceeds maximum length."""
    pass


class InvalidReminderError(ValidationError):
    """Raised when reminder time is invalid."""
    pass


class InvalidCategoryError(ValidationError):
    """Raised when category is invalid."""
    pass


__all__ = [
    'EmptyTitleError',
    'TitleTooLongError',
    'InvalidReminderError',
    'InvalidCategoryError',
]
