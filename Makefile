PYTHON  = python3
VENV = drone_venv
VENV_BIN= $(VENV)/bin
VENV_PYTHON = $(VENV)/bin/python3
VENV_PIP = $(VENV)/bin/pip

MAIN = main.py
MAP_FILE = /home/wcheung/git-fly/maps/hard/02_capacity_hell.txt

# PY_FILES := main.py network.py parser.py \
# 			engine.py pathfinder.py visualiser.py

# OK := \033[0;32mOK\033[0m
# KO := \033[0;31mKO\033[0m

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

# benchmark:
# 	@echo "========================================"
# 	@echo "Running Fly-in Performance Benchmarks"
# 	@echo "========================================"
# 	@echo ""
# 	@check_result() { \
# 		target=$$1; \
# 		if [ $$steps -le $$target ]; then \
# 			echo "≤$$target $(OK)"; \
# 			passed=$$((passed + 1)); \
# 		else \
# 			echo "≤$$target $(KO) (exceeded by $$((steps - target)))"; \
# 			failed=$$((failed + 1)); \
# 		fi; \
# 	}; \
# 	total=0; passed=0; failed=0; \
# 	for py_path in $$(find ./maps -type f -iname '*.txt' | sort); do \
# 		py_file=$$(basename "$$py_path"); \
# 		difficulty=$$(dirname "$$py_path" | xargs basename); \
# 		echo "Testing: $$py_file [$$difficulty]"; \
# 		steps=$$($(VENV_PYTHON) $(MAIN) "$$py_path" | wc -l); \
# 		printf "  Result: $$steps steps | Target: "; \
# 		total=$$((total + 1)); \
# 		case $$py_file in \
# 			01_linear_path.txt) check_result 6 ;; \
# 			02_simple_fork.txt) check_result 6 ;; \
# 			03_basic_capacity.txt) check_result 8 ;; \
# 			01_dead_end_trap.txt) check_result 15 ;; \
# 			02_circular_loop.txt) check_result 20 ;; \
# 			03_priority_puzzle.txt) check_result 12 ;; \
# 			01_maze_nightmare.txt) check_result 45 ;; \
# 			02_capacity_hell.txt) check_result 60 ;; \
# 			03_ultimate_challenge.txt) check_result 35 ;; \
# 			01_the_impossible_dream.txt) check_result 45 ;; \
# 		esac; \
# 		echo ""; \
# 	done; \
# 	echo "========================================"; \
# 	echo "Benchmark Summary"; \
# 	echo "========================================"; \
# 	echo "Total tests: $$total"; \
# 	echo "Passed: $$passed $(OK)"; \
# 	echo "Failed: $$failed $(KO)"; \
# 	if [ $$failed -eq 0 ]; then \
# 		echo ""; \
# 		echo "🎉 All benchmarks passed!"; \
# 	fi

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
