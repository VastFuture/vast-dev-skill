# AGE 目录结构对 docs-pipeline 的启发

## 1. AGE 目录结构完整列表（带职责说明）

源自 `.working/docs/index.md` — Attractor-Guided Engineering 模板的完整 docs/ 结构：

| 目录 | 职责 |
|------|------|
| `docs/context/` | 强制 AI 上下文、所有者优先级、项目级约定 |
| `docs/backlog/` | 优先级候选工作项和 AI 可执行的下一行动 |
| `docs/input/` | 原始外部输入（PM notes、原型截图、文章摘录等） |
| `docs/discussions/` | 可选的需求澄清对话和未解决疑问记录 |
| `docs/requirements/` | 合成后的可直接实现的需求文档 |
| `docs/design/` | 稳定的应用层功能和业务流 owner 文档 |
| `docs/architecture/` | 跨领域技术基线和模块边界 truth |
| `docs/process/` | 工作流和操作流程文档 |
| `docs/lessons/` | 从重复问题和恢复中提取的持久工程教训 |
| `docs/references/` | 稳定的查询指南和维护辅助 |
| `docs/articles/` | 对外的方法论和解释性文章 |
| `docs/examples/` | 可小规模复制的时间戳工作文档骨架 |
| `docs/plans/` | 带关闭标准的执行计划 |
| `docs/audits/` | 审计方法和审计记录，含 plan/closure 审计证据 |
| `docs/skills/` | 可复用的 AI prompt 和审计/审查 playbook |
| `docs/logs/` | 时间戳实现记录 |
| `docs/testing/` | 可选的探索性和手动测试记录 |
| `docs/bugs/` | 非显而易见的 bug 历史和回归笔记 |
| `docs/analysis/` | 可选的研究、权衡分析和被拒绝的方向 |
| `docs/retrospectives/` | 可选的交付后差距分析和过程改进 |
| `docs/archive/` | 被人类决策移动到这里的非活跃文档；保留供历史参考 |

---

## 2. docs-pipeline 当前目录结构

源自 `docs-pipeline/SKILL.md` — 模式 A（文档跟随项目）：

```
项目根/
├── CLAUDE.md                 # Linus 角色 + 沟通规范 + 通用开发规则
├── AGENTS.md                 # Codex CLI 全局指令
├── MBTI_DEV_TRAPS.md         # 16 种人格陷阱清单
├── karpathy-guidelines.md    # LLM 编码行为指南
├── ARCHITECTURE.md           # 基于项目代码探索生成
├── .mcp.json                 # 7 个常用 MCP 服务
├── .claude/
│   └── commands/
│       └── ideas.md          # /ideas 随手记命令
└── docs/
    ├── CLAUDE.md             # docs 总规则
    ├── ideas/
    │   └── README.md         # 灵感池（随手记，零结构）
    ├── research/
    │   └── README.md
    ├── prd/
    │   └── README.md
    ├── exec-plans/
    │   ├── README.md
    │   ├── active/
    │   ├── completed/
    │   └── tech-debt-tracker.md
    ├── handover/
    │   └── README.md
    ├── issues/               # Bug 追踪
    │   └── README.md
    └── lessons/
        └── README.md
```

**共 8 个 docs/ 子目录**：`ideas/`、`research/`、`prd/`、`exec-plans/`、`handover/`、`issues/`、`lessons/`，加根级的 `CLAUDE.md`。

---

## 3. 两者对比分析表格

| 维度 | AGE | docs-pipeline | 差距分析 |
|------|-----|---------------|----------|
| **总规则** | `docs/index.md`（路由权威） | `docs/CLAUDE.md` | AGE 将 index.md 作为顶层路由；docs-pipeline 用 CLAUDE.md — 功能等效，但命名不统一 |
| **AI 上下文** | `docs/context/`（含 README + project-context / ai-autonomy-policy / codebase-map / source-of-truth-and-precedence 等） | **缺失** | docs-pipeline 完全没有 AI 强制上下文层，这是最大功能缺口 |
| **需求输入** | `docs/input/` + `docs/discussions/` + `docs/requirements/` | `docs/prd/` + `docs/research/` | AGE 有三段式（原始输入 → 讨论 → 合成需求）；docs-pipeline 只有两级，prd 实际承担了合成需求角色 |
| **设计分层** | `docs/design/`（应用层）+ `docs/architecture/`（技术层）分离 | **缺失**（只有根级 `ARCHITECTURE.md`） | AGE 明确分离应用层设计和技术架构；docs-pipeline 没有对应目录 |
| **流程文档** | `docs/process/` | **缺失** | AGE 有专门流程文档；docs-pipeline 没有 |
| **执行计划** | `docs/plans/` | `docs/exec-plans/active/` + `docs/exec-plans/completed/` | 功能基本对等，但 AGE 含 audit 关联，docs-pipeline 含 tech-debt-tracker |
| **审计体系** | `docs/audits/`（含 plan/closure 审计方法 + 证据记录） | **缺失** | AGE 有完整 audit 工作流；docs-pipeline 完全没有 audit 概念 |
| **可复用技能** | `docs/skills/`（含 audit/review playbooks） | **缺失** | AGE 有独立 skills 层；docs-pipeline 没有 |
| **实现日志** | `docs/logs/` | **缺失** | AGE 有时间戳实现日志；docs-pipeline 没有 |
| **测试记录** | `docs/testing/` + `docs/testing/known-good-baselines.md` | **缺失** | AGE 有探索性测试和 known-good 基线；docs-pipeline 没有 |
| **Bug 追踪** | `docs/bugs/` | `docs/issues/` | 功能类似，但 AGE 的 bugs/ 专用于"非显而易见回归"；docs-pipeline issues/ 是通用 bug 追踪 |
| **分析研究** | `docs/analysis/` | `docs/research/` | 功能对应，但 AGE analysis 含权衡分析和被拒绝方向 |
| **经验教训** | `docs/lessons/` + `docs/retrospectives/` | `docs/lessons/` | AGE 把 lessons（工程教训）和 retrospectives（交付后差距分析）分开；docs-pipeline lessons 可能是两者的混合 |
| **参考指南** | `docs/references/` + `docs/articles/` + `docs/examples/` | **缺失** | AGE 有大量辅助文档层；docs-pipeline 完全没有 |
| **Backlog** | `docs/backlog/` | **缺失** | AGE 有优先级工作候选队列；docs-pipeline 没有 |
| **Archive** | `docs/archive/` | **缺失** | AGE 有归档机制；docs-pipeline 没有 |
| **Handover** | `docs/handover/` | `docs/handover/` | 两者都有此目录，功能对等 |

---

## 4. 具体的融合建议

### 4.1 高优先级补充（缩小核心功能差距）

| 建议 | 说明 | 操作方式 |
|------|------|----------|
| **新增 `docs/context/`** | 这是 AGE 最核心的结构优势。AI 必须理解项目的强制上下文才能可靠工作。至少补充：`context/README.md`、`context/project-context.md`、`context/ai-autonomy-policy.md`、`context/codebase-map.md` | 在 `docs/` 下新建 `context/` 目录，写入模板文件 |
| **新增 `docs/requirements/`** | 将 `docs/prd/` 逐步演进为更结构化的 requirements 层（输入 → 讨论 → 合成）。或者将 prd/README.md 重命名为 requirements/README.md，明确其合成需求的职责 | 重命名或新建目录 |
| **新增 `docs/audits/`** | 为 exec-plans 中的每个 plan 添加 plan audit 和 closure audit 证据的存储位置 | 在 `docs/exec-plans/` 同级新增 `audits/` |

### 4.2 中优先级补充（完善工作流覆盖）

| 建议 | 说明 |
|------|------|
| **新增 `docs/design/` + `docs/architecture/`** | 将根级 `ARCHITECTURE.md` 的内容拆分到 `docs/architecture/` 和 `docs/design/` 中，前者负责技术基线，后者负责应用层业务设计 |
| **新增 `docs/backlog/`** | 为 AI 提供优先级候选工作项的存储位置，避免工作项散落在 chat 或 issue tracker 中 |
| **新增 `docs/logs/`** | 添加时间戳实现日志，记录每个 session 的关键决策和交付物 |
| **新增 `docs/skills/`** | 将常用的 audit prompts 和 review playbooks 提取为可复用模板 |

### 4.3 低优先级补充（提升辅助能力）

| 建议 | 说明 |
|------|------|
| **将 `docs/issues/` 重命名为 `docs/bugs/`** | 使命名与 AGE 保持一致，更明确其用于"非显而易见的回归" |
| **新增 `docs/process/`** | 添加应用开发工作流文档 |
| **新增 `docs/references/` + `docs/articles/` + `docs/examples/`** | 补充查表指南、方法论文档、骨架文件 |
| **新增 `docs/archive/`** | 为长期不活跃的文档提供归档位置 |

### 4.4 命名与路由统一

| 问题 | 建议 |
|------|------|
| AGE 用 `docs/index.md` 作为顶层路由；docs-pipeline 用 `docs/CLAUDE.md` | 统一为 `docs/index.md` 作为路由入口，`docs/CLAUDE.md` 作为 AI 行为规范（两个文件职责不同） |
| `docs/prd/` 与 `docs/requirements/` 职责重叠 | 逐步将 prd 演进为 requirements，或明确 prd 是"原始需求输入"而 requirements 是"合成后可执行的" |

### 4.5 融合后的目标结构

```
docs/
├── index.md              # 顶层路由入口（从 CLAUDE.md 重命名）
├── CLAUDE.md             # AI 行为规范（保留）
├── context/              # 【新增】强制 AI 上下文
│   ├── README.md
│   ├── project-context.md
│   ├── ai-autonomy-policy.md
│   ├── codebase-map.md
│   └── source-of-truth-and-precedence.md
├── backlog/              # 【新增】优先级候选工作
├── input/                 # 【新增】原始外部输入
├── discussions/           # 【新增】需求澄清对话
├── requirements/          # 【由 prd 演进】合成后需求
├── design/                # 【新增】应用层设计
├── architecture/           # 【由 ARCHITECTURE.md 拆分】技术基线
├── process/               # 【新增】工作流文档
├── plans/                 # 【由 exec-plans 改名】执行计划
├── audits/                # 【新增】审计方法和证据
├── skills/                # 【新增】可复用 AI prompts
├── logs/                  # 【新增】时间戳实现日志
├── testing/               # 【新增】探索性测试
├── bugs/                  # 【由 issues 改名】非显而易见回归
├── analysis/              # 【新增】权衡分析
├── retrospectives/        # 【新增】交付后差距分析
├── references/            # 【新增】查表指南
├── articles/              # 【新增】方法论文档
├── examples/              # 【新增】骨架文件
├── lessons/               # 【保留】
├── handover/              # 【保留】
└── archive/               # 【新增】长期归档
```

---

## 5. 总结

docs-pipeline 的当前结构覆盖了 AGE 约 **40%** 的目录功能（ideas、research、prd、exec-plans、handover、issues、lessons）。最显著的功能缺口是：

1. **强制 AI 上下文层**（`docs/context/`）— 这是 AI 可靠工作的基础
2. **需求生命周期管理**（input → discussions → requirements 三段式）
3. **设计分层**（design 与 architecture 分离）
4. **审计体系**（plan audit + closure audit）
5. **实现记忆**（logs、testing、bugs 的联动）

建议分阶段补充：高优先级先补 context/backlog/requirements 三层，中期补充 audits/design/architecture，长期完善 references/articles/examples/archive 等辅助层。
