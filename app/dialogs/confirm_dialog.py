"""
Confirmation dialog for destructive actions.
"""

import logging
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)


class ConfirmDialog(QDialog):
    """Dialog for confirming destructive actions."""

    def __init__(
        self,
        title: str,
        message: str,
        confirm_text: str = "Confirm",
        cancel_text: str = "Cancel",
        destructive: bool = True,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Initialize confirmation dialog.

        Args:
            title: Dialog title
            message: Confirmation message
            confirm_text: Text for confirm button
            cancel_text: Text for cancel button
            destructive: If True, use destructive styling
            parent: Parent widget
        """
        super().__init__(parent)

        self._setup_ui(
            title,
            message,
            confirm_text,
            cancel_text,
            destructive,
        )

    def _setup_ui(
        self,
        title: str,
        message: str,
        confirm_text: str,
        cancel_text: str,
        destructive: bool,
    ) -> None:
        """Setup dialog UI."""
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(400)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)

        # Message
        message_label = QLabel(message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("font-size: 14px;")
        main_layout.addWidget(message_label)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # Cancel button
        cancel_button = QPushButton(cancel_text)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        # Confirm button
        confirm_button = QPushButton(confirm_text)

        if destructive:
            confirm_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #ba1a1a;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
                """
            )
        else:
            confirm_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #0050cb;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: #0066ff;
                }
                """
            )

        confirm_button.clicked.connect(self.accept)
        button_layout.addWidget(confirm_button)

        main_layout.addLayout(button_layout)