SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

SKILL_SOURCE_DIR := .claude/skills/specflow
CLAUDE_SKILL_TARGET_DIR := $(HOME)/.claude/skills/specflow
CODEX_SKILL_TARGET_DIR := $(HOME)/.codex/skills/specflow
ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))

.PHONY: help install dev check test build release clean

help:
	@printf "Available targets:\n"
	@printf "  install  Install development dependencies\n"
	@printf "  dev      Run specflow CLI, optionally with ARGS='...'\n"
	@printf "  check    Run ruff and mypy checks\n"
	@printf "  test     Run pytest\n"
	@printf "  build    Build source and wheel distributions\n"
	@printf "  release  Install package and sync skill files\n"
	@printf "  clean    Remove local build and cache artifacts\n"

install:
	uv sync --group dev

dev:
	uv run specflow $(ARGS)

check:
	uv run ruff check --fix src tests
	uv run ruff format src tests
	uv run mypy src

test:
	uv run pytest

build:
	python -m build

release:
	pip install -e .
	test -f "$(SKILL_SOURCE_DIR)/SKILL.md" || { printf '%s\n' "Missing skill source: $(SKILL_SOURCE_DIR)/SKILL.md" >&2; exit 1; }
	mkdir -p "$(CLAUDE_SKILL_TARGET_DIR)" "$(CODEX_SKILL_TARGET_DIR)"
	rsync -av "$(SKILL_SOURCE_DIR)"/ "$(CLAUDE_SKILL_TARGET_DIR)"/ --del
	rsync -av "$(SKILL_SOURCE_DIR)"/ "$(CODEX_SKILL_TARGET_DIR)"/ --del
	printf '%s\n' "Installed specflow package in editable mode."
	printf '%s\n' "Synced specflow skill files to $(CLAUDE_SKILL_TARGET_DIR)"
	printf '%s\n' "Synced specflow skill files to $(CODEX_SKILL_TARGET_DIR)"

clean:
	find . -type d -name "__pycache__" -not -path "./.git/*" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -not -path "./.git/*" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -not -path "./.git/*" -exec rm -rf {} +
	rm -rf dist build *.egg-info
	rm -f .coverage

%:
	@:
