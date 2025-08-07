# event.py

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass(frozen=True, slots=True)
class Event:
    """
    Event – a minimal, immutable record of something that occurred.

    Fields:
        - name   : str   – event type/name (e.g. "study")
        - amount : float – how much of the event occurred
        - unix_time : float – when it occurred (seconds since epoch)

    Example:
        >>> Event(name="study", amount=10, unix_time=1721155200)
        Event(name='study', amount=10, unix_time=1721155200)
    """
    name: str
    amount: float
    unix_time: float

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Event.name must be a non-empty string")
        if not isinstance(self.amount, (int, float)) or self.amount < 0:
            raise ValueError("Event.amount must be a non-negative number")
        if not isinstance(self.unix_time, (int, float)):
            raise ValueError("Event.unix_time must be a number")

    def __repr__(self) -> str:
        return f"Event(name={self.name!r}, amount={self.amount}, unix_time={self.unix_time})"

    def __str__(self) -> str:
        return f"Event('{self.name}', {self.amount}) @ {int(self.unix_time)}"


@dataclass(frozen=True, slots=True)
class EventMeta:
    """
    EventMeta – contextualized Event, enriched from YAML config and user meta.

    Fields:
        - event   : Event                – the core event
        - unit    : str                  – measurement unit (from YAML)
        - value   : float                – base value/weight (from YAML)
        - calc    : str                  – calculation method (from YAML)
        - meta    : Dict[str, Any]       – meta attributes and user input
        - config  : Dict[str, Any]       – full config snapshot at instantiation

    Example:
        >>> e = Event(name="study", amount=10, unix_time=1721155200)
        >>> meta = EventMeta(event=e, unit="pages", value=2.0, calc="linear", meta={"focus": 1.1}, config={"unit": "pages", "value": 2.0, "calc": "linear"})
        >>> str(meta)
        "Event('study', 10) @ 1721155200 +meta"
        >>> meta.meta["focus"]
        1.1
    """
    event: Event
    unit: str
    value: float
    calc: str
    meta: Dict[str, Any] = field(default_factory=dict)
    config: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not isinstance(self.event, Event):
            raise TypeError("EventMeta.event must be an Event instance")
        if not isinstance(self.unit, str) or not self.unit.strip():
            raise ValueError("EventMeta.unit must be a non-empty string")
        if not isinstance(self.value, (int, float)):
            raise ValueError("EventMeta.value must be numeric")
        if not isinstance(self.calc, str) or not self.calc.strip():
            raise ValueError("EventMeta.calc must be a non-empty string")
        if not isinstance(self.meta, dict):
            raise TypeError("EventMeta.meta must be a dict")
        if not isinstance(self.config, dict):
            raise TypeError("EventMeta.config must be a dict")

    def __repr__(self) -> str:
        return f"EventMeta(event={self.event!r}, unit={self.unit!r}, value={self.value}, calc={self.calc!r}, meta={self.meta}, config={self.config})"

    def __str__(self) -> str:
        return f"{self.event} +meta"
