"""
Test configuration and fixtures.
"""

import logging
import sys
from pathlib import Path
from typing import Generator

import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

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

# Configure logging for tests
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


@pytest.fixture
def temp_settings(tmp_path) -> AppSettings:
    """Create temporary settings for testing."""
    settings = AppSettings()
    settings._data_dir = tmp_path / "data"
    settings._config_file = tmp_path / "settings.json"
    settings._data_dir.mkdir(parents=True, exist_ok=True)
    return settings


@pytest.fixture
def db_manager(temp_settings) -> Generator[DatabaseManager, None, None]:
    """Create database manager for testing."""
    manager = DatabaseManager(temp_settings)
    manager.initialize()
    yield manager
    manager.close()


@pytest.fixture
def task_repository(db_manager) -> TaskRepository:
    """Create task repository."""
    return TaskRepository(db_manager.session_factory)


@pytest.fixture
def category_repository(db_manager) -> CategoryRepository:
    """Create category repository."""
    return CategoryRepository(db_manager.session_factory)


@pytest.fixture
def reminder_repository(db_manager) -> ReminderRepository:
    """Create reminder repository."""
    return ReminderRepository(db_manager.session_factory)


@pytest.fixture
def settings_repository(db_manager) -> SettingsRepository:
    """Create settings repository."""
    return SettingsRepository(db_manager.session_factory)


@pytest.fixture
def task_service(task_repository, reminder_repository) -> TaskService:
    """Create task service."""
    return TaskService(task_repository, reminder_repository)


@pytest.fixture
def category_service(category_repository) -> CategoryService:
    """Create category service."""
    return CategoryService(category_repository)


@pytest.fixture
def reminder_service(reminder_repository, task_repository) -> ReminderService:
    """Create reminder service."""
    return ReminderService(reminder_repository, task_repository)


@pytest.fixture
def settings_service(settings_repository) -> SettingsService:
    """Create settings service."""
    return SettingsService(settings_repository)


@pytest.fixture
def notification_service() -> NotificationService:
    """Create notification service."""
    return NotificationService()


@pytest.fixture
def scheduler_service(
    task_service,
    reminder_service,
    notification_service,
    settings_service,
) -> SchedulerService:
    """Create scheduler service."""
    return SchedulerService(
        task_service,
        reminder_service,
        notification_service,
        settings_service,
    )


@pytest.fixture
def sample_task_data() -> dict:
    """Sample task data for testing."""
    return {
        'title': 'Test Task',
        'description': 'This is a test task',
        'due_date': None,
        'due_time': None,
        'priority': 'medium',
        'status': 'pending',
        'category_id': None,
        'reminder_minutes': 30,
    }


@pytest.fixture
def created_task(task_service, sample_task_data) -> dict:
    """Create a task and return it."""
    task = task_service.create_task(sample_task_data)
    return task


@pytest.fixture
def sample_category_data() -> dict:
    """Sample category data."""
    return {
        'name': 'Work',
        'description': 'Work-related tasks',
    }