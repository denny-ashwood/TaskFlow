"""
Base repository pattern implementation.
"""

import logging
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.base import Base

logger = logging.getLogger(__name__)

# Generic type for models
T = TypeVar('T', bound=Base)


class BaseRepository(Generic[T]):
    """Base repository with common CRUD operations."""

    def __init__(self, model_class: Type[T], session_factory) -> None:
        """
        Initialize repository.

        Args:
            model_class: SQLAlchemy model class
            session_factory: Session factory for creating database sessions
        """
        self.model_class = model_class
        self.session_factory = session_factory

    def get_by_id(self, id: int) -> Optional[T]:
        """Get entity by ID."""
        with self.session_factory() as session:
            return session.get(self.model_class, id)

    def get_all(self) -> List[T]:
        """Get all entities."""
        with self.session_factory() as session:
            stmt = select(self.model_class).order_by(self.model_class.created_at.desc())
            result = session.execute(stmt)
            return list(result.scalars().all())

    def create(self, **kwargs: Any) -> T:
        """
        Create new entity.

        Args:
            **kwargs: Entity attributes

        Returns:
            Created entity
        """
        with self.session_factory() as session:
            entity = self.model_class(**kwargs)
            session.add(entity)
            session.commit()
            session.refresh(entity)
            logger.debug(f"Created {self.model_class.__name__} with ID {entity.id}")
            return entity

    def update(self, id: int, **kwargs: Any) -> Optional[T]:
        """
        Update entity.

        Args:
            id: Entity ID
            **kwargs: Attributes to update

        Returns:
            Updated entity or None if not found
        """
        with self.session_factory() as session:
            entity = session.get(self.model_class, id)
            if not entity:
                logger.warning(f"{self.model_class.__name__} with ID {id} not found")
                return None

            for key, value in kwargs.items():
                if hasattr(entity, key):
                    setattr(entity, key, value)

            session.commit()
            session.refresh(entity)
            logger.debug(f"Updated {self.model_class.__name__} with ID {id}")
            return entity

    def delete(self, id: int) -> bool:
        """
        Delete entity.

        Args:
            id: Entity ID

        Returns:
            True if deleted, False if not found
        """
        with self.session_factory() as session:
            entity = session.get(self.model_class, id)
            if not entity:
                logger.warning(f"{self.model_class.__name__} with ID {id} not found")
                return False

            session.delete(entity)
            session.commit()
            logger.debug(f"Deleted {self.model_class.__name__} with ID {id}")
            return True

    def count(self) -> int:
        """Count total entities."""
        with self.session_factory() as session:
            from sqlalchemy import func
            stmt = select(func.count()).select_from(self.model_class)
            result = session.execute(stmt)
            return result.scalar() or 0

    def exists(self, id: int) -> bool:
        """Check if entity exists."""
        return self.get_by_id(id) is not None