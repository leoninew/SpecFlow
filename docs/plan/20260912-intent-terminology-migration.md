# Intent / 意图术语迁移计划
最后修改时间: 2026-09-12 14:30:53


## Review status / 审查状态

Accepted

## Mode / 模式

strict / 严格

## Intent and spec basis / 意图与规格依据

依据已接受的同名意图记录和规格：第一阶段统一为 Intent / 意图及 `intent`；不保留旧名称的兼容；仅将第一阶段目录从旧名称迁移到 `docs/intent/`，不重构其余文档布局。

## Implementation steps / 实施步骤

1. 更新 CLI 的阶段文件常量和阶段集合，使 `init` 复制 `intent.md` 模板，`status` 在三种既有布局中发现并输出 `intent`。移除仅为旧第一阶段名称服务的常量值、文件名和测试样例。
2. 更新 CLI 单元测试：覆盖新的模板文件、阶段目录、扁平文件后缀和状态列；保持现有帮助、时间戳、空文档和三种布局行为的覆盖。
3. 更新插件技能、四个模板及中英文 README：将流程第一阶段、别名、示例、阶段职责、文档路径和交接说明统一为 Intent / 意图；仅替换表达该协议概念的文字。
4. 将现有第一阶段目录中的六份 Markdown 文件以原文件名移动到 `docs/intent/`，并更新其中的标题、章节、链接和正文；同步更新 `docs/spec/`、`docs/verification/` 和本次过程记录中的相关引用，消除仓库内该语义下的旧术语。
5. 使用全仓语义检索复核未替换的位置，逐项处理匹配结果；不修改与协议无关的普通叙述。
6. 运行格式、静态检查、单元测试、构建和 CLI 状态检查，确认插件包与新目录内容一致。
7. 将 Python 包、锁文件和两个插件 manifest 的发布版本统一升至 `0.1.1`；Codex manifest 在该基础版本上生成单一刷新后缀。

## Files to change / 待修改文件

- `src/specflow/cli.py`
- `tests/test_cli.py`
- `plugins/specflow/skills/specflow/SKILL.md`
- `plugins/specflow/skills/specflow/template/`
- `README.md`、`README.zh-CN.md`
- `pyproject.toml`、`uv.lock`、`src/specflow/__init__.py`
- `plugins/specflow/.claude-plugin/plugin.json`、`plugins/specflow/.codex-plugin/plugin.json`
- 现有第一阶段目录中的六份同名过程记录
- `docs/spec/`、`docs/verification/` 及本次过程记录中相关的术语和链接

## Verification plan / 验证计划

- 使用 `rg` 检查源代码、测试、插件、README 和过程文档中表示第一阶段或工作项的旧中英文术语是否已清除。
- 执行 `make check`，验证格式、lint 和类型检查。
- 执行 `make test`，验证 CLI 初始化、状态读取和布局发现。
- 执行 `make release`，验证 source 与 wheel 构建。
- 执行 `uv run --locked --no-sync specflow status`，确认仓库过程记录显示 `intent` 且各阶段状态符合迁移后的文件位置。

## Blockers / 阻塞项

无。

## Assumptions / 假设

- 现有第一阶段目录中的六份文件均迁移到 `docs/intent/`，文件名、时间线和审查状态保留。
- README、模板、技能和过程记录中的所有协议语义用语都应同步改写；与协议无关的同形词由逐项审查决定是否保留。

## Risks / 风险

- 路径迁移遗漏会导致 `status` 将第一阶段显示为 `missing`，因此迁移后必须运行 CLI 和单元测试验证。
- 全仓替换可能触及历史描述或 Python 标识符，实施时需要先检索再按语义修改。
- 外部采用旧名称的项目不属于兼容范围，升级后必须自行迁移。

## Rollback / 回退

- 若迁移验证失败，回退本次提交即可同时恢复代码、模板和过程文档路径；不涉及数据库或外部状态变更。

## User review notes / 用户审查记录

- 用户要求将发布版本升至 `0.1.1`。
