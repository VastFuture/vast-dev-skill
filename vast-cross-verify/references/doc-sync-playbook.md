# Doc Sync Playbook

## Phase 7: 文档同步手册

**目的**: 在 Phase 4-6 修复后将设计文档与实际代码同步，确保"设计文档 = 代码真相"。

## 何时执行

满足任一条件时必须执行：
- 修复了 Critical/High 问题（改变了核心流程）
- 实现过程中有 3+ 个设计偏差
- 回滚了失败的简化尝试
- 部分现在明显与代码不一致

## 核心原则

1. **保留原始意图** — 不要重写；添加行内注释如 `> ⚠️ Original design vs actual: ...` 并追加 Evolution Log
2. **记录推理，不只是结果** — 包含为什么做此决定
3. **记录失败** — 失败的尝试是最有价值的知识；记录根本原因和教训
4. **在末尾追加 Evolution Log** — 这是核心交付物

## 两种文档类型

**Spec 文档** 获取 Evolution Log 附录 (§N)，跟踪：
- 初始实现阶段
- 评审修复（含 commit SHAs）
- 失败尝试和回滚
- 当前偏差索引
- 新增的防御机制

**Plan 文档** 获取两个附加项：
- 顶部状态表（task → commit → status）
- 末尾 Part G（实现后修复，含 commit 引用）

## 反模式

- ❌ 大爆炸式重写 spec（保留原文档 + 注解）
- ❌ 提交代码前更新文档
- ❌ 删除失败尝试记录
- ❌ 过于详细的行级引用

## 输出结构

```
docs/superpowers/
├── specs/YYYY-MM-DD-<feature>-design.md   # With §N Evolution Log
├── plans/
│   ├── YYYY-MM-DD-<feature>.md            # With status table + Part G
│   └── YYYY-MM-DD-<feature>-review-fixes.md
└── tests/YYYY-MM-DD-<feature>-verification-runbook.md  # if applicable
```

## 关键验收问题

- 明天别人能从文档理解当前代码的推理吗？
- 所有 Critical/High 修复都记录了吗？
- 失败尝试包含根本原因和教训吗？
- 跨团队开放问题被主动沟通了吗（不只是写了）？
- Ops SOP 变更在 runbook 中更新了吗？