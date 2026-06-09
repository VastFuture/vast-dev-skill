# design/

应用层设计 + 系统现状（SDD 驱动）

## 职责

- 存放应用层的设计文档
- 同时记录设计意图和实现现状
- 是项目的"吸引子"（AGE 哲学）

## SDD 核心原则

1. **先写设计**：功能开发前，在这里写设计意图
2. **再写代码**：根据设计实现功能
3. **同步设计**：代码完成后，更新设计文档为实现现状
4. **设计即文档**：design/ 既是设计，也是文档

## 文件组织

按功能模块组织：

```
design/
├── auth/
│   ├── api.md           # API 设计
│   ├── db.md            # 数据模型
│   └── business-rule.md # 业务规则
├── user/
│   ├── api.md
│   └── db.md
└── README.md
```

## 与其他目录的关系

| 目录 | 关系 |
|------|------|
| `prd/` | PRD 是输入，design/ 是输出 |
| `architecture/` | architecture/ 是技术约束，design/ 是业务实现 |
| `standards/` | standards/ 是规范，design/ 是应用 |
| `plans/` | plans/ 规划如何实现，design/ 定义实现什么 |
