"""
Dashboard view implementation.
"""

import logging
from datetime import datetime
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QFrame,
    QSizePolicy,
)

from app.models.task import Task
from app.services.category_service import CategoryService
from app.services.task_service import TaskService
from app.widgets.empty_state import EmptyState
from app.widgets.summary_card import SummaryCard
from app.widgets.task_widget import TaskWidget

logger = logging.getLogger(__name__)


class DashboardView(QWidget):
    """Dashboard view showing overview and today's tasks."""

    add_task_requested = Signal()
    edit_task_requested = Signal(int)
    delete_task_requested = Signal(int)
    task_completed = Signal(int)

    def __init__(
        self,
        task_service: TaskService,
        category_service: CategoryService,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Initialize dashboard view.

        Args:
            task_service: Task service instance
            category_service: Category service instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.task_service = task_service
        self.category_service = category_service

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup dashboard UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()

        header_text_layout = QVBoxLayout()

        # Greeting based on time
        greeting = self._get_greeting()
        self.greeting_label = QLabel(greeting)
        self.greeting_label.setStyleSheet(
            "font-size: 28px; font-weight: 700;"
        )
        header_text_layout.addWidget(self.greeting_label)

        self.subtitle_label = QLabel(
            "Here's what you need to accomplish today.")
        self.subtitle_label.setStyleSheet(
            "font-size: 14px; color: gray;"
        )
        header_text_layout.addWidget(self.subtitle_label)

        header_layout.addLayout(header_text_layout)
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
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0066ff;
            }
            """
        )
        self.add_task_button.clicked.connect(self.add_task_requested.emit)
        header_layout.addWidget(self.add_task_button)

        main_layout.addLayout(header_layout)

        # Summary cards
        summary_layout = QHBoxLayout()
        summary_layout.setSpacing(16)

        self.total_card = SummaryCard("Total Tasks", "0", color="#0050cb")
        self.completed_card = SummaryCard("Completed", "0", color="#505f76")
        self.pending_card = SummaryCard("Pending", "0", color="#a33200")
        self.overdue_card = SummaryCard("Overdue", "0", color="#ba1a1a")

        summary_layout.addWidget(self.total_card)
        summary_layout.addWidget(self.completed_card)
        summary_layout.addWidget(self.pending_card)
        summary_layout.addWidget(self.overdue_card)

        main_layout.addLayout(summary_layout)

        # Content area with equal split
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Today's tasks section (50% width)
        today_section = self._create_today_section()
        content_layout.addWidget(today_section, stretch=1)

        # Upcoming tasks section (50% width)
        upcoming_section = self._create_upcoming_section()
        content_layout.addWidget(upcoming_section, stretch=1)

        main_layout.addLayout(content_layout, stretch=1)

    def _create_today_section(self) -> QWidget:
        """Create today's tasks section."""
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(12)

        # Section header
        header_layout = QHBoxLayout()

        today_title = QLabel("Today's Tasks")
        today_title.setStyleSheet(
            "font-size: 18px; font-weight: 600;"
        )
        header_layout.addWidget(today_title)

        # Task count badge
        self.today_count_label = QLabel("0")
        self.today_count_label.setStyleSheet(
            """
            background-color: #e0e0e0;
            color: #333333;
            border-radius: 10px;
            padding: 2px 8px;
            font-size: 12px;
            font-weight: 600;
            """
        )
        header_layout.addWidget(self.today_count_label)

        header_layout.addStretch()

        section_layout.addLayout(header_layout)

        # Scrollable task list
        self.today_tasks_container = QWidget()
        self.today_tasks_layout = QVBoxLayout(self.today_tasks_container)
        self.today_tasks_layout.setContentsMargins(0, 0, 0, 0)
        self.today_tasks_layout.setSpacing(8)

        today_scroll = QScrollArea()
        today_scroll.setWidget(self.today_tasks_container)
        today_scroll.setWidgetResizable(True)
        today_scroll.setStyleSheet(
            """
            QScrollArea {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: #fafafa;
            }
            """
        )
        section_layout.addWidget(today_scroll)

        return section_widget

    def _create_upcoming_section(self) -> QWidget:
        """Create upcoming tasks section."""
        section_widget = QWidget()
        section_layout = QVBoxLayout(section_widget)
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(12)

        # Section header
        header_layout = QHBoxLayout()

        upcoming_title = QLabel("Upcoming")
        upcoming_title.setStyleSheet(
            "font-size: 18px; font-weight: 600;"
        )
        header_layout.addWidget(upcoming_title)

        # Task count badge
        self.upcoming_count_label = QLabel("0")
        self.upcoming_count_label.setStyleSheet(
            """
            background-color: #e0e0e0;
            color: #333333;
            border-radius: 10px;
            padding: 2px 8px;
            font-size: 12px;
            font-weight: 600;
            """
        )
        header_layout.addWidget(self.upcoming_count_label)

        header_layout.addStretch()

        section_layout.addLayout(header_layout)

        # Scrollable upcoming list
        self.upcoming_tasks_container = QWidget()
        self.upcoming_tasks_layout = QVBoxLayout(self.upcoming_tasks_container)
        self.upcoming_tasks_layout.setContentsMargins(0, 0, 0, 0)
        self.upcoming_tasks_layout.setSpacing(8)

        upcoming_scroll = QScrollArea()
        upcoming_scroll.setWidget(self.upcoming_tasks_container)
        upcoming_scroll.setWidgetResizable(True)
        upcoming_scroll.setStyleSheet(
            """
            QScrollArea {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                background-color: #fafafa;
            }
            """
        )
        section_layout.addWidget(upcoming_scroll)

        return section_widget

    def _get_greeting(self) -> str:
        """Get time-appropriate greeting."""
        hour = datetime.now().hour

        if hour < 12:
            return "Good morning"
        elif hour < 17:
            return "Good afternoon"
        else:
            return "Good evening"

    def refresh(self) -> None:
        """Refresh dashboard data."""
        self._update_summary_cards()
        self._load_today_tasks()
        self._load_upcoming_tasks()

    def _update_summary_cards(self) -> None:
        """Update summary cards with current statistics."""
        stats = self.task_service.get_statistics()

        self.total_card.update_value(str(stats.get('total', 0)))
        self.completed_card.update_value(str(stats.get('completed', 0)))
        self.pending_card.update_value(str(stats.get('pending', 0)))
        self.overdue_card.update_value(str(stats.get('overdue', 0)))

    def _load_today_tasks(self) -> None:
        """Load today's tasks."""
        # Clear existing widgets
        self._clear_layout(self.today_tasks_layout)

        # Get today's tasks
        tasks = self.task_service.get_today_tasks()
        logger.debug(f"Loading {len(tasks)} today's tasks")

        # Update count badge
        self.today_count_label.setText(str(len(tasks)))

        if not tasks:
            empty_state = EmptyState(
                "No tasks scheduled for today.",
                icon="🎉",
                action_text="Add Task",
            )
            empty_state.action_clicked.connect(self.add_task_requested.emit)
            self.today_tasks_layout.addWidget(empty_state)
        else:
            for task in tasks:
                task_widget = TaskWidget(task)
                # Connect signals properly
                task_widget.completed.connect(self._handle_task_completed)
                task_widget.edit_requested.connect(self._handle_edit_task)
                task_widget.delete_requested.connect(self._handle_delete_task)
                task_widget.clicked.connect(self._handle_task_clicked)
                self.today_tasks_layout.addWidget(task_widget)

            self.today_tasks_layout.addStretch()

    def _load_upcoming_tasks(self) -> None:
        """Load upcoming tasks."""
        # Clear existing widgets
        self._clear_layout(self.upcoming_tasks_layout)

        # Get upcoming tasks (next 7 days)
        tasks = self.task_service.get_upcoming_tasks(days=7)
        logger.debug(f"Loading {len(tasks)} upcoming tasks")

        # Update count badge
        self.upcoming_count_label.setText(str(len(tasks)))

        if not tasks:
            empty_state = EmptyState(
                "No upcoming tasks.",
                icon="📅",
            )
            self.upcoming_tasks_layout.addWidget(empty_state)
        else:
            # Show up to 10 upcoming tasks
            for task in tasks[:10]:
                task_widget = TaskWidget(task)
                # Connect signals properly
                task_widget.completed.connect(self._handle_task_completed)
                task_widget.edit_requested.connect(self._handle_edit_task)
                task_widget.delete_requested.connect(self._handle_delete_task)
                self.upcoming_tasks_layout.addWidget(task_widget)

            self.upcoming_tasks_layout.addStretch()

    def _handle_task_completed(self, task_id: int) -> None:
        """Handle task completion."""
        logger.info(f"Task completed signal received for task {task_id}")
        self.task_completed.emit(task_id)
        # Refresh immediately
        self.refresh()

    def _handle_edit_task(self, task_id: int) -> None:
        """Handle edit task request."""
        logger.info(f"Edit task signal received for task {task_id}")
        self.edit_task_requested.emit(task_id)

    def _handle_delete_task(self, task_id: int) -> None:
        """Handle delete task request."""
        logger.info(f"Delete task signal received for task {task_id}")
        self.delete_task_requested.emit(task_id)

    def _handle_task_clicked(self, task_id: int) -> None:
        """Handle task click."""
        logger.debug(f"Task clicked: {task_id}")
        # Open edit dialog on click
        self.edit_task_requested.emit(task_id)

    def _clear_layout(self, layout) -> None:
        """Clear all widgets from layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self._clear_layout(item.layout())
