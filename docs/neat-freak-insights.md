# neat-freak 启发录

> 来源: https://github.com/VastFuture/khazix-skills/tree/main/neat-freak
> 日期: 2026-06-03
> 背景: docs-pipeline 升级过程中，分析 neat-freak 的"知识库洁癖"理念

## neat-freak 是什么

一个会话结束后的知识库清理工具，用"洁癖级"审查确保文档、记忆、代码三者同步。核心价值：**让知识体系的每一层都跟得上代码的变化**。

---

## 5个核心洞察

### 1. 三层知识体系 + 三种受众

**关键理念**：知识分层，受众不同，职责不重叠

| 位置 | 受众 | 职责 | 不同步的代价 |
|------|------|------|-------------|
| **Agent 记忆** | Agent 自己 | 个人偏好、项目事实 | 下次会话忘记历史决策 |
| **CLAUDE.md/AGENTS.md** | 当前项目 AI | 项目约定、红线、路由 | 下次 AI 走弯路 |
| **docs/ + README** | 其他人（人类/下游/未来 AI） | 接入指南、架构、运维 | **其他人无法正确接入** |

**关键判断**：
- "我记得上次做了什么" ≠ "AI 下次编码需要看到什么规则" ≠ "其他人如何接入"
- CLAUDE.md 里写"新增了 device flow 五个路由" ≠ docs/integration-guide.md 里"下游怎么接这套 flow"
- 前者是提醒自己，后者是教别人。**两份都要写**

### 2. CLAUDE.md 是规则手册，不是变更日志

**最常见翻车模式**：每次开发完在 CLAUDE.md 顶部加 blockquote 历史叙事
- 一次很爽 → 半年后 200 行 blockquote 把真正规则挤出去
- **这种叙事不属于 CLAUDE.md**，归 git log / CHANGELOG / docs/CHANGES.md

**判断标准**：下次 AI 写代码时如果没看到这条，会不会犯错？

| 例子 | 进 CLAUDE.md？ | 理由 |
|-----|---------------|------|
| "Prisma 查询只写在 `modules/**/data/`" | ✅ | 违反就是边界破坏 |
| "rsync 单文件部署必须用完整 target 路径" | ✅ | 踩坑警示 |
| "禁止裸跑 systemctl stop aihot-worker" | ✅ | 红线，事故级 |
| "2026-05-08 timelineAt 上线，详见 docs/ARCHITECTURE.md §5.4" | ❌ | 详细机制在 docs；指针表已做这件事 |
| "5/8 修了 X bug 的复盘细节" | ❌ | 单次事故记忆，归 memory 或删 |

**✅ 该进的**：硬边界规则、禁止事项、命令速查、权限模型、踩坑警示  
**❌ 不该进的**：历史叙事、详细机制、单次事故复盘、bug fix 流水账

### 3. 尺寸体检（防膨胀）是最高优先级

**核心原则**：超尺寸 > 补漏

**原因**：超尺寸的 CLAUDE.md 让 AI 看不到真正重要的规则（被叙事段挤到 200 行外，进不了 prompt 重点段）

| 文件 | Soft limit | 红灯线 |
|------|-----------|--------|
| CLAUDE.md/AGENTS.md | ~300 行 / ~15KB | 净涨幅 > 30 行 |
| 记忆索引（如 MEMORY.md） | ~150 行 | - |
| 单条 memory | ~100 行 | - |
| docs/<single>.md | ~1500 行 | 需切分 |

**执行顺序**：先精简（破除膨胀）→ 再做本次会话增量同步（补漏）

**净涨幅红灯**：每次更新 CLAUDE.md，净涨幅 > 30 行就是红灯
- 新增的是"AI 必须看到的规则"？→ ✅
- 新增的是"便条"（历史叙事）？→ ❌

### 4. 变更影响矩阵

**系统化映射**：这次改动 → 要同步哪些文件

| 本次对话发生的事 | 要改的文件 |
|----------------|-----------|
| 新增 API/路由 | CLAUDE.md 路由清单 + docs/integration-guide + docs/architecture Routes |
| 新增/改名环境变量 | CLAUDE.md 环境变量表 + docs/runbook + docs/integration-guide |
| 新增数据库表 | CLAUDE.md 数据库表 + docs/architecture Data Model |
| 新增大特性 | 以上全部 + docs/architecture 新章节 + docs/handoff 已完成清单 |

**标准动作（四处都补）**：
1. **integration-guide**：怎么用（curl / SDK 示例 / 错误码）
2. **architecture**：怎么工作（数据流、状态机、设计取舍）
3. **runbook**：怎么运维（冒烟命令、故障排查、环境变量）
4. **handoff / CHANGELOG**：已完成

### 5. 执行纪律

**第一步：盘点现状（强制机械式枚举）**
- **先做 ls，再做判断**
- 列出 agent 记忆文件、项目根目录、docs/、所有 .md
- 输出文件清单：「评估过 / 要改 / 不用改」
- **漏一个不行**

**第二步：识别变更（用变更影响矩阵思考）**
- 不要只看对话增量有什么新事实
- 要看新事实会波及哪些文档层级
- **关键检查**：这次对话是不是跨项目的？下游项目 docs 也要改

**第三步：实际修改（用工具，不只是描述）**
- 真的用 Edit 修改、用 Write 创建、用删除命令清理
- **顺序**：先改 docs/（影响外部）→ 再改 CLAUDE.md → 最后理记忆

**编辑原则**：
- **减优于加**（最重要）：能删的先删
- **合并优于追加**：新信息更新旧条目
- **删除优于保留**：完成的临时计划 → 删
- **精确优于冗长**：一条记忆说清楚一件事
- **绝对时间**：永远 `2026-04-29`，不写"今天"、"最近"
- **面向读者**：docs/ 的读者是"第一次接触的外部人"
- **受众不混**：CLAUDE.md 不抄 docs/ 全文
- **指针不重复**：同一条事实只在指针表出现一次

**第四步：自检清单（必须逐项过）**

尺寸/反膨胀：
- [ ] CLAUDE.md/AGENTS.md 净涨幅 ≤ 30 行
- [ ] 没新增历史叙事（"X 起 Y 上线，详见 docs/"）
- [ ] 没在 CLAUDE.md 抄 docs/ 详细机制
- [ ] 单条 memory < 100 行

完整性/反漏改：
- [ ] 每个文件都判断了"不用改"或"已改"
- [ ] 新增 API：在 integration-guide 和 architecture 都出现了
- [ ] 新增环境变量：在 runbook 和项目根 markdown 都出现了
- [ ] 新增数据库表：在 architecture 和项目根 markdown 都出现了
- [ ] 跨项目影响：下游项目 docs 也改了
- [ ] 没有相对时间遗留（`grep -E "今天|昨天|最近"` 清零）

---

## 对 docs-pipeline 的5个启发

### 启发 1：缺失"文档所有权边界"

**现状**：有 context/、backlog/、prd/、design/ 等目录，但没说"这个目录是给谁看的"、"职责边界在哪"

**改进方向**：在 `docs/context/source-of-truth-and-precedence.md` 添加：

```markdown
## 文档所有权边界

| 文档 | 受众 | 职责 | 不该出现 |
|------|------|------|---------|
| CLAUDE.md/AGENTS.md | 项目 AI | 硬边界规则、禁止事项 | 历史叙事、"详见 docs/" |
| docs/context/ | AI 上下文 | 项目约定、验证命令 | 详细实现 |
| docs/prd/ | 人类+AI | 需求、验收标准 | 实现细节、运维 |
| docs/design/ | 人类+AI | 架构、数据模型 | 使用示例、运维 |
| docs/handover/ | 人类 | 交接、已知问题 | 实现细节（归 design/） |
```

### 启发 2：缺失"防膨胀机制"

**现状**：有 300 行限制，但没有"净涨幅 > 30 行红灯"机制

**改进方向**：创建 `docs/context/anti-bloat-rules.md`：

```markdown
## 防膨胀规则

### 净涨幅红灯
每次更新 CLAUDE.md/AGENTS.md，净涨幅 > 30 行就是红灯。

**判断**：新增的是"AI 必须看到的规则"还是"便条"？
- ✅ 规则：边界约定、禁止事项
- ❌ 便条：历史叙事、"X 时刻起 Y 上线"

### 编辑原则
- 减优于加：能删的先删
- 合并优于追加：更新旧条目
- 删除优于保留：完成的临时计划 → 删
- 指针不重复：docs/ 已详写，CLAUDE.md 只留指针
```

### 启发 3：缺失"变更影响矩阵"

**现状**：有任务路由表（任务类型 → 必读文档），但没有"变更影响矩阵"（新增 API → 要改哪些文件）

**改进方向**：创建 `docs/sync-matrix.md`（参考 neat-freak 的 references/sync-matrix.md）

### 启发 4：缺失"自检清单"

**现状**：有验证命令前置条件，但没有"改完后逐条检查"的自检清单

**改进方向**：在 `docs/exec-plans/README.md` 补充完成前自检清单

### 启发 5：借鉴"四处都补"原则

**现状**：有使用场景示例，但没有"标准动作"清单

**改进方向**：在使用场景 1（添加新功能）中补充标准四步

---

## 核心价值对比

| 维度 | docs-pipeline（当前） | neat-freak 理念 | 结合方向 |
|------|---------------------|----------------|---------|
| 关注阶段 | 初始化 | 持续维护 | 初始化 + 持续维护 |
| 核心目标 | 快速搭建文档结构 | 保持知识同步 | 搭建 + 同步 |
| 文档分层 | 有目录结构 | 有受众边界 | 补充受众边界 |
| 防膨胀 | 有行数限制 | 有净涨幅红灯 | 补充净涨幅机制 |
| 变更管理 | 有任务路由表 | 有变更影响矩阵 | 补充变更矩阵 |
| 执行纪律 | 有验证前置 | 有自检清单 | 补充自检清单 |

---

## 实施优先级

**P0 - 立即可做（不破坏现有结构）**：
1. 创建 `docs/neat-freak-insights.md`（本文档）
2. 在 `docs/context/source-of-truth-and-precedence.md` 补充文档所有权边界
3. 在使用场景中补充"标准四步"

**P1 - 需要设计（新增文档）**：
1. 创建 `docs/context/anti-bloat-rules.md`（防膨胀规则）
2. 创建 `docs/sync-matrix.md`（变更影响矩阵）
3. 在 `docs/exec-plans/README.md` 补充自检清单

**P2 - 需要实践验证（需实际使用后调整）**：
1. 在实际项目中测试"四处都补"原则
2. 积累变更影响矩阵的实际案例
3. 完善自检清单的具体条目

---

## 关键引用

- neat-freak SKILL.md: `/tmp/khazix-skills/neat-freak/SKILL.md`
- 变更影响矩阵: `/tmp/khazix-skills/neat-freak/references/sync-matrix.md`
- Agent 路径速查: `/tmp/khazix-skills/neat-freak/references/agent-paths.md`

---

## 核心金句

> "在 AI 协作开发中，代码可以随时重写，但**文档和记忆是跨会话、跨 Agent 的唯一桥梁**。"

> "判断一条信息该不该进 CLAUDE.md，问一句：**下次 AI 写代码时如果没看到这条，会不会犯错？**"

> "超尺寸是这个 skill 的最高优先级，大于'补本次会话漏掉的同步'。原因：超尺寸的 CLAUDE.md 实际上让下次 AI 看不到真正重要的规则。"

> "减优于加（最重要）：每次同步动作结束后，CLAUDE.md / AGENTS.md 净涨幅 > 30 行就是红灯。"

> "新增一个能力的标准动作是**四处都补**：integration-guide（怎么用）+ architecture（怎么工作）+ runbook（怎么运维）+ handoff（已完成）。"
