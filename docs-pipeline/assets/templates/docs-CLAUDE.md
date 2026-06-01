# Docs 目录

> 产物链路 + Owner Docs 职责划分 + 真相优先级

## 产物链路

```
ideas（随手记）→ research（调研）→ prd（需求）→ exec-plans/active（计划进行中）→ exec-plans/completed（计划完成）
                                                                               ↓
                                                                           lessons（踩坑教训，按需横切）
```

**按需推进，不强制全流程：**
- 小功能：直接进 `exec-plans/active/`，无需 PRD/research
- 中功能：`prd/` → `exec-plans/active/` → `completed/`
- 大功能（schema 变更 / 跨 3+ 模块 / 分阶段交付）：走全流程
- 踩坑了：当下写 `lessons/`，不等流程结束

---

## Owner Docs 职责

每个目录有明确的 owner，决策权威不同：

| Owner | 负责内容 | 决策权威 |
|-------|---------|---------|
| `context/` | 强制 AI 上下文、真相优先级、项目惯例 | **最高** |
| `backlog/` | 优先级候选工作和 AI 自主标签 | 无决策权威 |
| `requirements/` | 可实施需求综合 | 需求层面 |
| `design/` | 稳定应用层业务和功能设计 | **应用层最高** |
| `architecture/` | 跨领域技术和模块边界 | **技术层最高** |
| `plans/` | 执行和闭包标准 | 无决策权威 |
| `audits/` | 审计工作流记录和方法论 | 审计权威 |

---

## 真相来源与优先级

当文档冲突时，按以下优先级决定：

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | `docs/design/` | 稳定应用层行为和功能设计 |
| 2 | `docs/architecture/` | 跨领域技术基线和模块边界 |
| 3 | `docs/requirements/` | 已确认的实施级需求 |
| 4 | `docs/context/` | 项目级约定和上下文 |
| 5 | 源代码 | 当文档与代码不一致时，代码优先（需更新文档） |

---

## 目录职责

| 目录 | 内容 | 时机 |
|------|------|------|
| `ideas/` | 灵感、模糊想法、随笔记录 | 随时，零摩擦捕获 |
| `research/` | 技术方案、可行性分析 | 立项前，不确定怎么做时 |
| `prd/` | 需求规格（做什么、为什么） | 需求方视角，相对稳定 |
| `exec-plans/active/` | 执行计划（怎么做、做到哪） | 开工时建，频繁更新状态 |
| `exec-plans/completed/` | 已完成的执行计划 | 计划完成后从 `active/` 搬家 |
| `exec-plans/tech-debt-tracker.md` | 技术债务清单 | 发现技术债时追加 |
| `handover/` | 已落地的架构、数据流、设计决策 | 沉淀已发生的事实 |
| `lessons/` | 踩坑教训（XX 不能这么做） | 当下记录，独立于流程 |

## 铁律

- 检索子目录前先读对应 `README.md`；增删文件后同步更新索引
- 一个产物只能在一个目录里；状态流转必须搬家
- `prd/` vs `handover/`：面向未来要做 → `prd/`；记录已发生的设计 → `handover/`
- `lessons/` vs `knowledge/`：教训型（不能这么做）→ `lessons/`；知识型（XX 是怎么工作的）→ `knowledge/`
