import re
from pathlib import Path

import pytest

from specflow.cli import _update_template_timestamp, main


def _write_document(tmp_path: Path, layout: str, stage: str, content: str) -> Path:
    feature = "20260609-specflow-rename"
    relative_path = {
        "stage-directory": f"{stage}/{feature}.md",
        "flat-file": f"{feature}-{stage}.md",
        "feature-directory": f"{feature}/{stage}.md",
    }[layout]
    path = tmp_path / "docs" / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


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
    filenames = (
        "intent.md",
        "plan.md",
        "verification.md",
        "task.md",
        "handoff.md",
    )
    assert {path.name for path in Path(".specflow/template").iterdir()} == set(
        filenames
    )
    for filename in filenames:
        content = Path(".specflow/template", filename).read_text(encoding="utf-8")
        assert re.search(
            r"^最后修改时间: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",
            content,
            re.MULTILINE,
        )
    assert not Path("plugins/specflow/skills/specflow").exists()
    assert not list(Path("docs").iterdir())


def test_init_preserves_existing_templates_and_historical_documents(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    template_dir = Path(".specflow/template")
    template_dir.mkdir(parents=True)
    custom_intent = b"# Custom intent\nLast edited manually\n"
    legacy_spec = b"# Historical spec\nKeep this content\n"
    (template_dir / "intent.md").write_bytes(custom_intent)
    (template_dir / "spec.md").write_bytes(legacy_spec)
    history = _write_document(tmp_path, "stage-directory", "spec", "Historical design")
    history_bytes = history.read_bytes()

    assert main(["init"]) == 0
    assert (template_dir / "intent.md").read_bytes() == custom_intent
    assert (template_dir / "spec.md").read_bytes() == legacy_spec
    assert (template_dir / "task.md").is_file()
    assert (template_dir / "handoff.md").is_file()
    first_init = {path.name: path.read_bytes() for path in template_dir.iterdir()}

    assert main(["init"]) == 0
    assert {
        path.name: path.read_bytes() for path in template_dir.iterdir()
    } == first_init
    assert history.read_bytes() == history_bytes


def test_update_template_timestamp_leaves_missing_line_unchanged(
    tmp_path: Path,
) -> None:
    target = tmp_path / "intent.md"
    content = "# Intent\n\n## Review status\n\nDraft\n"
    target.write_text(content, encoding="utf-8")

    _update_template_timestamp(target)

    assert target.read_text(encoding="utf-8") == content


@pytest.mark.parametrize(
    "layout", ["stage-directory", "flat-file", "feature-directory"]
)
@pytest.mark.parametrize("heading", ["## Review status", "## Review status / 审查状态"])
def test_status_reports_three_stages_for_supported_layouts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    layout: str,
    heading: str,
) -> None:
    monkeypatch.chdir(tmp_path)
    _write_document(tmp_path, layout, "intent", f"# Intent\n\n{heading}\n\nDraft\n")
    _write_document(tmp_path, layout, "plan", f"# Plan\n\n{heading}\n\nAccepted\n")
    for auxiliary in ("spec", "task", "handoff"):
        _write_document(tmp_path, layout, auxiliary, f"{heading}\n\nAccepted\n")

    assert main(["status"]) == 0

    assert capsys.readouterr().out == (
        "docs/20260609-specflow-rename:\n"
        "  intent       Draft\n"
        "  plan         Accepted\n"
        "  verification missing\n"
    )


@pytest.mark.parametrize(
    "layout", ["stage-directory", "flat-file", "feature-directory"]
)
def test_status_does_not_discover_features_from_legacy_or_auxiliary_documents(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    layout: str,
) -> None:
    monkeypatch.chdir(tmp_path)
    for auxiliary in ("spec", "task", "handoff"):
        _write_document(tmp_path, layout, auxiliary, "## Review status\n\nAccepted\n")

    assert main(["status"]) == 0

    assert capsys.readouterr().out == "No SpecFlow feature documents found in docs/.\n"


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        ("", "empty"),
        ("# Intent\n\nReview status: Accepted\n", "present"),
        ("## Review status notes\n\nAccepted\n", "present"),
        ("## Review status / Other\n\nAccepted\n", "present"),
        ("## Review status\n\n", "unknown"),
        ("## Review status / 审查状态\n\n## Goals\n\nAccepted\n", "unknown"),
        ("## Review status\n\nApproved\n", "Approved"),
        ("  ## REVIEW STATUS / 审查状态  \n\nAccepted\n", "Accepted"),
    ],
)
def test_status_preserves_diagnostics_and_requires_a_review_heading(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    content: str,
    expected: str,
) -> None:
    monkeypatch.chdir(tmp_path)
    document = _write_document(tmp_path, "stage-directory", "verification", content)
    original = document.read_bytes()

    assert main(["status"]) == 0

    output = capsys.readouterr().out
    assert f"  verification {expected}\n" in output
    assert document.read_bytes() == original


def test_status_handles_missing_docs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tmp_path)

    result = main(["status"])

    output = capsys.readouterr().out
    assert result == 0
    assert "No docs/ directory found" in output
