"""
Upcoming view implementation.
"""

import logging
from datetime import date, timedelta
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.services.task_service import TaskService
from app.widgets.empty_state import EmptyState
from app.widgets.task_widget import TaskWidget

logger = logging.getLogger(__name__)


class UpcomingView(QWidget):
    """View for upcoming tasks grouped by date."""

    add_task_requested = Signal()
    edit_task_requested = Signal(int)
    delete_task_requested = Signal(int)
    task_completed = Signal(int)

    def __init__(
        self,
        task_service: TaskService,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Initialize upcoming view.

        Args:
            task_service: Task service instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.task_service = task_service

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup upcoming view UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()

        self.title_label = QLabel("Upcoming")
        self.title_label.setStyleSheet(
            "font-size: 28px; font-weight: 700;"
        )
        header_layout.addWidget(self.title_label)

        header_layout.addStretch()

        # Add task button
        self.add_task_button = QPushButton("+ Add Task")
        self.add_task_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0050cb;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #0066ff;
            }
            """
        )
        self.add_task_button.clicked.connect(self.add_task_requested.emit)
        header_layout.addWidget(self.add_task_button)

        main_layout.addLayout(header_layout)

        # Scrollable content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none; background: transparent;")

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(16)

        scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(scroll_area)

    def refresh(self) -> None:
        """Refresh upcoming tasks."""
        self._clear_content()
        self._load_tasks()

    def _load_tasks(self) -> None:
        """Load upcoming tasks grouped by date."""
        tasks = self.task_service.get_upcoming_tasks(days=30)

        if not tasks:
            empty_state = EmptyState(
                "No upcoming tasks.",
                icon="📅",
                action_text="Add Task",
            )
            empty_state.action_clicked.connect(self.add_task_requested.emit)
            self.content_layout.addWidget(empty_state)
            return

        # Group tasks by date
        tasks_by_date = {}
        for task in tasks:
            if task.due_date:
                if task.due_date not in tasks_by_date:
                    tasks_by_date[task.due_date] = []
                tasks_by_date[task.due_date].append(task)

        # Display grouped tasks
        today = date.today()
        tomorrow = today + timedelta(days=1)

        for task_date in sorted(tasks_by_date.keys()):
            date_tasks = tasks_by_date[task_date]

            # Format date label
            if task_date == tomorrow:
                date_label_text = "Tomorrow"
            elif task_date == today + timedelta(days=2):
                date_label_text = f"Day After Tomorrow ({task_date.strftime('%A')})"
            else:
                date_label_text = task_date.strftime("%A, %B %d")

            self._add_date_section(date_label_text, date_tasks)

        self.content_layout.addStretch()

    def _add_date_section(self, date_text: str, tasks: list) -> None:
        """Add a date section with tasks."""
        # Date label
        date_label = QLabel(date_text)
        date_label.setStyleSheet(
            "font-size: 16px; font-weight: 600; color: #0050cb;"
            "padding: 12px 0 4px 0;"
            "border-bottom: 1px solid #e0e3e5;"
        )
        self.content_layout.addWidget(date_label)

        # Task widgets
        for task in tasks:
            task_widget = TaskWidget(task)
            task_widget.completed.connect(self.task_completed.emit)
            task_widget.edit_requested.connect(self.edit_task_requested.emit)
            task_widget.delete_requested.connect(self.delete_task_requested.emit)
            self.content_layout.addWidget(task_widget)

    def _clear_content(self) -> None:
        """Clear all content widgets."""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()