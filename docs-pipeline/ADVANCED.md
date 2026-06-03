# docs-pipeline 高级特性

本文档包含 docs-pipeline 的可选高级特性，不属于核心安装流程。

---

## Pensieve 集成（可选插件）

> Pensieve 是可选的版本控制增强工具，**不在默认安装范围内**。

**默认行为**：跳过 Pensieve 集成，不检测、不询问、不提示。

**激活条件**（满足任一）：
1. 环境变量 `ENABLE_PENSIEVE=true`
2. 已存在 `.pensieve/` 目录（说明用户已手动安装）

**集成流程**（仅在激活时执行）：

**分支 A — `.pensieve/` 已存在**：

1. 按 [references/pensieve-integration.md](./references/pensieve-integration.md) 执行 doctor → sync-instructions → .gitignore 保护 → doctor 验证流程
2. 检测 CLAUDE.md 是否已有 `## Pensieve 版本控制` 段落：`Bash grep -q "^## Pensieve 版本控制" CLAUDE.md`
   - 不存在 → 用 `Edit` 把 `assets/templates/pensieve-gitignore-snippet.md` 追加到文件末尾
   - 已存在 → 跳过

**分支 B — `.pensieve/` 不存在 且 `ENABLE_PENSIEVE=true`**：

1. 用 `AskUserQuestion` 询问用户是否要安装 Pensieve
2. 用户确认 → 按 [references/pensieve-integration.md](./references/pensieve-integration.md) 的"安装"章节执行（读取 GitHub 仓库最新 README 获取安装步骤，不要硬编码），然后走分支 A 的完整流程
3. 用户拒绝 → 跳过，报告"已跳过 Pensieve 集成"

**不激活时**：完全跳过此步骤，不在报告中提及。

---

## ARCHITECTURE.md 生成降级策略

`ARCHITECTURE.md` 不能简单 cp，必须基于目标项目的实际代码生成。流程：

### 检测

```bash
test -f ARCHITECTURE.md && echo "EXISTS" || echo "MISSING"
```

- **EXISTS** → 跳过，记入"已存在跳过"清单
- **MISSING** → 进入子代理生成

### 调用 Explore 子代理

用 `Agent` 工具，`subagent_type: "Explore"`，提示词如下（中文）：

> 探索目标项目（当前工作目录）的代码结构，按以下固定 5 个章节生成 `ARCHITECTURE.md` 内容并直接写入项目根 `ARCHITECTURE.md`：
>
> 1. **项目概述**：一句话定位 + 后端/前端/数据库技术栈（无则填"无"）
> 2. **常用命令**：后端启动/测试命令、前端启动/构建/测试命令、完整启动说明（按实际项目情况列出，无则省略对应小节）
> 3. **架构**：核心源码目录树（二级深度），每个目录附一句话职责注释
> 4. **数据模型**：列出核心数据模型 + 一句话职责。纯前端/CLI 项目填"无（不涉及持久化数据模型）"
> 5. **开发注意事项**：数据库迁移、代理配置、路由入口、其他关键约定（按实际有无列出 3-5 条即可）
>
> 严格遵守：
> - 只生成这 5 个章节，不要加其他章节
> - 每个章节必须出现，无内容时填"无"
> - 文件开头加一行 `# ARCHITECTURE.md`，第二行加 `> 项目架构文档 - 参见 [CLAUDE.md](./CLAUDE.md) 的行为规范。`
> - 控制在 100 行以内
> - 探索预算：≤8 次工具调用
>
> 探索完成后，用 `Write` 工具写入 `<项目根绝对路径>/ARCHITECTURE.md`，然后简短报告"已生成"。

### 智能降级

如果 Explore 子代理失败（返回错误、超时、或未能写入文件），按以下顺序尝试降级：

**降级策略 1：基于 package.json 生成（Node.js 项目）**

```bash
if [ -f "package.json" ]; then
  # 读取 package.json
  NAME=$(jq -r '.name // "未命名项目"' package.json)
  DESC=$(jq -r '.description // "无描述"' package.json)
  SCRIPTS=$(jq -r '.scripts | keys[]' package.json 2>/dev/null || echo "无")
  
  # 生成基本 ARCHITECTURE.md
  cat > ARCHITECTURE.md << EOF
# ARCHITECTURE.md

> 项目架构文档 - 参见 [CLAUDE.md](./CLAUDE.md) 的行为规范。

## 项目概述

**项目名称**：$NAME

**描述**：$DESC

**技术栈**：Node.js / TypeScript（基于 package.json 检测）

## 常用命令

\`\`\`bash
# 可用的 npm scripts:
$SCRIPTS
\`\`\`

## 架构

**注意**：此文档由自动检测生成，仅包含基本信息。请根据实际项目结构补充：
- 源码目录结构（src/）
- 数据模型（如有）
- 开发注意事项

可运行 \`tree src -L 2\` 查看实际目录结构。
EOF
  
  echo "⚠️ Explore 失败，已基于 package.json 生成基本 ARCHITECTURE.md，需补充完整"
  exit 0
fi
```

**降级策略 2：其他项目类型的简化模板**

```bash
# Python 项目
if [ -f "setup.py" ] || [ -f "pyproject.toml" ]; then
  PROJECT_TYPE="Python"
  START_CMD="python main.py"
  
# Go 项目
elif [ -f "go.mod" ]; then
  PROJECT_TYPE="Go"
  START_CMD="go run ."
  
# Rust 项目
elif [ -f "Cargo.toml" ]; then
  PROJECT_TYPE="Rust"
  START_CMD="cargo run"
  
# 无法识别
else
  PROJECT_TYPE="未知"
  START_CMD="<启动命令>"
fi

# 生成通用骨架
cat > ARCHITECTURE.md << 'EOF'
# ARCHITECTURE.md

> 项目架构文档 - 参见 [CLAUDE.md](./CLAUDE.md) 的行为规范。

## 项目概述

**技术栈**：$PROJECT_TYPE

## 常用命令

```bash
# 启动
$START_CMD
```

## 架构

**注意**：此文档为模板骨架，需要手动填充：
1. 项目概述（一句话定位 + 技术栈细节）
2. 常用命令（构建、测试、启动命令）
3. 核心源码目录树（二级深度）
4. 数据模型（如有）
5. 开发注意事项
EOF

echo "⚠️ Explore 失败且无法自动检测项目类型，已生成模板骨架，需手动填充"
```

**降级策略 3：完全失败（最后手段）**

如果以上策略都失败，在报告中提示：

```
⚠️ 需人工处理：
  - ARCHITECTURE.md 生成失败，请手动创建或运行 tree src -L 2 查看目录结构
```

不生成任何 ARCHITECTURE.md 文件。
