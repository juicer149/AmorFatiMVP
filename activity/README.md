# `activity/` – The Foundation of Event Logging

This package forms the semantic core of the Amor Fati system. Here, the most fundamental building blocks of a person's lived log are defined, created, and manipulated.

## Purpose

To distinguish **what happens** from **how it is interpreted**.

Or in Aristotelian terms:
- `Energeia` – what is (action)
- `Symbebēkos` – what follows (attribute, circumstance)

---

## Overview

```text
activity/
├── activity.py           # Defines Activity and MetaActivity
├── activity_factory.py   # Builds instances from YAML configuration
├── activity_tools.py     # Helpers for validation, transformation, etc.
├── jsonl_logger.py       # Flat JSONL logging (event-based)
├── test_attr_log.py      # CLI interface for testing attribute-logger
├── configs/
│   ├── meditate.yaml     # Example activity: meditation
│   └── run.yaml          # Example activity: running
```

---

## `activity.py`

Defines two central data classes:

* `Activity` – an objective, unembellished log: name, amount, unit, unix timestamp.
* `MetaActivity` – a contextualized `Activity` with arbitrary metadata (location, mood, weather...).

All semantics are moved out of the core – this is a **truthful** logging layer, free of interpretation.

---

## `activity_factory.py`

Creates `MetaActivity` from YAML configurations in `configs/`.

* Each YAML file holds an activity's *name*, *unit*, and optionally which `meta` fields to prompt.
* Example:

```yaml
# configs/run.yaml
unit: time
meta:
  intensity: 1.2
  weather: 0.1
  streak: 0.4
```

Weights are used *only* if logic is defined elsewhere (`economy`). Otherwise, metadata is recorded without interpretation.

---

## `jsonl_logger.py`

Provides two logging modes:

1. **Event-based (default)** – each log entry is a full JSON object:
   ```json
   {
     "name": "run",
     "unit": "time",
     "amount": 30,
     "unix_time": 1754229600.0,
     "meta": { "weather": "sunny", ... }
   }
   ```

2. **Attributive (experimental)** – each attribute is logged on its own line:
   ```json
   { "id": 1754229600.0, "key": "name", "value": "run" }
   { "id": 1754229600.0, "key": "unit", "value": "time" }
   ```

This enables log parsing as a *linked list* of atomic facts, decoupling structure from semantics. Ideal for machine learning or time-series pipelines.

Use `test_attr_log.py` to test this logic manually.

---

## `activity_tools.py`

Provides tools for:

* YAML validation
* transformation helpers
* future API integrations (e.g., weather, emotion recognition)

---

## `configs/`

Each `.yaml` represents an activity:

* `run.yaml` → `"run"` activity
* `meditate.yaml` → `"meditate"` activity

This separation allows semantic expansion without touching code.

---

## Philosophical Foundation

This layer is epistemologically minimalist:

> "That something happened" is not the same as understanding why.
> `activity/` only concerns itself with **what occurred**.

Interpretation is layered above (`economy`, `xp`, `praxēs`...).

---

## Usage

```python
from activity.activity_factory import build_meta_activity

meta = build_meta_activity("run", amount=30, unix_time=time.time())
```

---

## Forward

This is the layer upon which future languages may be built – NLP, statistics, self-reflection. But here, in `activity/`, reality speaks first.

