"""
Logging configuration utilities.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from platformdirs import user_log_dir

from app.config.constants import (
    APP_NAME,
    LOG_BACKUP_COUNT,
    LOG_DATE_FORMAT,
    LOG_FORMAT,
    LOG_MAX_BYTES,
    ORGANIZATION_NAME,
)


def setup_logging(
    app_name: str = APP_NAME,
    log_level: str = "INFO",
    log_format: str = LOG_FORMAT,
    log_dir: Optional[Path] = None,
) -> None:
    """
    Configure application logging.

    Args:
        app_name: Application name for log file
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Log message format
        log_dir: Custom log directory (defaults to OS-specific location)
    """
    # Determine log directory
    if log_dir is None:
        log_dir = Path(user_log_dir(APP_NAME, ORGANIZATION_NAME))

    # Create log directory if needed
    log_dir.mkdir(parents=True, exist_ok=True)

    # Log file path
    log_file = log_dir / f"{app_name.lower()}.log"

    # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Clear existing handlers
    root_logger.handlers.clear()

    # Create formatters
    formatter = logging.Formatter(
        fmt=log_format,
        datefmt=LOG_DATE_FORMAT
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler with rotation
    try:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=LOG_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not create log file handler: {e}")

    # Log startup info
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized - file: {log_file}")
