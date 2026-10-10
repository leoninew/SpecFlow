# Task / 子任务 T01：文档契约与模板
最后修改时间: 2026-10-10 21:38:47

## Review status / 审查状态

Accepted

## Parent and authority / 父任务与权威记录

[总意图](../../intent/20261009-workload-aware-task-decomposition.md)，[总计划](../../plan/20261009-workload-aware-task-decomposition.md)。分配和执行状态以总计划 T01 登记为准；本文记录局部方案与交付事实。

## Goal and acceptance / 目标与验收

交付一套可供仲裁与执行会话共用的文档契约，对应 A01–A09。所有任务采用意图、计划、实现、验证；复杂度只决定是否增加 task。大任务能表达 DAG、前置条件、分配、局部实施和交付审查。字段和状态分别定义，有单一维护来源。

## Inputs and eligibility / 输入与可开始条件

无前置任务。总计划及本方案被接受、用户明确授权 Implementation，且总计划登记有效分配后才开始。本文不自行授予执行权。

## Scope and files / 范围与文件

修改 plugins/specflow/skills/specflow/template/intent.md、plan.md、verification.md，删除模式字段及按模式分支；新增 task.md、handoff.md 及 references/task-coordination.md。技术设计在计划 / task 中表达；历史过程文档和用户已有 spec.md 不在删除范围。

顺序调整：现有 CLI init 仍直接读取 plugin 的 spec.md，删除动作移到 T03 与消费者取消引用一起完成。T01 保留该过渡文件，但它不属于新文档契约；本轮不修改 CLI 来绕过该依赖。

不修改 skill 入口、Python CLI、安装引擎和 README；这些由后续节点负责。多份模板共享同一契约，集中交付；若字段设计仍明显过大，先回报主会话调整节点。

## Implementation outline / 实施安排

1. 固定任务定义 / 执行登记字段、任务 ID、辅助文档路径、依赖放行和编号撤销规则。
2. 在意图与计划模板加入工作量评估及条件性 task 拆分，所有任务保留计划；技术设计纳入计划 / task，协作细节集中放入参考文件。
3. 建立单任务模板和提示词模板，包含权威位置、阶段授权、基线、接收与交付要求。
4. 在验证模板加入子任务证据、版本有效性、集成与总体验收归属。

## Checks and delivery / 检查与交付

用小任务、串行依赖、竞争请求和重新分配样例检查字段能表达完整事实；核对统一流程、复杂度仅决定 task、无重复归属维护、无自动跨阶段、无原子互斥承诺。交付可读取的文档版本、字段决策、样例结论和剩余风险，由主会话 review 后放行 T02 / T03。

## Risks / 风险

模板可能膨胀或重复；优先保留小任务路径和按需参考。任务方案 Accepted 与执行交付 accepted 必须区分。单一写入者约定依赖参与者遵守规则，不能提供原子互斥。

T02 / T03 交付前，skill 入口与 CLI 仍执行旧协议；新增 task / handoff 暂不能通过现有 init 获取，CLI 所需的 spec 模板暂时保留。T04 才核对发行包资源，不将本次源码资源检查视为完整迁移或安装验证。

## Reception, progress and result / 接收、进展与结果

- 2026-10-10 21:17:31：用户授权“开始 T01”，当前会话 / root 接收实施。
- 有效分配编号：T01-7ffdca45fef046b78bf269d520b14903；方案修订 1，权威登记见总计划。
- 工作基线：93231697829a595bfcc56705a4c2cd76c5e70223，及同一工作区内已接受的意图、计划和任务方案。
- 2026-10-10 21:29:19：六份资源完成，交付版本为 T01-docs-20261010-212919，总计划登记 submitted，等待审查；Review status Accepted 仍只表示方案已接受。

## Delivery and review / 交付与审查

当前分配编号：T01-7ffdca45fef046b78bf269d520b14903；方案修订 1。无前置交付。交付位置为 D:/SourceCodes/mywork/SpecFlow 的当前工作区，基于 93231697829a595bfcc56705a4c2cd76c5e70223；未提交的资源以以下 SHA-256 标识本次版本。后续修改需重新核对版本，不能仅用基线提交认定本次交付内容。

### Actual changes / 实际变更

- intent：移除模式字段，增加有依据的工作量评估、候选拆分与依赖；区分工作量、复杂度和风险，允许保持单任务或先调查，对应 A01 / A02。
- plan：技术设计纳入计划，固定任务定义与执行登记两表，记录协调根、方案修订、DAG、并行和分配历史，对应 A03–A05 / A08。
- task / handoff：记录局部范围、接收、进展、证据和交付，提示词绑定权威记录、唯一分配、授权与基线，默认交接给可见会话，对应 A06 / A07。
- verification：核对当前有效交付、前置版本、集成与总体验收，区分开发检查和整体 Verification，对应 A09。
- task-coordination：集中定义状态、可分配条件、竞争处理、撤销与重新安排；覆盖四个规则走查示例。协议入口接入仍属于 T02。

### Resource version / 资源版本

以下路径均相对于 plugins/specflow/skills/specflow/。

| 文件 | SHA-256 |
| --- | --- |
| template/intent.md | `b50ba867ac5f21e19ec5c75c3698ff685cfe77dc8201d83fc0aa1eb6396b330b` |
| template/plan.md | `365f0cdc5b216af6e29137788c1bfe43747f86a0df1f6a27c9cb445826759ed3` |
| template/verification.md | `f7e78950f8c9d78fbf41e3dde189a856197eb9a0f60b4745d343e36d2820de70` |
| template/task.md | `0768403695f693e7a337c6ae76af084c2aff79bd8316c255fd267ea26a94bf9a` |
| template/handoff.md | `edf761433c50b4d48623314f6512718fd2922b88423ecd31a26e059e464e789a` |
| references/task-coordination.md | `7f89e78e3a27c15d83587451ab9e6ae6c1c2d859cb2bf1a8f5d0bc66ff1a9847` |

### Worked cases / 规则走查结果

这些是文档字段与决策走查，没有启动额外会话或真实并发执行者。

| 场景与输入 | 核对结论 |
| --- | --- |
| 小任务：单一明确结果，范围与检查集中 | 意图记录不拆分依据；计划保留技术选择与步骤，将协调节写为不适用并移除占位表；验证保留三类阶段记录，不创建 task。通过。 |
| T02 依赖 T01；上游提交或版本不可访问 | T01 为 submitted 时等待；即便 accepted，产物无法用于下游基线时仍等待；实现、检查、接受和版本可用后才检查 T02 自身授权及冲突。通过。 |
| A、B 同时请求 T01 | 仲裁者顺序处理，为 A 登记唯一编号后，B 的请求依据当前 assigned 状态等待或改选；执行者只记录 task 接收与进展，不能自行授予执行权。通过。 |
| A 的旧分配被撤销，B 获新编号，A 迟到提交 | 撤销前核实停止与共享修改；旧编号及结果保留在历史，迟到交付只供复核，不能把 B 的当前分配置为 accepted；上游变更还须复核下游。通过。 |

### Checks / 检查结果

- `uv run --locked --no-sync pytest tests/test_cli.py`：7 项通过；现有 init 仍能读取四份过渡模板。
- `python C:/Users/leon/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/specflow/skills/specflow`：通过，输出 Skill is valid。先用项目 uv 环境运行时缺少 yaml，改用已安装的系统 Python 后通过，没有修改项目依赖。
- PowerShell 只读检查：八份过程文档的方案均为 Accepted，时间戳符合要求，19 个本地文档链接有效；六份资源无模式字段、独立 Spec 标题、尾随空白或复制后失效的相对资源链接。
- DAG 检查：六个唯一节点、六条依赖，无自依赖或环；Mermaid 图与任务定义表一致，合法顺序为 T01、T02、T03、T04、T05、T06。
- `git diff --check`：通过；实际产品变更仅为本任务的六份 Markdown 资源。过程记录同步不代表修改其他任务的实现。
- 完整项目检查、安装包 smoke 与整体 Verification 尚未运行，分别由后续节点承担；本次没有新增固定措辞测试。

### Review / 审查记录

2026-10-10 21:38:47：用户要求“推进下一步”，主会话复核六份资源与记录哈希一致，检查字段、依赖放行、分配与撤销规则、四个场景及既有检查证据，无阻止接受的发现。总计划已将 T01-docs-20261010-212919 登记为 accepted；T02 / T03 可使用此交付作为前置输入，各自执行仍按总计划安排。这是 T01 交付审查，不代表整体 Verification 完成。
