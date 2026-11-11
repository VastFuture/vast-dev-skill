---
name: vast-extract-learnings
description: 'Use when a user wants to extract, summarize,沉淀或复盘已完成开发工作的 decisions, lessons, reusable patterns, and surprises into a project-bound external documentation system. Triggers include "提取经验", "阶段复盘", "总结这次开发", "沉淀项目经验", "复盘刚完成的功能", "把经验写到文档系统", "extract learnings", "capture lessons learned", release review, milestone review, feature retrospective, refactor retrospective, and incident learning extraction.'
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: '[--source path] [--rebind] [--show-config]'
metadata:
  version: "1.0.0"
---

# vast-extract-learnings

从项目产物中提取可追溯的 Decision、Lesson、Pattern、Surprise，并写入项目绑定的外部文档系统。

以下命令中的 `$SKILL_DIR` 指当前 `vast-extract-learnings` 技能目录；运行前用实际绝对路径替换或设置该变量。

## Iron Law

**只提取产物明确支持的知识。每条学习必须有 Source；没有证据就不写。** Git、代码和当前会话只能帮助定位产物，不能单独支撑学习结论。

## Workflow Checklist

- [ ] 1. 定位项目根并读取项目级绑定
- [ ] 2. 首次运行时确认并固定文档根
- [ ] 3. AI 判断本次复盘对象
- [ ] 4. 发现、筛选并读取证据产物
- [ ] 5. 提取四类学习并逐条归因
- [ ] 6. 确定日期前缀与稳定主题名
- [ ] 7. 检查覆盖安全并写入文档
- [ ] 8. 验证输出并报告结果

## 1. 定位项目根和配置

运行：

```bash
python3 "$SKILL_DIR/scripts/config.py" locate --start "$PWD"
```

项目根优先级由脚本处理：Git 根目录 → 向上查找 `.vast/config.yml` → 项目标识文件 → 当前目录。若返回 `needs_confirmation: true`，先让用户确认项目根。

读取绑定：

```bash
python3 "$SKILL_DIR/scripts/config.py" read --project-root "$PROJECT_ROOT"
```

`--show-config` 只显示解析后的配置和输出目录，然后停止。`--rebind` 跳过已有绑定，进入首次绑定流程。

## 2. 首次绑定

配置固定在项目根 `.vast/config.yml`，是本机项目级配置，不入库。用户无需每次重复提供路径。

1. 若配置不存在、失效或用户传入 `--rebind`，询问文档系统的绝对根目录。已有 `DOCS_ROOT` 时可作为建议值，但仍需确认。
2. `docs_root` 必须已存在；禁止替用户创建整个文档系统。
3. 若 `<docs_root>/lessons/` 不存在，展示路径并确认后创建。
4. Git 项目中若 `.gitignore` 尚未精确忽略 `.vast/config.yml`，说明原因并确认后追加；不要忽略整个 `.vast/`。
5. 用户确认后运行：

```bash
python3 "$SKILL_DIR/scripts/config.py" init \
  --project-root "$PROJECT_ROOT" \
  --docs-root "$DOCS_ROOT" \
  --create-learnings \
  --update-gitignore
```

重新绑定时将 `init` 换成 `rebind`。若用户拒绝必要的本地配置保护，不写绑定并停止。

## 3. AI 判断复盘对象

用户不提供 scope type 或 scope ID。**由 AI 判断**本次复盘是阶段、里程碑、发布、功能、重构、事故还是会话，并仅把结果作为内部元数据。

判断顺序：用户当前表达 → 活动/已完成计划 → SUMMARY/VERIFICATION/UAT/handover/postmortem → Git 分支、tag 和最近提交 → 当前会话实际完成的工作。

只有多个业务主题同等可能或无法可靠判断时才询问。用业务名称提问，不要问“请选择 scope”。

## 4. 发现证据产物

运行发现脚本；每个用户提供的 `--source` 都追加一个参数：

```bash
python3 "$SKILL_DIR/scripts/discover.py" \
  --project-root "$PROJECT_ROOT" \
  --docs-root "$DOCS_ROOT" \
  --learnings-dir "$LEARNINGS_DIR" \
  --source path/to/extra-evidence.md
```

加载 `references/artifact-discovery.md`，根据优先级筛选与本次主题明确相关的候选文件。至少需要一个相关产物。发现脚本不会把目标 `lessons/` 中的生成文档再次作为输入。

首次绑定后展示识别到的主题和主要来源文件。后续运行默认低打扰：证据明确时直接继续；证据不足或来源文件不存在时，请用户补充文件，不要猜测。

## 5. 提取四类学习

加载 `references/extraction-model.md`。固定提取：

| Category | 问题 | 必需字段 |
|---|---|---|
| Decision | 决定了什么，为什么？ | What, Rationale, Source |
| Lesson | 执行后学到了什么？ | What, Context, Source |
| Pattern | 什么方法以后可以复用？ | Pattern, When to use, Source |
| Surprise | 什么事情出乎预期？ | What, Impact, Source |

同一事实只放入最匹配的一类。某类没有可靠条目时写 `无（本轮未发现）`，不要凑数。

## 6. 命名和日期

输出固定为：

```text
<docs_root>/lessons/YYYY-MM-DD-<topic>-learnings.md
```

日期优先级：明确完成日期 → SUMMARY/VERIFICATION 日期 → 本次生成日期。主题由 AI 从工作对象生成稳定的英文 kebab-case slug；优先使用阶段编号、发布版本、计划名或功能名，不要用泛化的 `latest-work`。

先扫描 `lessons/*-<topic>-learnings.md`：

- 找到 `generated_by: vast-extract-learnings` 的同主题文件：保留原日期前缀并覆盖。
- 找到同主题但无生成标记的文件：视为人工文档，禁止自动覆盖；询问用户换名或明确授权。
- 首次生成：使用确定的完成日期。

## 7. 写入文档

读取 `assets/learnings-template.md` 作为结构骨架。Frontmatter 必须包含：

```yaml
generated_by: vast-extract-learnings
```

完整覆盖技能自己的旧文件，不追加，不做智能 merge。第一版只写入 `lessons/`；**不要修改索引**、`index.md`、`README.md` 或其他导航文件。

## 8. 验证和报告

写入后运行：

```bash
python3 "$SKILL_DIR/scripts/validate_output.py" \
  --file "$OUTPUT_FILE" \
  --docs-root "$DOCS_ROOT" \
  --project-root "$PROJECT_ROOT"
```

校验失败时修正文档并重跑，不得跳过。报告主题、输出路径、四类计数、来源文件数和缺失产物；提醒用户人工复核准确性。

## Stop Conditions

仅在以下情况暂停询问：

- 项目根无法可靠确定
- 首次绑定或重新绑定文档根
- 需要创建 `lessons/` 或追加 `.gitignore`
- 多个业务主题同等可能
- 没有明确关联的证据产物
- 将覆盖无 `generated_by` 标记的人工文档

## Anti-Patterns

- 不要求用户提供 scope type、scope ID 或固定阶段编号。
- 不从代码 diff 或 Git 提交直接推演经验结论。
- 不把 TODO、风险或行动项混入四类学习。
- 不把旧 learnings 文件作为新一轮输入。
- 不自动创建不存在的 `docs_root`。
- 不静默覆盖人工文档。
- 不更新文档系统索引。
