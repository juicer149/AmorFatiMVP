# event/test_attr_log.py

from .event_factory import EventFactory
from .jsonl_logger import log_event


def main():
    event = EventFactory(name="run", amount=30).build()
    log_event(event)
    print("Event logged successfully.")
    print(event)


if __name__ == "__main__":
    main()
