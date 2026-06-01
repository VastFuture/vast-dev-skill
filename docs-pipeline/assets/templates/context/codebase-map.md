# Codebase Map / 代码库地图

> 项目入口点、常见变更路线、脆弱文件。

## 入口点

| 文件 | 作用 |
|------|------|
| `<entry-point-1>` | 主入口，CLI 命令或 HTTP 服务入口 |
| `<entry-point-2>` | 次要入口或管理命令 |

## 目录结构

```
<project-root>/
├── src/                   # 源代码
│   ├── routes/           # HTTP 路由处理
│   ├── services/         # 业务逻辑
│   ├── models/           # 数据模型
│   └── utils/            # 工具函数
├── tests/                # 测试套件
├── config/               # 配置文件
└── docs/                  # 文档
```

## 常见变更路线

| 任务类型 | 修改位置 | 说明 |
|---------|---------|------|
| 添加 API | `src/routes/` + `src/services/` | 需要同步更新 owner docs |
| 修改数据模型 | `src/models/` | 影响多个模块，需评估影响 |
| 添加配置项 | `config/` | 注意环境变量优先级 |

## 脆弱文件

| 文件 | 脆弱原因 |
|------|---------|
| `<fragile-file-1>` | `<原因>` |
| `<fragile-file-2>` | `<原因>` |

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | `<framework/lang>` |
| 前端 | `<framework/lang>` |
| 数据库 | `<db-type>` |
| 部署 | `<deployment>` |