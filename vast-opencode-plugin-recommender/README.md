# vast-opencode-plugin-recommender

OpenCode 插件推荐列表管理器 - 维护和分享值得安装的 OpenCode 插件。

## 功能

- 📋 **查看插件列表** - 展示所有推荐的 OpenCode 插件
- ➕ **添加插件** - 添加新插件到推荐列表
- 🗑️ **删除插件** - 从列表中移除插件
- ✏️ **更新插件** - 修改插件的描述或配置

## 使用方法

### 查看插件列表

```
/opencode-plugin
```

或自然语言：
- "查看 OpenCode 插件推荐"
- "有哪些推荐的插件"
- "插件列表"

### 添加插件

```
/opencode-plugin add
```

或自然语言：
- "添加一个 OpenCode 插件"
- "我想推荐一个插件"

### 删除插件

```
/opencode-plugin delete <plugin-id>
```

### 更新插件

```
/opencode-plugin update <plugin-id>
```

### 查看插件详情

```
/opencode-plugin show <plugin-id>
```

## 插件分类

- **生态桥接** - Claude Code、Cursor、其他 AI 编辑器的生态适配器
- **通知提醒** - 消息推送、状态通知、告警插件
- **工作流增强** - 自动化、任务编排、流程优化
- **开发工具** - 代码生成、构建工具、版本控制辅助
- **AI 增强** - MCP Servers、AI 工具集成、模型扩展
- **效率工具** - 快捷操作、代码片段、模板管理
- **其他插件** - 未分类的实用插件

## 内置推荐插件

### 1. cc-adapter-v2

Claude Code 生态桥接到 OpenCode。轻量级适配器，支持 Commands、Skills、MCP、Agents、Plugins 五大模块。

**安装**:
```bash
npm install -g cc-adapter-v2
```

**配置**:
```json
{
  "plugin": ["cc-adapter-v2"],
  "claude_code": {
    "commands": true,
    "skills": true,
    "mcp": true,
    "agents": false,
    "plugins": false
  }
}
```

**特性**:
- 从 `.claude/commands/` 加载命令到 `/` 自动补全
- 从 7 个来源发现技能，注入 system prompt
- 加载 `.mcp.json` MCP 服务器（stdio + HTTP）
- 从 `.claude/agents/` 加载 Agent 定义（实验性）
- 从 `.claude/plugins/` 加载 Claude Code 插件（实验性）

### 2. opencode-wecom-ping

企业微信群机器人通知插件。当 OpenCode 会话完成、出错或需要权限确认时，自动推送到手机微信。

**安装**:
```bash
npm install -g opencode-wecom-ping
```

**配置**:
```json
{
  "plugin": ["opencode-wecom-ping"],
  "agent": {
    "wecom-notify": {
      "mode": "primary",
      "description": "Agent that sends WeChat Work notifications",
      "prompt": "You are wecom-notify, an agent that notifies the user via WeChat Work.",
      "color": "#07C160"
    }
  }
}
```

**环境变量**:
```bash
export WECOM_BOT_KEY="你的群机器人key"
```

**特性**:
- 会话完成/出错/权限请求自动推送
- 默认静默，三种启用方式（Agent/命令/关键词）
- 内置去重，避免循环刷屏
- 零依赖，仅用 Node fetch
- 支持本地路径、npm、GitHub Release 多种安装方式

## 数据存储

- **内置列表**: `plugin-builtin.json`（只读，随技能发布）
- **用户列表**: `~/.claude/opencode-plugin-recommend.json`（可写，用户自己添加）

## License

MIT

### 3. ralph-loop

Ralph Loop 自动续写插件。实现自我引用的完成循环，让 AI Agent 持续工作直到任务真正 100% 完成。

**安装**:
```bash
cd ~/.cache/opencode
npm install FountainChan/opencode-ralph-loop
```

**配置**:
```json
{
  "plugin": ["ralph-loop"],
  "agent": {
    "ebuilder": {
      "mode": "primary",
      "description": "Autonomous agent with auto-continuation.",
      "prompt": "You are ebuilder, an autonomous agent that works continuously until the task is 100% complete. When FULLY done, output: <promise>DONE</promise>"
    }
  }
}
```

**使用方式**:

1. **命令模式**:
```bash
# 标准循环（最多 100 次迭代）
/ralph-loop "重构认证模块并确保所有测试通过"

# 超强工作模式（最多 500 次迭代）
/ulw-loop "迁移所有 API 客户端到 v2"

# 自定义参数
/ralph-loop "构建仪表板" --max-iterations=50 --completion-promise=SHIPPED

# 取消循环
/cancel-ralph
```

2. **ebuilder Agent 模式**（推荐用于长任务）:
   - 在 TUI 中切换到 **ebuilder** agent
   - 正常输入任务
   - Agent 将持续工作，无需停止
   - 切换回 **build** agent 即可停止自动续写

**特性**:
- `/ralph-loop` - 标准完成循环（最多 100 次迭代）
- `/ulw-loop` - 超强工作模式（最多 500 次迭代）
- `/cancel-ralph` - 取消活动循环
- ebuilder agent - 切换到 ebuilder agent 自动启用续写
- 完成承诺检测 - 扫描 Agent 输出中的 `<promise>DONE</promise>`
- Toast 通知 - 实时迭代和完成状态更新
- 防重复处理 - 避免重复 idle 事件
- 自定义参数 - 支持 `--max-iterations` 和 `--completion-promise`
- 零依赖 - 单文件实现，无外部依赖

**注意事项**:
- Agent 完成任务时需要输出 `<promise>DONE</promise>` 标记
- 循环状态保存在 `.ralph-loop.state.json` 和 `.ebuilder.state.json`
- 受 oh-my-opencode 的 Ralph Loop 和 Sisyphus 启发，轻量级单文件实现

