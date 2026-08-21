"""
Task widget for displaying individual tasks.
"""

import logging
from typing import Optional

from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtGui import QColor, QAction, QContextMenuEvent
from PySide6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMenu,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.config.constants import PRIORITY_HIGH, PRIORITY_MEDIUM
from app.models.task import Task

logger = logging.getLogger(__name__)


class TaskWidget(QFrame):
    """Widget for displaying a single task."""

    completed = Signal(int)  # task_id
    edit_requested = Signal(int)  # task_id
    delete_requested = Signal(int)  # task_id
    clicked = Signal(int)  # task_id

    def __init__(
        self,
        task: Task,
        show_checkbox: bool = True,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Initialize task widget.

        Args:
            task: Task model instance
            show_checkbox: Whether to show completion checkbox
            parent: Parent widget
        """
        super().__init__(parent)
        self.task = task
        self.setObjectName("taskWidget")
        self.setProperty("class", "task-widget")
        self.setCursor(Qt.PointingHandCursor)

        # Enable context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

        self._setup_ui(show_checkbox)

    def _setup_ui(self, show_checkbox: bool) -> None:
        """Setup widget UI."""
        # Basic frame styling
        self.setStyleSheet("""
            #taskWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
            }
            #taskWidget:hover {
                border-color: #0050cb;
                background-color: #f8f9ff;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(8)

        # Completion checkbox
        if show_checkbox:
            self.checkbox = QCheckBox()
            self.checkbox.setChecked(self.task.is_completed)
            self.checkbox.setToolTip("Mark as completed")
            self.checkbox.setCursor(Qt.PointingHandCursor)
            self.checkbox.setStyleSheet("""
                QCheckBox {
                    spacing: 0px;
                }
                QCheckBox::indicator {
                    width: 18px;
                    height: 18px;
                    border-radius: 4px;
                    border: 2px solid #cccccc;
                    background: white;
                }
                QCheckBox::indicator:hover {
                    border-color: #0050cb;
                    background: #f0f6ff;
                }
                QCheckBox::indicator:checked {
                    background-color: #0050cb;
                    border-color: #0050cb;
                }
            """)
            self.checkbox.stateChanged.connect(self._on_checkbox_changed)
            layout.addWidget(self.checkbox, alignment=Qt.AlignTop)

        # Task info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        # Title
        self.title_label = QLabel(self.task.title)
        self.title_label.setStyleSheet(
            "font-weight: 600; font-size: 13px;"
        )
        self.title_label.setWordWrap(True)
        if self.task.is_completed:
            self.title_label.setStyleSheet(
                "font-weight: 600; font-size: 13px; "
                "text-decoration: line-through; color: #888888;"
            )
        info_layout.addWidget(self.title_label)

        # Description (if exists) - limit to 1 line
        if self.task.description:
            description = self.task.description[:60]
            if len(self.task.description) > 60:
                description += "..."
            self.description_label = QLabel(description)
            self.description_label.setStyleSheet(
                "font-size: 11px; color: gray;"
            )
            self.description_label.setWordWrap(False)
            info_layout.addWidget(self.description_label)

        layout.addLayout(info_layout, stretch=1)

        # Right side info
        right_layout = QVBoxLayout()
        right_layout.setSpacing(2)
        right_layout.setAlignment(Qt.AlignRight)

        # Due time
        if self.task.due_time:
            time_str = self.task.due_time.strftime("%I:%M %p")
            self.time_label = QLabel(f"🕐 {time_str}")
            self.time_label.setStyleSheet(
                "font-size: 11px; color: #666666;"
            )
            right_layout.addWidget(self.time_label)

        # Priority badge
        priority_badge = self._create_priority_badge()
        right_layout.addWidget(priority_badge, alignment=Qt.AlignRight)

        layout.addLayout(right_layout)

        # Category badge (if exists)
        if self.task.category:
            category_badge = QLabel(f"📁 {self.task.category.name}")
            category_badge.setStyleSheet(
                "background-color: #f0f0f0; "
                "color: #666666; "
                "border-radius: 4px; "
                "padding: 2px 6px; "
                "font-size: 10px;"
            )
            layout.addWidget(category_badge)

        # More menu button (three dots)
        self.menu_button = QPushButton("⋯")
        self.menu_button.setFixedSize(24, 24)
        self.menu_button.setToolTip("More options")
        self.menu_button.setCursor(Qt.PointingHandCursor)
        self.menu_button.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
                font-size: 16px;
                font-weight: bold;
                color: #666666;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                color: #0050cb;
            }
        """)
        self.menu_button.clicked.connect(self._show_menu)
        layout.addWidget(self.menu_button)

    def _create_priority_badge(self) -> QLabel:
        """Create priority badge label."""
        badge = QLabel(self.task.priority.upper())

        if self.task.priority == PRIORITY_HIGH:
            badge.setStyleSheet(
                "background-color: #ffdad6; "
                "color: #93000a; "
                "border-radius: 4px; "
                "padding: 1px 6px; "
                "font-size: 10px; "
                "font-weight: 600;"
            )
        elif self.task.priority == PRIORITY_MEDIUM:
            badge.setStyleSheet(
                "background-color: #fff3e0; "
                "color: #a33200; "
                "border-radius: 4px; "
                "padding: 1px 6px; "
                "font-size: 10px; "
                "font-weight: 600;"
            )
        else:
            badge.setStyleSheet(
                "background-color: #e8f5e9; "
                "color: #1b5e20; "
                "border-radius: 4px; "
                "padding: 1px 6px; "
                "font-size: 10px; "
                "font-weight: 600;"
            )

        return badge

    def _on_checkbox_changed(self, state: int) -> None:
        """Handle checkbox state change."""
        if state == Qt.Checked:
            logger.debug(f"Checkbox checked for task {self.task.id}")
            self.completed.emit(self.task.id)
            # Visual feedback
            self.title_label.setStyleSheet(
                "font-weight: 600; font-size: 13px; "
                "text-decoration: line-through; color: #888888;"
            )
        elif state == Qt.Unchecked:
            logger.debug(f"Checkbox unchecked for task {self.task.id}")

    def _show_menu(self) -> None:
        """Show context menu from three-dot button."""
        self._create_and_show_menu(self.menu_button.mapToGlobal(
            self.menu_button.rect().bottomLeft()
        ))

    def _show_context_menu(self, pos: QPoint) -> None:
        """Show context menu on right-click."""
        self._create_and_show_menu(self.mapToGlobal(pos))

    def _create_and_show_menu(self, position) -> None:
        """Create and show context menu."""
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 4px;
            }
            QMenu::item {
                padding: 8px 16px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background-color: #f0f6ff;
                color: #0050cb;
            }
        """)

        # Complete/Restore option
        if not self.task.is_completed:
            complete_action = menu.addAction("✓ Mark Complete")
            complete_action.triggered.connect(
                lambda: self._handle_complete()
            )
        else:
            restore_action = menu.addAction("↩ Restore Task")

        menu.addSeparator()

        # Edit option
        edit_action = menu.addAction("✎ Edit")
        edit_action.triggered.connect(
            lambda: self.edit_requested.emit(self.task.id)
        )

        # Delete option
        delete_action = menu.addAction("🗑 Delete")
        delete_action.triggered.connect(
            lambda: self.delete_requested.emit(self.task.id)
        )

        # Show menu
        menu.exec(position)

    def _handle_complete(self) -> None:
        """Handle complete action from menu."""
        if hasattr(self, 'checkbox'):
            self.checkbox.setChecked(True)
        self.completed.emit(self.task.id)

    def mousePressEvent(self, event) -> None:
        """Handle mouse press."""
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.task.id)
        super().mousePressEvent(event)

    def update_task(self, task: Task) -> None:
        """Update widget with new task data."""
        self.task = task
        self.title_label.setText(task.title)

        if hasattr(self, 'checkbox'):
            # Block signals temporarily to avoid loops
            self.checkbox.blockSignals(True)
            self.checkbox.setChecked(task.is_completed)
            self.checkbox.blockSignals(False)

        # Update styles
        if task.is_completed:
            self.title_label.setStyleSheet(
                "font-weight: 600; font-size: 13px; "
                "text-decoration: line-through; color: #888888;"
            )
        else:
            self.title_label.setStyleSheet(
                "font-weight: 600; font-size: 13px;"
            )