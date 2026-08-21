"""
Settings repository implementation.
"""

import json
import logging
from typing import Any, Dict, List, Optional

from sqlalchemy import select

from app.models.setting import Setting
from app.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class SettingsRepository(BaseRepository[Setting]):
    """Repository for Setting entities."""

    def __init__(self, session_factory) -> None:
        super().__init__(Setting, session_factory)

    def get_value(self, key: str, default: Any = None) -> Any:
        """
        Get setting value by key.

        Args:
            key: Setting key
            default: Default value if not found

        Returns:
            Setting value (parsed from JSON if possible)
        """
        with self.session_factory() as session:
            stmt = select(Setting).where(Setting.key == key)
            result = session.execute(stmt)
            setting = result.scalar_one_or_none()

            if setting is None:
                return default

            return self._parse_value(setting.value)

    def set_value(self, key: str, value: Any) -> None:
        """
        Set setting value.

        Args:
            key: Setting key
            value: Setting value (will be serialized to JSON)
        """
        serialized_value = self._serialize_value(value)

        with self.session_factory() as session:
            stmt = select(Setting).where(Setting.key == key)
            result = session.execute(stmt)
            setting = result.scalar_one_or_none()

            if setting:
                setting.value = serialized_value
            else:
                setting = Setting(key=key, value=serialized_value)
                session.add(setting)

            session.commit()
            logger.debug(f"Setting '{key}' updated")

    def get_all_settings(self) -> Dict[str, Any]:
        """
        Get all settings as dictionary.

        Returns:
            Dictionary of all settings
        """
        with self.session_factory() as session:
            stmt = select(Setting).order_by(Setting.key)
            result = session.execute(stmt)
            settings = result.scalars().all()

            return {
                setting.key: self._parse_value(setting.value)
                for setting in settings
            }

    def update_settings(self, settings_dict: Dict[str, Any]) -> None:
        """
        Update multiple settings.

        Args:
            settings_dict: Dictionary of settings to update
        """
        with self.session_factory() as session:
            for key, value in settings_dict.items():
                serialized_value = self._serialize_value(value)

                stmt = select(Setting).where(Setting.key == key)
                result = session.execute(stmt)
                setting = result.scalar_one_or_none()

                if setting:
                    setting.value = serialized_value
                else:
                    setting = Setting(key=key, value=serialized_value)
                    session.add(setting)

            session.commit()
            logger.debug(f"Updated {len(settings_dict)} settings")

    def delete_setting(self, key: str) -> bool:
        """
        Delete setting by key.

        Args:
            key: Setting key

        Returns:
            True if deleted, False if not found
        """
        with self.session_factory() as session:
            stmt = select(Setting).where(Setting.key == key)
            result = session.execute(stmt)
            setting = result.scalar_one_or_none()

            if not setting:
                return False

            session.delete(setting)
            session.commit()
            return True

    @staticmethod
    def _serialize_value(value: Any) -> str:
        """Serialize value to JSON string."""
        return json.dumps(value)

    @staticmethod
    def _parse_value(value: str) -> Any:
        """Parse JSON string to Python value."""
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
