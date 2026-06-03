# vast-c4-architecture

> 集成自 [VastFuture/agent-toolkit](https://github.com/VastFuture/agent-toolkit/tree/main/skills/c4-architecture)（fork 自 [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit)）的 C4 架构图生成技能。
> 用 Mermaid 语法绘制 C4 模型图（Context / Container / Component / Deployment / Dynamic），输出到 `docs/architecture/`。

## 来源与溯源

> ⚠️ **重要：双源声明**。用户提供的链接指向 VastFuture 的 fork，但 VastFuture 在 fork 后**未对 `c4-architecture/` 路径做任何独立改动**（路径下仅有 1 个 commit，即上游 PR #16 同步带过来的 `CONTRIBUTING.md` 提交）。所有内容真实来源是 **softaworks/agent-toolkit**。

| 字段 | 值 |
| :--- | :--- |
| 用户指定链接 | https://github.com/VastFuture/agent-toolkit/tree/main/skills/c4-architecture |
| 直接仓库（fork） | [VastFuture/agent-toolkit](https://github.com/VastFuture/agent-toolkit) |
| 真实上游仓库 | [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) |
| 路径 | `skills/c4-architecture/` |
| 集成时 Commit SHA | `3027f20f3181758385a1bb8c022d4041dfb4de84`（含 c4-architecture 的最新快照） |
| 集成时间 | 2026-06-03 |
| Fork 关系 | VastFuture/agent-toolkit forked from softaworks/agent-toolkit |
| 原始作者 | [@leonardocouy](https://github.com/leonardocouy) (Leonardo Flores) |
| 版权 / 许可 | **MIT License** — Copyright (c) 2026 Leonardo Flores |
| 上游安装命令 | `npx skills add softaworks/agent-toolkit`（支持 Claude Code / Codex / Cursor 等） |

### 同步方式

本目录以**快照**方式集成，未建立 git submodule / 远程跟踪。后续若上游更新：

```bash
cd .working && rm -rf agent-toolkit
git clone --depth 1 --filter=blob:none --sparse https://github.com/softaworks/agent-toolkit.git
cd agent-toolkit
git sparse-checkout set skills/c4-architecture
# 重新拷贝 skills/c4-architecture/* 到本目录
```

---

## 技能结构

```
vast-c4-architecture/
├── README.md              # 用户使用文档（生成哪些图、用法示例、最佳实践）
├── SKILL.md               # Agent 触发指令与工作流定义
└── references/
    ├── c4-syntax.md       # 完整 Mermaid C4 语法参考
    ├── common-mistakes.md # 反模式 / 常见错误清单
    └── advanced-patterns.md  # 微服务、事件驱动、部署等高级模式
```

---

## 技能能力

用 Mermaid C4 语法生成 5 个层级的架构图：

| Level | 名称 | 受众 | 内容 | 是否必须 |
| :---: | :--- | :--- | :--- | :---: |
| 1 | **C4Context** | 所有人 | 系统 + 外部角色 | ✅ 始终 |
| 2 | **C4Container** | 技术 | 应用、数据库、服务 | ✅ 始终 |
| 3 | **C4Component** | 开发者 | 内部组件 | ⬜ 视价值 |
| 4 | **C4Deployment** | DevOps | 基础设施节点 | ⬜ 生产系统 |
| - | **C4Dynamic** | 技术 | 编号请求流 | ⬜ 复杂工作流 |

> 关键洞察：**Context + Container 已足够大多数团队**，Component/Code 图只在确实增加价值时再画。

### 触发词

> "architecture diagram" · "C4 diagram" · "system context" · "container diagram" · "component diagram" · "deployment diagram" · "document architecture" · "visualize architecture"

### 输出位置

架构文档写入 `docs/architecture/`，命名约定：

- `c4-context.md` — System Context 图
- `c4-containers.md` — Container 图
- `c4-components-{feature}.md` — 按 feature 拆分的 Component 图
- `c4-deployment.md` — Deployment 图
- `c4-dynamic-{flow}.md` — 按 flow 命名的 Dynamic 图

### 核心原则（节选自 SKILL.md）

1. **每个元素必须有**：Name、Type、Technology（适用时）、Description
2. **单向箭头** — 双向箭头制造歧义
3. **箭头用动词标签** — "Sends email using" / "Reads from"，不只写 "uses"
4. **技术标签** — "JSON/HTTPS" / "JDBC" / "gRPC"
5. **每图 ≤ 20 个元素** — 复杂系统拆成多张图

---

## 使用方法

### Claude Code

```bash
# 单技能安装
cp -r vast-c4-architecture ~/.claude/skills/
```

然后在 Claude Code 中用触发词调用，例如：

> "Create architecture diagrams for my workout tracker app"

### Cursor / Codex / 其他 Agent

由于遵循 [Agent Skills](https://agentskills.io/) 格式，理论上可兼容，但需要相应 host 支持。

---

## 致谢

- **Leonardo Flores** ([@leonardocouy](https://github.com/leonardocouy)) — 原始作者，版权所有
- **[softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit)** — 真实上游仓库
- **[VastFuture/agent-toolkit](https://github.com/VastFuture/agent-toolkit)** — 用户指定的 fork 镜像
- **本项目 ([vast-dev-skill](https://github.com/0x43e96f/vast-dev-skill))** — 集成归档

## 许可与版权

- 本目录的所有 `*.md` 内容（含 `SKILL.md` / `README.md` / `references/`）遵循 **MIT License** — Copyright (c) 2026 Leonardo Flores
- 完整 LICENSE 文本见上游 [softaworks/agent-toolkit/LICENSE](https://github.com/softaworks/agent-toolkit/blob/main/LICENSE)
- 本目录的"集成说明 / 同步方式"部分为本项目补充，遵循本项目 MIT License
