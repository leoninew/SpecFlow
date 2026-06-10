# 需求：RSPV 文档分类管理

## Review status

Accepted

## Mode

light / 轻量

## Goal

在 `docs/` 下对 RSPV 相关文档进行分门别类管理，使文档结构更清晰、便于查找和维护。

文档采用 stage 目录命名，而不是 `docs/<feature>/<stage>.md` 目录形式。RSPV 表示：

- R：`requirement.md`
- S：`spec.md`
- P：`plan.md`
- V：`verification.md`

具体文件名：

- `docs/requirement/<yyyymmdd>-<功能>.md`
- `docs/spec/<yyyymmdd>-<功能>.md`
- `docs/plan/<yyyymmdd>-<功能>.md`
- `docs/verification/<yyyymmdd>-<功能>.md`

其中 `<yyyymmdd>` 使用 8 位日期格式（例如 `20260609`），用于按时间排序；`<功能>` 用于表达需求或功能主题；stage 目录用于区分 requirement/spec/plan/verification。

## Non-goal

- 不重新设计 SDD 协议本身。
- 不迁移或整理非 RSPV 文档，除非它们需要作为命名示例或兼容性检查。
- 不引入数据库、索引服务或额外文档生成系统。

## Acceptance

- RSPV 文档在 `docs/` 下使用 `docs/<stage>/<yyyymmdd>-<功能>.md` 命名。
- 同一功能的 requirement/spec/plan/verification 通过相同 `<yyyymmdd>-<功能>.md` 文件名归组，分别放在对应 stage 目录下。
- `<stage>` 只使用 `requirement`、`spec`、`plan`、`verification`。
- 文件名能够按日期排序，并能从功能名看出文档主题。
- 后续新增 RSPV 文档时，能够根据命名规则找到合适文件名。

## Risk

- “RSPV 文档”的范围尚未完全明确，实施前需要识别当前仓库中哪些文档属于 RSPV。
- 功能名如果过长或含特殊字符，文件名需要有稳定的 slug/命名规则。
- 如果已有外部引用指向旧路径，移动文档可能造成链接失效。
- stage 目录内文件较多时，需要依赖日期和功能名保持可读性。

## User review notes

-
