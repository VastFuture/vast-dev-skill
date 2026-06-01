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

## 例外情况

- `docs/prd/` vs `docs/handover/`：面向未来 → `prd/`；记录已发生 → `handover/`
- `docs/lessons/` vs `knowledge/`：教训型 → `lessons/`；知识型 → `knowledge/`