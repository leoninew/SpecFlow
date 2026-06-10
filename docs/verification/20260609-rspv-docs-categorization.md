# 验证：RSPV 文档分类管理

## Review status

Draft

## Mode

light / 轻量

## What changed

- 更新 `sdd status`，优先识别 `docs/<stage>/<yyyymmdd>-<feature>.md` stage 目录文档命名。
- 保留旧的 `docs/<feature>/<stage>.md` 目录式状态识别作为 fallback，避免现有目录式过程文档立刻不可见。
- 更新 CLI 测试，覆盖 stage 目录命名和旧结构 fallback。
- 更新 README、skill prompt、内部 requirement/spec 中的文档位置说明。
- 迁移当前过程文档到 `docs/requirement/20260609-rspv-docs-categorization.md` 和 `docs/verification/20260609-rspv-docs-categorization.md`。

## Acceptance

- RSPV/SDD 过程文档规则已改为 `docs/<stage>/<yyyymmdd>-<feature>.md`。
- 同一功能通过相同 `<yyyymmdd>-<feature>.md` 文件名归组，分别放在对应 stage 目录下。
- stage 识别限定为 `requirement`、`spec`、`plan`、`verification`。
- `sdd status` 能按 stage 目录结构输出各阶段状态。

## Commands

- `make test`：通过，6 passed。

## Remaining risk

- 已迁移当前过程文档到 stage 目录命名。
- 如果同一 feature 同时存在 stage 目录文件和旧结构文件，`status` 会优先显示 stage 目录文件。
