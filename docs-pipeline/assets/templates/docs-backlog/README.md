# 工作队列 (Backlog)

## 用途

用此文件列出 AI 可以检查或执行的候选工作。

工作队列不是需求、owner docs 或计划的替代品。它只帮助选择下一个切片。

## 工作项

| 优先级 | 项目 | 需求 | Owner Doc | 计划 | 状态 | AI 自主级别 | 阻塞项 | 最后检查 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| P0 | `<第一个切片>` | `docs/prd/<path>` | `docs/design/<path>` | `docs/exec-plans/<path-or-none>` | `needs-requirement` | `blocked` | `模板占位符未替换` | `<YYYY-MM-DD>` |

## 就绪不变量

`ready` 意味着以下全部为真：

- 需求路径存在且有可测试的验收标准
- owner doc 路径存在且对此切片不已知过时
- `docs/context/project-context.md` 中的验证命令是真实的
- 阻塞性的开放问题不存在或明确非阻塞
- 受保护区域已在 `docs/context/ai-autonomy-policy.md` 中配置
- 计划触发器已检查

`Plan: none` 仅在项目明确符合无计划路径时有效。如果需要计划，将 AI 自主级别设为 `plan-first` 直到计划审计通过。

代理可以将过时的行从 `ready` 降级为 `needs-*` 或 `blocked`（需有证据）。代理**不得**将行升级为 `ready`、将自主级别改为 `implement` 或清除阻塞项（除非有人工确认或人工批准的 owner doc 证据）。

## 状态值

- `idea` — 尚未准备好实现
- `needs-requirement` — 原始输入存在但无实现就绪的需求
- `needs-design` — 需求存在但 owner doc 缺失或过时
- `ready` — AI 可以根据自主级别标签继续
- `in-progress` — 当前正在实现或规划中
- `blocked` — 阻塞项解决前无法继续
- `done` — 已完成并验证

## AI 自主级别值

使用 `docs/context/ai-autonomy-policy.md` 中的值：

- `implement`
- `plan-first`
- `ask-first`
- `research-only`
- `blocked`

## 选择规则

被要求继续而没有指定任务时，选择优先级最高的 `ready` 项，其 `AI 自主级别` 为 `implement` 且 `阻塞项` 为 `none`。

实现前，确认关联的需求、owner doc、计划字段、自主策略和计划触发器仍然有效。不要仅从聊天推断就绪状态。
