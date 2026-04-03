PYTHON  = python3
VENV = drone_venv
VENV_BIN= $(VENV)/bin
VENV_PYTHON = $(VENV)/bin/python3
VENV_PIP = $(VENV)/bin/pip

# MAIN = a_maze_ing.py
# CONFIG = config.txt

all: install run

$(VENV_BIN)/$(PYTHON):
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV)

install: $(VENV_BIN)/$(PYTHON)
# 	cd mazegen && $(abspath $(VENV_PIP)) install -e .[dev]
# 	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install flake8
	$(VENV_PIP) install mypy
# 	$(VENV_PIP) install pydantic

run: $(VENV_BIN)/$(PYTHON)
# 	$(VENV_PYTHON) $(MAIN) $(CONFIG)

debug: $(VENV_BIN)/$(PYTHON)
# 	$(VENV_PYTHON) -m pdb $(MAIN) $(CONFIG)

lint: $(VENV_BIN)/$(PYTHON)
	$(VENV_PYTHON) -m flake8 .
	$(VENV_PYTHON) -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict: $(VENV_BIN)/$(PYTHON)
	$(VENV_PYTHON) -m flake8 **/*.py
	$(VENV_PYTHON) -m mypy --strict .

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
