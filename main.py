#!/usr/bin/env python3

"""
TaskFlow - Personal Task Management Application

Main entry point for the application.

@author Denzell S'fisokuhle Yona
@company D-Tek Solutions
@github https://github.com/denny-ashwood/TaskFlow.git
@version 1.0.0
@license MIT
"""

from app.utils.logging_config import setup_logging
from app.config.constants import (
    APP_NAME,
    APP_VERSION,
    LOG_FORMAT,
    LOG_LEVEL,
)
import sys
import logging
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    """
    Main application entry point.

    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    # Initialize logging
    setup_logging(
        app_name=APP_NAME,
        log_level=LOG_LEVEL,
        log_format=LOG_FORMAT,
    )

    logger = logging.getLogger(__name__)
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")

    try:
        from app.application import TaskFlowApplication

        # Create and initialize application
        app = TaskFlowApplication()
        app.initialize()

        # Run application
        exit_code = app.run()

        logger.info(f"{APP_NAME} exited with code {exit_code}")
        return exit_code

    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        return 0

    except Exception as e:
        logger.exception("Fatal error during application execution")
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
