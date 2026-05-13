## Pensieve 版本控制

`.pensieve/` 是项目知识库，四层结构中只有知识层应提交到 git：

| 层 | 目录 | 提交？ | 说明 |
|----|------|--------|------|
| MUST | `maxims/` | 提交 | 工程原则，团队共享 |
| WANT | `decisions/` | 提交 | 架构决策记录 |
| HOW | `pipelines/` | 提交 | 可复用工作流 |
| IS | `knowledge/` | 提交 | 探索结果缓存 |
| — | `MEMORY.md` | 提交 | 记忆索引 |
| — | `.state/` | 不提交 | 运行时缓存，Pensieve 自带 `.gitignore` 排除 |
| — | `state.md` | 不提交 | 运行时生命周期状态，项目根 `.gitignore` 排除 |
