"""
Material Icons manager for TaskFlow.
Uses Material Icons font for consistent icon rendering.
"""

import logging
from pathlib import Path
from typing import Dict, Optional

from PySide6.QtGui import QFont, QFontDatabase, QIcon, QPixmap, QPainter, QColor
from PySide6.QtCore import QSize, Qt

logger = logging.getLogger(__name__)


class MaterialIcons:
    """Manages Material Icons font and provides icon creation."""

    # Material Icons codepoints (Unicode)
    ICONS = {
        'dashboard': '\ue871',      # grid_view
        'today': '\ue8df',           # today
        'upcoming': '\ueb96',        # event_upcoming
        'overdue': '\ue85c',         # assignment_late
        'completed': '\ue86c',       # task_alt
        'calendar': '\uebcc',        # calendar_month
        'settings': '\ue8b8',        # settings
        'add': '\ue145',             # add
        'search': '\ue8b6',          # search
        'notifications': '\ue7f4',   # notifications
        'person': '\ue7fd',          # person
        'more_vert': '\ue5d4',       # more_vert
        'close': '\ue5cd',           # close
        'edit': '\ue3c9',            # edit
        'delete': '\ue872',          # delete
        'check': '\ue5ca',           # check
        'check_circle': '\ue86c',    # check_circle
        'schedule': '\ue8b5',        # schedule
        'folder': '\ue2c7',          # folder
        'priority_high': '\ue645',   # priority_high
        'chevron_left': '\ue5cb',    # chevron_left
        'chevron_right': '\ue5cc',   # chevron_right
        'expand_more': '\ue5cf',     # expand_more
        'inbox': '\ue156',           # inbox
        'work': '\ue8f9',            # work
        'personal': '\ue7fd',        # person
        'study': '\ue80c',           # school
        'finance': '\ue227',         # attach_money
        'health': '\ue8b8',          # favorite
        'other': '\ue145',           # more
        'restore': '\ue8ba',         # restore
        'bell': '\ue7f4',            # notifications
        'palette': '\ue40a',         # palette
        'tune': '\ue429',            # tune
        'apps': '\ue5c3',            # apps
        'arrow_back': '\ue5c4',      # arrow_back
        'arrow_forward': '\ue5c8',   # arrow_forward
        'warning': '\ue002',         # warning
        'info': '\ue88e',            # info
        'help': '\ue887',            # help
        'star': '\ue838',            # star
        'flag': '\ue153',            # flag
        'label': '\ue892',           # label
        'tag': '\ue892',             # tag
        'filter': '\uef4f',          # filter_alt
        'sort': '\ue164',            # sort
        'list': '\ue896',            # list
        'grid': '\ue8f0',            # grid_on
        'menu': '\ue5d2',            # menu
        'refresh': '\ue5d5',         # refresh
        'save': '\ue161',            # save
        'download': '\ue2c4',        # download
        'upload': '\ue2c6',          # upload
        'print': '\ue8ad',           # print
        'share': '\ue80d',           # share
        'lock': '\ue897',            # lock
        'unlock': '\ue898',          # lock_open
        'visibility': '\ue8f4',      # visibility
        'visibility_off': '\ue8f5',  # visibility_off
        'email': '\ue0be',           # email
        'phone': '\ue0cd',           # phone
        'location': '\ue0c8',        # location_on
        'link': '\ue157',            # link
        'code': '\ue86f',            # code
        'bug': '\ue868',             # bug_report
        'cloud': '\ue2bd',           # cloud
        'sync': '\ue627',            # sync
        'history': '\ue889',         # history
        'update': '\ue923',          # update
        'timer': '\ue425',           # timer
        'alarm': '\ue855',           # alarm
        'event': '\ue878',           # event
        'note': '\ue8d2',            # note
        'description': '\ue873',     # description
        'title': '\ue264',           # title
    }

    _font_loaded = False
    _font_family = "Material Icons"

    @classmethod
    def load_font(cls) -> bool:
        """Load Material Icons font."""
        if cls._font_loaded:
            return True

        try:
            # Try multiple possible font locations
            font_paths = [
                Path(__file__).parent.parent.parent / 'assets' / 'fonts' / 'MaterialIcons-Regular.ttf',
                Path(__file__).parent.parent.parent / 'assets' / 'fonts' / 'MaterialIconsOutlined-Regular.otf',
                Path(__file__).parent.parent.parent / 'assets' / 'fonts' / 'MaterialIconsRound-Regular.otf',
            ]

            for font_path in font_paths:
                if font_path.exists():
                    font_id = QFontDatabase.addApplicationFont(str(font_path))
                    if font_id != -1:
                        font_families = QFontDatabase.applicationFontFamilies(font_id)
                        if font_families:
                            cls._font_family = font_families[0]
                            cls._font_loaded = True
                            logger.info(f"Material Icons font loaded: {cls._font_family}")
                            return True

            logger.warning("Material Icons font not found, using fallback")
            return False

        except Exception as e:
            logger.error(f"Failed to load Material Icons font: {e}")
            return False

    @classmethod
    def get_icon_char(cls, name: str) -> str:
        """Get icon character for given name."""
        return cls.ICONS.get(name, cls.ICONS.get('other', '\ue145'))

    @classmethod
    def create_icon(
        cls,
        name: str,
        size: int = 24,
        color: str = "#000000",
    ) -> QIcon:
        """
        Create QIcon from Material Icon.

        Args:
            name: Icon name
            size: Icon size in pixels
            color: Icon color (hex string)

        Returns:
            QIcon instance
        """
        # Ensure font is loaded
        cls.load_font()

        # Create pixmap
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)

        # Draw icon
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set font
        font = QFont(cls._font_family)
        font.setPixelSize(size)
        painter.setFont(font)

        # Set color
        painter.setPen(QColor(color))

        # Draw icon text centered
        icon_char = cls.get_icon_char(name)
        painter.drawText(
            pixmap.rect(),
            Qt.AlignCenter,
            icon_char
        )

        painter.end()

        return QIcon(pixmap)

    @classmethod
    def create_pixmap(
        cls,
        name: str,
        size: int = 24,
        color: str = "#000000",
    ) -> QPixmap:
        """
        Create QPixmap from Material Icon.

        Args:
            name: Icon name
            size: Icon size in pixels
            color: Icon color

        Returns:
            QPixmap instance
        """
        icon = cls.create_icon(name, size, color)
        return icon.pixmap(QSize(size, size))

    @classmethod
    def setup_button(
        cls,
        button,
        icon_name: str,
        size: int = 24,
        color: str = "#666666",
    ) -> None:
        """
        Setup button with Material Icon.

        Args:
            button: QPushButton instance
            icon_name: Icon name
            size: Icon size
            color: Icon color
        """
        icon = cls.create_icon(icon_name, size, color)
        button.setIcon(icon)
        button.setIconSize(QSize(size, size))

    @classmethod
    def setup_label(
        cls,
        label,
        icon_name: str,
        size: int = 24,
        color: str = "#666666",
        text: str = "",
    ) -> None:
        """
        Setup label with Material Icon.

        Args:
            label: QLabel instance
            icon_name: Icon name
            size: Icon size
            color: Icon color
            text: Optional text to display next to icon
        """
        icon = cls.create_icon(icon_name, size, color)
        if text:
            label.setText(f"{cls.get_icon_char(icon_name)} {text}")
            font = QFont(cls._font_family)
            font.setPixelSize(size)
            label.setFont(font)
        else:
            label.setPixmap(icon.pixmap(QSize(size, size)))


class IconFactory:
    """Factory for creating themed icons."""

    @staticmethod
    def for_sidebar(icon_name: str, size: int = 20) -> QIcon:
        """Create icon for sidebar (light color for dark background)."""
        return MaterialIcons.create_icon(icon_name, size, "#cccccc")

    @staticmethod
    def for_button(icon_name: str, size: int = 20) -> QIcon:
        """Create icon for buttons."""
        return MaterialIcons.create_icon(icon_name, size, "#666666")

    @staticmethod
    def for_priority(priority: str, size: int = 16) -> QIcon:
        """Create icon for priority badge."""
        colors = {
            'high': '#ba1a1a',
            'medium': '#a33200',
            'low': '#1b5e20',
        }
        return MaterialIcons.create_icon(
            'priority_high',
            size,
            colors.get(priority, '#666666')
        )