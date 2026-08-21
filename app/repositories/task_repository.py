"""
Task repository implementation.
"""

import logging
from datetime import date, datetime, time, timedelta
from typing import Dict, List, Optional

from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import joinedload

from app.config.constants import (
    STATUS_COMPLETED,
    STATUS_CANCELLED,
    STATUS_PENDING,
)
from app.models.category import Category
from app.models.task import Task
from app.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class TaskRepository(BaseRepository[Task]):
    """Repository for Task entities."""

    def __init__(self, session_factory) -> None:
        super().__init__(Task, session_factory)

    def get_today_tasks(self) -> List[Task]:
        """Get tasks due today."""
        today = date.today()
        with self.session_factory() as session:
            stmt = (
                select(Task)
                .options(joinedload(Task.category))
                .where(
                    and_(
                        Task.due_date == today,
                        Task.status == STATUS_PENDING,
                    )
                )
                .order_by(Task.due_time)
            )
            result = session.execute(stmt)
            return list(result.scalars().all())

    def get_upcoming_tasks(self, days: int = 30) -> List[Task]:
        """
        Get upcoming tasks.

        Args:
            days: Number of days to look ahead

        Returns:
            List of upcoming tasks
        """
        today = date.today()
        end_date = today + timedelta(days=days)

        with self.session_factory() as session:
            stmt = (
                select(Task)
                .options(joinedload(Task.category))
                .where(
                    and_(
                        Task.due_date > today,
                        Task.due_date <= end_date,
                        Task.status == STATUS_PENDING,
                    )
                )
                .order_by(Task.due_date, Task.due_time)
            )
            result = session.execute(stmt)
            return list(result.scalars().all())

    def get_overdue_tasks(self) -> List[Task]:
        """Get overdue tasks."""
        now = datetime.now()
        today = now.date()
        current_time = now.time()

        with self.session_factory() as session:
            stmt = (
                select(Task)
                .options(joinedload(Task.category))
                .where(
                    and_(
                        Task.status == STATUS_PENDING,
                        or_(
                            Task.due_date < today,
                            and_(
                                Task.due_date == today,
                                Task.due_time < current_time,
                            )
                        )
                    )
                )
                .order_by(Task.due_date, Task.due_time)
            )
            result = session.execute(stmt)
            return list(result.scalars().all())

    def get_completed_tasks(self, limit: int = 100) -> List[Task]:
        """
        Get completed tasks.

        Args:
            limit: Maximum number of tasks to return

        Returns:
            List of completed tasks
        """
        with self.session_factory() as session:
            stmt = (
                select(Task)
                .options(joinedload(Task.category))
                .where(Task.status == STATUS_COMPLETED)
                .order_by(Task.completed_at.desc())
                .limit(limit)
            )
            result = session.execute(stmt)
            return list(result.scalars().all())

    def get_by_category(self, category_id: int) -> List[Task]:
        """Get tasks by category."""
        with self.session_factory() as session:
            stmt = (
                select(Task)
                .options(joinedload(Task.category))
                .where(
                    and_(
                        Task.category_id == category_id,
                        Task.status != STATUS_CANCELLED,
                    )
                )
                .order_by(Task.due_date, Task.due_time)
            )
            result = session.execute(stmt)
            return list(result.scalars().all())

    def get_by_priority(self, priority: str) -> List[Task]:
        """Get tasks by priority."""
        with self.session_factory() as session:
            stmt = (
                select(Task)
                .options(joinedload(Task.category))
                .where(
                    and_(
                        Task.priority == priority,
                        Task.status == STATUS_PENDING,
                    )
                )
                .order_by(Task.due_date, Task.due_time)
            )
            result = session.execute(stmt)
            return list(result.scalars().all())

    def get_by_date_range(self, start_date: date, end_date: date) -> List[Task]:
        """
        Get tasks within date range.

        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)

        Returns:
            List of tasks in date range
        """
        with self.session_factory() as session:
            stmt = (
                select(Task)
                .options(joinedload(Task.category))
                .where(
                    and_(
                        Task.due_date >= start_date,
                        Task.due_date <= end_date,
                        Task.status != STATUS_CANCELLED,
                    )
                )
                .order_by(Task.due_date, Task.due_time)
            )
            result = session.execute(stmt)
            return list(result.scalars().all())

    def get_by_month(self, year: int, month: int) -> List[Task]:
        """
        Get tasks for a specific month.

        Args:
            year: Year
            month: Month (1-12)

        Returns:
            List of tasks in month
        """
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)

        return self.get_by_date_range(start_date, end_date)

    def search(self, query: str, filters: Optional[Dict] = None) -> List[Task]:
        """
        Search tasks with filters.

        Args:
            query: Search query string
            filters: Optional filters (status, priority, category, date range)

        Returns:
            List of matching tasks
        """
        with self.session_factory() as session:
            stmt = (
                select(Task)
                .options(joinedload(Task.category))
                .where(
                    or_(
                        Task.title.ilike(f"%{query}%"),
                        Task.description.ilike(f"%{query}%"),
                    )
                )
            )

            if filters:
                if 'status' in filters:
                    stmt = stmt.where(Task.status == filters['status'])
                if 'priority' in filters:
                    stmt = stmt.where(Task.priority == filters['priority'])
                if 'category_id' in filters:
                    stmt = stmt.where(Task.category_id == filters['category_id'])
                if 'start_date' in filters:
                    stmt = stmt.where(Task.due_date >= filters['start_date'])
                if 'end_date' in filters:
                    stmt = stmt.where(Task.due_date <= filters['end_date'])

            stmt = stmt.order_by(Task.due_date, Task.due_time)
            result = session.execute(stmt)
            return list(result.scalars().all())

    def get_statistics(self) -> Dict[str, int]:
        """
        Get task statistics.

        Returns:
            Dictionary with task counts
        """
        with self.session_factory() as session:
            total = session.execute(
                select(func.count()).select_from(Task)
            ).scalar() or 0

            completed = session.execute(
                select(func.count()).select_from(Task).where(
                    Task.status == STATUS_COMPLETED
                )
            ).scalar() or 0

            pending = session.execute(
                select(func.count()).select_from(Task).where(
                    Task.status == STATUS_PENDING
                )
            ).scalar() or 0

            overdue = session.execute(
                select(func.count()).select_from(Task).where(
                    and_(
                        Task.status == STATUS_PENDING,
                        Task.due_date < date.today(),
                    )
                )
            ).scalar() or 0

            return {
                'total': total,
                'completed': completed,
                'pending': pending,
                'overdue': overdue,
            }

    def get_with_reminders(self) -> List[Task]:
        """Get tasks with pending reminders."""
        with self.session_factory() as session:
            stmt = (
                select(Task)
                .options(joinedload(Task.reminders))
                .where(
                    and_(
                        Task.status == STATUS_PENDING,
                        Task.reminders.any(),
                    )
                )
            )
            result = session.execute(stmt)
            return list(result.scalars().unique().all())