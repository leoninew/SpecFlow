ROOT_DIR := $(CURDIR)
SKILL_SOURCE_DIR := $(ROOT_DIR)/.claude/skills/specflow
CLAUDE_SKILL_TARGET_DIR := $(HOME)/.claude/skills/specflow
CODEX_SKILL_TARGET_DIR := $(HOME)/.codex/skills/specflow

.PHONY: help install dev check build release clean

help:
	@printf '%s\n' 'Targets:'
	@printf '%s\n' '  install  Install package and development dependencies'
	@printf '%s\n' '  dev      Start interactive Python shell with package loaded'
	@printf '%s\n' '  check    Run lint and typecheck'
	@printf '%s\n' '  build    Build source and wheel distributions'
	@printf '%s\n' '  release  Install package in editable mode and sync skill files'
	@printf '%s\n' '  clean    Clean build artifacts'

install:
	python -m pip install -e ".[dev]"

dev:
	uv run python -m specflow

check:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy .

build:
	python -m build

release:
	python -m pip install -e .
	@test -f '$(SKILL_SOURCE_DIR)/SKILL.md' || { printf '%s\n' 'Missing skill source: $(SKILL_SOURCE_DIR)/SKILL.md' >&2; exit 1; }
	mkdir -p '$(CLAUDE_SKILL_TARGET_DIR)' '$(CODEX_SKILL_TARGET_DIR)'
	rsync -av '$(SKILL_SOURCE_DIR)'/ '$(CLAUDE_SKILL_TARGET_DIR)'/ --del
	rsync -av '$(SKILL_SOURCE_DIR)'/ '$(CODEX_SKILL_TARGET_DIR)'/ --del
	@printf '%s\n' 'Installed specflow package in editable mode.'
	@printf '%s\n' 'Synced specflow skill files to $(CLAUDE_SKILL_TARGET_DIR)'
	@printf '%s\n' 'Synced specflow skill files to $(CODEX_SKILL_TARGET_DIR)'

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache dist build *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
