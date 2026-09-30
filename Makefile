PYTHON := python3

.PHONY: test doctest check run-demo

test:
	$(PYTHON) -m event.test_attr_log

doctest:
	$(PYTHON) -m doctest -v event/event.py event/event_tools.py

check:
	$(PYTHON) -m compileall -q .
	$(PYTHON) -m doctest -v event/event.py event/event_tools.py

run-demo:
	$(PYTHON) -m event.log_event run 30
