PYTHON  = python3
VENV = venv
VENV_PYTHON = $(VENV)/bin/python3
VENV_PIP = $(VENV)/bin/pip

# --- MANDATORY RULES ---

# 1. Install dependencies
# Checks if the 'venv' folder exists. If not, it creates it.
# Then it installs the package in editable mode inside that venv.
install:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating venv..."; \
		python3 -m venv $(VENV); \
	fi
	$(VENV_PIP) install -e .[dev]

# 2. Run the main program
# Uses $(PYTHON) which points to venv/bin/python3
run:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Please run 'make install' first."; \
		exit 1; \
	fi
	$(VENV_PYTHON) a_maze_ing.py config.txt

# 3. Debug mode
debug:
	$(VENV_PYTHON) -m pdb a_maze_ing.py config.txt

# 4. Clean up
# Now also removes the 'venv' folder so you can start fresh if needed
clean:
	rm -rf $(VENV)
	rm -rf __pycache__
	rm -rf src/mazegen/__pycache__/
	rm -rf .mypy_cache/
	rm -rf *.pyc
	rm -rf *.pyo
	rm -rf src/mazegen.egg-info/

# 5. Linting (Mandatory)
# Runs flake8 and mypy using the venv binaries
lint:
	$(VENV_PYTHON) -m flake8 .
	$(VENV_PYTHON) -m mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

# 6. Strict Linting (Optional)
lint-strict:
	$(VENV_PYTHON) -m flake8 **/*.py
	$(VENV_PYTHON) -m mypy --strict .

# Helper to avoid file conflicts
.PHONY: install run debug clean lint lint-strict


# • install: Install project dependencies using pip, uv, pipx, or any other package
# manager of your choice.
# • run: Execute the main script of your project (e.g., via Python interpreter).
# • debug: Run the main script in debug mode using Python’s built-in debugger (e.g.,
# pdb).
# • clean: Remove temporary files or caches (e.g., __pycache__, .mypy_cache) to
# keep the project environment clean.
# • lint: Execute the commands flake8 . and mypy . --warn-return-any
# --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs
# --check-untyped-defs
# • lint-strict (optional): Execute the commands flake8 . and mypy . --strict
