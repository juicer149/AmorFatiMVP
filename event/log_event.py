# log_event.py

import argparse

from .event_factory import EventFactory
from .jsonl_logger import log_event


def parse_args():
    """
    Parse CLI arguments for event logging.

    Returns
    -------
    argparse.Namespace
        Parsed command-line arguments including name, amount, and clock.
    """
    parser = argparse.ArgumentParser(description="Log an event via CLI.")
    parser.add_argument("name", help="Event name, e.g., 'run'")
    parser.add_argument("amount", type=float, help="Amount of event")
    parser.add_argument(
        "--clock",
        help="Clock time in HH:MM format",
        default=None,
    )
    return parser.parse_args()


def main():
    """
    Entry point for CLI event logging.

    Builds the event via EventFactory and logs it in attributive format.

    Design rationale:
    - Delegates event construction to the factory for consistency.
    - Uses an attribute-centric logging model for composable logs.
    - Does not assume anything about higher-level interpretation.
    """
    args = parse_args()

    factory = EventFactory(
        name=args.name,
        amount=args.amount,
        clock=args.clock,
    )

    event = factory.build()
    log_event(event)

    print(f"Logged (attributive): {event}")


if __name__ == "__main__":
    main()
