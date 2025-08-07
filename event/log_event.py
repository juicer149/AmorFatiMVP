# log_event.py

import argparse
from .event_factory import EventFactory
from .jsonl_logger import log_event  # Attribute-based logger


def parse_args():
    """
    Parse CLI arguments for event logging.

    Returns
    -------
    argparse.Namespace
        Parsed command-line arguments including name, amount, clock, and unit.
    """
    parser = argparse.ArgumentParser(description="Log an event via CLI.")
    parser.add_argument("name", help="Event name, e.g., 'run'")
    parser.add_argument("amount", type=int, help="Amount of event")
    parser.add_argument("--clock", help="Clock time in HH:MM format", default=None)
    parser.add_argument("--unit", help="Override unit (disables YAML config)")
    return parser.parse_args()


def main():
    """
    Entry point for CLI event logging.

    Builds the event via EventFactory and logs it in attributive format
    using jsonl_logger_attributive.

    Design rationale:
    - Delegates event construction to the factory for consistency.
    - Uses an attribute-centric logging model for more composable, pattern-friendly logs.
    - Does not assume anything about the higher system (economy, xp, etc).
    """
    args = parse_args()

    factory = EventFactory(
        name=args.name,
        amount=args.amount,
        clock=args.clock,
        unit=args.unit,
        use_yaml=(args.unit is None),
    )

    event = factory.build()
    log_event(event)

    print(f"Logged (attributive): {event}")

if __name__ == "__main__":
    main()

