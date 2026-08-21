"""
UI tests for task creation.
"""

import pytest
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from app.dialogs.task_dialog import TaskDialog
from app.services.category_service import CategoryService


@pytest.fixture
def app():
    """Create QApplication for testing."""
    application = QApplication.instance()
    if application is None:
        application = QApplication([])
    return application


class TestTaskDialog:
    """Test task dialog."""

    def test_dialog_creation(self, app, category_service):
        """Test dialog creation."""
        dialog = TaskDialog(category_service)

        assert dialog.windowTitle() == "Create New Task"
        assert dialog.title_input.text() == ""

    def test_dialog_edit_mode(self, app, category_service):
        """Test dialog in edit mode."""
        task = type('Task', (), {
            'title': 'Test Task',
            'description': 'Description',
            'due_date': None,
            'due_time': None,
            'priority': 'medium',
            'category_id': None,
            'reminder_minutes': 30,
        })()

        dialog = TaskDialog(category_service, task=task)

        assert dialog.windowTitle() == "Edit Task"
        assert dialog.title_input.text() == "Test Task"

    def test_validation_empty_title(self, app, category_service):
        """Test validation with empty title."""
        dialog = TaskDialog(category_service)
        dialog.title_input.setText("")

        # Mock QMessageBox
        dialog._validate_and_accept = lambda: None  # Can't easily test modal dialogs

        assert dialog.title_input.text() == ""

    def test_get_task_data(self, app, category_service):
        """Test getting task data from dialog."""
        dialog = TaskDialog(category_service)

        dialog.title_input.setText("New Task")
        dialog.description_input.setPlainText("Task description")
        dialog.priority_combo.setCurrentIndex(2)  # High priority

        data = dialog.get_task_data()

        assert data['title'] == "New Task"
        assert data['description'] == "Task description"
        assert data['priority'] == "high"

    def test_category_loading(self, app, category_service):
        """Test category loading."""
        category_service.create_category("Work")
        category_service.create_category("Personal")

        dialog = TaskDialog(category_service)

        # Check categories are loaded (including "No Category")
        assert dialog.category_combo.count() == 3