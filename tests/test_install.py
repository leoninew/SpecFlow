import importlib.util
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

SCRIPT = Path(__file__).parents[1] / "scripts" / "install.py"
SPEC = importlib.util.spec_from_file_location("specflow_install", SCRIPT)
assert SPEC is not None
assert SPEC.loader is not None
install: Any = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = install
SPEC.loader.exec_module(install)


def test_command_failure_message_includes_stdout_and_stderr() -> None:
    completed = subprocess.CompletedProcess(
        ["claude", "plugin", "list", "--json"],
        1,
        stdout="partial response\n",
        stderr="connection failed\n",
    )

    message = install.command_failure_message(
        install.ClientTarget("claude", "claude"),
        ("plugin", "list", "--json"),
        completed,
    )

    assert message.endswith("partial response\nconnection failed\n")


def test_plan_codex_removes_invalid_marketplace_and_retries() -> None:
    target = install.ClientTarget("codex", "codex")
    runner = FakeCodexRunner(
        target,
        install.CommandError(
            target,
            ("plugin", "marketplace", "list", "--json"),
            subprocess.CompletedProcess(
                ["codex"],
                1,
                stdout="",
                stderr=(
                    "Error: failed to load marketplace(s):\n"
                    "- `stale-marketplace` at D:\\missing: "
                    "marketplace root does not contain a supported manifest\n"
                ),
            ),
        ),
    )

    plan = install.plan_codex(install.configured_release().plugins[0], target, runner)

    assert runner.changes == [
        ("plugin", "marketplace", "remove", "stale-marketplace", "--json")
    ]
    assert plan.selector == "specflow@specflow-local"


def test_plan_codex_prompts_for_manual_marketplace_repair() -> None:
    target = install.ClientTarget("codex", "codex")
    runner = FakeCodexRunner(
        target,
        install.CommandError(
            target,
            ("plugin", "marketplace", "list", "--json"),
            subprocess.CompletedProcess(
                ["codex"],
                1,
                stdout="",
                stderr="Error: failed to load marketplace(s): remote catalog is unavailable\n",
            ),
        ),
    )

    with pytest.raises(
        install.SyncError, match="Repair the failing Codex marketplace"
    ) as error:
        install.plan_codex(install.configured_release().plugins[0], target, runner)

    assert "remote catalog is unavailable" in str(error.value)


class FakeCodexRunner:
    def __init__(self, target: install.ClientTarget, first_response: Exception) -> None:
        self.target = target
        self.first_response = first_response
        self.calls = 0
        self.changes: list[tuple[str, ...]] = []

    def inspect(self, target: install.ClientTarget, arguments: tuple[str, ...]) -> Any:
        assert target == self.target
        assert arguments == ("plugin", "marketplace", "list", "--json")
        self.calls += 1
        if self.calls == 1:
            raise self.first_response
        return {"marketplaces": []}

    def change(self, target: install.ClientTarget, arguments: tuple[str, ...]) -> None:
        assert target == self.target
        self.changes.append(arguments)
