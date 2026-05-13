# Docs 目录

## 产物链路

```
research（调研）→ prd（需求）→ exec-plans/active（计划进行中）→ exec-plans/completed（计划完成）
                                                                   ↓
                                                               lessons（踩坑教训，按需横切）
```

**按需推进，不强制全流程：**
- 小功能：直接进 `exec-plans/active/`，无需 PRD/research
- 中功能：`prd/` → `exec-plans/active/` → `completed/`
- 大功能（schema 变更 / 跨 3+ 模块 / 分阶段交付）：走全流程
- 踩坑了：当下写 `lessons/`，不等流程结束

## 目录职责

| 目录 | 内容 | 时机 |
|------|------|------|
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
