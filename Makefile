# Recipes use POSIX shell commands; GNU Make with bash is required on Windows.
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c

.DEFAULT_GOAL := help

UV ?= uv
ARGS ?=
CHECK_FIX := $(filter 1 true yes,$(fix))
TEST_COV_ARGS :=
RUFF_FORMAT_ARGS := --check
RUFF_CHECK_ARGS :=

ifneq ($(CHECK_FIX),)
RUFF_FORMAT_ARGS :=
RUFF_CHECK_ARGS := --fix
endif

ifneq ($(filter 1 true yes,$(cov)),)
TEST_COV_ARGS := --cov=src/specflow --cov-report=term-missing --cov-report=html
endif

.PHONY: help deps install dev check test release clean

help: ## Show the public workflow.
	@printf "Available targets:\n"
	@printf "  deps            Sync locked development dependencies\n"
	@printf "  install         Install the editable CLI and sync agent plugins\n"
	@printf "  dev             Run the SpecFlow CLI, optionally with ARGS='...'\n"
	@printf "  check [fix=1]   Check format, lint, and types\n"
	@printf "  test [cov=1]    Run unit tests, optionally with coverage\n"
	@printf "  release         Build source and wheel distributions\n"
	@printf "  clean           Remove explicitly listed local artifacts\n"

deps: ## Sync locked development dependencies without installing the project.
	$(UV) sync --all-groups --locked --no-install-project

install: ## Install the user-level editable CLI and synchronize agent plugins.
	$(UV) tool install --editable . --force
	@command -v specflow >/dev/null || { \
		printf "specflow is not visible on PATH after uv tool install; add the directory from 'uv tool dir --bin' and restart the shell.\n" >&2; \
		exit 1; \
	}
	$(UV) run --locked python scripts/release.py plugin check
	$(UV) run --locked python scripts/release.py plugin apply

dev: ## Run the SpecFlow CLI, optionally with ARGS='...'.
	$(UV) run --locked specflow $(ARGS)

check: ## Check format, lint, and types; use fix=1 to apply fixes.
	$(UV) run --locked ruff format $(RUFF_FORMAT_ARGS) src tests
	$(UV) run --locked ruff check $(RUFF_CHECK_ARGS) src tests
	$(UV) run --locked mypy src

test: ## Run unit tests; use cov=1 to collect coverage.
	$(UV) run --locked pytest tests scripts/test_release.py $(TEST_COV_ARGS)

release: ## Build source and wheel distributions without publishing them.
	$(UV) build

clean: ## Remove explicitly listed local artifacts.
	rm -rf build dist .pytest_cache .ruff_cache .mypy_cache htmlcov .coverage *.egg-info
