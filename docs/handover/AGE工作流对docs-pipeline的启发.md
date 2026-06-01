# AGE 工作流对 docs-pipeline 的启发

## 背景

本文档对比分析 **Attractor-Guided Engineering (AGE)** 模板与 **docs-pipeline** 在工作流设计上的差异，聚焦于 docs-pipeline 可从 AGE 借鉴的关键设计模式。

---

## 一、核心概念对照

### 1.1 AGE 核心概念

| 概念 | 含义 |
|------|------|
| **Planning Triggers** | 明确列举"何种情况下必须创建正式计划"，是 AGE 工作流的守门机制 |
| **强制 AI 上下文** | `docs/context/` 目录存放 AI 必须先读的 5 个核心文件，确保 AI 每次行动前有足够项目上下文 |
| **三步控制循环** | Generate Design Docs → Generate Plan → Audit Periodically |
| **独立 Plan Audit / Closure Audit** | 计划执行前和完成后都必须经过独立审查，防止 AI 自我确认偏差 |
| **Task Routing** | AI 在写代码前必须先分类任务类型，再按类型决定路由 |
| **Autonomy Levels** | `implement / plan-first / ask-first / research-only / blocked` 五级授权体系 |
| **Source of Truth Precedence** | 明确每类问题的"第一答案来源"，避免文档冲突时无人负责 |

### 1.2 docs-pipeline 核心概念

| 概念 | 含义 |
|------|------|
| **产物链路** | `ideas → research → prd → exec-plans/active → exec-plans/completed` |
| **按需推进** | 小功能直接进 exec-plans，大功能走全流程 |
| **幂等初始化** | 重复调用不覆盖已有内容，只补缺失项 |
| **双模式支持** | 文档跟随项目 vs 独立文档仓库 |
| **Plan 模式（可选）** | 通过 `sequential-thinking` MCP 做复杂规划，存入 `plan/*.md` |

---

## 二、关键步骤缺失对比

### 2.1 对比表格

| 步骤/机制 | AGE | docs-pipeline | 缺失影响 |
|-----------|-----|---------------|----------|
| **Stage 0 - 读上下文** | 强制要求读 5 个 `docs/context/` 文件 | 无 | AI 可能在没有项目上下文情况下直接写代码 |
| **Task Routing** | 强制分类任务类型后再行动 | 无 | AI 可能跳过需求澄清直接进入实现 |
| **Planning Triggers** | 明确列举 7 种必须创建计划的情形 | 无（Plan 模式为"可选"） | 复杂任务可能被低质量执行 |
| **Design → Plan 两阶段** | 先产设计文档，再从设计产计划 | 混在一起（PRD 即是需求也是设计） | 计划缺乏独立的设计基底 |
| **Plan Audit** | 所有计划必须通过独立审查 | 无 | 计划错误不会被纠正 |
| **Closure Audit** | 计划完成后必须通过独立审查 | 无 | 完成标准由 AI 自我认定 |
| **Autonomy Levels** | 五级授权体系嵌入上下文 | 无 | AI 不知道何时应"停下来问" |
| **Source of Truth Precedence** | 完整的所有权与冲突解决规则 | 无 | 文档冲突时无法定胜负 |
| **上下文新鲜度** | `documentation freshness` 字段跟踪文档状态 | 无 | AI 可能基于过时文档做决策 |
| **Protected Areas** | 支付/数据删除/认证等区域需要额外审批 | 无 | 高风险变更缺乏特殊保护 |
| **Skill Extraction** | 重复失败后自动提取为可复用 Skill | 无 | 经验无法积累为资产 |
| **Small Complete Slices** | 强调"一个完整切片"优先于"广泛占位" | 无 | AI 可能追求 demo 广度而忽视深度 |

### 2.2 关键缺失详解

#### 缺失 1：Planning Triggers（计划触发条件）

AGE 规定以下情况**必须**创建正式计划：

- 变更 API、数据库/模型、认证、集成、部署或公共契约行为
- 变更多个功能表面的用户可见行为
- 涉及多个模块并修改共享行为
- 预计需要超过一个 AI session
- 修改超过 5 个文件或约 200 行代码
- 需要分阶段执行或明确的关闭门
- 存在未解决的产品或技术风险

**docs-pipeline 的现状**：Plan 模式是"可选"的，没有明确的触发规则。复杂任务可能直接被执行而无正式计划，导致执行路径不清晰、风险未提前暴露。

#### 缺失 2：独立的 Plan Audit / Closure Audit

AGE 要求所有计划在**实施前**和**完成后**都必须经过独立审查（人类评审、子代理评审或冷 replay）。

**docs-pipeline 的现状**：没有计划审查机制。AI 生成的执行计划由 AI 自己判定完成，缺乏独立校验。

#### 缺失 3：强制 AI 上下文

AGE 的 `docs/context/` 目录强制包含 5 个文件：

1. `project-context.md` - 项目身份、当前 milestone、活跃工作项
2. `ai-autonomy-policy.md` - AI 可以自行决定还是必须先问
3. `codebase-map.md` - 代码库路由，避免 AI 重复发现
4. `source-of-truth-and-precedence.md` - 谁说什么算
5. `conventions.md` - 项目通用约定

**docs-pipeline 的现状**：仅在 `docs/CLAUDE.md` 中有简短的目录说明，无强制上下文机制。

---

## 三、强制 AI 上下文设计是否值得借鉴？

### 3.1 AGE 的强制上下文设计优势

1. **降低 AI 盲目性**：AI 每次行动前都有基础上下文，不会"拿到任务就写代码"
2. **可验证的 baseline**：`project-context.md` 包含"文档新鲜度"字段，AI 可判断当前行动基于的文档是否过时
3. **路由清晰**：`codebase-map.md` 直接告诉 AI "这个任务类型从这里开始查"
4. **授权明确**：`ai-autonomy-policy.md` 让 AI 知道自己是处于"implement"还是"ask-first"模式

### 3.2 借鉴建议

**值得借鉴**，但应考虑轻量化：

| AGE 文件 | 建议做法 |
|----------|----------|
| `project-context.md` | 简化为 `docs/project-context.md`，包含：项目技术栈 + 当前 milestone + 活跃需求路径 + 文档新鲜度 |
| `ai-autonomy-policy.md` | 简化为 `docs/autonomy.md`，包含：默认授权级别 + 高风险区域列表 |
| `codebase-map.md` | 简化为 `docs/codebase-map.md`，包含：入口点路由表 + 常用命令 |
| `source-of-truth-and-precedence.md` | 可直接借用 |
| `conventions.md` | 已有 `AGENTS.md` 的一部分，可整合 |

**不建议照搬的部分**：
- `project-context.md` 中的 `Active Work` 表格（需频繁更新，维护成本高）
- 过于复杂的 Protected Areas 表格（初期项目用简单的"高风险区域"列表即可）

---

## 四、Planning Triggers 概念能否融入 docs-pipeline？

### 4.1 融入方案

**可以融入**，建议通过以下方式实现：

#### 方案 A：在 `docs/exec-plans/active/README.md` 中增加触发规则

在执行计划的 README 中增加"计划触发条件"章节：

```markdown
## 计划触发条件

以下情况**必须**创建执行计划并存入 `active/`：

- 涉及 API、数据库模型、认证或外部集成变更
- 跨 3+ 个模块或涉及共享行为修改
- 预计需要超过 1 个 AI session
- 修改超过 5 个文件
- 有未解决的产品或技术风险
- 需要分阶段交付或有明确关闭门

**小功能可直接执行但仍需记录**，写入 `lessons/` 如果踩坑。
```

#### 方案 B：在 AGENTS.md 中增加 Plan 触发规则

在 `AGENTS.md` 的 Plan 模式章节增加触发条件，使其从"可选"变为"条件强制"。

### 4.2 融入的挑战

| 挑战 | 应对 |
|------|------|
| docs-pipeline 的轻量定位可能被破坏 | 将触发规则限制在 1 页内，规则本身简洁明了 |
| 用户可能不习惯被约束 | 提供"跳过确认"选项，仅在高风险情况强制触发 |
| 与现有 Plan 模式的关系需理清 | 明确：Plan 模式是执行方式，触发规则是何时必须用 |

---

## 五、具体建议汇总

### 5.1 立即可采纳（低摩擦）

| 建议 | 优先级 | 说明 |
|------|--------|------|
| 在 `AGENTS.md` 中增加"任务路由"规则：写代码前先分类任务类型 | 高 | 防止直接跳入实现 |
| 在 `docs/exec-plans/active/README.md` 中增加"计划触发条件"章节 | 高 | 填补"何时必须计划"的空白 |
| 在 `docs/exec-plans/completed/README.md` 中增加"完成标准"参考 | 中 | 让完成判定有据可依 |
| 借鉴 `source-of-truth-and-precedence.md` 的冲突解决规则 | 中 | 在 `AGENTS.md` 或 `docs/CLAUDE.md` 中增加"文档所有权与冲突解决"章节 |

### 5.2 中期改进（需要模板更新）

| 建议 | 优先级 | 说明 |
|------|--------|------|
| 新增 `docs/autonomy.md`（五级授权简化版） | 高 | 明确 AI 何时该停下来问 |
| 新增 `docs/codebase-map.md`（入口点路由表） | 高 | 减少 AI 重复发现代码结构 |
| 新增 `docs/project-context.md`（技术栈 + milestone + 文档新鲜度） | 中 | 建立项目基础上下文 |
| 在 `AGENTS.md` 中增加 Plan Audit/Closure Audit 规则 | 中 | 需要子agent或人类review机制 |
| 新增 `docs/skills/` 目录和可复用 Skill 模板 | 低 | 用于沉淀重复失败的检查清单 |

### 5.3 长期方向（可能影响架构）

| 建议 | 说明 |
|------|------|
| 将 `exec-plans/active` 改名为 `plans/active` 与 AGE 对齐 | 目录命名统一可降低跨项目学习成本 |
| 引入"独立审查"机制作为可选增强 | 在复杂项目中可启用子agent review |
| 产物链路增加 `context/` 阶段 | 在 `input` 和 `requirements` 之间增加上下文澄清环节 |

---

## 六、总结

AGE 和 docs-pipeline 代表了两种不同的设计哲学：

- **AGE** 偏向"防患于未然"：通过强制上下文、计划触发条件、独立审计等机制，在错误发生前建立保护网。
- **docs-pipeline** 偏向"按需轻量"：通过幂等初始化、按需推进、最小化模板来降低使用门槛。

两者的优势可以互补。docs-pipeline 的轻量框架 + AGE 的关键守卫机制（Planning Triggers + 强制上下文 + 计划审查）可以在不显著增加复杂度的情况下，显著提升 AI 执行质量。

---

*文档版本：v1.0*
*分析日期：2026-06-01*
*对比版本：AGE (latest) vs docs-pipeline v1.5.0*
