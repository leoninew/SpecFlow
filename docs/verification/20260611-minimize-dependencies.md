# Verification: minimize dependencies

## Review status

Draft

## What changed

- Replaced the Click-based CLI with a standard-library `argparse` implementation while preserving `specflow`, `specflow -h`, `specflow --help`, `specflow init`, and `specflow status` behavior.
- Updated CLI tests to use `pytest` fixtures (`tmp_path`, `monkeypatch`, `capsys`) instead of `click.testing.CliRunner`.
- Removed the `click` runtime dependency from `pyproject.toml`.
- Replaced the uv-specific development dependency group with standard `project.optional-dependencies.dev`.
- Added `build>=1.2` to the dev extra so standard packaging works through `python -m build` while retaining `hatchling` as the build backend.
- Updated README, Chinese README, and Makefile to use `python -m pip`, `python -m pytest`, and `python -m build` instead of uv commands.
- Removed `uv.lock` because uv is no longer the required project toolchain.
- Removed the tracked local permission allowlist entry for `Bash(uv run:*)`.

## Acceptance

- [x] `src/specflow/cli.py` no longer imports or depends on `click`.
- [x] `pyproject.toml` no longer declares `click` as a runtime dependency.
- [x] README, Chinese README, and Makefile no longer require `uv`.
- [x] Standard packaging remains available through `python -m build`.
- [x] Tests no longer use `click.testing.CliRunner`.
- [x] `specflow` no-argument help, `--help`, and `status` were checked.
- [x] Project tests pass after installing dev dependencies.

## Commands

- `python -m pytest -q`
  - Initial result: failed because the active Python environment did not have `pytest` installed.
- `python -m build`
  - Initial result: failed because the active Python environment did not have `build` installed.
- `python -m pip install -e ".[dev]"`
  - Result: passed; installed editable package plus `build` and `pytest` dev dependencies.
- `python -m pytest -q`
  - Result: passed, `6 passed in 0.03s`.
- `python -m build`
  - Result: passed; built `specflow-0.1.0.tar.gz` and `specflow-0.1.0-py3-none-any.whl`.
- `specflow --help`
  - Result: passed; printed argparse help with `init` and `status` commands.
- `specflow status`
  - Result: passed; listed current SpecFlow feature document statuses.
- `python -m specflow.cli --help`
  - Result: passed after adding the module entrypoint guard.
- `make test`
  - Result: not executed successfully in this environment because `make` is not installed (`/usr/bin/bash: line 1: make: command not found`).
- `make build`
  - Result: not executed successfully in this environment because `make` is not installed (`/usr/bin/bash: line 1: make: command not found`).

## Remaining risk

- Removing `uv.lock` means development dependency versions are no longer locked by uv; this is intentional for minimizing required tooling, but it reduces lockfile reproducibility.
- The project still documents Makefile targets, but this local environment does not have `make` installed. Equivalent Python commands were verified directly.
- `argparse` help formatting differs from Click formatting, so tests assert stable help content rather than exact output formatting.
