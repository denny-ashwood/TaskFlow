"""
Theme management for TaskFlow application.
"""

import logging
from enum import Enum
from typing import Dict, Optional

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

logger = logging.getLogger(__name__)


class ThemeMode(Enum):
    """Theme modes."""
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


class ThemeManager:
    """Manages application theming."""

    # Color palette for light theme
    LIGHT_PALETTE = {
        'primary': '#0050cb',
        'primary_container': '#0066ff',
        'on_primary': '#ffffff',
        'secondary': '#505f76',
        'secondary_container': '#d0e1fb',
        'on_secondary_container': '#0b1c30',
        'background': '#f7f9fb',
        'surface': '#f7f9fb',
        'surface_container': '#eceef0',
        'surface_container_low': '#f2f4f6',
        'surface_container_lowest': '#ffffff',
        'surface_container_high': '#e6e8ea',
        'on_surface': '#191c1e',
        'on_surface_variant': '#424656',
        'outline': '#727687',
        'outline_variant': '#c2c6d8',
        'error': '#ba1a1a',
        'error_container': '#ffdad6',
        'on_error_container': '#93000a',
        'tertiary': '#a33200',
        'tertiary_container': '#cc4204',
        'on_tertiary_container': '#fff6f4',
    }

    # Color palette for dark theme
    DARK_PALETTE = {
        'primary': '#b3c5ff',
        'primary_container': '#003fa4',
        'on_primary': '#001849',
        'secondary': '#b7c8e1',
        'secondary_container': '#38485d',
        'on_secondary_container': '#d3e4fe',
        'background': '#1a1c1e',
        'surface': '#1a1c1e',
        'surface_container': '#2d3133',
        'surface_container_low': '#26292b',
        'surface_container_lowest': '#1a1c1e',
        'surface_container_high': '#333739',
        'on_surface': '#e2e2e6',
        'on_surface_variant': '#c4c6d0',
        'outline': '#8e9099',
        'outline_variant': '#44474e',
        'error': '#ffb4ab',
        'error_container': '#93000a',
        'on_error_container': '#ffdad6',
        'tertiary': '#ffb59d',
        'tertiary_container': '#832600',
        'on_tertiary_container': '#ffdbd0',
    }

    def __init__(self) -> None:
        self._current_mode: ThemeMode = ThemeMode.LIGHT
        self._current_palette: Dict[str, str] = self.LIGHT_PALETTE

    @property
    def current_mode(self) -> ThemeMode:
        """Get current theme mode."""
        return self._current_mode

    @property
    def palette(self) -> Dict[str, str]:
        """Get current color palette."""
        return self._current_palette

    def set_theme(self, mode: str) -> None:
        """
        Set theme mode.

        Args:
            mode: Theme mode ('light', 'dark', or 'system')
        """
        try:
            self._current_mode = ThemeMode(mode)
        except ValueError:
            logger.warning(f"Invalid theme mode: {mode}, using light")
            self._current_mode = ThemeMode.LIGHT

        self._apply_theme()
        logger.info(f"Theme set to {self._current_mode.value}")

    def _apply_theme(self) -> None:
        """Apply current theme to application."""
        if self._current_mode == ThemeMode.SYSTEM:
            # Detect system theme
            system_theme = self._detect_system_theme()
            self._current_palette = (
                self.DARK_PALETTE if system_theme == 'dark' else self.LIGHT_PALETTE
            )
        elif self._current_mode == ThemeMode.DARK:
            self._current_palette = self.DARK_PALETTE
        else:
            self._current_palette = self.LIGHT_PALETTE

        # Apply to QApplication
        app = QApplication.instance()
        if app:
            app.setPalette(self._create_qt_palette())
            app.setStyleSheet(self._generate_stylesheet())

    def _detect_system_theme(self) -> str:
        """Detect system theme preference."""
        # This is a simplified detection; in production, use platform-specific APIs
        import os
        if os.name == 'nt':  # Windows
            import winreg
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
                )
                value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                winreg.CloseKey(key)
                return 'light' if value == 1 else 'dark'
            except:
                return 'light'
        elif os.name == 'posix':  # macOS/Linux
            # Check common environment variables
            if 'GTK_THEME' in os.environ:
                return 'dark' if 'dark' in os.environ['GTK_THEME'].lower() else 'light'
            # Default to light
            return 'light'
        return 'light'

    def _create_qt_palette(self) -> QPalette:
        """Create Qt palette from current colors."""
        palette = QPalette()

        # Convert hex to QColor
        def hex_to_qcolor(hex_color: str) -> QColor:
            return QColor(hex_color)

        # Set palette colors
        palette.setColor(QPalette.Window, hex_to_qcolor(
            self._current_palette['background']))
        palette.setColor(QPalette.WindowText, hex_to_qcolor(
            self._current_palette['on_surface']))
        palette.setColor(QPalette.Base, hex_to_qcolor(
            self._current_palette['surface_container_lowest']))
        palette.setColor(QPalette.AlternateBase, hex_to_qcolor(
            self._current_palette['surface_container']))
        palette.setColor(QPalette.ToolTipBase, hex_to_qcolor(
            self._current_palette['surface_container_high']))
        palette.setColor(QPalette.ToolTipText, hex_to_qcolor(
            self._current_palette['on_surface']))
        palette.setColor(QPalette.Text, hex_to_qcolor(
            self._current_palette['on_surface']))
        palette.setColor(QPalette.Button, hex_to_qcolor(
            self._current_palette['surface_container']))
        palette.setColor(QPalette.ButtonText, hex_to_qcolor(
            self._current_palette['on_surface']))
        palette.setColor(QPalette.Highlight, hex_to_qcolor(
            self._current_palette['primary']))
        palette.setColor(QPalette.HighlightedText, hex_to_qcolor(
            self._current_palette['on_primary']))

        return palette

    def _generate_stylesheet(self) -> str:
        """Generate Qt stylesheet from current palette."""
        p = self._current_palette

        return f"""
        /* Global styles */
        QWidget {{
            font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', sans-serif;
            font-size: 14px;
            color: {p['on_surface']};
        }}

        /* Main window */
        QMainWindow {{
            background-color: {p['background']};
        }}

        /* Sidebar */
        #sidebar {{
            background-color: {p['surface_container_lowest']};
            border-right: 1px solid {p['outline_variant']};
        }}

        #sidebar QPushButton {{
            text-align: left;
            padding: 10px 16px;
            border: none;
            border-radius: 8px;
            color: {p['on_surface_variant']};
            background: transparent;
            font-weight: 500;
        }}

        #sidebar QPushButton:hover {{
            background-color: {p['surface_container_high']};
            color: {p['on_surface']};
        }}

        #sidebar QPushButton:checked {{
            background-color: {p['secondary_container']};
            color: {p['on_secondary_container']};
            font-weight: 600;
        }}

        /* Header */
        #header {{
            background-color: rgba(255, 255, 255, 0.8);
            border-bottom: 1px solid {p['outline_variant']};
        }}

        /* Cards */
        .card {{
            background-color: {p['surface_container_lowest']};
            border: 1px solid {p['outline_variant']};
            border-radius: 12px;
            padding: 20px;
        }}

        .summary-card {{
            background-color: {p['surface_container']};
            border-radius: 12px;
            padding: 16px;
        }}

        /* Buttons */
        QPushButton {{
            padding: 8px 16px;
            border-radius: 6px;
            border: 1px solid {p['outline_variant']};
            background-color: {p['surface_container']};
            color: {p['on_surface']};
        }}

        QPushButton:hover {{
            background-color: {p['surface_container_high']};
        }}

        QPushButton:primary {{
            background-color: {p['primary']};
            color: {p['on_primary']};
            border: none;
            font-weight: 600;
        }}

        QPushButton:primary:hover {{
            background-color: {p['primary_container']};
        }}

        /* Input fields */
        QLineEdit, QTextEdit, QDateEdit, QTimeEdit, QComboBox {{
            background-color: {p['surface_container_lowest']};
            border: 1px solid {p['outline_variant']};
            border-radius: 6px;
            padding: 8px;
            color: {p['on_surface']};
        }}

        QLineEdit:focus, QTextEdit:focus, QDateEdit:focus, QTimeEdit:focus, QComboBox:focus {{
            border: 2px solid {p['primary']};
        }}

        /* Lists */
        QListWidget {{
            background-color: transparent;
            border: none;
        }}

        QListWidget::item {{
            padding: 8px;
            border-radius: 8px;
        }}

        QListWidget::item:hover {{
            background-color: {p['surface_container_low']};
        }}

        QListWidget::item:selected {{
            background-color: {p['secondary_container']};
            color: {p['on_secondary_container']};
        }}

        /* Scrollbars */
        QScrollBar:vertical {{
            background: transparent;
            width: 10px;
            margin: 0;
        }}

        QScrollBar::handle:vertical {{
            background: {p['outline_variant']};
            border-radius: 5px;
            min-height: 20px;
        }}

        QScrollBar::handle:vertical:hover {{
            background: {p['outline']};
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}

        QScrollBar:horizontal {{
            background: transparent;
            height: 10px;
            margin: 0;
        }}

        QScrollBar::handle:horizontal {{
            background: {p['outline_variant']};
            border-radius: 5px;
            min-width: 20px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background: {p['outline']};
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0;
        }}

        /* Calendar */
        #calendarWidget {{
            background-color: {p['surface_container_lowest']};
            border: 1px solid {p['outline_variant']};
            border-radius: 12px;
        }}

        #calendarWidget QToolButton {{
            background-color: transparent;
            border: none;
            padding: 8px;
            border-radius: 6px;
        }}

        #calendarWidget QToolButton:hover {{
            background-color: {p['surface_container_high']};
        }}

        #calendarWidget QAbstractItemView {{
            background-color: {p['surface_container_lowest']};
            border: none;
        }}

        /* Task widget */
        .task-widget {{
            background-color: {p['surface_container_lowest']};
            border: 1px solid {p['outline_variant']};
            border-radius: 8px;
            padding: 12px;
        }}

        .task-widget:hover {{
            border-color: {p['primary']};
            background-color: {p['surface_container_low']};
        }}

        .priority-high {{
            background-color: {p['error_container']};
            color: {p['on_error_container']};
            border-radius: 4px;
            padding: 2px 8px;
            font-size: 11px;
            font-weight: 600;
        }}

        .priority-medium {{
            background-color: {p['secondary_container']};
            color: {p['on_secondary_container']};
            border-radius: 4px;
            padding: 2px 8px;
            font-size: 11px;
            font-weight: 600;
        }}

        .priority-low {{
            background-color: {p['surface_container_high']};
            color: {p['on_surface_variant']};
            border-radius: 4px;
            padding: 2px 8px;
            font-size: 11px;
            font-weight: 600;
        }}

        .category-badge {{
            background-color: {p['surface_container_high']};
            color: {p['on_surface_variant']};
            border-radius: 4px;
            padding: 2px 8px;
            font-size: 11px;
        }}

        /* Empty state */
        .empty-state {{
            color: {p['on_surface_variant']};
            font-size: 16px;
        }}

        .empty-state-icon {{
            font-size: 48px;
            color: {p['outline_variant']};
        }}

        /* Dialogs */
        QDialog {{
            background-color: {p['surface_container_lowest']};
        }}

        QDialog QLabel {{
            color: {p['on_surface']};
        }}

        /* Menu */
        QMenu {{
            background-color: {p['surface_container_lowest']};
            border: 1px solid {p['outline_variant']};
            border-radius: 8px;
            padding: 4px;
        }}

        QMenu::item {{
            padding: 8px 16px;
            border-radius: 4px;
        }}

        QMenu::item:selected {{
            background-color: {p['secondary_container']};
            color: {p['on_secondary_container']};
        }}

        /* Tooltips */
        QToolTip {{
            background-color: {p['surface_container_high']};
            color: {p['on_surface']};
            border: 1px solid {p['outline_variant']};
            border-radius: 4px;
            padding: 4px 8px;
        }}
        """
