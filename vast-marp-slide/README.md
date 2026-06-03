# vast-marp-slide

> 集成自 [VastFuture/agent-toolkit](https://github.com/VastFuture/agent-toolkit/tree/main/skills/marp-slide)（fork 自 [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit)）的 Marp 幻灯片生成技能。
> 用 **Marp**（Markdown Presentation Ecosystem）语法把 Markdown 转换为 HTML 幻灯片，内置 7 套主题（default / business / colorful / dark / gradient / minimal / tech）+ 7 套模板。

## 来源与溯源

> ⚠️ **重要：双源声明**。用户提供的链接指向 VastFuture 的 fork，但 VastFuture 在 fork 后**未对 `marp-slide/` 路径做任何独立改动**（路径下仅有 1 个 commit，即上游 PR #16 同步带过来的 `CONTRIBUTING.md` 提交）。所有内容真实来源是 **softaworks/agent-toolkit**。

| 字段 | 值 |
| :--- | :--- |
| 用户指定链接 | https://github.com/VastFuture/agent-toolkit/tree/main/skills/marp-slide |
| 直接仓库（fork） | [VastFuture/agent-toolkit](https://github.com/VastFuture/agent-toolkit) |
| 真实上游仓库 | [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) |
| 路径 | `skills/marp-slide/` |
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
git sparse-checkout set skills/marp-slide
# 重新拷贝 skills/marp-slide/* 到本目录
```

---

## 技能结构

```
vast-marp-slide/                                  # 23 文件 / 132K
├── README.md                                     # 用户使用文档
├── SKILL.md                                      # Agent 触发指令与工作流
├── assets/
│   ├── template-{basic,business,colorful,dark,gradient,minimal,tech}.md  # 7 套 Markdown 模板
│   └── theme-{default,business,colorful,dark,gradient,minimal,tech}.css  # 7 套 CSS 主题
└── references/
    ├── marp-syntax.md          # 完整 Marp 语法参考
    ├── best-practices.md       # 最佳实践
    ├── advanced-features.md    # 高级特性（背景图、片段、数学公式等）
    ├── image-patterns.md       # 图片与背景用法
    ├── official-themes.md      # 官方主题介绍
    ├── theme-selection.md      # 主题选择指南
    └── theme-css-guide.md      # 自定义 CSS 指南
```

---

## 技能能力

用 Marp 语法生成**单文件 Markdown** → **HTML 幻灯片**，支持：

- 标准 Marpit 语法（`---` 分页指令 + `<!-- theme: ... -->` 主题）
- 7 套开箱即用主题（default / business / colorful / dark / gradient / minimal / tech）
- 7 套场景化模板（开场 / 商务 / 彩页 / 深色 / 渐变 / 极简 / 科技）
- 背景图、渐变、自定义 CSS
- 数学公式（KaTeX）、代码高亮、Mermaid 图嵌入
- 导出 HTML / PDF / PPTX

### 触发词

> "create slides" · "Marp presentation" · "Markdown slides" · "Marpit" · "convert markdown to slides" · "presentation deck" · "deck in Marp"

### 输出格式

- 主输出：HTML 幻灯片（可在浏览器播放 + 打印 PDF）
- 可选：导出 PDF / PPTX
- 源文件：单个 `.md`（便于版本控制与协作编辑）

### 主题快速选择

| 主题 | 适用场景 |
| :--- | :--- |
| **default** | 通用 / 内部汇报 |
| **business** | 商务演示、客户提案 |
| **tech** | 技术分享、工程评审 |
| **dark** | 演讲、舞台展示、视觉冲击 |
| **minimal** | 设计评审、极简风格 |
| **gradient** | 产品发布、市场活动 |
| **colorful** | 培训、教学、互动场景 |

---

## 使用方法

### Claude Code

```bash
# 单技能安装
cp -r vast-marp-slide ~/.claude/skills/
```

调用示例：

> "Create a tech talk deck for our Q3 architecture review, use the dark theme"
>
> "Convert this outline into a Marp presentation with the business theme"
>
> "Make a 10-slide product launch deck, gradient theme"

### 系统依赖

- [Marp CLI](https://github.com/marp-team/marp-cli)（`@marp-team/marp-cli`）— 用于本地渲染
- 或 [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode) 扩展
- 或 [Marp Web](https://web.marp.app/) 在线编辑器

具体命令详见 `SKILL.md` 工作流。

---

## 致谢

- **Leonardo Flores** ([@leonardocouy](https://github.com/leonardocouy)) — 原始作者，版权所有
- **[softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit)** — 真实上游仓库
- **[VastFuture/agent-toolkit](https://github.com/VastFuture/agent-toolkit)** — 用户指定的 fork 镜像
- **[Marp](https://marp.app/)** — Markdown Presentation Ecosystem
- **本项目 ([vast-dev-skill](https://github.com/0x43e96f/vast-dev-skill))** — 集成归档

## 许可与版权

- 本目录的所有 `*.md` 与 `*.css` 内容遵循 **MIT License** — Copyright (c) 2026 Leonardo Flores
- 完整 LICENSE 文本见上游 [softaworks/agent-toolkit/LICENSE](https://github.com/softaworks/agent-toolkit/blob/main/LICENSE)
- 本目录的"集成说明 / 同步方式"部分为本项目补充，遵循本项目 MIT License
