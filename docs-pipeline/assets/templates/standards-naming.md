# 命名规范 (Naming Standard)

> 最后更新: [YYYY-MM-DD]

## 1. 通用原则

1. **可读性优先**：名称应清晰表达含义，避免缩写
2. **一致性**：同类事物使用相同命名模式
3. **语言统一**：代码使用英文，注释可使用中文

---

## 2. 代码命名

### 包名
- 全小写，使用点分隔
- 格式：`com.{公司}.{项目}.{模块}.{层}`
- 示例：`com.example.user.domain.aggregate`

### 类名
- 大驼峰（PascalCase）
- 后缀表达类型：

| 类型 | 后缀 | 示例 |
|------|------|------|
| Controller | `*Controller` | `UserController` |
| Service | `*Service` / `*AppService` | `UserService` |
| Repository | `*Repository` / `*RepositoryImpl` | `UserRepository` |
| Entity | 无特殊后缀 | `User`, `Branch` |
| Value Object | 无特殊后缀 | `Money`, `Address` |
| DTO | `*Command` / `*QueryDTO` / `*Response` | `UserCreateCommand` |
| Mapper | `*Mapper` | `UserMapper` |
| PO | `*PO` | `UserPO` |
| Assembler | `*Assembler` | `UserAssembler` |
| Converter | `*Converter` | `UserConverter` |

### 方法名
- 小驼峰（camelCase）
- 动词开头，表达行为：

| 场景 | 前缀 | 示例 |
|------|------|------|
| 查询 | `get` / `find` / `query` | `getUserById()` |
| 创建 | `create` / `add` / `insert` | `createUser()` |
| 更新 | `update` / `modify` | `updateUser()` |
| 删除 | `delete` / `remove` | `deleteUser()` |
| 判断 | `is` / `has` / `can` | `isActive()` |

### 变量名
- 小驼峰（camelCase）
- 简洁明了，避免单字母（循环变量除外）

### 常量名
- 全大写，下划线分隔
- 示例：`MAX_RETRY_COUNT`, `DEFAULT_PAGE_SIZE`

---

## 3. 数据库命名

### 表名
- 小写蛇形（snake_case）
- 单数形式
- 示例：`user`, `branch`, `operation_log`

### 字段名
- 小写蛇形（snake_case）
- 示例：`user_id`, `created_by`, `updated_time`

### 索引名
- 格式：`idx_{表名}_{字段名}`
- 示例：`idx_user_name`, `idx_order_status`

### 外键名
- 格式：`fk_{表名}_{引用表}`
- 示例：`fk_order_user`

---

## 4. API 命名

### URL 路径
- 小写，连字符分隔（kebab-case）
- 名词复数形式
- 示例：`/users`, `/user-roles`

### Query 参数
- 小驼峰（camelCase）
- 示例：`?pageNumber=1&pageSize=10`

### Header
- 请求头：`X-` 前缀（自定义）或标准名称
- 示例：`X-Request-Id`, `Authorization`

---

## 5. 配置命名

### 环境变量
- 全大写，下划线分隔
- 示例：`DATABASE_URL`, `REDIS_HOST`

### 配置文件
- 小写，连字符或点分隔
- 示例：`application-dev.yml`, `logback.xml`

---

## 6. 文件命名

### 代码文件
- 与类名一致
- 示例：`UserController.java`, `UserService.java`

### 配置文件
- 小写，连字符分隔
- 示例：`application.yml`, `bootstrap.yml`

### 文档文件
- 小写，连字符分隔
- 示例：`api-design.md`, `database-schema.md`

---

## 7. Git 命名

### 分支
- 格式：`{类型}/{描述}`
- 示例：`feature/user-login`, `fix/order-bug`, `docs/api-guide`

### Commit
- 格式：`{类型}: {描述}`
- 示例：`feat: add user login`, `fix: resolve order bug`

### 类型
- `feat`: 新功能
- `fix`: 修复
- `docs`: 文档
- `style`: 格式
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建/工具
