"""
Task service implementation.
"""

import logging
from datetime import date, datetime, time, timedelta
from typing import Dict, List, Optional

from app.config.constants import (
    PRIORITIES,
    STATUS_CANCELLED,
    STATUS_COMPLETED,
    STATUS_PENDING,
)
from app.exceptions.task_errors import (
    InvalidPriorityError,
    InvalidStatusError,
    TaskAlreadyCompletedError,
    TaskNotFoundError,
)
from app.exceptions.validation_errors import EmptyTitleError, TitleTooLongError
from app.models.task import Task
from app.repositories.reminder_repository import ReminderRepository
from app.repositories.task_repository import TaskRepository

logger = logging.getLogger(__name__)


class TaskService:
    """Service for task management operations."""

    def __init__(
        self,
        task_repository: TaskRepository,
        reminder_repository: Optional[ReminderRepository] = None,
    ) -> None:
        """
        Initialize task service.

        Args:
            task_repository: Task repository instance
            reminder_repository: Reminder repository instance (optional)
        """
        self.task_repository = task_repository
        self.reminder_repository = reminder_repository

    def create_task(self, data: Dict) -> Task:
        """
        Create new task.

        Args:
            data: Task data dictionary

        Returns:
            Created task

        Raises:
            EmptyTitleError: If title is empty
            TitleTooLongError: If title exceeds 255 characters
            InvalidPriorityError: If priority is invalid
        """
        # Validate data
        validated_data = self.validate_task_data(data)

        # Create task
        task = self.task_repository.create(**validated_data)
        logger.info(f"Task created: ID={task.id}, title='{task.title}'")

        return task

    def update_task(self, task_id: int, data: Dict) -> Optional[Task]:
        """
        Update task.

        Args:
            task_id: Task ID
            data: Updated task data

        Returns:
            Updated task or None if not found
        """
        # Check if task exists
        task = self.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        # Validate data
        validated_data = self.validate_task_data(data, partial=True)

        # Update task
        updated_task = self.task_repository.update(task_id, **validated_data)
        logger.info(f"Task updated: ID={task_id}")

        return updated_task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete task.

        Args:
            task_id: Task ID

        Returns:
            True if deleted, False if not found
        """
        # Check if task exists
        task = self.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        # Delete task
        deleted = self.task_repository.delete(task_id)
        logger.info(f"Task deleted: ID={task_id}")

        return deleted

    def complete_task(self, task_id: int) -> Optional[Task]:
        """
        Mark task as completed.

        Args:
            task_id: Task ID

        Returns:
            Updated task

        Raises:
            TaskNotFoundError: If task not found
            TaskAlreadyCompletedError: If task already completed
        """
        task = self.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        if task.status == STATUS_COMPLETED:
            raise TaskAlreadyCompletedError(f"Task {task_id} is already completed")

        task.complete()
        updated_task = self.task_repository.update(
            task_id,
            status=task.status,
            completed_at=task.completed_at,
        )

        logger.info(f"Task completed: ID={task_id}")
        return updated_task

    def restore_task(self, task_id: int) -> Optional[Task]:
        """
        Restore completed task.

        Args:
            task_id: Task ID

        Returns:
            Updated task
        """
        task = self.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        if task.status != STATUS_COMPLETED:
            logger.warning(f"Task {task_id} is not completed, cannot restore")
            return task

        task.restore()
        updated_task = self.task_repository.update(
            task_id,
            status=task.status,
            completed_at=None,
        )

        logger.info(f"Task restored: ID={task_id}")
        return updated_task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        return self.task_repository.get_by_id(task_id)

    def get_today_tasks(self) -> List[Task]:
        """Get tasks due today."""
        return self.task_repository.get_today_tasks()

    def get_upcoming_tasks(self, days: int = 30) -> List[Task]:
        """Get upcoming tasks."""
        return self.task_repository.get_upcoming_tasks(days)

    def get_overdue_tasks(self) -> List[Task]:
        """Get overdue tasks."""
        return self.task_repository.get_overdue_tasks()

    def get_completed_tasks(self, limit: int = 100) -> List[Task]:
        """Get completed tasks."""
        return self.task_repository.get_completed_tasks(limit)

    def get_statistics(self) -> Dict[str, int]:
        """Get task statistics."""
        return self.task_repository.get_statistics()

    def search_tasks(self, query: str, filters: Optional[Dict] = None) -> List[Task]:
        """Search tasks with filters."""
        return self.task_repository.search(query, filters)

    def validate_task_data(self, data: Dict, partial: bool = False) -> Dict:
        """
        Validate task data.

        Args:
            data: Task data dictionary
            partial: If True, only validate provided fields

        Returns:
            Validated data dictionary

        Raises:
            EmptyTitleError: If title is empty
            TitleTooLongError: If title exceeds 255 characters
            InvalidPriorityError: If priority is invalid
            InvalidStatusError: If status is invalid
        """
        validated = {}

        # Validate title
        if 'title' in data or not partial:
            title = data.get('title', '').strip()
            if not title:
                raise EmptyTitleError("Task title cannot be empty")
            if len(title) > 255:
                raise TitleTooLongError("Task title cannot exceed 255 characters")
            validated['title'] = title

        # Validate description
        if 'description' in data:
            validated['description'] = data['description']

        # Validate due_date
        if 'due_date' in data:
            due_date = data['due_date']
            if due_date is not None and not isinstance(due_date, date):
                if isinstance(due_date, str):
                    try:
                        due_date = date.fromisoformat(due_date)
                    except ValueError:
                        raise ValueError(f"Invalid date format: {due_date}")
                else:
                    raise ValueError(f"Invalid date type: {type(due_date)}")
            validated['due_date'] = due_date

        # Validate due_time
        if 'due_time' in data:
            due_time = data['due_time']
            if due_time is not None and not isinstance(due_time, time):
                if isinstance(due_time, str):
                    try:
                        due_time = time.fromisoformat(due_time)
                    except ValueError:
                        raise ValueError(f"Invalid time format: {due_time}")
                else:
                    raise ValueError(f"Invalid time type: {type(due_time)}")
            validated['due_time'] = due_time

        # Validate priority
        if 'priority' in data or not partial:
            priority = data.get('priority', 'medium')
            if priority not in PRIORITIES:
                raise InvalidPriorityError(
                    f"Invalid priority: {priority}. Valid values: {PRIORITIES}"
                )
            validated['priority'] = priority

        # Validate status
        if 'status' in data:
            status = data['status']
            if status not in [STATUS_PENDING, STATUS_COMPLETED, STATUS_CANCELLED]:
                raise InvalidStatusError(f"Invalid status: {status}")
            validated['status'] = status

        # Validate category_id
        if 'category_id' in data:
            validated['category_id'] = data['category_id']

        # Validate reminder_minutes
        if 'reminder_minutes' in data:
            reminder_minutes = data['reminder_minutes']
            if reminder_minutes is not None and reminder_minutes < 0:
                raise ValueError("Reminder minutes cannot be negative")
            validated['reminder_minutes'] = reminder_minutes

        return validated