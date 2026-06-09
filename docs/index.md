# 文档路由中枢

## 设计哲学

本项目遵循三大核心理念：

1. **设计是吸引子（AGE）**：`design/` 是稳定的基线，代码向设计收敛
2. **代码是真相（DDD）**：`design/` 同时记录实现现状，通过 SDD 同步
3. **SDD 驱动**：先写设计，再写代码，设计即文档

## 目录说明

| 目录 | 职责 | Owner |
|------|------|-------|
| `context/` | 项目上下文、背景信息、全局约束 | PM |
| `backlog/` | 需求池、待办事项、优先级排序 | PM |
| `prd/` | 需求规格、用户故事、验收标准 | PM |
| `design/` | 设计意图 + 实现现状（SDD 双向同步） | Tech Lead |
| `architecture/` | 架构决策、系统设计、技术选型 | Architect |
| `standards/` | 编码规范、最佳实践、团队约定 | Tech Lead |
| `exec-plans/` | 执行计划、里程碑规划 | PM |
| `exec-plans/completed/` | 已完成的历史计划 | PM |
| `lessons/` | 经验教训、复盘文档 | 全员 |
| `logs/` | 变更日志、操作记录 | 全员 |
| `issues/` | 问题追踪、Bug 记录 | QA |

## 任务路由表

| 任务类型 | 目标目录 | 模板文件 |
|----------|----------|----------|
| 新增需求 | `prd/` | `TEMPLATE.md` |
| 问题追踪 | `issues/` | `TEMPLATE.md` |
| 执行计划 | `exec-plans/` | `TEMPLATE.md` |
| 架构设计 | `architecture/` | - |
| 编码规范 | `standards/` | - |
| 经验复盘 | `lessons/` | - |

## 文档所有权

| 所有者 | 目录 | 职责 |
|--------|------|------|
| PM | `context/` | 维护项目背景和全局约束 |
| PM | `backlog/` | 管理需求池和优先级 |
| PM | `prd/` | 编写和维护需求规格 |
| Tech Lead | `design/` | 驱动 SDD 双向同步 |
| Architect | `architecture/` | 维护架构决策 |
| Tech Lead | `standards/` | 维护编码规范 |
| PM | `exec-plans/` | 制定和跟踪执行计划 |
| 全员 | `lessons/` | 记录经验教训 |
| 全员 | `logs/` | 记录操作日志 |
| QA | `issues/` | 追踪和管理问题 |
