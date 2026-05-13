---
name: vast-dev-cross-verify
description: 7阶段高风险功能开发工作流，包含4轮独立交叉验证，在投入生产前捕获并发、幂等性和跨服务 bug。用于金融交易、订单/库存状态机、分布式锁、跨服务接口变更、在线 schema 迁移等高风险场景。触发词：'cross-verified'、'交叉验证'、'高风险功能开发'、'vast-dev-cross-verify'。
---

# Cross-Verified Feature Development Skill

> 7阶段高风险功能开发工作流，包含4轮独立交叉验证，在投入生产前捕获并发、幂等性和跨服务 bug。

## 何时使用

触发此工作流开发时使用：
- 金融交易（支付、退款、结算）
- 订单/库存状态机
- 分布式锁、并发控制、幂等重试逻辑
- 跨服务接口或共享 proto 变更
- 在线 schema 迁移或双写策略
- 估计开发时间 ≥3 人天且失败成本高

## 7个阶段

### Phase 1: 需求与设计 → `brainstorming`
结构化需求文档，包含：
- 问题陈述
- 技术决策
- 不变量（invariants）
- 失败模式（failure modes）

### Phase 2: 架构评审 → ADRs（可选，高风险时必须）
关键决策的架构决策记录

### Phase 3: 实现计划 → 任务分解
每个任务包含：
- 文件/行号
- 验证命令
- 部署策略

### Phase 4: 🔥 交叉验证（核心创新）

#### 4.1 系统性自检（Self-Review）
用"假如出 bug"视角扫描代码，最便宜，1轮思考

#### 4.2 冷上下文评审（Cold-Context Review）⭐
评审者**看不到设计文档**，只看 diff —— 最高价值，发现设计盲点

> "设计文档代表作者相信系统应该如何工作。熟悉设计的 reviewer 会默认作者的假设是对的，从而看不到这个假设本身就是错的。"

#### 4.3 行为保留 Diff（Behavior-Preservation Diff）
对比 master vs feature，确认重构未改变业务逻辑

#### 4.4 跨仓库影响扫描（Cross-Repo Impact Scan）
微服务必做，识别对其他仓库的影响

#### 4.5 业务不变量验证（Business Invariant Check）
验证资金/状态机/库存等硬约束，命中相关场景必做

**执行顺序**：
1. 4.1 先做 —— 便宜，帮自己清醒
2. 4.2 紧跟 —— 最高价值，找设计盲点
3. 4.3 + 4.4 + 4.5 并行 dispatch —— 节省时间

**产出**：汇总成表格（来源/严重度/位置/问题/修复方向），交给 Phase 5

### Phase 5: 修复迭代
按严重度修复，独立提交，修复后重新测试

### Phase 6: 谨慎简化
验证假设后再移除"冗余"代码：
1. 记录为什么它存在 —— 检查 git blame、commit messages、issues
2. 验证每个原因已过时 —— 找到证据证明问题不再发生
3. 检查所有路径 —— retry、并发、失败路径保持正确
4. 运行冷上下文评审 —— 新视角捕获熟悉度遗漏的问题

> **关键规则**："代码现在正确" ≠ "某部分是冗余的"。这是两个根本不同的命题。

### Phase 7: 文档同步
将设计文档与实际代码同步，确保"设计文档 = 代码真相"

需要执行的情况（任一）：
- 修复了 Critical/High 问题（改变了核心流程）
- 实现过程中有 3+ 个设计偏差
- 回滚了失败的简化尝试
- 部分现在明显与代码不一致

## 核心洞察

> "单一视角的 review 有系统性盲点" — single-perspective review has systematic blind spots.

独立评审者发现的 bug 集合接近**并集，而非交集**。冷上下文评审者（不看设计文档）能捕获开发者对自己代码忽略的设计级缺陷。

## 成本效益

- **成本**：~40-50% 额外时间
- **Critical bug 检测率**：从 ~40% 提升到 ~95%

---

## 触发词

`/cross-verified`、`交叉验证`、`高风险功能开发`

## 参考资料

- `references/cross-verification-techniques.md` — 4+1 种验证技术详解
- `references/anti-patterns.md` — 12 种常见失败模式
- `references/case-studies.md` — 6 个真实 bug 案例
- `references/doc-sync-playbook.md` — Phase 7 文档同步 playbook