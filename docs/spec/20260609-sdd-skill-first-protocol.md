# 规格：SDD Skill-first 开发流程协议

## Review status

Draft

## Requirement basis

基于 `docs/requirement/20260609-sdd-skill-first-protocol.md`。

Requirement review status: Draft。

用户明确要求在 Requirement 尚未 approved 的情况下进入 Spec。因此本 Spec 带着以下前提继续：

- Requirement 仍可能变化。
- Requirement 中未解决的问题应作为风险或假设延续到 Spec。
- 如果后续 Requirement 修改与本 Spec 冲突，必须回头修订 Spec。

## Overview

sdd 将围绕一个单一的用户入口 skill 重新设计，定位为 Skill-first 的开发流程协议。

主要用户体验不是一串 CLI 命令。用户通过自然语言或 skill 入口调用 sdd，skill 引导开发过程经过以下阶段：

1. Requirement
2. Spec
3. Plan
4. Implementation
5. Verification

Claude Code / Codex 仍然负责代码理解、文件修改、测试执行和实现 review。sdd 只提供流程结构：阶段边界、review 节点、文档要求和风险提示。

CLI 保持最小化，只负责初始化文档模板以及可选的诊断状态查看。CLI 不安装项目级 skill，不提供用户级 install 命令，也不应成为 workflow runner、阶段转换系统，或 skill 每一步都调用的隐藏命令序列。

## Design principles

1. Skill-first UX

   用户只需要面对一个 sdd skill，而不是一组命令或多个阶段专用 skill。

2. 按任务大小选择流程模式

   sdd 支持 strict、standard、light 三种模式：

   - strict：Requirement → Spec → Plan → Implementation → Verification
   - standard：Requirement → Plan → Implementation → Verification
   - light：Requirement → Implementation → Verification

   light 仍必须保留经过适中澄清的 requirement 和 verification；verification 不得缩水成极简验收备注。

3. 低命令噪声

   Skill 应主要依赖常规文件读写和模型推理能力，不应在每次阶段转换时调用 CLI 子命令。

3. 软流程护栏

   默认路径鼓励 Requirement → Spec → Plan → Implementation → Verification，并在主要文档阶段要求 review。

   如果用户明确要求在 review 不完整时继续推进，skill 应先提示缺失确认、open questions 和风险，然后按用户指令继续。

4. 不做运行时状态机

   阶段状态体现在文档中，而不是持久化到 workflow 数据库、状态文件或运行时对象。

5. 现有 Agent 继续负责工程工作

   sdd 不替代代码搜索、实现、测试或代码 review 能力。

6. 不做向后兼容

   旧的 `architect / implement / review` 三 skill 模型会被替换，不需要兼容旧行为或旧测试断言。

## Proposed structure

### Skill structure

将当前多 skill 模型替换为一个主 skill：

```text
sdd
```

该 skill 编码流程协议：

- 根据用户意图和已有文档识别当前阶段
- 明确告知用户当前阶段
- 默认只做当前阶段合适粒度的工作
- 当用户要求跳阶段时，提示前置条件不足、待定事项和风险
- 更新当前阶段对应的过程文档
- 当前阶段 draft 完成后，请求用户 review

Skill 不应依赖频繁 CLI 调用。

### Document structure

sdd 包自身的过程文档放在包内 `docs/`，并使用 stage 目录命名规则：

```text
docs/requirement/20260609-sdd-skill-first-protocol.md
docs/spec/20260609-sdd-skill-first-protocol.md
docs/plan/20260609-sdd-skill-first-protocol.md
docs/verification/20260609-sdd-skill-first-protocol.md
```

安装到其他项目后，feature 文档仍使用：

```text
docs/requirement/<yyyymmdd>-<feature>.md
docs/spec/<yyyymmdd>-<feature>.md
docs/plan/<yyyymmdd>-<feature>.md
docs/verification/<yyyymmdd>-<feature>.md
```

### CLI structure

CLI 保持极简：

```text
sdd init
sdd status
```

#### `sdd init`

初始化项目级 sdd 支持：

- 创建 `docs/`，如果不存在
- 创建 `.sdd/template/`
- 写入默认模板

#### `sdd status`

可选诊断命令。

它可以报告：

- 过程文档是否存在
- 检测到的 review status
- 明显未完成的章节

它不应成为正常 skill 流程的必要步骤。

## Skill behavior

### Stage detection

Skill 应从以下信息推断阶段：

- 用户指令
- 已有过程文档
- 文档中的 review status
- 文档中的 open questions 或 risks

Skill 不应需要通过 CLI 命令来决定下一步做什么。

### Requirement stage

新任务默认从 Requirement 阶段开始。

职责：

- 澄清问题和目标结果
- 识别 goals 和 non-goals
- 捕获用户场景和验收标准
- 记录 open questions 和 decisions
- 更新 `requirement.md`
- 请求用户 review requirement draft

Skill 在该阶段不应主动编写 Spec、Plan 或代码。

### Spec stage

职责：

- 设计技术方案
- 识别受影响组件和接口
- 记录关键设计决策
- 暴露技术不确定项
- 更新 `spec.md`
- 请求用户 review spec draft

如果 Requirement 未 approved，skill 应在开始时明确说明，并把未解决事项作为 assumptions 或 risks 延续下来。

### Plan stage

职责：

- 将已确认或用户明确要求推进的 Spec 转换为实施步骤
- 识别可能修改的文件
- 定义验证方式
- 捕获 blockers、assumptions、risks 和 rollback/recovery 说明
- 更新 `plan.md`
- 请求用户 review plan draft

如果 Spec 未 approved，skill 应在开始时明确说明，并把未解决技术事项作为 assumptions 或 risks 延续下来。

### Implementation stage

职责：

- 使用 Claude Code / Codex 的正常实现能力
- 遵循已有 requirement/spec/plan 约束
- 如果 plan 缺失或未 approved，但用户明确要求实现，则提示风险后在用户给定范围内继续
- 如果代码现实与 plan 冲突，报告冲突并按需要更新过程文档，而不是静默改变范围
- 默认流程下，实现完成后停留在 Implementation，汇报实际改动、未运行检查、风险和可能偏离范围；等待用户人工验收并明确要求 Verification
- 如果用户明确要求连续完成实现和验证，先汇报实现结果和风险，再进入 Verification

### Verification stage

进入条件：默认需要用户已看过 Implementation 结果和风险，并在实现完成后明确要求开始 Verification。如果用户明确要求连续完成实现和验证，该请求可作为进入 Verification 的授权；进入前仍必须先汇报实现结果和风险。

职责：

- 对照 requirement/spec/plan 检查实现
- 运行或收集相关测试结果
- 记录 alignment、risks、incomplete items 和 conclusion
- 更新 `verification.md`

## Template changes

### `requirement.md`

新增或保留章节：

- Review status
- Background
- Goals
- Non-goals
- User stories / scenarios
- Acceptance criteria
- Open questions
- Decisions
- User review notes

### `spec.md`

新增或保留章节：

- Review status
- Requirement basis
- Overview
- Design principles
- Proposed structure
- Skill behavior
- CLI behavior
- Data model / document format
- Risks and trade-offs
- Alternatives considered
- Open technical questions
- User review notes

### `plan.md`

新增或保留章节：

- Review status
- Requirement basis
- Spec basis
- Implementation steps
- Files to change
- Verification plan
- Risks / blockers / assumptions
- Rollback / recovery
- User review notes

### `verification.md`

新增或保留章节：

- Requirement alignment
- Spec alignment
- Plan alignment
- Test results
- Risks
- Incomplete items
- Conclusion

## CLI implementation impact

### Skill and template source files

当前协议源文件位于 `.claude/skills/sdd/`：

```text
.claude/skills/sdd/SKILL.md
.claude/skills/sdd/requirement.md
.claude/skills/sdd/spec.md
.claude/skills/sdd/plan.md
.claude/skills/sdd/verification.md
```

CLI 需要模板时直接读取这些 Markdown 源文件，不再通过 Python 模块内嵌大段模板文本。

文档模板需要体现：

- review status
- open questions
- decisions
- user review notes
- soft guardrails，而不是硬性阶段阻断

### `sdd/src/sdd/cli.py`

保留命令：

- `init`
- `status`

更新行为：

- `init` 创建 `docs/` 和 `.sdd/template/`，写入默认文档模板
- `init` 不安装项目级 sdd skill
- `status` 只作为诊断命令
- 不检测、不提示、不兼容旧 `architect / implement / review` skills

不新增：

- `next`
- `feature`
- `mark`
- `approve`
- `workflow`
- `run`

### `sdd/tests/test_cli.py`

更新测试以匹配更简单的模型：

- `init` 创建 docs/templates，不创建项目级 sdd skill
- `status` 尽可能报告文档存在性和 review status
- `help` 入口支持 `sdd`、`sdd --help`、`sdd -h`

删除或避免假设命令驱动阶段转换、旧 skill 兼容提示的测试。

## Status model

Review status 只使用：

- `Draft`
- `Accepted`

用户明确确认当前阶段，或明确要求进入后一阶段，都视为接受当前/前一阶段。skill 应自动更新前置文档状态，避免反复询问 review 后才能继续。

Verification 是特殊边界：默认流程下，实现完成后不自动进入 Verification。skill 必须先汇报实现结果和风险，等待用户人工验收并明确要求开始 Verification。用户明确要求连续完成实现和验证时，skill 也必须先汇报实现结果和风险，再进入 Verification。

不引入 `Approved`、`Blocked`、`Completed`、`Proceeded with assumptions` 等额外状态；风险和假设写入章节内容。

## Risks and trade-offs

1. 单一 skill prompt 可能变长

   缓解方式：skill 指令保持简洁、流程导向；详细结构由模板承载。

2. 软护栏依赖模型遵守

   因为没有硬状态机，skill 指令必须清楚表达预期行为。这是可以接受的，因为 sdd 是协议，不是强制执行基础设施。

3. 用户可以跳过 review

   这是有意设计。sdd 应提醒并记录风险，而不是覆盖用户明确指令。

4. `status` 命令容易被过度设计

   应保持诊断用途，不演变成 `next` 或阶段转换引擎。

5. 不向后兼容会改变已安装产物

   这是接受的取舍。旧模型会被直接替换。

## Alternatives considered

### 保留 `architect / implement / review`

不采用。

原因：`architect` 容易暗示一次性生成 requirement/spec/plan，不能自然表达 Requirement review → Spec review → Plan review。

### 为每个阶段增加 CLI 命令

不采用。

原因：这会把 sdd 变成用户可见的 workflow CLI，并制造命令噪声。

### 让 skill 每个阶段都调用内部 CLI 命令

不采用。

原因：这只是把噪声从用户交互转移到 skill 执行中，也重复了 Claude Code / Codex 已经具备的文件读写能力。

### 硬性阻断阶段跳转

不采用。

原因：用户可能明确选择在 review 不完整时继续推进。sdd 应提醒、记录风险并继续，而不是拒绝。

## Open technical questions

1. 项目级 skill 是否由 `sdd init` 安装？

   已决策：不安装。`sdd init` 只初始化 `docs/` 和 `.sdd/template/`。

2. `status` 应只解析简单的 `Review status` 标题，还是模板应改用 frontmatter？

   当前倾向：解析简单 Markdown 标题，保持文档 human-first。

3. README 是否应该记录 CLI？

   当前倾向：应该记录，但只作为 setup/diagnostic support；主要使用章节应是 Skill-first。

## User review notes

-
