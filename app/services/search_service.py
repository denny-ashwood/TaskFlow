"""
Search service implementation.
"""

import logging
from typing import Dict, List, Optional

from app.models.task import Task
from app.repositories.task_repository import TaskRepository

logger = logging.getLogger(__name__)


class SearchService:
    """Service for search and filtering."""

    def __init__(self, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    def search(
        self,
        query: str = "",
        status: Optional[str] = None,
        priority: Optional[str] = None,
        category_id: Optional[int] = None,
        start_date=None,
        end_date=None,
        sort_by: str = "due_date",
        sort_order: str = "asc",
    ) -> List[Task]:
        """
        Search tasks with filters and sorting.

        Args:
            query: Search query string
            status: Filter by status
            priority: Filter by priority
            category_id: Filter by category
            start_date: Filter by start date
            end_date: Filter by end date
            sort_by: Sort field
            sort_order: Sort order ('asc' or 'desc')

        Returns:
            List of matching tasks
        """
        filters = {}

        if status:
            filters['status'] = status
        if priority:
            filters['priority'] = priority
        if category_id:
            filters['category_id'] = category_id
        if start_date:
            filters['start_date'] = start_date
        if end_date:
            filters['end_date'] = end_date

        tasks = self.task_repository.search(query, filters)

        # Apply sorting
        tasks = self.sort_tasks(tasks, sort_by, sort_order)

        return tasks

    def sort_tasks(
        self,
        tasks: List[Task],
        sort_by: str = "due_date",
        sort_order: str = "asc",
    ) -> List[Task]:
        """
        Sort tasks by field.

        Args:
            tasks: List of tasks
            sort_by: Sort field
            sort_order: Sort order

        Returns:
            Sorted task list
        """
        reverse = sort_order.lower() == "desc"

        sort_keys = {
            'due_date': lambda t: (t.due_date or date.max, t.due_time or time.max),
            'priority': lambda t: {'low': 0, 'medium': 1, 'high': 2}.get(t.priority, 0),
            'created_at': lambda t: t.created_at,
            'updated_at': lambda t: t.updated_at,
            'title': lambda t: t.title.lower(),
        }

        key_func = sort_keys.get(sort_by, sort_keys['due_date'])
        return sorted(tasks, key=key_func, reverse=reverse)