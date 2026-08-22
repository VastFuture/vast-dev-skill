# vast-opencode-plugin-recommender

OpenCode 插件推荐列表管理器，支持维护推荐项，以及通过安全的“预览、确认、应用”流程安装插件。

## 功能

- 查看内置和用户维护的 OpenCode 插件推荐
- 添加、更新、删除用户推荐项
- 区分“可自动安装”和“仅手动安装”插件
- 将 npm 插件包写入全局或项目 OpenCode 配置
- 安装前检查重复项、版本冲突、配置冲突和插件目录
- 使用 SHA-256 检测预览后的陈旧计划
- 写入失败时自动回滚，并报告验证结果

## 使用方法

```text
/opencode-plugin
/opencode-plugin show <id-or-name>
/opencode-plugin add
/opencode-plugin update <id-or-name>
/opencode-plugin delete <id-or-name>
/opencode-plugin install <id-or-name>
```

也可以使用自然语言，例如：

- “查看 OpenCode 插件推荐”
- “添加一个 OpenCode 插件”
- “更新这个插件推荐”
- “删除这个用户插件”
- “安装 cc-adapter-v2”
- “把 wecom 插件安装到当前项目”
- “全局安装这个 OpenCode 插件”

## 安装安全流程

每一次安装都必须重新选择范围：

- **全局**：目标通常是 `~/.config/opencode/opencode.json`，对所有项目生效
- **项目**：目标是所选 Git 仓库根目录中的 OpenCode 配置，只对该项目生效

选择后，助手先调用 `scripts/install-plugin.mjs` 预览。预览不会写文件：

```bash
node scripts/install-plugin.mjs --plugin <id-or-name> --scope global
```

```bash
node scripts/install-plugin.mjs --plugin <id-or-name> --scope project --project-dir <git-root>
```

助手会展示：

- 安装目标文件
- 将追加的插件标识，不展示完整现有配置
- 警告和冲突
- 所需环境变量的名称，但绝不显示变量值
- 当前配置的 `beforeSha256`

只有用户看到本次预览并明确确认后，才会应用。应用命令必须携带预览返回的精确 `beforeSha256`：

```bash
node scripts/install-plugin.mjs --plugin <id-or-name> --scope global --apply --expect-sha256 <beforeSha256>
```

项目安装还要带上同一个 `--project-dir <git-root>`。

如果摘要检查前文件已发生变化，安装器返回 `stale-plan`。此时旧计划和旧确认全部失效，必须重新预览、重新确认，再用新的摘要重试。该摘要不是文件系统级 CAS，不能保证阻止检查之后的所有并发写入；验证失败时的回滚会再次检查本次写入摘要，避免覆盖后续修改。

如果发现版本、配置格式或插件目录同名文件冲突，安装会停止，不会猜测或覆盖。项目安装会检查已知全局配置；全局安装没有项目目录时不承诺扫描项目配置，完全相同的 npm spec 由 OpenCode 去重。若写入后的验证失败，安装器会在回滚前再次检查文件摘要；发现后续修改时停止自动回滚并要求人工检查。摘要检查用于降低覆盖并发修改的风险，但不是文件系统级 CAS。

安装成功后必须**完全退出并重新启动 OpenCode**。仅关闭当前会话或刷新界面不能保证插件加载。

## 自动安装与手动安装

只有同时包含以下元数据的推荐项才能自动安装：

```json
{
  "packageSpec": "npm-package-name",
  "installStrategy": "opencode-config",
  "supportedScopes": ["global", "project"]
}
```

缺少任一字段的推荐项会标记为“仅手动安装”。`packageSpec` 只接受裸或 scoped npm 包，可带版本或 tag；路径、URL、git spec 和空白字符会被拒绝。`installCommand` 只是显示给人的说明，安装器从不执行它，也绝不会从它推断包名、安装策略或支持范围。

添加或更新用户推荐时，可以明确提供 `packageSpec`、`installStrategy`、`supportedScopes`。不完整就保持手动安装；系统不会自动补值。名称与任何内置或用户推荐重复时必须拒绝；读取遗留同名数据时内置项优先。环境变量只记录名称，不能录入秘密值。

## 内置推荐插件

### cc-adapter-v2

Claude Code 生态到 OpenCode 的轻量桥接器，支持 Commands、Skills、MCP、Agents 和 Plugins。

- 推荐仓库：<https://github.com/VastFuture/opencode-cc-adapter>
- npm 包名：`cc-adapter-v2`
- 安装方式：可自动安装，全局或项目范围

这两个名字并不矛盾：`opencode-cc-adapter` 是 GitHub 仓库名，`cc-adapter-v2` 是写入 OpenCode 配置的包名。

OpenCode 会根据配置加载 npm 包，不需要也不应先运行 `npm install -g`：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["cc-adapter-v2"]
}
```

插件专属选项不由安装器写入。需要调整行为时，以插件仓库当前文档和 OpenCode Schema 为准。

### opencode-wecom-ping

企业微信群机器人通知插件。OpenCode 会话完成、出错或请求权限时，可以向企业微信群机器人发送通知。

- 推荐仓库：<https://github.com/VastFuture/opencode-wecom-ping>
- npm 包名：`opencode-wecom-ping`
- 安装方式：可自动安装，全局或项目范围
- 环境变量名称：`WECOM_BOT_KEY`

同样采用配置驱动安装，不运行 `npm install -g`：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["opencode-wecom-ping"]
}
```

文档和安装预览只显示 `WECOM_BOT_KEY` 这个名称，不读取或展示它的值。

### ralph-loop

Ralph Loop 自动续写插件，支持 `/ralph-loop`、`/ulw-loop`、`/cancel-ralph` 和 `ebuilder` agent。

- 推荐仓库：<https://github.com/VastFuture/opencode-ralph-loop>
- 安装方式：**仅手动安装**
- 仓库源码版本：`1.0.0`
- npm `latest`：`0.0.1-alpha.0`

npm 最新发布明显落后于仓库源码，因此本技能不会自动安装，也**不推荐安装陈旧的 npm `ralph-loop` 包**。需要使用时，应先阅读推荐仓库当前版本的手动安装说明并核对源码版本；不要把旧 npm 包写入 OpenCode 配置。

## 数据存储

- 内置列表：`plugin-builtin.json`，随技能发布，只读
- 用户列表：`~/.claude/opencode-plugin-recommend.json`，由用户维护

内置推荐不能更新或删除。用户推荐可以更新或删除，但操作前必须展示目标并取得确认。

## License

MIT
