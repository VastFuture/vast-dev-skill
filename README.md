# vast-dev-skill

> 一套面向 Claude Code / Gemini CLI 的 AI Agent 技能合集。

本项目致力于提供一套完整的 AI 辅助开发与办公技能，涵盖了从需求分析、方案设计、编码执行、代码审查到可视化展示的全流程。

---

## 🚀 核心技能概览

### 🛠️ 开发工作流 (Development Workflow)
| 技能名称 | 说明 | 对应目录 |
| :--- | :--- | :--- |
| **vast-dev-kickoff-pua** | 高代理开发循环引擎：规划 → 执行 → 审查 → 验证 → 提交。内置失败压力升级机制。 | `vast-dev-kickoff-pua` |
| **vast-dev-kickoff** | 先问你再动手：通过 Interview Me 技术收敛需求，避免盲目编码。 | `vast-dev-kickoff` |
| **vast-dev-office-hours** | 6 个强制性问题，迫使你在动手前想清楚产品的核心价值。 | `vast-dev-office-hours` |
| **vast-dev-challenge** | 引入第二个 AI 模型（对抗性验证）来挑毛病，只找问题，不提方案。 | `vast-dev-challenge` |
| **vast-dev-brainstorming** | 在任何创意工作前，先探索意图、需求和设计。 | `vast-dev-brainstorming` |
| **vast-dev-arch-top** | 具有五层结构（策略、功能、交互、数据模型、视觉）的项目开发宪法。 | `vast-dev-arch-top` |
| **vast-dev-taste-checker** | 使用 Linus Torvalds 的 "Good Taste" 哲学审查代码。 | `vast-dev-taste-checker` |
| **vast-dev-project-analyzer** | 深度代码库分析，生成架构、模块、测试和部署的白皮书。 | `vast-dev-project-analyzer` |

### 📊 产品管理 (Product Management)
| 技能名称 | 说明 | 对应目录 |
| :--- | :--- | :--- |
| **vast-pm-prd-writer** | 将模糊、碎片的原始需求转化为结构化、可评审的 PRD 文档。 | `vast-pm-prd-writer` |
| **vast-pm-product-describer** | 运用“六维法”描述产品，生成高质量原型开发指令。 | `vast-pm-product-describer` |
| **vast-pm-roadmap-planner** | 从目标、产能、依赖出发，设计可执行的版本路线图。 | `vast-pm-roadmap-planner` |
| **vast-pm-prd-design-expert** | 根据用户故事创建产品需求规格说明书。 | `vast-pm-prd-design-expert` |
| **vast-lenny-pm-skills** | 集成自 [wuwu119/lenny-pm-skills](https://github.com/wuwu119/lenny-pm-skills) 的 86 个产品管理技能（中文版），覆盖 PM/领导力/AI 技术/增长/营销/职业/销售/工程/设计十大领域。 | `vast-lenny-pm-skills` |

### 🎨 视觉与可视化 (Visualization)
| 技能名称 | 说明 | 对应目录 |
| :--- | :--- | :--- |
| **vast-draw-tech-graph** | 生产级 SVG 技术架构图生成与导出 (支持 7 种专业风格)。 | `vast-draw-tech-graph` |
| **vast-draw-mermaid** | 自动生成流程图、架构图、时序图等 Mermaid 图表。 | `vast-draw-mermaid` |
| **vast-draw-thinking-logic** | 将复杂信息转换为清晰的视觉思维模型。 | `vast-draw-thinking-logic` |
| **vast-draw-visual-card-designer** | 将长内容转换为逻辑模型或极简图形风格的竖屏卡片。 | `vast-draw-visual-card-designer` |
| **vast-social-xhs-card** | 生成小红书/Instagram 风格的视觉知识卡片。 | `vast-social-xhs-card` |
| **vast-c4-architecture** | 集成自 [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) 的 C4 架构图生成技能（Mermaid C4: Context / Container / Component / Deployment / Dynamic）。 | `vast-c4-architecture` |
| **vast-draw-io** | 集成自 [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) 的 draw.io 图表生成技能（含 200+ AWS 官方图标、PNG 转换脚本）。 | `vast-draw-io` |
| **vast-excalidraw** | 集成自 [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) 的 Excalidraw 图表技能，通过 subagent 委托处理大 JSON 避免 context 爆炸。 | `vast-excalidraw` |

### 📖 内容处理与工具 (Content & Tools)
| 技能名称 | 说明 | 对应目录 |
| :--- | :--- | :--- |
| **vast-markdown-proxy** | 获取任何 URL（含微信、飞书、X）的干净 Markdown 内容。 | `vast-markdown-proxy` |
| **vast-universal-system-prompt** | 量子织锦认知引擎框架，激活深度思考模式。 | `vast-universal-system-prompt` |
| **vast-md-translator/summarizer** | Markdown 文件的专业翻译与结构化总结。 | `vast-md-translator/summarizer` |
| **vast-social-xhs-content-script** | 生成小红书爆款文案和口播脚本。 | `vast-social-xhs-content-script` |
| **vast-skill-recommender** | 维护并展示本项目及其他推荐技能列表。 | `vast-skill-recommender` |
| **vast-marp-slide** | 集成自 [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) 的 Marp 幻灯片技能，Markdown → HTML 演示文稿（7 主题 + 7 模板）。 | `vast-marp-slide` |

### 🛡️ 专家评审与代码质量 (Review & Quality)
| 技能名称 | 说明 | 对应目录 |
| :--- | :--- | :--- |
| **vast-pragmatic-clean-code-reviewer** | 严格遵循 Clean Code & Pragmatic Programmer 准则的代码审查。 | `vast-pragmatic-clean-code-reviewer` |
| **vast-code-review-expert** | 以高级工程师视角检测 SOLID 违反、安全风险。 | `vast-code-review-expert` |
| **vast-agent-skill-reviewer** | 审查 Agent Skill 目录和 SKILL.md 实现是否符合最佳实践。 | `vast-agent-skill-reviewer` |

### 📈 交易决策 (Trading)
| 技能名称 | 说明 | 对应目录 |
| :--- | :--- | :--- |
| **vast-trading-cognitive-guardrails** | 反确认偏误协议：确保客观、中立的财务投资分析。 | `vast-trading-cognitive-guardrails` |

---

## 📦 安装与使用

### 安装

本项目技能支持通过 `skills add` 或手动复制安装。

```bash
# 克隆仓库
git clone https://github.com/0x43e96f/vast-dev-skill.git ~/vast-dev-skill

# 安装示例 (以 kickoff 为例)
cp -r ~/vast-dev-skill/vast-dev-kickoff ~/.claude/skills/
```

> 注：部分技能依赖环境变量（如 `FEISHU_APP_ID`）或本地工具（如 `playwright`、`rsvg-convert`），请查阅各技能目录下的 `SKILL.md`。

### 推荐工作流

1. **构思阶段**: `/brainstorming` -> `/arch-top`
2. **需求对齐**: `/kickoff` -> `/office-hours` -> `/pm-prd-writer`
3. **执行循环**: `/kickoff-pua` (自动包含计划、执行、审查、提交)
4. **可视化**: `/draw-tech-graph` (用于文档配图)

---

## 🤝 致谢

- [tanweai/pua](https://github.com/tanweai/pua) — 压力升级概念
- [garrytan/gstack](https://github.com/garrytan/gstack) — office-hours 强制问题
- [obra/superpowers](https://github.com/obra/superpowers) — 核心开发技能灵感
- [r.jina.ai](https://r.jina.ai) — Markdown 转换服务
- [wuwu119/lenny-pm-skills](https://github.com/wuwu119/lenny-pm-skills) — 86 个产品管理技能中文版（基于 [Lenny's Newsletter](https://www.lennysnewsletter.com/) 洞察，[Refound AI](https://refoundai.com/lenny-skills/) 授权翻译）
- [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) — c4-architecture / draw-io 架构图技能（作者 [@leonardocouy](https://github.com/leonardocouy)，MIT License）

## ⚖️ License

MIT
