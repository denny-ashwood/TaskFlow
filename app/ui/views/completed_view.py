"""
Completed view implementation.
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


class CompletedView(QWidget):
    """View for completed tasks."""

    edit_task_requested = Signal(int)
    delete_task_requested = Signal(int)
    task_restored = Signal(int)

    def __init__(
        self,
        task_service: TaskService,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Initialize completed view.

        Args:
            task_service: Task service instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.task_service = task_service

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup completed view UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()

        self.title_label = QLabel("Completed")
        self.title_label.setStyleSheet(
            "font-size: 28px; font-weight: 700;"
        )
        header_layout.addWidget(self.title_label)

        header_layout.addStretch()

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
        """Refresh completed tasks."""
        self._clear_content()
        self._load_tasks()

    def _load_tasks(self) -> None:
        """Load completed tasks."""
        tasks = self.task_service.get_completed_tasks(limit=50)

        if not tasks:
            empty_state = EmptyState(
                "No completed tasks yet.",
                icon="📋",
            )
            self.content_layout.addWidget(empty_state)
            return

        # Task widgets
        for task in tasks:
            task_widget = TaskWidget(task, show_checkbox=False)
            task_widget.edit_requested.connect(self.edit_task_requested.emit)
            task_widget.delete_requested.connect(self.delete_task_requested.emit)

            # Add restore button
            restore_button = QPushButton("Restore")
            restore_button.setStyleSheet(
                """
                QPushButton {
                    background-color: transparent;
                    color: #0050cb;
                    border: 1px solid #0050cb;
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #0050cb;
                    color: white;
                }
                """
            )
            restore_button.clicked.connect(
                lambda checked, task_id=task.id: self.task_restored.emit(task_id)
            )

            # Add restore button to task widget layout
            task_widget.layout().addWidget(restore_button)

            self.content_layout.addWidget(task_widget)

        self.content_layout.addStretch()

    def _clear_content(self) -> None:
        """Clear all content widgets."""
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()