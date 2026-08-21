"""
Application factory for TaskFlow.
"""

import logging
from typing import Optional

from PySide6.QtWidgets import QApplication

from app.config.constants import APP_NAME, APP_VERSION, ORGANIZATION_NAME
from app.config.settings import AppSettings
from app.database.connection import DatabaseManager
from app.repositories.category_repository import CategoryRepository
from app.repositories.reminder_repository import ReminderRepository
from app.repositories.settings_repository import SettingsRepository
from app.repositories.task_repository import TaskRepository
from app.services.category_service import CategoryService
from app.services.notification_service import NotificationService
from app.services.reminder_service import ReminderService
from app.services.scheduler_service import SchedulerService
from app.services.settings_service import SettingsService
from app.services.task_service import TaskService
from app.ui.main_window import MainWindow

logger = logging.getLogger(__name__)


class TaskFlowApplication:
    """Main application class."""

    def __init__(self) -> None:
        """Initialize application."""
        self.settings: Optional[AppSettings] = None
        self.db_manager: Optional[DatabaseManager] = None

        self.task_repository: Optional[TaskRepository] = None
        self.category_repository: Optional[CategoryRepository] = None
        self.reminder_repository: Optional[ReminderRepository] = None
        self.settings_repository: Optional[SettingsRepository] = None

        self.task_service: Optional[TaskService] = None
        self.category_service: Optional[CategoryService] = None
        self.reminder_service: Optional[ReminderService] = None
        self.settings_service: Optional[SettingsService] = None
        self.notification_service: Optional[NotificationService] = None
        self.scheduler_service: Optional[SchedulerService] = None

        self.main_window: Optional[MainWindow] = None
        self.qt_app: Optional[QApplication] = None

    def initialize(self) -> None:
        """Initialize all application components."""
        logger.info(f"Initializing {APP_NAME} v{APP_VERSION}")

        # Initialize Qt application
        self.qt_app = QApplication.instance() or QApplication([])
        self.qt_app.setApplicationName(APP_NAME)
        self.qt_app.setApplicationVersion(APP_VERSION)
        self.qt_app.setOrganizationName(ORGANIZATION_NAME)
        self.qt_app.setStyle("Fusion")

        # Initialize settings
        self.settings = AppSettings()
        self.settings.load()

        # Initialize database
        self.db_manager = DatabaseManager(self.settings)
        self.db_manager.initialize()

        # Initialize repositories
        self.task_repository = TaskRepository(self.db_manager.session_factory)
        self.category_repository = CategoryRepository(
            self.db_manager.session_factory)
        self.reminder_repository = ReminderRepository(
            self.db_manager.session_factory)
        self.settings_repository = SettingsRepository(
            self.db_manager.session_factory)

        # Initialize services
        self.task_service = TaskService(
            self.task_repository,
            self.reminder_repository,
        )
        self.category_service = CategoryService(self.category_repository)
        self.reminder_service = ReminderService(
            self.reminder_repository,
            self.task_repository,
        )
        self.settings_service = SettingsService(self.settings_repository)
        self.notification_service = NotificationService()
        self.scheduler_service = SchedulerService(
            self.task_service,
            self.reminder_service,
            self.notification_service,
            self.settings_service,
        )

        # Initialize default categories
        self._initialize_default_categories()

        # Initialize main window
        self.main_window = MainWindow(
            task_service=self.task_service,
            category_service=self.category_service,
            settings_service=self.settings_service,
            scheduler_service=self.scheduler_service,
            notification_service=self.notification_service,
        )

        logger.info("Application initialization complete")

    def _initialize_default_categories(self) -> None:
        """Create default categories if they don't exist."""
        default_categories = ['Work', 'Personal',
                              'Study', 'Finance', 'Health', 'Other']

        existing_categories = self.category_service.get_all_categories()
        existing_names = {c.name for c in existing_categories}

        for category_name in default_categories:
            if category_name not in existing_names:
                try:
                    self.category_service.create_category(
                        name=category_name,
                        description=f"Default {category_name.lower()} category",
                    )
                    logger.info(f"Created default category: {category_name}")
                except Exception as e:
                    logger.warning(
                        f"Failed to create default category {category_name}: {e}")

    def run(self) -> int:
        """
        Run the application.

        Returns:
            Exit code
        """
        if not self.main_window:
            logger.error("Application not initialized")
            return 1

        # Show main window
        self.main_window.show()

        # Start scheduler
        if self.scheduler_service:
            self.scheduler_service.start()

        # Run event loop
        exit_code = self.qt_app.exec()

        # Cleanup
        self.shutdown()

        return exit_code

    def shutdown(self) -> None:
        """Shutdown application and cleanup resources."""
        logger.info("Shutting down application")

        # Stop scheduler
        if self.scheduler_service:
            self.scheduler_service.stop()

        # Close database
        if self.db_manager:
            self.db_manager.close()

        logger.info("Application shutdown complete")
