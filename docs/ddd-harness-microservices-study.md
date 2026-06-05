# DDD Harness Microservices 学习成果

> 学习时间: 2026-06-05
> 项目地址: https://github.com/domain-driven-design/ddd-harness-microservices

## 1. 项目概述

DDD Harness Microservices 是一个全栈微服务脚手架，采用 Java 11 / Spring Boot 2.2.x 后端 + Vite + Vue 3 + TypeScript 前端的技术栈。

### 核心架构

```
Client → frontend → service-bff (鉴权/路由) → service-base / service-domain-demo
```

### 模块职责

| 模块 | 路径 | 职责 |
|------|------|------|
| service-bff | `backends/service-bff` | API 网关，统一入口、JWT 鉴权、路由转发 |
| service-base | `backends/service-base` | 基础域服务（用户、网点、操作日志、定时任务） |
| service-domain-demo | `backends/service-domain-demo` | 示例域服务，团队规范样板（CQRUD、测试、DB reset） |
| package-common | `backends/package-common` | 可复用 SDK，非独立部署 |

---

## 2. 文档体系结构

### 2.1 文档分类

```
docs/
├── standards/      # 开发规范（分层、API、DB、安全、命名）
├── features/       # 需求原始规格
├── designs/        # 系统设计现状（API、DB、业务规则、数据字典）
└── plans/          # 执行方案与变更记录
```

### 2.2 文档职责

| 目录 | 职责 | 更新频率 |
|------|------|----------|
| `standards/` | 开发规范，相对稳定 | 低频（架构变更时） |
| `features/` | 需求原始规格 | 中频（新需求时） |
| `designs/` | 系统当前设计现状 | 高频（每次变更） |
| `plans/` | 执行方案与变更记录 | 每轮任务 |

---

## 3. 核心规范亮点

### 3.1 四层架构规范

```text
adapter → application → domain ← infrastructure
```

**依赖方向（强制）**：
- adapter → application → domain
- infrastructure → domain（实现 domain 定义的接口）
- domain 不得依赖 infrastructure/adapter

**各层职责**：

| 层 | 职责 | 约束 |
|----|------|------|
| adapter | HTTP Controller、MQ Listener、参数校验 | ❌ 不含业务逻辑 |
| application | 用例编排、事务边界管理 | ❌ 不依赖 Web 框架 |
| domain | 核心业务逻辑、Entity/Aggregate/ValueObject | ❌ 不依赖 infrastructure |
| infrastructure | DB 持久化、外部 API、MQ、缓存 | ❌ 不含业务逻辑 |

### 3.2 DTO/Assembler/Converter 约定

| 类型 | 后缀 | 示例 |
|------|------|------|
| 写操作入参 | `*Command` | `UserCreateCommand` |
| 读操作入参 | `*QueryDTO` | `UserQueryDTO` |
| 对外返回 | `*Response` | `UserResponse` |

**映射组件**：
- Assembler：application 侧 DTO 转换（MapStruct）
- Converter：infrastructure 侧 PO ↔ domain 转换（MapStruct）

### 3.3 文档同步规则（核心亮点）

**每轮任务完成后必须检查**：
- [ ] `docs/designs/api.yaml` 是否需要更新？
- [ ] `docs/designs/db.md` 是否需要更新？
- [ ] `docs/designs/others/businessrule.md` 是否需要更新？
- [ ] `docs/designs/others/data-dict.md` 是否需要更新？

**PR/MR 描述中必须包含**：
- [ ] `docs/designs/` 同步检查（已更新 / 不涉及）

### 3.4 测试规范（TDD 原则）

**强制要求**：
1. **先写测试，后实现**：任何新 API 或业务逻辑，必须先编写测试用例
2. **测试即规格**：测试用例被视为需求规格的可执行版本
3. **红-绿-重构**：先运行测试看到失败（红），再编写最小代码使其通过（绿），最后重构优化

**测试覆盖要求**：
- 每个新 API **必须先编写** 集成测试
- 至少覆盖：1 个 Happy Path + 关键失败分支
- DB 相关用例必须可重复执行

### 3.5 PR/Change Checklist

```markdown
- 分层检查：adapter 不含业务逻辑；domain 不依赖 infrastructure；事务边界在 application
- 错误处理：业务校验使用 `BusinessException`，避免裸 `RuntimeException`
- DTO/映射：新增字段同步更新 Assembler/Converter，并保证向后兼容
- 安全：不记录 token/敏感信息；对外接口做鉴权/越权检查
- 验证：本地至少运行相关模块的测试
```

---

## 4. 与 docs-pipeline 的对比分析

### 4.1 文档结构对比

| 维度 | ddd-harness-microservices | docs-pipeline |
|------|---------------------------|---------------|
| **焦点** | 代码架构规范 | 文档管理流程 |
| **规范层** | standards/（分层、API、DB、安全） | agent-guides/（AI 行为指南） |
| **设计层** | designs/（系统现状） | design/（应用层设计） |
| **需求层** | features/（原始规格） | prd/（实现就绪需求） |
| **执行层** | plans/（变更记录） | exec-plans/（执行计划） |
| **同步机制** | 强制同步检查 | 无强制机制 |

### 4.2 核心差异

| 维度 | ddd-harness-microservices | docs-pipeline |
|------|---------------------------|---------------|
| **文档粒度** | 细粒度（每个规范独立文件） | 粗粒度（目录级管理） |
| **更新机制** | 强制同步（PR Checklist） | 无强制机制 |
| **代码关联** | 强关联（designs/ 反映代码现状） | 弱关联（文档独立于代码） |
| **AI 集成** | AGENTS.md 详细架构规范 | AGENTS.md 通用指令 |

### 4.3 可借鉴点

1. **文档同步机制**：强制要求每次变更后更新 designs/
2. **PR Checklist**：将文档同步检查纳入 PR 流程
3. **规范文件独立**：每个规范独立文件，便于维护和引用
4. **代码现状文档化**：designs/ 目录反映系统当前状态

---

## 5. 改进建议

### 5.1 融合方案

将 ddd-harness-microservices 的文档同步机制融入 docs-pipeline：

#### 方案 A：扩展 docs-pipeline 目录结构

```text
docs/
├── context/          # AI 上下文（现有）
├── backlog/          # 工作队列（现有）
├── prd/              # 需求文档（现有）
├── design/           # 应用层设计（现有）
├── exec-plans/       # 执行计划（现有）
├── lessons/          # 经验教训（现有）
├── standards/        # 【新增】开发规范
│   ├── layers.md     # 分层架构规范
│   ├── api.md        # API 设计规范
│   ├── db.md         # 数据库规范
│   └── security.md   # 安全规范
├── designs/          # 【新增】系统现状
│   ├── api.yaml      # API 现状
│   ├── db.md         # 数据库现状
│   └── others/       # 其他设计现状
└── agent-guides/     # AI 行为指南（现有）
```

#### 方案 B：增强同步机制

在 docs-pipeline 中增加同步检查：

1. **检测变更类型**：分析代码变更涉及的层（adapter/application/domain/infrastructure）
2. **提示同步更新**：根据变更类型提示需要更新的文档
3. **生成同步报告**：在执行报告中显示同步状态

#### 方案 C：集成 PR Checklist

在 AGENTS.md 中增加 PR Checklist 模板：

```markdown
## PR Checklist

### 文档同步
- [ ] docs/designs/ 是否需要更新？
- [ ] docs/standards/ 是否需要更新？

### 代码质量
- [ ] 分层检查：adapter 不含业务逻辑
- [ ] 错误处理：使用 BusinessException
- [ ] 测试覆盖：新增 API 有集成测试
```

### 5.2 具体改进点

#### 1. 增加 standards/ 目录

在 docs-pipeline 中增加开发规范目录，存放：
- 分层架构规范
- API 设计规范
- 数据库规范
- 安全规范

#### 2. 增加 designs/ 目录

增加系统现状目录，存放：
- API 现状（OpenAPI/Swagger）
- 数据库现状（表结构）
- 业务规则现状

#### 3. 增强同步检查

在 SKILL.md 中增加同步检查步骤：

```markdown
### 10. 文档同步检查

检测代码变更，提示需要同步更新的文档：

- 新增/修改 API → 更新 docs/designs/api.yaml
- 新增/修改数据表 → 更新 docs/designs/db.md
- 新增/修改业务规则 → 更新 docs/designs/others/businessrule.md
```

#### 4. 增加 PR Checklist 模板

在 AGENTS.md 模板中增加 PR Checklist：

```markdown
## PR Checklist

### 文档同步
- [ ] docs/designs/ 同步检查（已更新 / 不涉及）

### 代码质量
- [ ] 分层检查通过
- [ ] 错误处理规范
- [ ] 测试覆盖充分
```

---

## 6. 总结

### ddd-harness-microservices 的核心价值

1. **文档驱动开发**：文档与代码强关联，强制同步更新
2. **规范先行**：详细的开发规范，减少沟通成本
3. **质量保障**：PR Checklist 确保变更质量

### docs-pipeline 的改进方向

1. **增加规范层**：补充开发规范目录
2. **增加现状层**：补充系统设计现状目录
3. **增强同步机制**：强制文档同步检查
4. **集成 PR 流程**：将文档同步纳入 PR Checklist

### 融合策略

将 ddd-harness-microservices 的**文档同步机制**和**规范体系**融入 docs-pipeline，形成：

- **规范层**（standards/）：开发规范，相对稳定
- **现状层**（designs/）：系统现状，高频更新
- **流程层**（现有目录）：文档管理流程
- **同步机制**：强制文档同步检查

这样既保持了 docs-pipeline 的通用性，又吸收了 ddd-harness-microservices 的文档驱动开发优势。
