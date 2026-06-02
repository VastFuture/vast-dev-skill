# 架构文档索引

## 用途

`docs/architecture/` 定义 `<project-name>` 的稳定跨切面技术基线。

`docs/design/` 用于应用层功能和业务设计。`docs/architecture/` 用于跨功能的技术结构。

## 建议阅读顺序

1. `project-vision.md` — 产品和系统意图
2. `system-baseline.md` — 当前技术栈和运行时基线
3. `module-boundaries.md` — 包/模块/领域所有权边界
4. 随项目增长添加更多特定 owner docs

## Owner Doc 规则

- 一个文档负责一个稳定主题
- 解释当前的理由和约束，而非逐步历史
- 实现改变支持的架构时，在同一变更中更新 owner doc
- 将拒绝的选项和探索笔记移入 `docs/analysis/`
- 当技术规则存在是为了支持具体产品行为时，引用 `docs/design/` 中的相关应用层 owner doc

## 优先级边界

- `docs/design/` 负责应用行为和功能语义
- `docs/architecture/` 负责技术结构和跨切面实现规则
- 如果问题是关于持久化或 schema 真相，模型/schema 文件本身是权威
