# Userspace Harness 与 Loop Engineering 讨论归档

> 日期：2026-08-25  
> 状态：已归档  
> 来源：关于 docs-pipeline v5 能否引导 AI 全自主工作的讨论  
> 后续 PRD：[PRD：AI 自主工作 Userspace Harness 与 Loop Engine](../prd/2026-08-25-ai-autonomous-userspace-harness-loop-engine.md)

## 用户问题

> 从你学习到的项目看它能否更好的引导AI全自主工作.满足user space harness, 满足loop engineer

## 回答原文

帅哥，基于现有信息，我理解你的需求是：判断当前 `docs-pipeline v5` 是否足以引导 AI 全自主工作，并满足 **userspace harness** 和 **loop engineering**。

## 【结论】

⚠️ **目前只能打好地基，还不能独立满足完整 Loop Engineer。**

当前方案能解决约 **60% 的基础问题**：

- AI 知道先读什么；
- AI 知道文档写到哪里；
- 需求、设计、计划、现实状态有明确 Owner；
- 安装、升级、检查、回滚不会随意破坏用户文件；
- 验证结果不会把“没检查”伪装成“通过”；
- 不同 AI 宿主可以通过统一入口理解项目。

但它还没有真正控制 AI 的自主执行循环：

```text
理解目标
→ 选择任务
→ 制定计划
→ 执行
→ 验证
→ 发现问题
→ 修复或重试
→ 判断是否完成
→ 沉淀结果
```

`docs-pipeline` 管的是**工作空间和知识治理**，不是完整的**自主执行引擎**。

## 【正确架构】

不要把 mission-driver 全塞进 docs-pipeline。那会把一个清晰工具做成巨型垃圾。

应该拆成两个深模块：

```text
┌─────────────────────────────────────┐
│ Userspace Harness                   │
│ AGENTS 路由、Owner、权限、文档结构  │
│ Manifest、Installer、State、Validator│
└──────────────────┬──────────────────┘
                   │ 提供可信工作空间
┌──────────────────▼──────────────────┐
│ Loop Engine                         │
│ 选任务、执行、验证、重试、暂停、恢复 │
│ 预算、证据、退出条件、人工升级       │
└─────────────────────────────────────┘
```

### 1. docs-pipeline 负责 Userspace Harness

它应提供：

- 根 `AGENTS.md`：只负责路由和硬门禁；
- `docs/context/`：AI 启动上下文；
- `prd/`：目标和验收标准；
- `plans/active/`：当前执行契约；
- `design/reality/`：当前系统事实；
- `State`：安装和文档治理状态；
- `Validator`：确定性检查；
- Profile：不同技术栈和宿主的能力声明；
- 权限边界：AI 可以自动做什么，什么必须询问用户。

这一部分，当前 v5 方向基本正确。

### 2. 独立增加 Loop Engine Capability

需要新增一套最小运行模型：

```text
Goal
  ↓
Work Item
  ↓
Plan
  ↓
Attempt
  ↓
Evidence
  ↓
Verdict
  ↓
Complete / Retry / Blocked / Escalate
```

每次循环至少记录：

```yaml
runId: run-001
goalId: goal-001
workItemId: task-003
status: running
currentStage: verify
attempt: 2
budget:
  maxAttempts: 3
  maxDurationMinutes: 30
evidenceRefs:
  - test-report-001
stopCondition:
  - all_acceptance_criteria_pass
```

## 【还缺少的关键能力】

### 1. 稳定的任务状态机

必须只有这些明确状态：

```text
planned
ready
running
blocked
verifying
completed
failed
cancelled
```

不能让 AI 靠自然语言猜“这个任务大概完成了”。

### 2. 可执行验收标准

每个任务必须关联稳定 AC：

```text
TASK-03
├── AC-01
├── AC-02
└── AC-03
```

只有所有阻断 AC 都有 `pass` 证据，任务才能完成。

`unobserved`、`blocked`、测试没运行，都不能算完成。

### 3. Evidence Packet

AI 不得只说“我检查过了”。

必须保存：

- 执行了什么命令；
- 退出码；
- 测试结果；
- 修改了哪些文件；
- 使用哪个 commit 和工作区；
- 哪个 AC 被什么证据满足；
- 哪些事情没有观察到。

### 4. 预算和防死循环

每个 Loop 必须有限额：

- 最大尝试次数；
- 最大运行时间；
- 最大 token 或成本；
- 同一错误重复次数；
- 无进展次数；
- 允许修改的目录；
- 允许执行的工具和命令。

超过限制就进入 `blocked` 或 `escalate`，不能无限自我修复。

### 5. 明确的停止条件

AI 只能因为以下原因停止：

```text
completed：所有阻断 AC 通过
blocked：缺少权限、凭证、输入或外部依赖
failed：已取得证据，证明无法满足要求
budget-exhausted：达到明确预算
cancelled：用户明确取消
```

不能因为“代码看起来不错”或“暂时没发现错误”就停止。

### 6. 崩溃恢复

恢复时必须检查：

- 工作区是否还是同一个；
- Manifest 是否变化；
- Plan 是否变化；
- 已完成步骤的输入和输出 Hash 是否匹配；
- 是否存在未完成的外部副作用。

不能只看“文件已经存在”就跳过任务。

### 7. 自主权策略

建议在 `docs/context/autonomy.md` 中定义三层权限：

| 等级 | AI 可以做什么 |
|---|---|
| `safe` | 读取、分析、运行只读检查 |
| `workspace-write` | 修改项目文件、运行测试、创建本地状态 |
| `external-effect` | 提交、推送、部署、发消息、修改远程系统 |

前两层可按授权自主执行。第三层必须显式授权，避免“全自主”变成“随便破坏外部世界”。

## 【最终判断】

### Userspace Harness

✅ **当前 v5 经过小幅补充后可以满足。**

还需补充：

- 宿主能力矩阵；
- 权限和自主等级；
- Work Item、Evidence、Verdict 的统一契约；
- 根 `AGENTS.md` 的 Loop 路由入口。

### Loop Engineer

⚠️ **当前 v5 不能单独满足。**

它缺少：

- Loop 状态机；
- 任务调度；
- 尝试和预算；
- Evidence Packet；
- Completion Gate；
- Stop Condition；
- 崩溃后执行恢复；
- 阻断时的人类升级机制。

## 【建议】

最好的方案不是继续膨胀 `docs-pipeline`，而是：

```text
docs-pipeline v5
    = Userspace Harness 基础设施

loop-engine capability
    = AI 自主执行协议

mission-driver / 其他运行器
    = Loop Engine 的可替换 Adapter
```

一句话概括：

> `docs-pipeline` 负责让 AI **知道真相、边界和验收标准**；`loop-engine` 负责让 AI **持续工作，直到有证据证明完成或明确阻塞**。

这样才能同时满足 **Never break userspace** 和真正的 **Loop Engineering**。
