# vast-khazix-neat-freak

## 来源

源自 [VastFuture/khazix-skills](https://github.com/VastFuture/khazix-skills) 中的 `neat-freak` 技能。

原始仓库：https://github.com/VastFuture/khazix-skills
原始路径：`neat-freak/`

## 许可证

MIT

## 简介

洁癖级知识库同步技能。会话结束后以 OCD 级别的严谨度审查并同步项目文档（CLAUDE.md、README.md、docs/）和 agent 记忆，确保知识体系始终干净、准确、对新人友好。

## 配套工作流

**推荐搭配 [docs-pipeline](../docs-pipeline) 使用**：

1. **项目初始化**：运行 `/docs-pipeline` 搭建标准化的 docs/ 骨架
   - 创建 12 个核心目录（minimal 模式 7 个）
   - 生成 32 个模板文件
   - 初始化 CLAUDE.md、AGENTS.md 等 AI 代理配置

2. **开发过程**：按 docs-pipeline 的"标准四步"进行（见 [USAGE.md](../docs-pipeline/USAGE.md#场景-1添加新功能标准四步)）
   - docs/prd/ → 需求文档
   - docs/design/ → 架构设计
   - docs/exec-plans/ → 执行计划
   - docs/handover/ → 交接清单

3. **会话收尾**：运行 `/neat-freak` 同步和清理
   - 审查 3 层知识（agent memory + CLAUDE.md + docs/）
   - 防止 CLAUDE.md 膨胀（软上限 ~300 行）
   - 清理过期内容和重复记录

**职责分离**：
- docs-pipeline = 数据结构设计（搭建骨架）
- neat-freak = 数据结构维护（同步、清理、防膨胀）