# 数据库表结构

> 新增/修改数据表后更新此文件。删表时同步移除对应条目。

## 表列表

<!-- TODO: 列出所有数据表 -->

### <示例表名>

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | uuid | PK | 主键 |
| created_at | timestamp | NOT NULL, DEFAULT NOW() | 创建时间 |
| updated_at | timestamp | NOT NULL | 更新时间 |

**索引**：
- `<idx_name>` (`<columns>`)

**外键**：
- `<column>` → `<ref_table>.<ref_column>`

## 更新记录

| 日期 | 变更 | 关联 PR |
|------|------|---------|
| - | - | - |
