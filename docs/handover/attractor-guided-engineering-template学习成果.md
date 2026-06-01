# Attractor-Guided Engineering (AGE) 模板学习成果

## 核心概念

**AGE = Attractor-Guided Engineering**

核心理念：项目应该持续回归到一个稳定的产品、设计和架构结构（attractor），在快速 AI 迭代过程中保持方向不偏移。

### 什么是 Attractor？

对于应用项目，attractor 由一组持久的 owner docs 承载：

- `docs/context/` — 强制项目上下文和真相规则
- `docs/backlog/` — 优先级候选工作和 AI 可执行的下一动作
- `docs/requirements/` — 可实施的需求解释
- `docs/design/` — 稳定的应用层行为和功能 owner 文档
- `docs/architecture/` — 稳定的技术结构和模块边界

Plans、tests、audits、logs、bugs 和 verification 不是 attractor，它们是工程 harness（控制工具）。

## AGE 与其他方法论的区分

| 方法论 | 核心问题 |
|--------|---------|
| **Harness-First** | 如何约束 AI？如何验证输出？如何审计和记忆？ |
| **AGE** | 项目应该持续回归到什么样的稳定结构？ |
| **Spec-Driven** | 行为变更应该组织为结构化的 spec delta |
| **Skill Library** | 技能库不能替代项目特定的路由 |

## 目录结构

```
docs/
├── index.md           # 文档路由和目录职责
├── context/          # 强制 AI 上下文、真相优先级、项目惯例
├── backlog/          # 优先级候选工作和 AI 自主标签
├── input/            # 原始 PM、原型、卡片集、文章、外部来源材料
├── discussions/      # 多轮澄清记录
├── requirements/     # 精化的可实施需求文件
├── design/           # 稳定应用层 owner 文档
├── architecture/     # 跨领域技术基线和模块边界
├── plans/            # 带闭包规则的执行计划
├── audits/          # 审计记录和工作流指导
├── skills/          # 可复用提示、审查手册、审计提示模板
├── logs/            # 每日开发日志
├── testing/         # 手动和自动化测试笔记
├── bugs/            # 复杂回归和根因笔记
├── lessons/         # 从失败中提取的持久教训
├── analysis/        # 研究和设计调查笔记
├── retrospectives/  # 实施后差距分析和过程改进
└── archive/         # 被归档的文档
```

## Owner Docs 职责划分

| Owner | 职责 |
|-------|------|
| `docs/context/` | 强制 AI 上下文、真相优先级、项目惯例 |
| `docs/backlog/` | 优先级候选工作和 AI 可执行下一动作 |
| `docs/input/` | 原始外部输入（PM笔记、卡片文档、文章摘录、原型引用） |
| `docs/discussions/` | 需求澄清对话和未解决问题记录 |
| `docs/requirements/` | 可实施需求综合 |
| `docs/design/` | 稳定应用层业务和功能设计 |
| `docs/architecture/` | 跨领域技术和模块边界真相 |
| `docs/lessons/` | 从 bugs、审计、复盘中提取的持久可重用教训 |
| `docs/plans/` | 非平凡工作的执行和闭包标准 |
| `docs/audits/` | 审计工作流记录和审计方法论 |
| `docs/skills/` | 可复用提示、审查手册、审计提示模板 |
| `docs/logs/` | 带日期的实施记忆 |
| `docs/testing/` | 手动和探索性测试记录 |
| `docs/bugs/` | 非平凡 bug 历史和回归笔记 |
| `docs/analysis/` | 研究、权衡分析和被拒绝的方向 |
| `docs/retrospectives/` | 实施后差距分析和过程改进 |

## 默认工作流

1. 在 `docs/input/` 收集原始材料
2. 需要时在 `docs/discussions/` 澄清歧义
3. 在 `docs/requirements/` 综合可实施需求
4. 将稳定设计拆分为 `docs/design/` 和 `docs/architecture/`
5. 路由任务并选择候选可复用技能
6. 当规划触发条件适用时，在 `docs/plans/` 编写或更新计划
7. 在实施前审计计划
8. 实现最小的完整切片
9. 运行验证
10. 对已创建计划运行闭包审计
11. 记录日志和任何需要的 bug 笔记

## 规划触发条件

创建计划的场景：
- 更改 API、数据库/模型、auth、集成、部署或公共契约行为
- 更改跨多个功能表面的用户可见行为
- 涉及多个模块并更改共享行为
- 预计需要多个 AI 会话
- 修改超过 5 个文件或可能超过约 200 行更改
- 需要分阶段执行或明确闭包门控
- 有必须隐藏在 chat 中的未解决产品或技术风险

## 核心原则

> 不要通过 chat 推送重要工作。

- 原始信息进入 `docs/input/`
- 强制上下文和 owner 优先级进入 `docs/context/`
- 优先级下一动作进入 `docs/backlog/`
- 不清楚的问题进入 `docs/discussions/`
- 已解决的需求进入 `docs/requirements/`
- 稳定的设计决策进入 `docs/design/` 和 `docs/architecture/`
- 执行控制进入 `docs/plans/`
- 证明和历史进入 `docs/logs/`、`docs/testing/` 和 `docs/bugs/`
- 过程改进成为 `docs/skills/`、`docs/lessons/` 或 `docs/retrospectives/`

## 稳定文件 vs 带日期文件

- 稳定的 owner docs 保持稳定的文件名
- 时间敏感的过程记录通常带日期

示例：
- 稳定：`docs/design/app-overview.md`、`docs/architecture/system-baseline.md`
- 带日期：`docs/analysis/2026-05-21-topic.md`、`docs/discussions/2026-05-21-topic.md`、`docs/plans/2026-05-21-topic-plan.md`
- 年度组织：`docs/logs/YYYY/MM-DD.md`

## 与 vast-dev-skill 的关联

attractor-guided-engineering-template 是 NOP 框架团队将 AI 开发工作流中轻量级部分提取出来，针对中小型应用团队适配而成。

本项目的 `.working` 目录包含该模板的克隆，供学习和评估使用。