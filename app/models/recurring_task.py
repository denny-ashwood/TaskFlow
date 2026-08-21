"""
Recurring task model (for future use).
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class RecurringTask(Base):
    """Recurring task entity."""

    __tablename__ = 'recurring_tasks'

    task_id = Column(Integer, ForeignKey('tasks.id', ondelete='CASCADE'), nullable=False)
    frequency = Column(String(20), nullable=False)  # daily, weekly, monthly, custom
    interval = Column(Integer, nullable=False, default=1)
    next_run_date = Column(DateTime, nullable=True)

    # Relationships
    task = relationship("Task")

    def __repr__(self) -> str:
        return f"<RecurringTask(id={self.id}, frequency='{self.frequency}')>"