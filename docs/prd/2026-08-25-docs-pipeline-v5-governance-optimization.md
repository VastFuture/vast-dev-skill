# PRD: docs-pipeline v5 文档治理闭环优化

> 文档编号：PRD-2026-08-25-001  
> 状态：Draft  
> 优先级：P0  
> Owner：docs-pipeline 维护者  
> 目标版本：v5.0.0  
> 最后更新：2026-08-25

## 1. 结论

`docs-pipeline` 当前应从“由 AI 按长篇说明临时拼装目录和模板”，升级为“由机器可读契约驱动安装、升级、校验和 CI 的文档治理工具”。

本次优化不以增加更多目录为目标。核心结构是：

```text
manifest
   ↓
installer
   ↓
generated docs + state
   ↓
validator
   ↓
CI / report
```

参考文档系统最值得吸收的精髓有六项：

1. 单一入口和渐进式路由。
2. 按问题类型定义唯一 Owner，而不是按文件外观分类。
3. 将设计意图与实现现实分开维护。
4. 从原始输入到验证关闭建立可追溯链路。
5. 将“缺少证据”建模为独立状态，不伪装成通过或失败。
6. 将文件所有权、安装副作用和可执行检查写成机器可读契约。

参考系统已经出现的目录膨胀、规则复制、手工索引漂移和“有指标无工具”等问题不得照搬。

## 2. 背景

### 2.1 当前产品定位

`docs-pipeline` 是面向 AI 辅助开发项目的文档系统初始化和治理 Skill。它应帮助团队快速建立：

- AI 启动上下文；
- 文档任务路由；
- 需求、设计、架构、规范和计划的 Owner 边界；
- 文档生命周期；
- 可验证、可升级、不可静默破坏的维护机制。

### 2.2 当前问题

当前实现已经有较完整的目录和模板，但真实行为由 `docs-pipeline/SKILL.md` 中 800 多行自然语言和 Shell 片段描述。测试脚本又复制了一套安装逻辑，而不是调用真实安装实现。

这形成了三份会独立漂移的“真相”：

1. `SKILL.md` 描述的预期行为；
2. `scripts/test-pipeline.sh` 模拟的行为；
3. 当前仓库 `docs/` 留下的历史行为。

直接后果包括：

| 问题 | 当前表现 | 用户风险 |
|------|----------|----------|
| 无单一安装实现 | Skill 和测试分别维护模板映射 | 测试通过也不能证明真实 Skill 可用 |
| Minimal 模式断裂 | 公共模板引用该模式未创建的目录 | 初始化后出现悬空链接和无效命令 |
| 独立仓库路径含糊 | `DOCS_ROOT` 同时像仓库根和内容根 | 文件可能写到错误层级 |
| 真相模型矛盾 | 设计文档和源代码都被描述为更高优先级 | AI 无法可靠裁决冲突 |
| “存在即跳过” | 旧模板永远不升级 | 修复、安全规则和迁移无法传播 |
| 同步检查脆弱 | 只看 `HEAD~1`，依赖 Java 文件名正则 | 漏掉工作区、多提交和其他技术栈变更 |
| 校验是假门禁 | 多个红叉只打印、不返回失败 | 用户得到虚假的成功报告 |
| 当前仓库未自用闭环 | `docs/` 与模板契约分叉 | 产品无法证明自己在真实项目中有效 |

### 2.3 参考系统研究结论

本 PRD 深入研究了以下文档系统：

`/home/fenghaolin/workspace/prj/develop/openai/human-resources/ai-dev-log/human-resources`

参考系统的关键设计证据：

| 设计 | 证据 | 提炼结论 |
|------|------|----------|
| 渐进式路由 | `docs/index.md:59-80` | 入口只路由，不复制 Owner 正文 |
| 目录 Owner | `docs/index.md:84-105` | 文档按“回答什么问题”归类 |
| 意图/现实分离 | `docs/design/README.md:21-38` | 历史设计与当前事实必须采用不同维护策略 |
| 变更触发映射 | `docs/design/README.md:82-100` | 代码变化应映射到具体 Owner 文档 |
| 输入到关闭闭环 | `docs/meta/documentation-system-guide.md:80-103` | 文档系统应管理完整生命周期，不只负责初始化 |
| 计划关闭门禁 | `docs/agent-guides/plan-mode.md:70-95` | “写完代码”不等于完成，必须有验证和关闭证据 |
| 维护预算 | `docs/index.md:109-115` | 新目录和长期文档必须付出明确维护成本 |

参考系统同时证明了以下反模式不能复制：

- 手工 README 表格承担状态数据库，最终发生漏项、重复和错分区；
- 同一规则复制到多个元文档，更新一个规则需要同步多处；
- 声称 100% 路由覆盖和索引同步，但没有自动检查；
- 用一条线性优先级混合“当前事实、目标要求、工程约束和执行计划”；
- 自动生成的巨型根级 `ARCHITECTURE.md` 很快因具体数量和配置变化而过时。

### 2.4 第二批参考项目校正

本 PRD 进一步研究了三个固定版本的本地参考项目：

| 项目 | 版本 | 主要价值 | 主要反例 |
|------|------|----------|----------|
| `attractor-guided-engineering-template` | `8c1eeb95a0ce71ed7f4a82cb27c6080002b794c6`（`v1.2.0` 后 27 个提交） | 显式安装白名单、consumer/dogfood 所有权边界、运行状态和崩溃对账 | “文件存在即跳过”、清单外副作用、缺少安装账本和事务升级 |
| `better-harness` | `8292495b1951e90a88bd18aa88db7702e71dbcab`（package version `0.6.4`；`v0.6.4` 后 77 个提交） | 能力切片、证据状态、冻结上下文、结构化验证、Stage → Validate → Publish | 多重声明面、正则驱动质量检查、设计中的恢复能力强于实际实现 |
| `ddd-harness-microservices` | `e2a1fc64bb489f5f1f8d474829ee83e438be236e` | 需求/规范/设计/计划分区、变更影响映射、真实集成测试样板 | API、数据库、字典、安全文档与代码漂移；文字规则缺少 CI 执行 |

第二批证据没有推翻 v5 的主结构，但收紧了四项契约：

1. Manifest 必须描述安装产生的全部持久副作用，不能只列模板复制。
2. Validator 必须区分 `pass`、`fail`、`unobserved` 和 `blocked`；未运行检查不能显示绿色。
3. 技术栈 Profile 必须声明独立能力及其可执行检查，不能只注入语言或框架教条。
4. Dogfood 不能只验证当前文件树；还必须验证消费者安装和上一版本升级路径。

本 PRD 不吸收 mission-driver 的完整任务编排、配额等待和多 Agent 恢复模型。docs-pipeline v5 Core 是本地文件治理工具，只有文件事务、安装状态、证据和崩溃恢复与其真实问题直接相关。

## 3. 产品目标

### 3.1 Goals

1. 建立一个机器可读 Manifest，成为模式、目录、模板和目标路径的唯一契约。
2. 建立一个真实 Installer，所有安装、修复、升级和测试共用该实现。
3. 建立一个 Validator，自动检查结构、链接、占位符、状态和 Owner 映射。
4. 明确当前事实、目标要求、工程约束和执行计划各自的 Owner，消除单线真相优先级。
5. 支持新项目初始化、既有项目无损接入、模板升级和跨版本迁移。
6. 让 Minimal 和 Standard 都成为内部完整、无悬空引用的可用产品。
7. 让当前仓库成为 docs-pipeline 的 dogfood 项目，持续验证真实升级路径。

### 3.2 Non-Goals

- 不把参考项目的全部目录复制到所有项目。
- 不在 v5.0 强制引入 MkDocs、Docusaurus 或文档发布网站。
- 不自动覆盖用户修改过的文档正文。
- 不自动删除或移动未知文件。
- 不用 AI 猜测数据库、API 或生产环境的真实状态。
- 不在第一阶段实现任意技术栈的完整语义代码分析。
- 不把 Pensieve、MCP 配置或人格提示作为核心安装的强依赖。

## 4. 用户与场景

| 用户 | 核心任务 | 成功结果 |
|------|----------|----------|
| 初学者/个人开发者 | 快速初始化最小文档链路 | 5 分钟内理解结构，无失效入口 |
| 团队维护者 | 建立标准文档治理 | Owner、生命周期和验证门禁明确 |
| AI Agent | 判断先读什么、该写哪里 | 只加载必要上下文，不误读历史文档 |
| Skill 维护者 | 修改模板或发布新版本 | 改一处契约，安装器和测试自动一致 |
| 既有项目负责人 | 升级旧版 docs-pipeline | 先看到 diff，不丢用户内容，可回滚 |
| 多仓库项目负责人 | 把代码和文档分仓维护 | 路径语义唯一，跨仓引用可验证 |

## 5. 核心产品原则

### 5.1 路由不拥有事实

根 `CLAUDE.md`、`AGENTS.md` 和 `docs/index.md` 只保留：

- 不可丢失的硬门禁；
- 默认阅读链；
- 任务到 Owner 的路由；
- 冲突时的裁决入口。

API、数据库、业务规则和具体架构不得复制到入口文件。

### 5.2 Owner 按问题定义

同一个功能可以出现在多类文档中，但每个问题只能有一个 Owner：

| 问题 | Owner |
|------|-------|
| 用户为什么需要、验收什么 | `prd/` |
| 编码前打算怎么实现 | `design/intent/` |
| 当前系统对外实际表现 | `design/reality/`（源代码、契约测试和运行结果是首要证据） |
| 系统内部模块如何组织 | `architecture/` |
| 代码必须遵守什么规则 | `standards/` |
| 本次按什么顺序执行 | `plans/` |
| 为什么当时这样决定 | `decisions/`、`discussions/` 或 `handover/` |
| 最近实际做了什么 | `logs/` |

### 5.3 当前事实与目标要求分域裁决

废弃全局线性“真相优先级”，改为问题域矩阵：

| 事实域 | 首要证据 | 文档冲突时动作 |
|--------|----------|----------------|
| 生产运行事实 | 生产配置、真实数据库、可观测结果 | 更新低层概览，不用文档覆盖生产事实 |
| 当前实现事实 | 源代码、可执行测试、生成契约 | 更新 `design/reality/`，必要时登记 drift |
| 已批准目标 | 已批准 PRD/Decision | 代码未实现时明确标记 gap，不伪装成现状 |
| 技术边界 | Architecture/ADR | 实现冲突时停止并要求架构裁决 |
| 工程规则 | Standards | Plan 和代码都不得静默绕过 |
| 本次执行 | Active Plan | 只约束本次范围，不重定义上层事实 |
| 历史原因 | Discussion/Log/Handover | 仅作证据，不覆盖当前 Owner |

### 5.4 历史和现实采用不同更新策略

- `design/reality/`：覆盖更新，目标是反映当前事实。
- `logs/`、`discussions/`、`handover/`：追加或保留，目标是保存当时语境。
- `design/intent/`：允许被现实超越，但必须能追到对应结果或 superseded 文档。

### 5.5 规则必须有机械执行能力

没有 Validator 或 CI 的规则只能标为“建议”，不能写成“强制 100%”。

强制规则必须至少满足一种条件：

- Installer 保证；
- Validator 检查；
- CI 阻断；
- 有明确人工 Owner 和可审计证据。

## 6. 信息架构

### 6.1 固定核心与按需能力

v5 不再用一个超大模板描述所有项目。所有可安装单元统一称为 Capability；`minimal` 和 `standard` 只是 Capability 预设集合，不是第三种分类。

#### `core` Capability：所有模式必须完整提供

```text
docs/
├── index.md
├── context/
│   ├── project-context.md
│   ├── autonomy.md
│   ├── codebase.md
│   └── source-of-truth.md
├── backlog/
├── prd/
├── plans/
│   ├── active/
│   └── completed/
└── lessons/
```

Core 只解决：理解项目、选择任务、定义需求、计划执行、沉淀教训。

#### Standard 预设默认 Capability

```text
docs/
├── design/
│   ├── intent/
│   └── reality/
├── architecture/
├── standards/
├── issues/
├── logs/
└── handover/
```

#### 其他按需 Capability

| Capability | 激活信号 | 默认行为 |
|------------|----------|----------|
| `input` | 存在外部 PM 素材、截图、会议记录 | 不默认创建 |
| `discussions` | 需求经常需要多轮澄清 | 不默认创建 |
| `decisions` | 已有 3 个以上跨期技术/产品决策 | 不默认创建 |
| `help-center` | 项目需要面向业务用户的操作文档 | 不默认创建 |
| `research` | 有稳定调研产物，而非临时搜索 | 不默认创建 |
| `skills` | 项目维护专有 Agent Skill | 不默认创建 |
| `ideas` | 团队明确需要低结构灵感入口 | 不默认创建；激活后才安装 `/ideas` |
| `mcp` | 用户明确要求安装项目级 MCP 配置 | 不默认创建；不得覆盖已有 `.mcp.json` |

新增目录的默认门槛：同类长期文件稳定达到 5 个，或现有 Owner 已发生 3 次以上边界冲突。Manifest 可以显式覆盖该建议。

### 6.2 命名决策

v5 将正式执行计划目录统一为 `docs/plans/`。

原因：

- 参考系统和当前多数文档都使用 `plans/`；
- `exec-plans/` 没有提供额外语义，反而制造引用迁移成本；
- “计划”本身已通过 README 和状态目录限定为执行计划。

兼容策略：

- 新项目只生成 `plans/`；
- 旧项目检测到 `exec-plans/` 时只报告迁移，不自动移动；
- `migrate` 子命令在用户确认后移动并更新引用；
- 不长期同时维护两个目录。

### 6.3 元数据与分类型状态模型

需要治理的长期 Markdown 文档使用统一基础 Frontmatter：

```yaml
---
id: prd-2026-08-25-docs-pipeline-v5
type: prd
status: draft
owner: docs-pipeline-maintainers
created: 2026-08-25
last-verified: 2026-08-25
supersedes: []
superseded-by: null
sources: []
related: []
---
```

状态不强行统一。Validator 根据 `type` 使用不同 Schema：

| Type | 允许状态 |
|------|----------|
| `prd` | `draft`, `approved`, `rejected`, `superseded` |
| `plan` | `planned`, `active`, `completed`, `cancelled`, `superseded` |
| `issue` | `open`, `investigating`, `resolved`, `wont-fix`, `superseded` |
| `decision` | `proposed`, `accepted`, `rejected`, `superseded` |
| `standard`, `architecture` | `active`, `deprecated`, `superseded` |
| `reality` | `current`, `stale`, `superseded` |

`README.md`、`index.md`、模板、每日 Log、`api.yaml`、SQL、图片和图表不强制使用该 Frontmatter；它们由各自的文件类型规则校验。对需要状态的文档，Frontmatter 是唯一机器真源，目录位置只是工作视图，README 索引由工具生成或校验，不再手工复制状态。

## 7. 功能需求

### FR-01：机器可读 Manifest

新增 `docs-pipeline/manifest.yaml`，至少描述：

- 产品版本；
- 安装模式；
- Capability；
- 模板 ID、源路径、目标路径；
- 模板适用模式；
- 目标文件所有权策略；
- 必需目录；
- 允许的链接目标；
- 技术栈 Profile；
- 迁移规则 ID。
- 安装动作类型及其全部持久副作用。

示例：

```yaml
version: 5.0.0

modes:
  minimal:
    capabilities: [core]
  standard:
    capabilities: [core, design, architecture, standards, issues, logs, handover]

templates:
  - id: docs-index-minimal
    source: assets/templates/minimal/docs-index.md
    target: docs/index.md
    modes: [minimal]
    strategy: create-only
  - id: docs-index-standard
    source: assets/templates/standard/docs-index.md
    target: docs/index.md
    modes: [standard]
    strategy: managed-file

actions:
  - id: ensure-docs-directory
    type: ensure-directory
    target: docs
  - id: ignore-runtime-state
    type: ensure-line
    target: .gitignore
    value: .docs-pipeline/runtime/
```

约束：目录数量、模板数量、测试预期和 README 模式表都必须从 Manifest 计算，不再手写重复数字。

Manifest 是安装结果的完整声明，不只是文件复制清单。它声明允许的持久路径模式和动作类型；run ID、事务 ID 等动态实例由每次运行的 Action Plan 展开。Installer 的所有持久写入必须经过唯一 Write Gateway，禁止业务代码直接调用文件写 API。Gateway 记录动作 ID、路径、动作类型、写入前后 Hash 和临时/持久生命周期；Action Plan 与实际 trace 必须一一对应。State、基线和事务日志由 Manifest 声明允许的路径模式管理，不要求静态枚举每个动态文件名。

允许的动作类型必须由 Schema 枚举；未知动作、重复目标、必需源缺失、目标越界和符号链接逃逸必须在任何写入前失败。可选源必须显式声明 `required: false`，缺失时进入结构化报告。临时文件也必须通过 Gateway 创建，并声明清理时点，但不计入最终安装树。

目标所有权策略必须使用以下固定语义：

| 策略 | 创建 | 升级 | 用户修改 | 删除 |
|------|------|------|----------|------|
| `create-only` | 缺失时创建 | 不升级 | 永不覆盖 | 永不自动删除 |
| `managed-file` | 缺失时创建 | 基线未修改时可升级 | 冲突并停止 | 仅显式迁移 |
| `managed-block` | 插入带稳定 ID 的区块 | 只更新受管区块 | 区块内冲突并停止 | 只在显式操作中移除区块 |
| `generated` | 工具完整生成 | 可重建 | 检测到手改时报错 | 可由 repair 重建 |

模板变量替换、换行符和编码规范化发生在计算基线 Hash 之前。`repair` 只能重建 `generated` 文件或缺失且未经弃用的受管理目标；Capability 关闭时只报告遗留文件，不自动删除。

`managed-block` 使用稳定且全局唯一的起止标记。State 按 block ID 保存目标路径、规范化基线内容 Hash 和边界 Hash。标记缺失、顺序错误、重复 ID、嵌套或边界被修改时必须停止；区块外移动但边界和内容均完整时允许定位，区块内用户修改按基线三方比较处理。

### FR-02：单一 Installer

新增真实安装器，例如 `docs-pipeline/scripts/docs_pipeline.py`：

```text
docs_pipeline.py init
docs_pipeline.py check
docs_pipeline.py repair
docs_pipeline.py upgrade
docs_pipeline.py adopt
docs_pipeline.py take-over --target <template-id|path|all>
docs_pipeline.py migrate
docs_pipeline.py migrate --resume <transaction-id>
docs_pipeline.py migrate --rollback <transaction-id>
```

通用参数：

```text
--project-root <path>
--docs-root <path>
--mode minimal|standard
--capability <name>
--dry-run
--apply
--format text|json
--non-interactive
```

要求：

1. `SKILL.md` 只负责交互、收集参数和调用 Installer。
2. 测试直接调用 Installer，不允许复制安装逻辑。
3. 所有路径使用规范化绝对路径计算，支持空格和非 ASCII 路径。
4. 错误必须返回非零退出码和稳定错误码。
5. 默认只预览，不写入；`--apply` 才允许写入。
6. 交互模式下，`--apply` 在写入前显示计划并要求确认；`--non-interactive --apply` 表示调用方已授权安全写入，但冲突仍必须停止。
7. `--non-interactive` 且没有 `--apply` 时只输出预览，不提示。
8. Dry-run 发现普通待变更项返回 0，发现契约错误或不可安全处理的冲突返回非零；`init`、`repair`、`upgrade`、`adopt`、`take-over`、`migrate` 使用同一语义。
9. `take-over --target all` 仍需输出逐文件清单；只接管用户明确选择的目标。`resume/rollback` 必须引用现存事务 ID，不允许猜测最近事务。

### FR-03：明确项目根和文档根

废弃含糊的 `DOCS_ROOT=/path/to/docs/repo` 表达。

统一定义：

- `project_root`：代码项目根；
- `docs_content_root`：最终包含 `index.md` 的文档目录。

推荐 CLI：

```bash
# 文档跟随项目
docs_pipeline.py init --project-root . --docs-root ./docs

# 独立文档仓库
docs_pipeline.py init \
  --project-root /path/to/code \
  --docs-root /path/to/docs-repo/docs
```

工具不得猜测 `docs_root` 是否还要再拼一层 `docs/`。

### FR-04：安装状态和升级

新增 `.docs-pipeline-state.json`，记录：

```json
{
  "version": "5.0.0",
  "mode": "standard",
  "stateOwnerRepoId": "git:<docs-containing-repo-id>",
  "codeRepoId": "git:<code-repo-id>",
  "docsRoot": "docs",
  "manifestHash": "...",
  "templates": {
    "docs-index-standard": {
      "target": "docs/index.md",
      "installedHash": "...",
      "sourceHash": "...",
      "baseTemplateVersion": "5.0.0",
      "baseTemplateId": "docs-index-standard"
    }
  }
}
```

State 只有一份可写权威副本，保存在实际包含受管 docs 内容的 Git 仓库根。Inline 模式下它就是代码项目根；Separate-repo 模式下它位于文档仓库根，代码仓库不保存第二份可写 State。CLI 通过显式 `--docs-root` 定位文档仓，再用该仓 Git root 和 canonical remote（无 remote 时使用持久生成 ID）校验 `stateOwnerRepoId`；仓库 ID 不匹配必须停止。

State 只保存仓库身份和仓内相对路径，不保存机器相关绝对路径。Separate-repo State 的 `codeRepoId` 只是只读关联元数据，模板 Hash、基线快照和文件所有权全部只由文档仓 State 管理。工具发行包必须保留所有仍受支持版本的规范化模板基线，或将安装时的规范化基线快照保存在文档仓根的 `.docs-pipeline/baselines/`。三方 diff 的三方固定为：安装基线、当前用户文件、新模板。只有 Hash 没有可恢复基线时，不得声称支持三方 diff。

旧项目执行 `adopt` 时没有可信安装基线，文件必须记录为 `ownership: unknown`，不得因为当前 Hash 与 Adopt Hash 相同就推断“用户未修改”。Adopt 只输出两方差异和接管候选；用户显式执行逐文件或按策略的 `take-over` 后，该文件才转为受管理状态，并以接管时内容建立基线。从 Take-over 后的下一次升级开始才支持三方 diff。未 Take-over 的文件始终不允许整文件升级。基线快照不得包含密钥，且必须纳入大小上限和清理策略。

升级分类：

| 状态 | 行为 |
|------|------|
| 目标未被用户修改 | 可在确认后安全升级 |
| 目标被用户修改 | 输出三方 diff，不覆盖 |
| 新模板 | 创建 |
| 模板已废弃 | 标记 deprecated，不自动删除 |
| 路径需要迁移 | 进入显式 migration |
| 状态文件缺失的旧项目 | 先运行 Adopt，记录当前快照和 `ownership: unknown`；不生成历史安装基线 |

### FR-05：Validator

Phase 1 的最小 Validator 必须执行以下稳定检查 ID；这些检查均为 blocking：

1. `VAL-MANIFEST-SCHEMA`：Manifest Schema；
2. `VAL-TEMPLATE-SOURCES`：模板源存在性和目标唯一性；
3. `VAL-MODE-COMPLETE`：模式输出完整性；
4. `VAL-MARKDOWN-LINKS`：Markdown 相对链接；
5. `VAL-ROOT-ROUTES`：根入口引用路径；
6. `VAL-CAPABILITY-BOUNDARY`：Minimal 不引用未安装 Capability；
7. `VAL-ACTION-BOUNDARY`：动作类型、目标唯一性、必需源、Write Gateway trace 和目标路径边界。

Phase 3 在最小 Validator 上增加以下稳定检查 ID；除特别说明外均为 blocking：

1. `VAL-FRONTMATTER-SCHEMA`：分类型 Frontmatter Schema；
2. `VAL-PLACEHOLDERS`：未替换占位符；
3. `VAL-INDEX-CONSISTENCY`：目录 README 与实际文件一致性；
4. `VAL-PLAN-LIFECYCLE`：`plans/active` 和 `plans/completed` 生命周期一致性；
5. `VAL-SUPERSEDED-LINKS`：`superseded-by` 双向引用；
6. `VAL-RUNTIME-POLLUTION`：隐藏运行时目录和敏感文件污染。

Manifest 为每项检查声明稳定 ID、适用模式和 `blocking: true|false`。每项检查必须分别记录执行结论和问题严重度。执行结论固定为：

- `pass`：检查已执行，证据支持预期；
- `fail`：检查已执行，证据反驳预期；
- `unobserved`：当前环境未取得足够证据；
- `blocked`：权限、配置或依赖导致检查无法开始。

问题严重度固定为：

- Error：结构或契约错误，退出码非零；
- Warning：可能漂移，但无法机械证明；
- Info：建议和统计。

`unobserved` 不等于 `pass`。单项 verdict、聚合 run verdict 和进程退出码是三个独立字段。任何 blocking 检查为 `fail`、`unobserved` 或 `blocked` 时均不放行且退出码非零，但聚合 verdict 保留根因：存在 `blocked` 时为 `blocked`，否则存在 `unobserved` 时为 `unobserved`，只有证据反驳断言时才为 `fail`。非阻断检查未通过时聚合 verdict 为 `partial`，并列出缺失证据和恢复条件。测试数量为 0、全部 skipped、命令未执行或检查器不可用均不得作为正向证据。

### FR-06：变更影响矩阵

将当前硬编码 Java 文件名正则替换为可配置影响矩阵：

```yaml
profiles:
  generic:
    impacts:
      api:
        code: ["**/routes/**", "**/controllers/**", "**/*Controller.*"]
        docs: ["docs/design/reality/api.*"]
      database:
        code: ["**/migrations/**", "**/*.sql", "**/schema.*"]
        docs: ["docs/design/reality/db.md", "docs/design/reality/tables.sql"]
```

检查范围必须包含：

- 指定 base 到 HEAD 的全部提交；
- staged 变更；
- unstaged 变更；
- untracked 但纳入检查范围的文件。

第一阶段只做“受影响 Owner 文档是否同一变更集中更新”的确定性检查，不声称能证明文档内容正确。

该强门禁在 v5.0 仅适用于代码与文档位于同一 Git 仓库的 Inline 模式。Separate-repo 模式不存在天然的“同一变更集”，v5.0 只提供路径、安装、升级和各仓独立校验，影响检查降级为 Warning。

Separate-repo 的跨仓强门禁属于后续 Capability，必须通过显式 Integration Descriptor 定义代码仓库 ID、文档仓库 ID、base ref、关联 PR/commit 元数据和 CI 获取方式；在该契约落地前不得声称跨仓变更已同步。

### FR-07：Intent 与 Reality

Standard 模式默认生成：

```text
docs/design/
├── README.md
├── intent/
└── reality/
```

`design/README.md` 必须明确：

- `intent/` 是编码前设计和历史方案；
- `reality/` 是当前应用行为和功能语义；
- `architecture/` 负责内部技术结构；
- `prd/` 负责目标和验收；
- 每个 Reality 文件必须声明其首要证据和更新触发器。

不再把 `api.yaml`、`db.md` 等当前事实文件直接放在 `design/` 根目录。

### FR-08：模板边界

PRD 模板只回答：

- 背景和问题；
- 用户；
- 目标和非目标；
- 用户故事；
- 功能和非功能需求；
- 验收标准；
- 风险和发布约束。

PRD 模板不得要求具体表字段、SQL、类名和实现步骤。

Plan 模板必须包含：

- Current Baseline；
- Goals / Non-Goals；
- Owner Docs；
- 分阶段任务；
- 每阶段 Exit Criteria；
- 验证命令；
- 回滚方式；
- Plan Audit；
- Closure Gates；
- 独立 Closure Audit 证据。

### FR-09：技术栈 Profile

根 `AGENTS.md` 只安装技术栈无关的规则。

技术栈规则按 Profile 选择：

```text
generic
node
python
go
rust
java
```

无法可靠识别时只安装 `generic`。不得把 Java/Spring 的 `BusinessException`、DTO/Assembler 等约束作为所有项目默认规则。

Profile 不是规则文本包，而是版本化能力声明。`available` 表示声明的输入范围已由指定检查器和未过期 receipt 完整验证；`partial` 表示已明确列出未覆盖输入或平台；`unavailable` 表示没有可执行检查，不得包含 validator。每项能力绑定检查器、输入范围、证据类型、验证 receipt 和有效期。例如：

```yaml
profiles:
  java-spring:
    version: 1
    checks:
      docs-links:
        availability: available
        validator: markdown-links
        inputs: ["docs/**/*.md"]
        evidence: ci-receipt:generic-docs-links-v1
        verified-version: 5.0.0
        evidence-valid-until: 2026-12-31
      api-contract:
        availability: partial
        validator: openapi-diff
        inputs: ["src/**/controllers/**"]
        evidence: fixture-receipt:spring-routes-v1
        verified-version: 5.0.0
        evidence-valid-until: 2026-10-31
        limitations: [framework-route-extraction-not-complete]
      architecture-boundaries:
        availability: unavailable
```

Profile 不得因为能发现某技术栈就宣称所有检查可用，也不得在不支持时借用其他 Profile 的规则伪造成功。v5.0 Core 只要求 `generic` 的确定性文档检查；API、数据库、架构和安全语义检查作为后续独立 Capability 演进。

### FR-10：Architecture 输出

根 `ARCHITECTURE.md` 改为稳定、短小的架构入口，建议不超过 150 行，只包含：

- 系统目的；
- 稳定边界；
- 顶层组件；
- 关键入口；
- 构建、测试、运行命令；
- 指向 `docs/architecture/` 和 `docs/design/reality/` 的链接；
- 最后验证日期和证据。

易漂移的端点数量、表数量、具体模型名和环境地址不进入根架构入口。自动探索只能生成候选草稿，不能把推测标成事实。

### FR-11：报告

所有操作同时支持人类文本和 JSON 报告，至少包含：

- run ID；
- 工具版本；
- 模式和 Capability；
- 项目根、文档根；
- Manifest Hash；
- created / updated / skipped / conflicted / deprecated 列表；
- errors / warnings；
- 每项检查的 `pass/fail/unobserved/blocked`、证据引用和限制；
- 下一步；
- 是否发生写入。

机器模式的标准输出必须是单个可解析 JSON 文档，诊断信息写入标准错误。报告不得把“命令已启动”“文件存在”或“未发现错误”提升为更强的执行证据。

### FR-12：CI

仓库 CI 至少执行：

```bash
python docs-pipeline/scripts/docs_pipeline.py check --project-root . --docs-root docs
python -m pytest docs-pipeline/tests
```

CI 必须在以下情况失败：

- Manifest 无效；
- 模式生成物缺文件或有悬空链接；
- 模板引用不存在；
- 测试出现失败断言；
- 临时运行状态进入模板包；
- 当前仓库受管理文件与状态记录发生未解释漂移。

### FR-13：可选集成解耦

- Pensieve 不再由核心流程安装或询问；
- `.mcp.json` 改为显式 Capability，默认不写入；
- `/ideas` 只在安装 `ideas` Capability 时创建；
- 人格和写作风格文档不属于 docs-pipeline Core；
- 第三方集成必须有独立入口、权限说明和失败隔离。

### FR-14：迁移事务与崩溃恢复

迁移不能只备份状态文件。`migrate --apply` 必须执行文件级事务：

1. 扫描并生成完整操作计划；
2. 在项目同一文件系统的临时事务目录保存每个将被修改、移动或删除的文件原文；
3. 生成所有目标文件和引用更新后的候选树；
4. 对候选树运行 Validator；
5. 写入包含操作序号、before/after Hash 和 commit point 的事务日志后，用原子替换逐项应用；
6. 对已提交结果再次运行 Validator，成功后写入新 State，再清理事务目录；
7. 任一步失败时按事务日志逆序恢复全部用户文件；
8. 进程中断后，下次运行必须检测未完成事务；默认只允许 `rollback`。只有日志能证明下一动作尚未应用、输入 Hash 未变化且动作可幂等重放时，才允许显式 `resume`。

跨文件系统移动不具备原子重命名条件，必须使用“复制到目标文件系统的 staging → 校验 → 切换 → 删除源”的显式流程；切换前不得删除源文件。测试必须覆盖应用中途失败和进程中断恢复。

## 8. 非功能需求

| 类别 | 要求 |
|------|------|
| 幂等 | 相同版本、相同参数、无用户改动时，第二次执行必须字节级无变化 |
| 安全 | 默认 dry-run；不自动覆盖用户修改；不自动删除未知文件 |
| 可移植 | Linux/macOS；路径含空格和中文；不依赖当前工作目录猜路径 |
| 可测试 | 所有核心行为可通过 Installer 的公开 CLI 测试 |
| 可解释 | 每个变更和冲突必须给出稳定原因码 |
| 性能 | 1,000 个文档以内的结构检查在普通开发机目标 5 秒内完成，不含外部链接网络检查 |
| 可维护 | 模式、文件映射和数量只在 Manifest 定义一次 |
| 兼容 | 旧项目默认只诊断；任何路径迁移需用户确认 |
| 资源清理 | 测试临时目录默认通过 `trap` 或测试夹具清理，显式保留时才不删除 |

## 9. 迁移策略

### 9.1 迁移原则

1. Never break userspace：v4 项目不会因安装 v5 自动搬家或覆盖。
2. 先 Adopt，后 Upgrade：先识别现状和用户修改，再决定接管哪些文件。
3. 路径迁移必须原子化：移动文件、更新引用、校验链接要么全部成功，要么不写入。
4. 历史文档不删除：增加 `superseded` 元数据和替代指针。
5. 出现不确定冲突时停止，不自动猜。

### 9.2 v4 到 v5

迁移流程：

```text
scan
  → classify managed/unmanaged/modified
  → generate migration report
  → user approval
  → stage candidate tree + backup affected files
  → validate candidate tree
  → write transaction journal
  → atomically apply path and template migration
  → validate committed result
  → commit state and cleanup, or rollback on failure
```

重点迁移：

| v4 状态 | v5 目标 | 默认动作 |
|---------|---------|----------|
| `exec-plans/` | `plans/` | 只报告；确认后移动并更新引用 |
| `design/*.md` | `design/reality/` | 按文件证据类型建议迁移，不自动判断业务语义 |
| `design/` 历史方案 | `design/intent/` | 需要用户确认 |
| 根级大型 `ARCHITECTURE.md` | 短入口 + `docs/architecture/` | 生成候选 diff，不覆盖 |
| 手工 README 状态表 | Frontmatter + 生成索引 | 先解析和报告无法识别项 |
| 旧 Agent guides | Core 或可选 Profile | 未被入口引用的文件标记候选移除 |
| 旧模板文件 | v5 受管理模板 | 未 Take-over 时只做两方 diff；Take-over 后的下一版本升级才做三方 diff |

## 10. 实施阶段

### Phase 0：冻结契约和修复确定性错误

目标：停止继续扩大漂移。

- 明确 `project_root` 和 `docs_root` 语义；
- 决定新项目统一使用 `plans/`；
- 修复不存在的 `docs/CLAUDE.md`、`requirements/` 和错误 Agent guide 引用；
- Minimal 暂时标为 experimental，直到拥有独立完整模板；
- 从核心流程移除 Pensieve 和默认 MCP 写入；
- 同步版本号单一来源。

Exit Criteria：

- 所有当前模板内部链接可通过检查；
- 文档中不再存在互相冲突的根路径定义；
- 不再新增手工模板映射。

### Phase 1：Manifest + Installer

目标：建立单一执行真相。

- 定义 Manifest Schema；
- 实现 `init/check/repair`，其中 `check` 包含 Manifest、模板、模式完整性和内部链接的最小 Validator；
- 支持 Minimal 和 Standard 的独立输出；
- 支持 dry-run 和 JSON 报告；
- 将现有测试改为调用 Installer。

Exit Criteria：

- Fresh minimal/standard 均通过结构和链接校验；
- 第二次运行字节级不变；
- 测试不再包含模板复制实现。

### Phase 2：State + Adopt + 安全升级基线

目标：先建立既有项目接管所需的数据结构，再要求当前仓库 Dogfood。

- 实现 State、基线快照和所有权策略；
- 实现旧项目 Adopt；
- 实现显式 Take-over；Adopt 文件默认保持 `ownership: unknown`；
- 实现用户修改检测和两方/三方 diff 的明确降级规则；
- 实现最小安全 Upgrade，不包含路径迁移。

Exit Criteria：

- 用户修改过的模板不会被覆盖；
- Adopt 项目明确标识 `ownership: unknown`，不得自动覆盖；
- 使用固定、只读并带 checksum 的 `v5.0.0 → v5.0.1-fixture` 模板验证：Take-over 后升级可生成真实三方 diff；
- Separate-repo 仅由文档仓 State 管理，传入仓库身份不匹配时失败。

### Phase 3：Validator + CI + Dogfood

目标：把规则从愿望变成门禁。

- 在 Phase 1 最小 Validator 上增加 Frontmatter、占位符、生命周期、污染和索引检查；
- 增加 GitHub Actions 或仓库实际 CI；
- 测试失败返回非零；
- 默认清理临时资源。

Exit Criteria：

- 人为制造坏链接、缺模板、状态冲突时 CI 必须失败；
- 空仓安装、消费者 fixture、固定上一版本 fixture 和当前仓库 Dogfood 四类 CI 场景均通过。

### Phase 4：Migration

目标：安全服务既有项目。

- v4 → v5 migration；
- 文件事务、崩溃恢复和冲突报告。

Exit Criteria：

- 用户修改过的模板不会被覆盖；
- `exec-plans/ → plans/` 迁移后所有仓库内引用有效；
- 迁移失败可回到写入前状态。

### Phase 5：变更影响和成熟治理

目标：让文档持续跟上代码，而非只在初始化时正确。

- 可配置影响矩阵；
- base...HEAD + 工作区检查；
- Owner 文档同变更集门禁；
- freshness 和 superseded 检查；
- 可选文档预览和健康报告。

Exit Criteria：

- API/Schema 示例变更可稳定触发对应 Owner 文档要求；
- 报告不再把“可能需更新”伪装成“已同步”。

## 11. 测试矩阵

| 场景 | 必须验证 |
|------|----------|
| Fresh minimal | 仅生成该模式文件；所有入口和链接有效 |
| Fresh standard | 完整固定能力；Intent/Reality 边界存在 |
| Manifest side effects | 拦截 Write Gateway，验证目录、文件、受管区块、忽略规则、State、基线、事务日志和运行目录均匹配 Action Plan；绕过 Gateway 的写入测试失败 |
| Required source missing | 写入前失败；目标树字节级不变 |
| Target escape/symlink escape | 写入前失败；不得越过允许根目录 |
| Rerun | 无文件变化、无重复 Managed Block |
| Repair | 缺失 managed-file 可补齐；漂移 managed-file 不覆盖；缺失或漂移 generated 可重建；手改 generated 先报告再经 `--apply` 重建 |
| User modified | 不覆盖，报告冲突和三方 diff |
| Adopt without baseline | 标记 `ownership: unknown`；只输出两方差异，不覆盖、不伪造三方 diff |
| Explicit take-over | 建立可信基线；下一版本可做三方 diff |
| Transaction resume | 仅在下一动作可证明未应用、输入未变化且可幂等重放时继续；否则拒绝并要求 rollback |
| Transaction rollback | 指定事务 ID 且用户文件 Hash 未发生事务外变化时完整恢复；检测到并发修改则停止并报告 |
| Separate repo | 文件准确落在传入 `docs_root`；跨仓影响检查明确为 Warning |
| Separate repo mismatch | `docs-root` 所在仓库与 State ID 不一致时失败 |
| Path with spaces/中文 | 初始化和检查通过 |
| No Git | 初始化可用；Git 影响检查明确跳过 |
| Initial commit | 不依赖 `HEAD~1` |
| Dirty worktree | staged/unstaged/untracked 均进入影响分析 |
| Missing template | 失败并返回稳定错误码 |
| Broken link | Validator 和 CI 失败 |
| Validator unavailable | blocking 检查保留 `blocked/unobserved` verdict、退出码非零且不放行，不得改写成 pass 或 fail |
| Zero/skipped checks | 不计为通过证据 |
| Invalid frontmatter | Validator 失败并定位文件/字段 |
| Migration success | 路径和引用一起更新 |
| Migration conflict | 不写入或完整回滚 |
| Migration interrupted | 下次运行可检测并 resume/rollback |
| Temp resources | 默认测试结束后清理 |
| Consumer fixture | 真实安装结果不包含维护仓内部资产，所有必需目标均验证 |
| Previous-version fixture | 使用发布 tag/包冻结并记录 checksum；无历史发布时使用明确标注的只读兼容 fixture，缺失 fixture 时 CI 为 blocked；从 fixture 升级后重复升级为 no-op，用户修改不被覆盖 |

## 12. 验收标准

### P0

- [ ] AC-01：Manifest 是模式、Capability、模板、目标、所有权、必需目录、Profile、检查策略、迁移规则和允许动作的唯一来源。
- [ ] AC-02：真实 Installer 承担安装行为，测试不复制安装逻辑。
- [ ] AC-03：Minimal 和 Standard 均无悬空目录、命令或链接。
- [ ] AC-04：`project_root` 与 `docs_root` 语义唯一且有独立仓库测试。
- [ ] AC-05：相同输入二次执行字节级无变化。
- [ ] AC-06：用户修改过的文件不会被静默覆盖。
- [ ] AC-07：真相裁决按事实域定义，不再使用矛盾的单线优先级。
- [ ] AC-08：Validator 发现确定性错误时返回非零。
- [ ] AC-09：Fresh install 和模板包通过 v5 检查；当前历史仓库在完成 Adopt 后进入 Dogfood。
- [ ] AC-21：所有持久写入经唯一 Write Gateway 执行并与 Manifest 展开的 Action Plan 对账；未知动作、必需源缺失、重复目标、绕过 Gateway 和路径逃逸在写入前失败。
- [ ] AC-22：Blocking Validator 未运行、被阻断或证据不足时保留原 verdict、退出码非零且不放行，不得报告为通过或错误改写成 `fail`。

### P1

- [ ] AC-10：Standard 默认分离 `design/intent/` 与 `design/reality/`。
- [ ] AC-11：PRD 和 Plan 模板边界与各自 Owner 职责一致。
- [ ] AC-12：旧项目可 Adopt，未知历史记录为 `ownership: unknown`；只有显式 Take-over 后才建立可恢复基线和受管理状态。
- [ ] AC-13：`exec-plans/` 可通过显式迁移安全转换为 `plans/`。
- [ ] AC-14：CI 自动运行 Manifest、链接、状态和测试校验。
- [ ] AC-15：测试默认清理临时目录和进程。
- [ ] AC-16：根 AGENTS 不再注入特定技术栈规则。
- [ ] AC-23：技术栈 Profile 按能力声明 `available/partial/unavailable`，只有绑定可执行检查和验证证据的能力可标为 `available`。
- [ ] AC-24：CI 同时覆盖空仓安装、消费者 fixture、带来源和 checksum 的上一稳定版本 fixture，以及当前仓库 Dogfood。

### P2

- [ ] AC-17：变更影响检查覆盖 base...HEAD、staged、unstaged 和 untracked。
- [ ] AC-18：变更影响矩阵支持按技术栈 Profile 扩展。
- [ ] AC-19：长期文档支持 superseded 链和 freshness 检查。
- [ ] AC-20：操作报告同时支持 text 和 JSON。

## 13. 成功指标

| 指标 | v5 目标 | 测量方式 |
|------|---------|----------|
| 模式输出完整率 | 100% | Manifest 驱动的集成测试 |
| 仓库内相对链接有效率 | 100% | Validator |
| Installer/测试逻辑重复 | 0 份 | 代码审查 + 测试结构检查 |
| 二次执行变更文件数 | 0 | 字节 Hash 对比 |
| 用户修改静默覆盖 | 0 | 冲突测试 |
| 模板未替换占位符 | 0 个 Error；允许显式 TODO Warning | Validator |
| 未观察却报告通过 | 0 次 | 结构化检查 verdict 测试 |
| Manifest 外持久副作用 | 0 项 | Installer action trace 与 Manifest 对账 |
| 当前仓库 dogfood | 主分支持续通过 | CI |
| 临时测试资源残留 | 0 | 测试 teardown 检查 |

不设置无法自动证明的“文档内容正确率 100%”。内容正确性由 Owner 审核、可执行证据和领域工具共同保证。

## 14. 风险与缓解

| 风险 | 影响 | 缓解 |
|------|------|------|
| v5 范围过大 | 长期停留在设计阶段 | 按 Phase 独立交付，Phase 1 先消除单一安装真相问题 |
| Frontmatter 增加写作负担 | 用户抗拒 | 只对长期文档强制；CLI 生成默认字段 |
| Manifest 变成新巨型配置 | 维护困难 | Schema 保持声明式；技术栈影响矩阵拆 Profile |
| 迁移误改用户文档 | 数据损失 | 默认 dry-run、Hash 检测、三方 diff、原子写入和回滚 |
| Intent/Reality 对小项目过重 | 空目录和分类成本 | Minimal 不启用该 Capability |
| 自动索引破坏人工说明 | README 内容丢失 | 只管理明确标记的 Generated Block |
| AI 自动探索写入错误事实 | 错误架构传播 | 生成草稿并标记证据，必须经 Validator 和 Owner 确认 |

## 15. 开放决策

以下决策应在进入实现计划前完成，不应在编码中临时拍脑袋：

1. Installer 使用 Python 标准库还是 Shell。推荐 Python，原因是路径处理、JSON/YAML、Hash、原子写入和测试更可靠。
2. Manifest 使用 YAML 还是 JSON。推荐 YAML 供维护者阅读，但必须有 Schema 校验；若不引入 YAML 依赖，则使用 JSON。
3. README 索引采用完全生成还是 Managed Block。推荐 Managed Block，保留人工目录边界说明。
4. v5 是否立即把当前仓库 `exec-plans/` 迁到 `plans/`。推荐在迁移器和链接检查完成后做，不手工提前搬。

已裁决：State 的权威副本只放在实际包含受管 docs 的仓库根。Inline 模式是代码项目根，Separate-repo 模式是文档仓库根；代码仓不保存第二份可写 State。跨仓影响门禁不进入 v5.0 Core。

## 16. 实施前门禁

进入实现前必须：

- [ ] PRD 评审通过；
- [ ] 为 Manifest Schema、CLI 契约和迁移事务写独立技术设计；
- [ ] 建立 Phase 1 执行计划；
- [ ] 明确 v4 行为兼容矩阵；
- [ ] 先写 Installer 的端到端失败测试；
- [ ] 指定独立 Reviewer 审核 Manifest 与迁移方案；
- [ ] 不在同一提交中同时重写所有模板和迁移当前仓库。

## 17. 参考资料

### 参考文档系统

- `human-resources/docs/index.md`
- `human-resources/docs/design/README.md`
- `human-resources/docs/meta/documentation-system-guide.md`
- `human-resources/docs/agent-guides/plan-mode.md`
- `human-resources/docs/context/source-of-truth.md`

负面证据样例：

- `human-resources/docs/meta/documentation-system-guide.md:153-161` 声明 100% 指标，`:262-284` 明确健康检查尚未实现；
- `human-resources/docs/prd/README.md:3-9` 规定 PRD 不写实现，`docs/prd/TEMPLATE.md:66-91` 又要求技术方案、数据模型和 API；
- `human-resources/docs/index.md:109-115` 限制 Active Plan 为 3 个，但实际目录和索引已出现超限与漏登记；
- `human-resources/docs/design/README.md:82-100` 的文件级更新触发器值得保留，但仍主要依赖人工执行；
- 根 `ARCHITECTURE.md:1-5` 是 2026-06-16 自动快照，`:284-304` 包含易漂移的表数量和具体事实。

这些证据来自 2026-08-25 的本地工作树快照，不代表稳定提交。进入实现前应将参考研究固化为可提交的证据附录，并记录参考仓库 commit SHA；本 PRD 中“值得借鉴/不应照搬”的判断属于基于该快照的产品推导。

完整本地路径：

`/home/fenghaolin/workspace/prj/develop/openai/human-resources/ai-dev-log/human-resources`

### 第二批参考项目

- `.ref-project/attractor-guided-engineering-template/install-age.manifest:1-36`：显式消费者安装白名单。
- `.ref-project/attractor-guided-engineering-template/tools/install-age.mjs:190-261`：存在即跳过、清单外副作用和非事务写入。
- `.ref-project/attractor-guided-engineering-template/docs/architecture/template-vs-realproject-boundary.md:14-63`：consumer、dogfood 和共享资产所有权。
- `.ref-project/attractor-guided-engineering-template/tools/mission-driver/src/run-reconcile.mjs:95-205`：保守 stale-run 对账。
- `.ref-project/better-harness/docs/ARCHITECTURE.md:10-23`：薄入口、唯一 Owner、AI 判断与确定性执行分离。
- `.ref-project/better-harness/models/agent-work-loop.md:91-149`：证据强度与验收结果分离。
- `.ref-project/better-harness/references/project-harness/agent-verify-loop.md:169-227`：`pass/fail/unobserved/blocked` 语义。
- `.ref-project/better-harness/scripts/harness-analysis/render-report.mjs:324-519`：Stage → Validate → Publish 与失败恢复。
- `.ref-project/ddd-harness-microservices/AGENTS.md:137-195`：变更类型到文档 Owner 的人工映射。
- `.ref-project/ddd-harness-microservices/docs/designs/api.yaml:11-155` 与 `backends/service-domain-demo/src/main/java/com/example/demo/adapter/controller/TicketController.java:23-55`：手写 API 文档漂移证据。
- `.ref-project/ddd-harness-microservices/docs/designs/db.md:103-153` 与 `backends/service-domain-demo/src/main/resources/db/migration/V20240311__add_ticket_table_as_example.sql:1-32`：数据库和枚举漂移证据。
- `.ref-project/ddd-harness-microservices/docs/designs/others/data-dict.md:35-69`、`backends/service-domain-demo/src/main/resources/application.yml:45-46` 与 `backends/service-domain-demo/src/main/java/com/example/demo/domain/aggregate/DemoDataDictionaryType.java:4-29`：字典配置和注册漂移证据。
- `.ref-project/ddd-harness-microservices/docs/standards/security.md:34-46` 与 `backends/service-bff/src/main/java/com/example/bff/utils/JwtUtil.java:11-26`：禁止硬编码密钥的规范与实现冲突。

第二批证据均固定到 2.4 节记录的 commit，不以当前工作树名称代替版本身份。

### 当前 docs-pipeline

- `docs-pipeline/SKILL.md`
- `docs-pipeline/assets/templates/`
- `docs-pipeline/scripts/test-pipeline.sh`
- `docs-pipeline/scripts/test-modes.sh`
- `docs-pipeline/scripts/check-template-refs.py`
- `docs-pipeline/README.md`
- `docs-pipeline/ADVANCED.md`
- `docs-pipeline/EVOLUTION.md`
- `docs/prd/2026-06-09-docs-pipeline-目录重构.md`

## 18. 决策摘要

**值得做。** 当前问题不是模板不够多，而是数据结构错了：同一安装契约被复制在 Skill、脚本、文档和现有产物中。继续追加条件和模板只会扩大漂移。

v5 的最小正确方向是：

1. 用 Manifest 消灭重复清单；
2. 用 Installer 消灭重复实现；
3. 用 Validator 把规则变成证据；
4. 用 State + Migration 保护既有用户；
5. 用 Owner + Intent/Reality 让文档回答正确的问题；
6. 用 CI 保证系统不是“初始化当天看起来正确”。
7. 用显式证据状态阻止“没有检查却显示绿色”。
