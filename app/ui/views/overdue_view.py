"""
Overdue view implementation.
"""

import logging
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


class OverdueView(QWidget):
    """View for overdue tasks."""

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
        Initialize overdue view.

        Args:
            task_service: Task service instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.task_service = task_service

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup overdue view UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()

        self.title_label = QLabel("Overdue")
        self.title_label.setStyleSheet(
            "font-size: 28px; font-weight: 700; color: #ba1a1a;"
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
        self.content_layout.setSpacing(8)

        scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(scroll_area)

    def refresh(self) -> None:
        """Refresh overdue tasks."""
        self._clear_content()
        self._load_tasks()

    def _load_tasks(self) -> None:
        """Load overdue tasks."""
        tasks = self.task_service.get_overdue_tasks()

        if not tasks:
            empty_state = EmptyState(
                "You're all caught up!",
                icon="✅",
                action_text="Add Task",
            )
            empty_state.action_clicked.connect(self.add_task_requested.emit)
            self.content_layout.addWidget(empty_state)
            return

        # Warning label
        warning_label = QLabel(f"You have {len(tasks)} overdue task(s).")
        warning_label.setStyleSheet(
            "font-size: 14px; color: #ba1a1a; font-weight: 600;"
            "padding: 8px;"
        )
        self.content_layout.addWidget(warning_label)

        # Task widgets
        for task in tasks:
            task_widget = TaskWidget(task)
            task_widget.completed.connect(self.task_completed.emit)
            task_widget.edit_requested.connect(self.edit_task_requested.emit)
            task_widget.delete_requested.connect(self.delete_task_requested.emit)

            # Add overdue indicator
            task_widget.setStyleSheet(
                task_widget.styleSheet() +
                "border-left: 4px solid #ba1a1a;"
            )

            self.content_layout.addWidget(task_widget)

        self.content_layout.addStretch()

    def _clear_content(self) -> None:
        """Clear all content widgets."""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()