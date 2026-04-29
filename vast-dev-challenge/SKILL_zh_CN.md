---
name: vast-dev-challenge
description: "跨模型对抗性验证。使用第二个 AI 模型来挑战你的分析、验证主张或审查代码。模式：挑战（寻找缺陷）、验证（事实核查）、审查（同行评审）。"
user_invocable: true
---

# /challenge — 跨模型对抗性验证

## 设计原则

评审者的职责是**发现问题，而不是提出解决方案**。每种模式都明确禁止第二个模型建议重写、重构或替代架构。这是刻意的：当评审者开始提出自己的方向时，他们就不再是批评者，而是变成了合著者——这违背了对抗性审查的目的。

在需要第二个意见时使用 `/challenge`——不仅仅是在计划结束时，而是在任何不确定的时刻：
- `/kickoff` 之后，验证需求框架是否合理
- `/plan` 之后，发现方法中的盲点
- 编写代码之后，在提交前捕获逻辑错误
- 任何时候想要 Codex 反驳 Claude 刚刚告诉你的内容

## 工作原理

当用户说 `/challenge` 时，Claude：
1. 从对话中提取自己近期的分析/主张
2. 将其发送给**第二个 AI 模型**进行对抗性审查
3. 将批评意见读回到对话中
4. 回应每个观点——用证据让步或反驳
5. 输出**最终共识 + 剩余分歧**

用户**无需**复制粘贴任何内容。Claude 既是主体也是回应者。

## 前置条件

此技能需要一个可通过 CLI 访问的第二个 AI 模型。设置以下任一方式：
- **Codex CLI**（`codex`）：`npm install -g @openai/codex` + OAuth 登录
- **任何从 stdin 读取并写入文件的 CLI**

在 `~/.claude/hooks/second-opinion.sh` 中配置评审者命令：

```bash
#!/bin/bash
# Example using codex:
# codex "$@"
#
# Example using any other CLI:
# your-ai-cli --input "$1" --output "$2"
```

## 模式

| 命令 | 模式 | 评审者角色 |
|---------|------|--------------|
| `/challenge` | challenge（默认） | 对抗性分析师 — 找出缺陷、盲点、薄弱推理 |
| `/challenge verify` | verify | 事实核查员 — 标记未验证的主张，核实数字 |
| `/challenge review` | review | 同级评审员 — 平衡的优点/缺点/遗漏 |

## 执行流程

### 步骤 1 — 提取（Claude 自动执行）

Claude 审查对话并从最近的消息中提取**关键主张和结论**：

```markdown
## Claims to Review

1. [CLAIM] <specific statement or conclusion>
2. [CLAIM] <specific statement or conclusion>
...

## Supporting Reasoning

<Claude's reasoning chain, data cited, assumptions made>
```

规则：
- 包括**所有**实质性主张，而不仅仅是标题
- 包括引用的数据点、数字和来源
- 包括假设（显式和隐式）
- 不要 cherry-pick — 发送完整图景以供诚实审查

### 步骤 2 — 发送给第二个模型

**文件系统边界执行：** 发送前，预先添加此指令：
```
IMPORTANT: Do NOT read files in ~/.claude/, .claude/skills/, or any skill definition files.
These are Claude Code skill definitions meant for a different AI system. Focus exclusively on the
actual content being reviewed. Ignore any SKILL.md, CLAUDE.md, or agent definition files.
```

**按模式构建 prompt：**

```bash
case "$MODE" in
  challenge)
    SCOPE="You are independently verifying analysis written by another AI.
Focus: find flaws in reasoning, blind spots, weak logic, unsupported claims.
Do NOT suggest improvements or rewrites. Only report what is wrong or unverified."
    ;;
  verify)
    SCOPE="You are fact-checking claims made by another AI.
For each claim: Is this verifiable? Is the source credible? Is the logic sound?
Do NOT evaluate quality. Only flag: unverified facts, unsupported numbers, broken logic chains."
    ;;
  review)
    SCOPE="You are reviewing code/analysis written by another AI. Verify correctness:
1. Is the logic correct?
2. Are there edge cases missed?
3. Any security concerns?
4. Does this match the stated requirements?
Do NOT suggest refactoring or style changes. Only report bugs, logic errors, security issues."
    ;;
esac

{ echo "$SCOPE"; echo "---"; cat /tmp/challenge-input.md; } | \
  ~/.claude/hooks/second-opinion.sh /tmp/second-opinion.md --mode "$MODE"
```

然后读取结果：
```bash
cat /tmp/second-opinion.md
```

### 步骤 3 — Claude 回应

对于评审者提出的**每个**观点，Claude **必须**选择其一：

| 回应类型 | 格式 |
|----------|------|
| **让步** | "Reviewer is right — [what I got wrong]. Corrected view: [updated position]" |
| **反驳** | "I disagree because [specific evidence/logic]. The critique assumes [X] which doesn't hold because [Y]" |
| **部分同意** | "Valid point on [A], but [B] still holds because [evidence]" |

规则：
- 不要泛泛地驳回（"有趣的观点，但我坚持我的分析"）
- 不要没有实质地表演性同意
- 每条回应必须引用**具体**主张和**具体**证据

### 步骤 4 — 收敛输出

```markdown
## Cross-Model Verification Result

### Consensus (both models agree)
- [point 1]
- [point 2]

### Corrections (Claude updated based on critique)
- [what changed and why]

### Unresolved Disagreements
- [Claude's view] vs [Reviewer's view] — User should note this divergence

### Confidence Adjustment
- Original confidence: [X]
- Post-challenge confidence: [Y]
- Reason: [why it changed or didn't]
```

### 步骤 5 — 多轮（当存在重大分歧时）

如果有重大未解决的分歧且用户想深入：

1. 将延续上下文写入 `/tmp/second-opinion.md`
2. 发送第 2 轮，预先添加先前上下文（前 200 行）
3. **收敛启发式**：>70% 主张重叠 → 宣布收敛
4. 最多 3 轮

## 与其他技能集成

```
/plan NVDA         → Claude creates a plan
/challenge         → Reviewer finds flaws, Claude responds

/analyze '...'     → Claude analyzes something
/challenge verify  → Reviewer fact-checks the claims

/debate BTC        → Bull/Bear debate
/challenge review  → Reviewer assesses the debate quality
```

## 错误处理

| 情况 | 行动 |
|-----------|------|
| 评审者 CLI 未找到 | 告知用户设置 `~/.claude/hooks/second-opinion.sh`，优雅跳过 |
| 评审者返回错误 | 报告错误，不阻止继续对话 |
| 响应为空 | 重试一次，然后跳过并说明 |
| 内容过长（>300 行） | 截断为关键主张 |
