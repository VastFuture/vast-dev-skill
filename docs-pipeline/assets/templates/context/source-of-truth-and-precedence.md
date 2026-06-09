# Source of Truth and Precedence / 真相来源与优先级

> 当文档之间或文档与代码之间冲突时，哪个说了算。

## 优先级规则

当不同文档描述不一致时，按以下优先级决定：

| 优先级 | 来源 | 说明 |
|--------|------|------|
| 1 | `docs/design/` | 稳定应用层行为和功能设计 |
| 2 | `docs/architecture/` | 跨领域技术基线和模块边界 |
| 3 | `docs/requirements/` | 已确认的实施级需求 |
| 4 | `docs/context/` | 项目级约定和上下文 |
| 5 | 源代码 | 当文档与代码不一致时，代码优先（需更新文档） |

## Owner Docs 职责

| Owner | 负责内容 | 决策权威 |
|-------|---------|---------|
| `docs/context/` | 强制 AI 上下文、真相优先级、项目惯例 | 最高 |
| `docs/backlog/` | 优先级候选工作和 AI 自主标签 | 无决策权威 |
| `docs/requirements/` | 可实施需求综合 | 需求层面 |
| `docs/design/` | 稳定应用层业务和功能设计 | **应用层最高** |
| `docs/architecture/` | 跨领域技术和模块边界 | **技术层最高** |

## 冲突解决流程

1. 检查哪个文档的优先级更高
2. 如果同优先级，检查哪个文档更新
3. 如果都无法确定，提 issue 给 maintainer

## 文档所有权边界

> 灵感来源：[neat-freak 三层知识体系](https://github.com/VastFuture/khazix-skills/tree/main/neat-freak)

**核心理念**：知识分层，受众不同，职责不重叠

| 文档 | 受众 | 职责 | 不该出现 |
|------|------|------|---------|
| **CLAUDE.md / AGENTS.md** | 项目 AI | 硬边界规则、禁止事项、命令速查 | 历史叙事、"详见 docs/"、详细机制 |
| **docs/context/** | AI 上下文 | 项目约定、验证命令、自主策略 | 详细实现、使用示例 |
| **docs/prd/** | 人类 + AI | 需求、验收标准、技术方案 | 实现细节、运维手册 |
| **docs/design/** | 人类 + AI | 架构、数据模型、设计取舍 | 使用示例、运维手册 |
| **docs/plans/** | AI | 执行计划、风险、依赖 | 需求详情（归 prd/） |
| **docs/handover/** | 人类 | 交接、已知问题、联系人 | 实现细节（归 design/） |
| **docs/issues/** | 人类 + AI | 问题描述、复现步骤、解决方案 | 需求（归 prd/） |
| **docs/lessons/** | 人类 + AI | 教训、预防措施、改进建议 | 单次事故细节 |

**关键判断**：
- "AI 下次编码需要看到什么规则" ≠ "其他人如何接入"
- CLAUDE.md 写"新增了 device flow 五个路由" ≠ docs/integration-guide.md 写"下游怎么接这套 flow"
- 前者是提醒自己，后者是教别人。**两份都要写**

**CLAUDE.md 判断标准**：下次 AI 写代码时如果没看到这条，会不会犯错？
- ✅ 该进：硬边界规则、禁止事项、命令速查、踩坑警示
- ❌ 不该进：历史叙事（"X 时刻起 Y 上线"）、详细机制、单次事故复盘

## 例外情况

- `docs/prd/` vs `docs/handover/`：面向未来 → `prd/`；记录已发生 → `handover/`
- `docs/lessons/` vs `knowledge/`：教训型 → `lessons/`；知识型 → `knowledge/`