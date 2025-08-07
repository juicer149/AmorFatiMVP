````markdown name=README.md
# `event/` – The Foundation of Event Logging

This package forms the semantic core of the Amor Fati system. Here, the most fundamental building blocks of a person's lived log are defined, created, and manipulated.

**Note:** The folder was previously named `activity/` but is now renamed to `event/` to better reflect its role as a general log of all types of events, not just activities.

## Purpose

To distinguish **what happens** from **how it is interpreted**.

Or in Aristotelian terms:
- `Energeia` – what is (action)
- `Symbebēkos` – what follows (attribute, circumstance)

---

## Overview

```text
event/
├── event.py                # Defines Event and EventMeta
├── event_factory.py        # Builds instances from YAML configuration
├── event_tools.py          # Helpers for validation, transformation, etc.
├── jsonl_logger_attributive.py # Attributive JSONL logging (attribute-based)
├── test_attr_log.py        # CLI interface for testing attribute-logger
├── configs/
│   ├── meditate.yaml       # Example event: meditation
│   └── run.yaml            # Example event: running
```

---

## `event.py`

Defines two central data classes:

* `Event` – an objective, unembellished log: name, amount, unix timestamp.
* `EventMeta` – a contextualized `Event` enriched from YAML (unit, value, calc, meta fields).

All semantics are moved out of the core – this is a **truthful** logging layer, free of interpretation.

---

## `event_factory.py`

Creates `EventMeta` from YAML configurations in `configs/`.

* Each YAML file holds an event's *unit*, *value*, *calc*, and optionally which `meta` fields to prompt.
* Example:

```yaml
# configs/run.yaml
unit: time
value: 1.0
calc: linear
meta:
  intensity:
    prompt: "How intense was your run?"
    weight: 1.2
  weather:
    prompt: "What was the weather?"
    weight: 0.1
  streak:
    prompt: "Current streak?"
    weight: 0.4
```

Weights and prompts are used for flexible context; all calculation logic is centralized elsewhere (e.g., in `ScoreCalculator`). Metadata is recorded without hardcoded interpretation.

---

## `jsonl_logger_attributive.py`

Provides **attributive logging** mode:

- Each attribute is logged on its own line, linked by a shared event id:
   ```json
   { "id": 1754229600.0, "key": "name", "value": "run" }
   { "id": 1754229600.0, "key": "unit", "value": "time" }
   { "id": 1754229600.0, "key": "intensity", "value": 1.2 }
   ```

This enables log parsing as a *linked list* of atomic facts, decoupling structure from semantics. Ideal for machine learning or time-series pipelines.

Use `test_attr_log.py` to test this logic manually.

---

## `event_tools.py`

Provides tools for:

* YAML validation
* transformation helpers
* future API integrations (e.g., weather, emotion recognition)

---

## `configs/`

Each `.yaml` represents an event:

* `run.yaml` → `"run"` event
* `meditate.yaml` → `"meditate"` event

This separation allows semantic expansion without touching code.

---

## Philosophical Foundation

This layer is epistemologically minimalist:

> "That something happened" is not the same as understanding why.
> `event/` only concerns itself with **what occurred**.

Interpretation is layered above (`economy`, `xp`, `praxis`...).

---

## Usage

```python
from event.event_factory import EventFactory

event_meta = EventFactory(name="run", amount=30).build()
```

---

## Forward

This is the layer upon which future languages may be built – NLP, statistics, self-reflection. But here, in `event/`, reality speaks first.
````
