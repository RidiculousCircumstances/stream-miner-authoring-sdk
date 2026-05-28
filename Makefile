PYTHON ?= python3
NPM ?= npm
PYTHON_WHEEL_DIR ?= /tmp/stream-miner-authoring-sdk-python-wheel
PYTHON_CHECK_VENV ?= /tmp/stream-miner-authoring-sdk-python-check

.PHONY: verify verify-python verify-javascript pack-python pack-javascript clean-python-check

verify: verify-python verify-javascript

verify-python: clean-python-check
	mkdir -p $(PYTHON_WHEEL_DIR)
	$(PYTHON) -m pip wheel ./python --wheel-dir $(PYTHON_WHEEL_DIR) --no-deps
	$(PYTHON) -m venv $(PYTHON_CHECK_VENV)
	$(PYTHON_CHECK_VENV)/bin/python -m pip install --upgrade pip mypy
	$(PYTHON_CHECK_VENV)/bin/python -m pip install $(PYTHON_WHEEL_DIR)/stream_miner_sdk_stubs-*.whl
	$(PYTHON_CHECK_VENV)/bin/python -m mypy --config-file python/mypy.ini python/tests/fixture_parser.py

verify-javascript:
	cd javascript && $(NPM) ci
	cd javascript && $(NPM) run typecheck

pack-python: clean-python-check
	mkdir -p $(PYTHON_WHEEL_DIR)
	$(PYTHON) -m pip wheel ./python --wheel-dir $(PYTHON_WHEEL_DIR) --no-deps
	ls -lh $(PYTHON_WHEEL_DIR)

pack-javascript:
	cd javascript && $(NPM) ci
	cd javascript && $(NPM) run pack:dry-run

clean-python-check:
	rm -rf $(PYTHON_WHEEL_DIR) $(PYTHON_CHECK_VENV)
