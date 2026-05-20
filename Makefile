PYTHON = python3
VENV = drone_venv
VENV_BIN = $(VENV)/bin
VENV_PYTHON = $(VENV)/bin/python3
VENV_PIP = $(VENV)/bin/pip

LINT_CHECK = main.py network.py parser.py pathfinder.py simulation.py visualiser.py

MAIN = main.py
MAP_FILE = challenger.txt

ifneq ($(words $(MAKECMDGOALS)),1)
MAP_FILE := $(word 2,$(MAKECMDGOALS))
$(eval $(MAP_FILE): ; @:)
endif

all: install run

$(VENV_PYTHON):
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)

install: $(VENV_PYTHON)
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install flake8
	$(VENV_PIP) install mypy

run: $(VENV_PYTHON)
	$(VENV_PYTHON) $(MAIN) $(MAP_FILE)

debug: $(VENV_PYTHON)
	$(VENV_PYTHON) -m pdb $(MAIN) $(MAP_FILE)

lint: $(VENV_PYTHON)
	$(VENV_PYTHON) -m flake8 $(LINT_CHECK)
	$(VENV_PYTHON) -m mypy --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs --check-untyped-defs $(LINT_CHECK)

lint-strict: $(VENV_PYTHON)
	$(VENV_PYTHON) -m flake8 $(LINT_CHECK)
	$(VENV_PYTHON) -m mypy --strict $(LINT_CHECK)

clean:
	rm -rf $(VENV) \
		__pycache__ \
		**/__pycache__/ \
		.mypy_cache/ \
		*.pyc \
		*.pyo \

re: clean install run

.PHONY: all install run debug clean lint lint-strict re

# .pyc → compiled bytecode files (created automatically by Python)
# .pyo → optimized bytecode (older Python versions, mostly obsolete now)
