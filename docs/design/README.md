# design/

> 应用层设计 + 系统现状 — AGE × DDD 融合驱动

---

## 两大哲学

### 吸引子（AGE）

> 来源：[Attractor-Guided Engineering](https://github.com/entropy-cloud/attractor-guided-engineering-template)

**"设计是稳定的吸引子，代码向设计收敛。"**

```
design/（设计意图）
    │
    ▼ 吸引代码向设计收敛
src/（代码实现）
    │
    ▼ 验证实现是否符合意图
tests/（测试验证）
```

design/ 定义了"系统应该是什么样"。写代码前先把设计想清楚，设计即文档。

### 代码即真相（DDD）

> 来源：[ddd-harness-microservices](https://github.com/domain-driven-design/ddd-harness-microservices)

**"代码是唯一真相，设计文档必须跟上代码。"**

```
src/（代码实现，唯一真相源）
    │
    ▼ 从代码中提取现状
design/（系统现状快照）
    │
    ▼ PR Checklist 强制同步
always in sync
```

每次代码变更后，design/ 必须同步更新。代码说了才算。

---

## SDD 融合循环

融合两套哲学，形成 **SDD（Spec-Driven Development）** 双向同步：

```
┌────────────────────────────────────────────────┐
│                      SDD                        │
│                                                  │
│   ① 写设计意图 ──▶ ② 按设计实现 ──▶ ③ 测试验证  │
│        ▲                                 │       │
│        │         ┌───────────────┐        │       │
│        └─────── │ ④ 同步到设计   │ ◀─────┘       │
│                 │   反映现状      │               │
│                 └───────────────┘               │
└────────────────────────────────────────────────┘
```

| 阶段 | 动作 | 体现的哲学 |
|------|------|-----------|
| ① 写设计意图 | 功能开发前，在这里写"要做什么"、"数据结构"、"接口定义" | **AGE** |
| ② 按设计实现 | 代码严格按设计意图编写 | **AGE** |
| ③ 测试验证 | 通过测试验证实现正确 | 两者 |
| ④ 同步到设计 | 代码完成后，更新设计文档反映实际实现 | **DDD** |

**核心原则**：
- 设计意图写完 → 代码才能开写（AGE）
- 代码写完 → 设计文档必须同步（DDD）
- 单一真相源：`design/` 同时承载意图和现状

---

## 目录结构

```
design/
├── README.md              # 本文件
├── api.yaml               # API 接口列表（路径、方法、参数、响应格式）
├── db.md                  # 数据库表结构（表名、字段、索引、约束）
├── business-rule.md       # 业务规则（不变量、校验、状态机）
├── data-dict.md           # 数据字典（字段含义、枚举值、映射关系）
├── <module>/              # 按模块组织（可选）
│   ├── api.md
│   ├── db.md
│   └── overview.md
└── <module>/
```

**两种组织方式**：

| 方式 | 适用场景 | 示例 |
|------|---------|------|
| 扁平文件 | 小项目、单体应用 | `api.yaml` + `db.md` + `business-rule.md` |
| 模块目录 | 多模块项目、微服务 | `user/api.md` + `user/db.md` + `order/api.md` |

---

## 文件说明

### api.yaml / api.md

API 接口清单。记录每个端点的路由、方法、请求/响应格式。

```yaml
# api.yaml
/api/users:
  GET:
    description: 获取用户列表
    params:
      page: int (optional)
    response: { users: [{ id, name }], total: int }
  POST:
    description: 创建用户
    body: { name: str, email: str }
    response: { id, name, email }
```

### db.md

数据库表结构。记录表名、字段类型、索引和约束。

```markdown
## users

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| id | uuid | PK | 用户ID |
| name | varchar(100) | NOT NULL | 用户名 |
| email | varchar(255) | UNIQUE, NOT NULL | 邮箱 |

**索引**：idx_users_email(email)
```

### business-rule.md

业务规则。记录不变量、状态流转和核心校验。

```markdown
## 用户注册

- 邮箱必须唯一
- 密码长度 ≥ 8 位
- 注册后自动创建默认工作区

## 订单状态机

pending → paid → shipped → delivered
  ↓
cancelled
```

### data-dict.md

数据字典。记录字段含义、枚举值和映射关系。

```markdown
## 用户状态

| 值 | 含义 | 说明 |
|----|------|------|
| active | 活跃 | 正常使用的用户 |
| suspended | 暂停 | 违规暂停，可恢复 |
| deleted | 已删除 | 软删除，不可恢复 |

## 订单类型

- `standard` — 标准订单
- `rush` — 加急订单（额外收费）
```

---

## 与其他目录的关系

| 目录 | 关系 | 数据流向 |
|------|------|---------|
| `prd/` | PRD 定义"要做什么" → design/ 定义"怎么做" | 输入 |
| `architecture/` | architecture/ 是技术约束 → design/ 在此约束下设计 | 约束 |
| `standards/` | standards/ 是编码规范 → design/ 应用这些规范 | 约束 |
| `exec-plans/active/` | exec-plans/ 规划如何实现 → 实现后回写 design/ | 输出 ↔ 反馈 |
| `lessons/` | 设计失误的教训 → design/ 避免重蹈覆辙 | 反馈 |

---

## 与模板同步的 PR Checklist

每次代码变更后，检查以下文档是否需要更新：

- [ ] **新增/修改 API** → 更新 `api.yaml` 或 `*/api.md`
- [ ] **新增/修改数据表** → 更新 `db.md` 或 `*/db.md`
- [ ] **新增/修改业务规则** → 更新 `business-rule.md`
- [ ] **新增/修改数据字段** → 更新 `data-dict.md`
- [ ] **删除或重构** → 删除对应条目，保持文档精简

**不要等待**：代码合入即同步，不做"稍后补"。

---

## 铁律

1. **一源两用**：一个 design/ 文件，既是"设计意图"也是"系统现状"
2. **设计先行**：先写设计，再写代码（AGE）
3. **代码驱动更新**：代码完成后，必须把实际状态写回设计（DDD）
4. **不积压**：每次 PR 同步，不累计到"大扫除"
5. **不重复**：不要在 prd/ 和 design/ 写同一件事，prd/ 定义"做什么"，design/ 定义"怎么做"
