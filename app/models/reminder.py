"""
Reminder model.
"""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.models.base import Base


class Reminder(Base):
    """Reminder entity."""

    __tablename__ = 'reminders'

    task_id = Column(Integer, ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    reminder_time = Column(DateTime, nullable=False)
    notification_sent = Column(Boolean, nullable=False, default=False)

    # Relationships
    task = relationship("Task", back_populates="reminders")

    @property
    def is_due(self) -> bool:
        """Check if reminder is due."""
        return self.reminder_time <= datetime.now() and not self.notification_sent

    def mark_sent(self) -> None:
        """Mark reminder as sent."""
        self.notification_sent = True

    def __repr__(self) -> str:
        return f"<Reminder(id={self.id}, task_id={self.task_id}, time={self.reminder_time})>"