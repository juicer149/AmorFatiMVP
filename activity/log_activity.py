# log_activity.py

import argparse
from .activity_factory import ActivityFactory
from .jsonl_logger import log_event


def main():
    parser = argparse.ArgumentParser(description="Log an activity.")
    parser.add_argument("name", type=str, help="Name of the activity (e.g., run)")
    parser.add_argument("amount", type=int, help="Amount performed (e.g., 30)")
    parser.add_argument("--clock", type=str, help="Time in HH:MM format")
    parser.add_argument("--meta", nargs="*", help="Optional meta as key=value pairs")
    parser.add_argument("--unit", type=str, help="Unit (if not using YAML)")
    parser.add_argument("--no-yaml", action="store_true", help="Disable YAML config")

    args = parser.parse_args()

    # Parse meta key=value pairs into dictionary
    meta = {}
    if args.meta:
        for pair in args.meta:
            if "=" in pair:
                key, val = pair.split("=", 1)
                try:
                    meta[key] = eval(val)  # type-aware (e.g., 1.2 → float)
                except Exception:
                    meta[key] = val  # fallback to string

    factory = ActivityFactory(
        name=args.name,
        amount=args.amount,
        clock=args.clock,
        meta=meta or None,
        unit=args.unit,
        use_yaml=not args.no_yaml
    )

    activity = factory.build()
    log_event(activity)
    print(f"Logged: {activity}")


if __name__ == "__main__":
    main()

