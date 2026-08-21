"""
Settings view implementation.
"""

import logging
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.services.settings_service import SettingsService

logger = logging.getLogger(__name__)


class SettingsView(QWidget):
    """Settings view for application preferences."""

    settings_changed = Signal()

    def __init__(
        self,
        settings_service: SettingsService,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Initialize settings view.

        Args:
            settings_service: Settings service instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.settings_service = settings_service

        self._setup_ui()
        self._load_settings()

    def _setup_ui(self) -> None:
        """Setup settings view UI."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Header
        self.title_label = QLabel("Settings")
        self.title_label.setStyleSheet(
            "font-size: 28px; font-weight: 700;"
        )
        main_layout.addWidget(self.title_label)

        # Scrollable content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("border: none; background: transparent;")

        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(20)

        scroll_area.setWidget(self.content_widget)
        main_layout.addWidget(scroll_area)

        # Notifications section
        self._setup_notifications_section()

        # Appearance section
        self._setup_appearance_section()

        # Task defaults section
        self._setup_task_defaults_section()

        # Application section
        self._setup_application_section()

        # Save button
        save_button = QPushButton("Save Settings")
        save_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0050cb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0066ff;
            }
            """
        )
        save_button.clicked.connect(self._save_settings)
        self.content_layout.addWidget(save_button)

        self.content_layout.addStretch()

    def _setup_notifications_section(self) -> None:
        """Setup notifications settings."""
        group = QGroupBox("Notifications")
        group.setStyleSheet(
            """
            QGroupBox {
                font-weight: 600;
                font-size: 16px;
                border: 1px solid #e0e3e5;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
            }
            """
        )

        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        # Enable notifications
        self.enable_notifications = QCheckBox("Enable notifications")
        self.enable_notifications.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.enable_notifications)

        # Default reminder time
        reminder_layout = QHBoxLayout()
        reminder_label = QLabel("Default reminder time:")
        reminder_label.setStyleSheet("font-size: 14px;")
        reminder_layout.addWidget(reminder_label)

        self.default_reminder = QComboBox()
        self.default_reminder.addItem("5 minutes before", 5)
        self.default_reminder.addItem("10 minutes before", 10)
        self.default_reminder.addItem("15 minutes before", 15)
        self.default_reminder.addItem("30 minutes before", 30)
        self.default_reminder.addItem("1 hour before", 60)
        self.default_reminder.addItem("2 hours before", 120)
        reminder_layout.addWidget(self.default_reminder)
        reminder_layout.addStretch()
        layout.addLayout(reminder_layout)

        # Notification sound
        sound_layout = QHBoxLayout()
        sound_label = QLabel("Notification sound:")
        sound_label.setStyleSheet("font-size: 14px;")
        sound_layout.addWidget(sound_label)

        self.notification_sound = QComboBox()
        self.notification_sound.addItem("Soft Chime", "chime")
        self.notification_sound.addItem("Digital Bell", "bell")
        self.notification_sound.addItem("Pop", "pop")
        self.notification_sound.addItem("None", "none")
        sound_layout.addWidget(self.notification_sound)
        sound_layout.addStretch()
        layout.addLayout(sound_layout)

        self.content_layout.addWidget(group)

    def _setup_appearance_section(self) -> None:
        """Setup appearance settings."""
        group = QGroupBox("Appearance")
        group.setStyleSheet(
            """
            QGroupBox {
                font-weight: 600;
                font-size: 16px;
                border: 1px solid #e0e3e5;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
            }
            """
        )

        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        # Theme selection
        theme_layout = QHBoxLayout()
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("font-size: 14px;")
        theme_layout.addWidget(theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Light", "light")
        self.theme_combo.addItem("Dark", "dark")
        self.theme_combo.addItem("System Default", "system")
        theme_layout.addWidget(self.theme_combo)
        theme_layout.addStretch()
        layout.addLayout(theme_layout)

        self.content_layout.addWidget(group)

    def _setup_task_defaults_section(self) -> None:
        """Setup task defaults settings."""
        group = QGroupBox("Task Defaults")
        group.setStyleSheet(
            """
            QGroupBox {
                font-weight: 600;
                font-size: 16px;
                border: 1px solid #e0e3e5;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
            }
            """
        )

        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        # Default priority
        priority_layout = QHBoxLayout()
        priority_label = QLabel("Default priority:")
        priority_label.setStyleSheet("font-size: 14px;")
        priority_layout.addWidget(priority_label)

        self.default_priority = QComboBox()
        self.default_priority.addItem("Low", "low")
        self.default_priority.addItem("Medium", "medium")
        self.default_priority.addItem("High", "high")
        priority_layout.addWidget(self.default_priority)
        priority_layout.addStretch()
        layout.addLayout(priority_layout)

        self.content_layout.addWidget(group)

    def _setup_application_section(self) -> None:
        """Setup application settings."""
        group = QGroupBox("Application")
        group.setStyleSheet(
            """
            QGroupBox {
                font-weight: 600;
                font-size: 16px;
                border: 1px solid #e0e3e5;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
            }
            """
        )

        layout = QVBoxLayout(group)
        layout.setSpacing(12)

        # Start with system
        self.start_with_system = QCheckBox("Start application with system")
        self.start_with_system.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.start_with_system)

        # Minimize to tray
        self.minimize_to_tray = QCheckBox("Minimize to system tray")
        self.minimize_to_tray.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.minimize_to_tray)

        # Close to tray
        self.close_to_tray = QCheckBox("Close to tray instead of quitting")
        self.close_to_tray.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.close_to_tray)

        self.content_layout.addWidget(group)

    def _load_settings(self) -> None:
        """Load current settings into UI."""
        # Notifications
        self.enable_notifications.setChecked(
            self.settings_service.get('notifications_enabled', True)
        )

        default_reminder = self.settings_service.get('default_reminder', 15)
        index = self.default_reminder.findData(default_reminder)
        if index >= 0:
            self.default_reminder.setCurrentIndex(index)

        notification_sound = self.settings_service.get(
            'notification_sound', 'chime')
        index = self.notification_sound.findData(notification_sound)
        if index >= 0:
            self.notification_sound.setCurrentIndex(index)

        # Appearance
        theme = self.settings_service.get('theme', 'light')
        index = self.theme_combo.findData(theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)

        # Task defaults
        default_priority = self.settings_service.get(
            'default_priority', 'medium')
        index = self.default_priority.findData(default_priority)
        if index >= 0:
            self.default_priority.setCurrentIndex(index)

        # Application
        self.start_with_system.setChecked(
            self.settings_service.get('start_with_system', False)
        )
        self.minimize_to_tray.setChecked(
            self.settings_service.get('minimize_to_tray', True)
        )
        self.close_to_tray.setChecked(
            self.settings_service.get('close_to_tray', True)
        )

    def _save_settings(self) -> None:
        """Save settings from UI."""
        settings = {
            'notifications_enabled': self.enable_notifications.isChecked(),
            'default_reminder': self.default_reminder.currentData(),
            'notification_sound': self.notification_sound.currentData(),
            'theme': self.theme_combo.currentData(),
            'default_priority': self.default_priority.currentData(),
            'start_with_system': self.start_with_system.isChecked(),
            'minimize_to_tray': self.minimize_to_tray.isChecked(),
            'close_to_tray': self.close_to_tray.isChecked(),
        }

        self.settings_service.update(settings)
        self.settings_changed.emit()
        logger.info("Settings saved")

    def refresh(self) -> None:
        """Refresh settings view."""
        self._load_settings()
