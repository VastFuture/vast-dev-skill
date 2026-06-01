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