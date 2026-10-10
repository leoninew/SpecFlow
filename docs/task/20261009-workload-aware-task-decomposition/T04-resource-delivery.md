# Task / 子任务 T04：发行资源与安装边界
最后修改时间: 2026-10-10 22:31:57

## Review status / 审查状态

Accepted

## Parent and authority / 父任务与权威记录

[总意图](../../intent/20261009-workload-aware-task-decomposition.md)，[总计划](../../plan/20261009-workload-aware-task-decomposition.md)。依赖、分配和执行状态以总计划 T04 登记为准。

## Goal and acceptance / 目标与验收

统一流程的五份模板在源码、editable 安装和干净 wheel 中可读取，原生 plugin 包包含 skill 参考与模板，保持唯一发现来源。对应 A11。

## Inputs and eligibility / 输入与可开始条件

直接前置 T03：CLI 行为及局部检查已接受，代码版本可用于工作基线。需计划接受、Implementation 授权和有效分配；与 T03 串行。

## Scope and files / 范围与文件

修改 pyproject.toml 的资源配置、src/specflow/cli.py 的必要资源读取、相关测试；必要时增强 .github/workflows/release.yml 既有 wheel smoke test。

审查 scripts/install.py 项目配置与包校验、tests/test_install.py。整个 skill 目录已通过 plugins/specflow 提供，配置足够时不改通用同步引擎；通用缺陷另行报告，不局部分叉客户端 adapter。

不新增用户 Home 镜像、独立重复 skill 来源、调度引擎或自动真实安装。版本升级在交付准备时按用户要求处理。

## Implementation outline / 实施安排

1. 先在隔离环境验证 wheel 的 init，确定当前资源缺口；模板以仓库 plugin 中的文件为唯一源。
2. 用 Hatch 构建映射将模板纳入包资源，用资源 API 读取，并验证源码 / editable 的同源路径。
3. 建立仓库外 init / status smoke，检查五份模板可读取、不生成 spec.md，status 报告三个活动文档类型，避免仅以 --help 作为资源验证。
4. 使用 JSON、源路径和 fake runner 核对原生插件资源引用；无需真实写入客户端状态。

## Checks and delivery / 检查与交付

构建发行包，在临时环境安装 wheel 并从仓库外运行 CLI；记录源码、editable、wheel 三种结果，以及 plugin 源引用检查。提交改动、产物检查证据和风险；主会话接受后供 T05 使用。

## Risks / 风险

Hatch editable 与 wheel 的资源路径可能不同；打包修复不得创建第二份手工维护模板。真实安装可能有外部状态副作用，局部测试使用隔离环境。

## Reception, progress and result / 接收、进展与结果

- 2026-10-10 21:59:35：用户要求继续推进，当前会话 / root 接收 T04 Implementation；方案修订 1。
- 分配编号：T04-4c9b7cec6fbc4f49bb5687978251d591；权威登记见总计划。
- 工作基线：93231697829a595bfcc56705a4c2cd76c5e70223，加已接受的 T01 至 T03 交付及过程文档；直接前置 T03 的代码、测试哈希和旧模板删除已核对。
- 已找到 D:/ProgramFiles/Cygwin64/Cygwin.bat，支持指定目录及 -c 命令，GNU Make 4.4.1 可用。
- 2026-10-10 22:07:00：本次实现与局部检查完成，总计划登记 submitted；交付版本 T04-resources-20261010-220700，等待审查。

## Delivery and review / 交付与审查

分配编号：T04-4c9b7cec6fbc4f49bb5687978251d591；方案修订 1。直接前置为已接受的 T03-cli-20261010-215438，开工前已核对代码、测试哈希及旧模板删除；工作基线为 93231697829a595bfcc56705a4c2cd76c5e70223 加 T01 至 T03 交付及过程文档。

交付位置为 D:/SourceCodes/mywork/SpecFlow 当前工作区。CLI 的本次修改是基于 T03 的资源读取增量，下游以本次版本核对集成结果。临时隔离环境位于 C:/Users/leon/AppData/Local/Temp/specflow-t04-4c9b7cec6fbc4f49bb5687978251d591，包含修复前后 wheel、editable 环境和仓库外工作目录。

### Findings and changes / 发现与实际变更

- 修复前构建 wheel 并安装到临时虚拟环境，从仓库外运行 init，退出码 1，FileNotFoundError 指向安装环境下不存在的 Lib/plugins/specflow/skills/specflow/template/intent.md；确认仅测试 import / help 无法发现资源缺失。
- pyproject.toml 使用 Hatch wheel force-include，将 plugin 中唯一维护的模板目录映射到 specflow/template。sdist 保留原始资源，wheel 从 sdist 构建成功。
- CLI 优先通过 importlib.resources 读取包内模板；源码 / editable 无包内目录时，读取同一仓库 plugin 模板源，不新增手工维护副本。
- 发布 workflow 增加仓库外 init / status smoke，核对恰好五份非空模板、重复初始化保持原文、三类规范模板被识别为 Draft。
- 安装测试通过既有纯读取校验核对 Claude / Codex marketplace 与 plugin manifest，并检查七份 skill 资源和无 standalone skill 配置。既有完整 plugin 包路径足够，本次未修改通用安装引擎。

### Delivery version / 交付版本

以下路径均相对于工作区根目录。发行产物保存在已忽略的 dist 中，用于本地检查，没有发布。

| 文件或产物 | SHA-256 |
| --- | --- |
| pyproject.toml | `c847b7adad76d1c5c645f1767113c306dab5863e3737380f4fe5dc8924667e4e` |
| src/specflow/cli.py | `494621aef1367b760713669df9482dec3c0e841c2febfe10c833af8b352bad5c` |
| tests/test_install.py | `685f9066cbadfc3ffd5210f8eaf63ac826c15ae1946af12713b6d120596b9abf` |
| .github/workflows/release.yml | `48fa58ed6c8e34fd849b4b294ed437b101a7c0d4f3d6dd6f35606d9fe690aff4` |
| dist/specflow-0.1.1-py3-none-any.whl | `4910a3518d88e88e5d894dcae5a03375a08a90eb5e7be35c61e3e3bcd0c1345c` |
| dist/specflow-0.1.1.tar.gz | `1a07b84fcffa7980a80c95c8c8c19c49456effa562aee6dec8764fed5290c5a0` |

### Checks / 检查结果

项目命令工作目录为 D:/SourceCodes/mywork/SpecFlow。Make 通过 `D:/ProgramFiles/Cygwin64/Cygwin.bat D:/SourceCodes/mywork/SpecFlow -c "make <target>"` 执行。

| 检查 | 实际结果 |
| --- | --- |
| `uv lock --check` | 通过；无需修改锁文件 |
| Cygwin `make check` | 格式、Ruff lint、mypy 全部通过 |
| Cygwin `make test` | 27 项通过，其中 CLI 23 项、安装相关 4 项；安装测试只读配置或使用 fake runner |
| Cygwin `make release` | 成功生成 sdist，再从 sdist 构建 wheel，版本均为 0.1.1 |
| 发行资源内容 | wheel 中恰好五份模板，逐份与仓库源字节一致；sdist 中也保留全部五份源模板 |
| 直接源码 | 在仓库外目录，用隔离 Python 显式加载 src；init 生成五份模板，status 正常报告尚无功能文档 |
| 干净 wheel 安装 | 用 `uv venv` 新建环境、`uv pip install --python <隔离解释器> --no-deps <wheel>` 安装；确认 import 来自隔离 site-packages，仓库外 init / status smoke 通过 |
| 独立 editable 安装 | 另建环境后 `uv pip install --python <隔离解释器> --no-deps --editable .`；确认 import 来自仓库 src，仓库外运行同一 smoke 通过 |
| CI 检查代码 | YAML 可解析；从 workflow 原样提取嵌入的 Python smoke，在上述 wheel / editable 环境执行通过 |
| `git diff --check` | 通过 |

### Risks and review / 风险与审查

2026-10-10 22:31:57：用户要求继续推进，主会话复核四份产品文件、两份构建产物的哈希与记录一致，资源映射及读取、三种本地运行方式、原生插件引用和质量检查证据满足约定，无阻止接受的发现。总计划将 T04-resources-20261010-220700 登记为 accepted。

源码、editable 和 wheel 已在本地 Windows / Cygwin 环境核对；远程 GitHub Actions runner 尚未执行，真实客户端安装状态也未刷新。完整集成验收仍由后续节点承担。T05 所需的 T02 / T04 前置已满足；局部构建与检查不表示整体 Verification 已完成。
