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

SpecFlow uses standard Python packaging tools and provides a Makefile.

Install the package and development dependencies:

```bash
make install
```

Install the package in editable mode and sync the SpecFlow skill files to both `~/.claude/skills/specflow/` and `~/.codex/skills/specflow/`:

```bash
make release
```

## Use

SpecFlow's primary interface is the coding-agent skill, such as `/specflow` in Claude Code, not the CLI. The CLI is only for setup and diagnostics.

When a conversation is ready to become a tracked software change, tell the agent which flow mode to use and which stage to start from.

### Choose a flow mode

- `strict`: for unclear requirements, cross-module work, or high-risk changes. Flow: Requirement → Spec → Plan → Implementation → Verification.
- `standard`: for ordinary feature work. Flow: Requirement → Plan → Implementation → Verification.
- `light`: for small, clearly scoped changes. Flow: Requirement → Implementation → Verification.

Light mode still keeps moderately clarified Requirement and Verification records, so the work does not become undocumented direct coding.

### Start the flow

Discuss the requirement with the agent first. Clarify the goal, constraints, examples, and edge cases in normal conversation. When you are ready to enter the flow, invoke `/specflow`. The agent creates or updates the stage document and asks you to review it. Stage documents use two states: `Draft` and `Accepted`.

Start strict mode from Requirement:

```text
Use /specflow strict: keep log files for 7 days, start Requirement.
```

Start standard mode from Requirement:

```text
Use /specflow standard: add report export, start Requirement.
```

Start light mode for a small, clearly scoped change from Requirement:

```text
Use /specflow light: make all modal dialogs use the same Cancel and Confirm button order, start Requirement.
```

During the Requirement stage, if there are assumptions, risks, or open questions, the agent lists them in the stage document and in its reply. If you still ask to continue, SpecFlow records them as risks or assumptions and moves to the target stage. When starting light mode from Requirement, the agent should only create or update the requirement draft and ask for review; it should not implement and verify in the same turn unless you explicitly ask to "implement and verify" or "run the full light flow."

### Move through stages

During review, reply naturally. You do not need command-style transitions like `next` or `approve`; just say what should change, or which stage you want to enter.

Accept the current requirement and start Spec:

```text
Looks good, start Spec.
```

Accept the current requirement and start Plan:

```text
Accepted, start Plan.
```

Accept the prerequisite stage, enter Implementation, and keep the work within the accepted scope:

```text
Confirmed, start Implementation.
```

### Handoff

After implementation is done, ask the agent to enter Verification:

```text
Looks good, start Verification.
```

SpecFlow does not automatically run `git add`, `git commit`, or `git push`.

## CLI

The CLI is a setup and diagnostic helper for the skill, not the primary user interface:

```bash
specflow init
specflow status
```

For normal feature work, start from `/specflow`; use the CLI only for setup and status diagnostics.

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

Build source and wheel distributions:

```bash
make build
```

## License

SpecFlow is released under the [MIT License](LICENSE).
