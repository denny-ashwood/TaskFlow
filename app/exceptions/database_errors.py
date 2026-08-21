"""
Database-related exceptions.
"""

from app.exceptions import DatabaseError


class ConnectionError(DatabaseError):
    """Raised when database connection fails."""
    pass


class MigrationError(DatabaseError):
    """Raised when database migration fails."""
    pass


class TransactionError(DatabaseError):
    """Raised when a database transaction fails."""
    pass


class IntegrityError(DatabaseError):
    """Raised when database integrity is violated."""
    pass


__all__ = [
    'ConnectionError',
    'MigrationError',
    'TransactionError',
    'IntegrityError',
]
