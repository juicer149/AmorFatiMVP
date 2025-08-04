# activity_factory.py

import os
from datetime import datetime
from typing import Optional, Dict, Any, Union
from dataclasses import dataclass

import yaml

from .activity import Activity, MetaActivity
from .activity_tools import parse_clock_time, to_unix_time


# Constants (consider moving to constants.py in future)
DEFAULT_SOURCE = "manual"


def load_yaml(path: str) -> dict:
    """
    Load a YAML file from disk.

    This function performs no semantic validation.
    It simply parses and returns the raw contents.

    Parameters
    ----------
    path : str
        Absolute or relative file path.

    Returns
    -------
    dict
        Parsed YAML data.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"No file found at path: {path}")
    if not path.endswith(".yaml"):
        raise ValueError(f"Expected a YAML file, but got: {path}")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"Error parsing YAML file {path}: {e}") from e


def load_config(name: str) -> dict:
    """
    Load configuration for a specific activity by name.

    Looks for ./configs/{name}.yaml and parses its content.

    Returns
    -------
    dict
        The raw YAML config.
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 

    if not name:
        raise ValueError("Activity name must be provided.")

    path = os.path.join(BASE_DIR, "configs", f"{name}.yaml")
    return load_yaml(path)


@dataclass
class ActivityFactory:
    """
    ActivityFactory – constructs (Meta)Activity objects from either YAML or direct input.

    This factory enables structured creation of semantic-free core events,
    optionally enriched with context. It supports both production usage (YAML-driven)
    and test or ad-hoc scenarios (manual input).

    Fields
    ------
    - name     : Name of the activity, e.g., "run"
    - amount   : Quantity of the activity, e.g., 30
    - clock    : Optional time string in "HH:MM" format; falls back to current time
    - meta     : Optional metadata dict (emotion, intensity, etc.)
    - unit     : Required only if `use_yaml=False`
    - use_yaml : If True, expects a config file in `./configs/{name}.yaml`

    Example
    -------
    # From YAML config (default)
    ActivityFactory(name="run", amount=20).build()

    # Manual, YAML-free mode
    ActivityFactory(name="read", amount=15, unit="pages", use_yaml=False).build()

    Examples:
        >>> from activity.activity_factory import ActivityFactory
        >>> af = ActivityFactory(name="read", amount=10, unit="pages", use_yaml=False)
        >>> a = af.build()
        >>> type(a).__name__
        'Activity'

        >>> af = ActivityFactory(name="meditate", amount=20, unit="minutes", meta={"mood": "calm"}, use_yaml=False)
        >>> m = af.build()
        >>> type(m).__name__
        'MetaActivity'
    """

    name: str
    amount: int
    clock: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
    unit: Optional[str] = None
    use_yaml: bool = True

    def build(self) -> Union[Activity, MetaActivity]:
        """
        Build a core Activity or a context-enriched MetaActivity.

        Returns
        -------
        Activity or MetaActivity depending on whether meta is provided.

        Raises
        ------
        ValueError if configuration is incomplete or invalid.
        """
        if self.use_yaml:
            config = load_config(self.name)
            unit = config.get("unit")
            if not unit:
                raise ValueError(f"Config for '{self.name}' must define a 'unit'.")
        else:
            if not self.unit:
                raise ValueError("Field 'unit' must be provided if YAML is disabled.")
            unit = self.unit

        dt = self._resolve_time(self.clock)
        unix_time = to_unix_time(dt)

        base = Activity(
            name=self.name,
            unit=unit,
            amount=self.amount,
            unix_time=unix_time,
        )

        if not self.meta:
            return base

        meta_data = dict(self.meta)
        meta_data.setdefault("source", DEFAULT_SOURCE)

        return MetaActivity(base=base, meta=meta_data)

    def _resolve_time(self, clock: Optional[str]) -> datetime:
        """
        Convert a clock string to a timezone-aware datetime.

        If no clock is given, current system time is used.

        Parameters
        ----------
        clock : str or None
            Format: "HH:MM"

        Returns
        -------
        datetime
            Local datetime representing the intended time.

        
        Examples:
            >>> ActivityFactory(name="test", amount=1, unit="x", use_yaml=False)._resolve_time("12:30").hour
            12
        """
        if clock:
            return parse_clock_time(clock)
        return datetime.now().astimezone()
