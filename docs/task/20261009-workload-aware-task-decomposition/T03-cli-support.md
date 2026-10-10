# Task / 子任务 T03：CLI 模板与状态配套
最后修改时间: 2026-10-10 21:59:35

## Review status / 审查状态

Accepted

## Parent and authority / 父任务与权威记录

[总意图](../../intent/20261009-workload-aware-task-decomposition.md)，[总计划](../../plan/20261009-workload-aware-task-decomposition.md)。依赖、分配和执行状态以总计划 T03 登记为准。

## Goal and acceptance / 目标与验收

init 提供意图、计划、验证和两份辅助模板，status 正确识别规范审查状态并报告三类阶段文档，保留现有三种文档布局。统一流程中的 Implementation 是实际开发，不要求独立文档。对应 A10。

## Inputs and eligibility / 输入与可开始条件

直接前置 T01：task / handoff 模板及审查格式已接受，且可在工作基线上读取。需计划接受、Implementation 授权和有效分配。可与 T02 隔离并行。

## Scope and files / 范围与文件

修改 src/specflow/cli.py、tests/test_cli.py，并删除 plugins/specflow/skills/specflow/template/spec.md。本节点取消消费者的 spec 引用时一起删除过渡模板，以保持 T01 至 T03 之间的 init 可用。安装包资源读取及构建由 T04 接续，不同时修改这些文件。

不增加 claim、next 或任务自动调度命令，不引入 Markdown 表格解析库，不把 task / handoff 加入阶段发现。Spec 退出活动阶段，但不删除用户已有历史文件。

## Implementation outline / 实施安排

1. 将 intent、plan、verification 三类阶段文档清单与五份模板清单分离；init 增加 task.md、handoff.md，停止生成 spec.md，并保持时间戳与不覆盖已有文件的行为。
2. 以明确的标题匹配规则识别英文和规范双语 Review status，不从正文任意提取 Accepted。
3. status 对三个活动文档类型保留 stage-directory、flat-file 和 feature-directory 发现规则，不再输出 spec 列；历史 spec 文件不主动删除。
4. 增加与可观察行为有关的测试，避免只断言新增常量或模板措辞。

## Checks and delivery / 检查与交付

覆盖五份模板、新 init 无 spec.md、重复 init 不覆盖已有文件及保留历史 spec.md、status 无 spec 列、辅助文件不成为阶段、三种布局，以及英文 / 双语标题下的 Draft / Accepted。运行相关 pytest、format / lint / type 检查，提交代码 diff、检查结果和风险，由主会话接受后放行 T04。

## Risks / 风险

阶段与模板继续混用会造成错误状态输出；过宽标题匹配可能误读正文。资源从 wheel 读取尚由 T04 验证，交付时明确此边界。

## Reception, progress and result / 接收、进展与结果

- 2026-10-10 21:50:17：用户要求“继续推进”，当前会话 / root 接收 T03 Implementation；方案修订 1。
- 分配编号：T03-9e22750a973d43249d0e670dd901377d；权威登记见总计划。
- 工作基线：93231697829a595bfcc56705a4c2cd76c5e70223，加已接受的 T01-docs-20261010-212919、T02-skill-20261010-214428 及过程文档。直接前置 T01 的六份资源哈希已复核，均可读取。
- 2026-10-10 21:54:38：CLI、对应测试及过渡 spec 模板删除完成，总计划登记 submitted；交付版本 T03-cli-20261010-215438，等待审查。

## Delivery and review / 交付与审查

分配编号：T03-9e22750a973d43249d0e670dd901377d；方案修订 1。直接前置为已接受的 T01-docs-20261010-212919，六份资源在本轮开工前核对哈希一致；同一工作区也包含已接受的 T02-skill-20261010-214428。

交付位置为 D:/SourceCodes/mywork/SpecFlow 当前工作区，基线为 93231697829a595bfcc56705a4c2cd76c5e70223 加上述交付和过程文档。以下记录标识本次尚未提交的变更：

| 文件 | 本次交付版本 |
| --- | --- |
| src/specflow/cli.py | SHA-256 `1f080c174b220d4b5b26eba20dfa814b529c0f31e66196b41ebaaecd38804841` |
| tests/test_cli.py | SHA-256 `be0ff899461f17d3976b28793b9661a3777c07d2735b630c8ba5cb2b596be728` |
| plugins/specflow/skills/specflow/template/spec.md | 删除；与 CLI 取消消费者引用一起交付 |

### Actual changes / 实际变更

- 阶段文档清单保留 intent、plan、verification；独立的模板清单另含 task、handoff，辅助模板不参与阶段发现。
- init 新建五份模板，保留时间戳处理，不覆盖既有模板或删除历史 spec 文件，也不自动建立任务过程文档。
- status 保留阶段目录、平铺文件和功能目录三种布局及既有发现优先级；输出三个活动阶段，忽略 spec 和辅助文档。
- 审查标题精确识别英文及规范双语形式，保留原有大小写和首尾空白兼容；正文提及 Accepted 或相近标题不会被当作审查状态。保留 empty / present / unknown / missing 诊断及历史状态文本。
- 移除 plugin 内过渡 spec 模板。实际修改范围与 T03 计划一致，资源加载和 wheel 构建留给 T04。

### Checks / 检查结果

所有命令均在 D:/SourceCodes/mywork/SpecFlow 运行。

| 命令或检查 | 结果 |
| --- | --- |
| `uv run --locked --no-sync pytest tests/test_cli.py` | 23 项通过；覆盖五份初始化模板、重复 init、历史文件保留、三种布局、英文与双语 Draft / Accepted、辅助文档不参与发现及诊断边界 |
| `make check` | 无法执行：当前环境没有 make；改为运行 Makefile 中相同的三条只读命令 |
| `uv run --locked --no-sync ruff format --check src tests` | 最终通过，4 个文件格式正确；首次检查发现本次测试的四处换行差异，按 Ruff 输出修正后复查通过 |
| `uv run --locked --no-sync ruff check src tests` | 通过，All checks passed |
| `uv run --locked --no-sync mypy src` | 通过，2 个源文件无类型问题 |
| `uv run --locked --no-sync specflow status` | 实际工作区 smoke 通过；本功能输出 intent Accepted、plan Accepted、verification missing，符合当前阶段 |
| `git diff --check` | 通过 |

未运行完整测试集、wheel 构建安装或整体 Verification；本任务已完成相关 CLI 测试和项目格式、lint、类型检查，发行资源由 T04 检查，整体集成由 T06 承担。

### Review / 审查记录

2026-10-10 21:59:35：用户继续要求推进，主会话复核 CLI 与测试哈希、旧模板删除、三种布局及初始化兼容行为和检查证据，无阻止接受的发现。总计划将 T03-cli-20261010-215438 登记为 accepted；由 T04 接续发行资源加载。用户补充的 cygwin.bat 已可用于后续 Make 检查。
