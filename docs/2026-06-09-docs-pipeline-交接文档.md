# 交接文档：docs-pipeline 目录重构

**日期**：2026-06-09  
**状态**：目录结构已创建，待迁移 docs-pipeline 模板  
**交接人**：上一个会话  
**接收人**：下一个代理

---

## 一、会话摘要

本会话完成了 docs-pipeline 项目的目录结构重构，从 14 个目录精炼为 10 个目录，解决了 design/ 和 designs/ 的命名冲突和哲学冲突。

---

## 二、关键决策

### 决策 1：采用 SDD 驱动 + 单一真相源

- **设计意图**和**实现现状**统一存放在 `design/` 目录
- 先写设计，再写代码，设计即文档
- 通过 PR Checklist 强制同步

### 决策 2：融合 AGE 和 DDD 两个模板

| 来源 | 贡献 |
|------|------|
| AGE 模板 | 吸引子哲学、context/、backlog/、plans/、lessons/、logs/ |
| DDD 模板 | prd/、standards/、features/（后改为 prd/） |

### 决策 3：最终目录结构（10 个）

```
docs/
├── context/           # 项目上下文、真相优先级
├── backlog/           # 工作队列、待定事项
├── prd/               # 需求规格、用户故事
├── design/            # 应用层设计 + 系统现状（SDD）
├── architecture/      # 技术基线、模块边界
├── standards/         # 开发规范、代码标准
├── plans/             # 执行计划、变更记录
│   └── completed/     # 已完成计划归档
├── lessons/           # 经验教训、复盘记录
├── logs/              # 开发日志、每日记录
├── issues/            # Bug 追踪、问题记录
└── index.md           # 文档路由中枢
```

---

## 三、已完成工作

### 3.1 目录结构创建

- [x] 创建所有 10 个目录
- [x] 创建 plans/completed/ 子目录
- [x] 创建所有 README.md 文件
- [x] 创建模板文件（TEMPLATE.md）
- [x] 创建 PRD-DESIGN-EXPERT.md

### 3.2 文档创建

- [x] docs/index.md - 文档路由中枢
- [x] docs/prd/2026-06-09-docs-pipeline-目录重构.md - PRD 文档
- [x] docs/2026-06-09-docs-pipeline-目录矩阵与流程图.md - 目录矩阵和流程图
- [x] docs/issues/2026-06-09-design-vs-designs-目录冲突.md - 问题诊断
- [x] docs/issues/2026-06-09-docs-pipeline-文档系统梳理.md - 系统梳理

### 3.3 清理工作

- [x] 删除旧文件（handover/、docs-pipeline-enhancement-proposal.md 等）
- [x] 重命名 features/ 为 prd/
- [x] 更新 index.md 中的引用

---

## 四、待办事项

### 4.1 高优先级

| 任务 | 描述 | 依赖 |
|------|------|------|
| 更新 docs-pipeline 模板 | 将新的目录结构同步到 assets/templates/ | 无 |
| 更新 SKILL.md | 修改工作流以支持新的目录结构 | 无 |
| 更新 CLAUDE.md 模板 | 更新文档所有权表格，移除 designs/ | 无 |
| 更新 AGENTS.md 模板 | 更新文档所有权表格，移除 designs/ | 无 |
| 更新 docs-index.md 模板 | 更新路由表，使用 prd/ 替代 features/ | 无 |

### 4.2 中优先级

| 任务 | 描述 | 依赖 |
|------|------|------|
| 创建迁移指南 | 指导已有项目从旧结构迁移到新结构 | 模板更新完成 |
| 更新测试脚本 | test-modes.sh 和 test-pipeline.sh | 模板更新完成 |
| 更新 USAGE.md | 更新使用场景和最佳实践 | 模板更新完成 |
| 更新 ADVANCED.md | 更新高级功能说明 | 模板更新完成 |

### 4.3 低优先级

| 任务 | 描述 | 依赖 |
|------|------|------|
| 更新 CHANGELOG.md | 记录本次重构 | 模板更新完成 |
| 更新 EVOLUTION.md | 记录架构演进 | 模板更新完成 |
| 创建示例项目 | 使用新结构的示例项目 | 所有更新完成 |

---

## 五、相关文件引用

### 5.1 本次会话创建的文件

| 文件路径 | 描述 |
|----------|------|
| `docs/index.md` | 文档路由中枢 |
| `docs/prd/README.md` | prd/ 目录说明 |
| `docs/prd/PRD-DESIGN-EXPERT.md` | PRD Design Expert 角色定义 |
| `docs/prd/2026-06-09-docs-pipeline-目录重构.md` | PRD 文档 |
| `docs/design/README.md` | design/ 目录说明（SDD 驱动） |
| `docs/architecture/README.md` | architecture/ 目录说明 |
| `docs/standards/README.md` | standards/ 目录说明 |
| `docs/plans/README.md` | plans/ 目录说明 |
| `docs/lessons/README.md` | lessons/ 目录说明 |
| `docs/logs/README.md` | logs/ 目录说明 |
| `docs/issues/README.md` | issues/ 目录说明 |
| `docs/2026-06-09-docs-pipeline-目录矩阵与流程图.md` | 目录矩阵和流程图 |
| `docs/issues/2026-06-09-design-vs-designs-目录冲突.md` | 问题诊断 |
| `docs/issues/2026-06-09-docs-pipeline-文档系统梳理.md` | 系统梳理 |

### 5.2 需要更新的 docs-pipeline 模板文件

| 文件路径 | 更新内容 |
|----------|----------|
| `docs-pipeline/assets/templates/CLAUDE.md` | 移除 designs/，更新文档所有权 |
| `docs-pipeline/assets/templates/AGENTS.md` | 移除 designs/，更新文档所有权 |
| `docs-pipeline/assets/templates/docs-index.md` | 使用 prd/ 替代 features/，更新路由表 |
| `docs-pipeline/assets/templates/designs-README.md` | 删除或合并到 design-README.md |
| `docs-pipeline/assets/templates/design-README.md` | 更新为 SDD 驱动说明 |
| `docs-pipeline/SKILL.md` | 更新工作流以支持新目录结构 |

### 5.3 参考资料

| 路径/URL | 描述 |
|----------|------|
| https://github.com/entropy-cloud/attractor-guided-engineering-template | AGE 模板 |
| https://github.com/domain-driven-design/ddd-harness-microservices | DDD 模板 |
| `docs-pipeline/EVOLUTION.md` | 演进历史 |

---

## 六、设计哲学备忘

### 核心原则

1. **设计是吸引子**（AGE）：design/ 是稳定的基线，代码向设计收敛
2. **代码是真相**（DDD）：design/ 同时记录实现现状，通过 SDD 同步
3. **SDD 驱动**：先写设计，再写代码，设计即文档
4. **单一真相源**：所有设计相关文档都在 design/

### SDD 核心循环

```
设计意图（design/）
    │
    ▼ ① 先写设计
实现代码（src/）
    │
    ▼ ② 再写代码
测试验证（tests/）
    │
    ▼ ③ 验证通过
同步设计（design/）
    │
    ▼ ④ 更新为实现现状
闭包审计（lessons/）
```

---

## 七、注意事项

1. **不要重复造轮子**：docs-pipeline 模板中已有的内容，直接复用
2. **保持兼容性**：更新模板时，确保已有项目可以平滑迁移
3. **更新引用**：所有模板文件中的引用必须一致（prd/ 而不是 features/）
4. **测试验证**：更新后运行 test-modes.sh 和 test-pipeline.sh 验证

---

## 八、建议的技能

| 技能 | 用途 |
|------|------|
| `docs-pipeline` | 用于初始化或修复 docs 目录结构 |
| `vast-dev-dir-organizer` | 用于整理和优化目录结构 |
| `vast-skill-forge` | 用于更新 SKILL.md 模板 |
| `skill-manage` | 用于管理 skill 的全生命周期 |
| `neat-freak` | 用于同步文档和代码的一致性 |

---

## 九、交接检查清单

- [ ] 确认 docs 目录结构正确（10 个目录 + plans/completed/）
- [ ] 确认所有 README.md 文件内容完整
- [ ] 确认 index.md 引用正确（prd/ 而不是 features/）
- [ ] 确认 PRD 文档和模板文件已创建
- [ ] 确认问题诊断和梳理文档已创建
- [ ] 确认旧文件已清理
- [ ] 阅读待办事项，了解下一步工作
- [ ] 阅读相关文件引用，了解需要更新的模板文件

---

**交接完成时间**：2026-06-09  
**下次会话重点**：更新 docs-pipeline 模板文件，将新目录结构同步到 assets/templates/
