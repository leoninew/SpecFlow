ROOT_DIR := $(CURDIR)
VENV_DIR := $(ROOT_DIR)/.venv
SKILL_SOURCE_DIR := $(ROOT_DIR)/.claude/skills/specflow
SKILL_TARGET_DIR := $(HOME)/.claude/skills/specflow

.PHONY: help sync install test

help:
	@printf '%s\n' 'Targets:'
	@printf '%s\n' '  sync       Install uv dependencies'
	@printf '%s\n' '  install    Install specflow package and sync skill files'
	@printf '%s\n' '  test       Run tests'

sync:
	uv sync

install:
	@if [ ! -d '$(VENV_DIR)' ]; then uv sync; fi
	pip install -e .
	@test -f '$(SKILL_SOURCE_DIR)/SKILL.md' || { printf '%s\n' 'Missing skill source: $(SKILL_SOURCE_DIR)/SKILL.md' >&2; exit 1; }
	mkdir -p '$(SKILL_TARGET_DIR)'
	rsync -av '$(SKILL_SOURCE_DIR)'/ '$(SKILL_TARGET_DIR)'/ --del
	@printf '%s\n' 'Installed specflow package in editable mode.'
	@printf '%s\n' 'Synced specflow skill files to $(SKILL_TARGET_DIR)'

test:
	uv run python -m pytest -q
