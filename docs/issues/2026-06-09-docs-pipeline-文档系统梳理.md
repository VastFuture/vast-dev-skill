# docs-pipeline 文档系统全面梳理

**日期**：2026-06-09  
**状态**：已完成梳理  
**目的**：理清整套文档系统的工作机制和逻辑链路

---

## 一、目录结构全景

```
docs-pipeline/
├── SKILL.md                    # 核心指令文件（855行），定义完整工作流
├── README.md                   # 用户文档，快速入门
├── USAGE.md                    # 使用场景和最佳实践
├── ADVANCED.md                 # 高级功能（Pensieve、ARCHITECTURE.md）
├── CHANGELOG.md                # 版本更新日志
├── EVOLUTION.md                # 架构演进记录
├── OPTIMIZATION-REPORT.md      # 优化报告
├── test-prompts.json           # 测试 prompt
│
├── assets/templates/           # 模板文件（39个）
│   ├── 根级模板
│   │   ├── CLAUDE.md           # 项目根 Claude 行为规范
│   │   ├── AGENTS.md           # 项目根 AI 代理全局指令
│   │   ├── claude-md-snippet.md
│   │   └── mcp.json
│   │
│   ├── docs/ 相关模板
│   │   ├── docs-CLAUDE.md      # docs/ 目录规则
│   │   └── docs-index.md       # 文档路由中枢
│   │
│   ├── context/ 模板
│   │   ├── project-context.md
│   │   ├── ai-autonomy-policy.md
│   │   ├── codebase-map.md
│   │   └── source-of-truth-and-precedence.md
│   │
│   ├── agent-guides/ 模板（7个）
│   │   ├── output-modes.md
│   │   ├── content-organization.md
│   │   ├── plan-mode.md
│   │   ├── requirement-confirmation.md
│   │   ├── engineering-rules.md
│   │   ├── karpathy-guidelines.md
│   │   └── MBTI_DEV_TRAPS.md
│   │
│   ├── standards/ 模板（6个）
│   │   ├── layers.md
│   │   ├── api.md
│   │   ├── db.md
│   │   ├── security.md
│   │   └── naming.md
│   │
│   ├── designs/ 模板（6个）
│   │   ├── api.yaml
│   │   ├── db.md
│   │   ├── others/businessrule.md
│   │   └── others/data-dict.md
│   │
│   ├── 各目录 README.md（9个）
│   │   ├── backlog-README.md
│   │   ├── prd-README.md
│   │   ├── design-README.md
│   │   ├── exec-plans-README.md
│   │   ├── ideas-README.md
│   │   ├── research-README.md
│   │   ├── handover-README.md
│   │   ├── issues-README.md
│   │   └── lessons-README.md
│   │
│   ├── 各目录 TEMPLATE.md（4个）
│   │   ├── prd-TEMPLATE.md
│   │   ├── exec-plans-TEMPLATE.md
│   │   ├── handover-TEMPLATE.md
│   │   └── issues-TEMPLATE.md
│   │
│   └── commands/
│       └── ideas.md
│
├── references/
│   ├── adding-templates.md
│   └── pensieve-integration.md
│
└── scripts/
    ├── test-modes.sh
    └── test-pipeline.sh
```

---

## 二、工作流程

### 2.1 完整流程（10步）

```
Step 0: 检测文档模式
  ├── 检查环境变量 DOCS_ROOT
  ├── 自动检测 docs/.git
  ├── 确定文档根路径
  ├── 确定项目根路径
  └── 检测安装模式（minimal/standard）
      🔴 CHECKPOINT · 模式确认

Step 1: 检测目标项目状态
  ├── 不存在 → 全新初始化
  ├── 部分存在 → 修复模式
  └── 全部齐全 → 跳过

Step 2: 建目录
  ├── Minimal: 7 个必需目录
  └── Standard: 12 个核心目录
      🔴 CHECKPOINT · 开始建目录

Step 3: 写入 docs/ 模板
  ├── docs/CLAUDE.md
  ├── docs/index.md
  ├── context/ (4个文件)
  ├── 各目录 README.md
  ├── 各目录 TEMPLATE.md
  ├── agent-guides/ (7个文件)
  ├── standards/ (6个文件)
  └── designs/ (6个文件)
      🔴 CHECKPOINT · 开始写入模板

Step 4: 写入项目根 AI 代理模板
  ├── CLAUDE.md
  ├── AGENTS.md
  └── .mcp.json
      🔴 CHECKPOINT · 写入项目根模板

Step 5: 写入项目级命令
  └── .claude/commands/ideas.md

Step 6: 处理项目根 CLAUDE.md 的"## 文档"段落
  ├── 已写入完整模板 → 跳过
  └── 已存在跳过 → 追加 claude-md-snippet.md

Step 7: Pensieve 集成（可选）
  ├── 默认跳过
  └── ENABLE_PENSIEVE=true 或 .pensieve/ 存在 → 激活

Step 8: 生成 ARCHITECTURE.md
  ├── 调用 Explore 子代理生成
  └── 失败降级：按项目类型智能降级
      🔴 CHECKPOINT · 生成 ARCHITECTURE.md

Step 9: 输出报告

Step 10: 文档同步检查（Standard 模式）
  ├── 检测代码变更
  ├── 分析变更类型
  ├── 提示同步更新
  └── 生成同步报告
      🔴 CHECKPOINT · 文档同步检查
```

### 2.2 两种安装模式

| 模式 | 目录数量 | 适用场景 |
|------|---------|---------|
| Minimal | 7 | 快速启动，最小化文档 |
| Standard | 12+ | 完整文档体系，适合正式项目 |

---

## 三、模板引用关系

### 3.1 核心引用链

```
SKILL.md（工作流定义）
    │
    ▼
CLAUDE.md（项目根行为规范）
    │
    ├──▶ AGENTS.md（AI 代理全局指令）
    │
    ├──▶ docs-CLAUDE.md（docs/ 目录规则）
    │
    └──▶ docs-index.md（文档路由中枢）
              │
              ├──▶ context/（4个文件）
              ├──▶ agent-guides/（7个文件）
              ├──▶ standards/（6个文件）
              ├──▶ designs/（6个文件）
              └──▶ 各目录 README.md（9个）
```

### 3.2 文档所有权定义

#### CLAUDE.md 中的定义

| 目录 | 职责 | 更新频率 |
|------|------|---------|
| `docs/context/` | 项目上下文，验证命令 | 中频 |
| `docs/backlog/` | 工作队列 | 高频 |
| `docs/research/` | 调研文档 | 中频 |
| `docs/prd/` | 产品需求文档 | 中频 |
| `docs/design/` | 稳定的应用层业务和功能设计 | 低频 |
| `docs/exec-plans/` | 执行计划 | 中频 |
| `docs/lessons/` | 经验教训 | 低频 |
| `docs/standards/` | 开发规范 | 低频 |
| `docs/designs/` | 系统设计现状（API/DB/业务规则/数据字典） | 高频 |

#### docs-index.md 中的路由表

| 任务类型 | 路由目标 |
|---------|---------|
| 设计变更 | `docs/design/` |
| API 变更 | `docs/designs/api.yaml` |
| 数据库变更 | `docs/designs/db.md` |
| 业务规则变更 | `docs/designs/others/businessrule.md` |
| 新增功能 | `docs/prd/` → `docs/design/` → `docs/exec-plans/` |
| Bug 修复 | `docs/issues/` |
| 调研 | `docs/research/` |

---

## 四、问题清单

### 4.1 严重问题

#### 问题 1：design/ 和 designs/ 职责边界模糊

**现状**：
- `docs/design/`：稳定的应用层业务和功能设计（低频更新）
- `docs/designs/`：系统设计现状（高频更新）

**冲突**：
- 两个目录都叫"design"相关，容易混淆
- 内容有重叠（如设计决策）
- 没有明确的划分规则
- `docs/index.md` 只引用 `design/`，没有 `designs/` 的路由

**影响**：用户不知道该用哪个目录，导致文档混乱。

---

#### 问题 2：哲学冲突

**现状**：
- AGE 哲学：设计驱动（设计先于代码，代码向设计收敛）
- v4.4.0 哲学：代码驱动（代码是真相，文档必须跟上代码）

**冲突**：
- 两套互斥的设计哲学被塞进同一个模板
- `CLAUDE.md` 和 `AGENTS.md` 同时引用两个目录
- 文档所有权表格列出了两个目录，但职责边界模糊

**影响**：用户困惑，不知道该遵循哪种哲学。

---

#### 问题 3：引用不一致

**现状**：
- `docs/index.md` 模板只引用 `design/`（单数）
- `CLAUDE.md` 和 `AGENTS.md` 模板同时引用两个目录
- 用户不知道该用哪个

**影响**：文档引用混乱，用户不知道该遵循哪个引用。

---

### 4.2 中等问题

#### 问题 4：owner docs 职责表格与实际目录不匹配

**现状**：
- `docs-CLAUDE.md` 中的 owner docs 职责表格列出了 `requirements/`、`architecture/`、`plans/`、`audits/` 等目录
- 但实际模板中只有 `context/`、`backlog/`、`research/`、`prd/`、`design/`、`exec-plans/`、`lessons/`、`standards/`、`designs/`

**影响**：用户困惑，不知道这些目录是否应该创建。

---

#### 问题 5：source-of-truth-and-precedence.md 中的优先级与实际不符

**现状**：
- 优先级是：`design/` > `architecture/` > `requirements/` > `context/` > 源代码
- 但实际模板中没有 `architecture/` 和 `requirements/` 目录

**影响**：用户困惑，不知道这些目录是否应该创建。

---

#### 问题 6：project-context.md 中的引用过时

**现状**：
- 引用了 `docs/requirements/<file>` 和 `docs/design/<file>` 或 `docs/architecture/<file>`
- 但实际模板中没有 `requirements/` 和 `architecture/` 目录

**影响**：用户困惑，不知道这些目录是否应该创建。

---

### 4.3 轻微问题

#### 问题 7：test-modes.sh 中的目录数量不准确

**现状**：
- standard 模式期望 12 个目录
- 但实际模板中 standard 模式创建 14 个目录

**影响**：测试脚本不准确，可能导致测试失败。

---

#### 问题 8：test-pipeline.sh 中的文件复制不完整

**现状**：
- 没有复制 `standards/` 和 `designs/` 目录下的模板文件

**影响**：测试脚本不完整，可能导致测试失败。

---

#### 问题 9：docs-index.md 中的引用过时

**现状**：
- 引用了 `docs/design/app-overview.md` 和 `docs/design/feature-inventory.md`
- 但实际模板中没有这些文件

**影响**：用户困惑，不知道这些文件是否应该创建。

---

#### 问题 10：design-README.md 中的引用过时

**现状**：
- 引用了 `app-overview.md`、`feature-inventory.md`、`roles-and-permissions.md`
- 但实际模板中没有这些文件

**影响**：用户困惑，不知道这些文件是否应该创建。

---

## 五、逻辑链路图

### 5.1 完整链路

```
┌─────────────────────────────────────────────────────────────┐
│                    文档系统逻辑链路                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  【入口层】                                                   │
│  SKILL.md ──▶ README.md ──▶ USAGE.md                        │
│       │                                                      │
│       ▼                                                      │
│  【模板层】                                                   │
│  CLAUDE.md ──▶ AGENTS.md                                    │
│       │                                                      │
│       ├──▶ docs-CLAUDE.md                                   │
│       │                                                      │
│       └──▶ docs-index.md                                    │
│              │                                               │
│              ├──▶ context/（4个文件）                         │
│              ├──▶ agent-guides/（7个文件）                    │
│              ├──▶ standards/（6个文件）                       │
│              ├──▶ designs/（6个文件）                         │
│              └──▶ 各目录 README.md（9个）                     │
│                                                             │
│       ▼                                                      │
│  【输出层】                                                   │
│  docs/ 目录结构 + 项目根 CLAUDE.md/AGENTS.md                 │
│       │                                                      │
│       ▼                                                      │
│  【使用层】                                                   │
│  AI 工作流：读取 context/ → 选择 backlog/ → 写 prd/          │
│       │                                                      │
│       ▼                                                      │
│  更新 design/ → 写 exec-plans/ → 实现                        │
│       │                                                      │
│       ▼                                                      │
│  验证 → 闭包审计 → 记录 lessons/                              │
│                                                             │
│  【同步层】                                                   │
│  代码变更 → 检查 designs/ → 更新文档                          │
│       │                                                      │
│       ▼                                                      │
│  PR Checklist → 强制同步检查                                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 关键断裂点

```
断裂点 1：design/ vs designs/
├── 问题：职责边界模糊，哲学冲突
├── 影响：用户不知道该用哪个目录
└── 修复：明确划分规则或合并

断裂点 2：引用不一致
├── 问题：docs-index.md 只引用 design/，CLAUDE.md/AGENTS.md 同时引用两个
├── 影响：文档引用混乱
└── 修复：统一引用规则

断裂点 3：owner docs 职责表格与实际目录不匹配
├── 问题：表格列出了 requirements/、architecture/ 等不存在的目录
├── 影响：用户困惑
└── 修复：更新表格或创建目录

断裂点 4：source-of-truth-and-precedence.md 优先级与实际不符
├── 问题：优先级包含不存在的目录
├── 影响：用户困惑
└── 修复：更新优先级或创建目录
```

---

## 六、决策建议

### 6.1 关于 design/ vs designs/

**推荐方案**：明确划分规则，两个都保留

**理由**：
1. **职责不同**：design/ 是设计基线，designs/ 是现状快照
2. **更新频率不同**：design/ 低频，designs/ 高频
3. **同步规则不同**：design/ 无强制，designs/ 强制同步

**划分规则**：
| 内容类型 | 归属目录 | 理由 |
|---------|---------|------|
| 产品功能基线 | design/ | 稳定，低频更新 |
| 页面流程 | design/ | 稳定，低频更新 |
| 角色权限 | design/ | 稳定，低频更新 |
| API 现状 | designs/ | 高频变更，需同步 |
| 数据库表结构 | designs/ | 高频变更，需同步 |
| 业务规则 | designs/ | 高频变更，需同步 |
| 数据字典 | designs/ | 高频变更，需同步 |

---

### 6.2 关于哲学冲突

**推荐方案**：采用混合哲学

**核心原则**：
- **设计意图**（design/）：设计先行，代码向设计收敛
- **实现现状**（designs/）：代码是真相，文档必须跟上代码

**工作流程**：
1. 新功能：先写 design/（设计意图），再写代码，最后同步 designs/（实现现状）
2. Bug 修复：先修代码，再同步 designs/，最后检查是否需要更新 design/
3. 重构：先更新 design/（新设计），再重构代码，最后同步 designs/

---

### 6.3 关于引用不一致

**推荐方案**：统一引用规则

**规则**：
1. `docs-index.md` 必须同时引用 design/ 和 designs/
2. 路由表必须覆盖所有目录
3. 所有模板引用必须一致

---

### 6.4 关于 owner docs 职责表格

**推荐方案**：更新表格或创建目录

**选项 A：更新表格**（推荐）
- 移除不存在的目录（requirements/、architecture/、plans/、audits/）
- 只保留实际存在的目录

**选项 B：创建目录**
- 如果确实需要这些目录，创建它们并更新模板

---

## 七、下一步行动

1. **决策 design/ vs designs/**：明确划分规则
2. **统一引用**：更新 docs-index.md、CLAUDE.md、AGENTS.md
3. **更新 owner docs 职责表格**：确保与实际目录匹配
4. **更新 source-of-truth-and-precedence.md**：确保优先级与实际目录匹配
5. **更新测试脚本**：确保与实际模板一致
6. **更新 EVOLUTION.md**：记录本次决策

---

## 附录：相关文件

- `docs-pipeline/EVOLUTION.md` — 演进历史
- `docs-pipeline/SKILL.md` — 核心工作流
- `docs-pipeline/assets/templates/CLAUDE.md` — 行 231、235
- `docs-pipeline/assets/templates/AGENTS.md` — 行 169、173
- `docs-pipeline/assets/templates/docs-index.md` — 行 17、26、39、58、74
- `docs-pipeline/assets/templates/docs-CLAUDE.md` — owner docs 职责表格
- `docs-pipeline/assets/templates/context/source-of-truth-and-precedence.md` — 优先级定义
