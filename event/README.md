# `event/` — The Foundation of Event Logging

The `event` package is the semantic core of the third Amor Fati experiment.

It represents a shift from activity-specific tracking toward a more general
event model: first record what happened, then let higher layers interpret it.

The package was previously named `activity/` and was renamed to `event/` during
the final refactor.

## Core model

`Event` is a minimal immutable record containing:

- `name`
- `amount`
- `unix_time`

`EventMeta` wraps an `Event` with configuration and optional contextual
metadata:

- `unit`
- `value`
- `calc`
- `meta`
- a snapshot of the YAML configuration

Both are immutable dataclasses using `frozen=True` and `slots=True`.

## Event factory

`EventFactory` builds an `EventMeta` from a small amount of user input and a
YAML configuration stored in `configs/`.

Example:

```python
from event.event_factory import EventFactory

event = EventFactory(name="run", amount=30).build()
```

The corresponding YAML file supplies configuration such as the event unit,
base value, calculation mode and optional metadata specification.

## Attributive JSONL logging

`jsonl_logger.py` stores an event as atomic key/value records linked by the
event's Unix timestamp.

For example:

```json
{"id": 1754229600.0, "key": "name", "value": "run"}
{"id": 1754229600.0, "key": "amount", "value": 30}
{"id": 1754229600.0, "key": "unix_time", "value": 1754229600.0}
```

Optional values from `EventMeta.meta` are written as additional records using
the same event id.

This was an experiment in keeping the stored representation simple and
attribute-oriented rather than committing to a fixed event schema.

## Time helpers

`event_tools.py` contains helpers for:

- parsing an `HH:MM` clock time
- attaching a timezone
- converting datetimes to Unix timestamps

## CLI

An event can be logged from the repository root with:

```bash
python3 -m event.log_event run 30
```

An optional clock time can also be supplied:

```bash
python3 -m event.log_event study 12 --clock 14:30
```

Logs are written to daily JSONL files under `logs_attr/`.

## Configuration

The repository contains example YAML definitions for:

- `run`
- `study`
- `meditate`

The configurations reflect the experimental state of the project. Some were
left incomplete while the event model was being developed.

## Philosophical foundation

The central idea was to distinguish what happened from how it should later be
interpreted.

In the terminology used during development:

- `Energeia` — what is or what occurred
- `Symbebēkos` — attributes or circumstances that follow

The event layer therefore attempts to record observations first and defer
scoring, interpretation and higher-level meaning to later layers.

## Verification

Run:

```bash
make check
```

This compiles the project and runs the original doctest-style verification.

## Historical restoration

This repository has been preserved close to its original 2025 state.

The restoration only:

- repaired the CLI after the final `activity` → `event` refactor
- aligned the CLI with the final `EventFactory` API
- allowed fractional event amounts
- corrected stale package and logger references
- added a small Makefile for repeatable verification
- documented the implemented behavior without completing unfinished ideas

The experimental data model and YAML configurations were otherwise left
intact.

## Project lineage

1. `RUTINHANTERARE` — first routine tracker and scoring CLI, 2024
2. `amor_fati` — YAML-driven activity model and catalog experiment, 2025
3. `AmorFatiMVP` — immutable event model and attributive JSONL logging, 2025

A later Django training-log project continued exploring related ideas.

## Status

Historical project preserved as the third stage of the Amor Fati project line.
