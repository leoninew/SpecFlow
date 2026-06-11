# Requirement / 需求：open-source-readiness

## Review status

Accepted

## Mode / 模式

light / 轻量

## Goal

- Prepare the repository for public open-source release.
- Rewrite `README.md` in English as the default project introduction.
- Add a Chinese README in a separate file and cross-link both language versions.
- Add an MIT license.
- Add a small number of maintainable diagrams for the project concept and workflow.
- Check for obvious sensitive information before delivery.
- Provide suggested GitHub description/About text and topics after completion.

## Non-goal

- Do not publish the repository or push changes to any remote.
- Do not create a release, upload to PyPI, or reserve package names.
- Do not introduce large community governance files unless needed for this round.
- Do not change SpecFlow protocol behavior or CLI behavior.

## Acceptance

- `README.md` is primarily English and suitable for a GitHub landing page.
- A Chinese README exists in a separate file and both README files link to each other.
- `LICENSE` contains the MIT license.
- Project metadata reflects the MIT license and improves discoverability where appropriate.
- Documentation includes a small number of GitHub-renderable diagrams.
- Sensitive information scan finds no obvious secrets or records any remaining risk.
- Final response includes GitHub description/About and topics, with English first and Chinese second.

## Risk

- License selection is a project/legal decision; user selected MIT for this task.
- Secret scanning by regex is not a substitute for a full history audit or dedicated secret-scanning service.
- GitHub About and Topics are recommendations only; they must be entered manually in GitHub unless the user later authorizes GitHub operations.
- `specflow status` currently recognizes `## Review status`; this document uses that exact heading for diagnostic compatibility.
