---
name: docs-pipeline
description: Initialize or repair docs/ pipeline + root AI agent templates (CLAUDE.md, AGENTS.md, etc.) for any Claude Code project. Supports both inline docs/ and separate docs repo. Idempotent.基于 AGE (Attractor-Guided Engineering) 增强：Task Routing + Planning Triggers + Verification Baseline. 来源: https://github.com/entropy-cloud/attractor-guided-engineering-template. Use for: "初始化文档结构", "搭建 docs pipeline", "set up docs structure", "initialize docs pipeline", "fix docs structure".
metadata:
  author: tracker-system
  version: "4.2"
allowed-tools: Bash Read Write Edit Glob Agent
---

# Docs Pipeline Skill

一键初始化或修复 Claude Code 项目的 `docs/` 产物链路 + 项目根 AI 代理模板 + 自动探索生成的 `ARCHITECTURE.md`。

基于 [AGE (Attractor-Guided Engineering)](https://github.com/entropy-cloud/attractor-guided-engineering-template) 增强。

## ⚡ 快速入门（30 秒）

```bash
# 标准模式（默认，12 个核心目录）
/docs-pipeline

# 最小化模式（7 个必需目录，适合小项目）
DOCS_PIPELINE_MODE=minimal /docs-pipeline
```

**初始化后**：
1. 📖 打开 `docs/index.md` 查看文档路由
2. ✅ 在 `docs/backlog/README.md` 添加第一个任务
3. 🧪 运行项目测试验证

详细说明见下文"安装模式"章节 ⬇️

---

## 安装模式

docs-pipeline 提供 2 种安装模式，适应不同项目规模。

### 模式选择

| 模式 | 适用场景 | 目录数 | 学习曲线 |
|------|---------|--------|---------|
| **minimal**（最小化） | 个人项目、快速原型、初学者 | 7 个必需目录 | 最低 |
| **standard**（标准，默认） | 大多数团队项目 | 12 个核心目录 + 模板 | 中等 |

### 指定模式

```bash
# 方式 1：环境变量
DOCS_PIPELINE_MODE=minimal /docs-pipeline

# 方式 2：默认（不指定则使用 standard）
/docs-pipeline
```

### 模式对比

#### Minimal（最小化）

**目录**：context, backlog, prd, exec-plans, lessons（7 个必需目录）

**特点**：
- 最快上手（< 5 分钟理解全部结构）
- 核心工作流完整（需求 → 计划 → 执行 → 教训）
- 适合个人或 2-3 人小团队

**缺失功能**：无 research、design、issues、handover 等扩展目录

#### Standard（标准，默认）

**目录**：minimal 的 7 个 + research, design, issues, handover, ideas（12 个核心目录）

**特点**：
- 平衡完整性与复杂度
- 支持调研、设计、Bug 追踪、项目交接
- 适合大多数团队项目

**包含模板**：PRD、执行计划、交接文档、问题记录

---

## 核心结构

### 模式 A：文档跟随项目（默认）

```
项目根/
├── CLAUDE.md                 # 不存在则建（Linus 角色 + 沟通规范 + 通用开发规则模板）【必需】
├── AGENTS.md                 # 不存在则建（AI 代理全局指令，含 AGE 10 条运营规则）【必需】
├── MBTI_DEV_TRAPS.md         # 不存在则建（16 种人格陷阱清单）【推荐】
├── karpathy-guidelines.md    # 不存在则建（LLM 编码行为指南）【推荐】
├── ARCHITECTURE.md           # 不存在则用 Explore 子代理探索后生成【推荐】
├── .mcp.json                 # 不存在则建（7 个常用 MCP 服务）【可选】
├── .claude/
│   └── commands/
│       └── ideas.md          # 不存在则建（/ideas 随手记命令）
└── docs/
    ├── CLAUDE.md             # 总规则（含 Owner Docs 职责）
    ├── index.md              # ★ 文档路由中枢
    ├── context/              # ★ 强制 AI 上下文【必需】
    │   ├── project-context.md       # 项目上下文、验证命令
    │   ├── ai-autonomy-policy.md   # AI 自主级别、受保护区域
    │   ├── codebase-map.md         # 代码库地图
    │   └── source-of-truth-and-precedence.md  # 真相优先级
    ├── backlog/              # ★ 工作队列、AI 自主级别标签【必需】
    │   └── README.md
    ├── prd/                  # 实现就绪的需求【必需】
    │   └── README.md
    ├── design/               # ★ 稳定的应用层设计基线【推荐】
    │   └── README.md
    ├── exec-plans/           # 执行计划（含 Plan/Closure 审计）【必需】
    │   ├── README.md
    │   ├── active/
    │   └── completed/
    │       └── tech-debt-tracker.md
    ├── ideas/                # 灵感池（随手记，零结构）【可选】
    │   └── README.md
    ├── research/             # 调研文档【推荐】
    │   └── README.md
    ├── handover/             # 项目交接【可选】
    │   └── README.md
    ├── issues/               # Bug 追踪【推荐】
    │   └── README.md
    └── lessons/              # 经验教训【必需】
        └── README.md
```

**目录优先级说明**：
- 【必需】：核心工作流必需，始终创建
- 【推荐】：大多数项目推荐使用
- 【可选】：按需激活，见下文"可选目录"章节

### 可选目录（按需手动创建）

如果项目需要更细粒度的分类，可以手动创建以下目录：

```
docs/
├── input/            # 原始 PM 素材
├── discussions/      # 需求澄清讨论
├── audits/           # 审计记录
├── bugs/             # 非显而易见的 bug 历史
├── logs/             # 每日实现记录
├── testing/          # 手动/探索性测试记录
├── skills/           # 可复用提示词模板
└── retrospectives/   # 交付后复盘
```

**注意**：这些目录不会自动创建，需要时运行 `mkdir -p docs/<目录名>` 即可。

### 模式 B：独立文档仓库

```
项目根/                          文档仓库根/
├── CLAUDE.md                   ├── .git/
├── AGENTS.md                   ├── CLAUDE.md             # docs-pipeline 模板
├── ...（项目代码）              ├── docs/                 # 标准 docs 结构
│                               │   ├── CLAUDE.md
│                               │   ├── ideas/
│                               │   ├── research/
│                               │   ├── prd/
│                               │   ├── exec-plans/
│                               │   ├── handover/
│                               │   ├── issues/
│                               │   └── lessons/
│                               └── ...（其他文档内容）

项目根 CLAUDE.md/AGENTS.md 中的文档引用指向：文档仓库根/docs/
```

**触发模式 B 的条件：**
1. 设置环境变量 `DOCS_ROOT=/path/to/docs/repo`
2. 或检测到 `docs/` 目录是一个独立的 git 仓库（有 `.git` 子目录）
3. 或用户明确指定文档仓库路径

## 工作流

调用此 skill 时，按以下步骤执行：

### 0. 检测文档模式

**Step 0.1：检查环境变量 `DOCS_ROOT`**
- 已设置 → 进入 **模式 B（独立文档仓库）**，文档根 = `$DOCS_ROOT`
- 未设置 → 进入 **Step 0.2**

**Step 0.2：自动检测 `docs/` 是否独立 git 仓库**
```bash
test -d docs/.git && echo "INDEPENDENT_REPO" || echo "INLINE"
```
- `INDEPENDENT_REPO` → **模式 B**，文档根 = `docs/`（相对于当前目录）
- `INLINE` → **模式 A**，文档根 = `docs/`（相对于当前目录）

**Step 0.3：确定文档根路径**
- 模式 A：`docs_root = ./docs`
- 模式 B：`docs_root = $DOCS_ROOT` 或 `./docs`（如果 docs 是独立仓库）

检测结果将在 Step 9 报告中展示，用户可事后调整配置。

**Step 0.4：确定项目根路径**
- 模式 A：`project_root = ./`
- 模式 B：`project_root = ./`（项目代码根），文档引用路径 = `docs_root 相对于 project_root 的路径`

**Step 0.5：检测安装模式**

检查环境变量 `DOCS_PIPELINE_MODE`：
- `minimal` → 最小化模式（7 个必需目录）
- `standard` → 标准模式（12 个核心目录，默认）
- 未设置 → 默认 `standard`

```bash
MODE="${DOCS_PIPELINE_MODE:-standard}"
```

### 1. 检测目标项目状态

先用 `Bash ls "$docs_root" 2>/dev/null || echo "MISSING"` 检测：

- 不存在 `docs/` → 全新初始化
- 存在 `docs/` 但缺部分目录/README → 修复模式
- 全部齐全 → 跳过，输出"已是规范结构"

### 2. 建目录

```bash
mkdir -p "$docs_root/context" "$docs_root/backlog" "$docs_root/prd" "$docs_root/design" "$docs_root/exec-plans/active" "$docs_root/exec-plans/completed" "$docs_root/ideas" "$docs_root/research" "$docs_root/handover" "$docs_root/issues" "$docs_root/lessons"
```

`mkdir -p` 本身是幂等的，已有目录不会报错。

**根据模式创建目录**：

```bash
# Minimal 模式（7 个必需目录）
if [ "$MODE" = "minimal" ]; then
  mkdir -p "$docs_root/context" "$docs_root/backlog" "$docs_root/prd" "$docs_root/exec-plans/active" "$docs_root/exec-plans/completed" "$docs_root/lessons" "$docs_root/agent-guides"
  
# Standard 模式（12 个核心目录，默认）
elif [ "$MODE" = "standard" ]; then
  mkdir -p "$docs_root/context" "$docs_root/backlog" "$docs_root/prd" "$docs_root/design" "$docs_root/exec-plans/active" "$docs_root/exec-plans/completed" "$docs_root/research" "$docs_root/issues" "$docs_root/handover" "$docs_root/ideas" "$docs_root/lessons" "$docs_root/agent-guides"
fi
```

**目录对照表**：

| 模式 | context | backlog | prd | exec-plans | lessons | research | design | issues | handover | ideas |
|------|---------|---------|-----|------------|---------|----------|--------|--------|----------|-------|
| minimal | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| standard | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**核心目录**：context、backlog、research、prd、design、exec-plans、lessons
**可选目录**：ideas、handover、issues（以及按需激活的 input、discussions、audits、bugs、logs、testing、skills、retrospectives）

### 3. 写入 docs/ 模板

模板位于本 skill 目录下 `assets/templates/`。对每个目标文件：

1. 用 `Read` 检测是否已存在
2. **不存在** → 用 `Read` 读取本 skill 下的模板，再用 `Write` 落地到目标路径
3. **已存在** → 跳过，记入"已存在跳过"清单

模板映射：

| 模板 | 目标路径 |
|------|---------|
| `assets/templates/docs-CLAUDE.md` | `$docs_root/CLAUDE.md` |
| `assets/templates/docs-index.md` | `$docs_root/index.md` |
| `assets/templates/context/project-context.md` | `$docs_root/context/project-context.md` |
| `assets/templates/context/ai-autonomy-policy.md` | `$docs_root/context/ai-autonomy-policy.md` |
| `assets/templates/context/codebase-map.md` | `$docs_root/context/codebase-map.md` |
| `assets/templates/context/source-of-truth-and-precedence.md` | `$docs_root/context/source-of-truth-and-precedence.md` |
| `assets/templates/backlog-README.md` | `$docs_root/backlog/README.md` |
| `assets/templates/prd-README.md` | `$docs_root/prd/README.md` |
| `assets/templates/prd-TEMPLATE.md` | `$docs_root/prd/TEMPLATE.md` |
| `assets/templates/design-README.md` | `$docs_root/design/README.md` |
| `assets/templates/exec-plans-README.md` | `$docs_root/exec-plans/README.md` |
| `assets/templates/exec-plans-TEMPLATE.md` | `$docs_root/exec-plans/TEMPLATE.md` |
| `assets/templates/ideas-README.md` | `$docs_root/ideas/README.md` |
| `assets/templates/research-README.md` | `$docs_root/research/README.md` |
| `assets/templates/handover-README.md` | `$docs_root/handover/README.md` |
| `assets/templates/handover-TEMPLATE.md` | `$docs_root/handover/TEMPLATE.md` |
| `assets/templates/issues-README.md` | `$docs_root/issues/README.md` |
| `assets/templates/issues-TEMPLATE.md` | `$docs_root/issues/TEMPLATE.md` |
| `assets/templates/lessons-README.md` | `$docs_root/lessons/README.md` |
| `assets/templates/docs-agent-guides/MBTI_DEV_TRAPS.md` | `$docs_root/agent-guides/MBTI_DEV_TRAPS.md` |
| `assets/templates/docs-agent-guides/karpathy-guidelines.md` | `$docs_root/agent-guides/karpathy-guidelines.md` |
| `assets/templates/docs-agent-guides/output-modes.md` | `$docs_root/agent-guides/output-modes.md` |
| `assets/templates/docs-agent-guides/engineering-rules.md` | `$docs_root/agent-guides/engineering-rules.md` |
| `assets/templates/docs-agent-guides/plan-mode.md` | `$docs_root/agent-guides/plan-mode.md` |
| `assets/templates/docs-agent-guides/requirement-confirmation.md` | `$docs_root/agent-guides/requirement-confirmation.md` |
| `assets/templates/docs-agent-guides/content-organization.md` | `$docs_root/agent-guides/content-organization.md` |

**根据模式选择模板**：

所有模式都复制：
- docs-CLAUDE.md, docs-index.md
- context/ 下 4 个文件
- backlog-README.md, prd-README.md, exec-plans-README.md, lessons-README.md
- agent-guides/ 下 7 个辅助文档

Standard 模式额外复制：
- prd-TEMPLATE.md, exec-plans-TEMPLATE.md
- research-README.md, design-README.md, issues-README.md, issues-TEMPLATE.md
- handover-README.md, handover-TEMPLATE.md, ideas-README.md

#### 自动填充验证命令

写入 `project-context.md` 后，自动检测项目类型并填充验证命令：

**检测逻辑**：
```bash
# 检测项目类型
if [ -f "package.json" ]; then
  # Node.js 项目
  BUILD_CMD="npm run build"
  TEST_CMD="npm test"
  START_CMD="npm start"
elif [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
  # Python 项目
  BUILD_CMD="无"
  TEST_CMD="pytest"
  START_CMD="python main.py"
elif [ -f "go.mod" ]; then
  # Go 项目
  BUILD_CMD="go build"
  TEST_CMD="go test ./..."
  START_CMD="go run ."
elif [ -f "Cargo.toml" ]; then
  # Rust 项目
  BUILD_CMD="cargo build"
  TEST_CMD="cargo test"
  START_CMD="cargo run"
else
  # 无法检测
  BUILD_CMD="<构建命令，占位则填\"无\">"
  TEST_CMD="<测试命令，占位则填\"无\">"
  START_CMD="<启动命令，占位则填\"无\">"
fi
```

用检测到的命令替换 `project-context.md` 中的占位符。如果无法检测，保留占位符并在报告中添加提醒：

```
⚠️ 需人工处理：
  - 验证命令未自动检测，请手动填写 docs/context/project-context.md
```

**不要因为验证命令是占位符就停止工作**。继续执行，让用户在实际使用时再填充。

### 4. 写入项目根 AI 代理模板

同样的"已存在则跳过"策略，目标在项目根：

| 模板 | 目标路径 | 用途 |
|------|---------|------|
| `assets/templates/CLAUDE.md` | `CLAUDE.md` | 项目根 Claude 行为规范（Linus 角色 + 沟通规范 + 通用开发规则；含 TODO 占位让用户填项目特有部分；引用 docs/agent-guides/ 下的辅助文档） |
| `assets/templates/AGENTS.md` | `AGENTS.md` | Codex CLI 全局指令（含 AGE Task Routing + Planning Triggers + Verification Baseline） |
| `assets/templates/mcp.json` | `.mcp.json` | 7 个常用 MCP 服务（playwright / thinking / chrome-devtools / fetch / time / context7 / serena），注意源文件名是 `mcp.json`，目标文件名是 `.mcp.json` |

注意：
- 项目根只保留 3 个核心文件（CLAUDE.md、AGENTS.md、.mcp.json）
- ARCHITECTURE.md 在 Step 8 生成
- 7 个辅助文档（MBTI_DEV_TRAPS.md、karpathy-guidelines.md 等）在 Step 3 已写入 `$docs_root/agent-guides/`

**模式 B 特殊处理：**
- 文档引用路径 = `docs_root 相对于 project_root 的相对路径`
- 例如：`DOCS_ROOT=../ai-dev-log` → 引用为 `../ai-dev-log/docs/prd/`

### 5. 写入项目级命令

同样的"已存在则跳过"策略：

| 模板 | 目标路径 | 用途 |
|------|---------|------|
| `assets/templates/commands/ideas.md` | `.claude/commands/ideas.md` | `/ideas` 随手记命令，将灵感直接写入 `$docs_root/ideas/` |

命令文件是 Claude Code 的项目级 slash command，放在 `.claude/commands/` 下即可被 `/命令名` 调用。

**模式 B 特殊处理：** `/ideas` 命令需写入到 `$docs_root/ideas/` 而非项目根 `docs/ideas/`

### 6. 处理项目根 CLAUDE.md 的"## 文档"段落

CLAUDE.md 的写入由 step 4 完成。本步只做一件事：如果 step 4 走的是"已存在跳过"分支（即用户已有自己的 CLAUDE.md），那么尝试追加"## 文档"段落，让用户的现有 CLAUDE.md 也能链接到 docs 产物链路。

- **step 4 写入了完整模板** → 跳过本步（模板自带"## 文档"段落）
- **step 4 因为已存在跳过** → 进入下面的子流程：
  - 检测：`Bash grep -q "^## 文档" CLAUDE.md`
  - 不存在 → 用 `Edit` 把 `assets/templates/claude-md-snippet.md` 追加到文件末尾
  - 已存在 → 跳过，提示"已有文档段落，未变更"

**模式 B 特殊处理：** 追加的"## 文档"段落中的路径引用需指向文档仓库路径

### 7. Pensieve 集成（可选插件）

> 详见 [ADVANCED.md](./ADVANCED.md#pensieve-集成可选插件)

**默认行为**：跳过 Pensieve 集成，不检测、不询问、不提示。

**激活条件**：环境变量 `ENABLE_PENSIEVE=true` 或已存在 `.pensieve/` 目录。

### 8. 生成 ARCHITECTURE.md（探索型模板）

> 详见 [ADVANCED.md](./ADVANCED.md#architecturemd-生成降级策略)

**流程概述**：检测文件存在 → 调用 Explore 子代理生成 → 失败则按项目类型智能降级（package.json / setup.py / go.mod / Cargo.toml / 通用骨架）。

### 9. 输出报告

按以下格式向用户总结：

```
📋 docs-pipeline 执行报告

📌 模式：模式 A（文档跟随项目）/ 模式 B（独立文档仓库：$DOCS_ROOT）
📌 安装模式：minimal / standard

✅ 已建（新增）：
  - <path>
  - ...

🔍 已探索生成（基于项目代码）：
  - ARCHITECTURE.md

⏭️ 已存在跳过（未变更）：
  - <path>
  - ...

⚠️ 需人工处理：
  - <说明>

🔄 迁移提示（如检测到旧位置文件）：
  - 检测到项目根目录的辅助文档（MBTI_DEV_TRAPS.md、karpathy-guidelines.md 等）
  - 建议移动到 docs/agent-guides/ 并更新 CLAUDE.md 引用
  - 旧文件列表：<列出检测到的文件>

🔌 可选插件：
  - Pensieve: 未激活（设置 ENABLE_PENSIEVE=true 启用）

---

⏭️ 下一步（重要）：
1. 🔧 填写验证命令：编辑 docs/context/project-context.md
2. 📖 了解文档结构：打开 docs/index.md
3. ✅ 添加第一个任务：编辑 docs/backlog/README.md
4. 🧪 验证初始化：运行项目测试命令

💡 快速入门指南：docs/CLAUDE.md
```

**迁移检测逻辑**（在 Step 9 执行）：

```bash
# 检测项目根目录是否有旧位置的辅助文档
OLD_FILES=""
for f in MBTI_DEV_TRAPS.md karpathy-guidelines.md output-modes.md engineering-rules.md plan-mode.md requirement-confirmation.md content-organization.md; do
  if [ -f "$f" ]; then
    OLD_FILES="$OLD_FILES\n  - $f"
  fi
done

if [ -n "$OLD_FILES" ]; then
  echo "🔄 迁移提示：检测到项目根目录的辅助文档，建议移动到 docs/agent-guides/ 并更新 CLAUDE.md 引用"
  echo "  旧文件列表：$OLD_FILES"
fi
```

## 使用场景

详见 [USAGE.md](./USAGE.md) 了解常见使用场景（添加功能、修复 Bug、AI 自主任务、项目交接）。

## 关键原则

- **幂等**：重复调用应得到相同结果，已有文件不覆盖
- **不智能 merge**：冲突就报警，不自动合并
- **不删除**：只新建/跳过，从不删用户已有内容
- **不破坏**：项目根 CLAUDE.md 只追加，不修改原有内容
- **不假设技术栈**：只管文档与 AI 代理配置，不碰业务代码

## 陷阱与注意事项

详见 [USAGE.md](./USAGE.md#gotchas常见陷阱) 了解常见陷阱和"不要做"清单。
