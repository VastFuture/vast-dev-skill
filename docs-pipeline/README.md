# docs-pipeline

一键初始化或修复 Claude Code 项目的 `docs/` 产物链路结构。

## 使用

在 Claude Code 里说：
- "初始化文档结构"
- "搭建 docs pipeline"
- "set up docs structure"

skill 会自动识别并执行。

## 产物链路

```
research（调研）→ prd（需求）→ exec-plans/active（计划进行中）→ exec-plans/completed（计划完成）
                                                                   ↓
                                                               lessons（踩坑教训，按需横切）
```

## 行为契约

| 状态 | 动作 |
|------|------|
| `docs/` 不存在 | 全新初始化（建 6 目录 + 6 README + 1 CLAUDE.md） |
| `docs/` 部分存在 | 修复模式，只补缺失项 |
| `docs/` 全部齐全 | 跳过，输出"已规范" |
| 项目根 `CLAUDE.md` 不存在 | 写入模板 |
| 项目根 `ARCHITECTURE.md` 不存在 | 调用 Explore 子代理探索后生成 |
| `.pensieve/` 存在且 CLAUDE.md 无 `## Pensieve 版本控制` | 追加版本控制规则（四层结构哪些提交、哪些排除） |
| `.pensieve/` 不存在 | 询问用户是否安装 Pensieve；确认则自动 init 并集成 |

## 关键特性

- **幂等**：重复调用安全，不覆盖已有文件
- **零破坏**：从不删除用户内容；只新建或跳过
- **零依赖**：不假设技术栈，只管文档与 AI 代理配置

## 完整规范

见 [SKILL.md](./SKILL.md)。

## 维护手册

见 [references/adding-templates.md](./references/adding-templates.md)。
