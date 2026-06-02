# Exec Plans / 执行计划

> 中大型功能的执行计划，包含分阶段目标、进度状态和决策日志。
> **基于 AGE 增强**：支持 Plan Audit 和 Closure Audit。

**AI 须知：**
- 新建执行计划放在 `active/`，完成后移至 `completed/`
- 纯调研/可行性分析仍放 `../research/`
- 修改或新增文件后更新下方索引
- 检索本目录前先读此文件
- **所有 Plan 必须通过独立审计后才能实施**

---

## 什么时候需要执行计划

| 触发条件 | 说明 |
|---------|------|
| 涉及数据库 schema 变更 | 高风险变更 |
| 跨 3 个以上模块的功能 | 多模块共享变更 |
| 需要分阶段交付的中大型功能 | 需分阶段 |
| 重构或迁移类任务 | 高复杂性 |
| 修改超过 5 个文件或 ~200+ 行变更 | 大规模变更 |
| 预计需要多个 AI 会话 | 长期任务 |
| 有未解决的产品或技术风险 | 有风险 |

**可跳过正式计划的场景**：本地低风险编辑（文案改动、小样式修复、仅测试清理、有清晰测试的单文件修复）。

---

## Plan Decision Table

| 范围 | 计划级别 | 审计规则 | 示例 |
|------|---------|---------|------|
| 琐碎本地编辑 | 无计划 | 无审计 | typo、单样式调整、测试清理 |
| 非平凡跟踪工作 | 完整计划 | 独立 plan audit + closure audit | 小 UI 优化、简单本地 bug 修复 |
| 契约/数据/API/权限/集成/部署/跨表面 | 完整计划 | 独立 plan audit + closure audit | 结算流程、登录行为、数据迁移 |

---

## 审计要求

| 审计类型 | 时机 | 要求 |
|---------|------|------|
| **Plan Audit（计划审计）** | 开始实施前 | 必须通过独立审查 |
| **Closure Audit（闭包审计）** | 标记完成前 | 必须通过独立审查 |

### Plan Audit 检查项

- [ ] 当前基线是否诚实
- [ ] 目标和非目标是否清晰
- [ ] 闭包门控是否真实
- [ ] 是否有隐藏依赖或未解决的需求缺口
- [ ] 是否有范围内的缺陷被悄悄降级
- [ ] 任务路由和技能选择是否诚实、必要、匹配 owner docs
- [ ] 证明和验证是否覆盖每个验收标准

### Closure Audit 检查项

- [ ] 线上行为是否真正落地
- [ ] 文档是否对齐
- [ ] 声称的证明是否实际存在于文件中
- [ ] 计划闭包门控是否全部满足
- [ ] 是否有范围内项目被降级为模糊的 follow-up
- [ ] 验证失败是否被当作非阻塞处理（需明确裁决）

---

## Anti-Slacking Rule / 反拖延规则

每个范围内项目在闭包前必须处于以下状态之一：`landed`、`adjudicated as residual-risk-only`、`moved to explicit successor ownership`、`removed from scope with recorded reason`。

以下词汇在范围内项目中**禁止使用**：`optional`、`if time permits`、`consider`、`maybe`、`nice to have`、`as needed`。

---

## 执行计划模板

```markdown
# {功能名称}

> Plan Status: planned
> 创建时间：YYYY-MM-DD
> 最后更新：YYYY-MM-DD
> Source: <requirement / bug / analysis / request>
> Audit: required

## Current Baseline

- <what is true today>
- <what gap remains>

## Goals

- <result to achieve>

## Non-Goals

- <explicitly excluded work>

## Task Route

- Type: <requirement clarification | design change | architecture change | implementation-only | bug investigation | verification>
- Owner Docs: <paths>

## Execution Plan

### Phase 1 - <name>

Status: planned
Targets: `<paths>`
Skill: `<skill-name | none>`

- [ ] <Fix: defect repair>
- [ ] <Add: net-new code or config>
- [ ] <Decision: record rationale and alternatives>
- [ ] <Proof: test strategy and verification commands>

Exit Criteria:

- [ ] <behavior lands>
- [ ] <relevant docs updated, or No owner-doc update required>
- [ ] `docs/lessons/` updated if lesson learned

## Plan Audit

- Status: <pending | passed>
- Reviewer: <independent reviewer or subagent>
- Evidence: <task id / audit file>

## Closure Gates

- [ ] in-scope behavior is complete
- [ ] relevant docs are aligned
- [ ] verification has run
- [ ] no in-scope item downgraded to deferred/follow-up
- [ ] plan audit passed before implementation
- [ ] closure audit was independent
- [ ] closure evidence exists in files

## Deferred But Adjudicated

### <item name>

- Classification: `watch-only residual | optimization candidate | out-of-scope improvement`
- Why Not Blocking Closure: <reason>

## Closure

Status Note: <why the plan can close>

Closure Audit Evidence:

- Reviewer: <independent reviewer or subagent>
- Evidence: <task id / log link / walkthrough record>

Follow-up:

- <non-blocking follow-up items only>
```

---

## 索引

### Active

| 文件 | 主题 | 状态 |
|------|------|------|
| _（暂无）_ | | |

### Completed

| 文件 | 主题 | 完成日期 |
|------|------|----------|
| _（暂无）_ | | |
