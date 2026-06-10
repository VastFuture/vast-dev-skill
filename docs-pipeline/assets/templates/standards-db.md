# 数据库规范 (Database Standard)

> 最后更新: [YYYY-MM-DD]
> ⚠️ **技术栈适配**：以下为 Java/MyBatis-Plus 示例。Python/SQLAlchemy、Go/GORM 等项目请替换 ORM 特有语法。

## 1. 通用约定

| 项目 | 约定 |
|------|------|
| 字符集 | `utf8mb4`（`CHARSET = utf8mb4`） |
| 排序规则 | `utf8mb4_bin` |
| 存储引擎 | InnoDB |

### 命名规范

| 对象 | 规则 | 示例 |
|------|------|------|
| 表名 | 小写蛇形（snake_case），单数 | `user`, `branch`, `operation_log` |
| 字段 | 小写蛇形 | `current_identity_id`, `maintain_by` |
| 主键 | `id` VARCHAR(64) | UUID 字符串 |
| 外键 | `{引用表}_id` | `user_id`, `ticket_id` |

### 公共字段（所有表必须包含）

```sql
created_by   varchar(64)   not null comment '创建人',
created_time datetime      default CURRENT_TIMESTAMP not null comment '创建时间',
updated_by   varchar(64)   not null comment '更新人',
updated_time datetime      default CURRENT_TIMESTAMP not null on update CURRENT_TIMESTAMP comment '更新时间'
```

- 字段顺序：业务字段在前，公共字段在最后
- `created_by` / `updated_by` 存储用户 ID

### 可选审计字段

```sql
deleted     tinyint(1) default 0 not null comment '是否删除',
version     int        default 1 not null comment '乐观锁版本'
```

---

## 2. 建表规范

### 主键
- `VARCHAR(64)`，UUID 字符串（通过 `IdUtil.uuid()` 生成）
- 不使用自增 ID（分布式环境不适用）

### 字段类型映射

| Java 类型 | MySQL 类型 |
|-----------|-----------|
| String | `VARCHAR(64)` / `VARCHAR(128)` / `TEXT` |
| Integer / int | `INT` |
| Boolean | `TINYINT(1)` |
| Enum | `VARCHAR(50)`（推荐）或 `ENUM` |
| OffsetDateTime / LocalDateTime | `datetime` |
| Long / BigInteger | `BIGINT` |
| BigDecimal | `DECIMAL(18,2)` |

### 索引规范
- 主键索引：`PRIMARY KEY (id)`
- 外键字段建普通索引（非 FK 约束）
- 查询频繁字段加单列索引

---

## 3. 迁移管理

**路径**：`src/main/resources/db/migration/`

**命名规则**：
```
V<YYYYMMDD>__<description>.sql
```

**约束**：
- 已发布的迁移脚本禁止修改
- 增量变更通过新脚本实现
- 每个脚本保证幂等性

---

## 4. ORM 规范

### PO（持久化对象）
- 位置：`infrastructure/persistence/po/`
- 命名：`*PO`（如 `UserPO`）
- 使用 `@TableName` 映射表名

### Mapper
- 位置：`infrastructure/persistence/mapper/`
- 命名：`*Mapper`
- 读写分离：`mapper/base/`（CRUD）+ `mapper/query/`（复杂查询）

### XML
- 位置：`src/main/resources/mapper/`
- namespace 指向 Mapper 接口全限定名
- 复杂查询手写 XML，简单 CRUD 用 ORM 内置方法

---

## 5. 现有数据表

| 模块 | 表名 | 说明 |
|------|------|------|
| <!-- 待补充 --> | | |

详细设计参见 `docs/design/db.md`。
