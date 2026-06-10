from pathlib import Path

from click.testing import CliRunner

from specflow.cli import main


def test_help_options_show_help() -> None:
    runner = CliRunner()

    for option in ("--help", "-h"):
        result = runner.invoke(main, [option])

        assert result.exit_code == 0
        assert "SpecFlow: a skill-first development protocol for coding agents." in result.output
        assert "init" in result.output
        assert "status" in result.output


def test_no_command_shows_help() -> None:
    runner = CliRunner()

    result = runner.invoke(main, [])

    assert result.exit_code == 0
    assert "SpecFlow: a skill-first development protocol for coding agents." in result.output
    assert "init" in result.output
    assert "status" in result.output


def test_init_creates_docs_and_project_templates() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(main, ["init"])

        assert result.exit_code == 0
        assert Path("docs").is_dir()
        assert Path(".specflow/template/requirement.md").is_file()
        assert Path(".specflow/template/spec.md").is_file()
        assert Path(".specflow/template/plan.md").is_file()
        assert Path(".specflow/template/verification.md").is_file()
        assert not Path(".claude/skills/specflow.md").exists()


def test_status_reports_review_status_and_missing_stage_directory_files() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
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

        result = runner.invoke(main, ["status"])

        assert result.exit_code == 0
        assert "docs/20260609-specflow-rename:" in result.output
        assert "requirement  Draft" in result.output
        assert "spec         Accepted" in result.output
        assert "plan         missing" in result.output
        assert "verification missing" in result.output


def test_status_falls_back_to_flat_protocol_files() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        docs = Path("docs")
        docs.mkdir()
        (docs / "20260609-specflow-rename-requirement.md").write_text(
            "# Requirement\n\n## Review status\n\nDraft\n", encoding="utf-8"
        )

        result = runner.invoke(main, ["status"])

        assert result.exit_code == 0
        assert "docs/20260609-specflow-rename:" in result.output
        assert "requirement  Draft" in result.output
        assert "spec         missing" in result.output



def test_status_handles_missing_docs() -> None:
    runner = CliRunner()

    with runner.isolated_filesystem():
        result = runner.invoke(main, ["status"])

        assert result.exit_code == 0
        assert "No docs/ directory found" in result.output
