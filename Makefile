UV_CACHE := /goinfre/$(USER)/uv_cache
HF_HOME := /goinfre/$(USER)/hf_cache
LINT_CHECK = src/
export UV_CACHE
export HF_HOME

# UV_CACHE ?= /tmp/$(USER)/uv_cache
# HF_HOME ?= /tmp/$(USER)/hf_cache
# LINT_CHECK = src/
# export PATH := $(HOME)/.local/bin:$(PATH)
# export UV_CACHE
# export HF_HOME

install:
	mkdir -p $(UV_CACHE)
	mkdir -p $(HF_HOME)
	uv sync --cache-dir $(UV_CACHE)

run:
	uv run python -m src 2> stderr_log.txt

debug:
	uv run python -m pdb -m src

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf $(UV_CACHE)
	rm -rf $(HF_HOME)

lint:
	uv run flake8 $(LINT_CHECK)
	uv run mypy --warn-return-any --warn-unused-ignores \
	--ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs $(LINT_CHECK)

lint-strict:
	uv run flake8 $(LINT_CHECK)
	uv run mypy --strict $(LINT_CHECK)

re: clean install run

.PHONY: install run debug clean lint lint-strict re

# UV_CACHE_DIR=/goinfre/$USER/uv_cache uv add ./llm_sdk
