# OpenCode 插件安装闭环设计

## 目标

让 `vast-opencode-plugin-recommender` 在展示推荐后提供安装入口，并在用户明确确认后安全地启用插件。

安装器只管理 OpenCode 配置。标准 npm 插件由 OpenCode 在重启后自行下载和加载，不执行 `npm install -g`。

## 用户流程

1. 用户查看列表或插件详情。
2. 技能提供 `/opencode-plugin install <id>`。
3. 技能每次询问安装作用域：
   - 全局：`~/.config/opencode/opencode.json`
   - 当前项目：项目根目录的 `opencode.json`
4. 安装器执行预检并输出计划，不修改文件：
   - 目标配置文件
   - 最小变更描述 `expectedChange.pluginAppend`，不输出完整现有配置
   - 已安装、重复加载或配置冲突
   - 缺失的环境变量名称，不读取或显示变量值
5. 用户明确确认后，技能携带预检生成的目标文件摘要调用安装器。
6. 安装器备份目标文件、幂等合并配置并验证写入结果。
7. 技能提示用户完全退出并重启 OpenCode，然后用 `opencode debug config` 验证运行时配置。

取消、模糊回复或预检冲突都不得修改文件。

## 数据模型

`plugin-builtin.json` 和用户推荐记录增加结构化安装元数据：

```json
{
  "packageSpec": "cc-adapter-v2",
  "installStrategy": "opencode-config",
  "supportedScopes": ["global", "project"]
}
```

- `packageSpec`：写入 OpenCode `plugin` 数组的唯一插件标识。本期只支持裸或 scoped npm 包，可带版本或 tag；拒绝 tuple、本地路径、URL、git spec、空白字符或任意补丁。
- `installStrategy`：本期只支持 `opencode-config`。
- `supportedScopes`：允许的安装作用域。
- `installCommand` 和 `configExample`：保留为人工参考，不作为自动安装输入。

结构化字段缺失时，安装器停止并说明该推荐记录不支持自动安装，不从 Shell 命令猜测安装行为。

## 安装器接口

新增无第三方依赖的 Node.js 脚本：

```text
node scripts/install-plugin.mjs \
  --plugin <id-or-name> \
  --scope <global|project> \
  [--project-dir <path>] \
  [--apply --expect-sha256 <digest|absent>]
```

- 默认是预览模式，结果包含目标路径、安装前摘要和最小变更描述，不包含完整现有配置。
- `--apply` 才允许写文件，并且必须携带预览得到的摘要。
- 应用前摘要不一致时返回 `stale-plan`，要求重新预览和确认。
- `beforeSha256` 用于陈旧计划检测，不是文件系统级 CAS，不承诺阻止摘要检查后的所有并发写入。
- 输出稳定的 JSON 结果，供不同 Agent 一致解析。
- 项目作用域必须明确提供项目目录，并验证它是 Git 工作区根目录。

## 配置合并规则

1. 目标作用域只检查根目录的 `opencode.json` 和 `opencode.jsonc`；项目 `.opencode/opencode.json` 不是配置目标候选。
2. 只有一个现存 JSON 文件时修改它；存在 JSONC 或多个候选文件时停止，不创建第二份配置。
3. 目标作用域没有配置文件时创建带 `$schema` 的标准 `opencode.json`。
4. 保留所有现有字段，只向 `plugin` 数组末尾追加 `packageSpec`。
5. 插件条目支持读取字符串和 `[spec, options]` tuple；同一 spec 已存在时不写文件。
6. 写入前记录原文件状态和摘要；写入使用临时文件加原子替换。
7. 写入后重新解析，并确认目标插件只出现一次。

本期只写标准 JSON。目标文件无法按 JSON 解析时停止，不尝试重写 JSONC、删除注释或修改插件专属配置。

## 重复加载检查

预检以下位置：

- 全局 `~/.config/opencode/opencode.json`
- 当前项目 `opencode.json`
- `OPENCODE_CONFIG` 指向的配置文件
- `~/.config/opencode/plugins/`
- 当前项目 `.opencode/plugins/`
- `OPENCODE_CONFIG_DIR` 下的 `plugin/` 和 `plugins/`

规则：

- 目标作用域已包含相同 `packageSpec`：报告“已安装”，不写文件。
- 已知的另一作用域包含完全相同 `packageSpec`：报告来源和警告，不重复写入。全局安装没有项目目录时不承诺扫描项目配置；完全相同的 npm spec 由 OpenCode 去重。另一作用域只有 JSONC 时无法安全解析，按冲突停止。
- 同一 npm 包名存在不同版本或不同 tuple options：报告冲突并停止。
- 自动发现目录中存在同名文件视为阻断冲突，避免同一 hook 被本地插件和 npm 插件重复加载；安装器不自动删除或覆盖该文件。
- `OPENCODE_CONFIG_CONTENT` 存在时提示运行时还有内存配置来源，但不读取或修改该变量。

远程和托管配置无法从文件系统完整检查。安装器必须把这项限制写入警告，不声称扫描了所有运行时来源。

## 验证与回滚

写入后执行两层验证：

1. 静态验证：重新解析目标文件，确认新增项符合 OpenCode `plugin` Schema 且插件标识唯一。
2. 运行时验证：如果 `opencode` 可用，在目标作用域使用 `OPENCODE_PURE=1 opencode debug config` 捕获并解析 JSON，确认精确 `packageSpec` 出现一次；纯模式避免验证过程下载或执行外部插件。命令不存在时标记为“待重启验证”。无效 JSON、命令失败或缺少精确插件标识都触发回滚。捕获内容仅在内存中校验，绝不回显，因为配置可能包含密钥。

写入后记录文件摘要。静态或运行时验证失败时，回滚前再次比较本次写入摘要：已检测到后续修改时停止自动回滚；未检测到时恢复原文件或删除新文件。摘要检查可以缩小竞态窗口，但不是文件系统级 CAS，无法完全消除检查与恢复之间的 TOCTOU。回滚只恢复配置，不删除 OpenCode 已下载的缓存包。

## 推荐项解析

- 按 ID 查询时要求唯一匹配。
- 按名称查询时先匹配内置推荐，再匹配用户推荐，防止用户记录遮蔽规范内置项。
- 添加或更新用户推荐时拒绝与任何内置或用户推荐重名。
- `ralph-loop` 当前仅提供规范仓库的手动安装说明，不配置自动安装元数据。

## 非目标

- 不安装或卸载全局 npm 包。
- 不自动下载 GitHub Release 或复制本地插件文件。
- 不收集、写入或显示密钥值。
- 不自动重启 OpenCode。
- 不解决任意 JSONC 配置编辑。
- 不覆盖已有冲突配置。
- 不自动写入 `configExample` 中的 Agent、命令或插件私有选项。

## 验收场景

- 新建全局配置并启用插件。
- 在已有配置中保留未知字段并合并插件配置。
- 同一安装重复执行时零修改。
- 全局与项目跨层重复时停止。
- 本地同名插件可能重复加载时停止。
- 用户未确认时零修改。
- 配置冲突、无效 JSON 或验证失败时不留下损坏配置。
- 输出不包含环境变量值或其他密钥。
- 预览后配置发生变化时拒绝应用陈旧计划。
- 测试使用临时 HOME、临时 Git 仓库和可注入的假 `opencode` 命令，不触碰用户配置。
