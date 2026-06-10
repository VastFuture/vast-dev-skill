# API 设计规范 (API Standard)

> 最后更新: [YYYY-MM-DD]
> ⚠️ **技术栈适配**：以下为 Java/Spring 示例。Python/FastAPI、Go、Rust 等项目请替换框架特有语法（如 `@RestController` → FastAPI router decorator，`@RequestBody` → Pydantic model）。

## 1. RESTful 风格

### URL 命名
- 小写 + 连字符（kebab-case）
- 名词复数形式表示资源集合

```
GET    /users              # 查询用户列表
POST   /users              # 创建用户
GET    /users/{id}         # 查询单个用户
PUT    /users/{id}         # 更新用户
DELETE /users/{id}         # 删除用户
```

### HTTP 方法语义

| 方法 | 语义 | 幂等 | 请求体 |
|------|------|------|--------|
| GET | 查询 | ✅ | 无（Query 参数） |
| POST | 创建 | ❌ | Command（JSON Body） |
| PUT | 更新 | ✅ | Command |
| DELETE | 删除 | ✅ | 无 |

### 参数风格
- **GET**：Query String（`@RequestParam` 或 DTO 自动绑定）
- **POST/PUT**：`@RequestBody` JSON Body
- **路径变量**：`{id}` 格式（`@PathVariable`）

---

## 2. 统一响应格式

### 成功响应

```json
// 单条
{ "id": "uuid-xxx", "name": "John Doe", "status": "NORMAL" }

// 分页
{ "records": [...], "total": 100, "size": 10, "current": 1 }
```

### 错误响应

使用 `ErrorResponse` 统一格式：

```json
{ "errorCode": "COMMON_RESOURCE_NOT_FOUND", "errorMessage": "User not found", "data": null }
```

### HTTP Status Code 映射

| 场景 | Status | ErrorCode 示例 |
|------|--------|----------------|
| 参数错误 | 400 | `COMMON_BAD_REQUEST` |
| 未授权 | 401 | `COMMON_UNAUTHORIZED_ACCESS` |
| 资源不存在 | 404 | `COMMON_RESOURCE_NOT_FOUND` |
| 业务冲突 | 409 | 各模块自定义 |
| 系统错误 | 500 | `COMMON_SYSTEM_INTERNAL_ERROR` |
| 服务不可用 | 503 | `COMMON_SERVER_NOT_AVAILABLE` |

---

## 3. 错误处理规范

### 异常体系

```
RuntimeException
 └── AbstractException (implements IError)
      ├── BusinessException    → 业务校验失败 (409)
      ├── SystemException      → 系统异常 (500)
      ├── ClientException      → 外部调用异常 (500)
      └── UnauthorizedException → 未授权 (401)
```

### 使用示例

```java
// 定义业务错误码
public enum DemoErrorCode implements IError {
    TICKET_NOT_FOUND("Ticket not found");
    @Override public ErrorGroup getErrorGroup() { return ErrorGroup.COMMON; }
    @Override public String getSubCode() { return this.name(); }
    @Override public String getMessage() { return this.message; }
}

// 抛出业务异常
throw new BusinessException(DemoErrorCode.TICKET_NOT_FOUND);
```

---

## 4. DTO 约定

### 命名

| 类型 | 后缀 | 示例 |
|------|------|------|
| 写操作入参 | `*Command` | `UserCreateCommand` |
| 读操作入参 | `*QueryDTO` | `UserQueryDTO` |
| 对外返回 | `*Response` | `UserResponse` |

### 分页
- 入参：`PageQuery`（`pageNumber=1`, `pageSize=10`）
- 出参：`PageResponse<T>`（`records`/`total`/`size`/`current`）

### 映射规则
- **adapter** 不操作 domain 实体
- **application**：Command→domain（`command.toEntity(currentUser)`），domain→Response（`Assembler`）
- 使用 **MapStruct**（`@Mapper(componentModel = "spring")`）

---

## 5. Header 规范

| Header | 必填 | 说明 | 来源 |
|--------|------|------|------|
| `Authorization` | 是 | `Bearer <token>` | 客户端 |
| `userId` | 是（内部） | 用户 ID | BFF 透传 |
| `userContext` | 是（内部） | JSON 序列化的 UserContext | BFF 透传 |

响应默认 `Content-Type: application/json`。
