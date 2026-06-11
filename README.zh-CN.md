# SpecFlow

**SpecFlow 是面向 coding agent 的 skill-first 开发流程协议。**

[English README](README.md)

SpecFlow 为 coding agent 提供轻量、可审查的软件变更流程。它定义阶段边界和文档约定；它不替代负责读代码、改文件、跑测试或做 review 的 agent runtime。

## 流程模式

![SpecFlow 开发流程模式](docs/assets/specflow-flow-models.jpg)

- `strict` / 严格：适合需求不清、跨模块或高风险变更。
- `standard` / 标准：适合普通功能开发。
- `light` / 轻量：适合范围明确的小改动。

每种模式都保留足够的过程记录，方便人类和后续 agent 审查“改了什么”和“为什么改”。

## 安装

SpecFlow 使用 [uv](https://docs.astral.sh/uv/) 并提供 Makefile。

安装依赖：

```bash
make install
```

以 editable mode 安装包，并将 SpecFlow skill 文件同步到 `~/.claude/skills/specflow/` 和 `~/.codex/skills/specflow/`：

```bash
make skill
```

## 使用

在 coding agent 工作流中作为 skill 使用：

```text
使用 /specflow 开始这个需求。
```

skill 会选择流程模式，写入相关过程文档，并在阶段需要接受时请求 review。

## CLI

CLI 是给 skill 使用的初始化和诊断辅助，不是用户主要入口：

```bash
specflow init
specflow status
```

用户通常从 `/specflow` 开始。SpecFlow 有意避免 `next`、`approve` 这类命令驱动的流程跳转；流程由 skill 结合 agent 的正常工作完成。

## 文档

SpecFlow 按 feature 存放阶段文档：

```text
docs/requirement/<yyyymmdd>-<feature>.md
docs/spec/<yyyymmdd>-<feature>.md
docs/plan/<yyyymmdd>-<feature>.md
docs/verification/<yyyymmdd>-<feature>.md
```

新文档只使用两种审查状态：`Draft` 和 `Accepted`。

## 开发

```bash
make test
```

等价命令：

```bash
uv run python -m pytest -q
```

## 许可证

SpecFlow 使用 [MIT License](LICENSE) 开源。
