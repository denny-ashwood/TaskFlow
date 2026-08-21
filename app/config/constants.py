"""
Application constants and configuration values.
"""

# Application information
APP_NAME = "TaskFlow"
APP_VERSION = "1.0.0"
ORGANIZATION_NAME = "TaskFlow"
ORGANIZATION_DOMAIN = "taskflow.app"

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

# Database configuration
DATABASE_FILENAME = "taskflow.db"
DATABASE_URL_TEMPLATE = "sqlite:///{path}"

# Task priorities
PRIORITY_LOW = "low"
PRIORITY_MEDIUM = "medium"
PRIORITY_HIGH = "high"
PRIORITIES = [PRIORITY_LOW, PRIORITY_MEDIUM, PRIORITY_HIGH]

# Task statuses
STATUS_PENDING = "pending"
STATUS_COMPLETED = "completed"
STATUS_CANCELLED = "cancelled"
STATUSES = [STATUS_PENDING, STATUS_COMPLETED, STATUS_CANCELLED]

# Default settings
DEFAULT_SETTINGS = {
    "theme": "light",
    "notifications_enabled": True,
    "default_reminder": 15,
    "notification_sound": "chime",
    "start_with_system": False,
    "minimize_to_tray": True,
    "close_to_tray": True,
    "default_priority": "medium",
    "default_category": None,
    "missed_reminder_window": 15,  # minutes
}

# UI configuration
WINDOW_MIN_WIDTH = 900
WINDOW_MIN_HEIGHT = 600
WINDOW_DEFAULT_WIDTH = 1200
WINDOW_DEFAULT_HEIGHT = 800

# Date/time formats
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = "%Y-%m-%d %H:%M"
DISPLAY_DATE_FORMAT = "%B %d, %Y"
DISPLAY_TIME_FORMAT = "%I:%M %p"
DISPLAY_DATETIME_FORMAT = "%B %d, %Y at %I:%M %p"

# Reminder options (minutes before)
REMINDER_OPTIONS = [
    (0, "At time of event"),
    (5, "5 minutes before"),
    (10, "10 minutes before"),
    (15, "15 minutes before"),
    (30, "30 minutes before"),
    (60, "1 hour before"),
    (120, "2 hours before"),
    (1440, "1 day before"),
]

# Keyboard shortcuts
SHORTCUT_NEW_TASK = "Ctrl+N"
SHORTCUT_SEARCH = "Ctrl+F"
SHORTCUT_SAVE = "Ctrl+Enter"
SHORTCUT_DELETE = "Delete"
SHORTCUT_CLOSE = "Escape"