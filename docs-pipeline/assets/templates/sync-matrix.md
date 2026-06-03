# 变更影响矩阵 / Change Impact Matrix

> 灵感来源：[neat-freak 变更影响矩阵](https://github.com/VastFuture/khazix-skills/tree/main/neat-freak)
> 用途：系统化映射"这次改动 → 要同步哪些文件"，防止漏改

## 使用方法

遇到不确定"这次改动要同步哪些文件"时查这张表。

**两个方向都要查**：
1. 补漏（加到哪些文件）
2. 防膨胀（应该从哪些文件删）

---

## 代码层变更 → 文档层变更

| 本次对话发生的事 | 要改的文件（按受众） |
|----------------|---------------------|
| **新增 API / 路由** | CLAUDE.md 路由清单 + docs/prd/ + docs/design/architecture + docs/handover/ |
| **新增 / 改名环境变量** | CLAUDE.md 环境变量表 + docs/context/project-context + docs/handover/ |
| **新增数据库表 / 列** | CLAUDE.md 数据库表 + docs/design/architecture Data Model |
| **新增 / 改动用户流程** | CLAUDE.md 用户流程 + README 命令示例 + docs/handover/ What Exists Today |
| **新增大特性（跨多文件）** | 以上全部 + docs/design/ 新章节 + docs/handover/ 已完成清单 |
| **新增术语 / 改命名** | docs/prd/ 术语表（如有）+ 全局搜索旧术语替换 |
| **部署参数 / 基础设施变化** | docs/handover/ + CLAUDE.md 部署章节 |
| **下游项目接入方式变化** | 下游项目的 docs/ + 上游项目的 docs/prd/ |

---

## 标准动作（四处都补）

新增一个能力（API、flow、特性）的标准动作：

| 编号 | 文档 | 内容 | 受众 |
|-----|------|------|------|
| 1 | **docs/prd/** | 需求、验收标准、技术方案 | 人类 + AI |
| 2 | **docs/design/** | 数据流、状态机、设计取舍 | 人类 + AI |
| 3 | **docs/exec-plans/** | 执行计划、风险、依赖 | AI |
| 4 | **docs/handover/** | 已完成、已知问题、运维注意 | 人类 |

**不要只改一处就结束**——这四处都要补。

---

## 反向：哪些信息该删除

CLAUDE.md / AGENTS.md 不是变更日志。下面这些反模式发现了就删 / 迁：

| 反模式 | 处理 |
|--------|------|
| "X 时刻起 Y 功能上线，详见 docs/Z.md" | 删除——指针角色已被「深入文档」指针表占掉 |
| 在 CLAUDE.md 里抄 docs/ 已有的详细机制 | 删除——AI 改到这块自然会读 docs |
| 已稳定 ≥ 7 天的"新功能上线"叙事 | 融入项目概览或删除 |
| 单次事故的复盘细节 | 留 1 行红线规则，事故详情归 docs/issues/ 或删 |
| 已被新版本取代的"中间态"叙事 | 只留最终态规则，中间历史删 |
| 单条 memory > 100 行 + 全是事故复盘 | 提炼成 ≤ 30 行"规则 + Why + How to apply" |

**判断标准**：这条信息在下次 AI 写代码时如果没看到，会犯错吗？不会就删 / 迁。

---

## 跨项目影响检查

**最容易漏改的场景**：

| 场景 | 影响范围 | 检查方法 |
|------|---------|---------|
| 上游 API 变了 | 下游 SDK 文档、集成指南 | 搜索所有引用此 API 的项目 |
| 共享子域 / 路由 / 环境变量改了 | 所有 consumer 项目的 setup 文档 | 搜索环境变量名、子域名 |
| 认证中台变更 | 所有接入应用的集成指南 | 搜索认证相关配置 |
| 公共组件 / 基础设施升级 | 各项目的 handover 提及版本号的地方 | 搜索版本号、组件名 |

**判断方法**：这次改的东西有没有 SDK、子域、共享配置、跨进程协议？

有 → 在所有依赖项目里搜一遍提到这件事的文档。

---

## 使用示例

### 示例 1：新增 API

**代码变更**：新增 `GET /api/v1/users/:id/profile` 路由

**要同步的文档**：

1. **CLAUDE.md**（如需）
   ```markdown
   ## API 路由清单
   - GET /api/v1/users/:id/profile — 获取用户资料
   ```

2. **docs/prd/user-profile.md**
   ```markdown
   ## API 设计
   - 路由：GET /api/v1/users/:id/profile
   - 参数：id（必需）
   - 返回：用户资料 JSON
   ```

3. **docs/design/architecture.md**
   ```markdown
   ## Routes
   - GET /api/v1/users/:id/profile
     - 数据流：API → UserService → Database
     - 权限：需要认证
   ```

4. **docs/handover/README.md**
   ```markdown
   ## 已完成功能
   - 用户资料 API（GET /api/v1/users/:id/profile）
   ```

**防膨胀检查**：
- CLAUDE.md 只加路由清单一行（~5 字符）
- 详细实现在 docs/design/
- 不在 CLAUDE.md 写历史叙事（"2026-06-03 新增用户资料 API"）

### 示例 2：新增环境变量

**代码变更**：新增 `DATABASE_MAX_CONNECTIONS=100` 环境变量

**要同步的文档**：

1. **CLAUDE.md**（如需）
   ```markdown
   ## 环境变量
   - DATABASE_MAX_CONNECTIONS — 数据库最大连接数（默认 100）
   ```

2. **docs/context/project-context.md**
   ```markdown
   ## 环境变量
   | 变量 | 说明 | 默认值 |
   |------|------|--------|
   | DATABASE_MAX_CONNECTIONS | 数据库最大连接数 | 100 |
   ```

3. **docs/handover/README.md**
   ```markdown
   ## 环境变量
   - DATABASE_MAX_CONNECTIONS：数据库连接池大小，生产环境建议 200
   ```

4. **如果下游需要配置**：
   - 下游项目的 `docs/integration-guide.md` 也要更新

### 示例 3：大特性（跨多文件）

**代码变更**：新增完整的"用户权限管理"特性（10+ 文件）

**要同步的文档**：

1. **docs/prd/permission-system.md**（新建）
   - 需求、用户故事、验收标准

2. **docs/design/architecture.md**（更新）
   - 新增"权限系统"章节
   - 数据模型：User、Role、Permission 表
   - 数据流：请求 → 权限中间件 → 业务逻辑

3. **docs/exec-plans/active/permission-impl.md**（新建，如触发计划触发器）
   - Phase 1：数据库 Schema
   - Phase 2：权限中间件
   - Phase 3：API 接口

4. **docs/handover/README.md**（更新）
   - 已完成：用户权限管理系统
   - 已知问题：角色继承尚未实现
   - 运维注意：权限缓存需要 Redis

5. **CLAUDE.md**（如需）
   - 不添加详细实现，只添加边界规则
   - 例如："权限检查必须在业务逻辑之前"

---

## 常见场景速查

| 我在做... | 我要改... |
|----------|----------|
| 添加新路由 | CLAUDE.md 路由清单 + docs/prd/ + docs/design/ + docs/handover/ |
| 改环境变量 | CLAUDE.md 环境变量表 + docs/context/project-context + docs/handover/ |
| 加数据库表 | CLAUDE.md 数据库表 + docs/design/architecture Data Model |
| 重构大模块 | docs/design/ + docs/exec-plans/ + docs/handover/ + docs/lessons/ |
| 修 Bug | docs/issues/ + （如发现新规则）CLAUDE.md |
| 改部署方式 | docs/handover/ + CLAUDE.md 部署章节 |

---

## 执行检查清单

完成代码变更后，逐项检查：

### 补漏检查
- [ ] 新增 API：在 prd、design、handover 都出现了
- [ ] 新增环境变量：在 project-context、handover 都出现了
- [ ] 新增数据库表：在 design 和 CLAUDE.md（如需）都出现了
- [ ] 跨项目影响：下游项目 docs 也改了

### 防膨胀检查
- [ ] CLAUDE.md 净涨幅 ≤ 30 行
- [ ] 没在 CLAUDE.md 抄 docs/ 详细机制
- [ ] 没新增历史叙事（"X 时刻起 Y 上线"）

### 一致性检查
- [ ] 同一条事实没在多个位置重复
- [ ] 指针表已包含所有详细机制的引用
- [ ] 所有相对时间转为绝对日期（`2026-06-03` 而非"今天"）

---

## 参考资料

- neat-freak 变更影响矩阵：`/tmp/khazix-skills/neat-freak/references/sync-matrix.md`
- 防膨胀规则：`docs/context/anti-bloat-rules.md`
- 文档所有权边界：`docs/context/source-of-truth-and-precedence.md`
