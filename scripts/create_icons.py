#!/usr/bin/env python3
"""
Generate placeholder icons for TaskFlow application.
Creates simple PNG icons using Qt.
"""

import sys
from pathlib import Path

# Create QApplication before using QPixmap
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QPainter, QPixmap, QColor, QBrush, QPen, QFont, QPolygon
from PySide6.QtCore import Qt, QRect, QPoint

# Create QApplication instance (required for QPixmap)
app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

def create_app_icon(size=256):
    """Create application icon."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    # Background circle
    painter.setBrush(QBrush(QColor("#0050cb")))
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(0, 0, size, size)

    # Checkmark
    painter.setPen(QPen(QColor("white"), size // 10, Qt.SolidLine, Qt.RoundCap))
    check_points = [
        QPoint(size // 4, size // 2),
        QPoint(size // 2 - size // 20, size * 3 // 4),
        QPoint(size * 3 // 4, size // 3),
    ]
    painter.drawPolyline(check_points)

    painter.end()
    return pixmap

def create_simple_icon(icon_type, size=64):
    """Create simple icons for various purposes."""
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    colors = {
        'dashboard': '#0050cb',
        'today': '#0066ff',
        'upcoming': '#505f76',
        'overdue': '#ba1a1a',
        'completed': '#00a862',
        'calendar': '#a33200',
        'settings': '#505f76',
        'add': '#0050cb',
        'search': '#505f76',
        'notifications': '#ba1a1a',
        'person': '#505f76',
        'more': '#505f76',
        'close': '#505f76',
        'edit': '#505f76',
        'delete': '#ba1a1a',
        'check': '#00a862',
        'check_circle': '#00a862',
        'schedule': '#505f76',
        'folder': '#a33200',
        'chevron_left': '#505f76',
        'chevron_right': '#505f76',
        'expand_more': '#505f76',
    }

    color = colors.get(icon_type, '#505f76')
    painter.setBrush(QBrush(QColor(color)))
    painter.setPen(Qt.NoPen)

    # Draw different shapes based on icon type
    if icon_type == 'dashboard':
        # Grid pattern
        cell_size = size // 4
        for i in range(4):
            for j in range(4):
                if (i + j) % 3 != 0:
                    painter.drawRect(i * cell_size + 1, j * cell_size + 1,
                                   cell_size - 2, cell_size - 2)

    elif icon_type == 'today':
        # Calendar icon
        painter.drawRect(size // 8, size // 4, size * 3 // 4, size * 5 // 8)
        painter.setBrush(QBrush(QColor("white")))
        painter.drawRect(size // 4, size // 8, size // 8, size // 4)
        painter.drawRect(size * 5 // 8, size // 8, size // 8, size // 4)

    elif icon_type == 'upcoming':
        # Arrow up
        polygon = QPolygon([
            QPoint(size // 2, size // 8),
            QPoint(size * 7 // 8, size // 2),
            QPoint(size * 5 // 8, size // 2),
            QPoint(size * 5 // 8, size * 7 // 8),
            QPoint(size * 3 // 8, size * 7 // 8),
            QPoint(size * 3 // 8, size // 2),
            QPoint(size // 8, size // 2),
        ])
        painter.drawPolygon(polygon)

    elif icon_type == 'overdue':
        # Exclamation mark
        painter.drawRect(size * 3 // 8, size // 8, size // 4, size // 2)
        painter.drawEllipse(size * 3 // 8, size * 5 // 8, size // 4, size // 4)

    elif icon_type == 'completed':
        # Checkmark circle
        painter.drawEllipse(size // 8, size // 8, size * 3 // 4, size * 3 // 4)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor("white"), size // 8, Qt.SolidLine, Qt.RoundCap))
        check_polygon = QPolygon([
            QPoint(size // 4, size // 2),
            QPoint(size * 3 // 8, size * 5 // 8),
            QPoint(size * 3 // 4, size // 3),
        ])
        painter.drawPolyline(check_polygon)

    elif icon_type == 'calendar':
        # Calendar with line
        painter.drawRect(size // 8, size // 4, size * 3 // 4, size * 5 // 8)
        painter.setPen(QPen(QColor("white"), size // 12, Qt.SolidLine))
        painter.drawLine(size // 8, size // 2, size * 7 // 8, size // 2)

    elif icon_type == 'settings':
        # Gear (simplified as circle with spokes)
        painter.drawEllipse(size // 4, size // 4, size // 2, size // 2)
        painter.setPen(QPen(QColor(color), size // 10, Qt.SolidLine))
        for angle in range(0, 360, 45):
            import math
            rad = math.radians(angle)
            x1 = size // 2 + int(size * 0.35 * math.cos(rad))
            y1 = size // 2 + int(size * 0.35 * math.sin(rad))
            x2 = size // 2 + int(size * 0.45 * math.cos(rad))
            y2 = size // 2 + int(size * 0.45 * math.sin(rad))
            painter.drawLine(x1, y1, x2, y2)

    elif icon_type == 'add':
        # Plus sign
        painter.drawRect(size * 3 // 8, size // 8, size // 4, size * 3 // 4)
        painter.drawRect(size // 8, size * 3 // 8, size * 3 // 4, size // 4)

    elif icon_type == 'search':
        # Magnifying glass
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(color), size // 8, Qt.SolidLine, Qt.RoundCap))
        painter.drawEllipse(size // 8, size // 8, size * 5 // 8, size * 5 // 8)
        painter.drawLine(size * 5 // 8, size * 5 // 8, size * 7 // 8, size * 7 // 8)

    elif icon_type == 'notifications':
        # Bell
        bell_polygon = QPolygon([
            QPoint(size // 2, size // 8),
            QPoint(size * 7 // 8, size * 5 // 8),
            QPoint(size // 8, size * 5 // 8),
        ])
        painter.drawPolygon(bell_polygon)
        painter.drawEllipse(size * 3 // 8, size * 5 // 8, size // 4, size // 8)

    elif icon_type == 'person':
        # Person icon
        painter.drawEllipse(size // 4, size // 8, size // 2, size // 2)
        painter.drawEllipse(size // 8, size * 5 // 8, size * 3 // 4, size // 3)

    elif icon_type == 'more':
        # Three dots
        for i in range(3):
            painter.drawEllipse(size * (2 + i) // 5, size // 2 - size // 10,
                               size // 5, size // 5)

    elif icon_type == 'close':
        # X mark
        painter.setPen(QPen(QColor(color), size // 8, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(size // 4, size // 4, size * 3 // 4, size * 3 // 4)
        painter.drawLine(size * 3 // 4, size // 4, size // 4, size * 3 // 4)

    elif icon_type == 'edit':
        # Pencil (simplified)
        painter.setPen(QPen(QColor(color), size // 8, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(size // 4, size * 3 // 4, size * 3 // 4, size // 4)
        painter.drawLine(size // 4, size * 3 // 4, size // 2, size * 3 // 4)

    elif icon_type == 'delete':
        # Trash can
        painter.drawRect(size // 4, size // 3, size // 2, size // 2)
        painter.drawRect(size // 3, size // 4, size // 3, size // 6)

    elif icon_type == 'check':
        # Simple checkmark
        painter.setPen(QPen(QColor(color), size // 8, Qt.SolidLine, Qt.RoundCap))
        check_polygon = QPolygon([
            QPoint(size // 4, size // 2),
            QPoint(size * 3 // 8, size * 5 // 8),
            QPoint(size * 3 // 4, size // 4),
        ])
        painter.drawPolyline(check_polygon)

    elif icon_type == 'check_circle':
        # Circle with checkmark
        painter.drawEllipse(size // 8, size // 8, size * 3 // 4, size * 3 // 4)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor("white"), size // 10, Qt.SolidLine, Qt.RoundCap))
        check_polygon = QPolygon([
            QPoint(size // 4, size // 2),
            QPoint(size * 3 // 8, size * 5 // 8),
            QPoint(size * 3 // 4, size // 4),
        ])
        painter.drawPolyline(check_polygon)

    elif icon_type == 'schedule':
        # Clock
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(color), size // 10, Qt.SolidLine))
        painter.drawEllipse(size // 8, size // 8, size * 3 // 4, size * 3 // 4)
        painter.drawLine(size // 2, size // 2, size // 2, size // 4)
        painter.drawLine(size // 2, size // 2, size * 5 // 8, size * 5 // 8)

    elif icon_type == 'folder':
        # Folder
        painter.drawRect(size // 8, size // 4, size * 3 // 4, size * 5 // 8)
        painter.drawRect(size // 8, size // 4, size // 3, size // 6)

    elif icon_type == 'chevron_left':
        # Left chevron
        chevron_polygon = QPolygon([
            QPoint(size * 5 // 8, size // 4),
            QPoint(size // 3, size // 2),
            QPoint(size * 5 // 8, size * 3 // 4),
        ])
        painter.setPen(QPen(QColor(color), size // 8, Qt.SolidLine, Qt.RoundCap))
        painter.setBrush(Qt.NoBrush)
        painter.drawPolyline(chevron_polygon)

    elif icon_type == 'chevron_right':
        # Right chevron
        chevron_polygon = QPolygon([
            QPoint(size // 3, size // 4),
            QPoint(size * 5 // 8, size // 2),
            QPoint(size // 3, size * 3 // 4),
        ])
        painter.setPen(QPen(QColor(color), size // 8, Qt.SolidLine, Qt.RoundCap))
        painter.setBrush(Qt.NoBrush)
        painter.drawPolyline(chevron_polygon)

    elif icon_type == 'expand_more':
        # Down chevron
        chevron_polygon = QPolygon([
            QPoint(size // 4, size // 3),
            QPoint(size // 2, size * 5 // 8),
            QPoint(size * 3 // 4, size // 3),
        ])
        painter.setPen(QPen(QColor(color), size // 8, Qt.SolidLine, Qt.RoundCap))
        painter.setBrush(Qt.NoBrush)
        painter.drawPolyline(chevron_polygon)

    painter.end()
    return pixmap

def main():
    """Generate all icons."""
    assets_dir = Path(__file__).parent.parent / 'assets'
    icons_dir = assets_dir / 'icons'
    images_dir = assets_dir / 'images'

    # Create directories
    icons_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)

    # Create app icon
    app_icon = create_app_icon()
    app_icon.save(str(icons_dir / 'app_icon.png'))
    print(f"Created: {icons_dir / 'app_icon.png'}")

    # Create other icons
    icon_types = [
        'dashboard', 'today', 'upcoming', 'overdue', 'completed',
        'calendar', 'settings', 'add', 'search', 'notifications',
        'person', 'more', 'close', 'edit', 'delete', 'check',
        'check_circle', 'schedule', 'folder', 'chevron_left',
        'chevron_right', 'expand_more',
    ]

    for icon_type in icon_types:
        icon = create_simple_icon(icon_type)
        icon.save(str(icons_dir / f'{icon_type}.png'))
        print(f"Created: {icons_dir / f'{icon_type}.png'}")

    # Create empty state images
    empty_states = [
        ('no_tasks', '🎉'),
        ('no_upcoming', '📅'),
        ('no_completed', '📋'),
        ('no_search', '🔍'),
        ('no_overdue', '✅'),
    ]

    for name, emoji in empty_states:
        pixmap = QPixmap(200, 200)
        pixmap.fill(Qt.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        font = QFont()
        font.setPointSize(80)
        painter.setFont(font)
        painter.drawText(QRect(0, 0, 200, 200), Qt.AlignCenter, emoji)
        painter.end()

        pixmap.save(str(images_dir / f'{name}.png'))
        print(f"Created: {images_dir / f'{name}.png'}")

    print("\nAll icons generated successfully!")

if __name__ == '__main__':
    main()
    # Clean up QApplication
    app.quit()