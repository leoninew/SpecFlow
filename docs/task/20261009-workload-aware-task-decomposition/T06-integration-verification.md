# Task / 子任务 T06：集成与整体验证
最后修改时间: 2026-10-10 22:52:31

## Review status / 审查状态

Accepted

## Parent and authority / 父任务与权威记录

[总意图](../../intent/20261009-workload-aware-task-decomposition.md)，[总计划](../../plan/20261009-workload-aware-task-decomposition.md)。依赖、分配和执行状态以总计划 T06 登记为准。

## Goal and acceptance / 目标与验收

检查各节点集成后的实际行为、文档一致性与 A01–A12 全部验收，形成 docs/verification/20261009-workload-aware-task-decomposition.md。局部节点通过不替代本次整体判断。

## Inputs and eligibility / 输入与可开始条件

直接前置 T05：交付被接受且版本可访问，其全部上游交付仍有效。用户看过实现摘要、检查和风险后明确开始 Verification，或在后续请求中明确授权连续实现与验证，才可执行。

## Scope and files / 范围与文件

负责整体验证及同名 verification 文档，汇总任务与总计划的交付记录。不默认顺手修复产品；发现失败时报告，并由主会话回到相关任务安排修改。

## Verification outline / 验证安排

1. 对照意图、计划、节点交付及实际 diff，核对文件范围和所有验收项。
2. 走查小任务与大任务均使用统一流程、复杂度只决定 task，以及依赖等待、并行冲突、竞争分配、编号撤销、跨会话接收、范围重拆和最终集成场景；核对模式规则和独立 Spec 不再参与活动流程，历史资料未被批量改写或删除。
3. 执行 uv lock --check、make check、make test、make release，以及仓库外 wheel init / status smoke，核对原生 plugin 源资源。
4. 记录预期与实际、命令结果、未完成项、风险和结论，不把任务状态文字当成已通过的证据。

## Delivery / 交付与审查

向用户提交总验证记录及实际检查结论。完成 Verification 并确认交付时，在屏幕上提供基于实际 diff 的完整 commit 建议；不自动暂存、提交、推送、发布或刷新用户级插件。

## Risks / 风险

Windows 检查入口需要 GNU Make + bash；缺失工具或检查失败要如实记录。行为走查不能证明不遵守协议的 Agent 也会互斥。

## Reception, progress and result / 接收、进展与结果

- 2026-10-10 22:46:20：用户在实现交付、风险和下一步说明后要求继续推进；当前会话 / root 接收 T06 Verification，方案修订 1。
- 分配编号：T06-c0f0280c10624162be36a1a97b44748b；权威登记见总计划。
- 工作基线：93231697829a595bfcc56705a4c2cd76c5e70223，加已接受的 T01 至 T05 交付及过程文档。开工前核对全部当前有效产品文件与 T04 构建产物哈希一致。
- T03 CLI 的历史版本由 T04 按计划增加资源读取逻辑；核对其当前 T04 版本，并通过完整回归检查确认 T03 行为保留。
- 2026-10-10 22:52:31：整体验证执行完成，提交 T06-verification-20261010-225231；总计划登记 submitted，整体报告待用户审查。

## Result and evidence / 结果与证据

- 分配编号：T06-c0f0280c10624162be36a1a97b44748b；前置交付为已接受的 T05-guidance-20261010-224033 及其有效上游版本，均在当前协调根可读取。
- 交付报告：[总验证](../../verification/20261009-workload-aware-task-decomposition.md)；SHA-256 为 `90833640bc0266e3a2b49e350f54825b7e3a768b5aa996d4dcd2bda95463f071`。报告 Draft 表示待用户审查。
- A01–A12 在首版约定的协议走查和本地执行范围内通过。六节点 DAG 无环、图表一致，检查全部验收归属；产品实际 diff 与计划范围一致，没有新增产品修复。
- `uv lock --check`、Cygwin `make check`、`make test`、`make release` 全通过；27 项测试通过。仓库 status 正确显示本功能 intent / plan Accepted、verification Draft。
- 重建 wheel / sdist，五份模板与仓库源字节一致，包含新版使用说明；干净 wheel、editable 和直接源码在仓库外 init/status 通过。当前 CI Python smoke 原样提取后在本地执行通过，原生 plugin 源配置由测试检查。
- 双语命令、路径、DAG 和本地引用检查通过；skill 结构校验及 `git diff --check` 通过。验证报告记录 12 个协作场景的输入与规则决定，没有实际启动多会话或子 agent。
- 本轮 wheel SHA-256：`6cd6039db00d2cdbc7358ea3d54d5cd41445d66daf5a068c552a1a10f3e9db67`；sdist SHA-256：`8442160b7948faa5b6253025db97b95a5e973b4bdb143c7b9319a45768bceddd`。产物位置在本协调根 dist，替代 T04 的历史构建快照，版本保持 0.1.1。
- 隔离脚本与环境：C:/Users/leon/AppData/Local/Temp/specflow-t06-c0f0280c10624162be36a1a97b44748b。没有修改项目依赖、刷新真实客户端、提交 Git 或发布。
- 尚未实测多会话并行、远程 GitHub Actions 或真实客户端刷新；这些边界与用户已有模板需自行迁移的说明均已写入报告。未发现阻断本次约定验收的问题。
