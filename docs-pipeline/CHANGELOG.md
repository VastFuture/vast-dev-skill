# docs-pipeline 更新日志

## [4.5.3] - 2026-06-10

### Changed

- **CLAUDE.md 模板改为薄引用** — 从 281 行全文缩减为 5 行 `@AGENTS.md` 入口，消除初始化时人造的 CLAUDE.md↔AGENTS.md 双重行。
- **AGENTS.md 模板标记为统一入口** — 头部加 `入口: CLAUDE.md → @AGENTS.md` 声明。
- **standards/ 模板加技术栈警告** — 5 个文件顶部加 `⚠️ 技术栈适配` 提示，明确 Java/Spring 示例需本地化。

## [4.5.2] - 2026-06-09

### Added

- **`project-context.md` 模板扩展 4 个操作章节** — 自检命令、测试环境要求、系统启动流程、CDP 验证流程（UI 改动必跑）
- **`AGENTS.md` 模板加职责边界声明** — 验证基线节注：操作细节归 `project-context.md`，本文件只定义验证流程规则

### Design

- **AGENTS.md vs project-context.md 职责划分**：AGENTS.md = AI 怎么工作（流程规则），project-context.md = 项目怎么跑（操作命令）。消除两者混装操作细节的反模式。

## [4.5.1] - 2026-06-09

### Fixed

- **删除 `docs-CLAUDE.md` 模板** — 与 `docs/index.md` + `source-of-truth` 三重重复。内容（Owner Docs 职责、真相优先级、铁律）已合入 `docs-index.md`。
- **修复 AGENTS.md 产物链路 `plans/` 不一致** — ASCII 图统一为 `exec-plans/active/` → `exec-plans/completed/`。

### Added

- **`project-context.md` 模板加 AI 自主维护规则** — "在 exec-plans/active/ 新建/移动计划文件时必须同步更新此表"。
- **`codebase-map.md` 模板加强占位符提醒** — 文件顶部加 ⚠️ 警告，明确要求 AI 首次使用时填充所有 `<...>` 占位符。

## [4.5.0] - 2026-06-09

### Breaking Changes

#### 目录结构重构：10 目录 SDD 驱动

基于 AGE 和 DDD 模板的深度研究，将目录结构从 14 个精炼为 10 个核心目录：

**删除的目录**：
- `designs/` — 合并到 `design/`，采用 SDD 双向同步（设计意图 + 实现现状在同一目录）
- `research/` — 改为可选目录
- `handover/` — 改为可选目录  
- `ideas/` — 改为可选目录

**新增/重命名的目录**：
- `architecture/` — 技术基线、模块边界、分层规范（新增）
- `logs/` — 开发日志、每日记录（新增，从可选升为核心）
- `prd/` — 需求规格（取代 `features/`）
- `plans/` — 执行计划（取代 `exec-plans/`，扁平化不再有 `active/` 子目录）

**保留的目录**：
- `context/`, `backlog/`, `design/`, `standards/`, `lessons/`, `issues/`

#### SDD 驱动替代 designs/ 

`design/` 现在同时承载：
- 设计意图（功能开发前写）
- 实现现状（代码完成后同步）
- 消除了 `design/` vs `designs/` 的哲学冲突

详见 `docs/prd/2026-06-09-docs-pipeline-目录重构.md`

### 模板更新

- CLAUDE.md 模板：更新文档所有权为 11 目录
- AGENTS.md 模板：更新工作流和产物链路
- docs-index.md 模板：更新路由表和目录职责
- SKILL.md：更新核心工作流和模板映射

## [4.4.0] - 2026-06-05

### 新增

#### 1. 文档同步机制

基于 [ddd-harness-microservices](https://github.com/domain-driven-design/ddd-harness-microservices) 项目的启发，增加了文档同步机制：

- **新增 `docs/standards/` 目录**：存放开发规范（分层、API、DB、安全、命名）
- **新增 `docs/designs/` 目录**：存放系统设计现状（API、DB、业务规则、数据字典）
- **新增文档同步检查步骤**（Step 10）：检测代码变更并提示需要更新的文档
- **新增 PR Checklist**：在 AGENTS.md 中增加文档同步检查项

#### 2. 新增模板文件

**standards/ 目录模板**（6 个文件）：
- `standards-README.md` - 规范目录说明
- `standards-layers.md` - 分层架构规范
- `standards-api.md` - API 设计规范
- `standards-db.md` - 数据库规范
- `standards-security.md` - 安全规范
- `standards-naming.md` - 命名规范

**designs/ 目录模板**（6 个文件）：
- `designs-README.md` - 现状目录说明
- `designs-api.yaml` - API 现状（OpenAPI/Swagger）
- `designs-db.md` - 数据库现状
- `designs-others-README.md` - 其他现状说明
- `designs-others-businessrule.md` - 业务规则现状
- `designs-others-data-dict.md` - 数据字典现状

### 修改

#### 1. SKILL.md

- 更新目录创建逻辑：Standard 模式增加 `standards/` 和 `designs/` 目录
- 更新目录对照表：增加 `standards` 和 `designs` 列
- 增加模板映射：12 个新模板文件
- 增加 Step 10：文档同步检查步骤
- 更新执行报告模板：增加文档同步状态显示

#### 2. AGENTS.md 模板

- 增加 PR / Change Checklist 段落
- 增加文档所有权表格：新增 `standards/` 和 `designs/` 目录

#### 3. docs-index.md 模板

- 增加目录职责表格：新增 `standards/` 和 `designs/` 目录
- 增加核心原则：说明文档同步规则

#### 4. README.md

- 增加参考项目链接：ddd-harness-microservices
- 增加核心目录表格：新增 `standards/` 和 `designs/` 目录

#### 5. USAGE.md

- 增加场景 6：代码变更后文档同步
- 更新文档决策树：增加文档同步分支
- 增加关键区别：`standards/` vs `designs/`、`design/` vs `designs/`

---

## 核心改进点

### 1. 文档同步机制

每次代码变更后，强制检查以下文档是否需要更新：

| 变更类型 | 需要更新的文档 |
|----------|---------------|
| 新增/修改 API | `docs/designs/api.yaml` |
| 新增/修改数据表 | `docs/designs/db.md` |
| 新增/修改业务规则 | `docs/designs/others/businessrule.md` |
| 新增/修改数据字典 | `docs/designs/others/data-dict.md` |
| 修改分层架构 | `docs/standards/layers.md` |
| 修改 API 规范 | `docs/standards/api.md` |
| 修改数据库规范 | `docs/standards/db.md` |
| 修改安全规范 | `docs/standards/security.md` |

### 2. PR Checklist 集成

在 AGENTS.md 中增加 PR Checklist，包含：
- 文档同步检查（强制）
- 代码质量检查
- 测试覆盖检查

### 3. 三层文档体系

- **规范层**（standards/）：开发规范，相对稳定
- **现状层**（designs/）：系统现状，高频更新
- **流程层**（现有目录）：文档管理流程

---

## 预期效果

- ✅ **文档完整性**：规范层 + 现状层 + 流程层
- ✅ **同步机制**：强制文档同步检查
- ✅ **开发体验**：文档驱动开发，减少沟通成本
- ✅ **质量保障**：PR Checklist 确保变更质量

---

## 参考资料

- [ddd-harness-microservices 项目](https://github.com/domain-driven-design/ddd-harness-microservices)
- [学习成果文档](../docs/ddd-harness-microservices-study.md)
- [改进方案文档](../docs/docs-pipeline-enhancement-proposal.md)

## [4.5.0] - 2026-06-05

### 优化（基于 darwin-skill 评估）

#### 1. 失败模式编码

为每个步骤添加了显式的失败模式编码：

| 步骤 | 失败模式 |
|------|----------|
| Step 1 | `ls` 命令失败、检测结果不明确 |
| Step 2 | 目录创建失败、磁盘空间不足、路径过长 |
| Step 3 | 模板文件不存在、目标目录不存在、写入权限不足、Read/Write 命令失败 |
| Step 4 | 模板文件不存在、目标文件已存在、写入权限不足 |
| Step 5 | `.claude/commands/` 目录不存在、模板文件不存在、目标文件已存在 |
| Step 6 | grep 命令失败、模板文件不存在、Edit 命令失败、文件格式不兼容 |
| Step 7 | 环境变量未设置、`.pensieve/` 目录不存在、Pensieve 初始化失败 |
| Step 8 | Explore 子代理超时、返回空、项目类型无法识别、模板写入失败 |
| Step 9 | 报告生成失败、文件列表不完整、格式化失败 |
| Step 10 | git 命令失败、变更文件列表为空、grep 命令失败、报告生成失败 |

#### 2. 检查点设计

在关键决策点添加了 🔴 CHECKPOINT / 🛑 STOP 视觉标记：

| 检查点 | 位置 | 用途 |
|--------|------|------|
| 模式确认 | Step 0.5 | 确认文档模式和安装模式 |
| 开始建目录 | Step 2 | 确认即将创建的目录列表 |
| 开始写入模板 | Step 3 | 确认即将写入的模板文件数量 |
| 写入项目根模板 | Step 4 | 确认即将写入的项目根文件 |
| 生成 ARCHITECTURE.md | Step 8 | 确认是否生成 ARCHITECTURE.md |
| 文档同步检查 | Step 10 | 确认是否执行文档同步检查 |

#### 3. fallback 路径表

为每个步骤添加了降级策略：

| 步骤 | 降级策略 |
|------|----------|
| Step 1 | 使用 `test -d` 替代 `ls` |
| Step 2 | 跳过非必需目录 |
| Step 3 | 跳过该文件，记录警告 |
| Step 4 | 跳过该文件，记录警告 |
| Step 5 | 跳过，记录需人工处理 |
| Step 6 | 跳过，记录需人工处理 |
| Step 7 | 跳过，不提示 |
| Step 8 | 按项目类型降级（见项目类型降级表） |
| Step 9 | 输出简化版报告 |
| Step 10 | 跳过同步检查，提示非 git 仓库 |

#### 4. 项目类型降级表

为 ARCHITECTURE.md 生成添加了智能降级策略：

| 检测文件 | 项目类型 | 降级模板 |
|----------|----------|----------|
| package.json | Node.js | `assets/templates/arch-nodejs.md` |
| setup.py / pyproject.toml | Python | `assets/templates/arch-python.md` |
| go.mod | Go | `assets/templates/arch-go.md` |
| Cargo.toml | Rust | `assets/templates/arch-rust.md` |
| 以上都无 | 通用 | `assets/templates/arch-generic.md` |

### 分数变化

| 维度 | 基线分数 | 优化后分数 | 变化 |
|------|----------|------------|------|
| 1. Frontmatter 质量 | 6/7 | 6/7 | 0 |
| 2. 工作流清晰度 | 10/12 | 11/12 | +1 |
| 3. 失败模式编码 | 6/12 | 11/12 | +5 |
| 4. 检查点设计 | 3/6 | 6/6 | +3 |
| 5. 可执行具体性 | 14/17 | 15/17 | +1 |
| 6. 资源整合度 | 4/4 | 4/4 | 0 |
| 7. 整体架构 | 10/12 | 11/12 | +1 |
| 8. 实测表现 | 0/23 | 20/23 | +20 |
| 9. 反例与黑名单 | 5/6 | 5/6 | 0 |
| **总分** | **58/94** | **89/94** | **+31** |

### 优化亮点

1. **失败模式编码**：每个步骤都有显式的 "如果 X 失败 → Y" 分支
2. **检查点设计**：关键决策前有 🔴 CHECKPOINT / 🛑 STOP 视觉标记
3. **实测表现**：通过 3 个典型场景验证了实际效果
4. **fallback 路径表**：每个步骤都有降级策略
5. **项目类型降级表**：ARCHITECTURE.md 生成失败时的智能降级
