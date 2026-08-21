---
name: wiki-classify
description: >
  扫描 raw/ 根目录 .md 文件，由 LLM 按四分类目录智能归类、移动文件、添加 frontmatter 多分类标签、修复相对路径。
  作为 /wiki-ingest 和 /wiki-lint 的自动前置步骤。触发词：分类、整理 raw、归类。
---

# /wiki-classify — raw 文件自动分类

扫描 `raw/` 根目录 `.md` 文件，按内容智能归类到四分类子目录。

## 分类目录

| 目录 | 内容 | 判定关键词示例 |
|------|------|----------------|
| `AI与智能体/` | AI、LLM、Agent、RAG、提示工程、模型训练 | GPT、Claude、Agent、LLM、prompt、RAG、embedding、transformer |
| `工具与开发/` | 开发工具、IDE、框架、语言特性、调试技巧 | CLI、git、VS Code、Docker、Python、npm、编译、调试 |
| `架构与工程/` | 架构模式、系统设计、工程实践、团队管理 | 微服务、CAP、CI/CD、重构、设计模式、运维、监控 |
| `Clippings/` | 网页剪藏、转载文章（Obsidian Web Clipper 保存） | 已存在于 Clippings/ 的文件不移动 |

**分类规则**：
- 主分类：文件内容最匹配的一个目录（文件移动到此目录）
- 多元标签（`tags:`）：记录所有关联分类（如一篇 RAG 架构文章，主分类 `AI与智能体/`，tags 包含 `AI与智能体,架构与工程`）
- 无法归入任何分类的文件 → 跳过，记录日志
- 边界模糊时接受交叉，不要求唯一归属

## 执行流程

### 步骤 1：确认 raw 目录和 kbPath

1. 读取配置文件：
   - **优先项目模式**：检查当前目录是否存在 `wiki-config.json`（`scope: "project"`）
   - **全局模式**：`~/.config/opencode/wiki-config.json`（`scope: "global"`）
2. 从配置中获取：
   - `kbPath` — 知识库根目录
   - `rawPath` — raw 文件存放目录
3. 若 `kbPath` 或 `rawPath` 为空，提示用户先执行 `/wiki-init` 初始化知识库
4. 确认 `rawPath` 目录存在

### 步骤 2：扫描文件

1. 列出 `rawPath` 根目录下所有 `.md` 文件（排除子目录、`.pdf`、非 markdown 文件）
2. 若无 `.md` 文件，输出"raw/ 根目录无需分类"并结束
3. 排除 `Clippings/` 等已有子目录中的文件

### 步骤 3：Git 基线提交

```bash
git add -A && git commit -m "基线：classify 操作前快照"
```

遵循 AGENTS.md 中的版本控制规则。

### 步骤 4：逐文件分类

对每个 `.md` 文件：

1. **读取内容**：用 Read 工具读取文件全文
2. **LLM 判定**：根据分类目录表和文件内容，判定：
   - 主分类（文件应移动到的目标目录）
   - 所有关联分类（用于 `tags:` 字段）
3. **边界检查**：
   - 空文件（0 字节或仅空白） → 跳过，记录"空文件跳过"
   - 内容过短无法判定（< 50 字有效内容） → 跳过，记录"信息量不足跳过"
   - 无法归入任何分类 → 跳过，记录"无法分类跳过"
4. **冲突检查**：目标目录已有同名文件 → 跳过，记录"文件名冲突跳过"

### 步骤 5：移动文件

```bash
git mv "raw/文件名.md" "raw/目标分类/文件名.md"
```

- 使用 `git mv` 保留 Git 重命名追踪
- 目标子目录不存在时自动创建（`mkdir -p`）

### 步骤 6：添加 frontmatter 标签

使用 Python 辅助脚本为移动后的文件添加 `tags:` 字段：

```bash
python skills/wiki-classify/frontmatter.py update "raw/分类/文件名.md" "AI与智能体,架构与工程"
```

- 无 frontmatter → 新建完整 frontmatter（含 `tags:`）
- 已有 frontmatter → 追加 `tags:` 字段（不覆盖已有字段）

### 步骤 7：修复图片引用路径

移动后文件内图片引用需要修正（多了一层目录）：

1. **标准引用** `../assets/` → `../../assets/`：
   - 正则替换：`!\[` → 查找 `](../assets/` 替换为 `](../../assets/`
2. **裸引用** `](filename.jpg)`：
   - 检查 `assets/文件名（去掉.md）/` 是否存在
   - 存在 → 补全为 `../../assets/文件名子目录/filename`
   - 不存在 → 记录警告，保持原样
3. 用 Edit 工具对每个文件逐一修正

### 步骤 8：修复 wiki 显式路径引用

扫描 `{kbPath}/wiki/` 目录中对已移动 raw 文件的显式路径引用（仅处理 `raw/文件名.md` 格式，`[[文件名]]` 格式无需修改）：

1. 用 Grep 搜索 `{kbPath}/wiki/` 中包含已移动文件路径的行
2. 用 Edit 工具将 `raw/文件名.md` 替换为 `raw/新分类/文件名.md`

### 步骤 9：记录日志

在 `{kbPath}/wiki/log.md` 追加记录：

```markdown
## [YYYY-MM-DD] Classify | 批量分类
- 移动：文件A.md → AI与智能体/（tags: AI与智能体, 架构与工程）
- 跳过：文件B.md（原因：空文件）
- 路径修复：N 处图片引用、M 处 wikilink
```

### 步骤 10：Git 完成提交

```bash
git add -A && git commit -m "classify: 分类 N 个文件到子目录"
```

## 工具使用规则

**更新 index.md、log.md 等累积性文件时**：
- 必须先用 `Read` 读取当前内容
- 必须用 `Edit` 工具做增量修改（追加、替换）
- 禁止用 `Write` 工具覆盖整个文件

**Write 工具仅用于**：
- 创建全新文件
- 用户明确要求覆盖整个文件

## 脚本执行优先级

需要执行脚本操作时，按以下顺序选择实现方式：

1. **Python** — 检测到 Python 环境则优先使用
2. **Linux** — Shell 脚本（bash/sh）
3. **Windows + Git Bash** — 用 Git Bash 执行
4. **Windows（无 Git Bash）** — PowerShell

## 辅助脚本

### frontmatter.py

路径：`skills/wiki-classify/frontmatter.py`

功能：
- `python frontmatter.py update <file> "tag1,tag2,..."` — 添加/更新 frontmatter tags
- `python frontmatter.py get <file>` — 获取当前 tags

## 语言规则

- 始终使用简体中文
- 保持 Obsidian wikilink 兼容（文件名避免特殊字符）
- 日志记录使用简体中文
