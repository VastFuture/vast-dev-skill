# 数据库设计现状 (Database Design)

> 最后更新: [YYYY-MM-DD]
>
> 本文档描述系统当前所有数据库表的定义。当新增或修改表时请同步更新本文件。

---

## 同步检查规则

| 变更类型 | 操作 |
|----------|------|
| 新增表 | 在对应模块下添加表定义 |
| 修改表 | 更新表定义，添加变更说明 |
| 删除表 | 从文档中移除，记录在变更历史 |

---

## 表定义模板

```sql
CREATE TABLE table_name (
    id           VARCHAR(64)   NOT NULL PRIMARY KEY COMMENT 'ID',
    -- 业务字段
    field1       VARCHAR(64)   NOT NULL COMMENT '字段1说明',
    field2       INT           NULL COMMENT '字段2说明',
    -- 公共字段（所有表必须包含）
    created_by   VARCHAR(64)   NOT NULL COMMENT '创建人',
    created_time DATETIME      DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '创建时间',
    updated_by   VARCHAR(64)   NOT NULL COMMENT '更新人',
    updated_time DATETIME      DEFAULT CURRENT_TIMESTAMP NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) COMMENT '表说明' CHARSET = utf8mb4;
```

---

## 模块名

<!-- 在此添加该模块的表定义 -->

### table_name — 表说明

```sql
CREATE TABLE table_name (
    id           VARCHAR(64)   NOT NULL PRIMARY KEY COMMENT 'ID',
    -- 业务字段
    created_by   VARCHAR(64)   NOT NULL COMMENT '创建人',
    created_time DATETIME      DEFAULT CURRENT_TIMESTAMP NOT NULL COMMENT '创建时间',
    updated_by   VARCHAR(64)   NOT NULL COMMENT '更新人',
    updated_time DATETIME      DEFAULT CURRENT_TIMESTAMP NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) COMMENT '表说明' CHARSET = utf8mb4;
```

**字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | VARCHAR(64) | 是 | 主键，UUID |
| created_by | VARCHAR(64) | 是 | 创建人 ID |
| created_time | DATETIME | 是 | 创建时间 |
| updated_by | VARCHAR(64) | 是 | 更新人 ID |
| updated_time | DATETIME | 是 | 更新时间 |

---

## 表关系图

```
<!-- 在此添加表关系图 -->

table1 ──1:N──> table2
```

---

## 变更历史

| 日期 | 变更类型 | 表名 | 说明 |
|------|----------|------|------|
| [YYYY-MM-DD] | 新增 | table_name | 初始创建 |
