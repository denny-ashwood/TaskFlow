"""
Task dialog for creating and editing tasks.
"""

import logging
from datetime import date, datetime, time
from typing import Dict, Optional

from PySide6.QtCore import QDate, QTime, Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

from app.models.task import Task
from app.services.category_service import CategoryService

logger = logging.getLogger(__name__)


class TaskDialog(QDialog):
    """Dialog for creating or editing tasks."""

    def __init__(
        self,
        category_service: CategoryService,
        task: Optional[Task] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Initialize task dialog.

        Args:
            category_service: Category service instance
            task: Task to edit (None for new task)
            parent: Parent widget
        """
        super().__init__(parent)
        self.category_service = category_service
        self.task = task

        self._setup_ui()

        if task:
            self._load_task_data()

        logger.debug(f"Task dialog initialized (editing: {task is not None})")

    def _setup_ui(self) -> None:
        """Setup dialog UI."""
        self.setWindowTitle("Edit Task" if self.task else "Create New Task")
        self.setModal(True)
        self.setMinimumWidth(500)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)

        # Title input
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Task title...")
        self.title_input.setStyleSheet(
            """
            QLineEdit {
                font-size: 20px;
                font-weight: 600;
                border: none;
                border-bottom: 2px solid #e0e3e5;
                padding: 8px 0;
            }
            QLineEdit:focus {
                border-bottom: 2px solid #0050cb;
            }
            """
        )
        main_layout.addWidget(self.title_input)

        # Description input
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Add details or context...")
        self.description_input.setMaximumHeight(100)
        self.description_input.setStyleSheet(
            """
            QTextEdit {
                border: 1px solid #e0e3e5;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 2px solid #0050cb;
            }
            """
        )
        main_layout.addWidget(self.description_input)

        # Form layout for fields
        form_layout = QFormLayout()
        form_layout.setSpacing(12)

        # Due date
        self.due_date_input = QDateEdit()
        self.due_date_input.setCalendarPopup(True)
        self.due_date_input.setDate(QDate.currentDate())
        self.due_date_input.setDisplayFormat("MMMM d, yyyy")
        form_layout.addRow("Due Date:", self.due_date_input)

        # Due time
        self.due_time_input = QTimeEdit()
        self.due_time_input.setTime(QTime.currentTime())
        self.due_time_input.setDisplayFormat("h:mm AP")
        form_layout.addRow("Due Time:", self.due_time_input)

        # Priority
        self.priority_combo = QComboBox()
        self.priority_combo.addItem("Low", "low")
        self.priority_combo.addItem("Medium", "medium")
        self.priority_combo.addItem("High", "high")
        form_layout.addRow("Priority:", self.priority_combo)

        # Category
        self.category_combo = QComboBox()
        self._load_categories()
        form_layout.addRow("Category:", self.category_combo)

        # Reminder
        self.reminder_combo = QComboBox()
        self.reminder_combo.addItem("None", None)
        self.reminder_combo.addItem("At time of event", 0)
        self.reminder_combo.addItem("5 minutes before", 5)
        self.reminder_combo.addItem("10 minutes before", 10)
        self.reminder_combo.addItem("15 minutes before", 15)
        self.reminder_combo.addItem("30 minutes before", 30)
        self.reminder_combo.addItem("1 hour before", 60)
        self.reminder_combo.addItem("2 hours before", 120)
        self.reminder_combo.addItem("1 day before", 1440)
        form_layout.addRow("Reminder:", self.reminder_combo)

        main_layout.addLayout(form_layout)

        # Button box
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.button(QDialogButtonBox.Ok).setText("Save Task")
        button_box.button(QDialogButtonBox.Ok).setStyleSheet(
            """
            QPushButton {
                background-color: #0050cb;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #0066ff;
            }
            """
        )
        button_box.button(QDialogButtonBox.Cancel).setText("Cancel")

        button_box.accepted.connect(self._validate_and_accept)
        button_box.rejected.connect(self.reject)

        main_layout.addWidget(button_box)

    def _load_categories(self) -> None:
        """Load categories into combo box."""
        self.category_combo.clear()
        self.category_combo.addItem("No Category", None)

        categories = self.category_service.get_all_categories()
        for category in categories:
            self.category_combo.addItem(category.name, category.id)

    def _load_task_data(self) -> None:
        """Load task data into form fields."""
        if not self.task:
            return

        self.title_input.setText(self.task.title)

        if self.task.description:
            self.description_input.setPlainText(self.task.description)

        if self.task.due_date:
            self.due_date_input.setDate(QDate(
                self.task.due_date.year,
                self.task.due_date.month,
                self.task.due_date.day,
            ))

        if self.task.due_time:
            self.due_time_input.setTime(QTime(
                self.task.due_time.hour,
                self.task.due_time.minute,
            ))

        # Set priority
        priority_index = self.priority_combo.findData(self.task.priority)
        if priority_index >= 0:
            self.priority_combo.setCurrentIndex(priority_index)

        # Set category
        if self.task.category_id:
            category_index = self.category_combo.findData(
                self.task.category_id)
            if category_index >= 0:
                self.category_combo.setCurrentIndex(category_index)

        # Set reminder
        if self.task.reminder_minutes is not None:
            reminder_index = self.reminder_combo.findData(
                self.task.reminder_minutes)
            if reminder_index >= 0:
                self.reminder_combo.setCurrentIndex(reminder_index)

    def _validate_and_accept(self) -> None:
        """Validate input and accept dialog."""
        # Validate title
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Validation Error",
                                "Task title cannot be empty.")
            self.title_input.setFocus()
            return

        if len(title) > 255:
            QMessageBox.warning(
                self,
                "Validation Error",
                "Task title cannot exceed 255 characters."
            )
            self.title_input.setFocus()
            return

        self.accept()

    def get_task_data(self) -> Dict:
        """
        Get task data from form.

        Returns:
            Dictionary with task data
        """
        # Get values
        title = self.title_input.text().strip()
        description = self.description_input.toPlainText().strip()

        # Due date
        qdate = self.due_date_input.date()
        due_date = date(qdate.year(), qdate.month(), qdate.day())

        # Due time
        qtime = self.due_time_input.time()
        due_time = time(qtime.hour(), qtime.minute())

        priority = self.priority_combo.currentData()
        category_id = self.category_combo.currentData()
        reminder_minutes = self.reminder_combo.currentData()

        data = {
            'title': title,
            'description': description or None,
            'due_date': due_date,
            'due_time': due_time,
            'priority': priority,
            'category_id': category_id,
            'reminder_minutes': reminder_minutes,
        }

        return data
