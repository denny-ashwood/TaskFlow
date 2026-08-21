"""
Database migration management.
"""

import logging
from pathlib import Path
from typing import List, Tuple

from sqlalchemy import text

logger = logging.getLogger(__name__)


class Migration:
    """Represents a database migration."""

    def __init__(self, version: int, name: str, sql: str) -> None:
        self.version = version
        self.name = name
        self.sql = sql


# Migration definitions
MIGRATIONS: List[Migration] = [
    Migration(
        version=1,
        name="initial_schema",
        sql="""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL UNIQUE,
            description TEXT,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            due_date DATE,
            due_time TIME,
            priority VARCHAR(10) NOT NULL DEFAULT 'medium',
            status VARCHAR(20) NOT NULL DEFAULT 'pending',
            category_id INTEGER,
            reminder_minutes INTEGER DEFAULT 30,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            completed_at DATETIME,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER NOT NULL,
            reminder_time DATETIME NOT NULL,
            notification_sent BOOLEAN NOT NULL DEFAULT 0,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key VARCHAR(100) NOT NULL UNIQUE,
            value TEXT,
            updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """
    ),
    Migration(
        version=2,
        name="add_indexes",
        sql="""
        CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
        CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
        CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
        CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category_id);
        CREATE INDEX IF NOT EXISTS idx_reminders_task ON reminders(task_id);
        CREATE INDEX IF NOT EXISTS idx_reminders_time ON reminders(reminder_time);
        """
    ),
]


class MigrationManager:
    """Manages database migrations."""

    def __init__(self, engine) -> None:
        self.engine = engine

    def get_current_version(self) -> int:
        """Get current schema version."""
        with self.engine.connect() as conn:
            result = conn.execute(text(
                "SELECT value FROM settings WHERE key = 'schema_version'"
            ))
            row = result.fetchone()
            return int(row[0]) if row else 0

    def set_version(self, version: int) -> None:
        """Set schema version."""
        with self.engine.begin() as conn:
            conn.execute(text(
                "INSERT OR REPLACE INTO settings (key, value) VALUES ('schema_version', :version)"
            ), {"version": str(version)})

    def migrate(self) -> None:
        """Run pending migrations."""
        current_version = self.get_current_version()
        logger.info(f"Current schema version: {current_version}")

        for migration in MIGRATIONS:
            if migration.version > current_version:
                logger.info(f"Applying migration {migration.version}: {migration.name}")
                try:
                    with self.engine.begin() as conn:
                        for statement in migration.sql.split(';'):
                            if statement.strip():
                                conn.execute(text(statement))
                        self.set_version(migration.version)
                    logger.info(f"Migration {migration.version} applied successfully")
                except Exception as e:
                    logger.error(f"Failed to apply migration {migration.version}: {e}")
                    raise