# Recipes use POSIX shell commands; GNU Make with bash is required on Windows.
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c

.DEFAULT_GOAL := help

UV ?= uv
UV_RUN ?= $(UV) run --locked --no-sync
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

.PHONY: help deps install check test release

help: ## Show the public workflow.
	@printf "Available targets:\n"
	@printf "  deps            Sync locked project and development dependencies\n"
	@printf "  install         Install the editable CLI and sync agent plugins\n"
	@printf "  check [fix=1]   Check format, lint, and types\n"
	@printf "  test [cov=1]    Run unit tests; coverage HTML is written to htmlcov/\n"
	@printf "  release         Build source and wheel distributions\n"

deps: ## Sync the locked project and development dependencies.
	$(UV) sync --all-groups --locked

install: ## Install the user-level editable CLI and synchronize agent plugins.
	$(UV) tool install --editable . --force
	$(UV) run --locked python scripts/install.py plugin check
	$(UV) run --locked python scripts/install.py plugin apply

check: ## Check format, lint, and types; use fix=1 to apply fixes.
	$(UV_RUN) ruff format $(RUFF_FORMAT_ARGS) src tests
	$(UV_RUN) ruff check $(RUFF_CHECK_ARGS) src tests
	$(UV_RUN) mypy src

test: ## Run unit tests; cov=1 writes terminal and HTML coverage reports.
	$(UV_RUN) pytest tests $(TEST_COV_ARGS)

release: ## Build source and wheel distributions without publishing them.
	$(UV) build
