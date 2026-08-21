"""
Category service implementation.
"""

import logging
from typing import List, Optional

from app.exceptions import CategoryNotFoundError, ValidationError
from app.models.category import Category
from app.repositories.category_repository import CategoryRepository

logger = logging.getLogger(__name__)


class CategoryService:
    """Service for category management operations."""

    def __init__(self, category_repository: CategoryRepository) -> None:
        self.category_repository = category_repository

    def create_category(self, name: str, description: str = None) -> Category:
        """
        Create new category.

        Args:
            name: Category name
            description: Category description

        Returns:
            Created category
        """
        # Validate name
        name = name.strip()
        if not name:
            raise ValidationError("Category name cannot be empty")

        # Check if category already exists
        existing = self.category_repository.get_by_name(name)
        if existing:
            raise ValidationError(f"Category '{name}' already exists")

        category = self.category_repository.create(
            name=name,
            description=description,
        )
        logger.info(f"Category created: ID={category.id}, name='{category.name}'")

        return category

    def update_category(self, category_id: int, **kwargs) -> Optional[Category]:
        """Update category."""
        category = self.get_category(category_id)
        if not category:
            raise CategoryNotFoundError(f"Category with ID {category_id} not found")

        if 'name' in kwargs:
            kwargs['name'] = kwargs['name'].strip()
            if not kwargs['name']:
                raise ValidationError("Category name cannot be empty")

        updated_category = self.category_repository.update(category_id, **kwargs)
        logger.info(f"Category updated: ID={category_id}")

        return updated_category

    def delete_category(self, category_id: int) -> bool:
        """Delete category."""
        category = self.get_category(category_id)
        if not category:
            raise CategoryNotFoundError(f"Category with ID {category_id} not found")

        deleted = self.category_repository.delete(category_id)
        logger.info(f"Category deleted: ID={category_id}")

        return deleted

    def get_category(self, category_id: int) -> Optional[Category]:
        """Get category by ID."""
        return self.category_repository.get_by_id(category_id)

    def get_all_categories(self) -> List[Category]:
        """Get all categories."""
        return self.category_repository.get_all()

    def get_categories_with_count(self) -> List[dict]:
        """Get categories with task counts."""
        return self.category_repository.get_with_task_count()

    def get_default_categories(self) -> List[Category]:
        """Get or create default categories."""
        return self.category_repository.get_default_categories()