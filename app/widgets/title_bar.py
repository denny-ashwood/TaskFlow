"""
Custom title bar widget.
"""

import logging
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)

from app.config.constants import APP_NAME

logger = logging.getLogger(__name__)


class TitleBar(QFrame):
    """Custom title bar with centered title."""

    minimize_requested = Signal()
    maximize_requested = Signal()
    close_requested = Signal()

    def __init__(
        self,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Initialize title bar.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)
        self.setObjectName("titleBar")
        self.setFixedHeight(40)

        self._setup_ui()
        self._setup_dragging()

    def _setup_ui(self) -> None:
        """Setup title bar UI."""
        # Set dark background
        self.setStyleSheet("""
            #titleBar {
                background-color: #1a1a2e;
                border-bottom: 1px solid #2a2a3e;
            }
            #titleBar QLabel {
                color: #ffffff;
            }
            #titleBar QLabel#titleLabel {
                font-weight: 600;
                font-size: 14px;
                letter-spacing: 1px;
            }
            #titleBar QPushButton {
                background-color: transparent;
                border: none;
                color: #ffffff;
                padding: 8px 12px;
                font-size: 14px;
            }
            #titleBar QPushButton:hover {
                background-color: #2a2a3e;
            }
            #titleBar QPushButton#closeButton:hover {
                background-color: #e81123;
                color: white;
            }
        """)

        # Main layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Left spacer (for symmetry)
        left_spacer = QWidget()
        left_spacer.setFixedWidth(120)  # Space for window controls
        layout.addWidget(left_spacer)

        # Centered title
        layout.addStretch()

        self.title_label = QLabel(APP_NAME)
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label, alignment=Qt.AlignCenter)

        layout.addStretch()

        # Window control buttons (right side)
        self.minimize_button = QPushButton("─")
        self.minimize_button.setObjectName("minimizeButton")
        self.minimize_button.setFixedSize(40, 40)
        self.minimize_button.setToolTip("Minimize")
        self.minimize_button.clicked.connect(self.minimize_requested.emit)
        layout.addWidget(self.minimize_button)

        self.maximize_button = QPushButton("□")
        self.maximize_button.setObjectName("maximizeButton")
        self.maximize_button.setFixedSize(40, 40)
        self.maximize_button.setToolTip("Maximize/Restore")
        self.maximize_button.clicked.connect(self.maximize_requested.emit)
        layout.addWidget(self.maximize_button)

        self.close_button = QPushButton("✕")
        self.close_button.setObjectName("closeButton")
        self.close_button.setFixedSize(40, 40)
        self.close_button.setToolTip("Close")
        self.close_button.clicked.connect(self.close_requested.emit)
        layout.addWidget(self.close_button)

        # Right spacer (for symmetry)
        right_spacer = QWidget()
        right_spacer.setFixedWidth(0)
        layout.addWidget(right_spacer)

    def _setup_dragging(self) -> None:
        """Setup window dragging."""
        self._drag_position = None
        self._is_dragging = False

    def mousePressEvent(self, event) -> None:
        """Handle mouse press for dragging."""
        if event.button() == Qt.LeftButton:
            self._drag_position = event.globalPosition().toPoint()
            self._is_dragging = True
            event.accept()

    def mouseMoveEvent(self, event) -> None:
        """Handle mouse move for dragging."""
        if self._is_dragging and self._drag_position:
            if event.buttons() & Qt.LeftButton:
                window = self.window()
                if window:
                    delta = event.globalPosition().toPoint() - self._drag_position
                    window.move(window.pos() + delta)
                    self._drag_position = event.globalPosition().toPoint()
                    event.accept()

    def mouseReleaseEvent(self, event) -> None:
        """Handle mouse release for dragging."""
        self._is_dragging = False
        event.accept()

    def mouseDoubleClickEvent(self, event) -> None:
        """Handle double click for maximize/restore."""
        if event.button() == Qt.LeftButton:
            self.maximize_requested.emit()
            event.accept()