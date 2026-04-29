---
name: vast-dev-project-analyzer
description: 基于深度代码库分析生成全面的项目文档（白皮书），涵盖架构、模块、测试和部署。
---

# 深度项目分析

本技能将 `code-reader` 的核心机制扩展为系统性分析整个代码库并综合生成全面的"项目白皮书"。它将深度模块级理解与高级架构综合以及工程实践（构建、测试、部署）相结合。

最终输出重点关注架构与模块深度解析（约 60%），并由实用的工程与运维指南支撑。

## 1. 团队角色

此工作流在综合生成最终文档之前，使用专门的 agent 收集不同类型的信息：

- **Agent A（技术写作）**：模块专家。**此角色通过调用 `code-reader` 技能直接履行。** 它阅读源代码以提取模块级能力、数据结构和状态流，通过内置的 ABC 验证循环确保高精度。
- **Agent B（DevOps 工程师）**：基础设施专家。扫描配置文件（Makefile、Dockerfile、CI/CD 流水线、`package.json` 等）以提取构建、测试和部署实践。
- **Agent C（首席架构师）**：综合专家。阅读所有来自 `code-reader` 模块技能和 DevOps 工程师的输出，撰写最终的综合项目文档，确保叙述连贯且架构准确。

**必需的子技能：** 你必须使用 `code-reader` 技能作为阶段 2 的引擎。

## 2. 使用方法

```bash
/project-analyzer <source> <output-dir>
```

- **source**: 本地路径（例如 `./path/to/repo`）或 GitHub URL
- **output-dir**: 最终白皮书和中间分析文件的写入位置

## 3. 完整流程

你必须按顺序遵循这些阶段以生成最终文档。

### 3.1 阶段 1：准备与扫描

此初始阶段处理目标源代码库的解析和准备工作。

1. 解析目标仓库（如果是 URL 则克隆，如果是本地则验证）。
2. 扫描目录结构以识别：
   - **代码模块**：包含核心业务逻辑的目录（`src/`、`lib/` 等）。
   - **基础设施文件**：构建脚本、Dockerfile、CI/CD 工作流、配置文件。
3. 生成模块间的初始依赖图。

### 3.2 阶段 2：深度模块阅读（通过 `code-reader`）

此阶段将代码理解的重任委托给 `code-reader` 技能。

对于每个已识别的核心模块，**调用 `code-reader` 技能** 指向该特定模块目录。

- `code-reader` 技能将运行其技术写作 → QA 工程师 → 初级开发验证循环。
- 收集为每个模块生成并完全验证的 `SKILL.md` 文件。
  _注意：此阶段纯粹关注代码、逻辑和数据结构。_

### 3.3 阶段 3：基础设施分析（DevOps 工程师）

此阶段从配置文件中提取工程实践。

通过使用 `devops-engineer-prompt.md` 分派 DevOps 工程师 agent。

- **输入**：所有已识别的基础设施文件（例如 `Makefile`、`Dockerfile`、`.github/workflows/`、`pom.json`）。
- **输出**：涵盖构建步骤、测试策略和部署拓扑的结构化报告。

### 3.4 阶段 4：架构综合（首席架构师）

此阶段生成最终的综合项目文档。

通过**阅读并严格遵循** `chief-architect-prompt.md` 分派首席架构师 agent。

- **输入**：阶段 2 生成的模块文档、阶段 3 的基础设施报告以及初始目录扫描。
- **项目名称**：你必须提取实际项目名称（例如从仓库目录名、`package.json` 或 `go.mod` 中），并用它替换输出文件名中所有 `{project-name}` 占位符。
- **指令约束**：
  - 架构师必须将文档深度和长度的约 60% 分配给系统架构和核心模块，其余 40% 分配给项目概述、场景和工程实践。
  - **图表**：你必须按首席架构师提示中的明确要求，输出 Mermaid 语法的架构图、流程图和时序图。
- **输出**：写入 `<output-dir>` 的 `<actual-project-name>-deep-dive.md`。文档必须遵循此确切 7 章大纲：
  1. 项目全局摘要 (Project Executive Summary)
  2. 系统架构分析 (System Architecture Analysis)
  3. 核心模块代码深度解析 (Core Modules Deep Dive)
  4. 核心功能执行流程分析 (Core Function Execution Flow)
  5. 质量与性能评估 (Quality & Performance Assessment)
  6. 项目构建与部署 (Project Build & Deployment)
  7. 二次开发指南 (Extension & Contribution Guide)

### 3.5 阶段 5：用户验收与审查

将生成的 `<actual-project-name>-deep-dive.md` 呈现给用户。

> "项目架构深度分析已生成。请查看 `<actual-project-name>-deep-dive.md`。如果你想深入了解任何特定模块细节或调整任何部分的权重，请告诉我。"

## 4. 关键规则

执行期间严格遵守以下规则：

- **只读源代码**：绝不修改源代码仓库。
- **内容权重**：确保首席架构师严格遵守架构/模块与工程实践之间 60/40 的比例。
- **文档格式**：最终输出必须遵循专业技术写作标准（层次化编号、无双语标题、术语一致）。
