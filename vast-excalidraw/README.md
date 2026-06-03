# vast-excalidraw

> 集成自 [VastFuture/agent-toolkit](https://github.com/VastFuture/agent-toolkit/tree/main/skills/excalidraw)（fork 自 [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit)）的 Excalidraw 图表生成与编辑技能。
> 通过 **subagent 委托** 处理 `.excalidraw` / `.excalidraw.json` 文件，避免大 JSON 撑爆主 context window。

## 来源与溯源

> ⚠️ **重要：双源声明**。用户提供的链接指向 VastFuture 的 fork，但 VastFuture 在 fork 后**未对 `excalidraw/` 路径做任何独立改动**（路径下仅有 1 个 commit，即上游 PR #16 同步带过来的 `CONTRIBUTING.md` 提交）。所有内容真实来源是 **softaworks/agent-toolkit**。

| 字段 | 值 |
| :--- | :--- |
| 用户指定链接 | https://github.com/VastFuture/agent-toolkit/tree/main/skills/excalidraw |
| 直接仓库（fork） | [VastFuture/agent-toolkit](https://github.com/VastFuture/agent-toolkit) |
| 真实上游仓库 | [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) |
| 路径 | `skills/excalidraw/` |
| 集成时 Commit SHA | `3027f20f3181758385a1bb8c022d4041dfb4de84` |
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
git sparse-checkout set skills/excalidraw
# 重新拷贝 skills/excalidraw/* 到本目录
```

---

## 技能结构

```
vast-excalidraw/
├── README.md    # 用户使用文档（10K）
└── SKILL.md     # Agent 触发指令与 subagent 委托工作流（8K）
```

> 本路径**没有** `references/` 或 `scripts/` 子目录 —— 与同仓库的 `c4-architecture` / `draw-io` 相比更精简。完整 Excalidraw 操作能力封装在 `SKILL.md` 内的 subagent 协议中。

---

## 技能能力

为 Claude Code 智能处理 Excalidraw 图表：

### 核心问题与解法

Excalidraw 文件本质上是冗长的 JSON 格式。**单个文件 4K–22K tokens**，经常超出主 context 的可读范围。**直接把整个 JSON 读进主 context 会撑爆**。

本技能的核心设计：**所有 Excalidraw 操作委托给 subagent**，主 context 只持有指令和结果摘要，不直接接触 JSON。

### 触发词

- 用户提供 `*.excalidraw` 或 `*.excalidraw.json` 文件
- 用户提到 "diagram" / "flowchart" / "architecture visualization"
- 用户请求创建 / 编辑 / 转换 Excalidraw 图表

### 工作流

1. **Main agent** 接收指令（如"修改这张图"）
2. **Main agent** 启动 **subagent**，将文件路径 + 指令传入
3. **Subagent** 用 Excalidraw CLI / API 读取/编辑/保存
4. **Subagent** 返回结构化摘要（如"修改了 3 个元素，更新了 2 个箭头连接"）
5. **Main agent** 拿到摘要，context 完全不被 JSON 污染

---

## 使用方法

### Claude Code

```bash
# 单技能安装
cp -r vast-excalidraw ~/.claude/skills/
```

调用示例：

> "Read the diagram in `docs/architecture.excalidraw` and add a new component for the auth service"
>
> "Convert this Excalidraw file to PNG"
>
> "Create a new system architecture diagram and save as `auth-flow.excalidraw`"

### 系统依赖

- Excalidraw CLI（可选，用于程序化编辑）
- 或浏览器访问 [excalidraw.com](https://excalidraw.com/) 直接打开/编辑

具体依赖请查阅 `SKILL.md`。

---

## 与同仓库其他集成技能的关系

| 技能 | 图表格式 | 适用场景 |
| :--- | :--- | :--- |
| `vast-c4-architecture` | Mermaid C4 | 多层级架构图（Context→Container→Component→Deployment） |
| `vast-draw-io` | `.drawio` | AWS 架构 / 网络拓扑 / 含官方图标 |
| `vast-excalidraw` | `.excalidraw` | 手绘风 / 快速草图 / 协作白板 |

> 三者可互补：根据受众与目标选工具，不要混用同一张图。

---

## 致谢

- **Leonardo Flores** ([@leonardocouy](https://github.com/leonardocouy)) — 原始作者，版权所有
- **[softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit)** — 真实上游仓库
- **[VastFuture/agent-toolkit](https://github.com/VastFuture/agent-toolkit)** — 用户指定的 fork 镜像
- **[Excalidraw](https://excalidraw.com/)** — 手绘风白板工具
- **本项目 ([vast-dev-skill](https://github.com/0x43e96f/vast-dev-skill))** — 集成归档

## 许可与版权

- 本目录的所有 `*.md` 内容遵循 **MIT License** — Copyright (c) 2026 Leonardo Flores
- 完整 LICENSE 文本见上游 [softaworks/agent-toolkit/LICENSE](https://github.com/softaworks/agent-toolkit/blob/main/LICENSE)
- 本目录的"集成说明 / 同步方式"部分为本项目补充，遵循本项目 MIT License
