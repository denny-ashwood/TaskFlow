"""
Scheduler service implementation.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

from app.models.reminder import Reminder
from app.services.notification_service import NotificationService
from app.services.reminder_service import ReminderService
from app.services.task_service import TaskService

logger = logging.getLogger(__name__)


class SchedulerService:
    """Service for background scheduling."""

    def __init__(
        self,
        task_service: TaskService,
        reminder_service: ReminderService,
        notification_service: NotificationService,
        settings_service=None,
    ) -> None:
        """
        Initialize scheduler service.

        Args:
            task_service: Task service instance
            reminder_service: Reminder service instance
            notification_service: Notification service instance
            settings_service: Settings service instance (optional)
        """
        self.task_service = task_service
        self.reminder_service = reminder_service
        self.notification_service = notification_service
        self.settings_service = settings_service

        self._scheduler: Optional[BackgroundScheduler] = None

    def start(self) -> None:
        """Start scheduler."""
        if self._scheduler:
            logger.warning("Scheduler already running")
            return

        self._scheduler = BackgroundScheduler()
        self._scheduler.start()

        # Rebuild schedule from database
        self.rebuild_schedule()

        logger.info("Scheduler started")

    def stop(self) -> None:
        """Stop scheduler."""
        if self._scheduler:
            self._scheduler.shutdown(wait=False)
            self._scheduler = None
            logger.info("Scheduler stopped")

    def schedule_reminder(self, reminder: Reminder) -> bool:
        """
        Schedule reminder notification.

        Args:
            reminder: Reminder entity

        Returns:
            True if scheduled successfully
        """
        if not self._scheduler:
            logger.error("Scheduler not running")
            return False

        try:
            job_id = f"reminder_{reminder.id}"

            # Remove existing job if any
            if self._scheduler.get_job(job_id):
                self._scheduler.remove_job(job_id)

            # Schedule new job
            self._scheduler.add_job(
                self._execute_reminder,
                trigger=DateTrigger(run_date=reminder.reminder_time),
                args=[reminder.id],
                id=job_id,
                replace_existing=True,
            )

            logger.debug(
                f"Reminder {reminder.id} scheduled for {reminder.reminder_time}")
            return True

        except Exception as e:
            logger.error(f"Failed to schedule reminder {reminder.id}: {e}")
            return False

    def cancel_reminder(self, reminder_id: int) -> bool:
        """
        Cancel scheduled reminder.

        Args:
            reminder_id: Reminder ID

        Returns:
            True if cancelled successfully
        """
        if not self._scheduler:
            return False

        try:
            job_id = f"reminder_{reminder_id}"
            if self._scheduler.get_job(job_id):
                self._scheduler.remove_job(job_id)
                logger.debug(f"Reminder {reminder_id} cancelled")
                return True
            return False

        except Exception as e:
            logger.error(f"Failed to cancel reminder {reminder_id}: {e}")
            return False

    def rebuild_schedule(self) -> None:
        """Rebuild schedule from pending reminders."""
        if not self._scheduler:
            logger.error("Scheduler not running")
            return

        try:
            # Get pending reminders
            pending_reminders = self.reminder_service.get_pending_reminders()

            # Schedule each reminder
            for reminder in pending_reminders:
                if reminder.reminder_time > datetime.now():
                    self.schedule_reminder(reminder)

            logger.info(
                f"Rebuilt schedule with {len(pending_reminders)} reminders")

        except Exception as e:
            logger.error(f"Failed to rebuild schedule: {e}")

    def _execute_reminder(self, reminder_id: int) -> None:
        """
        Execute reminder notification.

        Args:
            reminder_id: Reminder ID
        """
        logger.debug(f"Executing reminder {reminder_id}")

        try:
            reminder = self.reminder_service.get_reminder(reminder_id)
            if not reminder:
                logger.warning(f"Reminder {reminder_id} not found")
                return

            # Check if already sent
            if reminder.notification_sent:
                logger.debug(f"Reminder {reminder_id} already sent")
                return

            # Get task
            task = self.task_service.get_task(reminder.task_id)
            if not task:
                logger.warning(
                    f"Task {reminder.task_id} not found for reminder")
                return

            # Check task status
            if task.status != "pending":
                logger.debug(
                    f"Task {task.id} is {task.status}, skipping reminder")
                return

            # Send notification
            self.notification_service.notify_task(task, is_reminder=True)

            # Mark as sent
            self.reminder_service.mark_as_sent(reminder_id)

        except Exception as e:
            logger.error(f"Failed to execute reminder {reminder_id}: {e}")

    def check_missed_reminders(self) -> None:
        """Check for missed reminders."""
        logger.debug("Checking for missed reminders")

        try:
            # Get missed reminders (due but not sent)
            pending_reminders = self.reminder_service.get_pending_reminders()

            for reminder in pending_reminders:
                # Calculate time difference
                time_diff = datetime.now() - reminder.reminder_time

                # Check if within missed window
                missed_window = 15  # minutes
                if self.settings_service:
                    missed_window = self.settings_service.get(
                        'missed_reminder_window', 15
                    )

                if time_diff <= timedelta(minutes=missed_window):
                    # Show missed notification
                    task = self.task_service.get_task(reminder.task_id)
                    if task and task.status == "pending":
                        self.notification_service.notify_missed_task(
                            task,
                            missed_by=f"{int(time_diff.total_seconds() // 60)} minutes"
                        )

                    # Mark as sent
                    self.reminder_service.mark_as_sent(reminder.id)
                else:
                    # Too old, mark as sent without notification
                    self.reminder_service.mark_as_sent(reminder.id)
                    logger.debug(
                        f"Reminder {reminder.id} too old, marked as sent without notification"
                    )

        except Exception as e:
            logger.error(f"Failed to check missed reminders: {e}")
