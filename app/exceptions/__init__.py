"""
Application-specific exceptions.
"""


class TaskFlowError(Exception):
    """Base exception for all TaskFlow errors."""
    pass


class ValidationError(TaskFlowError):
    """Raised when data validation fails."""
    pass


class TaskNotFoundError(TaskFlowError):
    """Raised when a task is not found."""
    pass


class CategoryNotFoundError(TaskFlowError):
    """Raised when a category is not found."""
    pass


class ReminderNotFoundError(TaskFlowError):
    """Raised when a reminder is not found."""
    pass


class DatabaseError(TaskFlowError):
    """Raised when a database operation fails."""
    pass


class SchedulerError(TaskFlowError):
    """Raised when scheduler operations fail."""
    pass


class NotificationError(TaskFlowError):
    """Raised when notification operations fail."""
    pass


__all__ = [
    'TaskFlowError',
    'ValidationError',
    'TaskNotFoundError',
    'CategoryNotFoundError',
    'ReminderNotFoundError',
    'DatabaseError',
    'SchedulerError',
    'NotificationError',
]