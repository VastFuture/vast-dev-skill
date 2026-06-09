# design/

> 应用层设计 + 系统现状 — AGE × DDD 融合驱动

## 两大哲学

### 吸引子（AGE）

> [Attractor-Guided Engineering](https://github.com/entropy-cloud/attractor-guided-engineering-template)

**"设计是稳定的吸引子，代码向设计收敛。"**
先写设计，再写代码，设计即文档。

### 代码即真相（DDD）

> [ddd-harness-microservices](https://github.com/domain-driven-design/ddd-harness-microservices)

**"代码是唯一真相，设计文档必须跟上代码。"**
每次代码变更后，design/ 必须同步更新。

## SDD 融合循环

```
① 写设计意图 ──▶ ② 按设计实现 ──▶ ③ 测试验证 ──▶ ④ 同步到设计（反映现状）
      AGE                AGE             两者              DDD
```

## 目录结构

```
design/
├── README.md              # 本文件
├── api.yaml               # API 接口列表
├── db.md                  # 数据库表结构
├── business-rule.md       # 业务规则（不变量、状态机）
├── data-dict.md           # 数据字典（枚举值、字段映射）
├── <module>/              # 按模块组织（可选）
│   ├── api.md
│   ├── db.md
│   └── overview.md
└── <module>/
```

**两种组织方式**：小项目用扁平文件，多模块项目用模块目录。

## 与其他目录的关系

| 目录 | 关系 |
|------|------|
| `prd/` | PRD 定义"要做什么" → design/ 定义"怎么做" |
| `architecture/` | architecture/ 是技术约束 → design/ 在此约束下设计 |
| `standards/` | standards/ 是编码规范 → design/ 应用这些规范 |
| `exec-plans/active/` | 实现后回写 design/ |
| `lessons/` | 设计失误的教训 → design/ 避免重蹈覆辙 |

## 同步 Checklist

- [ ] 新增/修改 API → 更新 `api.yaml`
- [ ] 新增/修改数据表 → 更新 `db.md`
- [ ] 新增/修改业务规则 → 更新 `business-rule.md`
- [ ] 新增/修改数据字段 → 更新 `data-dict.md`

**铁律**：代码合入即同步，不积压。
