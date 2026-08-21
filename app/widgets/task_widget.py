"""
Task widget with Material Icons.
"""

import logging
from typing import Optional

from PySide6.QtCore import Qt, Signal, QPoint, QSize
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
from app.ui.material_icons import MaterialIcons

logger = logging.getLogger(__name__)


class TaskWidget(QFrame):
    """Widget for displaying a single task."""

    completed = Signal(int)
    edit_requested = Signal(int)
    delete_requested = Signal(int)
    clicked = Signal(int)

    def __init__(
        self,
        task: Task,
        show_checkbox: bool = True,
        parent: Optional[QWidget] = None,
    ) -> None:
        """Initialize task widget."""
        super().__init__(parent)
        self.task = task
        self.setObjectName("taskWidget")
        self.setCursor(Qt.PointingHandCursor)

        # Enable context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

        self._setup_ui(show_checkbox)

    def _setup_ui(self, show_checkbox: bool) -> None:
        """Setup widget UI."""
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
            self.checkbox.stateChanged.connect(self._on_checkbox_changed)
            layout.addWidget(self.checkbox, alignment=Qt.AlignTop)

        # Task info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)

        self.title_label = QLabel(self.task.title)
        self.title_label.setStyleSheet("font-weight: 600; font-size: 13px;")
        self.title_label.setWordWrap(True)
        info_layout.addWidget(self.title_label)

        if self.task.description:
            description = self.task.description[:60]
            self.description_label = QLabel(description)
            self.description_label.setStyleSheet(
                "font-size: 11px; color: gray;")
            info_layout.addWidget(self.description_label)

        layout.addLayout(info_layout, stretch=1)

        # Right side info with Material Icons
        if self.task.due_time:
            time_str = self.task.due_time.strftime("%I:%M %p")
            time_label = QLabel()
            time_label.setPixmap(
                MaterialIcons.create_pixmap('schedule', 14, "#666666")
            )
            time_text = QLabel(time_str)
            time_text.setStyleSheet("font-size: 11px; color: #666666;")

            time_layout = QHBoxLayout()
            time_layout.setSpacing(4)
            time_layout.addWidget(time_label)
            time_layout.addWidget(time_text)
            layout.addLayout(time_layout)

        # Priority with Material Icon
        priority_badge = self._create_priority_badge()
        layout.addWidget(priority_badge)

        # Category badge
        if self.task.category:
            category_badge = self._create_category_badge()
            layout.addWidget(category_badge)

        # More menu button with Material Icon
        self.menu_button = QPushButton()
        self.menu_button.setFixedSize(28, 28)
        self.menu_button.setToolTip("More options")
        self.menu_button.setIcon(
            MaterialIcons.create_icon('more_vert', 20, "#666666")
        )
        self.menu_button.setIconSize(QSize(20, 20))
        self.menu_button.clicked.connect(self._show_menu)
        layout.addWidget(self.menu_button)

    def _create_priority_badge(self) -> QWidget:
        """Create priority badge with icon."""
        badge_widget = QWidget()
        badge_layout = QHBoxLayout(badge_widget)
        badge_layout.setContentsMargins(4, 2, 4, 2)
        badge_layout.setSpacing(2)

        # Priority icon
        icon_label = QLabel()
        if self.task.priority == PRIORITY_HIGH:
            icon_label.setPixmap(
                MaterialIcons.create_pixmap('priority_high', 12, "#93000a")
            )
            badge_widget.setStyleSheet(
                "background-color: #ffdad6; border-radius: 4px;"
            )
        elif self.task.priority == PRIORITY_MEDIUM:
            icon_label.setPixmap(
                MaterialIcons.create_pixmap('flag', 12, "#a33200")
            )
            badge_widget.setStyleSheet(
                "background-color: #fff3e0; border-radius: 4px;"
            )
        else:
            icon_label.setPixmap(
                MaterialIcons.create_pixmap('flag', 12, "#1b5e20")
            )
            badge_widget.setStyleSheet(
                "background-color: #e8f5e9; border-radius: 4px;"
            )

        badge_layout.addWidget(icon_label)

        # Priority text
        text_label = QLabel(self.task.priority.upper())
        text_label.setStyleSheet("font-size: 10px; font-weight: 600;")
        badge_layout.addWidget(text_label)

        return badge_widget

    def _create_category_badge(self) -> QWidget:
        """Create category badge with icon."""
        badge_widget = QWidget()
        badge_layout = QHBoxLayout(badge_widget)
        badge_layout.setContentsMargins(4, 2, 4, 2)
        badge_layout.setSpacing(2)

        # Folder icon
        icon_label = QLabel()
        icon_label.setPixmap(
            MaterialIcons.create_pixmap('folder', 12, "#666666")
        )
        badge_layout.addWidget(icon_label)

        # Category name
        text_label = QLabel(self.task.category.name)
        text_label.setStyleSheet("font-size: 10px; color: #666666;")
        badge_layout.addWidget(text_label)

        badge_widget.setStyleSheet(
            "background-color: #f0f0f0; border-radius: 4px;"
        )

        return badge_widget

    def _on_checkbox_changed(self, state: int) -> None:
        """Handle checkbox state change."""
        if state == Qt.Checked:
            self.completed.emit(self.task.id)
            self.title_label.setStyleSheet(
                "font-weight: 600; font-size: 13px; "
                "text-decoration: line-through; color: #888888;"
            )

    def _show_menu(self) -> None:
        """Show context menu."""
        self._create_and_show_menu(
            self.menu_button.mapToGlobal(self.menu_button.rect().bottomLeft())
        )

    def _show_context_menu(self, pos: QPoint) -> None:
        """Show context menu on right-click."""
        self._create_and_show_menu(self.mapToGlobal(pos))

    def _create_and_show_menu(self, position) -> None:
        """Create and show context menu."""
        menu = QMenu(self)

        # Complete option with Material Icon
        if not self.task.is_completed:
            complete_action = menu.addAction(
                MaterialIcons.create_icon('check_circle', 18, "#00a862"),
                "Mark Complete"
            )
            complete_action.triggered.connect(
                lambda: self.completed.emit(self.task.id)
            )

        menu.addSeparator()

        # Edit option
        edit_action = menu.addAction(
            MaterialIcons.create_icon('edit', 18, "#0050cb"),
            "Edit"
        )
        edit_action.triggered.connect(
            lambda: self.edit_requested.emit(self.task.id)
        )

        # Delete option
        delete_action = menu.addAction(
            MaterialIcons.create_icon('delete', 18, "#ba1a1a"),
            "Delete"
        )
        delete_action.triggered.connect(
            lambda: self.delete_requested.emit(self.task.id)
        )

        menu.exec(position)
