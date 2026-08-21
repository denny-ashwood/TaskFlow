"""
Today view implementation.
"""

import logging
from datetime import datetime, time
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


class TodayView(QWidget):
    """View for today's tasks grouped by time period."""

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
        Initialize today view.

        Args:
            task_service: Task service instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.task_service = task_service

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup today view UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()

        self.title_label = QLabel("Today")
        self.title_label.setStyleSheet(
            "font-size: 28px; font-weight: 700;"
        )
        header_layout.addWidget(self.title_label)

        # Date label
        today = datetime.now()
        self.date_label = QLabel(today.strftime("%A, %B %d"))
        self.date_label.setStyleSheet(
            "font-size: 14px; color: gray;"
        )
        header_layout.addWidget(self.date_label)

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
        """Refresh today's tasks."""
        self._clear_content()
        self._load_tasks()

    def _load_tasks(self) -> None:
        """Load today's tasks grouped by period."""
        tasks = self.task_service.get_today_tasks()

        if not tasks:
            empty_state = EmptyState(
                "No tasks scheduled for today.",
                icon="🎉",
                action_text="Add Task",
            )
            empty_state.action_clicked.connect(self.add_task_requested.emit)
            self.content_layout.addWidget(empty_state)
            return

        # Group tasks by time period
        morning_tasks = []
        afternoon_tasks = []
        evening_tasks = []
        no_time_tasks = []

        for task in tasks:
            if not task.due_time:
                no_time_tasks.append(task)
            elif task.due_time < time(12, 0):
                morning_tasks.append(task)
            elif task.due_time < time(17, 0):
                afternoon_tasks.append(task)
            else:
                evening_tasks.append(task)

        # Display grouped tasks
        if morning_tasks:
            self._add_period_section("Morning", morning_tasks)

        if afternoon_tasks:
            self._add_period_section("Afternoon", afternoon_tasks)

        if evening_tasks:
            self._add_period_section("Evening", evening_tasks)

        if no_time_tasks:
            self._add_period_section("No Time Set", no_time_tasks)

        self.content_layout.addStretch()

    def _add_period_section(self, period_name: str, tasks: list) -> None:
        """Add a period section with tasks."""
        # Period label
        period_label = QLabel(period_name)
        period_label.setStyleSheet(
            "font-size: 16px; font-weight: 600; color: #505f76;"
            "padding: 8px 0;"
        )
        self.content_layout.addWidget(period_label)

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