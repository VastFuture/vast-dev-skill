# vast-sanyuan-wiki-ingest

## 来源 (Source)

**上游仓库**：[sanyuan0704/sanyuan-skills](https://github.com/sanyuan0704/sanyuan-skills/tree/main/skills/wiki-ingest)
**上游路径**：`skills/wiki-ingest/SKILL.md`
**同步方式**：手动拷贝（非 git clone / 非 submodule）
**同步日期**：2026-09-18

## 与 `vast-wiki-ingest` 的核心区别

| 维度 | vast-wiki-ingest | vast-sanyuan-wiki-ingest |
|---|---|---|
| 设计哲学 | 摄入管道：raw → 摘要/概念/实体 | 实体提取：直接抽取概念 → 建页 |
| 目录结构 | `raw/` + `摘要/` + `概念/` + `实体/` | `concepts/` + `products/` + `patterns/` + `comparisons/` |
| 输入类型 | URL / Markdown / 对话汇总 | 文件路径 / 目录批量 / 粘贴文本 |
| 跨引用 | 提到 Obsidian 兼容 | 明确指定 `[[category/page-name]]` 格式 |
| 语言 | 中文 | 英文 |

## 使用场景

- 当你需要 **"实体驱动的结构化知识库"**（每个实体一个页面，强调交叉引用）
- 当你已经有大量文本/笔记，需要从中**抽取概念而非堆叠原料**
- 当你想要 Obsidian 风格的 `[[wikilink]]` 交叉引用体验

## 不适用场景

- 需要摄入 URL 自动下载 → 用 `vast-wiki-ingest`
- 需要保留原始资料（raw/）→ 用 `vast-wiki-ingest`
- 需要中文界面 → 用 `vast-wiki-ingest`

## 文件清单

```
vast-sanyuan-wiki-ingest/
├── SKILL.md                       # 主技能定义（英文原文 + 来源标注）
├── README.md                      # 本文件
└── references/
    └── page-templates.md          # 页面模板（concepts/products/patterns/comparisons）
```

## 维护说明

- 上游为独立项目，本地不会自动同步
- 如需更新，手动对比上游并同步
- 如发现差异，欢迎提 issue / PR
