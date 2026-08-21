"""
Calendar view implementation.
"""

import logging
from datetime import date, timedelta
from typing import Optional

from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtWidgets import (
    QCalendarWidget,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.services.task_service import TaskService
from app.widgets.empty_state import EmptyState

logger = logging.getLogger(__name__)


class CalendarView(QWidget):
    """Calendar view for tasks."""

    add_task_requested = Signal()
    edit_task_requested = Signal(int)

    def __init__(
        self,
        task_service: TaskService,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Initialize calendar view.

        Args:
            task_service: Task service instance
            parent: Parent widget
        """
        super().__init__(parent)
        self.task_service = task_service

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self) -> None:
        """Setup calendar view UI."""
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Calendar section
        calendar_section = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()

        self.title_label = QLabel("Calendar")
        self.title_label.setStyleSheet(
            "font-size: 28px; font-weight: 700;"
        )
        header_layout.addWidget(self.title_label)

        header_layout.addStretch()

        # Today button
        self.today_button = QPushButton("Today")
        self.today_button.clicked.connect(self._go_to_today)
        header_layout.addWidget(self.today_button)

        # Add task button
        self.add_task_button = QPushButton("+ Add Task")
        self.add_task_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0050cb;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #0066ff;
            }
            """
        )
        self.add_task_button.clicked.connect(self.add_task_requested.emit)
        header_layout.addWidget(self.add_task_button)

        calendar_section.addLayout(header_layout)

        # Calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar.setStyleSheet(
            """
            QCalendarWidget {
                background-color: white;
                border: 1px solid #e0e3e5;
                border-radius: 8px;
            }
            QCalendarWidget QToolButton {
                background-color: transparent;
                border: none;
                padding: 8px;
                font-weight: 600;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #f2f4f6;
                border-radius: 4px;
            }
            QCalendarWidget QAbstractItemView {
                background-color: white;
                selection-background-color: #d0e1fb;
                selection-color: #0b1c30;
            }
            """
        )
        calendar_section.addWidget(self.calendar)

        main_layout.addLayout(calendar_section, stretch=2)

        # Selected date tasks section
        tasks_section = QVBoxLayout()

        self.selected_date_label = QLabel("Tasks for Selected Date")
        self.selected_date_label.setStyleSheet(
            "font-size: 18px; font-weight: 600;"
        )
        tasks_section.addWidget(self.selected_date_label)

        # Task list
        self.task_list = QListWidget()
        self.task_list.setStyleSheet(
            """
            QListWidget {
                background-color: white;
                border: 1px solid #e0e3e5;
                border-radius: 8px;
                padding: 8px;
            }
            QListWidget::item {
                padding: 12px;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #f2f4f6;
            }
            QListWidget::item:selected {
                background-color: #d0e1fb;
                color: #0b1c30;
            }
            """
        )
        tasks_section.addWidget(self.task_list)

        main_layout.addLayout(tasks_section, stretch=1)

    def _connect_signals(self) -> None:
        """Connect calendar signals."""
        self.calendar.selectionChanged.connect(self._on_date_selected)
        self.task_list.itemDoubleClicked.connect(self._on_task_double_clicked)

    def _go_to_today(self) -> None:
        """Navigate to today's date."""
        self.calendar.setSelectedDate(QDate.currentDate())

    def _on_date_selected(self) -> None:
        """Handle date selection change."""
        selected_date = self.calendar.selectedDate()
        python_date = date(
            selected_date.year(),
            selected_date.month(),
            selected_date.day(),
        )

        # Update label
        self.selected_date_label.setText(
            f"Tasks for {selected_date.toString('dddd, MMMM d')}"
        )

        # Load tasks for selected date
        self._load_tasks_for_date(python_date)

    def _load_tasks_for_date(self, target_date: date) -> None:
        """Load tasks for specific date."""
        self.task_list.clear()

        # Get tasks for date
        tasks = self.task_service.search_tasks(
            query="",
            filters={
                'start_date': target_date,
                'end_date': target_date,
            }
        )

        if not tasks:
            # Show empty state in list
            empty_item = QListWidgetItem("No tasks for this date")
            empty_item.setFlags(Qt.NoItemFlags)
            self.task_list.addItem(empty_item)
            return

        # Add tasks to list
        for task in tasks:
            time_str = task.due_time.strftime("%I:%M %p") if task.due_time else ""
            display_text = f"{time_str} - {task.title}" if time_str else task.title

            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, task.id)

            if task.priority == 'high':
                item.setForeground(Qt.red)
            elif task.priority == 'medium':
                item.setForeground(Qt.darkYellow)

            self.task_list.addItem(item)

    def _on_task_double_clicked(self, item: QListWidgetItem) -> None:
        """Handle task double-click."""
        task_id = item.data(Qt.UserRole)
        if task_id:
            self.edit_task_requested.emit(task_id)

    def refresh(self) -> None:
        """Refresh calendar view."""
        self._on_date_selected()