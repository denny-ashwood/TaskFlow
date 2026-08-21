"""
Settings service implementation.
"""

import logging
from typing import Any, Dict

from app.config.constants import DEFAULT_SETTINGS
from app.repositories.settings_repository import SettingsRepository

logger = logging.getLogger(__name__)


class SettingsService:
    """Service for settings management."""

    def __init__(self, settings_repository: SettingsRepository) -> None:
        self.settings_repository = settings_repository
        self._cache: Dict[str, Any] = {}
        self._load_settings()

    def _load_settings(self) -> None:
        """Load settings into cache."""
        self._cache = DEFAULT_SETTINGS.copy()
        stored_settings = self.settings_repository.get_all_settings()
        self._cache.update(stored_settings)
        logger.debug(f"Loaded {len(self._cache)} settings")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get setting value.

        Args:
            key: Setting key
            default: Default value if not found

        Returns:
            Setting value
        """
        return self._cache.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set setting value.

        Args:
            key: Setting key
            value: Setting value
        """
        self._cache[key] = value
        self.settings_repository.set_value(key, value)
        logger.debug(f"Setting '{key}' set to {value}")

    def update(self, settings_dict: Dict[str, Any]) -> None:
        """
        Update multiple settings.

        Args:
            settings_dict: Dictionary of settings
        """
        self._cache.update(settings_dict)
        self.settings_repository.update_settings(settings_dict)
        logger.debug(f"Updated {len(settings_dict)} settings")

    def get_all(self) -> Dict[str, Any]:
        """Get all settings."""
        return self._cache.copy()

    def reset(self) -> None:
        """Reset settings to defaults."""
        self._cache = DEFAULT_SETTINGS.copy()
        self.settings_repository.update_settings(DEFAULT_SETTINGS)
        logger.info("Settings reset to defaults")

    def reload(self) -> None:
        """Reload settings from database."""
        self._load_settings()