"""
Calendar service implementation.
"""

import logging
from datetime import date, timedelta
from typing import Dict, List

from app.models.task import Task
from app.repositories.task_repository import TaskRepository

logger = logging.getLogger(__name__)


class CalendarService:
    """Service for calendar operations."""

    def __init__(self, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    def get_month_tasks(self, year: int, month: int) -> Dict[date, List[Task]]:
        """
        Get tasks grouped by date for a month.

        Args:
            year: Year
            month: Month (1-12)

        Returns:
            Dictionary mapping dates to task lists
        """
        tasks = self.task_repository.get_by_month(year, month)

        # Group tasks by date
        tasks_by_date: Dict[date, List[Task]] = {}
        for task in tasks:
            if task.due_date:
                if task.due_date not in tasks_by_date:
                    tasks_by_date[task.due_date] = []
                tasks_by_date[task.due_date].append(task)

        return tasks_by_date

    def get_week_tasks(self, start_date: date) -> Dict[date, List[Task]]:
        """
        Get tasks grouped by date for a week.

        Args:
            start_date: Week start date

        Returns:
            Dictionary mapping dates to task lists
        """
        end_date = start_date + timedelta(days=6)
        tasks = self.task_repository.get_by_date_range(start_date, end_date)

        # Group tasks by date
        tasks_by_date: Dict[date, List[Task]] = {}
        for task in tasks:
            if task.due_date:
                if task.due_date not in tasks_by_date:
                    tasks_by_date[task.due_date] = []
                tasks_by_date[task.due_date].append(task)

        return tasks_by_date

    def get_day_tasks(self, target_date: date) -> List[Task]:
        """
        Get tasks for a specific day.

        Args:
            target_date: Target date

        Returns:
            List of tasks for the day
        """
        tasks = self.task_repository.get_by_date_range(
            target_date, target_date)
        return sorted(tasks, key=lambda t: (t.due_time or timedelta.max))
