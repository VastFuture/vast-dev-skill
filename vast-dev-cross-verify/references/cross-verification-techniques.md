# Cross-Verification Techniques

## Phase 4 验证技术概览

这份文档描述了代码评审工作流的第四阶段——交叉验证，包含 **4+1 种技术**：

## 核心四种验证

| 技术 | 目的 | 价值 |
|------|------|------|
| **4.1 Systematic Debugging** | 内部自查，用"假如出 bug"视角扫描代码 | 成本最低，1 轮思考 |
| **4.2 Cold-Context Review** ⭐ | 独立评审，不提供设计文档，只看 diff | **最高 ROI，发现设计盲点** |
| **4.3 Behavior-Preservation Diff** | 对比 master vs feature，确认重构未改变业务逻辑 | 防止回归 |
| **4.4 Cross-Repo Impact Scan** | 识别对其他仓库的影响 | 微服务必做 |
| **4.5 Business Invariant Check** | 验证资金/状态机/库存等硬约束 | 命中相关场景必做 |

## 执行顺序

1. **4.1 先做** — 便宜，帮自己清醒
2. **4.2 紧跟** — 最高价值，找设计盲点
3. **4.3 + 4.4 + 4.5 并行 dispatch** — 节省时间

## 关键原则

> "设计文档代表作者相信系统应该如何工作。熟悉设计的 reviewer 会默认作者的假设是对的，从而看不到这个假设本身就是错的。"

Cold-context reviewer 只看代码实际做什么，反而能发现**设计层面的漏洞**。

## 产出汇总

所有验证结束后，将发现的 issue 汇总成表格（来源/严重度/位置/问题/修复方向），交给 Phase 5 规划修复。