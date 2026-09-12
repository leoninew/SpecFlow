# Intent / 意图术语迁移规格
最后修改时间: 2026-09-12 14:20:11


## Review status / 审查状态

Accepted

## Mode / 模式

strict / 严格

## Intent basis / 意图依据

依据 `docs/intent/20260912-intent-terminology-migration.md` 中已接受的迁移意图：仓库内表达软件变更起点或工作项的旧术语统一改为 Intent / 意图；历史过程记录也迁移；不保留旧名称或路径的扫描、生成和输出兼容。

## Overview / 概览

将协议第一阶段的标准标识改为 `intent`，并同步替换面向使用者、维护者和自动化的所有语义引用。CLI 保持 `init` 与 `status` 两个命令及参数不变，但模板文件、阶段发现和状态标签采用 `intent`。`docs/intent/` 中的所有过程记录逐个移动到 `docs/intent/`，其余文档布局保持不变，相关历史引用同步更新。

## Design decisions / 设计决策

- 规范名称固定为 Intent / 意图，机器可读标识固定为小写 `intent`。
- `src/specflow/cli.py` 的阶段文件常量改为 `intent.md`，派生的阶段集合和 `status` 输出随之变为 `intent`。
- `status` 继续支持现有的阶段目录、扁平文件名和按功能分目录三种布局，但三者都只识别 `intent`；不识别、映射或显示旧阶段名称。
- `init` 保持当前仅创建 `docs/` 和 `.specflow/template/` 的行为，但生成 `.specflow/template/intent.md`；新过程记录的规范路径为 `docs/intent/<yyyymmdd>-<feature>.md`。
- 插件技能、四个阶段模板、README 中英文版本和 CLI 测试均使用 Intent / 意图的术语及示例。
- 仓库内历史过程记录的目录、文件名、正文、交叉引用和状态输出预期一并迁移；本次过程记录在实施时也移至 `docs/intent/`。
- 只替换表示协议第一阶段或工作项的语义。与软件变更无关的普通文字不做机械替换。

## Affected files / components / 受影响文件 / 组件

- `src/specflow/cli.py`：阶段文件及状态发现逻辑。
- `tests/test_cli.py`：模板、阶段目录、扁平文件名和输出的断言。
- `plugins/specflow/skills/specflow/SKILL.md`：流程阶段、别名、路径和阶段职责。
- `plugins/specflow/skills/specflow/template/*.md`：文件名、标题、引用和阶段说明。
- `README.md`、`README.zh-CN.md`：流程介绍、示例、交接说明和文档路径。
- `docs/intent/`、`docs/spec/`、`docs/verification/`：目录迁移以及历史记录中的术语、路径和引用更新。

## Data model / interfaces / 数据模型 / 接口

- CLI 命令接口不变：`specflow init` 与 `specflow status`。
- 新模板接口：`.specflow/template/intent.md`，替代旧的第一阶段模板文件。
- 新阶段目录接口：`docs/intent/<yyyymmdd>-<feature>.md`。
- `specflow status` 输出中的第一阶段列固定为 `intent`；缺失状态仍为 `missing`，审查状态的读取规则不变。
- 旧第一阶段目录、旧模板文件和包含旧阶段后缀的扁平文件不属于新 CLI 的可识别输入。

## Open technical questions / 待定技术问题

暂无需要用户确认的未决事项。

## Risks and trade-offs / 风险与权衡

- 已有外部项目若未将过程记录迁移到新名称，升级后不会被 `status` 发现；这是已接受的不兼容行为。
- 仓库历史记录中可能有旧路径作为证据描述；这些文字也会被改写，因此无法保留原始措辞的逐字历史。
- 保留三种新名称布局的读取能力避免扩大无关的行为破坏，但会继续维护它们的测试覆盖。

## Alternatives considered / 已考虑替代方案

- 保留旧目录读取并在输出中显示新名称：拒绝，会延续旧契约并违背无兼容决策。
- 仅替换 README 和技能的显示文字：拒绝，CLI、模板和过程记录仍会暴露旧语义。
- 使用全仓文本替换：拒绝，可能错误修改与协议无关的文字或代码；实施时按匹配位置审查。

## User review notes / 用户审查记录

-
