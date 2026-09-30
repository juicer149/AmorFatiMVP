PYTHON := python3

.PHONY: demo doctest check run-demo

demo:
	$(PYTHON) -m event.demo

doctest:
	$(PYTHON) -m doctest -v event/event.py event/event_tools.py

check:
	$(PYTHON) -m compileall -q .
	$(PYTHON) -m doctest -v event/event.py event/event_tools.py

run-demo:
	$(PYTHON) -m event.log_event run 30
