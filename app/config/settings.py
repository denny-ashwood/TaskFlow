"""
Application settings management.
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from platformdirs import user_data_dir

from app.config.constants import (
    APP_NAME,
    DATABASE_FILENAME,
    DEFAULT_SETTINGS,
    ORGANIZATION_NAME,
)

logger = logging.getLogger(__name__)


class AppSettings:
    """Manages application configuration and settings."""

    def __init__(self) -> None:
        """Initialize settings manager."""
        self._settings: Dict[str, Any] = DEFAULT_SETTINGS.copy()
        self._data_dir: Optional[Path] = None
        self._config_file: Optional[Path] = None
        self._initialize_paths()

    def _initialize_paths(self) -> None:
        """Initialize application data and config paths."""
        # Get OS-specific data directory
        self._data_dir = Path(user_data_dir(APP_NAME, ORGANIZATION_NAME))
        self._data_dir.mkdir(parents=True, exist_ok=True)

        # Configuration file path
        self._config_file = self._data_dir / "settings.json"

        logger.debug(f"Data directory: {self._data_dir}")
        logger.debug(f"Config file: {self._config_file}")

    @property
    def data_dir(self) -> Path:
        """Get application data directory."""
        return self._data_dir

    @property
    def database_path(self) -> Path:
        """Get database file path."""
        return self._data_dir / DATABASE_FILENAME

    @property
    def config_file(self) -> Path:
        """Get configuration file path."""
        return self._config_file

    def load(self) -> None:
        """Load settings from configuration file."""
        if not self._config_file or not self._config_file.exists():
            logger.info("No settings file found, using defaults")
            self.save()
            return

        try:
            with open(self._config_file, 'r') as f:
                loaded_settings = json.load(f)
                self._settings.update(loaded_settings)
            logger.info("Settings loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            logger.info("Using default settings")

    def save(self) -> None:
        """Save settings to configuration file."""
        if not self._config_file:
            return

        try:
            with open(self._config_file, 'w') as f:
                json.dump(self._settings, f, indent=2)
            logger.info("Settings saved successfully")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value by key."""
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set setting value and save."""
        self._settings[key] = value
        self.save()

    def update(self, updates: Dict[str, Any]) -> None:
        """Update multiple settings and save."""
        self._settings.update(updates)
        self.save()

    def reset(self) -> None:
        """Reset settings to defaults."""
        self._settings = DEFAULT_SETTINGS.copy()
        self.save()

    def __getitem__(self, key: str) -> Any:
        """Get setting using dictionary syntax."""
        return self._settings[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """Set setting using dictionary syntax."""
        self._settings[key] = value

    def __contains__(self, key: str) -> bool:
        """Check if setting exists."""
        return key in self._settings