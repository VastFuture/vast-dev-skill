# Claude Config Advisor

Claude Code 项目配置审查与设计工具。

## 功能

- **审查现有配置**：评估 `.claude/` 目录结构、`CLAUDE.md` 等文件的合理性
- **设计新配置**：从零规划适合项目的 Claude Code 配置结构

## 使用方法

在项目中直接调用本技能：

```
/vast-claude-config-advisor
```

或当用户提到以下关键词时自动触发：
- `.claude` 配置
- `CLAUDE.md` 文件
- Claude 配置文件
- 配置结构设计

## 工作流程

1. **识别场景**：判断是"审查模式"还是"设计模式"
2. **读取文件**：读取最小必要文件进行分析
3. **判断合理性**：从职责清晰度、结构匹配度、内容可维护性等角度评估
4. **输出评价**：给出结构化评价与优化建议

## 文件结构

```
vast-claude-config-advisor/
├── SKILL.md              # 技能定义与工作流程
├── references/           # 参考文档
│   ├── layout-and-rules.md      # 目录结构说明
│   ├── claude-md-guide.md       # CLAUDE.md 编写指南
│   ├── review-rubric.md          # 审查评分标准
│   └── structure-patterns.md    # 推荐结构模式
└── README.md             # 本文件
```
