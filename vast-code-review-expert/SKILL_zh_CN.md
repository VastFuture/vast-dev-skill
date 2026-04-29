---
name: vast-code-review-expert
description: "以高级工程师的视角对当前的 git 变更进行专家级代码审查。检测 SOLID 原则违反、安全风险，并提出可行的改进建议。"
---

# Code Review Expert

## 概述

对当前 git 变更进行结构化审查，重点关注 SOLID、架构、可删除代码和安全风险。默认输出审查报告，除非用户明确要求实施变更。

## 严重等级

| 等级 | 名称 | 描述 | 处理方式 |
|------|------|------|----------|
| **P0** | 严重 | 安全漏洞、数据丢失风险、正确性缺陷 | 必须阻止合并 |
| **P1** | 高 | 逻辑错误、重大 SOLID 违规、性能回退 | 合并前应修复 |
| **P2** | 中 | 代码异味、可维护性问题、轻微 SOLID 违规 | 在本 PR 中修复或创建后续任务 |
| **P3** | 低 | 代码风格、命名、轻微建议 | 可选改进 |

## 工作流程

### 1) 预检上下文

- 使用 `git status -sb`、`git diff --stat` 和 `git diff` 确定变更范围。
- 必要时，使用 `rg` 或 `grep` 查找相关模块、用法和契约。
- 识别入口点、所有权边界和关键路径（认证、支付、数据写入、网络）。

**边界情况：**
- **无变更**：如果 `git diff` 为空，告知用户并询问是否要审查已暂存的变更或特定提交范围。
- **大规模 diff（>500 行）**：先按文件汇总，再按模块/功能区域分批审查。
- **混合关注点**：按功能逻辑分组，而非仅按文件顺序。

### 2) SOLID + 架构异味

- 加载 `references/solid-checklist.md` 获取具体审查提示。
- 重点查找：
  - **SRP**：职责过载的模块，包含不相关的职责。
  - **OCP**：频繁通过编辑添加行为，而非使用扩展点。
  - **LSP**：违反预期的子类，或需要类型检查的子类。
  - **ISP**：包含未使用方法的宽接口。
  - **DIP**：高层逻辑与低层实现紧耦合。
- 提出重构建议时，解释*为何*它能改进内聚/耦合，并概述最小、安全的拆分方案。
- 如果重构较复杂，提出增量计划而非大规模重写。

### 3) 可删除候选 + 迭代计划

- 加载 `references/removal-plan.md` 获取模板。
- 识别未使用、冗余或通过功能开关禁用的代码。
- 区分**立即安全删除**与**计划推迟删除**。
- 提供包含具体步骤和检查点（测试/指标）的后续计划。

### 4) 安全性和可靠性扫描

- 加载 `references/security-checklist.md` 获取覆盖范围。
- 检查项：
  - XSS、注入（SQL/NoSQL/命令）、SSRF、路径遍历
  - AuthZ/AuthN 缺口、缺少租户隔离检查
  - 日志/env/文件中的密钥泄露或 API 密钥
  - 速率限制、无界循环、CPU/内存热点
  - 不安全反序列化、弱加密、不安全默认值
  - **竞态条件**：并发访问、检查后操作、TOCTOU、缺少锁
- 同时指出**可利用性**和**影响**。

### 5) 代码质量扫描

- 加载 `references/code-quality-checklist.md` 获取覆盖范围。
- 检查项：
  - **错误处理**：吞掉的异常、过于宽泛的 catch、缺少错误处理、异步错误
  - **性能**：N+1 查询、热路径中的 CPU 密集型操作、缺少缓存、无界内存使用
  - **边界条件**：null/undefined 处理、空集合、数字边界、差一错误
- 标记可能导致静默失败或生产事故的问题。

### 6) 输出格式

按以下结构组织审查报告：

```markdown
## Code Review Summary

**Files reviewed**: X files, Y lines changed
**Overall assessment**: [APPROVE / REQUEST_CHANGES / COMMENT]

---

## Findings

### P0 - Critical
(none or list)

### P1 - High
1. **[file:line]** Brief title
  - Description of issue
  - Suggested fix

### P2 - Medium
2. (continue numbering across sections)
  - ...

### P3 - Low
...

---

## Removal/Iteration Plan
(if applicable)

## Additional Suggestions
(optional improvements, not blocking)
```

**行内注释**：使用以下格式标记特定文件的发现：
```
::code-comment{file="path/to/file.ts" line="42" severity="P1"}
Description of the issue and suggested fix.
::
```

**无问题审查**：如果未发现问题，明确说明：
- 已检查的内容
- 未覆盖的区域（例如，"未验证数据库迁移"）
- 剩余风险或建议的后续测试

### 7) 后续步骤确认

提出发现后，询问用户如何处理：

```markdown
---

## Next Steps

I found X issues (P0: _, P1: _, P2: _, P3: _).

**How would you like to proceed?**

1. **Fix all** - I'll implement all suggested fixes
2. **Fix P0/P1 only** - Address critical and high priority issues
3. **Fix specific items** - Tell me which issues to fix
4. **No changes** - Review complete, no implementation needed

Please choose an option or provide specific instructions.
```

**重要提示**：在用户明确确认之前，**不要**实施任何变更。这是审查优先的工作流程。

## 资源

### references/

| 文件 | 用途 |
|------|------|
| `solid-checklist.md` | SOLID 异味提示和重构启发式 |
| `security-checklist.md` | Web/应用安全和运行时风险检查清单 |
| `code-quality-checklist.md` | 错误处理、性能、边界条件 |
| `removal-plan.md` | 可删除候选和后续计划模板 |
