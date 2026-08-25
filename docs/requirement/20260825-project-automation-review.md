# SpecFlow Makefile 审查结果

最后修改时间: 2026-08-25 22:25:34

Review status: Accepted

## 结论

`FAIL`。项目已有 `[project.scripts]`，但 `install` 仍是 uv 开发环境同步，`check` 默认修改源码，`release` 混合插件发布和 editable 安装。

## 证据

- `Makefile:19-20` 使用 `uv sync --group dev`。
- `Makefile:25-28` 默认执行 `ruff check --fix`、`ruff format`、mypy。
- `Makefile:36-39` 在 release 中执行 plugin check、editable 安装和 plugin apply。
- `Makefile:33-34` 的 build 才是包构建入口。

## 目标规范

将依赖同步移至 `deps`；`install` 使用 `uv tool install --editable . --force` 并同步 agent plugin/skill；check/test/release 分别遵守 `fix=1`、`cov=1` 和纯构建职责。
