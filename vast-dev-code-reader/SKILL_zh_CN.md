---
name: vast-dev-code-reader
description: 当您想要深度理解一个陌生的代码库并从中生成可重用的认知技能时使用，通过提供本地路径或 GitHub URL。
---

# Deep Code Reader

系统性地阅读和理解代码库，生成一组经验证的可重用认知技能——涵盖模块能力、设计逻辑、数据结构、状态流和修改指南。

核心机制：闭卷考试验证循环确保生成的技能是真正全面的，而非浅层总结。

## 1. 团队角色

为了使这个过程稳健且概念清晰，系统采用三个不同的智能体，模拟软件工程团队：

- **Agent A（技术写作者）**：深度阅读器。阅读源代码并编写全面的技能文档。
- **Agent B（QA 工程师）**：考官。阅读源代码，提取可验证的事实，并生成测试问题。
- **Agent C（初级开发者）**：考生。扮演新团队成员，只能阅读 Agent A 编写的文档来回答 Agent B 的问题。

## 2. 使用方法

这是触发深度代码阅读工作流的 CLI 命令：

```bash
/deep-code-read <source> <output-dir>
```

- **source**：本地路径（例如 `./path/to/repo`）或 GitHub URL（例如 `https://github.com/org/repo`）
- **output-dir**：生成的技能写入位置（例如你的平台技能目录）

## 3. 完整流程

你**必须**按顺序遵循这些阶段。使用平台的 task/todo 跟踪机制跟踪跨模块的进度。

### 3.1 阶段 1：准备

这个初始阶段处理目标源代码库的解析和准备工作。

1. 确定项目名称：
   - 本地路径 → 目录名
   - GitHub URL → 仓库名
2. 如果 source 是 URL：
   - 克隆到 `{output-dir}/{project-name}/`
   - 如果目录已存在，跳过克隆，直接使用
3. 如果 source 是本地路径：
   - 验证路径存在且是 git 仓库
   - 直接使用（只读 — **不要**修改源仓库中的任何文件）
4. 检测版本：
   - 在源仓库运行 `git tag --list`
   - 如果存在标签，使用语义版本感知排序（处理 `v` 前缀），推荐最新版本
   - 如果没有合理的标签，推荐 `main` 或 `master` 分支
5. **暂停 — 向用户呈现推荐：**
   > "检测到以下标签/分支：[list]。我推荐跟踪 `{recommended}`。请确认或指定其他目标。"
6. 检出确认的 ref

### 3.2 阶段 2：扫描

这个阶段扫描仓库结构以识别边界和依赖关系。

1. 扫描源仓库目录结构
2. 使用启发式方法识别模块边界：
   - `src/`、`lib/`、`pkg/`、`packages/` 或项目根目录下的顶级目录
   - 语言特定模式：Python 包（`__init__.py`）、Go 包、Node 包（`package.json`）等
   - 查找现有的模块文档或清单文件
3. 分析模块之间的导入/依赖关系
4. **暂停 — 向用户呈现模块列表和依赖图：**
   > "找到以下模块：[list，附带一行描述]。选择要深度阅读的模块（或 'all'）。"
5. 记录用户的选择 — 每个选定的模块一个任务

### 3.3 阶段 3：深度阅读（Agent A - 技术写作者）

这个阶段生成基础技能文档。

对于每个选定的模块，使用来自 `tech-writer-prompt.md` 的 prompt 模板调度子智能体。

**子智能体调度参数：**

- `prompt`：渲染后的 `tech-writer-prompt.md`，填充变量
- `description`："Deep read {module-name}"

**prompt 中要填充的变量：**

- `{source-dir}`：源仓库路径
- `{module-dir}`：源仓库内特定模块的路径
- `{output-dir}`：技能输出目录
- `{project-name}`：提取的项目名称
- `{module-name}`：模块名称
- `{ref}`：跟踪的 tag/分支

技术写作者完成后，验证技能文件是否写入 `{output-dir}/{project-name}-dr-{module-name}/`。更新模块的任务状态。

### 3.4 阶段 4：验证（ABC 循环）

这个阶段执行核心验证循环，确保生成的技能准确完整。

对于每个生成了技能的模块，运行验证周期：

**步骤 1 — Agent B / QA 工程师（问题生成）：**

使用 `qa-engineer-prompt.md` 调度子智能体，使用轻量级/小型模型（例如 Haiku 类）。

**子智能体调度参数：**

- `prompt`：渲染后的 `qa-engineer-prompt.md`
- `model`：一个更小、更便宜的模型 — 越弱越好（如果它能捕获差距，那些差距就是真实存在的）
- `description`："Generate questions for {module-name}"

**变量：**

- `{source-dir}`, `{module-dir}`, `{module-name}`
- `{previous_questions}`：第一轮为空字符串

QA 工程师返回两组：

- 带答案密钥的验证问题（JSON 数组）
- 推荐给用户的问题（JSON 数组）

保存推荐问题（保留在上下文中供阶段 6 使用）。跨轮累积所有到目前为止问过的验证问题。

**步骤 2 — Agent C / 初级开发者（闭卷答题）：**

使用 `junior-dev-prompt.md` 调度子智能体。

**子智能体调度参数：**

- `prompt`：渲染后的 `junior-dev-prompt.md`，嵌入验证问题
- `description`："Verify skills for {module-name}"

**变量：**

- `{skill-dir}`：`{output-dir}/{project-name}-dr-{module-name}/`
- `{questions}`：来自 QA 工程师的验证问题（不含答案密钥）

初级开发者返回每个问题的答案。

**步骤 3 — 评估：**

使用你自己的推理（作为主编排器）评估初级开发者的答案：
对于每个问题，将初级开发者的答案与 QA 工程师的 `required_facts` 列表进行核对：

- 如果答案覆盖**所有**必需事实（精确匹配或语义等价），则**通过**
- 如果答案遗漏任何必需事实，则**失败**
- 这是一个客观检查，而非主观判断。仔细提取 QA 工程师和初级开发者的 JSON 输出，忽略任何 markdown 格式化（如 `json`）。

**步骤 4 — 循环或继续：**

**硬规则：你必须继续循环，直到 100% 的验证问题通过，或者你已完成恰好 3 轮。没有提前退出。99% 的通过率仍然是失败——继续循环。**

- 100% 通过 → 模块验证完成，更新任务，移到下一个模块
- 任何问题失败（即使只有一个）→ 你**必须**继续下一轮：
  1. 收集失败的问题：问题、QA 工程师的答案密钥、初级开发者的失败答案
  2. 将这些反馈给技术写作者：再次调度，`{feedback}` 变量包含失败的问题、QA 工程师的预期答案密钥和识别的差距
  3. 重新运行 QA 工程师和初级开发者，传递所有之前的问题（跨所有轮）作为 `{previous_questions}`，以便 QA 工程师生成新问题而非重复旧问题
  4. 再次评估 — 重复直到 100% 或完成 3 轮
- **恰好 3 轮后仍有失败** → 向用户展示未解决的问题和通过率，供其判断。不要静默跳过。

**不要为提前停止找借口。**"差不多了"、"大多数问题都通过了"、"边际效益递减"不是跳过一轮的有效理由。循环的存在是为了捕获差距——如需要，使用全部 3 轮。

### 3.5 阶段 5：生成全局索引

这个阶段将经验证的模块技能整合到全局索引文件中。

所有模块验证完成后，生成 `{output-dir}/{project-name}-dr/SKILL.md`：

```yaml
---
name: {project-name}-dr
description: 当使用 {project-name} 代码库时使用 — 提供全面的模块知识、设计逻辑和修改指南（从 {ref} 生成）
---
```

内容必须包括：

- Repo 来源（如果适用则为 GitHub URL，否则为本地路径）
- 版本：tag 或 commit hash
- 跟踪的分支
- 生成时间戳
- 每个模块的一行用途（来自模块技能）
- 模块间依赖关系（来自阶段 2 扫描）
- 跨模块场景入口指南：对于跨多个模块的常见操作，描述涉及哪些模块及其顺序

要生成跨模块场景，阅读所有模块技能并综合典型的用户工作流程。

### 3.6 阶段 6：用户验收

这个阶段向用户展示结果以供最终验证。

展示从阶段 4 收集的推荐问题：

> "Skills generated and verified. Here are some questions you might want to test:
> [list recommended questions]
>
> Feel free to ask any question about {project-name}. I'll answer using ONLY the generated skills."

在这个阶段回答用户问题时：

- **只**阅读 `{output-dir}/{project-name}-dr*/` 中生成的技能文件
- **不要**阅读源代码
- 如果无法仅从技能中回答问题，诚实说明 — 这表明存在差距

继续直到用户满意或决定结束会话。

### 3.7 阶段 7：清理

这个最后阶段在必要时处理临时文件的清理。

如果 source 是从 URL 克隆的（即在阶段 1 中创建了 `{output-dir}/{project-name}/`）：

> "Skills are ready. The cloned source code is at `{output-dir}/{project-name}/`. Want me to delete it to save disk space, or keep it for reference?"

- 用户说删除 → 删除克隆的目录
- 用户说保留 → 保持原样

如果 source 是本地路径（我们没有克隆任何内容），则跳过此阶段。

## 4. 关键规则

在整个执行过程中严格遵守以下规则：

- **永不修改源代码** — 源仓库全程只读
- **智能体隔离至关重要** — 每个智能体的 prompt 严格定义其可读取的内容
- **技能必须自给自足** — 验证循环的存在就是为了确保这一点
- **跟踪进度** — 每个模块是一个任务，随着其阶段推进而更新
- **通过 writing-skills 格式化** — 技术写作者遵循 `superpowers:writing-skills` 格式化约定（frontmatter、CSO 描述、目录结构），但不运行完整的 writing-skills TDD 循环
