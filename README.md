# Claude Code Skills


> https://github.com/0x43e96f/skills

一套 Claude Code skill 合集。两个方向：开发工作流 + 交易决策。

---

## 开发工作流

| Skill | 说明 | 来源 |
|-------|------|------|
| [pua](./pua/SKILL.md) | 完整开发闭环：需求澄清 → 计划 → 执行 → Codex 审查 → 安全扫描 → 提交 | 改自 [tanweai/pua](https://github.com/tanweai/pua) |
| [kickoff](./kickoff/SKILL.md) | 先问你再动手 — Claude 提问收敛需求，而不是你先写一大段 prompt | 基于 [Axel Bitblaze](https://x.com/Axel_bitblaze69) 的 Interview Me Technique |
| [office-hours](./office-hours/SKILL.md) | 6 个强制问题，逼你想清楚在动手前：这是不是真正该解决的问题？ | 改自 [garrytan/gstack](https://github.com/garrytan/gstack/blob/main/office-hours/SKILL.md) |
| [challenge](./challenge/SKILL.md) | 让第二个 AI 模型来挑毛病——只找问题，不提方案，不改架构 | 原创 |
| [brainstorming](./brainstorming/SKILL.md) | 写代码之前先把想法变成设计 | 改自 [obra/superpowers](https://github.com/obra/superpowers) |

### 工作流逻辑

核心原则：**任务复杂度决定需要多少前期对齐**。`/pua` 永远在最后跑——它会读之前的上下文，自动跳过已经做完的环节。

```
简单任务               →  /pua
需求没想清楚           →  /kickoff → /pua
大项目，方向未定       →  /kickoff → /office-hours → /pua
```

`/challenge` 可以插入任意节点，随时让 Codex 来反驳：

```
/kickoff  →  [/challenge]  →  /pua
/kickoff  →  /office-hours  →  [/challenge]  →  /pua
```

### 其他值得安装的 skill（来自 [obra/superpowers](https://github.com/obra/superpowers)）

这几个基本没改，建议直接从 obra/superpowers 安装：

- `systematic-debugging` — 4 阶段根因分析，先找原因再动手修
- `verification-before-completion` — 用真实命令验证，不靠"我觉得完成了"
- `finishing-a-development-branch` — 结构化处理 merge/PR/分支清理
- `using-git-worktrees` — 高风险改动放隔离分支

---

## 交易决策

| Skill | 说明 | 来源 |
|-------|------|------|
| [cognitive-guardrails](./trading/cognitive-guardrails/SKILL.md) | 反确认偏误协议 — 防止 Claude 只给你想听的答案 | 原创 |

---

## 安装

```bash
git clone https://github.com/0x43e96f/skills ~/skills-repo

# 安装单个 skill
cp -r ~/skills-repo/kickoff ~/.claude/skills/
cp -r ~/skills-repo/pua ~/.claude/skills/

# 安装全部开发 skill
cp -r ~/skills-repo/kickoff ~/skills-repo/pua ~/skills-repo/office-hours \
      ~/skills-repo/challenge ~/skills-repo/brainstorming \
      ~/.claude/skills/

# 安装交易 skill
cp -r ~/skills-repo/trading/cognitive-guardrails ~/.claude/skills/
```

---

## 致谢

- [tanweai/pua](https://github.com/tanweai/pua) — 压力升级概念
- [Axel Bitblaze](https://x.com/Axel_bitblaze69) — Interview Me Technique（kickoff 的来源）
- [garrytan/gstack](https://github.com/garrytan/gstack) — office-hours 强制问题
- [obra/superpowers](https://github.com/obra/superpowers) — brainstorming 及核心开发 skill

## License

MIT
