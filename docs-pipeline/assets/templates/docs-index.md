# <project-name> 文档索引

## 用途

`docs/` 目录是 `<project-name>` 的持久记忆和路由中枢。

- 开始非平凡任务前先读这里
- 优先用最小的文件回答当前问题
- 把持久结论放在文件里，不能只在聊天中

## 路由权威

本文件是顶层文档路由器。

- `docs/index.md` 负责导航和目录职责
- `AGENTS.md` 负责代理工作流规则和执行期望
- `docs/design/` 负责稳定的项目吸引子

## 先读这里

| 如果你需要... | 先读 | 再读 |
| --- | --- | --- |
| 了解强制 AI 上下文和当前项目状态 | `docs/context/project-context.md` | `docs/context/ai-autonomy-policy.md`、`docs/context/codebase-map.md` |
| 选择下一个就绪的工作项 | `docs/backlog/README.md` | `docs/context/ai-autonomy-policy.md`、活跃需求和 owner doc |
| 在编码前路由任务 | `AGENTS.md` | 相关 owner doc |
| 了解当前应用层基线 | `docs/design/app-overview.md` | `docs/design/feature-inventory.md` |
| 了解真相优先级和 owner doc 边界 | `docs/context/source-of-truth-and-precedence.md` | 相关 owner doc |
| 读取实现就绪的需求 | `docs/prd/README.md` | 活跃需求文件 |
| 开始或审查非平凡实现 | `AGENTS.md` | `docs/exec-plans/README.md`、活跃计划 |
| 审查持久可复用的工程教训 | `docs/lessons/README.md` | 相关教训 |

## 任务路由

根据任务类型，读取对应文档并产出结果：

| 任务类型 | 必读文档 | 产出位置 | 是否写计划 |
|---------|---------|---------|-----------|
| 需求澄清 | `context/project-context.md`, `prd/` | `docs/prd/<topic>.md` | 否 |
| 设计变更 | `context/source-of-truth-and-precedence.md`, `design/` | `docs/design/<topic>.md` | 视规模 |
| 架构变更 | `context/codebase-map.md`, `design/`, `ARCHITECTURE.md` | `docs/exec-plans/active/<task>.md` | 必须 |
| 纯实现 | `context/project-context.md`, `prd/`, `design/` | 代码 + 测试 | 视规模 |
| Bug 调查 | `context/codebase-map.md`, `issues/` | `docs/issues/<issue>.md` | 视风险 |
| 验证审计 | `context/project-context.md` | 测试结果摘要 | 否 |

**使用方法**：
1. 确定任务类型（从上表选择）
2. 读取对应的"必读文档"
3. 按需写计划（参考"是否写计划"列）
4. 将产出放到指定位置

## 推荐默认路径

大多数任务的默认路径：

1. `docs/context/` — 读取强制项目上下文
2. `docs/backlog/` — 选择下一个工作项
3. `docs/prd/` — 确认实现就绪的需求
4. `docs/design/` — 确认稳定的设计基线
5. `docs/exec-plans/` — 计划触发器满足时写或更新计划
6. 实现
7. 验证
8. `docs/lessons/` — 需要时记录教训

## 目录职责

### 核心（必须有）

| 目录 | 职责 |
|------|------|
| `docs/context/` | 强制 AI 上下文、真相优先级、项目约定 |
| `docs/backlog/` | 工作队列、AI 自主级别标签 |
| `docs/research/` | 调研文档（技术方案、可行性分析） |
| `docs/prd/` | 实现就绪的需求文档 |
| `docs/design/` | 稳定的应用层设计基线 |
| `docs/exec-plans/` | 执行计划（含 Plan/Closure 审计） |
| `docs/lessons/` | 可复用的工程教训 |

### 可选（按需激活）

| 目录 | 什么时候需要 |
|------|-------------|
| `docs/input/` | 有原始 PM 素材需要管理时 |
| `docs/discussions/` | 需求模糊、需要多轮澄清时 |
| `docs/audits/` | 需要独立审计证据时 |
| `docs/bugs/` | 有非显而易见的 bug 需要记录时 |
| `docs/logs/` | 需要每日实现记录时 |
| `docs/testing/` | 需要手动/探索性测试记录时 |
| `docs/skills/` | 有可复用的提示词模板时 |
| `docs/retrospectives/` | 交付后需要复盘时 |

## 核心原则

用文件承载持久真相。

- context 承载强制项目规则和真相优先级
- backlog 承载优先的下一步动作和自主级别标签
- prd 承载应该构建什么
- design 承载必须保持不变的东西
- exec-plans 承载非平凡切片如何闭包
- lessons 承载出了什么问题以及如何避免

## 命名规则

- 稳定的 owner docs 保持稳定文件名
- 时间敏感的记录通常包含日期（如 `2026-05-21-主题.md`）
