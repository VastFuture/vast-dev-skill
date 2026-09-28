---
description: Campaign 模式的展开手册。一次 PR 清扫某个子系统（一个插件或一个核心区域）的整套测试面。SKILL.md 里的 value bar、retention bar、candidate evidence、validation 同样适用；本文件只补步骤顺序与全程教训。
---

# Test-pruning campaign

Campaign 模式：一次 PR 清扫某个子系统（一个插件如 `extensions/<plugin>`，或一个核心区域）的整套测试面。[SKILL.md](SKILL.md) 里的 value bar、retention bar、candidate evidence、validation 全程适用。本文件只补步骤顺序和从完整 campaign 中总结的教训。每一步以其完成标准结束，未达标不开始下一步。

---

## 1. Baseline

在固定的 `main` SHA 上，记录该子系统的测试与支撑行数，以及每个测试文件的 pass/fail 状态。Baseline 失败单列：通常是真实产品 bug，不是陈旧测试。

Done 当：范围内每个测试文件都有记录在案的 baseline 结果。

---

## 2. Lanes and inventory

按产线 **owner boundary** 而非文件前缀划分 lane。典型：accounts、commands、context、dispatch、inbound、outbound、persistence、transport、shared、harness、live/QA scenarios。包含该子系统在共享核心边界的 case、QA 场景、live-proof harness 测试。

Done 当：子系统拥有的每个测试文件和 QA scenario 恰好属于一条 lane。

---

## 3. Read-only ledger per lane

每条 lane 派一个只读 agent。Agent 完整读每个分配到的测试，包括参数表。它也读产线 owner、入口、调用方、历史、CI 路由。每个测试声明写入一份 **ledger**，打一个标。`it.each` 算一条声明，除非它的各行需要不同标，那各行分别标。

- `R`：保留，写明契约与捕获的 bug；只移到更名文件的保留测试仍是 `R`，注明移动
- `F`：保留契约但修复断言（如只缺一项时仍然通过的 vacuous 负断言）
- `C`：合并，写明首先吸收断言的 owner：兄弟表驱动用例、更强边界 suite、或另一 package 的共享 owner
- `D`：删除，写明保留的证明，或为何不存在契约

判定看断言而非名字。一个名为“retiring a progress window”的测试，实际断言窗口**未被**清空——名字误人。

Done 当：lane 内每条声明都有标和证据行。

---

## 4. Layer plan per lane

把 per-test ledger 当输入而非编辑清单。第二轮只读以 ledger 为起点，寻找冗余 **layer**。多个 dispatch suite 在一个 mock preview 下复放同一共享 compositor，外面已有更强的真实流和 HTTP fixture suite。给每个契约点名 **keeper** suite。优先用真实 transport 边界 + 假网络，而非 mock 协作者。修正本轮发现的 ledger 错误。

Done 当：每条 lane 计划都点名了退役文件、每个契约的 keeper、要搬入 keeper 的断言、以及解锁的测试专用产线缝。

---

## 5. Cutover

按 lane 编辑。共享 harness 与支撑文件的改动走单一 owner 串行化。每个 lane 解锁的测试专用产线缝同步删掉：注入参数、getter、reset export、间接层。迁移的 suite 在 CI 路由和测试 inventory 注册。更新 shrink-only line-cap baseline。把本次 campaign 实际发现的测试所有权规则写到子系统的 `AGENTS.md`。

Done 当：每条 lane 计划已应用，每个 lane 的 keeper 通过。

---

## 6. Preservation review

声称完成前，请独立评审员按边界分组对比已删覆盖与 keeper，每组一个评审员。找那些“失去唯一证明”的契约。也找新加的不可失败断言（如生产代码根本不触达的拒绝行）。一次 Telegram 评审找到九个真实缺口和一个不可达断言。

每个恢复的契约，对产线 owner 做一次刻意 **mutation**，确认 keeper 变红。然后逐字节还原源码。

Done 当：每个被报告的缺口已恢复或带源码证据驳回，每个恢复的契约都有被捕获的 mutation。

---

## 7. Product defects

能存活进 keeper 的 baseline 失败是 bug 报告。把它在 owner 处单独 commit 修复，走真实用户流证明，并跑一次**对照**：还原 fix、重现旧行为。把过程中发现的不相关产品差异写成 follow-up，不在 campaign 里修。

Done 当：每个修复的缺陷都有对照失败和同一 harness 上的候选通过。

---

## 8. Reconcile and hand off

Campaign 跨多个 `main` commit。`git merge main`，不要 rebase 一个长、多 commit 的 campaign。若 `main` 改动了 campaign 已删的文件，保留删除；把新契约搬进 keeper，确认 `main` 新增的回归仍有归属。重新跑整套子系统 suite，并在合并 head 上重跑 live proof。

预期评审工具在这么大的 diff 上看到截断的文件列表。通用兼容性 flag 的维护者决策写到 PR evidence，不去改 gate。

按 [SKILL.md](SKILL.md) 的报告结构交付，并补：

- baseline 与最终测试/支撑行数，产线单列
- lane、退役 layer 与 keeper
- 找到的 preservation 缺口与对应 mutation
- 产品缺陷及对照/候选证明