"""
Integration tests for scheduler.
"""

import pytest
import time
from datetime import datetime, timedelta

from app.models.reminder import Reminder


class TestSchedulerIntegration:
    """Test scheduler operations."""

    def test_schedule_reminder(self, scheduler_service, reminder_service, task_service):
        """Test scheduling a reminder."""
        # Create task
        task = task_service.create_task({
            'title': 'Scheduled Task',
            'reminder_minutes': 5,
        })

        # Create reminder
        reminder_time = datetime.now() + timedelta(minutes=5)
        reminder = reminder_service.create_reminder(task.id, reminder_time)

        # Schedule reminder
        success = scheduler_service.schedule_reminder(reminder)
        assert success is True

    def test_cancel_reminder(self, scheduler_service, reminder_service, task_service):
        """Test cancelling a reminder."""
        # Create task and reminder
        task = task_service.create_task({'title': 'Cancel Test'})
        reminder = reminder_service.create_reminder(
            task.id,
            datetime.now() + timedelta(hours=1),
        )

        # Schedule and cancel
        scheduler_service.schedule_reminder(reminder)
        cancelled = scheduler_service.cancel_reminder(reminder.id)

        assert cancelled is True

    def test_rebuild_schedule(self, scheduler_service, reminder_service, task_service):
        """Test rebuilding schedule."""
        # Create multiple tasks and reminders
        task1 = task_service.create_task({'title': 'Task 1'})
        task2 = task_service.create_task({'title': 'Task 2'})

        reminder1 = reminder_service.create_reminder(
            task1.id,
            datetime.now() + timedelta(hours=1),
        )
        reminder2 = reminder_service.create_reminder(
            task2.id,
            datetime.now() + timedelta(hours=2),
        )

        # Rebuild schedule
        scheduler_service.rebuild_schedule()

        # Check if jobs were scheduled
        assert scheduler_service._scheduler.get_job(
            f"reminder_{reminder1.id}") is not None
        assert scheduler_service._scheduler.get_job(
            f"reminder_{reminder2.id}") is not None
