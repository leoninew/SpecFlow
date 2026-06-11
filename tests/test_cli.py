from pathlib import Path

import pytest

from specflow.cli import main


def test_help_options_show_help(capsys: pytest.CaptureFixture[str]) -> None:
    for option in ("--help", "-h"):
        with pytest.raises(SystemExit) as error:
            main([option])

        assert error.value.code == 0
        output = capsys.readouterr().out
        assert "SpecFlow: a skill-first development protocol for coding agents." in output
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
    assert Path(".specflow/template/requirement.md").is_file()
    assert Path(".specflow/template/spec.md").is_file()
    assert Path(".specflow/template/plan.md").is_file()
    assert Path(".specflow/template/verification.md").is_file()
    assert not Path(".claude/skills/specflow.md").exists()


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
