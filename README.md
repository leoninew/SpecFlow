# SpecFlow

SpecFlow is **a skill-first development protocol for coding agents**.

它用于在现有 coding agent 工作流中提供低噪声、可审查的阶段边界。它不替代 Claude Code / Codex 的代码理解、规划、实现、测试或 review 能力；它只定义开发过程中的流程模式、阶段文档和 review 规则。

## Skill 定义位置

本项目根目录就是 SpecFlow 项目根目录。

Skill 和文档模板定义在：

```text
.claude/skills/specflow/SKILL.md
.claude/skills/specflow/template/requirement.md
.claude/skills/specflow/template/spec.md
.claude/skills/specflow/template/plan.md
.claude/skills/specflow/template/verification.md
```

这些 Markdown 文件是 SpecFlow 协议的源文件。CLI 需要模板时读取这些文件，不再通过 Python 模块内嵌大段 Markdown。

## 安装

使用 Makefile 安装本项目并覆盖同步 skill：

```bash
make install
```

该命令会：

1. 如果没有 `.venv`，先执行 `uv sync`。
2. 执行 `pip install -e .`，以 editable mode 安装本项目。
3. 覆盖同步 skill 和文档模板到用户目录：

```text
~/.claude/skills/specflow/SKILL.md
~/.claude/skills/specflow/template/requirement.md
~/.claude/skills/specflow/template/spec.md
~/.claude/skills/specflow/template/plan.md
~/.claude/skills/specflow/template/verification.md
```

## 核心定位

SpecFlow 的用户入口是一个 skill，而不是一串 CLI 命令。

用户通常这样开始：

```text
使用 specflow 帮我实现这个功能
```

而不是：

```bash
specflow next
specflow mark
specflow approve
```

CLI 只用于初始化模板和诊断。

## 流程模式

SpecFlow 根据任务大小支持三种模式。模式名支持中英双语：

- `strict` / 严格 / 严格模式
- `standard` / 标准 / 标准模式
- `light` / 轻量 / 轻量模式

### strict / 严格模式

适合需求不清、跨模块、风险高、需要完整设计审查的变更。

```text
Requirement → Spec → Plan → Implementation → Verification
```

### standard / 标准模式

适合普通功能或中等复杂度变更。

```text
Requirement → Plan → Implementation → Verification
```

### light / 轻量模式

适合范围明确的小修小改或简单 bugfix。

```text
Scope note → Implementation → Verification
```

light / 轻量模式仍必须保留最小 scope note / 范围说明和 verification / 验证，避免变成无过程记录的直接实现。

light scope note 可以保持很短：目标、非目标、验收、风险。light verification 也可以保持很短：改了什么、验收对齐、命令结果、遗留风险。

## 文档位置

每个功能使用 feature-specific stage 目录文档：

```text
docs/requirement/<yyyymmdd>-<feature>.md
docs/spec/<yyyymmdd>-<feature>.md
docs/plan/<yyyymmdd>-<feature>.md
docs/verification/<yyyymmdd>-<feature>.md
```

同一功能的 requirement/spec/plan/verification 使用相同 `<yyyymmdd>-<feature>.md` 文件名，分别放在对应 stage 目录下。`<yyyymmdd>` 使用 8 位日期格式，例如 `20260609`。

standard / 标准模式可以不创建 `spec.md`。light / 轻量模式可以只创建最小 scope note / 范围说明和 `verification.md`；scope note 可以写在 `requirement.md` 中。

SpecFlow 包自身的改造文档同样使用该规则，例如：

```text
docs/requirement/20260609-specflow-skill-first-protocol.md
docs/spec/20260609-specflow-skill-first-protocol.md
```

## 文档隔离

用户表达“新需求”、“开始需求”、“新任务”、“新 feature”或类似语义时，默认创建新的 `docs/requirement/<yyyymmdd>-<feature>.md` 文档。

不要修改相邻、同名相近或历史 feature 文档，除非用户明确说沿用、更新现有需求、继续上次，或修改指定过程文档。

## Review status

阶段文档使用简单的 Markdown 状态：

```markdown
## Review status

Draft
```

只使用两种状态：

- `Draft`：阶段内容仍在形成中，或尚未被用户接受。
- `Accepted`：用户已接受该阶段内容，或用户明确要求进入后一阶段。

新文档只写 `Draft` 或 `Accepted`。历史文档可能出现 `Approved`，可以按已接受理解，但不需要主动迁移或清理。

不要新增 `Blocked`、`Completed`、`Proceeded with assumptions` 等状态。风险、假设、阻塞项应写进对应章节。

## 阶段流转

用户明确确认当前阶段时，skill 将当前阶段文档标记为 `Accepted`。

用户明确要求进入后一阶段时，也视为接受前一阶段。例如：

```text
进入 spec
开始 plan
开始实现
继续下一阶段
```

skill 应先将前一阶段标记为 `Accepted`，再进入目标阶段。

如果前置阶段存在 open questions、risks 或 assumptions，但用户仍要求继续，skill 应记录这些事项并继续，不要反复要求用户确认。

## Verification

Verification 是每种模式都必须保留的阶段。

通用 verification 应检查：

- requirement / spec / plan alignment
- actual diff summary
- planned vs actual changed files
- acceptance criteria checklist
- test / command results
- missed or expanded scope
- risks
- incomplete items
- conclusion

运行命令前应先识别当前项目开发语言、工具链，优先使用 README、Makefile、package scripts、CI 配置或项目已有测试/lint/format 命令。

不要在通用协议中硬编码语言、框架或业务特定检查；这些应由具体项目的测试、lint、format、review 或用户要求决定。

## CLI

CLI 是 setup 和 diagnostic support，不是主工作流，也不负责安装 skill。

### `specflow init`

初始化项目级 SpecFlow 文档模板：

```bash
specflow init
```

创建：

```text
docs/
.specflow/template/
```

并写入默认文档模板。

### `specflow status`

诊断 `docs/<stage>/<yyyymmdd>-<feature>.md` 过程文档：

```bash
specflow status
```

示例输出：

```text
docs/20260609-specflow-rename:
  requirement   Accepted
  spec          Draft
  plan          missing
  verification  missing
```

`status` 只显示文档存在性和 review status，不输出 next step，也不推进流程。

## 不向后兼容

SpecFlow 新模型直接替换旧的三 skill 模型：

```text
architect.md
implement.md
review.md
```

不提供旧模型兼容逻辑。

## 不做什么

SpecFlow 不做：

- Agent Runtime
- Workflow Engine
- 持久状态机
- 任务数据库
- 项目管理系统
- 用户手动驱动的一串 CLI 流程
- skill 内部频繁调用 CLI 的隐藏流程

不应新增或推荐以下命令：

```text
specflow next
specflow mark
specflow approve
specflow enter-stage
specflow create-stage
specflow workflow
specflow run
```
