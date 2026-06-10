# 需求：SDD Skill-first 开发流程协议

## Review status

Draft

## Background

Claude Code / Codex 已经具备足够好的代码理解、规划、实现、测试和 review 能力。

sdd 不应该替代这些能力，也不应该实现新的 Agent Runtime、Workflow Engine、状态机，或一组由用户手动驱动的 CLI 流程。

sdd 要解决的问题是：在使用现有 coding agent 开发功能时，缺少一个稳定、低噪声、可审查的流程协议。这个协议应帮助 Agent 和用户按阶段完成需求澄清、方案设计、实施计划、代码实现和验证，避免跳过用户确认，也避免把未讨论事项直接实现。

## Goals

1. 提供一个 Skill-first 的流程化开发协议

   用户主要通过一个 sdd skill 进入流程，而不是手动执行一串 `sdd xxx` 命令。

2. 保持 Claude Code / Codex 作为主要执行者

   sdd 只规定流程边界、阶段产物和确认规则，不替代现有 Agent 的代码理解、规划、实现和测试能力。

3. 按阶段推进开发

   流程应明确分为：

   - Requirement
   - Spec
   - Plan
   - Implementation
   - Verification

4. 每个阶段都支持用户 review

   Requirement、Spec、Plan 阶段都必须允许用户讨论、修改和确认。

   默认流程应建议用户先 review 当前阶段，再进入下一阶段。但如果用户明确要求进入后续阶段，sdd skill 不应强行阻止；它应检查前置条件是否充分，提醒未确认事项、open questions 和风险，然后按用户指令开始目标阶段。

5. 明确处理不确定事项

   如果当前阶段存在 open questions、风险、冲突或缺失信息，skill 必须和用户讨论，而不是自行假设并继续推进。

   如果用户选择继续推进，这些事项应被记录为风险、假设或待确认项。

6. 保留可审查的过程文档

   每个 feature 的过程文档使用：

   - `docs/requirement/<yyyymmdd>-<feature>.md`
   - `docs/spec/<yyyymmdd>-<feature>.md`
   - `docs/plan/<yyyymmdd>-<feature>.md`
   - `docs/verification/<yyyymmdd>-<feature>.md`

   sdd 自身这轮改造位于 `sdd/` 包内，因此使用同一 stage 目录命名规则：

   - `docs/requirement/20260609-sdd-skill-first-protocol.md`
   - `docs/spec/20260609-sdd-skill-first-protocol.md`
   - `docs/plan/20260609-sdd-skill-first-protocol.md`
   - `docs/verification/20260609-sdd-skill-first-protocol.md`

7. 保持 CLI 极简

   CLI 只用于初始化文档模板和可选诊断，不作为用户主流程，也不作为 skill 每一步都必须调用的编排工具。

## Non-goals

1. 不实现新的 Agent Runtime

   不构建 Planner、Executor、Workflow Engine、Task Graph、Checkpoint、Session Runtime 等系统。

2. 不替代 Claude Code / Codex

   不重新实现代码搜索、代码修改、测试执行、review、规划或推理能力。

3. 不设计用户手动执行的一串 CLI 流程

   用户不应该需要通过连续执行 `sdd feature`、`sdd next`、`sdd mark` 等命令完成开发流程。

4. 不让 skill 内部频繁调用 CLI

   CLI 不应成为隐藏的流程编排器，避免把噪声从用户侧转移到 skill 内部。

5. 不维护持久状态机

   sdd 不应保存“当前阶段”到数据库、状态文件或运行时对象中。

6. 不自动替用户确认阶段

   只有用户明确表达确认后，skill 才能把阶段文档标记为 `Accepted`。

7. 不做项目管理系统

   不替代 Jira、Linear、GitHub Issues 或其他项目管理工具。

## User workflow

### Entry point

用户通过自然语言或 skill 入口启动：

```text
使用 sdd 帮我做 GitHub OAuth 登录
```

而不是：

```bash
sdd feature "GitHub OAuth 登录"
sdd next ...
sdd mark ...
```

### Requirement phase

Skill 应进入 Requirement 阶段：

- 只澄清需求
- 不写 spec
- 不写 plan
- 不改代码
- 识别 open questions
- 与用户讨论并更新 `requirement.md`

完成 draft 后，skill 应请求用户 review。

默认情况下，skill 应建议先确认 Requirement 再进入 Spec。如果用户明确要求直接进入 Spec，skill 应先说明 requirement 尚未确认、列出 open questions 或风险，然后继续开始 Spec 阶段。

### Spec phase

Skill 基于 `requirement.md` 进入 Spec 阶段：

- 设计技术方案
- 讨论技术不确定项
- 记录关键设计决策
- 更新 `spec.md`
- 不写 plan
- 不改代码

如果 Requirement 尚未确认，skill 应在开始 Spec 前明确提示这一点，并把相关待定事项作为风险或假设记录到 `spec.md`。

完成 draft 后，skill 应请求用户 review。

默认情况下，skill 应建议先确认 Spec 再进入 Plan。如果用户明确要求直接进入 Plan，skill 应先说明 spec 尚未确认、列出技术待定事项或风险，然后继续开始 Plan 阶段。

### Plan phase

Skill 基于 `requirement.md` 和 `spec.md` 进入 Plan 阶段：

- 制定实施步骤
- 明确风险
- 明确验证方式
- 明确回滚或恢复方式
- 更新 `plan.md`
- 不改代码

如果 Spec 尚未确认，skill 应在开始 Plan 前明确提示这一点，并把相关待定事项作为风险或假设记录到 `plan.md`。

完成 draft 后，skill 应请求用户 review。

默认情况下，skill 应建议先确认 Plan 再进入 Implementation。如果用户明确要求直接实现，skill 应先说明 plan 尚未确认、列出实施风险和待定事项，然后按用户指令开始实现。

### Implementation phase

Skill 基于已有 requirement/spec/plan 允许 Claude Code / Codex 正常实现。

如果 Plan 尚未确认但用户明确要求实现，skill 应提示风险后继续。

如果实现过程中发现 plan 与代码现实冲突，skill 应停止并回到 Plan 讨论，或在用户明确指示下更新相关文档，而不是静默扩大或改变范围。

### Verification phase

实现完成后，skill 进入 Verification 阶段：

- 对照 requirement 检查目标是否满足
- 对照 spec 检查设计是否一致
- 对照 plan 检查是否按计划实施
- 汇总测试结果
- 记录风险和未完成项
- 写入 `verification.md`

## Document requirements

### Common requirements

每个阶段文档应包含：

- 当前阶段名称
- Review status
- Open questions
- Decisions
- User review notes

Review status 只支持：

```text
Draft
Accepted
```

风险、假设、阻塞项应写入对应章节，不通过额外状态表达。

### `requirement.md`

必须包含：

- Background
- Goals
- Non-goals
- User stories / scenarios
- Acceptance criteria
- Open questions
- Decisions
- User review notes
- Review status

### `spec.md`

必须包含：

- Requirement basis
- Overview
- Design decisions
- Affected files / components
- Data model / interfaces
- Open technical questions
- Risks and trade-offs
- Alternatives considered
- User review notes
- Review status

### `plan.md`

必须包含：

- Requirement basis
- Spec basis
- Implementation steps
- Files to change
- Verification plan
- Risks / blockers / assumptions
- Rollback / recovery
- User review notes
- Review status

### `verification.md`

必须包含：

- Requirement alignment
- Spec alignment
- Plan alignment
- Test results
- Risks
- Incomplete items
- Conclusion

## Skill behavior requirements

1. sdd 应主要表现为一个 skill，而不是一组用户命令。

2. Skill 必须明确告诉用户当前阶段。

3. Skill 默认应聚焦当前阶段，避免主动跳阶段。

4. 如果用户明确要求进入 Spec，即使 Requirement 未确认，Skill 也可以开始 Spec；但必须先提示 Requirement 未确认、列出已知待定事项和风险。

5. 如果用户明确要求进入 Plan，即使 Spec 未确认，Skill 也可以开始 Plan；但必须先提示 Spec 未确认、列出技术待定事项和风险。

6. 如果用户明确要求开始实现，即使 Plan 未确认，Skill 也可以开始实现；但必须先提示 Plan 未确认、列出实施风险和可能偏离点。

7. Skill 遇到不确定事项时必须提问；如果用户选择继续推进，Skill 应记录这些不确定事项，而不是静默假设。

8. Skill 只有在用户明确确认后，才能把对应文档标记为 `Accepted`。

9. Skill 可以直接使用 Claude Code / Codex 的文件读写能力维护文档，不需要每一步调用 CLI。

10. Skill 可以在必要时建议或使用 CLI 做初始化或诊断，但 CLI 不是主流程。

## CLI requirements

CLI 应保持最小化。

### Required commands

#### `sdd init`

用于初始化项目内的 sdd 文件：

- 创建 `docs/`
- 创建 `.sdd/template/`
- 写入默认文档模板

#### `sdd status`

可选诊断命令，用于查看文档完整性和 review status。

它不应作为流程推进的必要步骤。

### Commands to avoid

不应新增或推荐以下类型命令：

- `sdd next`
- `sdd mark`
- `sdd approve`
- `sdd enter-stage`
- `sdd create-stage`
- `sdd workflow`
- `sdd run`

这些命令会让 sdd 滑向 CLI workflow 或状态机。

## Acceptance criteria

1. 用户可以通过一个 sdd skill 启动流程。

2. 用户不需要手动执行一串 CLI 命令完成开发流程。

3. Skill 能按 Requirement → Spec → Plan → Implementation → Verification 顺序工作。

4. Requirement、Spec、Plan 每个阶段都支持用户 review/approve，默认流程会建议先确认再进入下一阶段。

5. 用户明确要求进入 Spec 时，Skill 会检查 Requirement 是否确认；若未确认，会提示待定事项和风险，然后继续开始 Spec。

6. 用户明确要求进入 Plan 时，Skill 会检查 Spec 是否确认；若未确认，会提示待定事项和风险，然后继续开始 Plan。

7. 用户明确要求开始实现时，Skill 会检查 Plan 是否确认；若未确认，会提示实施风险和可能偏离点，然后继续开始实现。

8. 不确定事项会被记录并向用户提问；如果用户选择继续推进，这些事项会作为风险或假设保留在后续文档中。

9. CLI 只承担 init/status 等低噪声辅助职责。

10. README 以 Skill-first 使用方式说明 sdd，而不是以 CLI 命令串说明流程。

## Open questions

1. Skill 名称是使用单一 `sdd`，还是保留多个内部 skill？

   当前倾向：单一 `sdd` skill，避免用户选择成本。

2. 项目级 skill 文件路径是否需要由 CLI 管理？

   已决策：`sdd init` 不安装项目级 skill；skill 源文件由项目仓库维护，安装/同步由 `make install` 或 Claude Code skill 机制处理。

3. `status` 是否需要 JSON 输出？

   当前倾向：可以保留，但定位为诊断/测试辅助，不作为主流程。

## Decisions

- sdd 是 Skill-first 流程协议。
- CLI 不是用户主入口。
- CLI 不做流程编排。
- Skill 不需要频繁调用 CLI。
- 阶段状态主要体现在文档中。
- 用户确认是默认阶段推进的推荐条件，但用户可以明确要求跳过确认继续推进；此时 Skill 必须提示条件不足、待定事项和风险。
- CLI 只提供 `init` / `status`，不提供 `install`。
- `sdd init` 不安装项目级 skill。
- sdd 使用 skill prompt 和过程文档作为软约束，不引入硬状态机或运行时强制机制。
