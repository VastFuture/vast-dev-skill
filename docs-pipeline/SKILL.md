---
name: docs-pipeline
description: Initialize or repair docs/ pipeline + root AI agent templates (CLAUDE.md, AGENTS.md, etc.) for any Claude Code project. Idempotent. Use for: "初始化文档结构", "搭建 docs pipeline", "set up docs structure", "initialize docs pipeline", "fix docs structure".
metadata:
  author: tracker-system
  version: "1.2.0"
allowed-tools: Bash Read Write Edit Glob Agent
---

# Docs Pipeline Skill

一键初始化或修复 Claude Code 项目的 `docs/` 产物链路 + 项目根 AI 代理模板 + 自动探索生成的 `ARCHITECTURE.md`。

## 核心结构

```
项目根/
├── CLAUDE.md                 # 不存在则建（Linus 角色 + 沟通规范 + 通用开发规则模板）
├── AGENTS.md                 # 不存在则建（Codex CLI 全局指令）
├── MBTI_DEV_TRAPS.md         # 不存在则建（16 种人格陷阱清单）
├── karpathy-guidelines.md    # 不存在则建（LLM 编码行为指南）
├── ARCHITECTURE.md           # 不存在则用 Explore 子代理探索后生成
├── .mcp.json                 # 不存在则建（7 个常用 MCP 服务）
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
    ├── handover/
    │   └── README.md
    └── lessons/
        └── README.md
```

## 工作流

调用此 skill 时，按以下步骤执行：

### 1. 检测目标项目状态

目标项目默认为当前工作目录。先用 `Bash ls docs/ 2>/dev/null || echo "MISSING"` 检测：

- 不存在 `docs/` → 全新初始化
- 存在 `docs/` 但缺部分目录/README → 修复模式
- 全部齐全 → 跳过，输出"已是规范结构"

### 2. 建目录

```bash
mkdir -p docs/ideas docs/research docs/prd docs/exec-plans/active docs/exec-plans/completed docs/handover docs/lessons
```

`mkdir -p` 本身是幂等的，已有目录不会报错。

### 3. 写入 docs/ 模板

模板位于本 skill 目录下 `assets/templates/`。对每个目标文件：

1. 用 `Read` 检测是否已存在
2. **不存在** → 用 `Read` 读取本 skill 下的模板，再用 `Write` 落地到目标路径
3. **已存在** → 跳过，记入"已存在跳过"清单

模板映射：

| 模板 | 目标路径 |
|------|---------|
| `assets/templates/docs-CLAUDE.md` | `docs/CLAUDE.md` |
| `assets/templates/ideas-README.md` | `docs/ideas/README.md` |
| `assets/templates/research-README.md` | `docs/research/README.md` |
| `assets/templates/prd-README.md` | `docs/prd/README.md` |
| `assets/templates/exec-plans-README.md` | `docs/exec-plans/README.md` |
| `assets/templates/handover-README.md` | `docs/handover/README.md` |
| `assets/templates/lessons-README.md` | `docs/lessons/README.md` |

### 4. 写入项目根 AI 代理模板

同样的"已存在则跳过"策略，目标在项目根：

| 模板 | 目标路径 | 用途 |
|------|---------|------|
| `assets/templates/CLAUDE.md` | `CLAUDE.md` | 项目根 Claude 行为规范（Linus 角色 + 沟通规范 + 通用开发规则；含 TODO 占位让用户填项目特有部分） |
| `assets/templates/AGENTS.md` | `AGENTS.md` | Codex CLI 全局指令 |
| `assets/templates/MBTI_DEV_TRAPS.md` | `MBTI_DEV_TRAPS.md` | 16 种 MBTI 人格的开发陷阱清单 |
| `assets/templates/karpathy-guidelines.md` | `karpathy-guidelines.md` | LLM 编码行为指南 |
| `assets/templates/mcp.json` | `.mcp.json` | 7 个常用 MCP 服务（playwright / thinking / chrome-devtools / fetch / time / context7 / serena），注意源文件名是 `mcp.json`，目标文件名是 `.mcp.json` |

注意：这五个文件**不属于** `docs/` 链路，是项目根级的 AI 代理配置文档。

### 5. 处理项目根 CLAUDE.md 的"## 文档"段落

CLAUDE.md 的写入由 step 4 完成。本步只做一件事：如果 step 4 走的是"已存在跳过"分支（即用户已有自己的 CLAUDE.md），那么尝试追加"## 文档"段落，让用户的现有 CLAUDE.md 也能链接到 `docs/` 产物链路。

- **step 4 写入了完整模板** → 跳过本步（模板自带"## 文档"段落）
- **step 4 因为已存在跳过** → 进入下面的子流程：
  - 检测：`Bash grep -q "^## 文档" CLAUDE.md`
  - 不存在 → 用 `Edit` 把 `assets/templates/claude-md-snippet.md` 追加到文件末尾
  - 已存在 → 跳过，提示"已有文档段落，未变更"

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

### 6. 生成 ARCHITECTURE.md（探索型模板）

`ARCHITECTURE.md` 不能简单 cp，必须基于目标项目的实际代码生成。流程：

#### 6.1 检测

```bash
test -f ARCHITECTURE.md && echo "EXISTS" || echo "MISSING"
```

- **EXISTS** → 跳过，记入"已存在跳过"清单
- **MISSING** → 进入 6.2

#### 6.2 调用 Explore 子代理

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

#### 6.3 失败降级

如果 Explore 子代理失败（返回错误、超时、或未能写入文件），用 `Read` 读取 `assets/templates/ARCHITECTURE.md.template`，用 `Write` 落地为 `ARCHITECTURE.md`。在报告中标注"探索失败，已落地骨架，需手动填充"。

### 7. 输出报告

按以下格式向用户总结：

```
📋 docs-pipeline 执行报告

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

## 不要做

- ❌ 不要在模板里塞业务示例（保持骨架空白）
- ❌ 不要自动填充索引（让用户用着用着自己填）
- ❌ 不要做 `--reset` / `--uninstall`（用户手动决定）
- ❌ 不要假设项目用 Python/Node/Rust
- ❌ 不要修改项目根 CLAUDE.md 已有内容（只追加"## 文档"段落，不改其他）
- ❌ 不要覆盖已有的 CLAUDE.md / AGENTS.md / MBTI_DEV_TRAPS.md / karpathy-guidelines.md / .mcp.json / ARCHITECTURE.md（用户可能已有定制版本）
- ❌ 不要让 Explore 子代理偏离 5 章节固定结构（保持跨项目一致）
