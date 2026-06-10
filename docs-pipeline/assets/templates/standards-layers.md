# 分层架构规范 (Layers Standard)

> 最后更新: [YYYY-MM-DD]
> ⚠️ **技术栈适配**：以下为 Java/Spring 示例。Python/FastAPI、Go、Rust 等项目请将分层名称替换为对应技术栈的术语（如 Python: router→service→model→repository）。

## 概述

本工程采用 **四层架构**，每个业务服务模块严格遵循以下分层。依赖方向为单向，禁止反向依赖。

```
adapter → application → domain ← infrastructure
```

---

## 1. adapter（对外适配层）

**职责**：HTTP Controller 入/出参协议转换、MQ Listener 消息接收、Scheduler 触发入口、参数基础校验

**约束**：
- ❌ 不包含业务逻辑
- ❌ 不直接操作 domain 实体
- ❌ 不调用 infrastructure 层
- ❌ 不引入 PO / Mapper 依赖
- ✅ 入参使用 Command / QueryDTO，出参使用 Response

**命名**：`*Controller`，统一使用 `@RestController` + `@RequestMapping`

---

## 2. application（用例编排层）

**职责**：业务用例编排与流程控制、组合 domain 行为、调用 repository/client、**事务边界管理**、Command→domain 转换、domain→Response 转换（通过 Assembler）

**约束**：
- ❌ 不依赖 Web 框架对象（HttpServletRequest/Response）
- ❌ 不包含基础设施代码
- ✅ 只依赖 domain 层定义的接口
- ✅ 方法粒度 = 一个用例

**命名**：
- Service：`*AppService` 或 `*Service`
- Assembler：`*Assembler`
- Command：`*Command`（如 `UserCreateCommand`）
- Query：`*QueryDTO`（如 `UserQueryDTO`）
- Response：`*Response`（如 `UserResponse`）

---

## 3. domain（领域模型层）

**职责**：核心业务逻辑与业务不变量、Entity / Aggregate / ValueObject / DomainService、状态机与业务规则校验、Repository 接口定义

**约束**：
- ❌ 不依赖 infrastructure / adapter 层
- ❌ 不引入 Spring 框架注解（除纯 Lombok）
- ❌ 不依赖 Web 框架对象
- ✅ 纯 POJO + Lombok
- ✅ 通过 `BusinessException` 报告业务校验失败

---

## 4. infrastructure（基础设施层）

**职责**：DB 持久化（PO + Mapper + RepositoryImpl）、外部 API 调用（Feign Client）、MQ 消息发送、缓存 / 配置 / 分布式锁

**约束**：
- ❌ 不包含业务逻辑
- ✅ 实现 domain 层定义的 Repository 接口
- ✅ 使用 `*RepositoryImpl` 命名实现类

---

## 5. 依赖方向（强制）

```
adapter  →  application  →  domain  ←  infrastructure
```

### 常见违规检查项

- adapter 中是否出现 `if (status.equals(...))` 业务判断？
- domain 中是否 `import` 了 `infra` 或 `mapper` 的类？
- PO 是否在 application/adapter 层被直接使用？
- `@Transactional` 是否放在了 domain 方法上？

---

## 6. 公共模块分层说明

| 模块 | 结构特点 |
|------|----------|
| **common** | 无四层结构，按功能分包（auth/error/domain/lock/datadictionary/businessrule） |
| **bff** | Spring Cloud Gateway 模式，只做鉴权与路由，无业务分层 |

---

## 7. 已知问题

<!-- 记录当前架构中的已知问题，便于后续改进 -->

- [ ] 待补充
