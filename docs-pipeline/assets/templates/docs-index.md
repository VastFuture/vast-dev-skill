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
- `docs/design/` 负责稳定的项目吸引子（SDD 双向同步）

## 先读这里

| 如果你需要... | 先读 | 再读 |
| --- | --- | --- |
| 了解强制 AI 上下文和当前项目状态 | `docs/context/project-context.md` | `docs/context/ai-autonomy-policy.md`、`docs/context/codebase-map.md` |
| 选择下一个就绪的工作项 | `docs/backlog/README.md` | `docs/context/ai-autonomy-policy.md`、活跃需求和 owner doc |
| 在编码前路由任务 | `AGENTS.md` | 相关 owner doc |
| 了解当前应用层基线 | `docs/design/README.md` | 按功能模块组织的设计文档 |
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
| 架构变更 | `context/codebase-map.md`, `design/`, `architecture/` | `docs/exec-plans/<task>.md` | 必须 |
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
4. `docs/design/` — 确认稳定的设计基线（SDD 双向同步）
5. `docs/exec-plans/` — 计划触发器满足时写或更新计划
6. 实现
7. 验证
8. `docs/lessons/` — 需要时记录教训

## 目录职责

### 核心（必须有）

| 目录 | 职责 | Owner |
|------|------|-------|
| `docs/context/` | 项目上下文、背景信息、全局约束 | PM |
| `docs/backlog/` | 工作队列、待办事项、优先级排序 | PM |
| `docs/prd/` | 需求规格、用户故事、验收标准 | PM |
| `docs/design/` | 应用层设计 + 系统现状（SDD 双向同步） | Tech Lead |
| `docs/architecture/` | 技术基线、模块边界、分层规范 | Architect |
| `docs/standards/` | 开发规范、代码标准 | Tech Lead |
| `docs/exec-plans/` | 执行计划、里程碑规划 | PM |
| `docs/exec-plans/completed/` | 已完成的历史计划 | PM |
| `docs/lessons/` | 经验教训、复盘文档 | 全员 |
| `docs/logs/` | 开发日志、每日记录 | 全员 |
| `docs/issues/` | 问题追踪、Bug 记录 | QA |

## 核心原则

用文件承载持久真相。

- context 承载项目上下文、背景信息、全局约束
- backlog 承载工作队列、待办事项、优先级排序
- prd 承载需求规格、用户故事、验收标准
- design 承载应用层设计 + 系统现状（SDD 双向同步）
- architecture 承载技术基线、模块边界、分层规范
- standards 承载开发规范、代码标准
- exec-plans 承载执行计划、里程碑规划
- lessons 承载经验教训、复盘文档

## 真相优先级

当文档冲突时，按以下优先级决定：

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | `docs/design/` | 应用层设计 + 系统现状（代码基线） |
| 2 | `ARCHITECTURE.md` | 技术基线和模块边界 |
| 3 | `docs/prd/` | 实施级需求 |
| 4 | `docs/context/` | 项目约定和上下文 |
| 5 | 源代码 | 代码优先（需更新文档） |

## 铁律

- 检索子目录前先读对应 `README.md`；增删文件后同步更新索引
- 一个产物只能在一个目录里；状态流转必须搬家
- `prd/` vs `handover/`：面向未来 → `prd/`；记录已发生 → `handover/`

**文档同步规则**：每次代码变更后，检查 `docs/design/` 是否需要更新（SDD 双向同步）。详见 `docs/design/README.md`。

## 命名规则

- 稳定的 owner docs 保持稳定文件名
- 时间敏感的记录通常包含日期（如 `2026-05-21-主题.md`）
- 计划文件使用 `YYYY-MM-DD-功能名.md` 格式
