# docs-pipeline

一键初始化或修复 Claude Code 项目的 `docs/` 产物链路结构。支持**文档跟随项目**和**独立文档仓库**两种模式。

基于 [AGE (Attractor-Guided Engineering)](https://github.com/entropy-cloud/attractor-guided-engineering-template) 增强：Task Routing + Planning Triggers + Verification Baseline。

## 参考项目

- [ddd-harness-microservices](https://github.com/domain-driven-design/ddd-harness-microservices) - DDD 微服务架构脚手架，包含完整的文档驱动开发流程

## 目录结构

```
docs-pipeline/
├── SKILL.md           # 核心指令文件
├── README.md          # 用户文档
├── USAGE.md           # 使用场景
├── ADVANCED.md        # 高级功能
├── CHANGELOG.md       # 更新日志
├── assets/templates/  # 模板文件
├── references/        # 参考文档
└── scripts/           # 测试脚本
    ├── test-modes.sh
    └── test-pipeline.sh
```

## 使用

在 Claude Code 里说：
- "初始化文档结构"
- "搭建 docs pipeline"
- "set up docs structure"

skill 会自动识别并执行。

## 文档模式

### 模式 A：文档跟随项目（默认）

`docs/` 在项目根目录下，与代码一起管理。

### 模式 B：独立文档仓库

文档在独立的 git 仓库中，通过环境变量指定：

```bash
export DOCS_ROOT=/path/to/docs/repo
```

或检测到 `docs/` 目录本身是一个独立的 git 仓库时自动启用。

## 产物链路

```
backlog → prd → design → exec-plans/active → exec-plans/completed
                                                  ↓
                                              lessons（踩坑教训）
```

## 核心目录（默认初始化）

| 目录 | 职责 |
|------|------|
| `docs/context/` | 强制 AI 上下文、真相优先级、项目约定 |
| `docs/backlog/` | 工作队列、AI 自主级别标签 |
| `docs/prd/` | 实现就绪的需求文档 |
| `docs/design/` | 稳定的应用层设计基线 |
| `docs/exec-plans/` | 执行计划（含 Plan/Closure 审计） |
| `docs/lessons/` | 可复用的工程教训 |
| `docs/standards/` | 开发规范（分层、API、DB、安全、命名），相对稳定 |
| `docs/designs/` | 系统设计现状（API、DB、业务规则、数据字典），高频更新 |

## 行为契约

| 状态 | 动作 |
|------|------|
| `docs/` 不存在 | 全新初始化（建 11 目录 + 15 模板 + 根级 AI 代理模板） |
| `docs/` 部分存在 | 修复模式，只补缺失项 |
| `docs/` 全部齐全 | 跳过，输出"已规范" |
| `.claude/commands/ideas.md` 不存在 | 写入 `/ideas` 随手记命令 |
| 项目根 `CLAUDE.md` 不存在 | 写入模板 |
| 项目根 `ARCHITECTURE.md` 不存在 | 调用 Explore 子代理探索后生成 |
| `.pensieve/` 存在且 CLAUDE.md 无 `## Pensieve 版本控制` | 追加版本控制规则（四层结构哪些提交、哪些排除） |
| `.pensieve/` 不存在 | 询问用户是否安装 Pensieve；确认则自动 init 并集成 |
| `DOCS_ROOT` 已设置或 `docs/.git` 存在 | 启用模式 B（独立文档仓库），路径引用自动适配 |
| **所有配置** | **主动询问用户确认，支持修改模式、路径、跳过项** |

## 交互流程

每次执行都会向用户展示检测结果并询问确认：

```
📋 docs-pipeline 配置检测

📌 文档模式：模式 A（文档跟随项目）
📁 文档根路径：./docs
📂 项目根路径：./
🔍 docs/ 状态：全新
📎 文档引用路径：docs/

请确认或修改：
1. 文档模式：模式 A / 模式 B
2. 文档根路径：./docs（可修改）
3. 是否跳过 ARCHITECTURE.md 生成？
4. 是否跳过 Pensieve 集成？
```

用户可修改任何配置项，确认后继续执行。

## 关键特性

- **幂等**：重复调用安全，不覆盖已有文件
- **零破坏**：从不删除用户内容；只新建或跳过
- **零依赖**：不假设技术栈，只管文档与 AI 代理配置
- **双模式**：支持文档跟随项目和独立文档仓库

## 完整规范

见 [SKILL.md](./SKILL.md)。

## 维护手册

见 [references/adding-templates.md](./references/adding-templates.md)。
