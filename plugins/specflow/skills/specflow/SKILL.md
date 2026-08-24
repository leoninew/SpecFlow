---
name: specflow
description: A skill-first development protocol for coding agents.
---

# SpecFlow

当用户希望通过结构化流程开发一个功能或变更时，使用本 skill。

SpecFlow is a skill-first development protocol for coding agents. 它不是 Claude Code、Codex 或任何 coding agent runtime 的替代品。coding agent 仍负责代码理解、文件修改、测试执行和 review；SpecFlow 只定义流程边界、review 节点和文档要求。

## 语言

说明、讨论和生成的过程文档以中文为主。命令、文件路径、代码标识符和通用技术术语在更清晰时保留英文。

协议概念必须支持中英双语表达。用户使用中文或英文都应命中同一语义，例如“轻量模式”和 `light` 等价，“开始实现”和 `Implementation` 等价。

## 术语别名

### 流程模式 / Flow mode

- `strict` / 严格 / 严格模式
- `standard` / 标准 / 标准模式
- `light` / 轻量 / 轻量模式

### 阶段 / Stage

- `Requirement` / 需求 / 需求阶段
- `Spec` / 规格 / 方案 / 规格阶段 / 方案阶段
- `Plan` / 计划 / 计划阶段
- `Implementation` / 实现 / 实施 / 开始实现 / 开发
- `Verification` / 验证 / 验收 / 验证阶段

### 状态 / Review status

文档中建议使用英文规范值，但识别用户语义时应支持中文：

- `Draft` / 草稿
- `Accepted` / 接受 / 已接受 / 确认 / 通过

新文档只写 `Draft` 或 `Accepted`。历史文档可能出现 `Approved`，可以按已接受理解，但不要主动迁移或清理历史状态。

## 流程模式

根据任务大小选择合适模式。不要让用户通过一串 `specflow xxx` 命令驱动流程。不要在每个阶段转换时调用 specflow CLI。优先使用 coding agent 正常的文件读写能力直接维护过程文档。

### strict / 严格模式

适合需求不清、跨模块、风险高、需要完整设计审查的变更。

流程：

1. Requirement / 需求
2. Spec / 规格
3. Plan / 计划
4. Implementation / 实现
5. Verification / 验证

### standard / 标准模式

适合普通功能或中等复杂度变更。

流程：

1. Requirement / 需求
2. Plan / 计划
3. Implementation / 实现
4. Verification / 验证

### light / 轻量模式

适合范围明确的小修小改或简单 bugfix。

流程：

1. Requirement / 需求
2. Implementation / 实现
3. Verification / 验证

light / 轻量模式必须保留适中澄清的 requirement / 需求和接近 standard / 标准模式的 verification / 验证；不得退化为直接实现或极简验收记录。

## 文档位置

使用 feature-specific stage 目录文档：

- `docs/requirement/<yyyymmdd>-<feature>.md`
- `docs/spec/<yyyymmdd>-<feature>.md`
- `docs/plan/<yyyymmdd>-<feature>.md`
- `docs/verification/<yyyymmdd>-<feature>.md`

同一功能的 requirement/spec/plan/verification 使用相同 `<yyyymmdd>-<feature>.md` 文件名，分别放在对应 stage 目录下。`<yyyymmdd>` 使用 8 位日期格式，例如 `20260609`；`<feature>` 用于表达需求或功能主题。

创建或修改 `docs/` 阶段文档时，大标题下一行必须保留 `最后修改时间: <yyyy-MM-dd HH:mm:ss>`，并写为本次创建或修改的当前时间。

standard / 标准模式可以不创建 `spec.md`。light / 轻量模式可以只创建经过适中澄清的 requirement / 需求和 `verification.md`；轻量需求仍写在 `docs/requirement/<yyyymmdd>-<feature>.md` 中。

## 文档隔离

用户表达“新需求”、“开始需求”、“新任务”、“新 feature”或类似语义时，默认创建新的 `docs/requirement/<yyyymmdd>-<feature>.md` 文档。

不要修改相邻、同名相近或历史 feature 文档，除非用户明确说：

- 沿用现有文档
- 更新现有需求
- 继续上次
- 修改这个 requirement / spec / plan / verification

如果不确定是新建还是沿用，先询问用户。

## Review status / 审查状态

阶段文档只使用两种状态：

- `Draft` / 草稿：阶段内容仍在形成中，或尚未被用户接受。
- `Accepted` / 接受：用户已接受该阶段内容，或用户明确要求进入后一阶段。

不要引入 `Approved`、`Blocked`、`Completed`、`Proceeded with assumptions` 等额外状态。风险、假设、阻塞项应写进对应章节，而不是扩展状态枚举。

## 阶段流转规则

- 始终告诉用户当前阶段和当前流程模式，优先使用“中文 + 英文”的形式，例如“当前：轻量模式 / light，需求 / Requirement”。
- 默认聚焦当前阶段，直到用户接受或要求进入下一阶段。
- 用户明确确认当前阶段时，将当前阶段文档 `Review status` 更新为 `Accepted`。
- 用户明确要求进入后一阶段时，视为接受前一阶段；先将前一阶段文档 `Review status` 更新为 `Accepted`，再进入目标阶段。
- “确认”、“通过”、“接受”、“进入 spec / 进入规格”、“开始 plan / 开始计划”、“开始实现”、“继续下一阶段”等表达，都表示接受当前/前一阶段。
- 如果前置阶段有 open questions、risks 或 assumptions，但用户仍要求继续，记录这些事项并进入目标阶段，不要反复要求用户确认。
- 如果当前阶段存在必须由用户决定的不确定事项，先询问用户；如果用户选择继续推进，把不确定事项记录为 risk 或 assumption。
- 阶段边界是默认硬边界。除非用户在当前消息中明确要求跨越多个阶段，否则一次回复只处理当前阶段，不要把 Requirement / 需求、Implementation / 实现和 Verification / 验证连跑。
- 默认流程下，Implementation / 实现完成后先停在实现阶段：汇报实现结果、实际 diff、已知风险、未运行检查和可能偏离范围，等待用户人工验收并明确要求开始 Verification / 验证。
- 如果用户在当前消息中明确要求连续完成实现和验证（例如“实现并验证”“实现后验证”“跑完整流程”），才可以在实现完成后继续进入 Verification / 验证；进入前仍必须先输出实现摘要和验证前风险，并在回复中清楚标记从 Implementation / 实现切换到 Verification / 验证。
- 当用户说“使用 light / 轻量模式，开始 Requirement / 需求”或类似表达时，只创建或更新 requirement 草稿并请求 review；不要在同一轮写产品代码、运行验证或创建 verification。
- light / 轻量模式仍需要分阶段推进：Requirement 被用户接受或用户明确要求开始实现后，才能进入 Implementation；默认在 Implementation 完成后等待用户人工验收并明确要求进入 Verification / 验证。

## Requirement / 需求阶段

澄清要做什么和为什么做。所有流程模式都使用 Requirement / 需求这一概念；light / 轻量模式采用适中澄清策略，但不向用户引入额外的阶段概念。

职责：

1. 创建或更新 `docs/requirement/<yyyymmdd>-<feature>.md`。
2. strict / 严格模式和 standard / 标准模式捕获 background、goals、non-goals、user scenarios、acceptance criteria、open questions、decisions 和 user review notes。
3. light / 轻量模式采用适中澄清策略，至少记录目标、非目标、验收标准、风险/假设；必要时也记录背景、场景、待定问题、决策和用户审查记录，但仍称为 Requirement / 需求。
4. 除非用户明确要求推进，否则不写 spec、plan 或产品代码。
5. draft 完成后请求用户 review requirement；如果用户要求进入后一阶段，自动将 requirement 标记为 `Accepted`。
6. 向用户展示 requirement / 需求草稿时，除了总结已确认的需求，还必须显式提示仍需要用户关注的未决事项。这些事项包括但不限于：尚未确认的假设、影响方案选择的决策点、范围边界不清之处、验收标准中的模糊点、依赖外部条件的风险，以及可以继续推进但需要后续确认的问题。如果没有这类事项，应明确说明“暂无需要用户确认的未决事项”。

## Spec / 规格阶段

设计如何实现需求。strict / 严格模式使用该阶段；standard / 标准模式和 light / 轻量模式通常跳过。

职责：

1. 读取 `docs/requirement/<yyyymmdd>-<feature>.md`。
2. 创建或更新 `docs/spec/<yyyymmdd>-<feature>.md`。
3. 捕获 requirement basis、overview、design decisions、affected components、interfaces、technical questions、risks、alternatives 和 user review notes。
4. 如果 Requirement 不是 `Accepted`，但用户要求进入 Spec / 规格，则先将 Requirement 标记为 `Accepted`。
5. 除非用户明确要求推进，否则不写 plan 或产品代码。

## Plan / 计划阶段

定义实施步骤和验证方式。strict / 严格模式和 standard / 标准模式使用该阶段。

职责：

1. 读取可用的 requirement/spec 文档。
2. 创建或更新 `docs/plan/<yyyymmdd>-<feature>.md`。
3. 捕获 implementation steps、files to change、verification plan、blockers、assumptions、risks、rollback 和 user review notes。
4. 如果前置 Requirement 或 Spec 不是 `Accepted`，但用户要求进入 Plan / 计划，则先将对应前置文档标记为 `Accepted`。
5. 除非用户明确要求实现，否则不写产品代码。

light / 轻量模式推荐需求结构：

```markdown
## Background

## Goal

## Non-goal

## User scenarios

## Acceptance

## Open questions

## Decisions

## Risk
```

如果变更确实很小，可以将无内容章节标为“不适用”，但不要跳过对目标、边界、验收和风险/假设的适中澄清。


## Implementation / 实现阶段

使用 coding agent 的正常能力，在已有过程约束内实现。

职责：

1. 读取可用的 requirement/spec/plan 文档。
2. 如果 Plan 缺失但当前是 light / 轻量模式，依据 requirement / 需求实现。
3. 将实现范围限制在用户指令和已有文档约束内。
4. 如果代码现实与 plan 或 requirement 冲突，报告冲突，并和用户一起更新过程文档，不要静默改变范围。
5. 默认在实现完成后停止在 Implementation / 实现阶段：汇报实际改动、已运行/未运行的检查、已知风险、可能偏离范围和建议用户验收的事项；不要创建 verification 文档、不要运行验证阶段专属流程、不要输出建议 git commit message，直到用户明确要求进入 Verification / 验证。若用户在当前消息中明确要求连续完成实现和验证，先输出实现摘要和验证前风险，再进入 Verification / 验证；即使连续进入 Verification / 验证，也只有 Verification / 验证完成后才输出建议 git commit message。

## Verification / 验证阶段

对照过程文档验证实现。

进入条件：默认需要用户已看过 Implementation / 实现结果和验证前风险，并在实现完成后明确要求开始 Verification / 验证。若用户在当前消息中明确要求连续完成实现和验证，该请求可作为进入 Verification / 验证的授权；进入前仍必须先输出实现摘要和验证前风险。

职责：

1. 读取可用的 requirement/spec/plan 文档。
2. 对照实际 diff 检查预期范围与实际改动是否一致。
3. 运行命令前先识别当前项目开发语言、工具链，不要预设所有项目都是 Python、uv、Node 或某种固定栈。
4. 优先使用项目显式入口：README、justfile、Makefile、package scripts、CI 配置、语言专用配置或已有测试/lint/format 命令。
5. 尽可能运行或收集相关测试、lint、format 或项目约定命令结果；不要在通用协议中硬编码语言、框架或业务特定检查。
6. 创建或更新 `docs/verification/<yyyymmdd>-<feature>.md`。
7. strict / standard 模式记录 requirement alignment、spec alignment、plan alignment、actual diff summary、expected vs actual changed files、acceptance criteria checklist、test results、missed or expanded scope、risks、incomplete items 和 conclusion。
8. Verification / 验证完成并确认交付时，在最终屏幕输出中基于实际 diff 提供建议 git commit message，帮助用户审视交付边界；该建议不写入 `verification.md`，也不代表自动提交。
9. 建议 git commit message 应是完整提交信息，不只是单行标题。除非用户明确要求 title-only，否则使用 fenced code block 输出，至少包含 subject、空行和 body；body 必须用列表形式输出，但应面向 git 历史说明本次提交的变更意图和影响，而不是复述 verification 过程；每条描述一个有意义的改动、行为变化、约束或兼容性影响。验证命令结果、验收清单、风险提示、未完成项或拆分建议应放在屏幕交付说明中，不写进建议 commit body。
10. 除非用户明确授权，不执行 `git add`、`git commit`、`git push` 等 Git 写操作。
11. 如果当前 diff 包含无关改动、验证失败或仍有 incomplete items，应在屏幕输出 commit 建议前明确说明风险，并建议用户先拆分或修复。
12. light / 轻量模式按 standard / 标准模式的主要验证维度记录：需求对齐、实际 diff 摘要、预期与实际改动对比、验收清单、命令结果、范围偏差、风险、未完成项和结论。没有 spec 或 plan 时，对应小节写“不适用”或“按 requirement / 需求核对”。不要只写变更摘要、验收、命令和剩余风险。

light / 轻量模式推荐使用完整 verification 模板；可合并明显重复的小节，但必须保留上述验证信息。


## CLI 使用

specflow CLI 只用于 setup 和 diagnostic support：

- `specflow init`
- `specflow status`

不要把 CLI 命令作为主要工作流机制。
