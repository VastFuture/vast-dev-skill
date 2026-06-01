---
name: docs-pipeline
description: Initialize or repair docs/ pipeline + root AI agent templates (CLAUDE.md, AGENTS.md, etc.) for any Claude Code project. Supports both inline docs/ and separate docs repo. Idempotent.基于 AGE (Attractor-Guided Engineering) 增强：Task Routing + Planning Triggers + Verification Baseline. Use for: "初始化文档结构", "搭建 docs pipeline", "set up docs structure", "initialize docs pipeline", "fix docs structure".
metadata:
  author: tracker-system
  version: "2.0.0"
allowed-tools: Bash Read Write Edit Glob Agent
---

# Docs Pipeline Skill

一键初始化或修复 Claude Code 项目的 `docs/` 产物链路 + 项目根 AI 代理模板 + 自动探索生成的 `ARCHITECTURE.md`。

## 核心结构

### 模式 A：文档跟随项目（默认）

```
项目根/
├── CLAUDE.md                 # 不存在则建（Linus 角色 + 沟通规范 + 通用开发规则模板）
├── AGENTS.md                 # 不存在则建（Codex CLI 全局指令，含 AGE Task Routing + Planning Triggers）
├── MBTI_DEV_TRAPS.md         # 不存在则建（16 种人格陷阱清单）
├── karpathy-guidelines.md    # 不存在则建（LLM 编码行为指南）
├── ARCHITECTURE.md           # 不存在则用 Explore 子代理探索后生成
├── .mcp.json                 # 不存在则建（7 个常用 MCP 服务）
├── .claude/
│   └── commands/
│       └── ideas.md          # 不存在则建（/ideas 随手记命令）
└── docs/
    ├── CLAUDE.md             # 总规则（含 Owner Docs 职责）
    ├── context/              # ★ 新增：强制 AI 上下文
    │   ├── project-context.md       # 项目上下文、验证命令
    │   ├── ai-autonomy-policy.md   # AI 自主级别、受保护区域
    │   ├── codebase-map.md         # 代码库地图
    │   └── source-of-truth-and-precedence.md  # 真相优先级
    ├── ideas/
    │   └── README.md         # 灵感池（随手记，零结构）
    ├── research/
    │   └── README.md
    ├── prd/
    │   └── README.md
    ├── exec-plans/
    │   ├── README.md         # 含 Plan Audit + Closure Audit 要求
    │   ├── active/
    │   └── completed/
    │       └── tech-debt-tracker.md
    ├── handover/
    │   └── README.md
    ├── issues/               # Bug 追踪
    │   └── README.md
    └── lessons/
        └── README.md
```
项目根/
├── CLAUDE.md                 # 不存在则建（Linus 角色 + 沟通规范 + 通用开发规则模板）
├── AGENTS.md                 # 不存在则建（Codex CLI 全局指令）
├── MBTI_DEV_TRAPS.md         # 不存在则建（16 种人格陷阱清单）
├── karpathy-guidelines.md    # 不存在则建（LLM 编码行为指南）
├── ARCHITECTURE.md           # 不存在则用 Explore 子代理探索后生成
├── .mcp.json                 # 不存在则建（7 个常用 MCP 服务）
├── .claude/
│   └── commands/
│       └── ideas.md          # 不存在则建（/ideas 随手记命令）
└── docs/
    ├── CLAUDE.md             # 总规则
    ├── ideas/
    │   └── README.md         # 灵感池（随手记，零结构）
    ├── research/
    │   └── README.md
    ├── prd/
    │   └── README.md
    ├── exec-plans/
    │   ├── README.md
    │   ├── active/
    │   └── completed/
    │   └── tech-debt-tracker.md
    ├── handover/
    │   └── README.md
    ├── issues/               # Bug 追踪
    │   └── README.md
    └── lessons/
        └── README.md
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

**Step 0.4：确定文档根路径**
- 模式 A：`docs_root = ./docs`
- 模式 B：`docs_root = $DOCS_ROOT` 或 `./docs`（如果 docs 是独立仓库）

**Step 0.5：确定项目根路径**
- 模式 A：`project_root = ./`
- 模式 B：`project_root = ./`（项目代码根），文档引用路径 = `docs_root 相对于 project_root 的路径`

### 0.5. 主动询问确认（交互流程）

**Step 0.5.1：展示检测结果**

向用户展示当前检测到的配置：

```
📋 docs-pipeline 配置检测

📌 文档模式：模式 A（文档跟随项目）/ 模式 B（独立文档仓库）
📁 文档根路径：$docs_root
📂 项目根路径：$project_root
🔍 docs/ 状态：全新 / 部分存在 / 已齐全
📎 文档引用路径：$relative_path（项目根文件中引用 docs 的路径）
```

**Step 0.5.2：询问用户确认**

使用 `AskUserQuestion` 询问：

```
检测到以下配置，请确认或修改：

1. 文档模式：模式 A（文档跟随项目）/ 模式 B（独立文档仓库）
   - 模式 A：docs/ 在项目根目录下，与代码一起管理
   - 模式 B：docs/ 在独立仓库中，通过环境变量或自动检测

2. 文档根路径：$docs_root
   - 如需修改，请输入新路径

3. 是否跳过 ARCHITECTURE.md 生成？
   - 是：跳过自动探索生成
   - 否：调用 Explore 子代理基于项目代码生成

4. 是否跳过 Pensieve 集成？
   - 是：跳过 Pensieve 安装和配置
   - 否：检测并集成 Pensieve
```

**Step 0.5.3：处理用户输入**

| 用户选择 | 动作 |
|---------|------|
| 确认默认 | 继续执行 Step 1 |
| 修改模式 | 根据选择切换模式 A/B，更新 `docs_root` |
| 修改路径 | 使用用户输入的路径作为 `docs_root` |
| 跳过 ARCHITECTURE.md | 跳过 Step 7，报告中注明 |
| 跳过 Pensieve | 跳过 Pensieve 集成，报告中注明 |

**Step 0.5.4：记录配置**

将最终确认的配置写入报告头部：

```
📋 docs-pipeline 执行报告

📌 文档模式：模式 A/B（用户确认）
📁 文档根路径：$docs_root（用户确认/自动检测）
📂 项目根路径：$project_root
📎 文档引用路径：$relative_path
⏭️ 跳过项：ARCHITECTURE.md / Pensieve（如有）
```

### 1. 检测目标项目状态

先用 `Bash ls "$docs_root" 2>/dev/null || echo "MISSING"` 检测：

- 不存在 `docs/` → 全新初始化
- 存在 `docs/` 但缺部分目录/README → 修复模式
- 全部齐全 → 跳过，输出"已是规范结构"

### 2. 建目录

```bash
mkdir -p "$docs_root/context" "$docs_root/ideas" "$docs_root/research" "$docs_root/prd" "$docs_root/exec-plans/active" "$docs_root/exec-plans/completed" "$docs_root/handover" "$docs_root/issues" "$docs_root/lessons"
```

`mkdir -p` 本身是幂等的，已有目录不会报错。

**新增 `context/` 目录**：AGE 强制 AI 上下文层，包含 4 个模板文件。

### 3. 写入 docs/ 模板

模板位于本 skill 目录下 `assets/templates/`。对每个目标文件：

1. 用 `Read` 检测是否已存在
2. **不存在** → 用 `Read` 读取本 skill 下的模板，再用 `Write` 落地到目标路径
3. **已存在** → 跳过，记入"已存在跳过"清单

模板映射：

| 模板 | 目标路径 |
|------|---------|
| `assets/templates/docs-CLAUDE.md` | `$docs_root/CLAUDE.md` |
| `assets/templates/context/project-context.md` | `$docs_root/context/project-context.md` |
| `assets/templates/context/ai-autonomy-policy.md` | `$docs_root/context/ai-autonomy-policy.md` |
| `assets/templates/context/codebase-map.md` | `$docs_root/context/codebase-map.md` |
| `assets/templates/context/source-of-truth-and-precedence.md` | `$docs_root/context/source-of-truth-and-precedence.md` |
| `assets/templates/ideas-README.md` | `$docs_root/ideas/README.md` |
| `assets/templates/research-README.md` | `$docs_root/research/README.md` |
| `assets/templates/prd-README.md` | `$docs_root/prd/README.md` |
| `assets/templates/exec-plans-README.md` | `$docs_root/exec-plans/README.md` |
| `assets/templates/handover-README.md` | `$docs_root/handover/README.md` |
| `assets/templates/issues-README.md` | `$docs_root/issues/README.md` |
| `assets/templates/lessons-README.md` | `$docs_root/lessons/README.md` |

### 4. 写入项目根 AI 代理模板

同样的"已存在则跳过"策略，目标在项目根：

| 模板 | 目标路径 | 用途 |
|------|---------|------|
| `assets/templates/CLAUDE.md` | `CLAUDE.md` | 项目根 Claude 行为规范（Linus 角色 + 沟通规范 + 通用开发规则；含 TODO 占位让用户填项目特有部分） |
| `assets/templates/AGENTS.md` | `AGENTS.md` | Codex CLI 全局指令（含 AGE Task Routing + Planning Triggers + Verification Baseline） |
| `assets/templates/MBTI_DEV_TRAPS.md` | `MBTI_DEV_TRAPS.md` | 16 种 MBTI 人格的开发陷阱清单 |
| `assets/templates/karpathy-guidelines.md` | `karpathy-guidelines.md` | LLM 编码行为指南 |
| `assets/templates/mcp.json` | `.mcp.json` | 7 个常用 MCP 服务（playwright / thinking / chrome-devtools / fetch / time / context7 / serena），注意源文件名是 `mcp.json`，目标文件名是 `.mcp.json` |

注意：这五个文件**不属于** `docs/` 链路，是项目根级的 AI 代理配置文档。

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

Pensieve 集成按以下分支处理：

**分支 A — `.pensieve/` 已存在**：

1. 按 [references/pensieve-integration.md](./references/pensieve-integration.md) 执行 doctor → sync-instructions → .gitignore 保护 → doctor 验证流程
2. 检测 CLAUDE.md 是否已有 `## Pensieve 版本控制` 段落：`Bash grep -q "^## Pensieve 版本控制" CLAUDE.md`
   - 不存在 → 用 `Edit` 把 `assets/templates/pensieve-gitignore-snippet.md` 追加到文件末尾
   - 已存在 → 跳过

**分支 B — `.pensieve/` 不存在**：

1. 用 `AskUserQuestion` 询问用户是否要安装 Pensieve
2. 用户确认 → 按 [references/pensieve-integration.md](./references/pensieve-integration.md) 的"安装"章节执行（读取 GitHub 仓库最新 README 获取安装步骤，不要硬编码），然后走分支 A 的完整流程
3. 用户拒绝 → 跳过，报告"已跳过 Pensieve 集成"

### 7. 生成 ARCHITECTURE.md（探索型模板）

`ARCHITECTURE.md` 不能简单 cp，必须基于目标项目的实际代码生成。流程：

#### 7.1 检测

```bash
test -f ARCHITECTURE.md && echo "EXISTS" || echo "MISSING"
```

- **EXISTS** → 跳过，记入"已存在跳过"清单
- **MISSING** → 进入 7.2

#### 7.2 调用 Explore 子代理

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

#### 7.3 失败降级

如果 Explore 子代理失败（返回错误、超时、或未能写入文件），用 `Read` 读取 `assets/templates/ARCHITECTURE.md.template`，用 `Write` 落地为 `ARCHITECTURE.md`。在报告中标注"探索失败，已落地骨架，需手动填充"。

### 8. 输出报告

按以下格式向用户总结：

```
📋 docs-pipeline 执行报告

📌 模式：模式 A（文档跟随项目）/ 模式 B（独立文档仓库：$DOCS_ROOT）

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
```

## 关键原则

- **幂等**：重复调用应得到相同结果，已有文件不覆盖
- **不智能 merge**：冲突就报警，不自动合并
- **不删除**：只新建/跳过，从不删用户已有内容
- **不破坏**：项目根 CLAUDE.md 只追加，不修改原有内容
- **不假设技术栈**：只管文档与 AI 代理配置，不碰业务代码

## Gotchas

- **Explore 子代理超时或返回空内容**：不要卡住，直接降级到 `ARCHITECTURE.md.template` 骨架，报告"探索失败，需手动填充"
- **项目根 CLAUDE.md 已有大量自定义内容**：只追加"## 文档"段落到末尾，绝不修改或删除已有内容。用 `grep -q "^## 文档"` 检测，存在就跳过
- **重复调用后误报"已建"**：幂等检测必须用 `Read` 确认文件实际存在，不能靠 `mkdir -p` 的返回值推断
- **Pensieve 不存在时强制创建**：`.pensieve/` 不存在就跳过 Step 5，不要 `mkdir .pensieve/`
- **`.pensieve/state.md` 漏加 .gitignore**：state.md 是运行时状态，每次操作都变，必须排除。`.state/` 由 Pensieve 自带 `.gitignore` 排除，但 state.md 需要项目根 `.gitignore` 兜底
- **用户拒绝安装 Pensieve 却继续执行**：分支 B 中用户拒绝后必须跳过，不要自动创建 `.pensieve/` 或暗示 Pensieve 是必需的
- **sync-instructions 路由不覆盖 skill 调用**：`sync-instructions.sh` 只插入 `commit`/`git commit` 触发词，不覆盖 skill 调用场景。必须执行 Step 4 替换为"any commit-related skill invocation"通用模式，否则 Pensieve 在 skill 调用时不触发
- **模板里的 TODO 占位被自动填充**：`<!-- TODO(docs-pipeline): ... -->` 是留给用户的，不要替换
- **模式 B 路径引用错误**：独立文档仓库模式下，项目根 CLAUDE.md/AGENTS.md 中的文档引用必须是正确的相对路径。用 `realpath --relative-to=project_root docs_root` 计算
- **docs/ 目录既是独立 git 仓库又是项目子目录**：检测优先级 `DOCS_ROOT` > `docs/.git` 存在 > 默认 inline
- **交互询问被跳过**：如果用户明确说"直接执行"或"不要问我"，则跳过 Step 0.5 直接执行，报告中注明"用户要求跳过交互确认"
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
