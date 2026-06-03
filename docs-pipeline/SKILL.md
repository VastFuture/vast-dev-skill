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
# 标准模式（推荐，12 个核心目录）
/docs-pipeline

# 最小化模式（7 个必需目录，适合小项目）
DOCS_PIPELINE_MODE=minimal /docs-pipeline

# 完整模式（所有目录，适合大型项目）
DOCS_PIPELINE_MODE=full /docs-pipeline
```

**初始化后**：
1. 📖 打开 `docs/index.md` 查看文档路由
2. ✅ 在 `docs/backlog/README.md` 添加第一个任务
3. 🧪 运行项目测试验证

详细说明见下文"安装模式"章节 ⬇️

---

## 安装模式

docs-pipeline 提供 3 种安装模式，适应不同项目规模和团队经验。

### 模式选择

| 模式 | 适用场景 | 目录数 | 学习曲线 |
|------|---------|--------|---------|
| **minimal**（最小化） | 个人项目、快速原型、初学者 | 7 个必需目录 | 最低 |
| **standard**（标准，默认） | 大多数团队项目 | 12 个核心目录 + 模板 | 中等 |
| **full**（完整） | 大型项目、严格流程 | 所有目录 + AGE 增强 | 较高 |

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

#### Full（完整）

**目录**：standard 的 12 个 + input, discussions, audits, bugs, logs, testing, skills, retrospectives（所有目录）

**特点**：
- 最完整的 AGE 工作流
- 支持审计、讨论、复盘等高级流程
- 适合大型项目或有严格流程要求的团队

**额外功能**：完整的 AGE 增强（任务路由、计划触发器、验证基线）

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

### 可选目录（按需激活，不在默认初始化范围内）

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
- `full` → 完整模式（所有目录）
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
  mkdir -p "$docs_root/context" "$docs_root/backlog" "$docs_root/prd" "$docs_root/exec-plans/active" "$docs_root/exec-plans/completed" "$docs_root/lessons"
  
# Standard 模式（12 个核心目录，默认）
elif [ "$MODE" = "standard" ]; then
  mkdir -p "$docs_root/context" "$docs_root/backlog" "$docs_root/prd" "$docs_root/design" "$docs_root/exec-plans/active" "$docs_root/exec-plans/completed" "$docs_root/research" "$docs_root/issues" "$docs_root/handover" "$docs_root/ideas" "$docs_root/lessons"
  
# Full 模式（所有目录）
elif [ "$MODE" = "full" ]; then
  mkdir -p "$docs_root/context" "$docs_root/backlog" "$docs_root/prd" "$docs_root/design" "$docs_root/exec-plans/active" "$docs_root/exec-plans/completed" "$docs_root/research" "$docs_root/issues" "$docs_root/handover" "$docs_root/ideas" "$docs_root/lessons" "$docs_root/input" "$docs_root/discussions" "$docs_root/audits" "$docs_root/bugs" "$docs_root/logs" "$docs_root/testing" "$docs_root/skills" "$docs_root/retrospectives"
fi
```

**目录对照表**：

| 模式 | context | backlog | prd | exec-plans | lessons | research | design | issues | handover | ideas | input | discussions | audits | bugs | logs | testing | skills | retrospectives |
|------|---------|---------|-----|------------|---------|----------|--------|--------|----------|-------|-------|-------------|--------|------|------|---------|--------|----------------|
| minimal | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| standard | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| full | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

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

**根据模式选择模板**：

所有模式都复制：
- docs-CLAUDE.md, docs-index.md
- context/ 下 4 个文件
- backlog-README.md, prd-README.md, exec-plans-README.md, lessons-README.md

Standard/Full 模式额外复制：
- prd-TEMPLATE.md, exec-plans-TEMPLATE.md
- research-README.md, design-README.md, issues-README.md, issues-TEMPLATE.md
- handover-README.md, handover-TEMPLATE.md, ideas-README.md

Full 模式额外复制：
- input-README.md, discussions-README.md, architecture-README.md

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
| `assets/templates/CLAUDE.md` | `CLAUDE.md` | 项目根 Claude 行为规范（Linus 角色 + 沟通规范 + 通用开发规则；含 TODO 占位让用户填项目特有部分） |
| `assets/templates/AGENTS.md` | `AGENTS.md` | Codex CLI 全局指令（含 AGE Task Routing + Planning Triggers + Verification Baseline） |
| `assets/templates/MBTI_DEV_TRAPS.md` | `MBTI_DEV_TRAPS.md` | 16 种 MBTI 人格的开发陷阱清单 |
| `assets/templates/karpathy-guidelines.md` | `karpathy-guidelines.md` | LLM 编码行为指南 |
| `assets/templates/output-modes.md` | `output-modes.md` | 混合输出模式详细说明（模式 A/B 结构、示例、状态标记） |
| `assets/templates/engineering-rules.md` | `engineering-rules.md` | AGE 工程规则详细说明（任务路由、计划触发器、运营规则） |
| `assets/templates/plan-mode.md` | `plan-mode.md` | Plan 模式详细说明（复杂度分级、Plan 文件规范） |
| `assets/templates/requirement-confirmation.md` | `requirement-confirmation.md` | 需求确认流程详细说明（5 层思考维度、决策输出） |
| `assets/templates/content-organization.md` | `content-organization.md` | 内容组织规范详细说明（列表限制、段落优先） |
| `assets/templates/mcp.json` | `.mcp.json` | 7 个常用 MCP 服务（playwright / thinking / chrome-devtools / fetch / time / context7 / serena），注意源文件名是 `mcp.json`，目标文件名是 `.mcp.json` |

注意：这十个文件**不属于** `docs/` 链路，是项目根级的 AI 代理配置文档。

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

> Pensieve 是可选的版本控制增强工具，**不在默认安装范围内**。

**默认行为**：跳过 Pensieve 集成，不检测、不询问、不提示。

**激活条件**（满足任一）：
1. 环境变量 `ENABLE_PENSIEVE=true`
2. 已存在 `.pensieve/` 目录（说明用户已手动安装）

**集成流程**（仅在激活时执行）：

**分支 A — `.pensieve/` 已存在**：

1. 按 [references/pensieve-integration.md](./references/pensieve-integration.md) 执行 doctor → sync-instructions → .gitignore 保护 → doctor 验证流程
2. 检测 CLAUDE.md 是否已有 `## Pensieve 版本控制` 段落：`Bash grep -q "^## Pensieve 版本控制" CLAUDE.md`
   - 不存在 → 用 `Edit` 把 `assets/templates/pensieve-gitignore-snippet.md` 追加到文件末尾
   - 已存在 → 跳过

**分支 B — `.pensieve/` 不存在 且 `ENABLE_PENSIEVE=true`**：

1. 用 `AskUserQuestion` 询问用户是否要安装 Pensieve
2. 用户确认 → 按 [references/pensieve-integration.md](./references/pensieve-integration.md) 的"安装"章节执行（读取 GitHub 仓库最新 README 获取安装步骤，不要硬编码），然后走分支 A 的完整流程
3. 用户拒绝 → 跳过，报告"已跳过 Pensieve 集成"

**不激活时**：完全跳过此步骤，不在报告中提及。

### 8. 生成 ARCHITECTURE.md（探索型模板）

`ARCHITECTURE.md` 不能简单 cp，必须基于目标项目的实际代码生成。流程：

#### 8.1 检测

```bash
test -f ARCHITECTURE.md && echo "EXISTS" || echo "MISSING"
```

- **EXISTS** → 跳过，记入"已存在跳过"清单
- **MISSING** → 进入 8.2

#### 8.2 调用 Explore 子代理

用 `Agent` 工具，`subagent_type: "Explore"`，提示词如下（中文）：

> 探索目标项目（当前工作目录）的代码结构，按以下固定 5 个章节生成 `ARCHITECTURE.md` 内容并直接写入项目根 `ARCHITECTURE.md`：
>
> 1. **项目概述**：一句话定位 + 后端/前端/数据库技术栈（无则填"无"）
> 2. **常用命令**：后端启动/测试命令、前端启动/构建/测试命令、完整启动说明（按实际项目情况列出，无则省略对应小节）
> 3. **架构**：核心源码目录树（二级深度），每个目录附一句话职责注释
> 4. **数据模型**：列出核心数据模型 + 一句话职责。纯前端/CLI 项目填"无（不涉及持久化数据模型）"
> 5. **开发注意事项**：数据库迁移、代理配置、路由入口、其他关键约定（按实际有无列出 3-5 条即可）
>
> 严格遵守：
> - 只生成这 5 个章节，不要加其他章节
> - 每个章节必须出现，无内容时填"无"
> - 文件开头加一行 `# ARCHITECTURE.md`，第二行加 `> 项目架构文档 - 参见 [CLAUDE.md](./CLAUDE.md) 的行为规范。`
> - 控制在 100 行以内
> - 探索预算：≤8 次工具调用
>
> 探索完成后，用 `Write` 工具写入 `<项目根绝对路径>/ARCHITECTURE.md`，然后简短报告"已生成"。

#### 8.3 智能降级

如果 Explore 子代理失败（返回错误、超时、或未能写入文件），按以下顺序尝试降级：

**降级策略 1：基于 package.json 生成（Node.js 项目）**

```bash
if [ -f "package.json" ]; then
  # 读取 package.json
  NAME=$(jq -r '.name // "未命名项目"' package.json)
  DESC=$(jq -r '.description // "无描述"' package.json)
  SCRIPTS=$(jq -r '.scripts | keys[]' package.json 2>/dev/null || echo "无")
  
  # 生成基本 ARCHITECTURE.md
  cat > ARCHITECTURE.md << EOF
# ARCHITECTURE.md

> 项目架构文档 - 参见 [CLAUDE.md](./CLAUDE.md) 的行为规范。

## 项目概述

**项目名称**：$NAME

**描述**：$DESC

**技术栈**：Node.js / TypeScript（基于 package.json 检测）

## 常用命令

\`\`\`bash
# 可用的 npm scripts:
$SCRIPTS
\`\`\`

## 架构

**注意**：此文档由自动检测生成，仅包含基本信息。请根据实际项目结构补充：
- 源码目录结构（src/）
- 数据模型（如有）
- 开发注意事项

可运行 \`tree src -L 2\` 查看实际目录结构。
EOF
  
  echo "⚠️ Explore 失败，已基于 package.json 生成基本 ARCHITECTURE.md，需补充完整"
  exit 0
fi
```

**降级策略 2：其他项目类型的简化模板**

```bash
# Python 项目
if [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
  PROJECT_TYPE="Python"
  START_CMD="python main.py"
  
# Go 项目
elif [ -f "go.mod" ]; then
  PROJECT_TYPE="Go"
  START_CMD="go run ."
  
# Rust 项目
elif [ -f "Cargo.toml" ]; then
  PROJECT_TYPE="Rust"
  START_CMD="cargo run"
  
# 无法识别
else
  PROJECT_TYPE="未知"
  START_CMD="<启动命令>"
fi

# 生成通用骨架
cat > ARCHITECTURE.md << 'EOF'
# ARCHITECTURE.md

> 项目架构文档 - 参见 [CLAUDE.md](./CLAUDE.md) 的行为规范。

## 项目概述

**技术栈**：$PROJECT_TYPE

## 常用命令

```bash
# 启动
$START_CMD
```

## 架构

**注意**：此文档为模板骨架，需要手动填充：
1. 项目概述（一句话定位 + 技术栈细节）
2. 常用命令（构建、测试、启动命令）
3. 核心源码目录树（二级深度）
4. 数据模型（如有）
5. 开发注意事项
EOF

echo "⚠️ Explore 失败且无法自动检测项目类型，已生成模板骨架，需手动填充"
```

**降级策略 3：完全失败（最后手段）**

如果以上策略都失败，在报告中提示：

```
⚠️ 需人工处理：
  - ARCHITECTURE.md 生成失败，请手动创建或运行 tree src -L 2 查看目录结构
```

不生成任何 ARCHITECTURE.md 文件。

### 9. 输出报告

按以下格式向用户总结：

```
📋 docs-pipeline 执行报告

📌 模式：模式 A（文档跟随项目）/ 模式 B（独立文档仓库：$DOCS_ROOT）
📌 模式：minimal / standard / full

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

## 使用场景

初始化完成后，常见的使用场景：

### 场景 1：添加新功能（标准四步）

> 灵感来源：[neat-freak 四处都补原则](https://github.com/VastFuture/khazix-skills/tree/main/neat-freak)

**标准四步（新增能力时四处都补）**：

1. **docs/prd/**：创建 `feature-name.md`（使用 `prd/TEMPLATE.md`）
   - 需求：要解决什么问题
   - 验收标准：如何验证完成
   - 技术方案：如何实现

2. **docs/design/**：更新架构文档
   - 数据流：数据如何流转
   - 设计取舍：为什么这样设计
   - 模块边界：影响哪些模块

3. **docs/exec-plans/active/**：创建执行计划（如触发计划触发器）
   - 触发条件：> 5 文件或 > 200 行
   - 分阶段：将大特性拆分为多个阶段
   - 风险与依赖：记录已知风险

4. **docs/handover/**：完成后更新已完成清单
   - 已完成功能：新增了什么
   - 已知问题：还有什么问题
   - 注意事项：运维要注意什么

**实施并验证**：
- 运行 `docs/context/project-context.md` 中的验证命令
- 在 `docs/lessons/` 记录教训（如有）

**⚠️ 防膨胀检查**：
如果需要更新 CLAUDE.md/AGENTS.md：
- 判断标准：下次 AI 写代码时如果没看到这条，会不会犯错？
- ✅ 该进：硬边界规则、禁止事项、踩坑警示
- ❌ 不该进：历史叙事（"X 时刻起 Y 上线"）、详细机制
- 红灯线：净涨幅 ≤ 30 行

### 场景 2：修复 Bug

1. 在 `docs/issues/` 创建 `bug-name.md`（使用 `issues/TEMPLATE.md`）
2. 记录问题描述、复现步骤、根因分析
3. 实施修复并验证
4. 更新 issue 状态为"已解决"

### 场景 3：AI 不知道做什么

1. 检查 `docs/backlog/README.md`
2. 确保至少有一个 `status=ready`、`AI 自主级别=implement` 的任务
3. AI 会自动选择优先级最高的任务
4. 如果所有任务都是 `blocked`，在阻塞项中说明原因

### 场景 4：项目交接

1. 在 `docs/handover/` 创建 `handover-YYYY-MM-DD.md`（使用 `handover/TEMPLATE.md`）
2. 填写项目概述、技术架构、关键决策、待办事项、已知问题
3. 提供给接手人阅读

## 关键原则

- **幂等**：重复调用应得到相同结果，已有文件不覆盖
- **不智能 merge**：冲突就报警，不自动合并
- **不删除**：只新建/跳过，从不删用户已有内容
- **不破坏**：项目根 CLAUDE.md 只追加，不修改原有内容
- **不假设技术栈**：只管文档与 AI 代理配置，不碰业务代码

## Gotchas

- **ARCHITECTURE.md 生成降级策略**：Explore 失败后，先尝试基于项目配置文件（package.json/setup.py/go.mod/Cargo.toml）生成基本结构，再尝试通用骨架，最后才完全跳过
- **项目根 CLAUDE.md 已有大量自定义内容**：只追加"## 文档"段落到末尾，绝不修改或删除已有内容。用 `grep -q "^## 文档"` 检测，存在就跳过
- **重复调用后误报"已建"**：幂等检测必须用 `Read` 确认文件实际存在，不能靠 `mkdir -p` 的返回值推断
- **Pensieve 不是必需的**：`.pensieve/` 不存在时完全跳过 Step 7，不询问、不提示。只有当 `ENABLE_PENSIEVE=true` 或 `.pensieve/` 已存在时才激活
- **模板里的 TODO 占位被自动填充**：`<!-- TODO(docs-pipeline): ... -->` 是留给用户的，不要替换
- **模式 B 路径引用错误**：独立文档仓库模式下，项目根 CLAUDE.md/AGENTS.md 中的文档引用必须是正确的相对路径。用 `realpath --relative-to=project_root docs_root` 计算
- **docs/ 目录既是独立 git 仓库又是项目子目录**：检测优先级 `DOCS_ROOT` > `docs/.git` 存在 > 默认 inline
- **用户修改路径后路径不存在**：用户输入的路径不存在时，询问是否创建，不自动创建
- **context/ 目录的 4 个文件是整体**：project-context.md、ai-autonomy-policy.md、codebase-map.md、source-of-truth-and-precedence.md 必须一起存在，才能保证 AI 上下文完整

## 不要做

- ❌ 不要在模板里塞业务示例（保持骨架空白）
- ❌ 不要自动填充索引（让用户用着用着自己填）
- ❌ 不要做 `--reset` / `--uninstall`（用户手动决定）
- ❌ 不要假设项目用 Python/Node/Rust
- ❌ 不要修改项目根 CLAUDE.md 已有内容（只追加"## 文档"段落，不改其他）
- ❌ 不要覆盖已有的 CLAUDE.md / AGENTS.md / MBTI_DEV_TRAPS.md / karpathy-guidelines.md / .mcp.json / ARCHITECTURE.md（用户可能已有定制版本）
- ❌ 不要让 Explore 子代理偏离 5 章节固定结构（保持跨项目一致）
- ❌ 模式 B 不要往项目根写 docs/ 目录（文档完全在独立仓库）
- ❌ 模式 B 不要硬编码文档仓库路径（用 `DOCS_ROOT` 环境变量或自动检测）
- ❌ 不要跳过交互询问（除非用户明确要求）
- ❌ 不要强制用户接受自动检测结果（始终提供修改选项）
