# vast-draw-io

> 集成自 [VastFuture/agent-toolkit](https://github.com/VastFuture/agent-toolkit/tree/main/skills/draw-io)（fork 自 [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit)）的 draw.io 架构图生成技能。
> 生成 draw.io 格式的架构图 / 流程图 / 网络拓扑图，可导出为 PNG/SVG，并支持 AWS 官方图标查找。

## 来源与溯源

> ⚠️ **重要：双源声明**。用户提供的链接指向 VastFuture 的 fork，但 VastFuture 在 fork 后**未对 `draw-io/` 路径做任何独立改动**（路径下仅有 1 个 commit，即上游 PR #16 同步带过来的 `CONTRIBUTING.md` 提交）。所有内容真实来源是 **softaworks/agent-toolkit**。

| 字段 | 值 |
| :--- | :--- |
| 用户指定链接 | https://github.com/VastFuture/agent-toolkit/tree/main/skills/draw-io |
| 直接仓库（fork） | [VastFuture/agent-toolkit](https://github.com/VastFuture/agent-toolkit) |
| 真实上游仓库 | [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) |
| 路径 | `skills/draw-io/` |
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
git sparse-checkout set skills/draw-io
# 重新拷贝 skills/draw-io/* 到本目录
```

---

## 技能结构

```
vast-draw-io/
├── README.md                 # 用户使用文档
├── SKILL.md                  # Agent 触发指令与工作流定义
├── references/
│   ├── layout-guidelines.md  # 布局规范
│   └── aws-icons.md          # AWS 官方图标完整参考（28K）
└── scripts/
    ├── convert-drawio-to-png.sh  # draw.io → PNG 转换脚本（保留执行权限）
    └── find_aws_icon.py          # AWS 图标 ID 查找工具
```

> 📦 脚本已保留 Linux 执行权限（`0755`）。Windows 用户在集成时可能需要重新 `chmod`。

---

## 技能能力

为任何系统生成 **draw.io** 格式（`.drawio`）的图表，支持：

- **架构图** — 云架构 / 微服务 / 系统拓扑
- **流程图** — 业务流程 / 用户旅程 / 决策树
- **网络拓扑** — VPC / 子网 / 安全组 / 负载均衡
- **时序图** — 序列交互（draw.io 原生支持）
- **组织结构图** — 树形层级
- **ER 图** — 数据库 schema 关系

### 触发词

> "drawio diagram" · "draw.io diagram" · "create architecture diagram" · "AWS architecture" · "network topology" · "system architecture" · "flowchart" · "export to PNG" · "convert drawio"

### 输出格式

- 主输出：`.drawio` XML 文件（draw.io 官方格式，可用 https://app.diagrams.net/ 打开）
- 可选：导出 PNG / SVG / PDF（通过 `scripts/convert-drawio-to-png.sh`）

### 核心能力

- **AWS 官方图标** — 200+ 预制 AWS 服务图标（EC2/S3/RDS/Lambda/VPC 等），通过 `scripts/find_aws_icon.py` 一键查找
- **布局规范** — 自动对齐、最小重叠、合理间距（见 `references/layout-guidelines.md`）
- **PNG 转换** — CLI 脚本批量转换 `.drawio` → `.png`

---

## 使用方法

### Claude Code

```bash
# 单技能安装
cp -r vast-draw-io ~/.claude/skills/
```

调用示例：

> "Create an AWS architecture diagram for a 3-tier web app with ALB, ECS, and RDS"
>
> "Draw a network topology showing VPC, public/private subnets, and NAT gateway"

### 系统依赖

使用 PNG 转换脚本需要：

- `drawio` CLI（[drawio-desktop](https://github.com/jgraph/drawio-desktop/releases) 命令行版本）
- 或 `xvfb-run` + drawio-desktop（headless 环境）

详见 `scripts/convert-drawio-to-png.sh` 头部说明。

---

## 致谢

- **Leonardo Flores** ([@leonardocouy](https://github.com/leonardocouy)) — 原始作者，版权所有
- **[softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit)** — 真实上游仓库
- **[VastFuture/agent-toolkit](https://github.com/VastFuture/agent-toolkit)** — 用户指定的 fork 镜像
- **draw.io** ([diagrams.net](https://app.diagrams.net/)) — 图表格式与渲染引擎
- **AWS Architecture Icons** — AWS 官方图标集
- **本项目 ([vast-dev-skill](https://github.com/0x43e96f/vast-dev-skill))** — 集成归档

## 许可与版权

- 本目录的所有 `*.md` 与 `scripts/*` 内容遵循 **MIT License** — Copyright (c) 2026 Leonardo Flores
- 完整 LICENSE 文本见上游 [softaworks/agent-toolkit/LICENSE](https://github.com/softaworks/agent-toolkit/blob/main/LICENSE)
- 本目录的"集成说明 / 同步方式"部分为本项目补充，遵循本项目 MIT License
