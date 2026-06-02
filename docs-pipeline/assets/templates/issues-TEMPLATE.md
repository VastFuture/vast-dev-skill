# 问题记录：[问题标题]

> 创建日期：YYYY-MM-DD
> 状态：🔍 调查中 / 🔧 修复中 / ✅ 已解决 / ❌ 无法复现
> 严重程度：🔴 严重 / 🟡 中等 / 🟢 轻微
> 负责人：[姓名]

## 问题描述

### 现象

[问题的具体表现，包括错误信息、截图、日志等]

### 复现步骤

1. [步骤1]
2. [步骤2]
3. [步骤3]

### 预期行为

[应该发生什么]

### 实际行为

[实际发生了什么]

## 影响范围

- **影响功能**：[哪些功能受影响]
- **影响用户**：[哪些用户受影响]
- **影响程度**：[完全不可用 / 部分功能受限 / 体验问题]

## 调查过程

### 初步分析

[初步判断可能的原因]

### 根本原因

[深入分析后的根本原因]

### 相关代码

```
[相关代码片段或文件路径]
```

## 解决方案

### 方案描述

[如何解决这个问题]

### 实现细节

[具体的实现步骤]

### 验证方法

[如何验证问题已解决]

1. [验证步骤1]
2. [验证步骤2]
3. [验证步骤3]

## 经验教训

### 预防措施

[如何避免类似问题再次发生]

### 改进建议

[流程、工具、文档等方面的改进建议]

## 相关资源

- [相关 Issue]
- [相关 PR]
- [相关文档]

## 变更记录

| 日期 | 变更内容 | 负责人 |
|------|---------|--------|
| YYYY-MM-DD | 创建问题记录 | [姓名] |

---

## 示例

# 问题记录：用户登录接口响应超时

> 创建日期：2026-06-01
> 状态：✅ 已解决
> 严重程度：🔴 严重
> 负责人：张三

## 问题描述

### 现象

用户登录接口 `/api/auth/login` 响应时间异常缓慢，平均耗时 5.2 秒，严重影响用户体验。错误日志显示大量慢查询告警。

```
[ERROR] 2026-06-01 14:23:15 - Slow query detected: SELECT * FROM user_permissions WHERE user_id IN (1,2,3...) - 4.8s
[WARN] 2026-06-01 14:23:20 - Login timeout threshold exceeded: 5000ms
```

### 复现步骤

1. 启动应用服务器和数据库
2. 使用 JMeter 发送 100 个并发登录请求
3. 观察接口响应时间监控

### 预期行为

登录接口应在 500ms 内返回结果，用户能够快速完成登录操作。

### 实际行为

接口响应时间达到 5+ 秒，用户界面出现长时间等待，部分用户因超时而登录失败。

## 影响范围

- **影响功能**：用户登录、权限验证、会话管理
- **影响用户**：所有需要登录的用户（约 10000+ 活跃用户）
- **影响程度**：完全不可用（响应超时导致登录失败）

## 调查过程

### 初步分析

通过 APM 监控发现瓶颈在数据库查询环节，怀疑是权限查询逻辑存在 N+1 查询问题。

### 根本原因

代码审查发现 `UserService.loadUserPermissions()` 方法存在严重的 N+1 查询问题：
- 每次用户登录都会查询该用户的所有权限模块
- 每个权限模块又单独查询其子权限列表
- 100 个权限模块 = 101 次数据库查询（1 + 100）

### 相关代码

```java
// UserService.java:156-180
public List<Permission> loadUserPermissions(Long userId) {
    // 第一次查询：获取用户权限模块
    List<PermissionModule> modules = permissionMapper.findModulesByUserId(userId);
    
    List<Permission> allPermissions = new ArrayList<>();
    for (PermissionModule module : modules) {
        // N 次查询：每个模块单独查询权限列表 - 这就是问题所在！
        List<Permission> permissions = permissionMapper.findPermissionsByModuleId(module.getId());
        allPermissions.addAll(permissions);
    }
    
    return allPermissions;
}
```

## 解决方案

### 方案描述

使用 Redis 缓存用户权限数据，同时优化 SQL 查询逻辑，采用 JOIN 查询一次性获取所有权限数据。

### 实现细节

1. **添加 Redis 权限缓存**
   - 缓存 key: `user:permissions:{userId}`
   - 缓存时间: 30 分钟
   - 权限变更时主动清理缓存

2. **优化 SQL 查询**
   ```sql
   -- 原来的 N+1 查询优化为单次 JOIN 查询
   SELECT p.* FROM permissions p
   INNER JOIN permission_modules pm ON p.module_id = pm.id
   INNER JOIN user_permissions up ON pm.id = up.module_id
   WHERE up.user_id = ?
   ```

3. **添加缓存逻辑**
   ```java
   public List<Permission> loadUserPermissions(Long userId) {
       String cacheKey = "user:permissions:" + userId;
       List<Permission> cached = redisTemplate.get(cacheKey);
       if (cached != null) return cached;
       
       // 优化后的单次查询
       List<Permission> permissions = permissionMapper.findUserPermissionsOptimized(userId);
       redisTemplate.setex(cacheKey, 1800, permissions); // 30分钟缓存
       return permissions;
   }
   ```

### 验证方法

1. 执行单元测试验证缓存逻辑正确性
2. 使用 JMeter 重复并发测试场景
3. 监控数据库慢查询日志确认优化效果

## 经验教训

### 预防措施

1. **代码审查强化**：针对数据库查询代码增加 N+1 查询检查清单
2. **性能测试左移**：在开发阶段就进行并发性能测试
3. **监控告警完善**：设置接口响应时间阈值告警（>1s 触发）

### 改进建议

1. **引入 MyBatis-Plus**：使用其内置的批量查询功能避免 N+1 问题
2. **数据库索引优化**：为 `user_permissions.user_id` 和 `permissions.module_id` 添加复合索引
3. **缓存策略统一**：制定统一的缓存命名和失效策略规范

## 相关资源

- [GitHub Issue #1234](https://github.com/example/project/issues/1234)
- [优化 PR #5678](https://github.com/example/project/pull/5678)
- [性能优化文档](./docs/performance-optimization.md)

## 变更记录

| 日期 | 变更内容 | 负责人 |
|------|---------|--------|
| 2026-06-01 | 创建问题记录 | 张三 |
| 2026-06-01 | 完成根因分析 | 张三 |
| 2026-06-01 | 实施缓存优化方案 | 张三 |
| 2026-06-01 | 验证修复效果，问题解决 | 张三 |
