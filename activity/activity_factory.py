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
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_config(name: str) -> dict:
    """
    Load configuration for a specific activity by name.

    Looks for ./configs/{name}.yaml and parses its content.

    Returns
    -------
    dict
        The raw YAML config.
    """
    path = os.path.join("./configs", f"{name}.yaml")
    return load_yaml(path)


@dataclass
class ActivityFactory:
    """
    Factory for constructing Activity or MetaActivity instances.

    Responsibilities:
    - Loads and interprets YAML config for the activity.
    - Transforms input into concrete immutable objects.
    - Determines whether meta-data exists and wraps appropriately.

    Philosophy:
    - Input is fully structured; no prompting or validation.
    - Time is resolved deterministically.
    - Output is pure data: either Activity or MetaActivity.
    """

    name: str
    amount: int
    clock: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

    def build(self) -> Union[Activity, MetaActivity]:
        """
        Construct the activity object.

        Returns
        -------
        Activity or MetaActivity
        """
        config = load_config(self.name)

        unit = config.get("unit")
        if not unit:
            raise ValueError(f"Config for '{self.name}' must define a 'unit'.")

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
        Convert input clock string to a datetime object.

        If no clock is provided, use current system time.

        Parameters
        ----------
        clock : Optional[str]
            Clock time in format "HH:MM"

        Returns
        -------
        datetime
        """
        if clock:
            return parse_clock_time(clock)
        return datetime.now().astimezone()

