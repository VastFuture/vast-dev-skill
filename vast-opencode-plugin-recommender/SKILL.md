---
name: vast-opencode-plugin-recommender
description: '维护和安装 OpenCode 插件推荐。用户明确提到 OpenCode 插件并要求查看、添加、删除、更新或安装，或使用 /opencode-plugin、/opencode-plugin install <id-or-name> 时使用。普通软件、编辑器或系统插件请求不触发。'
allowed-tools: Read, Write, Glob, Grep, Bash
---

# OpenCode 插件推荐与安装

维护 OpenCode 插件推荐列表，并通过受控的配置变更安装具备自动安装元数据的插件。

## 命令

```text
/opencode-plugin
/opencode-plugin show <id-or-name>
/opencode-plugin add
/opencode-plugin update <id-or-name>
/opencode-plugin delete <id-or-name>
/opencode-plugin install <id-or-name>
```

自然语言触发必须包含 OpenCode 上下文，例如“查看 OpenCode 插件推荐”“添加 OpenCode 插件”“安装 OpenCode 插件”和“为当前项目安装 cc-adapter-v2”。单独的“安装插件”或“全局安装插件”不触发。

## 数据来源

- 内置推荐：技能目录的 `plugin-builtin.json`，只读，`builtin: true`
- 用户推荐：`~/.claude/opencode-plugin-recommend.json`，可写，`builtin: false`
- 查询时合并两份列表；内置项优先，按分类展示
- 内置项不可更新或删除；用户项可更新或删除

插件分类：生态桥接、通知提醒、工作流增强、开发工具、AI 增强、效率工具、其他插件。

## 安装能力模型

推荐项分为两类，不能混淆：

### 可自动安装

同时具备以下元数据才可调用安装器：

```json
{
  "packageSpec": "npm-package-name",
  "installStrategy": "opencode-config",
  "supportedScopes": ["global", "project"]
}
```

- `packageSpec`：写入 OpenCode `plugin` 数组的精确值，只接受裸 npm 包或 scoped npm 包，可带版本或 tag；拒绝路径、URL、git spec 和空白字符
- `installStrategy`：当前仅支持 `opencode-config`
- `supportedScopes`：允许的安装范围，只能包含 `global`、`project`

### 仅手动安装

缺少任一自动安装元数据的推荐项都是“仅手动安装”。展示原因和仓库链接，但不得调用安装器，不得把 `installCommand` 当成可执行命令，也不得从中推断任何自动安装元数据。

`installCommand` 只是一段给人看的历史说明，不是可信安装源，永远不执行。

## 安装流程

`/opencode-plugin install <id-or-name>` 必须严格执行以下流程。

### 1. 选择范围

每一次安装都要询问用户选择：

- **全局**：修改 `~/.config/opencode/opencode.json`，对所有项目生效
- **项目**：修改所选 Git 仓库根目录的 OpenCode 配置，只对该项目生效

即使用户之前选过，也不能沿用。项目范围还必须取得 Git 仓库根目录；不能替用户猜目录。若插件不支持所选范围，停止并说明。

### 2. 仅运行预览

先定位技能目录中的 `scripts/install-plugin.mjs`，运行预览，不加 `--apply`：

```bash
node scripts/install-plugin.mjs --plugin <id-or-name> --scope global
```

```bash
node scripts/install-plugin.mjs --plugin <id-or-name> --scope project --project-dir <git-root>
```

安装器输出单个 JSON 对象。预览阶段不得修改配置。

### 3. 展示计划

向用户展示：

- 插件名称和 `packageSpec`
- 安装范围
- `targetPath`，即将修改的配置文件
- `expectedChange.pluginAppend`，即将追加的插件标识；安装器绝不公开完整现有配置
- 全部 `warnings`
- 全部 `conflicts`
- 插件要求的环境变量**名称**
- `beforeSha256`，用于识别预览后已发生的变化；它不是文件系统级 CAS，不能保证杜绝摘要检查后的所有并发写入
- 安装后必须完整重启 OpenCode

绝不读取、展示、记录或回显环境变量的值。配置、警告或命令输出中出现秘密值时也要脱敏；只允许显示变量名，例如 `WECOM_BOT_KEY`。`OPENCODE_CONFIG`、`OPENCODE_CONFIG_DIR`、`OPENCODE_CONFIG_CONTENT` 也只显示名称和是否影响检查，不显示值。

### 4. 明确确认

只有 `status: "ready"` 且没有冲突时，才能询问明确确认。确认问题必须指出插件、范围和 `targetPath`，例如：

```text
将把 cc-adapter-v2 写入项目配置 /path/to/opencode.json。确认按上述预览执行吗？
```

沉默、含糊回答、先前确认或“继续处理”都不算确认。没有本次预览后的明确确认，不得应用。

### 5. 使用同一摘要应用

确认后，用预览返回的**原始且完整** `beforeSha256` 作为 `--expect-sha256`，不得重新计算、截断或替换：

```bash
node scripts/install-plugin.mjs --plugin <id-or-name> --scope global --apply --expect-sha256 <beforeSha256>
```

```bash
node scripts/install-plugin.mjs --plugin <id-or-name> --scope project --project-dir <git-root> --apply --expect-sha256 <beforeSha256>
```

### 6. 报告结果并重启

- `installed`：报告目标文件和验证结果，提醒**完全退出并重新启动 OpenCode**；仅关闭会话或重载界面不够
- `pending-restart`：配置已写入，但运行时验证要等完整重启后确认
- `already-installed`：目标范围已存在，不重复写入
- `already-installed-other-scope`：已知的另一范围已存在，展示警告并停止。全局安装未提供项目目录时不会承诺扫描项目配置；OpenCode 会对完全相同的 npm spec 去重

## 异常处理

- `stale-plan`：预览后配置被修改。不得复用旧确认或旧摘要；重新预览、重新展示计划、重新取得明确确认，再用新的 `beforeSha256` 重试
- `conflict`：展示全部冲突并停止。版本冲突、元组选项、非数组 `plugin`、插件目录中的同名文件等都必须由用户处理，不能自动覆盖或合并
- `ambiguous-config`：同一范围发现多个候选配置。展示候选并让用户先整理，不能替用户选择
- `unsupported-jsonc`：安装器不修改 JSONC。说明限制并停止
- `invalid-json`：目标配置不是合法 JSON。说明错误并停止
- `validation-failed` 且 `rolledBack: true`：说明验证失败且已恢复原配置
- `validation-failed` 且 `rolledBack: false`：配置在验证期间又被修改，自动回滚为避免覆盖并发修改而跳过；立即警告用户人工检查 `targetPath`
- `expect-sha256-required`：安全参数缺失。重新从预览开始，不能绕过

任何失败都不能改用 `npm install -g`、执行 `installCommand` 或直接手改配置来规避安装器。

## 查看与详情

列表至少展示：名称、描述、分类、安装方式（可自动安装/仅手动安装）、支持范围、来源（内置/用户）。

详情至少展示：ID、名称、描述、GitHub、分类、特性、配置示例、环境变量名称、安装方式、支持范围、来源、添加时间、更新时间。环境变量只显示名称。

## 添加插件

添加用户推荐时收集：

- 必填：名称、描述、GitHub 链接
- 可选：显示用安装说明 `installCommand`、配置示例、环境变量名称、分类、标签、特性
- 可选的自动安装元数据：`packageSpec`、`installStrategy`、`supportedScopes`

规则：

1. 用户明确提供并确认完整自动安装元数据后，才保存为可自动安装项。
2. 不得从 `installCommand`、仓库名、插件名、配置示例或 URL 推断 `packageSpec`、`installStrategy`、`supportedScopes`。
3. 自动安装元数据不完整时，保存为仅手动安装项；不要补默认值。
4. `envVars` 只保存变量名，不收集或保存变量值。
5. 生成 UUID，设置 `builtin: false`，日期使用 `YYYY-MM-DD`，写入用户列表后再读取验证。
6. 名称不能与内置或用户列表中的现有名称重复；重复名称必须拒绝。查询同名历史数据时，内置名称优先于用户名称。

## 更新插件

只允许更新用户推荐。先展示目标项，再询问字段和新值，明确确认后更新 `updatedAt` 并写回。

更新时可以收集 `packageSpec`、`installStrategy`、`supportedScopes`，但必须遵守与添加相同的规则：只接受用户明确提供的值，绝不从 `installCommand` 推断。若删除或破坏任一必需元数据，该项立即变为仅手动安装。更新名称时同样拒绝与任何其他内置或用户推荐重名。

## 删除插件

只允许删除用户推荐。先展示目标项和影响，取得明确确认后按 ID 删除，再读取验证。内置项提示“该插件为内置推荐，无法修改或删除”。

## 内置推荐的特殊说明

- `cc-adapter-v2`：继续推荐；规范仓库是 `https://github.com/VastFuture/opencode-cc-adapter`，写入配置的 npm 包名是 `cc-adapter-v2`
- `opencode-wecom-ping`：可自动安装；通过 OpenCode 配置的 `plugin` 数组加载，不使用 `npm install -g`
- `ralph-loop`：仅手动安装。npm `latest` 为 `0.0.1-alpha.0`，落后于推荐仓库源码 `1.0.0`；打开规范仓库并按当前 README 手动操作，不得推荐或自动安装陈旧 npm 包

## 安全铁律

- 永远先预览，后确认，再用相同 `beforeSha256` 应用
- `beforeSha256` 只做陈旧计划检测，不宣称阻止检查之后的所有并发写入
- 每次安装都重新选择全局或项目范围
- 永远不执行或解析 `installCommand`
- 永远不显示环境变量值或其他秘密
- 有冲突就停止，不猜、不覆盖
- 验证失败优先依赖安装器回滚，并如实报告回滚结果
- 安装成功后要求完整重启 OpenCode
