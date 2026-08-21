"""
Main application window.
"""

import logging
from typing import Optional

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.config.constants import (
    APP_NAME,
    APP_VERSION,
    WINDOW_DEFAULT_HEIGHT,
    WINDOW_DEFAULT_WIDTH,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
)
from app.services.category_service import CategoryService
from app.services.notification_service import NotificationService
from app.services.scheduler_service import SchedulerService
from app.services.settings_service import SettingsService
from app.services.task_service import TaskService
from app.ui.theme import ThemeManager
from app.widgets.sidebar import Sidebar
from app.widgets.title_bar import TitleBar

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(
        self,
        task_service: TaskService,
        category_service: CategoryService,
        settings_service: SettingsService,
        scheduler_service: SchedulerService,
        notification_service: NotificationService,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Initialize main window.

        Args:
            task_service: Task service instance
            category_service: Category service instance
            settings_service: Settings service instance
            scheduler_service: Scheduler service instance
            notification_service: Notification service instance
            parent: Parent widget
        """
        super().__init__(parent)

        # Store services
        self.task_service = task_service
        self.category_service = category_service
        self.settings_service = settings_service
        self.scheduler_service = scheduler_service
        self.notification_service = notification_service

        # Initialize theme manager
        self.theme_manager = ThemeManager()

        # Setup window
        self._setup_window()
        self._setup_ui()
        self._apply_settings()

        logger.info("Main window initialized")

    def _setup_window(self) -> None:
        """Setup window properties."""
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)

        # Enable frameless window for custom title bar
        self.setWindowFlags(
            Qt.Window |
            Qt.FramelessWindowHint |
            Qt.WindowSystemMenuHint |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowMaximizeButtonHint
        )

    def _setup_ui(self) -> None:
        """Setup main UI."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main vertical layout (title bar + content)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Title bar
        self.title_bar = TitleBar()
        self.title_bar.minimize_requested.connect(self.showMinimized)
        self.title_bar.maximize_requested.connect(self._toggle_maximize)
        self.title_bar.close_requested.connect(self.close)
        main_layout.addWidget(self.title_bar)

        # Content layout (sidebar + content stack)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.navigation_changed.connect(self._navigate_to)
        content_layout.addWidget(self.sidebar)

        # Content stack
        self.content_stack = QStackedWidget()
        content_layout.addWidget(self.content_stack, stretch=1)

        main_layout.addLayout(content_layout, stretch=1)

        # Initialize views
        self._initialize_views()

    def _toggle_maximize(self) -> None:
        """Toggle maximize/restore window."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def _initialize_views(self) -> None:
        """Initialize all views."""
        # Import views
        from app.ui.views.dashboard_view import DashboardView
        from app.ui.views.today_view import TodayView
        from app.ui.views.upcoming_view import UpcomingView
        from app.ui.views.overdue_view import OverdueView
        from app.ui.views.completed_view import CompletedView
        from app.ui.views.calendar_view import CalendarView
        from app.ui.views.settings_view import SettingsView

        # Dashboard view
        self.dashboard_view = DashboardView(
            self.task_service,
            self.category_service,
        )
        self.content_stack.addWidget(self.dashboard_view)

        # Today view
        self.today_view = TodayView(self.task_service)
        self.content_stack.addWidget(self.today_view)

        # Upcoming view
        self.upcoming_view = UpcomingView(self.task_service)
        self.content_stack.addWidget(self.upcoming_view)

        # Overdue view
        self.overdue_view = OverdueView(self.task_service)
        self.content_stack.addWidget(self.overdue_view)

        # Completed view
        self.completed_view = CompletedView(self.task_service)
        self.content_stack.addWidget(self.completed_view)

        # Calendar view
        self.calendar_view = CalendarView(self.task_service)
        self.content_stack.addWidget(self.calendar_view)

        # Settings view
        self.settings_view = SettingsView(self.settings_service)
        self.content_stack.addWidget(self.settings_view)

        # Connect signals
        for view in [self.dashboard_view, self.today_view, self.upcoming_view,
                     self.overdue_view, self.completed_view]:
            if hasattr(view, 'add_task_requested'):
                view.add_task_requested.connect(self.show_add_task_dialog)
            if hasattr(view, 'edit_task_requested'):
                view.edit_task_requested.connect(self.show_edit_task_dialog)
            if hasattr(view, 'delete_task_requested'):
                view.delete_task_requested.connect(self.delete_task)
            if hasattr(view, 'task_completed'):
                view.task_completed.connect(self.complete_task)

        # Set initial view
        self._navigate_to('dashboard')

    def _apply_settings(self) -> None:
        """Apply saved settings."""
        # Apply theme
        theme = self.settings_service.get('theme', 'light')
        self.theme_manager.set_theme(theme)

    def _navigate_to(self, view_name: str) -> None:
        """Navigate to specified view."""
        view_map = {
            'dashboard': self.dashboard_view,
            'today': self.today_view,
            'upcoming': self.upcoming_view,
            'overdue': self.overdue_view,
            'completed': self.completed_view,
            'calendar': self.calendar_view,
            'settings': self.settings_view,
        }

        if view_name in view_map:
            view = view_map[view_name]
            self.content_stack.setCurrentWidget(view)

            # Refresh view
            if hasattr(view, 'refresh'):
                view.refresh()

            # Update sidebar
            self.sidebar.set_active(view_name)

            logger.debug(f"Navigated to {view_name}")

    def show_add_task_dialog(self) -> None:
        """Show add task dialog."""
        from app.dialogs.task_dialog import TaskDialog

        dialog = TaskDialog(
            self.category_service,
            parent=self,
        )

        if dialog.exec():
            task_data = dialog.get_task_data()
            self.task_service.create_task(task_data)
            self.refresh_current_view()
            logger.info("Task created via dialog")

    def show_edit_task_dialog(self, task_id: int) -> None:
        """Show edit task dialog."""
        from app.dialogs.task_dialog import TaskDialog

        task = self.task_service.get_task(task_id)
        if not task:
            QMessageBox.warning(self, "Error", "Task not found")
            return

        dialog = TaskDialog(
            self.category_service,
            task=task,
            parent=self,
        )

        if dialog.exec():
            task_data = dialog.get_task_data()
            self.task_service.update_task(task_id, task_data)
            self.refresh_current_view()
            logger.info(f"Task {task_id} updated via dialog")

    def delete_task(self, task_id: int) -> None:
        """Delete task with confirmation."""
        task = self.task_service.get_task(task_id)
        if not task:
            return

        # Show confirmation dialog
        reply = QMessageBox.question(
            self,
            "Delete Task",
            f"Delete this task?\n\n'{task.title}'\n\nThis action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self.task_service.delete_task(task_id)
            self.refresh_current_view()
            logger.info(f"Task {task_id} deleted")

    def complete_task(self, task_id: int) -> None:
        """Complete task."""
        self.task_service.complete_task(task_id)
        self.refresh_current_view()
        logger.info(f"Task {task_id} completed")

    def refresh_current_view(self) -> None:
        """Refresh current view."""
        current_view = self.content_stack.currentWidget()
        if hasattr(current_view, 'refresh'):
            current_view.refresh()

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        # Check if minimize to tray is enabled
        minimize_to_tray = self.settings_service.get('minimize_to_tray', True)
        close_to_tray = self.settings_service.get('close_to_tray', True)

        if minimize_to_tray and close_to_tray:
            # Just hide window instead of closing
            event.ignore()
            self.hide()
            logger.info("Window minimized to tray")
        else:
            # Actually close
            event.accept()
            logger.info("Window closed")
