"""
Task model.
"""

from datetime import date, datetime, time
from typing import Optional

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import relationship

from app.config.constants import PRIORITY_MEDIUM, STATUS_PENDING
from app.models.base import Base


class Task(Base):
    """Task entity."""

    __tablename__ = 'tasks'

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    due_date = Column(Date, nullable=True)
    due_time = Column(Time, nullable=True)
    priority = Column(String(10), nullable=False, default=PRIORITY_MEDIUM)
    status = Column(String(20), nullable=False, default=STATUS_PENDING)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='SET NULL'), nullable=True)
    reminder_minutes = Column(Integer, nullable=True, default=30)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    category = relationship("Category", back_populates="tasks")
    reminders = relationship("Reminder", back_populates="task", cascade="all, delete-orphan")

    @property
    def is_completed(self) -> bool:
        """Check if task is completed."""
        return self.status == "completed"

    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue."""
        if self.is_completed or not self.due_date:
            return False

        now = datetime.now()
        if self.due_time:
            due_datetime = datetime.combine(self.due_date, self.due_time)
            return due_datetime < now
        else:
            return self.due_date < now.date()

    @property
    def due_datetime(self) -> Optional[datetime]:
        """Get combined due date and time."""
        if self.due_date and self.due_time:
            return datetime.combine(self.due_date, self.due_time)
        elif self.due_date:
            return datetime.combine(self.due_date, time.min)
        return None

    def complete(self) -> None:
        """Mark task as completed."""
        self.status = "completed"
        self.completed_at = datetime.now()

    def restore(self) -> None:
        """Restore completed task."""
        self.status = "pending"
        self.completed_at = None

    def cancel(self) -> None:
        """Cancel task."""
        self.status = "cancelled"

    def __repr__(self) -> str:
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"