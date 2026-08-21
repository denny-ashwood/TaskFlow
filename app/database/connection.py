"""
Database connection management.
"""

import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Optional

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.config.constants import DATABASE_URL_TEMPLATE
from app.exceptions.database_errors import ConnectionError

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and sessions."""

    def __init__(self, settings) -> None:
        """
        Initialize database manager.

        Args:
            settings: Application settings instance
        """
        self.settings = settings
        self._engine: Optional[Engine] = None
        self._session_factory: Optional[sessionmaker] = None
        self._initialize_engine()

    def _initialize_engine(self) -> None:
        """Initialize SQLAlchemy engine."""
        try:
            db_path = self.settings.database_path
            db_path.parent.mkdir(parents=True, exist_ok=True)

            database_url = DATABASE_URL_TEMPLATE.format(path=db_path)

            self._engine = create_engine(
                database_url,
                echo=False,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
            )

            # Enable foreign key constraints
            @event.listens_for(self._engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

            self._session_factory = sessionmaker(
                bind=self._engine,
                expire_on_commit=False,
                autoflush=False,
            )

            logger.info(f"Database engine initialized: {db_path}")

        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise ConnectionError(f"Failed to initialize database: {e}")

    @property
    def engine(self) -> Engine:
        """Get SQLAlchemy engine."""
        if not self._engine:
            raise ConnectionError("Database engine not initialized")
        return self._engine

    @property
    def session_factory(self) -> sessionmaker:
        """Get session factory."""
        if not self._session_factory:
            raise ConnectionError("Session factory not initialized")
        return self._session_factory

    def create_session(self) -> Session:
        """Create a new database session."""
        return self._session_factory()

    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        """
        Provide a transactional scope around operations.

        Yields:
            Database session

        Raises:
            Exception: If transaction fails
        """
        session = self.create_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def initialize(self) -> None:
        """Initialize database schema."""
        from app.models.base import Base

        try:
            Base.metadata.create_all(self._engine)
            logger.info("Database schema initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database schema: {e}")
            raise ConnectionError(f"Failed to initialize database schema: {e}")

    def close(self) -> None:
        """Close database connections."""
        if self._engine:
            self._engine.dispose()
            logger.info("Database connections closed")