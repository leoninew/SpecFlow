# Scope note: minimize dependencies

## Review status

Accepted

## Goal

评估并实施依赖最小化：移除运行时依赖 `click`，并移除项目对 `uv` 作为必需开发工具的约束，使项目安装、测试和 CLI 运行尽量依赖 Python 标准工具链。

## Non-goal

- 不改变 SpecFlow skill 协议语义或文档流程。
- 不移除 `pytest` 作为开发/测试依赖，除非后续明确要求。
- 不强制移除构建后端 `hatchling`；它属于构建依赖，不是运行时依赖。
- 不移除标准打包能力；`uv build` 应替换为 `python -m build`。
- 不增加新的第三方运行时依赖。

## Acceptance

- `src/specflow/cli.py` 不再 import 或依赖 `click`。
- `pyproject.toml` 不再声明 `click` 运行时依赖。
- README、中文 README 和 Makefile 不再把 `uv` 作为必需工具链。
- 打包文档和开发依赖支持标准命令 `python -m build`。
- 测试不再依赖 `click.testing.CliRunner`。
- `specflow -h` / `specflow --help`、无参数、`init`、`status` 的核心行为保持可用。
- 项目测试通过。

## Risk

- `argparse` 或手写 CLI 的 help 输出格式会与 Click 不完全一致，测试应只断言稳定的关键内容。
- 删除 `uv.lock` 会降低开发依赖版本锁定的可复现性，但能减少工具链约束。
- Makefile 继续使用 `rsync`，这与当前实现一致；本需求不处理跨平台同步命令替换。
