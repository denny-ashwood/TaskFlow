"""
Search bar widget.
"""

import logging
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
)

logger = logging.getLogger(__name__)


class SearchBar(QWidget):
    """Search bar with integrated button."""

    search_requested = Signal(str)  # search query
    cleared = Signal()

    def __init__(self, placeholder: str = "Search tasks...", parent: Optional[QWidget] = None) -> None:
        """Initialize search bar."""
        super().__init__(parent)

        self._setup_ui(placeholder)

    def _setup_ui(self, placeholder: str) -> None:
        """Setup search bar UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(placeholder)
        self.search_input.returnPressed.connect(
            lambda: self.search_requested.emit(self.search_input.text())
        )
        self.search_input.textChanged.connect(self._on_text_changed)
        layout.addWidget(self.search_input)

        # Clear button
        self.clear_button = QPushButton("✕")
        self.clear_button.setFixedSize(24, 24)
        self.clear_button.setStyleSheet(
            "border: none; background: transparent; font-size: 14px;"
        )
        self.clear_button.clicked.connect(self._clear_search)
        self.clear_button.hide()
        layout.addWidget(self.clear_button)

    def _on_text_changed(self, text: str) -> None:
        """Handle text changes."""
        self.clear_button.setVisible(bool(text))

    def _clear_search(self) -> None:
        """Clear search input."""
        self.search_input.clear()
        self.cleared.emit()

    def get_text(self) -> str:
        """Get search text."""
        return self.search_input.text()

    def set_text(self, text: str) -> None:
        """Set search text."""
        self.search_input.setText(text)

    def clear(self) -> None:
        """Clear search."""
        self.search_input.clear()