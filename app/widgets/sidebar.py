"""
Sidebar navigation widget.
"""

import logging
from typing import List, Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)


class Sidebar(QFrame):
    """Sidebar navigation widget."""

    navigation_changed = Signal(str)  # view name

    NAV_ITEMS = [
        ('dashboard', 'Dashboard', '📊'),
        ('today', 'Today', '📅'),
        ('upcoming', 'Upcoming', '📈'),
        ('overdue', 'Overdue', '⚠️'),
        ('completed', 'Completed', '✅'),
        ('calendar', 'Calendar', '🗓️'),
    ]

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        """Initialize sidebar."""
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(220)

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup sidebar UI."""
        # Set sidebar style
        self.setStyleSheet("""
            #sidebar {
                background-color: #1a1a2e;
                border-right: 1px solid #2a2a3e;
            }
            #sidebar QLabel {
                color: #ffffff;
            }
            #sidebar QLabel#appTitle {
                font-size: 20px;
                font-weight: 700;
                color: #ffffff;
                padding: 16px 16px 8px 16px;
            }
            #sidebar QLabel#sectionLabel {
                font-size: 10px;
                font-weight: 600;
                color: #888888;
                padding: 16px 16px 4px 16px;
                text-transform: uppercase;
            }
            #sidebar QPushButton {
                text-align: left;
                padding: 10px 16px;
                border: none;
                border-radius: 8px;
                color: #cccccc;
                background: transparent;
                font-weight: 500;
                font-size: 13px;
            }
            #sidebar QPushButton:hover {
                background-color: #2a2a3e;
                color: #ffffff;
            }
            #sidebar QPushButton:checked {
                background-color: #0f3460;
                color: #ffffff;
                font-weight: 600;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(2)

        # App title
        title_label = QLabel("📋 TaskFlow")
        title_label.setObjectName("appTitle")
        layout.addWidget(title_label)

        # Navigation section label
        nav_label = QLabel("General")
        nav_label.setObjectName("sectionLabel")
        layout.addWidget(nav_label)

        # Navigation buttons
        self.button_group = QButtonGroup(self)
        self.button_group.setExclusive(True)

        self.nav_buttons = {}
        for view_name, display_name, icon in self.NAV_ITEMS:
            button = QPushButton(f"  {icon}  {display_name}")
            button.setCheckable(True)
            button.setProperty('view_name', view_name)
            button.clicked.connect(
                lambda checked, v=view_name: self.navigation_changed.emit(v)
            )

            self.button_group.addButton(button)
            self.nav_buttons[view_name] = button
            layout.addWidget(button)

        # Settings section
        settings_label = QLabel("Preferences")
        settings_label.setObjectName("sectionLabel")
        layout.addWidget(settings_label)

        settings_button = QPushButton("  ⚙️  Settings")
        settings_button.setCheckable(True)
        settings_button.setProperty('view_name', 'settings')
        settings_button.clicked.connect(
            lambda: self.navigation_changed.emit('settings')
        )
        self.button_group.addButton(settings_button)
        self.nav_buttons['settings'] = settings_button
        layout.addWidget(settings_button)

        layout.addStretch()

        # User info at bottom
        user_frame = QFrame()
        user_frame.setStyleSheet("""
            QFrame {
                background-color: #2a2a3e;
                border-radius: 8px;
                padding: 8px;
            }
            QLabel {
                color: #ffffff;
                font-size: 12px;
            }
        """)

        user_layout = QVBoxLayout(user_frame)
        user_layout.setContentsMargins(8, 8, 8, 8)
        user_layout.setSpacing(2)

        user_name = QLabel("👤 S'fisokuhle")
        user_name.setStyleSheet("font-weight: 600;")
        user_layout.addWidget(user_name)

        user_email = QLabel("sfiso@za.d-teksolutions.com")
        user_email.setStyleSheet("color: #888888; font-size: 10px;")
        user_layout.addWidget(user_email)

        layout.addWidget(user_frame)

    def set_active(self, view_name: str) -> None:
        """Set active navigation item."""
        if view_name in self.nav_buttons:
            self.nav_buttons[view_name].setChecked(True)
