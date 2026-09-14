# PRD：AI 自主工作 Userspace Harness 与 Loop Engine

> 文档编号：PRD-2026-08-25-002  
> 状态：Draft  
> 优先级：P1  
> 产品 Owner：docs-pipeline 维护者与 loop-engine 维护者  
> 依赖：[docs-pipeline v5 文档治理闭环优化](2026-08-25-docs-pipeline-v5-governance-optimization.md)  
> 来源讨论：[Userspace Harness 与 Loop Engineering](../discussions/2026-08-25-userspace-harness-loop-engineering.md)  
> 执行计划：[Userspace Harness 与 Loop Engine 实施计划](../exec-plans/active/2026-08-25-userspace-harness-loop-engine.md)

## 1. 结论

docs-pipeline v5 应承担 AI 自主工作的 Userspace Harness，提供可信上下文、文档 Owner、权限、状态和验证能力；自主循环应作为独立的 `loop-engine` Capability，通过稳定接口使用 Harness，不得把特定运行器塞入 docs-pipeline Core。

核心链路：

```text
Userspace Harness
  → Goal / Work Item / Acceptance Criteria
  → Loop Engine Adapter
  → Attempt
  → Evidence Packet
  → Verdict
  → Complete / Retry / Blocked / Escalate
```

## 2. 用户问题

AI Agent 即使获得完整文档，仍可能出现：

- 不知道下一步应该执行哪个任务；
- 把“命令执行过”当作“结果已通过”；
- 在没有证据时宣布完成；
- 无限制重试同一失败；
- 崩溃后重复外部副作用；
- 越过用户授权执行提交、推送或部署；
- 不同运行器各自定义状态，无法替换或审计。

文档治理只能提供可信工作空间，不能自动形成可信执行循环。

## 3. 目标

1. 让 AI 从稳定入口获得目标、边界、计划和验收标准。
2. 用机器可读状态机管理 Work Item 和 Attempt。
3. 只有阻断验收标准获得 `pass` 证据时才允许完成。
4. 用预算、无进展检测和停止条件防止无限循环。
5. 明确本地写入和外部副作用的授权边界。
6. 允许 mission-driver 或其他运行器作为可替换 Adapter 接入。
7. 让每次完成、阻塞和失败都能被恢复与审计。

## 4. 非目标

- 不在 docs-pipeline Core 中实现通用任务调度器。
- 不绑定 Claude Code、OpenCode、Codex 或 mission-driver。
- 不允许 AI 自动获得提交、推送、部署或远程写入权限。
- 不保证任意非幂等外部操作都能自动恢复。
- 不使用自然语言总结代替测试、命令结果或人工审批证据。
- 不在第一阶段实现分布式 Worker、跨机器 Lease 或无限运行。

## 5. 用户故事

### US-01：自主执行

作为项目维护者，我希望 AI 能从一个已批准目标开始持续执行，直到有证据证明完成或明确说明阻塞原因。

### US-02：可信完成

作为 Reviewer，我希望每个 completed Work Item 都能追到验收标准、命令、退出码和产物证据，而不是只看到 AI 的口头声明。

### US-03：安全授权

作为项目所有者，我希望 AI 能自主修改已授权的工作区，但提交、推送、部署和远程写入仍需明确授权。

### US-04：可替换运行器

作为工具维护者，我希望不同 Loop Engine 通过同一接口读取任务和写入结果，不把运行器私有状态污染项目文档。

### US-05：中断恢复

作为 Agent，我希望恢复时能识别已验证步骤、输入漂移和待处理副作用，避免重复执行危险操作。

## 6. 核心模型

### 6.1 模块边界

| 模块 | 负责 | 不负责 |
|------|------|--------|
| Userspace Harness | 上下文、Owner、权限策略、项目中的 Work Item 实例、验收标准和验证入口 | 定义运行时协议、调度和执行具体循环 |
| Loop Engine | 机器契约、运行状态、Evidence Packet，以及选择下一动作、执行、重试、暂停、恢复和停止 | 重定义项目事实、权限和验收标准 |
| Adapter | 将具体运行器映射到统一接口 | 添加私有业务规则 |

Harness 通过 Loop Engine 的公开机器契约创建和校验 Work Item 实例，但不复制或重新定义该契约。Loop Engine 读取 Harness 提供的项目事实，不拥有这些事实的内容。

责任归属：docs-pipeline 维护者拥有 Harness 模板、项目路由和安装集成；loop-engine 维护者拥有机器契约、状态机、Completion Gate、恢复内核和 Adapter 契约；具体 Adapter 由对应宿主集成维护者拥有。

### 6.2 状态机

Work Item 状态固定为：

```text
planned → ready → running → verifying → completed
                     │           │
                     ├──────────→ blocked
                     ├──────────→ failed
                     └──────────→ cancelled
```

`completed` 的唯一入口是 Completion Gate。`budget-exhausted` 是停止原因，最终状态为 `blocked`，不得伪装成 `failed` 或 `completed`。

### 6.3 自主权等级

| 等级 | 允许行为 | 默认授权 |
|------|----------|----------|
| `safe` | 读取、搜索、静态分析、只读检查 | 是 |
| `workspace-write` | 修改授权目录、运行本地测试、写本地运行状态 | 由项目策略授予 |
| `external-effect` | commit、push、PR、部署、消息和远程系统写入 | 否；逐项显式授权 |

## 7. 功能需求

### FR-01：Work Item 契约

每个 Work Item 至少包含：

```yaml
id: WORK-001
goalId: GOAL-001
status: ready
owner: docs-pipeline-maintainers
planRef: docs/exec-plans/active/example.md
acceptanceCriteria: [AC-001, AC-002]
autonomyLevel: workspace-write
allowedPaths: [docs-pipeline/**, docs/**]
stopConditions:
  maxAttempts: 3
  maxDurationMinutes: 30
```

缺少目标、Owner、验收标准、权限或停止条件时不得进入 `ready`。

### FR-02：Attempt 与预算

每次执行生成独立 Attempt，记录输入摘要、开始和结束时间、使用的 Adapter、动作、结果及消耗。Loop Engine 必须执行：

- 最大尝试次数；
- 最大运行时间；
- 同一失败指纹最大重复次数；
- 最大连续无进展次数；
- 允许路径和工具边界。

达到预算后进入 `blocked`，写明 `budget-exhausted` 和恢复条件。

### FR-03：Evidence Packet

Evidence Packet 至少记录：

- workspace identity 和 Git commit；
- Manifest、Plan 和输入摘要；
- 执行命令及退出码；
- 测试和 Validator verdict；
- 修改文件列表；
- AC 到 evidence ref 的映射；
- `unobserved` 和 `blocked` 项；
- 外部副作用 receipt。

AI 只能引用 Packet 中存在的 evidence ref。

### FR-04：Completion Gate

只有满足以下条件才能进入 `completed`：

1. 所有 blocking AC 都存在；
2. 每个 blocking AC 的 verdict 都是 `pass`；
3. 没有未解决的外部副作用；
4. 工作区、Manifest 和 Plan 摘要仍与验证时一致；
5. 必需的独立 Reviewer 或人工审批已经完成。

`unobserved`、`blocked`、零测试和全部 skipped 都是 non-passing。

### FR-05：停止和升级

合法停止结果只有：

| 结果 | 条件 |
|------|------|
| `completed` | Completion Gate 通过 |
| `blocked` | 缺少输入、权限、依赖，或预算耗尽 |
| `failed` | 已有证据证明要求无法满足 |
| `cancelled` | 用户或上游明确取消 |

每个 non-completed 结果必须给出原因码、最后证据、恢复条件和下一位 Owner。

### FR-06：恢复

恢复前必须重新检查：

- workspace、Manifest、Plan 和输入摘要；
- 已完成阶段的输出摘要；
- pending side effect；
- 授权是否过期；
- 用户是否在中断后修改了目标文件。

不能证明幂等的动作不得自动恢复，只能阻塞并请求人工裁决。

### FR-07：Adapter 接口

Loop Engine 必须通过稳定、版本化的 Adapter 契约接入运行器。契约至少覆盖能力发现、执行生命周期、取消、证据采集和中断对账；具体方法、传输形式和进程边界由技术设计裁决。

每项能力声明 `available`、`partial` 或 `unavailable`。Loop Engine 内核不得导入 Adapter 私有实现，docs-pipeline 也不得拥有 Loop Engine 内核或运行器实现。

### FR-08：Harness 路由

根 `AGENTS.md` 只增加：

- 何时进入 Loop；
- Work Item 和 Plan 的 Owner；
- Completion Gate；
- 权限升级入口；
- blocked 时写到哪里。

状态、证据 Schema 和运行器细节不得复制进根入口。

## 8. 非功能需求

| 类别 | 要求 |
|------|------|
| 安全 | 默认不允许 external-effect；越权动作在执行前阻断 |
| 可审计 | 所有终态能追到 Work Item、Attempt、Evidence 和 verdict |
| 可恢复 | 输入未漂移且动作幂等时可恢复；否则明确阻塞 |
| 可替换 | 至少两个独立 Adapter 实现满足同一公开契约 |
| 可解释 | 所有停止、重试和升级都有稳定原因码 |
| 防循环 | 每个运行必须有时间、尝试和无进展预算 |
| 隐私 | State 只保存证据引用，不复制密钥和完整私密 transcript |

## 9. 验收标准

### P0

- [ ] AC-01：缺少 blocking AC、权限或停止条件的 Work Item 不能进入 `ready`。
- [ ] AC-02：只有所有 blocking AC 为 `pass` 时才能进入 `completed`。
- [ ] AC-03：`unobserved`、`blocked`、零测试和全部 skipped 均不能通过 Completion Gate。
- [ ] AC-04：达到尝试、时间或无进展预算后停止循环并进入 `blocked`。
- [ ] AC-05：未授权的 external-effect 在执行前被阻断。
- [ ] AC-06：每个终态都有可解析 Evidence Packet、原因码和恢复条件。
- [ ] AC-07：恢复时输入摘要不匹配会停止，不重复执行非幂等副作用。

### P1

- [ ] AC-08：两个独立 Adapter 实现满足同一公开契约。
- [ ] AC-09：根 AGENTS 只路由，不复制状态机和证据 Schema。
- [ ] AC-10：Work Item、Attempt、Evidence 和 verdict 可以通过稳定 ID 双向追踪。
- [ ] AC-11：独立 Reviewer 可以仅使用 Evidence Packet 判断 Completion Gate 是否成立。

## 10. 发布阶段

1. **Phase 1：协议**：冻结 Work Item、Attempt、Evidence 和 verdict 的版本化机器契约。
2. **Phase 2：确定性内核**：实现状态机、预算、Completion Gate 和授权检查。
3. **Phase 3：Adapter**：用两个独立 Adapter 实现验证同一契约，其中至少一个覆盖真实本地执行边界。
4. **Phase 4：Harness 接入**：安装路由、模板和 Validator。
5. **Phase 5：Dogfood**：用 docs-pipeline 自身任务跑完整 Loop，独立复核证据。

## 11. 风险

| 风险 | 缓解 |
|------|------|
| 把 docs-pipeline 做成调度器 | Loop Engine 保持独立 Capability，只通过接口接入 |
| AI 自己判自己通过 | Completion Gate 确定性执行；高风险任务要求独立 Reviewer |
| 状态模型过重 | 第一阶段只保留一个 Work Item、顺序 Attempt 和本地 State |
| 无限重试 | 时间、次数、失败指纹和无进展四类预算强制存在 |
| 外部副作用重复 | 默认禁用；执行前去重并保存可审计凭据；无法证明安全时阻塞 |

## 12. 决策

**值得做。** 但必须保持模块边界：Userspace Harness 负责可信上下文和治理，Loop Engine 负责执行循环，具体运行器只是 Adapter。
