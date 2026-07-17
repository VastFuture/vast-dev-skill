# vast-cli-recommender

专门用于管理和推荐 CLI 工具的技能。

## 功能

- 📋 查看内置 + 用户自定义的 CLI 工具推荐列表
- ➕ 添加新的 CLI 工具推荐
- 🗑️ 删除用户添加的 CLI 工具
- ✏️ 更新用户添加的 CLI 工具信息

## 使用方式

### 触发词

- `/cli-recommend`
- "CLI推荐"
- "添加CLI"
- "删除CLI"
- "更新CLI"

### 命令示例

```bash
# 查看所有推荐的 CLI 工具
/cli-recommend

# 添加新 CLI 工具
/cli-recommend add

# 删除 CLI 工具（仅用户添加的）
/cli-recommend delete <tool-id>

# 更新 CLI 工具（仅用户添加的）
/cli-recommend update <tool-id>

# 查看 CLI 工具详情
/cli-recommend show <tool-id>
```

## 数据存储

### 内置推荐列表（只读）
- 路径：`vast-cli-recommender/cli-builtin.json`
- 包含出厂预置的 CLI 工具推荐
- 不可删除或修改

### 用户推荐列表（可写）
- 路径：`~/.claude/cli-recommend.json`
- 用户自定义添加的 CLI 工具
- 可以自由添加、删除、更新

## CLI 工具分类

- **开发工具** - 代码生成、构建工具、版本控制辅助
- **AI 工具** - AI Agent CLI、提示词工具、AI 辅助开发
- **内容平台** - 社交媒体 CLI、内容发布工具
- **效率工具** - 终端增强、快捷命令、自动化脚本
- **监控工具** - 状态监控、日志分析、性能追踪
- **其他工具** - 未分类的实用 CLI

## 内置推荐 CLI 工具

当前包含以下内置推荐（共13个）：

### 开发工具
1. **gh** - GitHub 官方 CLI（PR/Issue/CI管理）
2. **git** - 版本控制系统
3. **typeui** - TypeUI 设计系统管理工具

### AI 工具
4. **aider** - AI 配对编程终端工具
5. **codex** - OpenAI Codex CLI 编排工具

### 内容平台
6. **opencli** - 主流社交和内容平台 CLI

### 数据处理
7. **jq** - JSON 处理器

### 网络工具
8. **curl** - HTTP 客户端

### 媒体处理
9. **ffmpeg** - 音视频处理工具
10. **imagemagick** - 图像处理工具

### 文档处理
11. **pandoc** - 文档格式转换工具

### 数据库
12. **sqlite3** - 嵌入式数据库

### 监控工具
13. **claude-hud** - Claude Code 状态栏插件

## 数据格式

```json
{
  "tools": [
    {
      "id": "builtin-tool-name",
      "name": "CLI工具名称",
      "description": "CLI工具描述",
      "url": "GitHub链接",
      "installCommand": "安装命令",
      "category": "分类",
      "tags": ["标签1", "标签2"],
      "addedAt": "2026-07-17",
      "updatedAt": "2026-07-17",
      "builtin": true
    }
  ]
}
```

## 安装

通过 vast-dev-skill 仓库直接使用，或复制到你的 `.claude/skills/` 目录。

## 许可

MIT License
