# Designs - 系统设计现状

本目录存放系统的当前设计现状，反映代码的实际状态。

## 重要原则

> **本文档必须与代码保持同步**
>
> 每次代码变更后，检查本目录是否需要更新。

## 目录结构

```
designs/
├── README.md      # 本文件
├── api.yaml       # API 现状（OpenAPI/Swagger）
├── db.md          # 数据库现状（表结构）
└── others/        # 其他设计现状
    ├── businessrule.md  # 业务规则现状
    └── data-dict.md     # 数据字典现状
```

## 同步检查规则

### 何时更新

| 变更类型 | 需要更新的文档 |
|----------|---------------|
| 新增/修改 API | `api.yaml` |
| 新增/修改数据表 | `db.md` |
| 新增/修改业务规则 | `others/businessrule.md` |
| 新增/修改数据字典 | `others/data-dict.md` |

### 同步检查流程

1. **代码变更后**：检查是否涉及上述变更类型
2. **更新文档**：如果涉及，更新对应文档
3. **PR 检查**：在 PR 描述中确认文档已同步

### PR Checklist

```markdown
## 文档同步检查

- [ ] `docs/designs/` 同步检查（已更新 / 不涉及）
  - 新增/修改 API → 更新 `docs/designs/api.yaml`
  - 新增/修改数据表 → 更新 `docs/designs/db.md`
  - 新增/修改业务规则 → 更新 `docs/designs/others/businessrule.md`
  - 新增/修改数据字典 → 更新 `docs/designs/others/data-dict.md`
```

## 使用方式

- **新人入职**：阅读本目录了解系统当前状态
- **代码审查**：参照本文档检查变更是否符合设计
- **AI 辅助**：AI Agent 参照本文档理解系统现状

## 文档格式

### api.yaml

使用 OpenAPI 3.0 格式描述 API：

```yaml
openapi: 3.0.0
info:
  title: API Title
  version: 1.0.0
paths:
  /users:
    get:
      summary: 查询用户列表
      responses:
        '200':
          description: 成功
```

### db.md

使用 SQL DDL 描述表结构：

```sql
CREATE TABLE user (
    id VARCHAR(64) NOT NULL PRIMARY KEY COMMENT '用户ID',
    name VARCHAR(64) NOT NULL COMMENT '用户名',
    -- 其他字段...
);
```

### others/businessrule.md

描述业务规则：

```markdown
## 规则名称

**触发条件**：...
**处理逻辑**：...
**异常处理**：...
```

### others/data-dict.md

描述数据字典：

```markdown
## 字典名称

| 编码 | 名称 | 说明 |
|------|------|------|
| 01 | 状态1 | 说明1 |
| 02 | 状态2 | 说明2 |
```
