# docs-pipeline

> **用户级通用版本**（来自 tracker-system 的 docs-pipeline skill v0.5.0）
> 适用于所有 Claude Code 项目，一键初始化文档产物链路 + AI 代理配置。

## 产物链路

## 产物链路

```
research（调研）→ prd（需求）→ exec-plans/active（计划进行中）→ exec-plans/completed（计划完成）
                                                                   ↓
                                                               lessons（踩坑教训，按需横切）
```

## 使用

在 Claude Code 里说：
- "初始化文档结构"
- "应用产物链路"
- "搭建 docs pipeline"
- "set up docs structure"

skill 会自动识别并执行。

## 行为契约

| 状态 | 动作 |
|------|------|
| `docs/` 不存在 | 全新初始化（建 6 目录 + 6 README + 1 CLAUDE.md） |
| `docs/` 部分存在 | 修复模式，只补缺失项 |
| `docs/` 全部齐全 | 跳过，输出"已规范" |
| 项目根 `CLAUDE.md` 不存在 | 写入模板（Linus 角色 + 沟通规范 + 通用开发规则，含 TODO 占位） |
| 项目根 `CLAUDE.md` 已存在但无 "## 文档" 段落 | 追加 snippet（不动其他内容） |
| 项目根 `CLAUDE.md` 已存在且有 "## 文档" | 跳过，提示人工 |
| 项目根 `AGENTS.md` 不存在 | 写入模板（Codex CLI 全局指令） |
| 项目根 `MBTI_DEV_TRAPS.md` 不存在 | 写入模板（人格陷阱清单） |
| 项目根 `karpathy-guidelines.md` 不存在 | 写入模板（LLM 编码行为指南） |
| 项目根 `.mcp.json` 不存在 | 写入模板（7 个常用 MCP 服务） |
| 项目根 `ARCHITECTURE.md` 不存在 | **调用 Explore 子代理探索代码后生成**；探索失败则落地空骨架 |

## 关键特性

- **幂等**：重复调用安全，不覆盖已有文件
- **零破坏**：从不删除用户内容；只新建或跳过
- **零依赖**：不假设技术栈，只管文档与 AI 代理配置
- **空白骨架 + TODO 占位**：docs/ 模板不预填业务内容；项目根模板用 `<!-- TODO(docs-pipeline): ... -->` 标记需要用户填的位置
- **探索生成**：`ARCHITECTURE.md` 基于目标项目代码自动探索生成（5 章节固定结构）

## 目录结构

```
docs-pipeline/
├── SKILL.md                            # Claude 行为指令（带 frontmatter）
├── README.md                           # 本文档（人类可读）
└── assets/templates/
    ├── docs-CLAUDE.md                  # docs/CLAUDE.md 总规则
    ├── research-README.md
    ├── prd-README.md
    ├── exec-plans-README.md
    ├── handover-README.md
    ├── lessons-README.md
    ├── claude-md-snippet.md            # 项目根 CLAUDE.md "## 文档" 段落（已存在时追加用）
    ├── CLAUDE.md                       # 项目根：完整 Claude 行为规范模板（含 TODO 占位）
    ├── AGENTS.md                       # 项目根：Codex CLI 全局指令
    ├── MBTI_DEV_TRAPS.md               # 项目根：16 种 MBTI 人格陷阱
    ├── karpathy-guidelines.md          # 项目根：LLM 编码行为指南
    ├── mcp.json                        # 项目根：→ .mcp.json（7 个常用 MCP 服务）
    └── ARCHITECTURE.md.template        # 项目根：探索失败时的降级骨架（5 章节）
```

## 设计原则

源自 Linus 哲学：

1. **数据结构先行**：5 个目录就是 5 种产物状态，状态机清晰
2. **消除特殊情况**：不区分"新项目/老项目"——用幂等替代分支
3. **不破坏 userspace**：只追加，不覆盖
4. **简洁**：SKILL.md 用自然语言指令驱动 Claude，不写脚本

---

## 维护手册：怎么加新模板

适用场景：发现某份通用文档（如 `MISTAKES.md`、`KNOWLEDGE.md`、某种代码规范）值得在每个新项目都自动落地，需要新增到 skill 的模板清单。

### 5 步流程

**Step 1：放模板进 assets/templates/**

```bash
cp <源文件路径> .claude/skills/docs-pipeline/assets/templates/<目标文件名>
```

模板文件名建议与目标落地路径同名，避免映射混淆。

**Step 2：改 SKILL.md（3 处）**

1. **frontmatter 的 `description`**：在括号里加上新模板名（影响 skill 触发匹配）
2. **「核心结构」目录树**：加入新文件位置
3. **「写入项目根 AI 代理模板」表格**（如果是根级模板）或「写入 docs/ 模板」表格（如果是 docs/ 内）：增加一行映射
4. **「不要做」清单**：在"不覆盖已有的 X / Y / Z"那一条加上新文件名

**Step 3：改 README.md（2 处）**

1. **「行为契约」表格**：加一行 `项目根 X 不存在 → 写入模板`
2. **「目录结构」**：在 `assets/templates/` 列表中加入新文件 + 一句话用途

**Step 4：升版本号**

SKILL.md 的 `metadata.version` 升级（语义版本：加新模板属于 minor，如 0.3.0 → 0.4.0）。

**Step 5：Dogfood 验证**

```bash
TARGET=/tmp/docs-pipeline-dogfood-$$
SKILL=<本 skill 绝对路径>

# Round 1: 全新初始化
mkdir -p $TARGET
mkdir -p $TARGET/docs/{research,prd,exec-plans/{active,completed},handover,lessons}
# 对每个模板: cp $SKILL/assets/templates/X $TARGET/X

# Round 2: 幂等性测试 (重跑应该全部跳过)

# 字节级 diff 验证
diff -q <源文件> $TARGET/<目标文件>

rm -rf $TARGET
```

通过标准：
- ✅ 全新模式：所有文件全部写入
- ✅ 二次模式：所有文件跳过（幂等）
- ✅ 字节级 diff：模板与源文件完全一致

### 反例：什么不该加

- ❌ 项目特有的业务文档（如某个公司的 PRD 模板、某个产品的接口文档）
- ❌ 与现有模板职责重叠的文档（如又一个"代码规范"）
- ❌ 频繁变化的内容（每月更新一次的清单）
- ❌ 体积巨大（>50KB）的文档（影响 skill 加载性能）

### 模板的两种类型

| 类型 | 例子 | 实现 |
|------|------|------|
| **静态模板** | AGENTS.md / karpathy-guidelines.md | `cp` 即可 |
| **探索型模板** | ARCHITECTURE.md | 需要调用 Explore 子代理读项目代码后生成 |

探索型模板的额外要求：
- 在 SKILL.md 里明确给 Claude 的"探索指令"（章节结构、字数预算、工具预算）
- **必须有降级骨架** `<name>.template`：探索失败时落地，不让流程卡住
- `allowed-tools` 必须包含 `Agent`

### 加模板前自问

1. 这份文档在 **3+ 个项目** 都需要吗？
2. 它在未来 6 个月内 **不会频繁修改** 吗？
3. 它和现有模板 **职责不重叠** 吗？

三个 yes 才加。否则放在原项目里就够。
