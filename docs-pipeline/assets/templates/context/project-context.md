# Project Context / 项目上下文

> 项目身份、当前工作、验证命令。AI 必须先读此文件再开始非平凡任务。

## 项目信息

| 字段 | 内容 |
|------|------|
| **项目名称** | `<project-name>` |
| **项目类型** | `<待检测>` 见下方"项目类型检测指南" |
| **技术栈** | `<待填充>` |
| **最后更新** | `YYYY-MM-DD` |

## 活跃工作

| 字段 | 内容 |
|------|------|
| **活跃需求** | `docs/prd/` |
| **活跃 Owner Doc** | `docs/design/` |
| **Documentation Freshness** | `fresh` — 文档体系在当前会话同步，代码技术债见 AGENTS.md 已知技术债表 |

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
| `<待根据项目类型填充>` | `<用途>` | `test -f <file>` |

## 自检命令

**自检命令（pre-commit hook 会自动执行前三项）：**

| 类型 | 命令 | 用途 | 耗时 |
|------|------|------|------|
| 快速检查 | `<待填充>` | typecheck + 单元测试，无需 dev server | ~4s |
| 冒烟测试 | `<待填充>` | UI 关键路径冒烟，需要 dev server | ~15s |
| 完整测试 | `<待填充>` | 跨页面/跨服务端到端 | ~60s+ |

修改代码后，commit 前至少确保 `快速检查` 通过。涉及 UI 改动时额外运行 `冒烟测试`。

## 测试环境要求

- **数据库**：测试使用独立实例（SQLite/PostgreSQL/MySQL），禁止连接生产库
- **可重复执行**：DB 相关用例不依赖执行顺序，每次测试前重置状态
- **并行**：后端测试可并行，E2E 串行（UI 状态互斥）
- **前端**：类型检查零 error，Chrome DevTools 或 Playwright 验证

## 系统启动流程

| 服务 | 命令 | 端口 |
|------|------|------|
| 后端 | `<待填充>` | `<端口>` |
| 前端 | `<待填充>` | `<端口>` |

## CDP 验证流程（UI 改动必跑）

> 修改组件、样式、布局后，必须通过 chrome-devtools MCP 实际验证：

1. `mcp__chrome-devtools__navigate_page` 打开对应页面（如 `http://localhost:5173/path`）
2. `mcp__chrome-devtools__take_snapshot` 确认页面元素正确
3. `mcp__chrome-devtools__take_screenshot` 截图确认渲染效果
4. `mcp__chrome-devtools__list_console_messages` 检查 console 无报错
5. 涉及交互的改动（按钮、表单、导航）需通过 CDP 模拟点击/输入并截图验证
6. 修改响应式布局时，用 `mcp__chrome-devtools__emulate` 的 viewport 参数分别验证桌面和移动端视口

## 活跃的 Plan（进行中）

> AI 自主维护规则：在 `exec-plans/active/` 新建/移动计划文件时，**必须**同步更新 `docs/exec-plans/README.md` 的索引表。
> 
> 活跃计划完整清单见 [docs/exec-plans/README.md](../exec-plans/README.md)。

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

---

## 🤖 AI 填充规则

初始化此文件时，AI 需要：
1. **检测项目类型**（读取 `package.json`, `requirements.txt`, `pom.xml` 等文件）
2. **查表填充**（使用下方映射表自动填充占位符）
3. **适配差异**（根据项目特征补充特定验证流程）

### 项目类型配置映射表

| 项目类型 | 检测特征 | 快速检查 | 冒烟测试 | 完整测试 | 关键配置文件 |
|---------|---------|---------|---------|---------|------------|
| **前端** | `package.json` 含 vite/react/vue/next | `npm run test` | `npm run test:smoke` | `npm run test:e2e` | tsconfig.json, vite.config.ts |
| **Python 后端** | `requirements.txt` 含 fastapi/uvicorn | `pytest -m "not integration"` | `pytest -m integration` | `pytest` | requirements.txt, pytest.ini |
| **Java 后端** | `pom.xml` 含 spring-boot | `mvn test -Dtest=*UnitTest` | `mvn test -Dtest=*IntegrationTest` | `mvn verify` | pom.xml, application.yml |
| **Go 后端** | `go.mod` | `go test -short ./...` | `go test -run Integration ./...` | `go test ./...` | go.mod, go.sum |
| **Rust 后端** | `Cargo.toml` | `cargo test --lib` | `cargo test --test integration` | `cargo test` | Cargo.toml, Cargo.lock |
| **全栈 Monorepo** | `apps/` + `pnpm-workspace.yaml` | `pnpm test` | `pnpm test:smoke` | `pnpm test:e2e` | pnpm-workspace.yaml, turbo.json |

### 前端/全栈项目补充验证

**如果检测到前端特征，必须补充 CDP 验证流程：**

修改组件、样式、布局后，通过 chrome-devtools MCP 验证：
1. 导航到页面 → 2. 快照元素 → 3. 截图渲染 → 4. 检查 console → 5. 交互测试 → 6. 响应式测试（viewport）

### 扩展原则

- 新项目类型：在映射表添加一行
- 特殊验证：在"补充验证"章节追加
- 保持主体通用：所有占位符格式一致

---

## 🧹 资源清理

### 测试后资源释放

**强制要求**：测试完毕后必须主动释放资源，避免资源泄漏。

**清理清单**：
1. **前端开发服务器**：测试完成后停止 `pnpm dev` / `npm run dev` 进程
2. **后端服务器**：测试完成后停止 `uvicorn` / `java -jar` / `go run` 进程
3. **浏览器标签页**：关闭测试打开的 Chrome DevTools 页面
4. **临时文件**：清理测试过程中生成的临时文件（如 `/tmp/*.png`）
5. **数据库连接**：确保测试后关闭所有数据库连接

**检查命令**：
```bash
# 检查是否有残留的开发服务器进程
ps aux | grep -E "(vite|uvicorn|webpack-dev-server)" | grep -v grep

# 检查是否有残留的浏览器进程
ps aux | grep -E "(chrome|chromium)" | grep -v grep
```

**提交后清理**：每次 `git commit` 后，检查并清理测试资源。
