# event_factory.py

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
import os
import yaml

from .event import Event, EventMeta
from .event_tools import parse_clock_time, to_unix_time

CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configs")

@dataclass
class EventFactory:
    """
    EventFactory – builds EventMeta from minimal user input + YAML config.

    Input:
        - name  : str – name of the event (e.g., "study")
        - amount: float – how much of the event occurred
        - clock : optional "HH:MM" string (default: now)
        - meta_values: optional dict of meta (e.g., {"focus": 1.1})

    Output:
        - EventMeta – enriched, contextualized event with config snapshot

    Flow:
        1. Loads configs/{name}.yaml → gets unit, value, calc, meta-spec
        2. Resolves time
        3. Wraps everything into EventMeta for downstream scoring/logging
    """
    name: str
    amount: float
    clock: Optional[str] = None
    meta_values: Optional[Dict[str, Any]] = None

    def build(self) -> EventMeta:
        # Step 1: Load YAML config
        config_path = os.path.join(CONFIG_DIR, f"{self.name}.yaml")
        if not os.path.isfile(config_path):
            raise FileNotFoundError(f"No config found for event: {self.name}")
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        unit = config["unit"]
        value = config["value"]
        calc = config.get("calc", "linear")
        meta_spec = config.get("meta", {})

        # Step 2: Resolve time
        dt = self._resolve_time(self.clock)
        unix_time = to_unix_time(dt)

        event = Event(name=self.name, amount=self.amount, unix_time=unix_time)

        # Step 3: Wrap everything into EventMeta with config snapshot
        meta_values = self.meta_values or {}

        return EventMeta(
            event=event,
            unit=unit,
            value=value,
            calc=calc,
            meta=meta_values,
            config=config,
        )

    def _resolve_time(self, clock: Optional[str]) -> datetime:
        if clock:
            return parse_clock_time(clock)
        return datetime.now().astimezone()
