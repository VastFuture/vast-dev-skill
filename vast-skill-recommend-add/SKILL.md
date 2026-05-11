---
name: vast-skill-recommend-add
description: 向 vast-skill-recommender 的内置推荐列表添加新技能，并同步安装到全局 skills 目录。触发词：登记推荐技能、添加内置推荐、推荐新技能。
---

# 添加内置推荐技能

本 skill 用于将一个外部 skill 添加到内置推荐列表，并同步到全局。

## 前提

用户提供 GitHub 仓库 URL，格式：`https://github.com/owner/repo`

## 执行步骤

### 步骤 1：获取仓库信息

```bash
curl -s https://api.github.com/repos/{owner}/{repo} | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'name: {d[\"name\"]}\ndesc: {d[\"description\"]}\ntopics: {d.get(\"topics\",[])}')"
```

### 步骤 2：读取内置推荐列表

```bash
cat vast-skill-recommender/skills-builtin.json
```

### 步骤 3：生成新记录

基于仓库信息生成一条新条目：
- `id`: `builtin-{name-kebab}` 格式
- `name`: 仓库名（小写）
- `description`: 仓库描述（截断到合理长度）
- `url`: `https://github.com/{owner}/{repo}`
- `tags`: 从 topics 或推断
- `addedAt` / `updatedAt`: 今日日期（YYYY-MM-DD）
- `builtin`: `true`

### 步骤 4：写入 JSON

使用 Edit 工具在 `skills-builtin.json` 的 `skills` 数组末尾追加新条目。

验证 JSON 合法：
```bash
python3 -c "import json; json.load(open('vast-skill-recommender/skills-builtin.json')); print('Valid')"
```

### 步骤 5：提交并推送

```bash
git add vast-skill-recommender/skills-builtin.json
git commit -m "feat: 为 vast-skill-recommender 添加 {name} 内置推荐"
git push
```

### 步骤 6：同步安装到全局（可选）

如果用户要求同步到全局：

```bash
ln -sf "$(pwd)/vast-skill-recommender" "$HOME/.claude/skills/vast-skill-recommender"
```

## 输出示例

```
✅ 已添加内置推荐：{name}
- 描述：{description}
- 链接：{url}
- 标签：{tags}

提交：{commit-sha}
```

## Gotchas

- `id` 必须唯一且以 `builtin-` 开头
- 不要覆盖已有条目
- 描述用中文，简洁
- 标签用英文小写