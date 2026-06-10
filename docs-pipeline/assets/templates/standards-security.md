# 安全规范 (Security Standard)

> 最后更新: [YYYY-MM-DD]
> ⚠️ **技术栈适配**：以下为 Java/BFF 示例。Python/FastAPI、Go 等项目请替换框架特有安全机制。

## 1. 认证架构

BFF（Backend For Frontend）模式：

```
Client → BFF (Gateway) → Backend Services
          ┌─ 校验 JWT Token
          ├─ 解析 UserContext
          └─ Header 透传 userId / userContext
```

### 请求流程

1. 客户端携带 `Authorization: Bearer <token>` 请求 BFF
2. `AuthenticationFilter`（GlobalFilter）校验 Token：
   - 空或格式错误 → 401
   - 签名无效 → 401
   - 成功 → 提取 UserContext
3. BFF 将 `userId` 和 `userContext`（JSON）写入请求 Header 透传
4. 后端 `UserContextInitializationFilter` 从 Header 解析并写入 `UserContextHolder`（ThreadLocal）
5. 应用层通过 `AuthService.currentUser()` 获取用户上下文

### 约束
- ❌ 后端服务不得自行解析 JWT，统一由 BFF 完成
- ❌ 应用层/领域层不得依赖 Web 框架对象（Request/Response）
- ✅ 只能通过 `AuthService` 或 `UserContext` 获取用户上下文

---

## 2. Token 规范

| 项目 | 值 |
|------|-----|
| 算法 | HS256 |
| Header | `userContext`（JSON 序列化的完整 UserContext） |
| Subject | 用户名 |
| 过期时间 | 1 小时 |

### Secret Key 安全
- 生产环境必须替换为独立密钥管理方案（Vault / KMS）
- 禁止硬编码在代码中

### 透传 Header

| Header | 类型 | 说明 |
|--------|------|------|
| `userId` | String | 当前用户 ID |
| `userContext` | String(JSON) | 完整用户上下文 |

---

## 3. 用户上下文 (UserContext)

```java
@Data @Builder
public class UserContext {
    private String userId;
    private String userName;
    private ContextUserIdentity currentIdentity;

    @Data @Builder
    public static class ContextUserIdentity {
        private String permissionBranchId;
        private List<UserIdentityRole> roles;
    }
}
```

**获取方式**：
```java
UserContext user = authService.currentUser();
String userId = authService.currentUserId();
```

---

## 4. 安全编码规范

| 类别 | 要求 |
|------|------|
| 输入校验 | Bean Validation（`@Valid` / `@NotNull`） |
| SQL 防护 | 禁止字符串拼接，使用参数绑定 `#{}` |
| 日志安全 | ❌ 不记录 Authorization Header / Token / 敏感信息 |
| 输出安全 | ❌ 不泄露 StackTrace / SQL / 文件路径 |
| 越权检查 | 操作资源前验证归属/权限 |

---

## 5. 分布式锁

**使用场景**：
- 防止重复提交
- 资源竞争控制
- 定时任务互斥

**实现方式**：
- Redis（推荐）
- 数据库（备选）

---

## 6. 敏感信息保护

| 类型 | 处理方式 |
|------|----------|
| 数据库密码 | 环境变量 / 配置中心注入 |
| JWT Secret | 密钥管理服务，禁止硬编码 |
| Token | BFF 解析后透传，后端不存储 |
