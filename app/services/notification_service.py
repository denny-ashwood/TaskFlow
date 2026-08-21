"""
Notification service implementation.
"""

import logging
from typing import Optional

from app.models.task import Task

logger = logging.getLogger(__name__)


class NotificationService:
    """Service for desktop notifications."""

    def __init__(self) -> None:
        self._notifier = None
        self._initialize_notifier()

    def _initialize_notifier(self) -> None:
        """Initialize notification backend."""
        try:
            from notifypy import Notify
            self._notifier = Notify()
            self._notifier.application_name = "TaskFlow"
            logger.info("Notification service initialized")
        except ImportError:
            logger.warning("notify-py not installed, notifications disabled")
            self._notifier = None

    def notify_task(self, task: Task, is_reminder: bool = True) -> bool:
        """
        Send notification for task.

        Args:
            task: Task to notify about
            is_reminder: If True, this is a reminder notification

        Returns:
            True if notification sent successfully
        """
        if not self._notifier:
            return False

        try:
            title = "Reminder" if is_reminder else "Upcoming Task"
            message = task.title

            if task.due_time:
                time_str = task.due_time.strftime("%I:%M %p")
                message += f"\nDue at {time_str}"

            if task.description:
                message += f"\n{task.description[:100]}"

            self._notifier.title = f"TaskFlow - {title}"
            self._notifier.message = message
            self._notifier.send()

            logger.info(f"Notification sent for task {task.id}: {task.title}")
            return True

        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return False

    def notify_missed_task(self, task: Task, missed_by: str) -> bool:
        """
        Send notification for missed task.

        Args:
            task: Missed task
            missed_by: Human-readable time difference

        Returns:
            True if notification sent successfully
        """
        if not self._notifier:
            return False

        try:
            self._notifier.title = "TaskFlow - Missed Reminder"
            self._notifier.message = (
                f"{task.title}\n"
                f"Reminder was due {missed_by} ago"
            )
            self._notifier.send()

            logger.info(f"Missed reminder notification sent for task {task.id}")
            return True

        except Exception as e:
            logger.error(f"Failed to send missed notification: {e}")
            return False

    def test_notification(self) -> bool:
        """
        Send test notification.

        Returns:
            True if notification sent successfully
        """
        if not self._notifier:
            return False

        try:
            self._notifier.title = "TaskFlow"
            self._notifier.message = "Test notification"
            self._notifier.send()
            logger.info("Test notification sent")
            return True

        except Exception as e:
            logger.error(f"Failed to send test notification: {e}")
            return False