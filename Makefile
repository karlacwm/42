PYTHON  = python3
VENV = drone_venv
VENV_BIN = $(VENV)/bin
VENV_PYTHON = $(VENV)/bin/python3
VENV_PIP = $(VENV)/bin/pip

LINT_CHECK = main.py network.py parser.py pathfinder.py simulation.py visualiser.py

MAIN = main.py
MAP_FILE = maps/challenger/01_the_impossible_dream.txt

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

test: $(VENV_PYTHON)
	$(VENV_PYTHON) $(MAIN) maps/easy/01_linear_path.txt
	@echo "Target is less than 6 turns"
	@echo "========================================"
	$(VENV_PYTHON) $(MAIN) maps/easy/02_simple_fork.txt
	@echo "Target is less than 6 turns"
	@echo "========================================"
	$(VENV_PYTHON) $(MAIN) maps/easy/03_basic_capacity.txt
	@echo "Target is less than 8 turns"
	@echo "========================================"

	$(VENV_PYTHON) $(MAIN) maps/medium/01_dead_end_trap.txt
	@echo "Target is less than 15 turns"
	@echo "========================================"
	$(VENV_PYTHON) $(MAIN) maps/medium/02_circular_loop.txt
	@echo "Target is less than 20 turns"
	@echo "========================================"
	$(VENV_PYTHON) $(MAIN) maps/medium/03_priority_puzzle.txt
	@echo "Target is less than 12 turns"
	@echo "========================================"

	$(VENV_PYTHON) $(MAIN) maps/hard/01_maze_nightmare.txt
	@echo "Target is less than 45 turns"
	@echo "========================================"
	$(VENV_PYTHON) $(MAIN) maps/hard/02_capacity_hell.txt
	@echo "Target is less than 60 turns"
	@echo "========================================"
	$(VENV_PYTHON) $(MAIN) maps/hard/03_ultimate_challenge.txt
	@echo "Target is less than 35 turns"
	@echo "========================================"

	$(VENV_PYTHON) $(MAIN) maps/challenger/01_the_impossible_dream.txt
	@echo "Target is less than 45 turns"

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

.PHONY: all install run debug clean lint lint-strict test re

# .pyc → compiled bytecode files (created automatically by Python)
# .pyo → optimized bytecode (older Python versions, mostly obsolete now)
