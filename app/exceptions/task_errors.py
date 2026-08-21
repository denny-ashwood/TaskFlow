"""
Task-related exceptions.
"""

from app.exceptions import (
    TaskFlowError,
    ValidationError,
    TaskNotFoundError,
)


class InvalidTaskDataError(ValidationError):
    """Raised when task data is invalid."""
    pass


class TaskAlreadyCompletedError(TaskFlowError):
    """Raised when attempting to complete an already completed task."""
    pass


class TaskAlreadyCancelledError(TaskFlowError):
    """Raised when attempting to cancel an already cancelled task."""
    pass


class InvalidDateError(ValidationError):
    """Raised when a date is invalid."""
    pass


class InvalidTimeError(ValidationError):
    """Raised when a time is invalid."""
    pass


class InvalidPriorityError(ValidationError):
    """Raised when priority is invalid."""
    pass


class InvalidStatusError(ValidationError):
    """Raised when status is invalid."""
    pass


__all__ = [
    'InvalidTaskDataError',
    'TaskAlreadyCompletedError',
    'TaskAlreadyCancelledError',
    'InvalidDateError',
    'InvalidTimeError',
    'InvalidPriorityError',
    'InvalidStatusError',
    'TaskNotFoundError', 
]