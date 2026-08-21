"""
Unit tests for repositories.
"""

import pytest
from datetime import date, datetime, timedelta

from app.models.task import Task
from app.models.category import Category
from app.models.reminder import Reminder


class TestTaskRepository:
    """Test TaskRepository."""

    def test_create_task(self, task_repository):
        """Test task creation."""
        task = task_repository.create(
            title="Test Task",
            description="Description",
            priority="high",
        )

        assert task.id is not None
        assert task.title == "Test Task"
        assert task.priority == "high"

    def test_get_task_by_id(self, task_repository):
        """Test getting task by ID."""
        created = task_repository.create(title="Test Task")
        fetched = task_repository.get_by_id(created.id)

        assert fetched is not None
        assert fetched.id == created.id
        assert fetched.title == "Test Task"

    def test_get_nonexistent_task(self, task_repository):
        """Test getting non-existent task."""
        task = task_repository.get_by_id(9999)
        assert task is None

    def test_get_all_tasks(self, task_repository):
        """Test getting all tasks."""
        task_repository.create(title="Task 1")
        task_repository.create(title="Task 2")
        task_repository.create(title="Task 3")

        tasks = task_repository.get_all()
        assert len(tasks) == 3

    def test_update_task(self, task_repository):
        """Test task update."""
        task = task_repository.create(title="Original Title")
        updated = task_repository.update(task.id, title="Updated Title")

        assert updated is not None
        assert updated.title == "Updated Title"

    def test_delete_task(self, task_repository):
        """Test task deletion."""
        task = task_repository.create(title="Test Task")
        deleted = task_repository.delete(task.id)

        assert deleted is True
        assert task_repository.get_by_id(task.id) is None

    def test_delete_nonexistent_task(self, task_repository):
        """Test deleting non-existent task."""
        deleted = task_repository.delete(9999)
        assert deleted is False

    def test_get_today_tasks(self, task_repository):
        """Test getting today's tasks."""
        today = date.today()
        tomorrow = today + timedelta(days=1)

        task_repository.create(title="Today Task", due_date=today)
        task_repository.create(title="Tomorrow Task", due_date=tomorrow)
        task_repository.create(title="No Date Task")

        today_tasks = task_repository.get_today_tasks()
        assert len(today_tasks) == 1
        assert today_tasks[0].title == "Today Task"

    def test_get_overdue_tasks(self, task_repository):
        """Test getting overdue tasks."""
        yesterday = date.today() - timedelta(days=1)
        tomorrow = date.today() + timedelta(days=1)

        task_repository.create(title="Overdue Task", due_date=yesterday)
        task_repository.create(title="Future Task", due_date=tomorrow)

        overdue_tasks = task_repository.get_overdue_tasks()
        assert len(overdue_tasks) == 1
        assert overdue_tasks[0].title == "Overdue Task"

    def test_get_completed_tasks(self, task_repository):
        """Test getting completed tasks."""
        task_repository.create(title="Pending Task", status="pending")
        task_repository.create(title="Completed Task", status="completed")

        completed_tasks = task_repository.get_completed_tasks()
        assert len(completed_tasks) == 1
        assert completed_tasks[0].title == "Completed Task"

    def test_search_tasks(self, task_repository):
        """Test task search."""
        task_repository.create(title="Meeting with team", description="Weekly sync")
        task_repository.create(title="Write report", description="Quarterly report")
        task_repository.create(title="Buy groceries")

        results = task_repository.search("report")
        assert len(results) == 1
        assert results[0].title == "Write report"

    def test_get_statistics(self, task_repository):
        """Test task statistics."""
        yesterday = date.today() - timedelta(days=1)

        task_repository.create(title="Task 1", status="pending")
        task_repository.create(title="Task 2", status="completed")
        task_repository.create(title="Task 3", status="pending", due_date=yesterday)

        stats = task_repository.get_statistics()
        assert stats['total'] == 3
        assert stats['completed'] == 1
        assert stats['pending'] == 2
        assert stats['overdue'] == 1


class TestCategoryRepository:
    """Test CategoryRepository."""

    def test_create_category(self, category_repository):
        """Test category creation."""
        category = category_repository.create(name="Work")

        assert category.id is not None
        assert category.name == "Work"

    def test_get_by_name(self, category_repository):
        """Test getting category by name."""
        category_repository.create(name="Personal")

        category = category_repository.get_by_name("Personal")
        assert category is not None
        assert category.name == "Personal"

    def test_get_nonexistent_by_name(self, category_repository):
        """Test getting non-existent category."""
        category = category_repository.get_by_name("Nonexistent")
        assert category is None

    def test_get_with_task_count(self, category_repository, task_repository):
        """Test getting categories with task counts."""
        work = category_repository.create(name="Work")
        personal = category_repository.create(name="Personal")

        task_repository.create(title="Task 1", category_id=work.id)
        task_repository.create(title="Task 2", category_id=work.id)
        task_repository.create(title="Task 3", category_id=personal.id)

        categories = category_repository.get_with_task_count()
        assert len(categories) == 2

        work_cat = [c for c in categories if c['name'] == 'Work'][0]
        assert work_cat['task_count'] == 2


class TestReminderRepository:
    """Test ReminderRepository."""

    def test_create_reminder(self, reminder_repository):
        """Test reminder creation."""
        reminder_time = datetime.now() + timedelta(hours=1)
        reminder = reminder_repository.create(
            task_id=1,
            reminder_time=reminder_time,
        )

        assert reminder.id is not None
        assert reminder.task_id == 1
        assert not reminder.notification_sent

    def test_get_pending_reminders(self, reminder_repository):
        """Test getting pending reminders."""
        past_time = datetime.now() - timedelta(minutes=5)
        future_time = datetime.now() + timedelta(hours=1)

        reminder_repository.create(task_id=1, reminder_time=past_time)
        reminder_repository.create(task_id=2, reminder_time=future_time)

        pending = reminder_repository.get_pending_reminders()
        assert len(pending) == 1
        assert pending[0].task_id == 1

    def test_mark_as_sent(self, reminder_repository):
        """Test marking reminder as sent."""
        reminder = reminder_repository.create(
            task_id=1,
            reminder_time=datetime.now(),
        )

        success = reminder_repository.mark_as_sent(reminder.id)
        assert success is True

        updated = reminder_repository.get_by_id(reminder.id)
        assert updated.notification_sent is True

    def test_delete_by_task(self, reminder_repository):
        """Test deleting reminders by task."""
        reminder_repository.create(task_id=1, reminder_time=datetime.now())
        reminder_repository.create(task_id=1, reminder_time=datetime.now())
        reminder_repository.create(task_id=2, reminder_time=datetime.now())

        count = reminder_repository.delete_by_task(1)
        assert count == 2

        remaining = reminder_repository.get_by_task(1)
        assert len(remaining) == 0