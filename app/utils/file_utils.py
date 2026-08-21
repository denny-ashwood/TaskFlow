"""
File operation utilities.
"""

import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


def ensure_directory(directory: Path) -> None:
    """
    Ensure directory exists.

    Args:
        directory: Directory path
    """
    directory.mkdir(parents=True, exist_ok=True)


def safe_read_json(file_path: Path) -> Optional[Dict]:
    """
    Safely read JSON file.

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON data or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to read JSON file {file_path}: {e}")
        return None


def safe_write_json(file_path: Path, data: Any) -> bool:
    """
    Safely write JSON file.

    Args:
        file_path: Path to JSON file
        data: Data to write

    Returns:
        True if successful
    """
    try:
        ensure_directory(file_path.parent)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        logger.error(f"Failed to write JSON file {file_path}: {e}")
        return False


def backup_file(file_path: Path) -> Optional[Path]:
    """
    Create backup of file.

    Args:
        file_path: Path to file

    Returns:
        Backup file path or None if failed
    """
    if not file_path.exists():
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_suffix(f".backup_{timestamp}{file_path.suffix}")

    try:
        shutil.copy2(file_path, backup_path)
        logger.info(f"Created backup: {backup_path}")
        return backup_path
    except Exception as e:
        logger.error(f"Failed to create backup of {file_path}: {e}")
        return None


def get_file_size(file_path: Path) -> int:
    """
    Get file size in bytes.

    Args:
        file_path: Path to file

    Returns:
        File size in bytes
    """
    return file_path.stat().st_size if file_path.exists() else 0


def humanize_size(size_bytes: int) -> str:
    """
    Convert bytes to human-readable size.

    Args:
        size_bytes: Size in bytes

    Returns:
        Human-readable size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"