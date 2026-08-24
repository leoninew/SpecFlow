import re
from pathlib import Path

import pytest

from specflow.cli import _update_template_timestamp, main


def test_help_options_show_help(capsys: pytest.CaptureFixture[str]) -> None:
    for option in ("--help", "-h"):
        with pytest.raises(SystemExit) as error:
            main([option])

        assert error.value.code == 0
        output = capsys.readouterr().out
        assert (
            "SpecFlow: a skill-first development protocol for coding agents." in output
        )
        assert "init" in output
        assert "status" in output


def test_no_command_shows_help(capsys: pytest.CaptureFixture[str]) -> None:
    result = main([])

    output = capsys.readouterr().out
    assert result == 0
    assert "SpecFlow: a skill-first development protocol for coding agents." in output
    assert "init" in output
    assert "status" in output


def test_init_creates_docs_and_project_templates(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tmp_path)

    result = main(["init"])

    output = capsys.readouterr().out
    assert result == 0
    assert "Initialized docs/ and .specflow/template/." in output
    assert Path("docs").is_dir()
    for filename in (
        "requirement.md",
        "spec.md",
        "plan.md",
        "verification.md",
    ):
        content = Path(".specflow/template", filename).read_text(encoding="utf-8")
        assert re.search(
            r"^最后修改时间: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",
            content,
            re.MULTILINE,
        )
    assert not Path("plugins/specflow/skills/specflow").exists()


def test_update_template_timestamp_leaves_missing_line_unchanged(
    tmp_path: Path,
) -> None:
    target = tmp_path / "requirement.md"
    content = "# Requirement\n\n## Review status\n\nDraft\n"
    target.write_text(content, encoding="utf-8")

    _update_template_timestamp(target)

    assert target.read_text(encoding="utf-8") == content


def test_status_reports_review_status_and_missing_stage_directory_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tmp_path)
    requirement_dir = Path("docs/requirement")
    spec_dir = Path("docs/spec")
    requirement_dir.mkdir(parents=True)
    spec_dir.mkdir(parents=True)
    (requirement_dir / "20260609-specflow-rename.md").write_text(
        "# Requirement\n\n## Review status\n\nDraft\n", encoding="utf-8"
    )
    (spec_dir / "20260609-specflow-rename.md").write_text(
        "# Spec\n\n## Review status\n\nAccepted\n", encoding="utf-8"
    )

    result = main(["status"])

    output = capsys.readouterr().out
    assert result == 0
    assert "docs/20260609-specflow-rename:" in output
    assert "requirement  Draft" in output
    assert "spec         Accepted" in output
    assert "plan         missing" in output
    assert "verification missing" in output


def test_status_falls_back_to_flat_protocol_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tmp_path)
    docs = Path("docs")
    docs.mkdir()
    (docs / "20260609-specflow-rename-requirement.md").write_text(
        "# Requirement\n\n## Review status\n\nDraft\n", encoding="utf-8"
    )

    result = main(["status"])

    output = capsys.readouterr().out
    assert result == 0
    assert "docs/20260609-specflow-rename:" in output
    assert "requirement  Draft" in output
    assert "spec         missing" in output


def test_status_handles_missing_docs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tmp_path)

    result = main(["status"])

    output = capsys.readouterr().out
    assert result == 0
    assert "No docs/ directory found" in output
