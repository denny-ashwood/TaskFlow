"""
Input validation utilities.
"""

import logging
import re
from datetime import date, datetime, time
from typing import Any, Optional

logger = logging.getLogger(__name__)


def validate_title(title: str) -> tuple[bool, Optional[str]]:
    """
    Validate task title.

    Args:
        title: Task title

    Returns:
        Tuple of (is_valid, error_message)
    """
    title = title.strip()

    if not title:
        return False, "Title cannot be empty"

    if len(title) > 255:
        return False, "Title cannot exceed 255 characters"

    return True, None


def validate_date(date_value: Any) -> tuple[bool, Optional[str]]:
    """
    Validate date value.

    Args:
        date_value: Date value

    Returns:
        Tuple of (is_valid, error_message)
    """
    if date_value is None:
        return True, None

    if isinstance(date_value, date):
        return True, None

    if isinstance(date_value, str):
        try:
            date.fromisoformat(date_value)
            return True, None
        except ValueError:
            return False, "Invalid date format (use YYYY-MM-DD)"

    return False, f"Invalid date type: {type(date_value)}"


def validate_time(time_value: Any) -> tuple[bool, Optional[str]]:
    """
    Validate time value.

    Args:
        time_value: Time value

    Returns:
        Tuple of (is_valid, error_message)
    """
    if time_value is None:
        return True, None

    if isinstance(time_value, time):
        return True, None

    if isinstance(time_value, str):
        try:
            time.fromisoformat(time_value)
            return True, None
        except ValueError:
            return False, "Invalid time format (use HH:MM)"

    return False, f"Invalid time type: {type(time_value)}"


def validate_priority(priority: str) -> tuple[bool, Optional[str]]:
    """
    Validate task priority.

    Args:
        priority: Priority value

    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_priorities = {'low', 'medium', 'high'}

    if priority not in valid_priorities:
        return False, f"Invalid priority: {priority}. Valid values: {valid_priorities}"

    return True, None


def validate_status(status: str) -> tuple[bool, Optional[str]]:
    """
    Validate task status.

    Args:
        status: Status value

    Returns:
        Tuple of (is_valid, error_message)
    """
    valid_statuses = {'pending', 'completed', 'cancelled'}

    if status not in valid_statuses:
        return False, f"Invalid status: {status}. Valid values: {valid_statuses}"

    return True, None


def validate_reminder_minutes(minutes: Any) -> tuple[bool, Optional[str]]:
    """
    Validate reminder minutes.

    Args:
        minutes: Reminder minutes

    Returns:
        Tuple of (is_valid, error_message)
    """
    if minutes is None:
        return True, None

    if not isinstance(minutes, int):
        return False, "Reminder minutes must be an integer"

    if minutes < 0:
        return False, "Reminder minutes cannot be negative"

    if minutes > 10080:  # 1 week
        return False, "Reminder minutes cannot exceed 1 week"

    return True, None


def validate_email(email: str) -> tuple[bool, Optional[str]]:
    """
    Validate email address.

    Args:
        email: Email address

    Returns:
        Tuple of (is_valid, error_message)
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not re.match(email_pattern, email):
        return False, "Invalid email address"

    return True, None