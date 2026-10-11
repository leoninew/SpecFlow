# Plan / 计划：明确跨会话接收、回报与状态更新
最后修改时间: 2026-10-11 09:30:04

## Review status / 审查状态

Accepted

## Intent basis / 意图依据

依据[总意图](../intent/20261011-handoff-reporting-clarity.md)，用户已要求更新 skill 和文档，当前授权为 Implementation 及必要开发检查。

## Technical decisions / 技术选择

- 协作参考集中定义责任、记录时点、授权与回报方式；skill 保留关键执行要求并指向参考。
- task、handoff 和 plan 模板提供可直接填写的字段与操作清单。task 中只回报事实和证据，不新增与总登记竞争的状态字段。
- 主会话登记分配即 assigned；执行者有效接收并落盘后可在授权范围内工作，总登记由主会话读到记录后同步，不增加重复开工批准。
- 默认通过当前执行会话输出可复制摘要，由用户转交主会话。写入文档不代表另一个会话已获通知。
- 无 task 时在交接中指定已有计划内的接收与交付记录位置，并协调写入范围；不建立 task 或任务登记表。

## Implementation steps and files / 实施与文件范围

1. 更新 plugins/specflow/skills/specflow/references/task-coordination.md 的交接和状态转换约定。
2. 同步 SKILL.md、template/task.md、template/handoff.md、template/plan.md；明确开工前、执行中、交付前和主会话审查动作。
3. 同步 README.md、README.zh-CN.md 的交接操作与状态更新说明。
4. 运行 skill 结构校验、资源链接与双语结构检查、现有 CLI 模板消费测试及 diff 检查；对照具体交接场景核对规则。

## Tasks and coordination / 子任务与协调

不适用。当前会话完成此单一文档契约增量，不建立子任务。

## Verification plan / 检查与后续验证

开发检查覆盖 A01–A05：有效授权交接、缺失或失效分配、接收落盘后登记滞后、完成写入失败、用户转交与主会话同步、返工、小任务交接。只作规则走查，不自动启动其他会话。最终汇报实际改动、检查与限制；整体 Verification 按后续授权进行。

## Risks and recovery / 风险与恢复

防止将提示词快照当成新授权，或让执行者自行修改全局状态。若发现表述冲突，在本次同一范围内修正；保留已完成历史任务记录及其版本证据，不回写旧验证结果。

## Implementation result / 实施结果

2026-10-11 09:30:04：七份计划内产品文档已更新，无产品范围偏差。增加授权与回报位置引用、执行者必做清单、主会话状态转换证据、用户转交摘要、总登记滞后和记录失败处理；保持既有五种执行状态，无 task 时复用计划章节。

开发检查结果：skill-creator 的 quick_validate.py 输出 Skill is valid；`uv run --locked --no-sync pytest tests/test_cli.py` 为 23 passed，模板初始化与幂等行为正常；`git diff --check` 通过。未改 Python 代码或发行配置，不重复构建发行包；未进行真实多会话执行或刷新客户端插件。结构检查与规则走查不能替代模型执行效果实测。

| 走查输入 | 对照最终文本的结果 |
| --- | --- |
| 有效分配、授权、基线和可写位置齐备 | 先写接收时间、编号、方案、授权和基线，再输出摘要并开工；A01、A02 |
| 只提供 task 路径，或编号已撤销、授权冲突 | 不推定授权；回报具体缺口，暂停受影响的实施；A01、A04 |
| 接收已写入，总登记仍 assigned | 执行者按有效授权继续；主会话读取后同步 running，不能重复派发；A03、A04 |
| 代码完成，交付文档缺失或写入失败 | 交付记录未完成，说明原因并提供待补记录；不能自报已登记 submitted；A02、A04 |
| 完整交付已写入，由用户转交摘要 | 主会话读取当前编号证据，先 submitted，再按实际审查 accepted 或 running；A03、A04 |
| 本地检查失败或有未完成验收 | 如实写入交付记录；完整记录不代表验收通过，下游不得放行；A02、A03 |
| 无 task 的跨会话交接 | 指定既有计划中的可写章节及读取方式，沿用接收和交付步骤，编号与执行状态不适用；A05 |

双语说明同步表达以上责任及时点；task 的 Draft / Accepted 均保留方案语义，没有新增第二套任务状态或自动通知承诺。整体 Verification 尚未启动，本节记录本次实施中的必要检查。
