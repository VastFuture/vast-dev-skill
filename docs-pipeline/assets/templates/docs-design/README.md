# 设计文档索引

## 用途

`docs/design/` 存放稳定的应用层 owner docs。

此目录用于：

- 产品功能基线
- 页面和流程行为
- 角色和权限
- 应用外壳行为

## 范围边界

- `docs/prd/` 负责当前切片应该构建什么
- `docs/design/` 负责该切片被接受后的稳定应用层基线
- `ARCHITECTURE.md` 负责技术设计和跨功能结构

当一个功能同时依赖业务设计和技术设计时，将两个关注点放在不同文件中并交叉引用。

## 起步文件

- `app-overview.md` — 当前应用表面、角色和核心工作流
- `feature-inventory.md` — 功能清单和状态
- `roles-and-permissions.md` — 角色定义和访问规则
