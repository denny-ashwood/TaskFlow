"""
Reminder repository implementation.
"""

import logging
from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.orm import joinedload

from app.models.reminder import Reminder
from app.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class ReminderRepository(BaseRepository[Reminder]):
    """Repository for Reminder entities."""

    def __init__(self, session_factory) -> None:
        super().__init__(Reminder, session_factory)

    def get_pending_reminders(self) -> List[Reminder]:
        """Get all pending reminders."""
        now = datetime.now()

        with self.session_factory() as session:
            stmt = (
                select(Reminder)
                .options(joinedload(Reminder.task))
                .where(
                    and_(
                        Reminder.notification_sent == False,
                        Reminder.reminder_time <= now,
                    )
                )
                .order_by(Reminder.reminder_time)
            )
            result = session.execute(stmt)
            return list(result.scalars().all())

    def get_upcoming_reminders(self, minutes: int = 60) -> List[Reminder]:
        """
        Get upcoming reminders within time window.

        Args:
            minutes: Time window in minutes

        Returns:
            List of upcoming reminders
        """
        now = datetime.now()
        end_time = datetime.fromtimestamp(now.timestamp() + minutes * 60)

        with self.session_factory() as session:
            stmt = (
                select(Reminder)
                .options(joinedload(Reminder.task))
                .where(
                    and_(
                        Reminder.notification_sent == False,
                        Reminder.reminder_time > now,
                        Reminder.reminder_time <= end_time,
                    )
                )
                .order_by(Reminder.reminder_time)
            )
            result = session.execute(stmt)
            return list(result.scalars().all())

    def get_by_task(self, task_id: int) -> List[Reminder]:
        """Get all reminders for a task."""
        with self.session_factory() as session:
            stmt = (
                select(Reminder)
                .where(Reminder.task_id == task_id)
                .order_by(Reminder.reminder_time)
            )
            result = session.execute(stmt)
            return list(result.scalars().all())

    def mark_as_sent(self, reminder_id: int) -> bool:
        """Mark reminder as sent."""
        return self.update(reminder_id, notification_sent=True) is not None

    def delete_by_task(self, task_id: int) -> int:
        """
        Delete all reminders for a task.

        Args:
            task_id: Task ID

        Returns:
            Number of deleted reminders
        """
        with self.session_factory() as session:
            reminders = session.execute(
                select(Reminder).where(Reminder.task_id == task_id)
            ).scalars().all()

            count = len(reminders)
            for reminder in reminders:
                session.delete(reminder)

            session.commit()
            logger.debug(f"Deleted {count} reminders for task {task_id}")
            return count