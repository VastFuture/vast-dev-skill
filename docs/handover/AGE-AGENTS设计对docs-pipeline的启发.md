# AGE AGENTS.md 设计对 docs-pipeline 的启发

## 文档信息

- 来源：`.working/`（attractor-guided-engineering-template 克隆）
- 对比对象：`docs-pipeline/assets/templates/AGENTS.md`（v3.5，2025-11-30）
- 分析目的：提炼 AGE 框架的设计精华，为 docs-pipeline 的 AGENTS.md 模板升级提供参考

---

## 一、AGE AGENTS.md 核心设计要素

### 1.1 项目定位与核心原则

```
This repository is for an application-layer product, not a framework-core project.
The repo is the source of truth. Chat is only a temporary working surface.
```

**关键差异：** AGE 模板有非常明确的产品类型假设（application-layer product），而 docs-pipeline AGENTS.md 是泛化的"AI 编码代理统一行为约束"，缺乏对目标项目类型的定义。

**启发 1：** docs-pipeline 的 AGENTS.md 应在开头增加"项目类型定位"段落，明确区分：
- 应用层产品（需要完整的需求→设计→计划→验证链路）
- 框架/工具库（可以简化流程，聚焦实现）
- 文档项目（以创作为主，验证方式不同）

### 1.2 Task Routing（任务路由）

AGE 设计的任务分类体系：

| 任务类型 | 路由动作 |
|---------|---------|
| requirement clarification | 先澄清，后行 |
| app-layer design change | 设计优先 |
| architecture change | 架构优先 |
| implementation-only change | 实现优先 |
| bug investigation | 诊断优先 |
| verification or audit work | 验证优先 |

**关键规则：**
```
Do not jump from a feature request directly to code unless the route is already 
obvious from the active requirement and owner docs.
```

**启发 2：docs-pipeline 应增加任务路由决策树**

当前 docs-pipeline AGENTS.md 有"工作流程"和"Plan 模式"，但缺少显式的任务分类和路由指引。建议增加：

```markdown
## 任务路由

在开始非平凡的实现前，先判断任务类型：

| 任务类型 | 前置动作 | 可跳过 Plan 的条件 |
|---------|---------|------------------|
| 需求澄清 | `docs/discussions/` 或 `docs/requirements/` | 仅当需求已完整且明确 |
| 设计变更 | `docs/design/` 或 `docs/architecture/` 更新 | 仅当单文件、单模块、无契约变更 |
| 实现变更 | 确认 owner doc 已更新 | 仅当本地低风险改动（见 Planning Rule） |
| Bug 修复 | 确认复现路径和测试覆盖 | 仅当单文件、有现有测试 |
| 验证/Audit | 确认验证命令存在 | 不适用 |

**铁律：不从功能请求直接跳到代码**，除非路由已从需求和 owner doc 中明确。
```

---

## 二、Operating Rules 的借鉴

### 2.1 AGE 的 15 条 Operating Rules

AGE 的 Operating Rules 可分为几类：

**文件协作类：**
1. Prefer file-in, file-out collaboration
2. Do not treat chat summaries as durable project memory
4. If input is ambiguous, first create or update a file in `docs/discussions/` or `docs/requirements/`

**流程纪律类：**
3. Do not jump from raw PM text or prototype screenshots straight to code when scope is still unclear
5. Create or update a plan before implementation when the planning triggers below apply
7. Keep logs short, dated, and append-only
11. Every created plan MUST pass an independent plan audit... and an independent closure audit

**知识管理类：**
6. Keep `docs/design/` and `docs/architecture/` focused on the current supported baseline
8. Record non-obvious regressions in `docs/bugs/`
9. If prototype and implementation diverge materially, capture the reason in `docs/retrospectives/`
10. Promote repeated process lessons into `docs/skills/` or `docs/audits/` only when the pattern is recurring enough

**代码质量类：**
12. Keep code comments minimal
13. When a referenced file is not found at its expected path, check `docs/archive/`
14. Treat reusable skills as method selectors, not substitutes for requirements, design, or architecture docs
15. When the same error pattern keeps recurring, first promote it into a reusable audit prompt...

**启发 3：docs-pipeline 应增加"协作纪律"章节**

当前 docs-pipeline AGENTS.md 的工作流程章节较散，建议增加独立的"协作纪律"段落：

```markdown
## 协作纪律

**文件优先：**
- 重要结论、计划、决策必须写入文件，聊天记录仅为临时工作面
- 输入不明确时，先在 `docs/discussions/` 或 `docs/requirements/` 澄清，再行实现

**不跳步：**
- 不从 PM 原文或原型截图直接跳到代码（当范围仍不清晰时）
- 不从功能请求直接跳到代码（除非路由已从需求和 owner doc 明确）

**日志规范：**
- 日志应短小、带日期、只追加
- 非显性 regression 记录在 `docs/bugs/`
- 原型与实现出现实质分歧时，记录在 `docs/retrospectives/`

**经验沉淀：**
- 重复出现的问题模式，先提炼为 `docs/skills/` 中的 audit prompt 或 checklist
- 再次复发时，评估是否需要提升为 static check、lint rule 或 CI guard
```

---

## 三、Planning Rule 的融入

### 3.1 AGE 的 Planning Rule 触发条件

AGE 明确列出了必须创建计划的条件：

| 触发条件 | 说明 |
|---------|------|
| changes API, database/model, auth, integration, deployment, or public contract behavior | 触及核心契约 |
| changes user-visible behavior across more than one feature surface | 跨表面行为变更 |
| touches multiple modules and changes shared behavior | 多模块共享行为变更 |
| is expected to take more than one AI session | 预期多会话 |
| modifies more than 5 total files or ~200 changed lines | 文件/行数阈值 |
| needs staged execution or explicit closure gates | 需要分阶段或有明确关闭门槛 |
| has unresolved product or technical risk that must not be hidden in chat | 有未解决风险 |

**唯一例外：**
```
Skip a formal plan only for local low-risk edits such as copy changes, 
small styling fixes, test-only cleanups, and single-file behavior fixes 
with clear existing tests.
```

### 3.2 融入 docs-pipeline 的建议

当前 docs-pipeline AGENTS.md 的 Plan 模式已经很详细，但缺少明确的触发条件判断。建议在"Plan 模式（可选）"之前增加：

```markdown
## Plan 触发判断

**必须创建 Plan 的任务特征（满足任一）：**

| 特征 | 说明 |
|-----|------|
| 触及核心契约 | API、数据库模型、认证、集成、部署或公开契约行为变更 |
| 跨功能表面 | 用户可见行为涉及多个功能面 |
| 多模块共享 | 触及多个模块并变更共享行为 |
| 预期多会话 | 预计需要超过一个 AI 会话 |
| 大规模变更 | 修改超过 5 个文件或约 200+ 行改动 |
| 分阶段执行 | 需要分阶段执行或有明确关闭门槛 |
| 存在未解决风险 | 有产品或技术风险不能在聊天中隐藏 |

**可跳过 Plan 的本地低风险改动：**
- 文本修改（copy changes）
- 小样式修复（small styling fixes）
- 仅测试清理（test-only cleanups）
- 单文件行为修复且已有明确测试覆盖

---

## 四、Skill Usage Rule 的融入

### 4.1 AGE 的 Skill Usage Rule

AGE 规定了使用可复用 Skill 前的四步确认：

```markdown
Before using a reusable skill, confirm all of the following:

1. the task type and route are already clear from the requirement and owner docs
2. the skill matches the work method, not just a similar business label
3. required inputs listed in `docs/skills/README.md` are available
4. the expected output is known and can be stored in the correct docs location

For non-trivial plans, each phase or item that depends on a reusable skill 
should record `Skill: <name>` or `Skill: none`.
```

### 4.2 融入 docs-pipeline 的建议

docs-pipeline 已有 `SKILL.md` 作为 skill 定义文档，但 AGENTS.md 中缺少 Skill 使用规范。建议在现有 Plan 模式后增加：

```markdown
## Skill 使用规范

**使用可复用 Skill 前必须确认：**

1. **任务类型已明确** — 从需求和 owner doc 已能判断任务类型和路由
2. **方法匹配** — Skill 匹配工作方法，而非仅业务标签相似
3. **输入就绪** — `docs/skills/README.md` 中列出的必需输入已存在
4. **输出位置明确** — 预期输出能存入正确的 docs 目录

**计划中的 Skill 记录：**
- 非平凡计划中，依赖可复用 Skill 的每个阶段或条目，应记录 `Skill: <name>` 或 `Skill: none`
- 这有助于审计追踪使用了哪些可复用方法

**Skill 与 Owner Doc 的边界：**
- Skill 是方法选择器，不是需求、设计或架构文档的替代品
- 业务知识首先属于 owner doc（`docs/design/` 或 `docs/architecture/`）
```

---

## 五、Verification Baseline 的启发

### 5.1 AGE 的 Verification Baseline 设计

```markdown
Do not assume this template's example commands are valid for the copied project.

Use the real commands listed in `docs/context/project-context.md`.

If verification commands are blank or still placeholders, stop and fill them 
before reporting verification success.
```

这是 AGE 模板中最实用的设计之一——通过 `project-context.md` 中的"Verification Commands"表格，强制要求团队在开始实现前填写真实验证命令：

| Purpose | Command |
|---------|---------|
| Install dependencies | `<fill real command>` |
| Run app locally | `<fill real command>` |
| Typecheck / compile check | `<fill real command or none>` |
| Build | `<fill real command or none>` |
| Lint / static check | `<fill real command or none>` |
| Unit tests | `<fill real command or none>` |
| E2E / integration tests | `<fill real command or none>` |

### 5.2 对 docs-pipeline 的启发

**启发 4：docs-pipeline 应强制 Verification Baseline 机制**

当前 docs-pipeline AGENTS.md 缺少对验证命令的强制约束。建议在 AGENTS.md 增加：

```markdown
## 验证基线

**原则：不假设模板示例命令对目标项目有效。**

每个项目必须维护自己的验证命令基线，位于项目根 `docs/` 下的验证命令文件中（如 `docs/context/project-context.md` 或 `docs/testing/verification-commands.md`）。

**硬性规则：**
- 如果验证命令为空或仍为占位符，**必须停止并填充**，不得报告验证成功
- 验证命令必须来自实际项目，非示例

**建议的验证命令表格：**

| 目的 | 命令 |
|-----|------|
| 安装依赖 | `<real command>` |
| 本地运行 | `<real command>` |
| 类型检查/编译检查 | `<real command or none>` |
| 构建 | `<real command or none>` |
| Lint / 静态检查 | `<real command or none>` |
| 单元测试 | `<real command or none>` |
| E2E / 集成测试 | `<real command or none>` |
```

**实现建议：** docs-pipeline 在初始化项目时，应自动生成 `docs/context/verification-commands.md` 模板（包含占位符），并通过 AGENTS.md 强制说明：

```
提示 AI：在执行非平凡实现前，检查 docs/context/verification-commands.md 
中的验证命令是否已填充真实值。若仍为占位符，必须先填充再继续。
```

---

## 六、AI Autonomy Policy 的借鉴

### 6.1 AGE 的 Autonomy Levels

| Level | 含义 |
|-------|------|
| `implement` | AI 可在阅读需求、owner doc 和验证命令后实现 |
| `plan-first` | AI 可起草或更新计划，但实现需等待计划审计和受保护区域批准 |
| `ask-first` | AI 必须在变更代码或用户可见行为前询问 |
| `research-only` | AI 可检查、总结和建议，但不能修改产品行为 |
| `blocked` | AI 必须停止，直到阻塞项在文件中解决或人工确认 |

### 6.2 Protected Areas 概念

```markdown
| Area | Rule | Required Evidence |
|------|------|-----------------|
| payment | ask first | owner doc + tests |
| data deletion | ask first | owner doc + tests |
| auth/permissions | plan-first | owner doc + tests |
```

### 6.3 融入 docs-pipeline 的建议

**启发 5：docs-pipeline 应增加简化的 Autonomy Policy**

docs-pipeline AGENTS.md 没有 AI 自主级别概念。建议在项目根 AGENTS.md 中增加：

```markdown
## AI 自主级别

| 级别 | 说明 | 适用场景 |
|-----|------|---------|
| `implement` | 可直接实现 | 本地低风险改动 + 验证命令已填充 |
| `plan-first` | 先起草计划 | 中等复杂度、多文件改动 |
| `ask-first` | 必须先询问 | 触及受保护区域（认证、支付、数据删除） |
| `research-only` | 仅研究 | 文档缺失、基线过时 |
| `blocked` | 必须停止 | 验证命令占位符、受保护区域无 owner doc |

**受保护区域**（需要 owner doc + 测试才能变更）：
- 认证/权限系统
- 支付相关逻辑
- 数据删除路径
- 公开契约（API 行为）

**硬性停止条件：**
- 验证命令仍有占位符
- 受保护区域无 owner doc 和测试策略
- 文档新鲜度为 stale 或 unknown
```

---

## 七、Documentation Ownership 的对比

### 7.1 AGE 的目录所有权定义

AGE AGENTS.md 明确列出了每个目录的职责所有者：

| 目录 | 职责 |
|------|------|
| `docs/context/` | 强制 AI 上下文、真实验证优先级、项目级约定 |
| `docs/backlog/` | 优先级候选工作和 AI-ready 下一步行动 |
| `docs/input/` | 原始外部输入（PM 笔记、卡片文档、文章摘录、原型引用、复制素材） |
| `docs/discussions/` | 需求澄清对话和未解决问题记录 |
| `docs/requirements/` | 实施就绪的需求综合 |
| `docs/design/` | 稳定的应用层业务和功能设计 |
| `docs/architecture/` | 跨领域技术真理和模块边界 |
| `docs/lessons/` | 从 bug、审计和回顾中提取的持久经验教训 |
| `docs/plans/` | 非平凡工作的执行和关闭标准 |
| `docs/audits/` | 审计工作流记录和审计方法 |
| `docs/skills/` | 可复用提示、审查剧本和审计提示模板 |
| `docs/logs/` | 带日期的实施记忆 |
| `docs/testing/` | 手动和探索性测试记录 |
| `docs/bugs/` | 非显性 bug 历史和回归注释 |
| `docs/analysis/` | 研究、权衡分析和被拒绝的方向 |
| `docs/retrospectives/` | 实施后差距分析和流程改进 |

### 7.2 docs-pipeline 当前目录结构

docs-pipeline 产物链路：
```
ideas → research → prd → exec-plans/active → exec-plans/completed → issues/lessons
```

目录：
- `ideas/` — 灵感池
- `research/` — 调研
- `prd/` — 需求规格
- `exec-plans/active/` — 计划进行中
- `exec-plans/completed/` — 计划完成
- `handover/` — 已落地的架构、数据流、设计决策
- `issues/` — Bug 追踪
- `lessons/` — 踩坑教训

### 7.3 对比分析与建议

**关键差距：**

| 维度 | AGE | docs-pipeline |
|-----|-----|--------------|
| 目录覆盖 | 21 个目录，分工极细 | 8 个目录，覆盖基础 |
| 上下文管理 | `docs/context/` 含强制 AI 上下文 | 无对应目录 |
| 真实性权威 | `source-of-truth-and-precedence.md` 定义权威来源 | 无对应文档 |
| 审计体系 | `docs/audits/` 含 plan audit 和 closure audit | 无对应目录 |
| 受保护区域 | `ai-autonomy-policy.md` 定义 | 无对应文档 |

**启发 6：docs-pipeline 应增加核心文档**

| 应增加的文档 | 位置 | 说明 |
|------------|------|------|
| AI 自主级别与受保护区域 | `docs/CLAUDE.md` 或 `AGENTS.md` | 定义 ask-first、blocked 等状态 |
| 验证命令基线 | `docs/context/verification-commands.md` | 必须在实现前填充真实命令 |
| 产物所有权定义 | `docs/CLAUDE.md` | 说明每个目录的职责（已有雏形但不完整） |

---

## 八、综合建议：docs-pipeline AGENTS.md 增强点

### 8.1 优先级排序

| 优先级 | 增强点 | 说明 |
|-------|--------|------|
| **P0** | 验证基线强制 | 增加"占位符验证命令必须先填充"硬性规则 |
| **P0** | Plan 触发条件 | 明确必须创建 Plan 的 7 个条件 |
| **P1** | 任务路由决策树 | 增加任务分类和路由指引 |
| **P1** | 协作纪律章节 | 整合文件优先、不跳步、日志规范等规则 |
| **P2** | Skill 使用规范 | 明确使用 Skill 前必须确认的 4 步 |
| **P2** | AI 自主级别 | 增加 implement/plan-first/ask-first/research-only/blocked |
| **P3** | 受保护区域定义 | 定义支付、认证、数据删除等受保护区域 |
| **P3** | Documentation Ownership | 明确每个 docs/ 子目录的职责 |

### 8.2 建议的文档结构

```markdown
# AGENTS.md（Codex CLI 全局指令）

## 设计目标（可选）

## 优先级栈
（保留现有）

## 沟通风格（保留现有）
- 模式 A/B 输出结构

## AI 自主级别（P1）
- implement / plan-first / ask-first / research-only / blocked
- 受保护区域定义

## 任务路由（P1）
- 任务分类（5-6 种类型）
- 路由决策表
- "不跳步"铁律

## Plan 触发判断（P0）
- 7 个必须创建 Plan 的条件
- 可跳过 Plan 的本地低风险改动示例

## Plan 模式（保留现有）
- complexity 分级
- sequential-thinking 使用规范

## 协作纪律（P1）
- 文件优先
- 不跳步规则
- 日志规范
- 经验沉淀规则

## Skill 使用规范（P2）
- 使用前 4 步确认
- 计划中 Skill 记录要求

## 验证基线（P0）
- 不假设示例命令有效
- 验证命令占位符必须先填充

## 代码规则（保留现有）

## 工具约定（保留现有）

## 安全与合规（保留现有）

## 实施检查清单（保留现有）

## 项目文档（保留现有）
- docs/ 目录使用说明（可补充目录所有权表）
```

---

## 九、总结

### 9.1 AGE 框架的核心价值

1. **Task Routing** — 强制在写代码前做任务分类，避免"功能请求→代码"的跳步
2. **Operating Rules** — 15 条协作纪律形成行为约束，减少 AI 随机性
3. **Planning Rule** — 明确的触发条件让计划创建有据可依
4. **Skill Usage Rule** — Skill 是方法选择器，不是业务知识的替代品
5. **Verification Baseline** — 验证命令必须来自真实项目，占位符是硬性停止条件
6. **AI Autonomy Policy** — 5 级自主级别 + 受保护区域防止高风险变更

### 9.2 docs-pipeline 的定位调整方向

docs-pipeline 作为"初始化文档结构"的 Skill，其 AGENTS.md 模板应从：
- **当前**：泛化的 AI 编码代理行为约束
- **目标**：面向应用层产品的 Attractor-Guided Engineering 工作流指令集

核心增强方向：
1. 在模板中内嵌 Task Routing + Planning Rule + Verification Baseline
2. 将 docs-pipeline 的"幂等初始化"能力与 AGE 的"过程纪律"结合
3. 为使用 docs-pipeline 初始化后的项目，提供更完整的行为约束

### 9.3 下一步行动建议

| 行动 | 说明 |
|------|------|
| 更新 `AGENTS.md` 模板 | 按第 8 节结构增强 docs-pipeline 的 AGENTS.md |
| 增加 `verification-commands.md` | 在模板中增加验证命令基线模板 |
| 更新 SKILL.md | 说明初始化后的项目应如何填充验证命令 |
| 文档移交 | 本分析文档存入 `docs/handover/AGE-AGENTS设计对docs-pipeline的启发.md` |
