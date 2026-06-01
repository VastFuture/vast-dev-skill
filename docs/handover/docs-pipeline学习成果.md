# docs-pipeline 技能学习成果

## 技能定位

docs-pipeline 是一个用于初始化或修复 Claude Code 项目文档结构的技能，支持模式 A（文档跟随项目）和模式 B（独立文档仓库）两种模式。

## 核心功能

### 模式 A：文档跟随项目（默认）

```
项目根/
├── CLAUDE.md                 # Linus 角色 + 沟通规范 + 通用开发规则模板
├── AGENTS.md                 # Codex CLI 全局指令
├── MBTI_DEV_TRAPS.md         # 16 种人格陷阱清单
├── karpathy-guidelines.md    # LLM 编码行为指南
├── ARCHITECTURE.md           # 自动探索生成的项目架构文档
├── .mcp.json                # 7 个常用 MCP 服务配置
├── .claude/
│   └── commands/
│       └── ideas.md          # /ideas 随手记命令
└── docs/
    ├── CLAUDE.md             # 文档总规则
    ├── ideas/                # 灵感池
    ├── research/             # 研究资料
    ├── prd/                  # 产品需求文档
    ├── exec-plans/           # 执行计划（active/completed）
    ├── handover/             # 交接文档
    ├── issues/               # Bug 追踪
    └── lessons/              # 经验教训
```

### 模式 B：独立文档仓库

当 `docs/` 是一个独立的 git 仓库时触发，适合文档与代码分离管理的项目。

## 关键设计原则

| 原则 | 说明 |
|------|------|
| **幂等** | 重复调用得到相同结果，已有文件不覆盖 |
| **不智能 merge** | 冲突就报警，不自动合并 |
| **不删除** | 只新建/跳过，从不删用户已有内容 |
| **不破坏** | 项目根 CLAUDE.md 只追加，不修改原有内容 |
| **不假设技术栈** | 只管文档与 AI 代理配置，不碰业务代码 |

## 工作流程

1. **检测模式** — 检查环境变量 `DOCS_ROOT` 或 `docs/.git`
2. **主动确认** — 向用户展示检测结果并确认配置
3. **检测状态** — 全新初始化 / 部分存在 / 已齐全
4. **建目录** — 创建标准的 docs 目录结构
5. **写模板** — 复制模板到目标路径（已存在则跳过）
6. **写根级 AI 代理模板** — CLAUDE.md、AGENTS.md 等
7. **Pensieve 集成** — 可选的笔记版本控制集成
8. **生成 ARCHITECTURE.md** — 通过 Explore 子代理基于项目代码生成
9. **输出报告** — 汇总执行结果

## 模板映射

| 模板文件 | 目标路径 |
|---------|---------|
| `assets/templates/docs-CLAUDE.md` | `docs/CLAUDE.md` |
| `assets/templates/ideas-README.md` | `docs/ideas/README.md` |
| `assets/templates/research-README.md` | `docs/research/README.md` |
| `assets/templates/prd-README.md` | `docs/prd/README.md` |
| `assets/templates/exec-plans-README.md` | `docs/exec-plans/README.md` |
| `assets/templates/handover-README.md` | `docs/handover/README.md` |
| `assets/templates/issues-README.md` | `docs/issues/README.md` |
| `assets/templates/lessons-README.md` | `docs/lessons/README.md` |
| `assets/templates/CLAUDE.md` | `CLAUDE.md` |
| `assets/templates/AGENTS.md` | `AGENTS.md` |
| `assets/templates/MBTI_DEV_TRAPS.md` | `MBTI_DEV_TRAPS.md` |
| `assets/templates/karpathy-guidelines.md` | `karpathy-guidelines.md` |
| `assets/templates/mcp.json` | `.mcp.json` |

## 重要 Gotchas

- Explore 子代理超时或返回空内容时，降级到骨架模板
- 项目根 CLAUDE.md 已有自定义内容时，只追加"## 文档"段落到末尾
- 重复调用后误报"已建"：必须用 `Read` 确认文件实际存在
- Pensieve 不存在时强制创建：`.pensieve/` 不存在就跳过
- 模式 B 路径引用必须是正确的相对路径

## 与本项目的关联

vast-dev-skill 项目中的 `docs-pipeline` 技能实现了上述完整功能，模板文件位于 `docs-pipeline/assets/templates/`。