"""
Empty state widget for displaying placeholder content.
"""

import logging
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)


class EmptyState(QWidget):
    """Widget for displaying empty states."""

    action_clicked = Signal()

    def __init__(
        self,
        message: str,
        icon: str = "📋",
        action_text: Optional[str] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Initialize empty state.

        Args:
            message: Main message to display
            icon: Icon emoji
            action_text: Optional action button text
            parent: Parent widget
        """
        super().__init__(parent)

        self._setup_ui(message, icon, action_text)

    def _setup_ui(
        self,
        message: str,
        icon: str,
        action_text: Optional[str],
    ) -> None:
        """Setup empty state UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignCenter)

        # Icon label
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 48px;")
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)

        # Message label
        message_label = QLabel(message)
        message_label.setStyleSheet(
            "font-size: 16px; color: gray;"
        )
        message_label.setAlignment(Qt.AlignCenter)
        message_label.setWordWrap(True)
        layout.addWidget(message_label)

        # Action button (optional)
        if action_text:
            action_button = QPushButton(action_text)
            action_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #0050cb;
                    color: white;
                    border: none;
                    border-radius: 20px;
                    padding: 10px 24px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #0066ff;
                }
                """
            )
            action_button.clicked.connect(self.action_clicked.emit)
            layout.addWidget(action_button, alignment=Qt.AlignCenter)