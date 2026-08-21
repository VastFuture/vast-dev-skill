---
name: wiki-init
description: >
  初始化 LLM Wiki 知识库目录结构。创建 raw/、wiki/ 及子目录（概念/实体/摘要/综合），
  生成 index.md 和 log.md，确认并配置 rawPath。首次使用知识库前必须执行。
argument-hint: "[raw目录绝对路径，可选]"
---

# /wiki-init — 初始化 LLM Wiki 知识库

初始化一个新的 LLM Wiki 知识库项目。

## 流程

1. 创建目录结构：
   - `raw/` — 原始资料（不可变）
   - `wiki/` — LLM 维护的笔记
   - `wiki/概念/` — 方法论、架构模式、第一性原理
   - `wiki/实体/` — 人名、公司、工具软件、项目
   - `wiki/摘要/` — 针对 raw 文件的一对一核心观点提炼
   - `wiki/综合/` — 深度研究报告
2. 创建系统文件：
   - `wiki/index.md` — 内容目录
   - `wiki/log.md` — 操作日志
3. 询问用户确认 raw 笔记保存目录的绝对路径
4. 将 `rawPath` 写入配置文件：
   - 全局模式：`~/.config/opencode/wiki-config.json`
   - 项目模式：项目根目录 `wiki-config.json`

## 配置

初始化完成后，`wiki-config.json` 示例：

```json
{
  "scope": "project",
  "rawPath": "D:/WorkDev/KnowleageBase/raw",
  "kbPath": "D:/WorkDev/KnowleageBase"
}
```

- `rawPath`：raw 原始资料存放目录的绝对路径
- `kbPath`：知识库项目根目录的绝对路径（`wiki/` 和 `AGENTS.md` 所在位置）

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
