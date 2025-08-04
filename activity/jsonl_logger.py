# jsonl_logger_attributive.py

import json
from datetime import datetime
from pathlib import Path
from typing import Union
from .activity import Activity, MetaActivity

# Log directory using date-based rotation (one file per day).
LOG_DIR = Path("logs_attr")
LOG_DIR.mkdir(exist_ok=True)

def _log_path_for_today() -> Path:
    """
    Get the path to today's JSON Lines log file.

    The logs are rotated daily to facilitate diary-like review
    and make historical processing easier.
    """
    today_str = datetime.now().strftime("%Y-%m-%d")
    return LOG_DIR / f"{today_str}.jsonl"

def _as_pairs(event: Union[Activity, MetaActivity], event_id: float) -> list[dict]:
    """
    Serialize an event as a list of {id, key, value} records.

    Each attribute from the core activity and any optional metadata
    is split into its own atomic record, linked by a shared id (usually unix_time).

    Rationale:
    - Enables atomic, attribute-level data analysis.
    - Allows structural evolution without schema migration.
    - Decouples logic from shape; patterns emerge from values alone.
    """
    items = []

    if isinstance(event, MetaActivity):
        core = event.base
        meta = event.meta
    else:
        core = event
        meta = {}

    # Core attributes from the base activity
    # These could be given by a registry pattern in the future?
    for key in ["name", "unit", "amount", "unix_time"]:
        value = getattr(core, key)
        items.append({"id": event_id, "key": key, "value": value})

    # Optional metadata attributes
    for k, v in meta.items():
        items.append({"id": event_id, "key": k, "value": v})

    return items

def log_event(event: Union[Activity, MetaActivity]) -> None:
    """
    Log an activity as a set of key-value records in JSONL format.

    Each line represents a single attribute:
    {"id": 1754229600.0, "key": "name", "value": "run"}

    This structure makes it easier to analyze events as linked records,
    independent of future changes in the data model.
    """
    event_id = getattr(event, "unix_time", datetime.now().timestamp())
    path = _log_path_for_today()
    with path.open("a", encoding="utf-8") as f:
        for row in _as_pairs(event, event_id):
            json.dump(row, f)
            f.write("\n")

