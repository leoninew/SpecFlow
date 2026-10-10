# Plan / 计划：<feature>

最后修改时间: 2026-10-10 21:25:56

## Review status / 审查状态

Draft

## Intent basis / 意图依据

关联 `docs/intent/<yyyymmdd>-<feature>.md`，说明目标、边界和验收依据。

用户明确进入 Plan 时接受前置意图；仍有未知项时记录假设和风险。所有任务都保留计划，小任务可以简明填写。

## Technical decisions / 技术设计与决策

- <实现方式、接口与数据约束、兼容性、关键选择及理由；局部细节可写入对应 task>

## Implementation steps / 实现步骤

1. <交付步骤、涉及范围和完成条件>

## Files to change / 需修改文件

- <预期修改的模块或文件；共享写入约束>

## Tasks and coordination / 子任务与协调

无 task 时将本节写为“不适用”，移除下列协调小节和占位表，不创建子任务文档。拆分时使用以下固定表，并按当前 SpecFlow skill 的 `references/task-coordination.md` 核对规则；本计划是依赖与分配的权威来源。

### Coordination / 协调信息

- 方案修订：<从 1 开始，任务边界、依赖或验收变化时递增>。
- 权威协调根：<所有执行会话能够读取的实际位置>。
- 仲裁会话：<唯一负责分配与审查的会话>。
- 阶段授权：<用户已授权的阶段、任务范围及指令依据>。

### Task definitions / 任务定义表

| ID | 任务文档 | 直接前置任务与要求 | 预期交付与验收 | 意图验收归属 |
| --- | --- | --- | --- | --- |
| T01 | `docs/task/<yyyymmdd>-<feature>/T01-<topic>.md` | <无，或前置 ID、所需产物与版本条件> | <交付物、检查及接受条件> | A01 |

### Execution registry / 执行登记表

| ID | 执行状态 | 执行者 | 分配编号 | 工作基线 / 交付位置 | 仲裁结论 / 当前阻塞 |
| --- | --- | --- | --- | --- | --- |
| T01 | unassigned | 无 | 无 | <派发时记录 / 尚无交付> | <可分配条件的核对结论或等待原因> |

执行状态为 unassigned、assigned、running、submitted、accepted。方案的 Review status Accepted 不表示实现已交付；只有主会话接受当前有效交付，任务执行状态才为 accepted。

### DAG and parallelism / DAG 与并行安排

<依据任务定义表表达 DAG 和一种合法执行顺序；标识、引用、无环及验收覆盖均须核对。说明共享文件、契约冲突和集成责任。图是表格的视图，不独立维护依赖。>

派发前重新核对：方案与阶段已授权、任务未分配、所有前置交付已实现或产出、必要检查通过、仲裁已接受且版本可访问，无未解决阻塞或写入冲突。

### Assignment history / 分配历史

尚无分配。用户要求派发后，先登记唯一分配编号，再输出交接提示词；撤销、返工或重新分配时保留原编号、执行者、时间和原因。权威登记仅由仲裁会话维护。

## Verification plan / 验证计划

- <相关检查、任务交付审查、集成验证和验收覆盖；列出项目已有命令及所需环境>

## Risks / blockers / assumptions / 风险 / 阻塞项 / 假设

-

## Rollback / recovery / 回滚 / 恢复

-

## User review notes / 用户审查记录

-
