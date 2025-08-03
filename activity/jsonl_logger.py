# jsonl_logger.py

import json
from datetime import datetime
from pathlib import Path
from typing import Union
from dataclasses import asdict

from .activity import Activity, MetaActivity


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


def _log_path_for_today() -> Path:
    today_str = datetime.now().strftime("%Y-%m-%d")
    return LOG_DIR / f"{today_str}.jsonl"


def serialize(obj: Union[Activity, MetaActivity]) -> dict:
    """
    Serialize an Activity or MetaActivity to a flat dictionary for logging.

    The result contains all relevant fields from Activity and, if applicable,
    any metadata fields from MetaActivity.

    Parameters
    ----------
    obj : Activity or MetaActivity

    Returns
    -------
    dict
        Flat key-value mapping of the event.
    """
    if isinstance(obj, MetaActivity):
        return {
            **asdict(obj.base),
            **obj.meta,
        }
    elif isinstance(obj, Activity):
        return asdict(obj) 
    else:
        raise TypeError(f"Cannot serialize object of type {type(obj)}") # type: ignore[unreachable]


def log_event(event: Union[Activity, MetaActivity]) -> None:
    """
    Append a single event to today's log file in JSON Lines format.

    Parameters
    ----------
    event : Activity or MetaActivity
        The event object to serialize and log.
    """
    path = _log_path_for_today()
    with path.open("a", encoding="utf-8") as f:
        json.dump(serialize(event), f)
        f.write("\n")

