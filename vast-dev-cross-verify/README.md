# vast-dev-cross-verify

> 源自 [MageByte-Zero/magebyte-power](https://github.com/MageByte-Zero/magebyte-power)，经重构适配本仓库。

**源仓库**：[MageByte-Zero/magebyte-power](https://github.com/MageByte-Zero/magebyte-power)

**原始技能**：`cross-verified-feature-development` — 一个 7 阶段高风险功能开发工作流，包含 4 轮独立交叉验证。

**适用场景**：
- 💰 金融交易（支付、退款、结算）
- 🔄 订单/库存状态机
- 🔒 分布式锁、并发控制、幂等重试逻辑
- 🔗 跨服务接口或共享 proto 变更
- 🗄️ Schema 迁移或双写策略
- ⏱️ ≥3 人天且失败成本高的功能

**核心价值**：Critical bug 检测率从 ~40% 提升到 ~95%（+40-50% 时间成本）

## 触发词

`/vast-dev-cross-verify`、`交叉验证`、`高风险功能开发`

## 目录结构

```
vast-dev-cross-verify/
├── SKILL.md                    # 主入口
├── README.md                   # 本文件
└── references/                 # 参考资料
    ├── cross-verification-techniques.md
    ├── anti-patterns.md
    ├── case-studies.md
    └── doc-sync-playbook.md
```

## 原始文档归档

原始仓库的说明文档归档于 `docs/` 目录：
- `docs/CLAUDE.md` — 源仓库的 CLAUDE.md
- `docs/README.md` — 源仓库的 README（英文）
- `docs/README.zh-CN.md` — 源仓库的 README（中文）
- `docs/articles/cross-verified-skill-intro.md` — 介绍文章（含图片）
- `docs/images/` — 原仓库的图片资源（excalidraw、png、html）