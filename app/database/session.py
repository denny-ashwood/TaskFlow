"""
Database session utilities.
"""

import logging
from contextlib import contextmanager
from typing import Generator, Optional

from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

# Global session factory (set during application initialization)
_session_factory = None


def set_session_factory(factory) -> None:
    """Set global session factory."""
    global _session_factory
    _session_factory = factory


def get_session_factory():
    """Get global session factory."""
    return _session_factory


@contextmanager
def db_session() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.

    Yields:
        Database session

    Raises:
        RuntimeError: If session factory not initialized
    """
    if not _session_factory:
        raise RuntimeError("Session factory not initialized")

    session = _session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()