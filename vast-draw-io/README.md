# vast-draw-io

> 从自然语言生成专业 draw.io 图表的技能。支持 6 种图表预设、代码库可视化、10,000+ 官方形状、321 个 AI/LLM 品牌 logo，导出 PNG/SVG/PDF/JPG。

## 来源与溯源

### 主要来源（v1.14.0）

| 字段 | 值 |
| :--- | :--- |
| 仓库 | https://github.com/Agents365-ai/drawio-skill |
| 版本 | v1.14.0 |
| 作者 | [Agents365-ai](https://github.com/Agents365-ai) |
| 许可 | MIT License |
| 集成时间 | 2026-06-08 |

### 历史来源（已废弃）

| 字段 | 值 |
| :--- | :--- |
| 仓库 | [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) |
| 路径 | `skills/draw-io/` |
| 原始作者 | [@leonardocouy](https://github.com/leonardocouy) (Leonardo Flores) |
| 集成时间 | 2026-06-03 |

> ⚠️ **注意**：原 softaworks/agent-toolkit 的功能已被 Agents365-ai/drawio-skill 完全覆盖并增强。

### 同步方式

本目录以**快照**方式集成，未建立 git submodule / 远程跟踪。后续若上游更新：

```bash
cd .working && rm -rf drawio-skill
git clone --depth 1 https://github.com/Agents365-ai/drawio-skill.git
# 重新拷贝 skills/drawio-skill/* 到本目录
cp -r drawio-skill/skills/drawio-skill/* <vast-draw-io-path>/
```

---

## 技能结构

```
vast-draw-io/
├── README.md                     # 用户使用文档
├── SKILL.md                      # Agent 触发指令与工作流定义（486 行）
├── data/
│   ├── lobe-icons.json           # AI/LLM 品牌 logo 数据
│   ├── shape-index.json.gz       # 10,000+ 官方形状索引
│   └── SHAPE-INDEX-NOTICE.md     # 形状索引说明
├── references/
│   ├── autolayout.md             # Graphviz 自动布局文档
│   ├── aws-icons.md              # AWS 官方图标参考（28K）
│   ├── diagram-types.md          # 6 种图表类型预设
│   ├── layout-guidelines.md      # 布局规范
│   ├── shapes.md                 # 形状搜索使用指南
│   ├── style-extraction.md       # 样式提取流程
│   ├── style-presets.md          # 样式预设系统
│   └── troubleshooting.md        # 故障排除
├── scripts/
│   ├── aiicons.py                # AI/LLM 品牌 logo 解析
│   ├── autolayout.py             # Graphviz 自动布局
│   ├── convert-drawio-to-png.sh  # draw.io → PNG 转换
│   ├── encode_drawio_url.py      # 浏览器回退 URL 生成
│   ├── find_aws_icon.py          # AWS 图标查找
│   ├── goimports.py              # Go 项目 import 图提取
│   ├── jsimports.py              # JS/TS 项目 import 图提取
│   ├── pyclasses.py              # Python 类继承图提取
│   ├── pyimports.py              # Python 项目 import 图提取
│   ├── repair_png.py             # PNG 修复（IEND chunk）
│   ├── rustimports.py            # Rust 项目 import 图提取
│   ├── shapesearch.py            # 10,000+ 官方形状搜索
│   └── validate.py               # .drawio 结构验证
└── styles/
    ├── schema.json               # 预设 schema 定义
    └── built-in/
        ├── corporate.json        # 企业风格预设
        ├── default.json          # 默认预设
        └── handdrawn.json        # 手绘风格预设
```

---

## 核心能力

### 图表类型预设

| 类型 | 特性 |
| :--- | :--- |
| **架构图** | 云架构 / 微服务 / 系统拓扑，层级泳道，hub-center 策略 |
| **ML/DL 图** | Transformer / CNN / LSTM / GRU，张量形状标注，层类型颜色编码 |
| **流程图** | 业务流程 / 用户旅程 / 决策树，语义形状（平行四边形 I/O，菱形决策） |
| **UML** | 类图 / 时序图，继承/组合/聚合箭头，生命线 + 激活框 |
| **ER 图** | 数据库 schema 关系，表容器，PK/FK 表示法 |
| **其他** | 组织结构图、思维导图、线框图 |

### 代码库可视化

支持从现有代码自动生成结构图：

```bash
# Python / JS/TS / Go/Rust 项目 import 图
python3 scripts/pyimports.py   myproject --group -o graph.json
python3 scripts/jsimports.py   ./src     --group -o graph.json
python3 scripts/goimports.py   ./module  --group -o graph.json
python3 scripts/rustimports.py ./crate   --group -o graph.json

# Python 类继承图
python3 scripts/pyclasses.py   mypackage --group -o graph.json

# 任意 extractor → 自动布局 → 可编辑 .drawio
python3 scripts/autolayout.py  graph.json -o diagram.drawio
```

### 形状搜索

搜索 10,000+ 官方 draw.io 形状：

```bash
python3 scripts/shapesearch.py "aws lambda" --limit 5
python3 scripts/shapesearch.py "kubernetes pod" --limit 3
```

### AI/LLM 品牌 Logo

321 个现代 AI/LLM 品牌 logo（OpenAI, Claude, Gemini, Mistral, Llama, Ollama, LangChain...）：

```bash
python3 scripts/aiicons.py "claude" --json      # CDN 引用（默认）
python3 scripts/aiicons.py "openai" --embed     # 内联 data URI
```

### 样式预设

内置 3 种预设：`default`、`corporate`、`handdrawn`

```bash
# 使用预设
Draw a microservices architecture using my "corporate" style

# 学习新样式
Learn my style from ~/diagrams/brand.drawio as "mybrand"
```

### 自检 + 自动修复

- 导出 PNG 后自动读取并检查问题
- 自动修复重叠、标签裁剪、边堆叠等问题（最多 2 轮）
- 迭代反馈循环（最多 5 轮）

---

## 输出格式

| 格式 | 命令 | 说明 |
| :--- | :--- | :--- |
| PNG | `drawio -x -f png -s 2 -o output.png input.drawio` | 默认格式，支持 `--embed-diagram` |
| SVG | `drawio -x -f svg -o output.svg input.drawio` | 矢量格式，支持 `--embed-diagram` |
| PDF | `drawio -x -f pdf -o output.pdf input.drawio` | 支持 `--embed-diagram` |
| JPG | `drawio -x -f jpg -o output.jpg input.drawio` | 位图格式 |

---

## 安装

### 1. 安装 draw.io Desktop CLI

| 平台 | 命令 |
| :--- | :--- |
| macOS | `brew install --cask drawio` |
| Windows | [下载安装包](https://github.com/jgraph/drawio-desktop/releases) |
| Linux | `.deb`/`.rpm` from [releases](https://github.com/jgraph/drawio-desktop/releases)；`sudo apt install xvfb` for headless |

验证：`drawio --version`

### 2. 安装技能

```bash
# Claude Code
cp -r vast-draw-io ~/.claude/skills/

# 其他 Agent（Claude Code, Cursor, Copilot, OpenClaw, Codex, Hermes）
npx skills add Agents365-ai/365-skills -g
```

### 3. 可选依赖

自动布局需要 Graphviz：

```bash
# macOS
brew install graphviz

# Linux
sudo apt install graphviz
```

---

## 触发词

> "drawio diagram" · "draw.io diagram" · "create architecture diagram" · "AWS architecture" · "network topology" · "system architecture" · "flowchart" · "export to PNG" · "convert drawio" · "ER diagram" · "UML class" · "sequence diagram" · "ML model diagram" · "visualize codebase" · "class hierarchy"

---

## 使用示例

### 微服务架构

```
Create a microservices e-commerce architecture with Mobile/Web/Admin clients,
API Gateway (auth + rate limiting + routing), Auth/User/Order/Product/Payment
services, Kafka message queue, Notification service, and User DB / Order DB /
Product DB / Redis Cache / Stripe API
```

### ML 模型

```
Draw a Transformer encoder-decoder for machine translation: 6-layer encoder
with self-attention, 6-layer decoder with cross-attention, input embeddings
(batch × 512 × 768), positional encoding, and a final output projection.
Annotate tensor shapes between layers and color-code by layer type.
```

### 代码库可视化

```
Visualize the module structure of this Python project
```

```
Draw the class hierarchy of mypackage
```

---

## 故障排除

详见 [references/troubleshooting.md](references/troubleshooting.md)

常见问题：
- CLI 不可用：尝试 `drawio`、`draw.io`、或 macOS 直接路径
- PNG 导出失败：确保未在预览步骤使用 `-e` 参数
- Vision API 400 错误：预览 PNG 不要使用 `-e` 参数，宽度限制 2000px

---

## 致谢

- **[Agents365-ai](https://github.com/Agents365-ai)** — 主要来源，drawio-skill 作者
- **[softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit)** — 历史来源（Leonardo Flores）
- **draw.io** ([diagrams.net](https://app.diagrams.net/)) — 图表格式与渲染引擎
- **[lobe-icons](https://github.com/lobehub/lobe-icons)** — AI/LLM 品牌 logo 数据源
- **AWS Architecture Icons** — AWS 官方图标集
- **本项目 ([vast-dev-skill](https://github.com/0x43e96f/vast-dev-skill))** — 集成归档

## 许可与版权

- 本目录的所有内容遵循 **MIT License**
- Agents365-ai/drawio-skill: Copyright (c) 2026 Agents365-ai
- softaworks/agent-toolkit: Copyright (c) 2026 Leonardo Flores
- 本目录的"集成说明 / 同步方式"部分为本项目补充，遵循本项目 MIT License
