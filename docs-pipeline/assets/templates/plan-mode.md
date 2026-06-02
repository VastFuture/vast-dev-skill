# Plan 模式详细说明

> 本文档被 AGENTS.md 引用，提供 Plan 模式的完整规范。

---

## 使用场景

- 适用：中等及以上复杂度、多步骤、跨文件/模块/服务的任务
- 不适用：单文件、小改动、一次性问答（直接按普通流程处理即可）
- 当任务看起来「不止两三步」时，优先建议使用 Plan 模式先规划再执行

---

## 入口与工具约束

**入口**：
- Slash 命令：`/prompts:plan <简要任务描述>`
- 示例：`/prompts:plan 帮我设计用户登录模块的实现方案`

**工具约束**：
- 每次进入 Plan 模式时，**必须优先调用 MCP 工具 `mcp__sequential-thinking__sequentialthinking`** 做多步思考
- 第一次调用建议参数：
  - `thought`：1–2 句话说明「正在为本次任务描述制定执行计划」
  - `thoughtNumber = 1`
  - `totalThoughts`：根据复杂度选择（见下文）
  - `nextThoughtNeeded = true`
- 后续调用可根据需要增加/减少 `totalThoughts`，直到计划足够细致且可实施
- 不直接输出工具内部完整推理过程，只用其结果整理结构化计划

---

## 复杂度分级与思考步数

| 复杂度 | 场景 | 推荐 totalThoughts |
|--------|------|-------------------|
| simple | 单文件/函数的小改动，步骤预计 < 5，且无跨系统影响 | 4 |
| medium | 多文件/模块，带一定设计决策（API 变更、数据结构调整等），需补测试和回归 | 7 |
| complex | 跨服务/子系统，或涉及架构/性能/数据迁移等 | 10-12 |

---

## 对话输出规范

在 Plan 模式下，面向用户的回复统一使用下列结构：

```markdown
🎯 任务：<一句话概括当前任务（可使用你的理解）>

📋 执行计划：
- Phase 1: <步骤 1，1–2 句，描述目标而不是实现细节>
- Phase 2: <步骤 2>
- Phase 3: <步骤 3>
...（最多 8–10 步，必要时可再细分）

🧠 当前思考摘要：
- <用 2–4 条 bullet 总结 mcp__sequential-thinking__sequentialthinking 得出的关键结论/权衡>

⚠️ 风险与阻塞：
- <风险 1（例如向后兼容性、数据安全、性能等）>
- <风险 2（例如依赖其他团队/服务、环境限制等）>

📎 Plan 文件：
- 路径：`plan/<你实际创建的文件名>.md`
- 状态：<已创建并写入 / 无法创建（说明原因）>
```

---

## Plan 文件规范

**目录与命名**：
- 以当前工作目录为根，在其中使用 `plan/` 子目录
- 文件建议命名为：`plan/YYYY-MM-DD_HH-mm-ss-<slug>.md`
  - 时间戳：类 Unix 环境用 `date +"%Y-%m-%d_%H-%M-%S"`
  - `<slug>`：从任务描述中提取关键字，去掉空白，转换为小写，非字母数字字符归一化为 `-`
  - 冲突时可在末尾追加 `-1`、`-2` 等后缀

**文件头部元数据**（YAML frontmatter）：

```markdown
---
mode: plan
cwd: <当前工作目录>
task: <任务标题或总结>
complexity: <simple|medium|complex>
tool: mcp__sequential-thinking__sequentialthinking
total_thoughts: <最终使用的思考步数>
created_at: <ISO8601 时间戳或 date 输出>
---
```

**正文结构推荐**：

```markdown
# Plan: <任务简要标题>

🎯 任务概述
<用 2–3 句话说明任务背景和目标。>

📋 执行计划
1. <步骤 1：一句话描述要做什么、为什么>
2. <步骤 2>
3. <步骤 3>
...（一般 4–10 步，根据 sequential-thinking 结果展开）

⚠️ 风险与注意事项
- <风险或注意点 1>
- <风险或注意点 2>

📎 参考
- `<文件路径:行号>`（例如 `src/main/java/App.java:42`）
- 其他有用的链接或说明
```

---

## 多次 Plan 调用的关联规则

**本会话第一次使用 Plan 模式**：
- 为当前任务创建新的 Plan 文件
- 在回复的「📎 Plan 文件」中给出路径

**会话中已有「当前 Plan」时**：

- 用户说「前面/刚才/之前的计划/在原来的基础上调整」等 → **继续同一个 Plan**
  - 使用前一次回复中记录的 Plan 文件路径
  - 先通过 `cat plan/XXXX.md` 回顾，再给出「变更摘要」+ 更新后的计划
  - 写回同一 Plan 文件，可以追加「变更记录」或重写相关小节

- 用户明确说「新的 Plan」「另一个任务」「重新为 YYY 设计方案」等 → **新 Plan**
  - 创建新的 Plan 文件，并在回复中说明与旧 Plan 的关系

- 若语义模糊，先用一句话确认是「调整上一个 Plan」还是「新任务」

---

## 风险与可控手段

- Plan 模式约束无法从系统层硬性强制，仍依赖 LLM 严格遵守本节规则
- 为提高可控性：
  - 要求在 frontmatter 中记录 `tool: mcp__sequential-thinking__sequentialthinking` 与 `total_thoughts`
  - 推荐通过脚本周期性检查 `plan/*.md` 是否满足该约定
  - 如发现偏离，可通过调整 `prompts/plan.md` 或在对话中显式纠正行为
