"""
Unit tests for models.
"""

import pytest
from datetime import date, datetime, time, timedelta

from app.models.task import Task
from app.models.category import Category
from app.models.reminder import Reminder
from app.models.setting import Setting


class TestTaskModel:
    """Test Task model."""

    def test_task_creation(self):
        """Test task creation with default values."""
        task = Task(title="Test Task")

        assert task.title == "Test Task"
        assert task.status == "pending"
        assert task.priority == "medium"
        assert task.description is None
        assert task.completed_at is None

    def test_task_is_completed(self):
        """Test task completion check."""
        task = Task(title="Test Task")
        assert not task.is_completed

        task.status = "completed"
        assert task.is_completed

    def test_task_is_overdue_no_due_date(self):
        """Test overdue check without due date."""
        task = Task(title="Test Task")
        assert not task.is_overdue

    def test_task_is_overdue_with_date(self):
        """Test overdue check with past date."""
        yesterday = date.today() - timedelta(days=1)
        task = Task(title="Test Task", due_date=yesterday)
        assert task.is_overdue

    def test_task_is_not_overdue_future(self):
        """Test overdue check with future date."""
        tomorrow = date.today() + timedelta(days=1)
        task = Task(title="Test Task", due_date=tomorrow)
        assert not task.is_overdue

    def test_task_due_datetime(self):
        """Test due datetime property."""
        due_date = date(2024, 1, 15)
        due_time = time(14, 30)
        task = Task(title="Test Task", due_date=due_date, due_time=due_time)

        expected = datetime(2024, 1, 15, 14, 30)
        assert task.due_datetime == expected

    def test_task_complete(self):
        """Test task completion."""
        task = Task(title="Test Task")
        task.complete()

        assert task.status == "completed"
        assert task.completed_at is not None

    def test_task_restore(self):
        """Test task restoration."""
        task = Task(title="Test Task")
        task.complete()
        task.restore()

        assert task.status == "pending"
        assert task.completed_at is None

    def test_task_cancel(self):
        """Test task cancellation."""
        task = Task(title="Test Task")
        task.cancel()

        assert task.status == "cancelled"

    def test_task_to_dict(self):
        """Test task to dictionary conversion."""
        task = Task(title="Test Task", priority="high")
        data = task.to_dict()

        assert data['title'] == "Test Task"
        assert data['priority'] == "high"


class TestCategoryModel:
    """Test Category model."""

    def test_category_creation(self):
        """Test category creation."""
        category = Category(name="Work", description="Work tasks")

        assert category.name == "Work"
        assert category.description == "Work tasks"

    def test_category_to_dict(self):
        """Test category to dictionary."""
        category = Category(name="Personal")
        data = category.to_dict()

        assert data['name'] == "Personal"


class TestReminderModel:
    """Test Reminder model."""

    def test_reminder_creation(self):
        """Test reminder creation."""
        reminder_time = datetime.now() + timedelta(hours=1)
        reminder = Reminder(task_id=1, reminder_time=reminder_time)

        assert reminder.task_id == 1
        assert reminder.reminder_time == reminder_time
        assert not reminder.notification_sent

    def test_reminder_is_due(self):
        """Test reminder due check."""
        past_time = datetime.now() - timedelta(minutes=5)
        reminder = Reminder(task_id=1, reminder_time=past_time)

        assert reminder.is_due

    def test_reminder_not_due(self):
        """Test reminder not due check."""
        future_time = datetime.now() + timedelta(hours=1)
        reminder = Reminder(task_id=1, reminder_time=future_time)

        assert not reminder.is_due

    def test_reminder_mark_sent(self):
        """Test mark reminder as sent."""
        reminder = Reminder(task_id=1, reminder_time=datetime.now())
        reminder.mark_sent()

        assert reminder.notification_sent


class TestSettingModel:
    """Test Setting model."""

    def test_setting_creation(self):
        """Test setting creation."""
        setting = Setting(key="theme", value="dark")

        assert setting.key == "theme"
        assert setting.value == "dark"