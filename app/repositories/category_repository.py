"""
Category repository implementation.
"""

import logging
from typing import List, Optional

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from app.models.category import Category
from app.models.task import Task
from app.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class CategoryRepository(BaseRepository[Category]):
    """Repository for Category entities."""

    def __init__(self, session_factory) -> None:
        super().__init__(Category, session_factory)

    def get_by_name(self, name: str) -> Optional[Category]:
        """Get category by name."""
        with self.session_factory() as session:
            stmt = select(Category).where(Category.name == name)
            result = session.execute(stmt)
            return result.scalar_one_or_none()

    def get_with_task_count(self) -> List[dict]:
        """Get categories with task counts."""
        with self.session_factory() as session:
            stmt = (
                select(
                    Category,
                    func.count(Task.id).label('task_count')
                )
                .outerjoin(Task, Task.category_id == Category.id)
                .group_by(Category.id)
                .order_by(Category.name)
            )
            result = session.execute(stmt)

            categories = []
            for category, task_count in result:
                categories.append({
                    'id': category.id,
                    'name': category.name,
                    'description': category.description,
                    'task_count': task_count,
                    'created_at': category.created_at,
                })

            return categories

    def get_default_categories(self) -> List[Category]:
        """Get default categories."""
        default_names = ['Work', 'Personal', 'Study', 'Finance', 'Health', 'Other']

        with self.session_factory() as session:
            stmt = select(Category).where(Category.name.in_(default_names))
            result = session.execute(stmt)
            categories = list(result.scalars().all())

            # Create missing default categories
            existing_names = {c.name for c in categories}
            for name in default_names:
                if name not in existing_names:
                    category = Category(name=name)
                    session.add(category)
                    categories.append(category)

            session.commit()
            return categories