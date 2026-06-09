# prd/

需求规格、用户故事、验收标准

## 职责

- 存放产品需求文档（PRD）
- 记录用户故事和验收标准
- 作为开发的功能输入

## 文件内容

- PRD 文档
- 用户故事
- 功能清单
- 验收标准
- PRD Design Expert 角色定义

## PRD Design Expert

本目录包含 PRD Design Expert 角色定义，用于指导 PRD 编写：

```markdown
# Role: PRD Design Expert

## Overview
Expert at transforming complex product requirements into structured, detailed specifications.

## Output Modules
1. Product positioning and background
2. Target audience
3. User stories
4. Function list
5. Implementation logic (with Mermaid flowchart)
6. Non-functional requirements
7. Interface design
8. Data requirements
9. Acceptance criteria
10. Risks and limitations
```

## 与其他目录的关系

| 目录 | 关系 |
|------|------|
| `backlog/` | backlog/ 是待定事项，prd/ 是已确定的需求 |
| `design/` | prd/ 是输入（要什么），design/ 是输出（怎么做） |
| `exec-plans/` | prd/ 定义需求，plans/ 规划实现 |
