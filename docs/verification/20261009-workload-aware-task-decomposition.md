# Verification / 验证：工作量评估、DAG 拆分与多会话协作
最后修改时间: 2026-10-10 22:52:31

## Review status / 审查状态

Draft

## Intent alignment / 意图对齐

依据已接受的[总意图](../intent/20261009-workload-aware-task-decomposition.md)，本次交付满足首版协议、模板、CLI 与发行资源的约定验收。统一为 Intent → Plan → Implementation → Verification；复杂度只决定是否增加 task。主会话按事实评估工作量、维护 DAG、登记唯一分配并审查交付，默认以提示词交接给用户可见会话。

本报告由 T06 在用户看过实现摘要并要求继续推进后形成。验证已执行，Draft 表示报告尚待用户审查，不表示存在检查失败。跨会话部分采用规则走查，没有启动额外执行者，也不能据此证明任意模型都会遵守文档协议。

## Plan alignment / 计划对齐

依据[总计划](../plan/20261009-workload-aware-task-decomposition.md)修订 1，基线为 develop / 93231697829a595bfcc56705a4c2cd76c5e70223 加 T01–T05 的已接受工作区交付。T06 分配编号为 T06-c0f0280c10624162be36a1a97b44748b，协调根为 D:/SourceCodes/mywork/SpecFlow，执行及集成审查由当前主会话 / root 承担。

实际按文档契约、skill、CLI、发行资源、说明和整体验证六个节点推进。模板是唯一资源源，wheel 通过 Hatch 映射打包；原生插件使用既有完整包路径。未扩展任务调度 CLI，也未分叉通用安装引擎。

## Task deliveries and integration / 子任务交付与集成

| ID | 当前有效交付版本 / 位置 | 必要检查与审查证据 | 集成与基线核对 | 验收归属与结果 |
| --- | --- | --- | --- | --- |
| T01 | T01-docs-20261010-212919；本协调根工作区 | [T01 记录](../task/20261009-workload-aware-task-decomposition/T01-document-contract.md)，六份资源哈希全部匹配，已接受 | skill、CLI 和 README 使用同一文档契约 | A01–A09；通过 |
| T02 | T02-skill-20261010-214428；同上 | [T02 记录](../task/20261009-workload-aware-task-decomposition/T02-skill-workflow.md)，skill 哈希匹配，结构校验及规则走查通过，已接受 | 引用五份模板和协作参考，T01 输入有效 | A01–A09；通过 |
| T03 | T03-cli-20261010-215438；CLI 资源增量以 T04 为准 | [T03 记录](../task/20261009-workload-aware-task-decomposition/T03-cli-support.md)，测试文件哈希匹配；本轮 23 项 CLI 测试通过，已接受 | T04 有计划地更新资源读取，保留 T03 初始化、状态和兼容行为；spec 模板已删除 | A10；通过 |
| T04 | T04-resources-20261010-220700 的四份产品文件；构建产物由本轮重建替代 | [T04 记录](../task/20261009-workload-aware-task-decomposition/T04-resource-delivery.md)，四份产品文件哈希匹配；4 项安装相关测试及发行 smoke 通过，已接受 | T03 行为保留；源码、editable、wheel 读取五份同源模板 | A11；通过 |
| T05 | T05-guidance-20261010-224033；同上 | [T05 记录](../task/20261009-workload-aware-task-decomposition/T05-user-guidance.md)，两份 README 哈希匹配；双语命令、路径、DAG、资源链接核对通过，已接受 | README 与 T02 / T04 行为相符，新内容已进入发行包 | A02、A06、A11；通过 |
| T06 | 本报告及本轮发行产物；[T06 记录](../task/20261009-workload-aware-task-decomposition/T06-integration-verification.md) | 本轮命令、规则走查、版本和 diff 核对见下文 | 未改变 T01–T05 产品文件；整体验证报告待用户审查 | A01–A12；本地约定检查通过 |

开工前对照 T01–T05 记录核对全部当前有效产品文件，以及当时 T04 构建产物的 SHA-256。T03 CLI 哈希与当前文件不同是 T04 已记录的必要资源增量，没有未解释的上游漂移。T04 历史产物不再代表包含 T05 说明的最终包；本轮重新构建并记录新哈希。

总计划检查得到 6 个唯一节点、6 条依赖，无自依赖或环；任务定义表与 Mermaid 边一致，合法顺序为 T01、T02、T03、T04、T05、T06。A01–A12 全部有归属，所有实际实现已在同一工作区集成。没有多 worktree 合并或并发共享写入待处理。

## Actual diff summary / 实际差异摘要

- skill、模板和协作参考统一流程，并要求工作量判断、DAG、分配、接收、交付、撤销及下游失效复核。
- CLI 分离三类阶段文档与五份初始化模板，支持规范双语审查标题，保留历史文档与三种布局。
- wheel 包含仓库同源模板，CLI 使用包资源 API 及源码路径回退；CI 增加仓库外 init/status 检查。
- 中英文说明移除旧模式和三模式图片引用，补充规模、可见会话交接、并发约束和旧模板迁移边界。
- T06 只新增验证报告、维护任务及计划记录、重建已忽略的发行产物；没有新增产品修复。

## Expected vs actual changed files / 预期与实际修改文件对比

| 计划范围 | 实际结果 |
| --- | --- |
| T01：intent、plan、verification 模板；新增 task、handoff、协作参考 | 六份资源全部按计划交付 |
| T02：plugins/specflow/skills/specflow/SKILL.md | 按计划替换旧流程与模式规则 |
| T03：src/specflow/cli.py、tests/test_cli.py；删除 template/spec.md | 按计划交付，历史用户文件由测试确认保留 |
| T04：pyproject.toml、CLI 资源读取、tests/test_install.py、release.yml | 按计划交付；无需修改 scripts/install.py 或 Makefile |
| T05：README.md、README.zh-CN.md | 按计划交付，旧流程图片文件保留 |
| T06：同名 verification、任务与计划过程记录 | 本报告及当前协调记录；不改其他功能的历史文档 |

产品 diff 共涉及 15 个路径：11 个既有文件修改、1 个旧模板删除、3 个新增资源。过程记录为本功能的总意图、总计划、6 份 task 和本验证报告。原生 marketplace、版本号、锁文件、通用安装引擎和既有历史过程文档没有改动。

## Acceptance criteria checklist / 验收标准检查清单

| 验收项 | 证据与结论 |
| --- | --- |
| A01：有依据的工作量判断 | Intent 模板及 skill 要求交付、职责、未知项、检查、审查上下文和协调成本；允许不拆分或调查前置。规则走查通过。 |
| A02：统一流程及文档数量 | skill、五份模板与双语 README 一致；小任务保留三类父级记录，大任务增加每节点一份 task。活动文档无旧模式选择或独立 Spec 流程。通过。 |
| A03：DAG 与验收归属 | 固定任务定义表含直接依赖、交付和验收；本功能实际 DAG 无环、图表一致、引用有效、验收无遗漏；无效输入处理见场景表。通过。 |
| A04：依赖放行 | 契约逐项要求实现、检查、主会话接受、版本可用、授权和无冲突；submitted 或不可访问版本均不放行。规则走查通过。 |
| A05：单一仲裁与有效编号 | 总计划独占分配写入权，唯一编号、历史、worktree 权威位置和非原子边界均明确；本功能六个节点保留分配历史。通过。 |
| A06：默认可见会话交接 | handoff 模板绑定任务、权威位置、编号、基线和阶段；只在请求后生成，不自动启动执行者；小任务无需额外 task。通过。 |
| A07：执行回报与审查 | task 有接收、进展、阻塞和交付记录；允许用户直接沟通，主会话按证据仲裁。通过。 |
| A08：范围变化与重新分配 | 契约规定修订方案、影响分析、核实停止、撤销旧编号、保留历史及迟到交付复核。规则走查通过。 |
| A09：局部检查与整体职责 | skill 与模板区分开发检查、交付接受及整体 Verification；本次由 root 核对全部有效交付和验收。通过。 |
| A10：CLI 与历史兼容 | 23 项 CLI 测试通过；初始化五份模板、幂等与历史保留、三种布局、双语状态及诊断边界均覆盖；无 task/handoff/spec 阶段列。通过。 |
| A11：资源交付与说明一致 | 源码、editable、干净 wheel 在仓库外运行成功；五份模板字节一致，原生 plugin 七份资源及 manifest 校验通过，双语说明一致。通过。 |
| A12：场景与项目检查 | 下述规则走查及本轮质量、测试、构建和 smoke 全部通过；模型跨会话实际执行与真实客户端状态不在本轮实测范围。 |

### Coordination walkthrough / 协作场景走查

以下是以当前 skill、模板及协作契约为依据的输入与决策核对，不是实际启动多个会话的模型效果测试，也没有新增任务状态机或原子锁。

| 场景输入 | 按当前规则得出的决定与记录 |
| --- | --- |
| 单一文字修改，交付和检查集中 | Intent 说明不拆分依据；Plan 写实施与检查，协调节不适用；最后保留 Verification，不建 task。 |
| 多个独立交付，接口选型未知 | 先提出调查节点，输出可供后续使用的结论；进入 Plan 明确边界、直接依赖和验收归属，不为每节点建立整套阶段文档。 |
| T02 依赖 T01，但 T01 仅 submitted | 不派发；取得必要检查、主会话接受和可访问版本后再次核对。T01 accepted 但版本不可访问时也不派发。 |
| A、B 同时请求 T01 | 主会话先登记 A 的唯一编号，B 依据最新 assigned 状态等待或改选；执行者自行编辑总计划不产生有效授权。 |
| 两个无依赖节点都要修改同一接口 | 先协调隔离或串行及集成责任；无依赖不能直接推导为可并发写入。 |
| 已获授权且条件齐备，仅请求交接提示词 | 主会话先登记，再填 handoff；执行者核对权威根、方案、编号、授权、基线及前置版本，在 task 回报接收。提示词本身不启动执行者。 |
| 新 worktree 中的计划副本显示任务未分配 | 回到交接指定的权威记录核对，不从分支副本取得执行权。 |
| 原执行者超时，拟重新分配 | 先核实是否停止并处理共享修改；无法核实时维持阻塞。撤销旧编号后登记新编号，迟到结果仅作历史复核。 |
| 执行中发现新增目标或上游接口变化 | 执行者回报主会话；修订方案并分析下游。受影响的 accepted 交付需要复核时回到 submitted，不以旧接受记录放行。 |
| 引用不存在的 T99、T01 依赖自身、T01 与 T02 互相依赖或遗漏 A12 | 分别触发标识、无自依赖、无环或验收覆盖检查；修正计划前不派发。实际总计划已用一次性结构检查确认没有这些错误；这不是新增 CLI 校验能力。 |
| 各节点自报完成，但集成版本不一致 | 核对有效版本、实际 diff 与总体验收后才能得出整体结论；方案 Accepted 不代替交付接受。 |
| 小任务交给另一会话 | 引用既有意图、计划和范围、阶段、基线即可，不为交接新增 task 或分配表。 |

## Test / command results / 测试 / 命令结果

项目为 Python 3.12+，使用 uv、Ruff、mypy、pytest、Hatchling，公共入口为 Makefile。仓库命令工作目录均为 D:/SourceCodes/mywork/SpecFlow。Make 通过 `D:/ProgramFiles/Cygwin64/Cygwin.bat D:/SourceCodes/mywork/SpecFlow -c 'make <target>'` 执行。

| 命令或检查 | 本轮实际结果 |
| --- | --- |
| `uv lock --check` | 通过，锁文件无需变化 |
| Cygwin `make check` | 通过；4 个文件格式正确、Ruff lint 全通过、mypy 检查 2 个源文件无问题 |
| Cygwin `make test` | 27 passed；CLI 23 项、安装相关 4 项 |
| Cygwin `make release` | 通过；先构建 sdist，再从 sdist 构建 0.1.1 wheel |
| 隔离发行检查脚本 `verify_distribution.py` | 通过；脚本及完整工作目录见下文 |
| 干净 wheel 环境 | `uv venv --python <项目解释器> <隔离环境>`，再 `uv pip install --python <隔离解释器> --no-deps <wheel>`；import 来自隔离 site-packages；仓库外 init/status 通过 |
| CI Python smoke | 从当前 release.yml 原样提取 Python 检查体执行；五份模板非空、重复 init 保持内容、三类模板状态为 Draft，全通过 |
| editable 与直接源码 | 复用 T04 独立 editable 环境，在新目录运行当前 smoke，确认 import 来自仓库 src；直接源码在另一仓库外目录 init/status 通过，模板除初始化时间戳外与源一致 |
| 包内容 | wheel/sdist 中五份模板与仓库源逐字节一致；wheel metadata 包含新版英文 README，sdist 包含新版中英文 README |
| 原生 plugin 资源 | tests/test_install.py 使用纯读取或 fake runner；Claude / Codex / Grok 源引用合法，skill、参考和五份模板共七份资源存在，无新增 standalone 发现来源 |
| skill 结构 | `python C:/Users/leon/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/specflow/skills/specflow` 输出 Skill is valid |
| DAG、文档与双语一致性 | 6 节点 6 边无环；A01–A12 全覆盖；包含验证报告的 12 份文档共 46 个本地链接有效；双语命令、路径、Mermaid 结构一致 |
| `uv run --locked --no-sync specflow status` | 通过；本功能显示 intent Accepted、plan Accepted、verification Draft，符合实际审查状态；其他历史功能保持原有诊断 |
| 产品与历史边界 | 活动产品文档无旧模式选择或旧图片引用；原历史文档、图片、Makefile 和通用安装引擎保留 |
| `git diff --check` | 通过 |

Cygwin 输出无终端作业控制的提示，所有检查命令退出码为 0。未安装或升级项目依赖；仅按计划在临时虚拟环境安装待验证 wheel。

隔离脚本与证据位置为 `C:/Users/leon/AppData/Local/Temp/specflow-t06-c0f0280c10624162be36a1a97b44748b/`，包含 verify_distribution.py、ci_wheel_smoke.py、wheel-venv、wheel-work、editable-work 和 source-work。脚本可供审查；若重跑，应使用新临时目录。临时脚本不作为产品新增工具交付。

### Final artifacts / 本轮发行产物

| 路径 | SHA-256 |
| --- | --- |
| dist/specflow-0.1.1-py3-none-any.whl | `6cd6039db00d2cdbc7358ea3d54d5cd41445d66daf5a068c552a1a10f3e9db67` |
| dist/specflow-0.1.1.tar.gz | `8442160b7948faa5b6253025db97b95a5e973b4bdb143c7b9319a45768bceddd` |

产物仅用于本地验证，仍为原版本 0.1.1，未发布。它们包含已验证的最终产品资源；过程文档在构建后继续补充最终验证记录。

## Missed or expanded scope / 遗漏或扩大的范围

没有发现约定产品目标遗漏或范围扩大。原计划已说明旧 spec 模板删除延至 T03 与 CLI 消费者同时调整；该实施顺序变化已记录，不改变目标或 DAG。

scripts/install.py 原配置已覆盖完整 plugin 包，检查后无需修改。首版保留文档协议和语义审查，不新增 claim/next 命令、自动派发、Markdown 原子锁或任务数据库。

## Risks / 风险

- 工作量判断和拆分质量仍依赖模型与仓库事实，规则走查不能保证一次拆分准确或所有执行者遵守流程。
- 单一仲裁写入者是参与者约定。真实多会话竞争、隔离 worktree 并行开发和跨机器执行未实测。
- 真实客户端插件尚未刷新，本机已安装的旧 skill 可能仍含旧模式；新版源码和安装包可用不等于用户级客户端已迁移。
- 远程 GitHub Actions runner 和真实插件安装未执行；当前证据覆盖本地 Windows/Cygwin、纯读取源配置和 CI Python smoke。Mermaid 检查源码及依赖边，未做渲染检查。
- 用户已有定制模板由 init 保留，更新时需要按新版文档契约核对，不能依靠重复 init 自动迁移。

## Incomplete items / 未完成事项

没有阻止本次首版产品验收的未完成实现或失败检查。待用户审查本报告；真实客户端刷新、发布版本安排、Git 提交和远程发布属于后续交付操作，未在本轮执行。

## Conclusion / 结论

A01–A12 在上述协议走查和本地执行范围内通过，T01–T05 交付版本有效并完成集成，质量、27 项测试、构建与仓库外 smoke 全部通过。可提交整体结果供用户验收。任务执行记录与本报告保持对验证边界的说明，不将文档状态或模型完成声明当成原子互斥、远程 CI 或真实多会话执行的证明。
