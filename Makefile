ROOT_DIR := $(CURDIR)
SKILL_SOURCE_DIR := $(ROOT_DIR)/.claude/skills/specflow
CLAUDE_SKILL_TARGET_DIR := $(HOME)/.claude/skills/specflow
CODEX_SKILL_TARGET_DIR := $(HOME)/.codex/skills/specflow

.PHONY: help install skill test build

help:
	@printf '%s\n' 'Targets:'
	@printf '%s\n' '  install  Install package and development dependencies'
	@printf '%s\n' '  skill    Install package and sync skill files'
	@printf '%s\n' '  test     Run tests'
	@printf '%s\n' '  build    Build source and wheel distributions'

install:
	python -m pip install -e ".[dev]"

skill: install
	@test -f '$(SKILL_SOURCE_DIR)/SKILL.md' || { printf '%s\n' 'Missing skill source: $(SKILL_SOURCE_DIR)/SKILL.md' >&2; exit 1; }
	mkdir -p '$(CLAUDE_SKILL_TARGET_DIR)' '$(CODEX_SKILL_TARGET_DIR)'
	rsync -av '$(SKILL_SOURCE_DIR)'/ '$(CLAUDE_SKILL_TARGET_DIR)'/ --del
	rsync -av '$(SKILL_SOURCE_DIR)'/ '$(CODEX_SKILL_TARGET_DIR)'/ --del
	@printf '%s\n' 'Installed specflow package in editable mode.'
	@printf '%s\n' 'Synced specflow skill files to $(CLAUDE_SKILL_TARGET_DIR)'
	@printf '%s\n' 'Synced specflow skill files to $(CODEX_SKILL_TARGET_DIR)'

test:
	python -m pytest -q

build:
	python -m build
