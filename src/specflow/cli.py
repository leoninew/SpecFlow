from pathlib import Path

import click

PROTOCOL_FILES = ("requirement.md", "spec.md", "plan.md", "verification.md")
PROTOCOL_STAGES = tuple(filename.removesuffix(".md") for filename in PROTOCOL_FILES)


@click.group(
    invoke_without_command=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)
@click.pass_context
def main(ctx: click.Context) -> None:
    """SpecFlow: a skill-first development protocol for coding agents."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@main.command()
def init() -> None:
    """Initialize project-local SpecFlow folders and templates."""
    docs_dir = Path("docs")
    template_dir = Path(".specflow") / "template"

    docs_dir.mkdir(exist_ok=True)
    template_dir.mkdir(parents=True, exist_ok=True)

    for filename in PROTOCOL_FILES:
        target = template_dir / filename
        if not target.exists():
            target.write_text(_template(filename), encoding="utf-8")

    click.echo("Initialized docs/ and .specflow/template/.")


@main.command()
def status() -> None:
    """Show SpecFlow document status for each feature."""
    docs_dir = Path("docs")
    if not docs_dir.exists():
        click.echo("No docs/ directory found. Run `specflow init` first.")
        return

    features = _features(docs_dir)
    if not features:
        click.echo("No SpecFlow feature documents found in docs/.")
        return

    for feature_name, documents in features:
        click.echo(f"docs/{feature_name}:")
        for stage in PROTOCOL_STAGES:
            click.echo(f"  {stage:<12} {_document_status(documents.get(stage))}")


def _features(docs_dir: Path) -> list[tuple[str, dict[str, Path]]]:
    stage_features: dict[str, dict[str, Path]] = {}
    for stage in PROTOCOL_STAGES:
        stage_dir = docs_dir / stage
        if not stage_dir.is_dir():
            continue
        for path in sorted(stage_dir.glob("*.md")):
            stage_features.setdefault(path.stem, {})[stage] = path

    if stage_features:
        return sorted(stage_features.items())

    flat_features: dict[str, dict[str, Path]] = {}
    for path in sorted(docs_dir.glob("*.md")):
        parsed = _flat_document(path)
        if parsed is None:
            continue
        feature_name, stage = parsed
        flat_features.setdefault(feature_name, {})[stage] = path

    if flat_features:
        return sorted(flat_features.items())

    directory_features = []
    for path in sorted(docs_dir.iterdir()):
        if not path.is_dir():
            continue
        documents = {
            filename.removesuffix(".md"): path / filename
            for filename in PROTOCOL_FILES
            if (path / filename).exists()
        }
        if documents:
            directory_features.append((path.name, documents))

    return directory_features


def _flat_document(path: Path) -> tuple[str, str] | None:
    stem = path.stem
    for stage in PROTOCOL_STAGES:
        suffix = f"-{stage}"
        if stem.endswith(suffix) and stem[: -len(suffix)]:
            return stem[: -len(suffix)], stage
    return None


def _template(filename: str) -> str:
    path = Path(__file__).resolve().parents[2] / ".claude" / "skills" / "specflow" / "template" / filename
    return path.read_text(encoding="utf-8")


def _document_status(path: Path | None) -> str:
    if path is None or not path.exists():
        return "missing"

    content = path.read_text(encoding="utf-8").strip()
    if not content:
        return "empty"

    review_status = _review_status(content)
    if review_status:
        return review_status

    return "present"


def _review_status(content: str) -> str | None:
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if line.strip().lower() != "## review status":
            continue

        for candidate in lines[index + 1 :]:
            stripped = candidate.strip()
            if not stripped:
                continue
            if stripped.startswith("#"):
                return "unknown"
            return stripped

        return "unknown"

    return None
