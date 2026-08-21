"""
Reminder service implementation.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional

from app.exceptions import ReminderNotFoundError, TaskNotFoundError
from app.models.reminder import Reminder
from app.models.task import Task
from app.repositories.reminder_repository import ReminderRepository
from app.repositories.task_repository import TaskRepository

logger = logging.getLogger(__name__)


class ReminderService:
    """Service for reminder management operations."""

    def __init__(
        self,
        reminder_repository: ReminderRepository,
        task_repository: TaskRepository,
    ) -> None:
        self.reminder_repository = reminder_repository
        self.task_repository = task_repository

    def create_reminder(self, task_id: int, reminder_time: datetime) -> Reminder:
        """
        Create reminder for task.

        Args:
            task_id: Task ID
            reminder_time: Reminder datetime

        Returns:
            Created reminder
        """
        # Check if task exists
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        reminder = self.reminder_repository.create(
            task_id=task_id,
            reminder_time=reminder_time,
        )
        logger.info(
            f"Reminder created: ID={reminder.id}, task={task_id}, time={reminder_time}")

        return reminder

    def create_reminder_from_minutes(self, task_id: int, minutes: int) -> Reminder:
        """
        Create reminder based on minutes before due time.

        Args:
            task_id: Task ID
            minutes: Minutes before due time

        Returns:
            Created reminder
        """
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")

        if not task.due_datetime:
            raise ValueError("Task has no due date/time")

        reminder_time = task.due_datetime - timedelta(minutes=minutes)
        return self.create_reminder(task_id, reminder_time)

    def cancel_reminders(self, task_id: int) -> int:
        """
        Cancel all reminders for task.

        Args:
            task_id: Task ID

        Returns:
            Number of cancelled reminders
        """
        count = self.reminder_repository.delete_by_task(task_id)
        logger.info(f"Cancelled {count} reminders for task {task_id}")
        return count

    def get_reminder(self, reminder_id: int) -> Optional[Reminder]:
        """Get reminder by ID."""
        return self.reminder_repository.get_by_id(reminder_id)

    def get_task_reminders(self, task_id: int) -> List[Reminder]:
        """Get all reminders for task."""
        return self.reminder_repository.get_by_task(task_id)

    def get_pending_reminders(self) -> List[Reminder]:
        """Get pending reminders."""
        return self.reminder_repository.get_pending_reminders()

    def get_upcoming_reminders(self, minutes: int = 60) -> List[Reminder]:
        """Get upcoming reminders."""
        return self.reminder_repository.get_upcoming_reminders(minutes)

    def mark_as_sent(self, reminder_id: int) -> bool:
        """Mark reminder as sent."""
        reminder = self.get_reminder(reminder_id)
        if not reminder:
            raise ReminderNotFoundError(
                f"Reminder with ID {reminder_id} not found")

        success = self.reminder_repository.mark_as_sent(reminder_id)
        logger.debug(f"Reminder {reminder_id} marked as sent")

        return success
