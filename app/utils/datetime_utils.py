"""
Date and time utility functions.
"""

import logging
from datetime import date, datetime, time, timedelta
from typing import Optional, Tuple
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)


def get_local_timezone() -> ZoneInfo:
    """Get local timezone."""
    return ZoneInfo("localtime")


def now_local() -> datetime:
    """Get current local datetime."""
    return datetime.now(get_local_timezone())


def combine_date_time(
    date_value: date,
    time_value: Optional[time] = None,
) -> datetime:
    """
    Combine date and time into datetime.

    Args:
        date_value: Date
        time_value: Time (optional, defaults to midnight)

    Returns:
        Combined datetime
    """
    if time_value is None:
        time_value = time.min

    return datetime.combine(date_value, time_value)


def parse_date(date_str: str) -> date:
    """
    Parse date string.

    Args:
        date_str: Date string in ISO format (YYYY-MM-DD)

    Returns:
        Parsed date
    """
    return date.fromisoformat(date_str)


def parse_time(time_str: str) -> time:
    """
    Parse time string.

    Args:
        time_str: Time string in ISO format (HH:MM)

    Returns:
        Parsed time
    """
    return time.fromisoformat(time_str)


def parse_datetime(datetime_str: str) -> datetime:
    """
    Parse datetime string.

    Args:
        datetime_str: Datetime string in ISO format

    Returns:
        Parsed datetime
    """
    return datetime.fromisoformat(datetime_str)


def format_date(date_value: date) -> str:
    """Format date for display."""
    return date_value.strftime("%B %d, %Y")


def format_time(time_value: time) -> str:
    """Format time for display."""
    return time_value.strftime("%I:%M %p")


def format_datetime(datetime_value: datetime) -> str:
    """Format datetime for display."""
    return datetime_value.strftime("%B %d, %Y at %I:%M %p")


def is_today(date_value: date) -> bool:
    """Check if date is today."""
    return date_value == date.today()


def is_tomorrow(date_value: date) -> bool:
    """Check if date is tomorrow."""
    return date_value == date.today() + timedelta(days=1)


def is_overdue(
    due_date: date,
    due_time: Optional[time] = None,
) -> bool:
    """
    Check if task is overdue.

    Args:
        due_date: Due date
        due_time: Due time (optional)

    Returns:
        True if overdue
    """
    now = datetime.now()

    if due_time:
        due_datetime = datetime.combine(due_date, due_time)
        return due_datetime < now
    else:
        return due_date < now.date()


def get_week_range(target_date: Optional[date] = None) -> Tuple[date, date]:
    """
    Get start and end of week for target date.

    Args:
        target_date: Target date (defaults to today)

    Returns:
        Tuple of (week_start, week_end)
    """
    if target_date is None:
        target_date = date.today()

    week_start = target_date - timedelta(days=target_date.weekday())
    week_end = week_start + timedelta(days=6)

    return week_start, week_end


def get_month_range(
    year: int,
    month: int,
) -> Tuple[date, date]:
    """
    Get start and end of month.

    Args:
        year: Year
        month: Month (1-12)

    Returns:
        Tuple of (month_start, month_end)
    """
    month_start = date(year, month, 1)

    if month == 12:
        month_end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        month_end = date(year, month + 1, 1) - timedelta(days=1)

    return month_start, month_end


def humanize_time_difference(diff: timedelta) -> str:
    """
    Convert timedelta to human-readable string.

    Args:
        diff: Time difference

    Returns:
        Human-readable string
    """
    total_seconds = int(diff.total_seconds())

    if total_seconds < 60:
        return f"{total_seconds} seconds"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''}"
    elif total_seconds < 86400:
        hours = total_seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''}"
    else:
        days = total_seconds // 86400
        return f"{days} day{'s' if days != 1 else ''}"
