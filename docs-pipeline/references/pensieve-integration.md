# Pensieve Integration

在 docs-pipeline 完成文件初始化后，自动同步路由标记和版本控制规则。如果项目未安装 Pensieve，询问用户是否安装。

## 触发条件

项目根目录存在 `.pensieve/` 目录（已安装）或用户确认安装（未安装）。

## 安装（仅 `.pensieve/` 不存在时）

当用户确认安装 Pensieve 时：

1. 用 `WebFetch` 读取 https://github.com/kingkongshot/Pensieve 的 README，提取安装步骤
2. 按 README 当前指引执行安装（不要硬编码安装命令，以仓库最新文档为准）
3. 安装完成后，继续执行下面的完整流程

## 执行步骤

### Step 1：健康检查

```bash
bash "${PENSIEVE_SKILL_ROOT:-$HOME/.claude/skills/pensieve}/.src/scripts/run-doctor.sh" --strict
```

- status=PASS → 跳过，报告"Pensieve 路由正常"
- status=FAIL 且 must_fix > 0 → 进入 Step 2

### Step 2：同步路由

```bash
bash "${PENSIEVE_SKILL_ROOT:-$HOME/.claude/skills/pensieve}/.src/scripts/sync-instructions.sh" --target auto
```

此命令向 `CLAUDE.md` 和 `AGENTS.md` 追加 `<!-- pensieve:instructions:start/end -->` 路由标记块。

### Step 3：确保 state.md 在 .gitignore

```bash
grep -q '^\.pensieve/state\.md$' .gitignore || echo '.pensieve/state.md' >> .gitignore
```

`state.md` 是 Pensieve 的运行时生命周期状态（Last Event、Short-Term 计数等），每次操作都变，不应提交到 git。`.state/` 子目录由 Pensieve 自带的 `.gitignore` 排除，但 `state.md` 在 `.state/` 外面，需要项目根 `.gitignore` 兜底。

### Step 4：补全路由为通用模式

`sync-instructions.sh` 只插入基础触发词（`commit`、`git commit`），不覆盖 skill 调用场景。需要替换为通用模式：

```bash
# 检查是否已是通用模式
grep -q 'any commit-related skill invocation' CLAUDE.md || {
  # 替换 CLAUDE.md 和 AGENTS.md 中的 commit 路由行
  sed -i 's/Commit requests (`commit`, `git commit`): use `.pensieve\/pipelines\/run-when-committing.md`. Check staged diff, decide whether reusable insight should be captured, then make atomic commits./Commit requests (`commit`, `git commit`, or any commit-related skill invocation): before executing `git commit`, always read `.pensieve\/pipelines\/run-when-committing.md` and execute Task 1 (insight judgment) + Task 2 (auto-capture). Task 3 (atomic commits) is handled by your commit flow or skill./' CLAUDE.md AGENTS.md
}
```

**为什么需要这步**：`sync-instructions.sh` 写死的触发词只覆盖裸命令，不覆盖 `/vast-dev-commit-as-prompt` 等 skill 调用。用"any commit-related skill invocation"通用模式一劳永逸，不再依赖具体 skill 名称。

### Step 5：验证

再次运行 Step 1 的 doctor 命令，确认 must_fix=0。

## 常见故障

| 症状 | 原因 | 修复 |
|------|------|------|
| doctor 报 STR-702 | CLAUDE.md/AGENTS.md 缺少路由标记 | 跑 sync-instructions |
| sync-instructions 报 markers unpaired | 标记对被手动破坏 | 手动删除残缺标记，重跑 sync-instructions |
| state.md 被提交到 git | `.gitignore` 缺少排除规则 | `echo '.pensieve/state.md' >> .gitignore` 然后 `git rm --cached .pensieve/state.md` |
| Pensieve 未初始化 | `.pensieve/` 不存在或为空 | 先跑 `pensieve` skill 的 init |

## 不要做

- ❌ 不要在 docs-pipeline 里安装 Pensieve（用户自己决定）
- ❌ 不要修改 `.pensieve/` 下的任何文件
- ❌ 不要在 `.pensieve/` 不存在时强制创建
