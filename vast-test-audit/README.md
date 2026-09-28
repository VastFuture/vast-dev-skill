# vast-test-audit

测试审计 Skill —— 编写闸门 + 现有测试清扫。覆盖三种模式：

- **Authoring**：写新测试前的硬门槛
- **Audit**：扫描低价值、与实现耦合、复述源码、为测试而留产线缝的测试
- **Campaign**：一次性修剪某个子系统整套测试面

## 来源

- **原始仓库**：https://github.com/openclaw/openclaw
- **原始路径**：`.agents/skills/test-audit/SKILL.md`
- **原始地址**：https://github.com/openclaw/openclaw/blob/main/.agents/skills/test-audit/SKILL.md
- **集成时间**：2026-09-28
- **版本**：1.0.0
- **改造点**：将 openclaw 专有变量（`$openclaw-testing` / `$crabbox` / `$autoreview` / `scripts/run-vitest.mjs` 等）泛化为“项目自身的 X”，跨项目可用；保留核心工作流与价值标尺。

## 使用

```
/vast-test-audit
```

或在编写、修改、审查测试时由 Skill 自动触发。

## 三种模式与价值标尺

| 模式 | 何时用 | 核心动作 |
| --- | --- | --- |
| Authoring | 写/改测试前 | 答四问 → 查 junk patterns → 查 retention bar |
| Audit | 清扫一批旧测试 | 只读 discovery → 收集 evidence → 按 owner boundary 分批删 |
| Campaign | 清扫某个插件或核心区域 | 先读 [CAMPAIGN.md](CAMPAIGN.md) 再启动 |

## 工作流（Authoring 闸门速查）

```text
新测试加入前：
1. 它保护什么行为 / 不变量 / 独立契约？
2. 什么可信回归会让它失败？
3. 现有覆盖为什么抓不住？
4. 是否引入产线缝（export / flag / wrapper / 注入钩子）？若需要，搬到真实边界。

然后查 retention bar；若都不命中 = 拒。
```

完整细节、junk patterns 清单、CAMPAIGN.md 入口见 [SKILL.md](SKILL.md)。

## 与 vast 系列的协同

- `vast-pragmatic-clean-code-reviewer` —— 代码审查的更广视角
- `vast-code-review-expert` —— 代码评审专家
- `vast-dev-taste-checker` —— 品味检查（包含“实现耦合”类坏味）
- `vast-agent-skill-reviewer` —— 评审 Skill 自身的契约与触发

## 适用项目类型

任何带测试套件的代码库。原始 openclaw 用 Vitest；其他 runner（Jest/MoR/JUnit/pytest/Go test 等）需把 SKILL.md 中 `scripts/run-vitest.mjs` 与 `scripts/check-changed.mjs` 替换为对应项目的命令。Skill 内已使用“项目自身的 X”描述，调用方按实际项目替换具体工具名。