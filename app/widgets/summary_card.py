"""
Summary card widget for displaying statistics.
"""

import logging
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)


class SummaryCard(QFrame):
    """Card widget for displaying summary statistics."""

    clicked = Signal()

    def __init__(
        self,
        title: str,
        value: str,
        icon: Optional[str] = None,
        color: str = "#0050cb",
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Initialize summary card.

        Args:
            title: Card title
            value: Card value
            icon: Icon name (optional)
            color: Accent color
            parent: Parent widget
        """
        super().__init__(parent)
        self.setObjectName("summaryCard")
        self.setProperty("class", "summary-card")
        self.setCursor(Qt.PointingHandCursor)

        # Store properties
        self._title = title
        self._value = value
        self._color = color

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup card UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)

        # Title label
        self.title_label = QLabel(self._title.upper())
        self.title_label.setStyleSheet(
            f"font-size: 11px; font-weight: 600; color: {self._color};"
        )
        layout.addWidget(self.title_label)

        # Value label
        self.value_label = QLabel(str(self._value))
        self.value_label.setStyleSheet(
            "font-size: 28px; font-weight: 700;"
        )
        layout.addWidget(self.value_label)

    def update_value(self, value: str) -> None:
        """Update card value."""
        self._value = value
        self.value_label.setText(str(value))

    def mousePressEvent(self, event) -> None:
        """Handle mouse press."""
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
