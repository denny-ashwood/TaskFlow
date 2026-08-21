"""
Unit tests for services.
"""

import pytest
from datetime import date, datetime, timedelta

from app.exceptions.task_errors import (
    TaskNotFoundError,
    TaskAlreadyCompletedError,
    EmptyTitleError,
    TitleTooLongError,
    InvalidPriorityError,
)
from app.exceptions import ValidationError


class TestTaskService:
    """Test TaskService."""

    def test_create_task(self, task_service):
        """Test task creation."""
        task = task_service.create_task({
            'title': 'Test Task',
            'description': 'Description',
            'priority': 'high',
        })

        assert task.id is not None
        assert task.title == 'Test Task'
        assert task.priority == 'high'

    def test_create_task_empty_title(self, task_service):
        """Test task creation with empty title."""
        with pytest.raises(EmptyTitleError):
            task_service.create_task({'title': ''})

    def test_create_task_long_title(self, task_service):
        """Test task creation with too long title."""
        with pytest.raises(TitleTooLongError):
            task_service.create_task({'title': 'A' * 256})

    def test_create_task_invalid_priority(self, task_service):
        """Test task creation with invalid priority."""
        with pytest.raises(InvalidPriorityError):
            task_service.create_task({'title': 'Test', 'priority': 'urgent'})

    def test_update_task(self, task_service, created_task):
        """Test task update."""
        updated = task_service.update_task(
            created_task.id,
            {'title': 'Updated Title'},
        )

        assert updated.title == 'Updated Title'

    def test_update_nonexistent_task(self, task_service):
        """Test updating non-existent task."""
        with pytest.raises(TaskNotFoundError):
            task_service.update_task(9999, {'title': 'Test'})

    def test_delete_task(self, task_service, created_task):
        """Test task deletion."""
        deleted = task_service.delete_task(created_task.id)
        assert deleted is True

        with pytest.raises(TaskNotFoundError):
            task_service.get_task(created_task.id)

    def test_delete_nonexistent_task(self, task_service):
        """Test deleting non-existent task."""
        with pytest.raises(TaskNotFoundError):
            task_service.delete_task(9999)

    def test_complete_task(self, task_service, created_task):
        """Test task completion."""
        completed = task_service.complete_task(created_task.id)

        assert completed.status == 'completed'
        assert completed.completed_at is not None

    def test_complete_already_completed(self, task_service, created_task):
        """Test completing already completed task."""
        task_service.complete_task(created_task.id)

        with pytest.raises(TaskAlreadyCompletedError):
            task_service.complete_task(created_task.id)

    def test_complete_nonexistent_task(self, task_service):
        """Test completing non-existent task."""
        with pytest.raises(TaskNotFoundError):
            task_service.complete_task(9999)

    def test_restore_task(self, task_service, created_task):
        """Test task restoration."""
        task_service.complete_task(created_task.id)
        restored = task_service.restore_task(created_task.id)

        assert restored.status == 'pending'
        assert restored.completed_at is None

    def test_get_task(self, task_service, created_task):
        """Test getting task."""
        task = task_service.get_task(created_task.id)
        assert task is not None
        assert task.id == created_task.id

    def test_get_nonexistent_task(self, task_service):
        """Test getting non-existent task."""
        task = task_service.get_task(9999)
        assert task is None

    def test_get_today_tasks(self, task_service):
        """Test getting today's tasks."""
        today = date.today()
        task_service.create_task({
            'title': 'Today Task',
            'due_date': today,
        })

        today_tasks = task_service.get_today_tasks()
        assert len(today_tasks) == 1
        assert today_tasks[0].title == 'Today Task'

    def test_get_statistics(self, task_service):
        """Test getting statistics."""
        task_service.create_task({'title': 'Task 1'})
        task_service.create_task({'title': 'Task 2'})

        stats = task_service.get_statistics()
        assert stats['total'] == 2
        assert stats['pending'] == 2


class TestCategoryService:
    """Test CategoryService."""

    def test_create_category(self, category_service):
        """Test category creation."""
        category = category_service.create_category('Work', 'Work tasks')

        assert category.id is not None
        assert category.name == 'Work'

    def test_create_category_empty_name(self, category_service):
        """Test category creation with empty name."""
        with pytest.raises(ValidationError):
            category_service.create_category('')

    def test_create_duplicate_category(self, category_service):
        """Test creating duplicate category."""
        category_service.create_category('Work')

        with pytest.raises(ValidationError):
            category_service.create_category('Work')

    def test_get_category(self, category_service):
        """Test getting category."""
        created = category_service.create_category('Personal')
        fetched = category_service.get_category(created.id)

        assert fetched is not None
        assert fetched.name == 'Personal'

    def test_delete_category(self, category_service):
        """Test category deletion."""
        category = category_service.create_category('Temp')
        deleted = category_service.delete_category(category.id)

        assert deleted is True

    def test_get_all_categories(self, category_service):
        """Test getting all categories."""
        category_service.create_category('Work')
        category_service.create_category('Personal')

        categories = category_service.get_all_categories()
        assert len(categories) == 2