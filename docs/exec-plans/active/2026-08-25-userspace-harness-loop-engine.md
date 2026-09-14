# Userspace Harness 与 Loop Engine 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在不膨胀 docs-pipeline Core 的前提下，建立可验证、可限额、可恢复的 AI 自主工作协议和可替换运行器接口。

**Architecture:** `docs-pipeline` 提供 Userspace Harness，新的 `loop-engine` Capability 提供状态机、预算、Evidence Packet 和 Completion Gate。具体运行器通过 Adapter 接口接入；所有终态由确定性规则裁决，不由模型自由宣告。

**Tech Stack:** Python 3 标准库、JSON Schema、pytest、Markdown 模板、Git。

---

## Owner Chain

| 类型 | Owner 文档 |
|------|------------|
| 原始讨论 | [`docs/discussions/2026-08-25-userspace-harness-loop-engineering.md`](../../discussions/2026-08-25-userspace-harness-loop-engineering.md) |
| 产品需求 | [`docs/prd/2026-08-25-ai-autonomous-userspace-harness-loop-engine.md`](../../prd/2026-08-25-ai-autonomous-userspace-harness-loop-engine.md) |
| 治理依赖 | [`docs/prd/2026-08-25-docs-pipeline-v5-governance-optimization.md`](../../prd/2026-08-25-docs-pipeline-v5-governance-optimization.md) |
| 执行日志 | [`docs/logs/2026/08-25.md`](../../logs/2026/08-25.md) |

责任分配：docs-pipeline 维护者负责 Harness 模板、路由和安装；loop-engine 维护者负责机器契约、内核和公共 Adapter 契约；每个具体 Adapter 由对应宿主集成维护者负责。

## Current Baseline

- docs-pipeline v5 PRD 已定义 Manifest、Installer、State、Validator 和 CI，但尚未实现。
- 当前仓库仍使用 `docs/exec-plans/`；迁移器完成前不手工改为 `docs/plans/`。
- 当前没有 `loop-engine` 代码、Schema 或契约测试。
- 本计划只定义实现顺序，不表示任何 Loop Engine 功能已经交付。

## File Structure

| Path | Responsibility |
|------|----------------|
| `loop-engine/schemas/work-item.schema.json` | Work Item 和权限、预算、AC 引用契约 |
| `loop-engine/schemas/attempt.schema.json` | Attempt 生命周期和执行结果契约 |
| `loop-engine/schemas/evidence-packet.schema.json` | 命令、verdict、artifact 和 AC 证据绑定 |
| `loop-engine/src/loop_engine.py` | 状态转换、预算、Completion Gate 和恢复内核 |
| `loop-engine/src/adapters.py` | Adapter 接口与 registry；不包含运行器业务规则 |
| `loop-engine/tests/test_contracts.py` | Schema 和非法输入测试 |
| `loop-engine/tests/test_state.py` | 状态机、预算和停止条件测试 |
| `loop-engine/tests/test_completion.py` | Completion Gate 与 Evidence Packet 测试 |
| `loop-engine/tests/test_traceability.py` | Work Item、Attempt、Evidence 和 verdict 双向追踪测试 |
| `loop-engine/tests/test_recovery.py` | 输入漂移、pending side effect 和恢复测试 |
| `docs-pipeline/assets/templates/context/autonomy.md` | 三层自主权策略模板 |
| `docs-pipeline/assets/templates/loop/` | Work Item 和 Evidence 示例模板 |
| `docs-pipeline/manifest.yaml` | 只声明 Loop Capability 的 Harness 模板、路由和检查，不包含 Loop Engine 内核 |

## Phase 1：冻结协议

### Task 1：定义 Schema 和非法状态测试

- [ ] 创建三个版本化 JSON Schema，固定 ID、必填字段、枚举和禁止的未知字段。
- [ ] 添加 fixture：合法 Work Item、缺少 AC、缺少权限字段、缺少预算、越权路径、合法 Evidence Packet、无 evidence ref 的假通过。
- [ ] 验证缺少权限字段的 Work Item 无法从 `planned` 进入 `ready`，并返回稳定原因码。
- [ ] 运行 `python -m pytest loop-engine/tests/test_contracts.py -q`，预期所有合法 fixture 通过、非法 fixture 被拒绝。
- [ ] 审查 Schema 是否覆盖 PRD AC-01、AC-05、AC-06 和 AC-10。

### Task 2：冻结状态转换表

- [ ] 在 `loop_engine.py` 中只定义 PRD 允许的状态和转换，不加入运行器逻辑。
- [ ] 测试 `ready → completed`、`planned → running`、`blocked → completed` 等非法跳转必须失败。
- [ ] 测试 `verifying → completed` 只有通过 Completion Gate 才允许。
- [ ] 运行 `python -m pytest loop-engine/tests/test_state.py -q`。

**Phase 1 Exit Criteria**

- [ ] Schema 和转换表有稳定版本。
- [ ] 未定义字段和非法状态转换 fail fast。
- [ ] 没有 Adapter 或 docs-pipeline 私有逻辑进入协议层。

## Phase 2：确定性 Loop 内核

### Task 3：实现预算和无进展检测

- [ ] 实现 attempt、duration、failure fingerprint 和 no-progress 四类预算。
- [ ] 使用固定时钟和内存 State fixture 测试每种预算边界。
- [ ] 验证预算耗尽得到 `blocked` 和 `budget-exhausted`，不得得到 `completed` 或 `failed`。
- [ ] 运行 `python -m pytest loop-engine/tests/test_state.py -q`。

### Task 4：实现 Evidence Packet 与 Completion Gate

- [ ] 将 blocking AC 与 evidence ref 做一一绑定。
- [ ] 拒绝 `unobserved`、`blocked`、零测试、全部 skipped 和未知 evidence ref。
- [ ] 在 workspace、Manifest 或 Plan digest 变化时拒绝完成。
- [ ] 分别执行 `completed`、`blocked`、`failed`、`cancelled` 四条终态路径，验证每条路径都生成 Evidence Packet、稳定原因码和恢复条件。
- [ ] 验证任一终态缺少上述字段时状态提交失败，并从 AC-06 可反查到四条终态测试证据。
- [ ] 运行 `python -m pytest loop-engine/tests/test_completion.py -q`。

### Task 5：实现稳定 ID 双向追踪

- [ ] 建立按 `workItemId`、`attemptId`、`evidenceId` 和 `verdictId` 查询的统一追踪索引。
- [ ] 从任一实体 ID 出发，返回同一链路中的 Goal、Work Item、全部 Attempt、Evidence 和最终 verdict。
- [ ] 引用不存在、链路跨 Work Item 或出现重复 ID 时 fail fast。
- [ ] 运行 `python -m pytest loop-engine/tests/test_traceability.py -q`，验证四种入口得到相同链路。

### Task 6：实现权限检查

- [ ] 在任何动作执行前按 `safe`、`workspace-write`、`external-effect` 校验。
- [ ] 验证越过 `allowedPaths` 和未授权 external-effect 均在 Adapter 调用前失败。
- [ ] 验证权限失败写入稳定原因码和恢复条件。

**Phase 2 Exit Criteria**

- [ ] PRD AC-01 至 AC-06 均有确定性测试。
- [ ] 模型输出不能绕过状态机、预算、权限或 Completion Gate。

## Phase 3：Adapter 和恢复

### Task 7：建立 Adapter 接口

- [ ] 在技术设计中比较函数调用、CLI/JSON 和事件协议三种 seam，选择最小稳定接口。
- [ ] 所选 Adapter 契约覆盖能力发现、执行生命周期、取消、证据采集和中断对账。
- [ ] 建立 fake Adapter 和 subprocess Adapter 两个 fixture。
- [ ] 对同一 Work Item 运行共享契约测试，确认两者产生相同核心状态和 Evidence 结构。

### Task 8：实现恢复门禁

- [ ] 恢复前比较 workspace、Manifest、Plan、输入和已完成输出 digest。
- [ ] 有 pending side effect 时验证 idempotency key 和 receipt。
- [ ] 无法证明幂等、授权过期或用户文件发生并发修改时进入 `blocked`。
- [ ] 运行 `python -m pytest loop-engine/tests/test_recovery.py -q`。

**Phase 3 Exit Criteria**

- [ ] 两个 Adapter 通过共享契约测试。
- [ ] PRD AC-07、AC-08 有自动化证据。
- [ ] 恢复不会重复不可证明幂等的副作用。

## Phase 4：Userspace Harness 接入

### Task 9：安装模板和路由

- [ ] 新增 `autonomy.md`、Work Item 和 Evidence 模板。
- [ ] 在 Manifest 中把 Loop Engine 声明为默认关闭的 Capability。
- [ ] 根 AGENTS 模板只增加 Loop 入口、Owner 路由、Completion Gate 和权限升级入口。
- [ ] Validator 检查所有 Loop 文档引用和 Schema。

### Task 10：端到端 Dogfood

- [ ] 在临时消费者 fixture 中安装 Loop Capability。
- [ ] 用一个只修改临时 Markdown 的任务跑通 `ready → running → verifying → completed`。
- [ ] 注入测试失败，验证 Loop 重试后达到预算并进入 `blocked`。
- [ ] 注入未授权 external-effect，验证动作未执行。
- [ ] 由独立 Reviewer 仅使用 Evidence Packet 复核 Completion Gate。

**Phase 4 Exit Criteria**

- [ ] PRD AC-09 至 AC-11 通过。
- [ ] 当前仓库 Dogfood 和消费者 fixture 均通过。
- [ ] docs-pipeline Core 不依赖任何具体运行器。
- [ ] docs-pipeline Core 不包含 Loop Engine 状态机、预算、Completion Gate 或恢复实现。

## Final Verification

- [ ] 运行 `python -m pytest loop-engine/tests docs-pipeline/tests -q`，预期全部通过且至少执行一个测试。
- [ ] 运行 docs-pipeline Validator，预期所有 blocking 检查为 `pass`。
- [ ] 运行 `git diff --check`，预期无输出。
- [ ] 检查测试临时目录和进程均已清理。
- [ ] 独立 Reviewer 按 PRD AC-01 至 AC-11 逐项签署 verdict 和 evidence ref。

## Completion Gates

- [ ] 所有 PRD P0 验收标准通过。
- [ ] 两个 Adapter fixture 通过共享契约测试。
- [ ] 未授权 external-effect 从未执行。
- [ ] 中断恢复不重复非幂等副作用。
- [ ] Discussion、PRD、Plan、Log 和代码证据可以双向追踪。
