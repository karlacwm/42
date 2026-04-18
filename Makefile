PYTHON  = python3
VENV = drone_venv
VENV_BIN= $(VENV)/bin
VENV_PYTHON = $(VENV)/bin/python3
VENV_PIP = $(VENV)/bin/pip

MAIN = main.py
MAP_FILE = maps/easy/01_linear_path.txt

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

# test-maps: $(VENV_PYTHON)
# 	@set -e; \
# 	for map in $$(find maps -type f -name '*.txt' | sort); do \
# 		echo "Testing $$map"; \
# 		$(VENV_PYTHON) -c "from parser import MapParser; from visualiser import Visualiser; p = MapParser('$$map'); p.parse(); Visualiser(p.network, 1700, 1200, 60).scale()"; \
# 	done; \
# 	echo "All maps validated."

lint: $(VENV_PYTHON)
	$(VENV_PYTHON) -m flake8 .
	$(VENV_PYTHON) -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict: $(VENV_PYTHON)
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

.PHONY: all install run debug clean lint lint-strict test-maps re

# .pyc → compiled bytecode files (created automatically by Python)
# .pyo → optimized bytecode (older Python versions, mostly obsolete now)
