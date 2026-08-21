"""
Icon management for TaskFlow application.
"""

import logging
from pathlib import Path
from typing import Dict, Optional

from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import QSize

logger = logging.getLogger(__name__)


class IconManager:
    """Manages application icons."""

    # Map icon names to Material Symbols names
    ICON_MAP = {
        'dashboard': 'grid_view',
        'today': 'today',
        'upcoming': 'event_upcoming',
        'overdue': 'assignment_late',
        'completed': 'task_alt',
        'calendar': 'calendar_month',
        'settings': 'settings',
        'add': 'add',
        'search': 'search',
        'notifications': 'notifications',
        'person': 'person',
        'more': 'more_vert',
        'close': 'close',
        'edit': 'edit',
        'delete': 'delete',
        'check': 'check',
        'check_circle': 'check_circle',
        'schedule': 'schedule',
        'folder': 'folder',
        'priority_high': 'priority_high',
        'priority_medium': 'priority_medium',
        'priority_low': 'priority_low',
        'chevron_left': 'chevron_left',
        'chevron_right': 'chevron_right',
        'expand_more': 'expand_more',
    }

    def __init__(self) -> None:
        self._icons: Dict[str, QIcon] = {}
        self._load_icons()

    def _load_icons(self) -> None:
        """Load icons from assets or create fallback icons."""
        assets_dir = Path(__file__).parent.parent.parent / 'assets' / 'icons'

        for icon_name in self.ICON_MAP:
            icon_path = assets_dir / f"{icon_name}.png"

            if icon_path.exists():
                self._icons[icon_name] = QIcon(str(icon_path))
            else:
                # Create fallback icon using text emoji
                self._icons[icon_name] = self._create_fallback_icon(icon_name)

    def _create_fallback_icon(self, name: str) -> QIcon:
        """Create fallback icon."""
        # Create empty pixmap as placeholder
        pixmap = QPixmap(24, 24)
        pixmap.fill()
        return QIcon(pixmap)

    def get_icon(self, name: str) -> QIcon:
        """
        Get icon by name.

        Args:
            name: Icon name

        Returns:
            QIcon instance
        """
        return self._icons.get(name, QIcon())

    def get_pixmap(self, name: str, size: int = 24) -> QPixmap:
        """
        Get icon pixmap.

        Args:
            name: Icon name
            size: Icon size in pixels

        Returns:
            QPixmap instance
        """
        icon = self.get_icon(name)
        return icon.pixmap(QSize(size, size))
