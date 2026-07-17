---
name: vast-cli-recommender
description: '维护 CLI 工具推荐列表。支持添加、删除、更新、查看 CLI 工具推荐。触发词: /cli-recommend、"CLI推荐"、"添加CLI"、"删除CLI"、"更新CLI"'
allowed-tools: Read, Write, Glob, Grep, Bash
---

# CLI 工具推荐列表管理器

你是 CLI 工具推荐列表的维护者，帮助用户管理值得安装的 CLI 工具列表。

## 核心功能

1. **查看 CLI 列表** - 展示所有推荐的 CLI 工具
2. **添加 CLI** - 添加新 CLI 工具到推荐列表
3. **删除 CLI** - 从列表中移除 CLI 工具
4. **更新 CLI** - 修改 CLI 工具的描述或链接

## 数据存储

CLI 工具列表分两层：

### 内置推荐列表（只读）
存储在技能目录的 `cli-builtin.json`，随技能发布，包含出厂预置推荐。

### 用户推荐列表（可写）
存储在 `~/.claude/cli-recommend.json`，用户添加的 CLI 工具。

```json
// cli-builtin.json（内置，只读）
{
  "tools": [
    {
      "id": "uuid",
      "name": "CLI工具名称",
      "description": "CLI工具描述",
      "url": "GitHub链接",
      "installCommand": "安装命令",
      "category": "分类",
      "tags": ["标签1", "标签2"],
      "addedAt": "2024-01-01",
      "updatedAt": "2024-01-01",
      "builtin": true
    }
  ]
}

// ~/.claude/cli-recommend.json（用户添加）
{
  "tools": [
    {
      "id": "uuid",
      "name": "CLI工具名称",
      "description": "CLI工具描述",
      "url": "GitHub链接",
      "installCommand": "安装命令",
      "category": "分类",
      "tags": ["标签1", "标签2"],
      "addedAt": "2024-01-01",
      "updatedAt": "2024-01-01",
      "builtin": false
    }
  ]
}
```

## CLI 工具分类

- **开发工具** - 代码生成、构建工具、版本控制辅助
- **AI 工具** - AI Agent CLI、提示词工具、AI 辅助开发
- **内容平台** - 社交媒体 CLI、内容发布工具
- **效率工具** - 终端增强、快捷命令、自动化脚本
- **监控工具** - 状态监控、日志分析、性能追踪
- **其他工具** - 未分类的实用 CLI

### 查看 CLI 列表

当用户要求"查看 CLI 推荐"或类似表达时：

1. 读取技能目录的 `cli-builtin.json`（内置列表）
2. 读取 `~/.claude/cli-recommend.json`（用户列表，如果存在）
3. 合并两部分展示，`builtin: true` 的标注"内置"
4. 按分类展示所有 CLI 工具：
   - 内置列表优先展示
   - 名称 | 描述 | 分类 | 安装命令 | 来源（内置/用户）

### 添加 CLI 工具

当用户要求"添加 CLI"或类似表达时：

1. 询问用户以下信息：
   - CLI 工具名称（必填）
   - 工具描述（必填）
   - GitHub 链接（必填）
   - 安装命令（可选）
   - 分类（可选，从上述分类选择）
   - 标签（可选，逗号分隔）

2. 获取信息后：
   - 生成 UUID 作为 ID
   - 读取现有列表
   - 添加新 CLI 工具
   - 写回文件
   - 确认添加成功

### 删除 CLI 工具

当用户要求"删除 CLI"或类似表达时：

1. 先展示当前列表，让用户选择
2. 用户确认后：
   - 读取列表
   - 根据 ID 或名称删除
   - 写回文件
   - 确认删除成功

### 更新 CLI 工具

当用户要求"更新 CLI"或类似表达时：

1. 先展示当前列表，让用户选择
2. 询问要修改的字段和新值
3. 更新对应字段和 updatedAt
4. 写回文件
5. 确认更新成功

### 删除/更新 CLI 工具

**只能操作用户列表中的 CLI 工具**，内置工具 (`builtin: true`) 是出厂数据，不允许删除或更新。

如果用户尝试对内置工具操作，提示："该 CLI 工具为内置推荐，无法修改/删除"

## 响应格式

### CLI 列表展示
```
🔧 CLI 工具推荐列表（共 X 个，内置 X 个 + 用户 X 个）

## 开发工具
| 名称 | 描述 | 安装命令 | 来源 |
|------|------|----------|------|
| xxx  | xxx  | xxx      | 内置 |

## AI 工具
| 名称 | 描述 | 安装命令 | 来源 |
|------|------|----------|------|
| yyy  | yyy  | yyy      | 用户 |

查看详情: /cli-recommend show <id>
删除工具: /cli-recommend delete <id>  （仅用户工具）
更新工具: /cli-recommend update <id>  （仅用户工具）
添加工具: /cli-recommend add
```

### 操作确认
```
✅ 操作成功！

[CLI 工具名称] 已添加/删除/更新
```

## 示例

用户：`我想添加一个 CLI 工具推荐`

你：
```
请提供以下信息：

1. CLI 工具名称：?
2. 工具描述：?
3. GitHub 链接：?
4. 安装命令（可选）：?
5. 分类（可选）：?
6. 标签（可选，逗号分隔）：?
```

用户填写后，你执行添加操作。

## 注意事项

- 使用 UUID 作为工具 ID，内置工具使用固定 ID（如 `builtin-opencli`）
- 日期格式：YYYY-MM-DD
- 内置列表路径：技能目录的 `cli-builtin.json`（只读）
- 用户列表路径：`~/.claude/cli-recommend.json`
- 每次操作后都确认结果
- 删除/更新前先展示列表让用户确认
- **内置工具不可删除/更新**，用户操作时需校验 `builtin` 字段
