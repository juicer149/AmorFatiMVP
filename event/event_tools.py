"""
activity_tools.py

Helper functions for date/time parsing, Unix-time conversion.
Used by the factory layer to convert user input into precise timepoints.

Supports both absolute datetimes (e.g. "2024-07-18 12:00:00") and
relative clock times (e.g. "12:00" today in local timezone).
"""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def parse_clock_time(clock_str: str, tz: str = "UTC") -> datetime:
    """
    Parse a simple clock time (e.g. "14:30") as a datetime for today.

    Parameters
    ----------
    clock_str : str
        Time string in "HH:MM" format.
    tz : str
        IANA timezone name.

    Returns
    -------
    datetime
        Datetime object with today's date and given time in specified tz.

    Raises
    ------
    ValueError
        If the input format is invalid or timezone is unknown.

    Examples
    --------
    >>> dt = parse_clock_time("13:45", tz="Europe/Stockholm")
    >>> dt.hour == 13 and dt.minute == 45
    True
    """

    # Validate timezone
    try:
        hour, minute = map(int, clock_str.strip().split(":"))
        if not (0 <= hour < 24 and 0 <= minute < 60):
            raise ValueError("Invalid clock time")
    except Exception:
        raise ValueError(f"Invalid clock time format: {clock_str!r}")

    # Get current date in specified timezone
    now = datetime.now(ZoneInfo(tz))

    return datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        hour=hour,
        minute=minute,
        tzinfo=ZoneInfo(tz)
    )


def to_unix_time(dt: datetime) -> float:
    """
    Convert a timezone-aware datetime to Unix timestamp (UTC).

    Parameters
    ----------
    dt : datetime
        Input datetime. If naive, it is assumed to be UTC.

    Returns
    -------
    float
        Seconds since Unix epoch.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.timestamp()

