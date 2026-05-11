# vast-skill-recommend-add

## 简介

用于向 vast-skill-recommender 内置推荐列表添加新技能的辅助工具。

## 使用方式

用户提供 GitHub 仓库 URL，本 skill 自动完成：
1. 获取仓库信息（名称、描述、topics）
2. 生成符合格式的 JSON 条目
3. 追加到 `skills-builtin.json`
4. 提交并推送

## 触发词

- 登记推荐技能
- 添加内置推荐
- 推荐新技能