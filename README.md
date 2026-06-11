# SpecFlow

**SpecFlow is a skill-first development protocol for coding agents.**

[中文说明](README.zh-CN.md)

SpecFlow gives coding agents a lightweight, reviewable process for software changes. It defines stage boundaries and document conventions; it does not replace the agent runtime that reads code, edits files, runs tests, or performs reviews.

## Flow modes

![SpecFlow development protocol flow models](docs/assets/specflow-flow-models.jpg)

- `strict`: for unclear, cross-module, or high-risk changes.
- `standard`: for ordinary feature work.
- `light`: for small, well-scoped changes.

Each mode keeps enough process record for humans and future agents to review what changed and why.

## Install

SpecFlow uses [uv](https://docs.astral.sh/uv/) and provides a Makefile.

Install dependencies:

```bash
make install
```

Install the package in editable mode and sync the SpecFlow skill files to both `~/.claude/skills/specflow/` and `~/.codex/skills/specflow/`:

```bash
make skill
```

## Use

Use SpecFlow as a skill in your coding agent workflow:

```text
Use /specflow to start this requirement.
```

The skill chooses a flow mode, writes the relevant process documents, and asks for review when a stage needs acceptance.

## CLI

The CLI is a setup and diagnostic helper for the skill, not the primary user interface:

```bash
specflow init
specflow status
```

Users normally start from `/specflow`. SpecFlow intentionally avoids command-driven workflow transitions such as `next` or `approve`; the skill manages the process through normal agent work.

## Documents

SpecFlow stores stage documents by feature:

```text
docs/requirement/<yyyymmdd>-<feature>.md
docs/spec/<yyyymmdd>-<feature>.md
docs/plan/<yyyymmdd>-<feature>.md
docs/verification/<yyyymmdd>-<feature>.md
```

New documents use only two review states: `Draft` and `Accepted`.

## Development

```bash
make test
```

Equivalent command:

```bash
uv run python -m pytest -q
```

## License

SpecFlow is released under the [MIT License](LICENSE).
