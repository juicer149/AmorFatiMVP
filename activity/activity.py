# activity.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict


# Energeia
@dataclass(frozen=True, slots=True)
class Activity:
    """
    Activity — a minimal, immutable record of a real-world event.

    This structure represents the bare occurrence of something that happened:
        - What:   the type or name of the event
        - How:    the measurement unit and amount
        - When:   the Unix timestamp of the event

    No interpretation, context, or human meaning is included here.
    This is the "black box" model: an objective log suitable for alien observers,
    a kernel trace, or any system that captures facts without valuing them.

    Examples: {"run", "time", 30, 1721155200} is as true in Paris as on Mars.
    """

    name: str
    unit: str
    amount: int
    unix_time: float

    # --------------------- Validation and Initialization ---------------------
    # In this layer we keep it simple and strict, if the validation becomes complex,
    # we can move it up to the factory or a separate validation function.

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Activity.name must be a non-empty string")
        if not isinstance(self.unit, str) or not self.unit.strip():
            raise ValueError("Activity.unit must be a non-empty string")
        if not isinstance(self.amount, int) or self.amount < 0:
            raise ValueError("Activity.amount must be a non-negative integer")
        if not isinstance(self.unix_time, (int, float)):
            raise ValueError("Activity.unix_time must be a number")

    # --------------------- String Representation ---------------------

    def __str__(self) -> str:
        return f"Activity('{self.name}', {self.amount} {self.unit}) @ {int(self.unix_time)}"

    def __repr__(self) -> str:
        return (
            f"Activity(name={self.name!r}, unit={self.unit!r}, amount={self.amount}, "
            f"unix_time={self.unix_time})"
        )


# Symbebekos 
@dataclass(frozen=True, slots=True)
class MetaActivity:
    """
    MetaActivity — an Activity enriched with contextual or interpretive data.

    This structure adds human-relevant metadata around a core factual event.
    The metadata may include intensity, streak, environment, emotion, location, 
    intention, or other semantic annotations that are meaningful to human observers.

    Philosophically, this mirrors the difference between:
        - what happened (Activity), and
        - what it meant (meta)

    While an alien system could parse an Activity, it would require a mind
    to interpret a MetaActivity. This distinction keeps the core log unambiguous,
    while allowing for rich, extensible meaning layers.
    """

    base: Activity
    meta: Dict[str, Any] = field(default_factory=dict)


    # --------------------- Validation and Initialization ---------------------
    # Here we ensure that the base is a valid Activity and meta is a dictionary

    def __post_init__(self):
        for k, v in self.meta.items():
            if not isinstance(v, (str, int, float, bool, list, dict, type(None))):
                raise TypeError(f"meta[{k!r}] has unsupported type: {type(v).__name__}")

        if not isinstance(self.base, Activity):
            raise TypeError("MetaActivity.base must be an instance of Activity")


    # ------------------------ String Representation --------------------------

    def __str__(self) -> str:
        return f"{self.base} +meta"

    def __repr__(self) -> str:
        return f"MetaActivity(base={self.base!r}, meta={self.meta})"

    # ------------------------ Factory Methods --------------------------

    def with_meta(self, **kwargs: Any) -> MetaActivity:
        """Return a new MetaActivity with updated or extended metadata."""
        new_meta = {**self.meta, **kwargs}
        return MetaActivity(base=self.base, meta=new_meta)

