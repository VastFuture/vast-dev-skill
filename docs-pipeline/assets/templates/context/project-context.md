# Project Context / 项目上下文

> 项目身份、当前工作、验证命令。AI 必须先读此文件再开始非平凡任务。

## 项目信息

| 字段 | 内容 |
|------|------|
| **项目名称** | `<project-name>` |
| **项目类型** | 应用层产品 / 框架核心 / 工具库 |
| **最后更新** | `YYYY-MM-DD` |

## 活跃工作

| 字段 | 内容 |
|------|------|
| **活跃需求** | `docs/requirements/<file>` |
| **活跃 Owner Doc** | `docs/design/<file>` 或 `docs/architecture/<file>` |
| **Documentation Freshness** | `fresh` / `partially stale` / `stale` / `unknown` |

## 验证命令

> 验证命令必须真实可执行。如果为空或仍是占位符，**停止**并填充，不要报告验证成功。

```bash
# 构建命令
<构建命令，占位则填"无">

# 测试命令
<测试命令，占位则填"无">

# 启动命令
<启动命令，占位则填"无">
```

### ⚠️ 验证命令前置条件

验证命令可能依赖以下配置文件。首次使用前，请确认这些文件存在：

| 配置文件 | 用途 | 检查命令 |
|---------|------|----------|
| `tsconfig.json` | TypeScript 配置 | `test -f tsconfig.json` |
| `.eslintrc.*` / `eslint.config.*` | ESLint 配置 | `ls .eslintrc* eslint.config.* 2>/dev/null` |
| `jest.config.*` | Jest 测试配置 | `ls jest.config.* 2>/dev/null` |
| `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` | 依赖锁定文件 | `ls package-lock.json yarn.lock pnpm-lock.yaml 2>/dev/null` |

**如果配置文件缺失**：
1. 检查 `package.json` 中的 scripts 是否依赖这些配置
2. 如果依赖，先安装或创建配置文件
3. 如果不依赖，可以跳过

**示例**：
```bash
# 检查 TypeScript 配置
test -f tsconfig.json && echo "✅ tsconfig.json 存在" || echo "❌ 缺少 tsconfig.json，运行 tsc --init 创建"

# 检查 ESLint 配置
ls .eslintrc* eslint.config.* 2>/dev/null && echo "✅ ESLint 配置存在" || echo "❌ 缺少 ESLint 配置"
```

## 活跃的 Plan（进行中）

| Plan 文件 | 状态 | 最后更新 |
|-----------|------|----------|
| `<plan file>` | `📋 进行中` / `✅ 已完成` | `YYYY-MM-DD` |

## 可选层激活状态

| 层 | 状态 | 说明 |
|---|------|------|
| `docs/audits/` | `❌ 未激活` | 计划/闭包审计证据存储 |
| `docs/testing/` | `❌ 未激活` | 手动/探索性测试记录 |
| `docs/retrospectives/` | `❌ 未激活` | 原型与实现重大分歧 |
| `docs/skills/` | `❌ 未激活` | 可复用提示和审计模板 |
| `docs/analysis/` | `❌ 未激活` | 研究和设计调查 |

## Documentation Freshness

- `fresh`：所有上下文文件反映当前代码状态
- `partially stale`：部分文件过时，但不影响当前任务
- `stale`：上下文严重过时，必须先更新才能继续
- `unknown`：从未确认过文档与代码的一致性