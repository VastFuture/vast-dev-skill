# docs-pipeline 更新日志

## [4.4.0] - 2026-06-05

### 新增

#### 1. 文档同步机制

基于 [ddd-harness-microservices](https://github.com/domain-driven-design/ddd-harness-microservices) 项目的启发，增加了文档同步机制：

- **新增 `docs/standards/` 目录**：存放开发规范（分层、API、DB、安全、命名）
- **新增 `docs/designs/` 目录**：存放系统设计现状（API、DB、业务规则、数据字典）
- **新增文档同步检查步骤**（Step 10）：检测代码变更并提示需要更新的文档
- **新增 PR Checklist**：在 AGENTS.md 中增加文档同步检查项

#### 2. 新增模板文件

**standards/ 目录模板**（6 个文件）：
- `standards-README.md` - 规范目录说明
- `standards-layers.md` - 分层架构规范
- `standards-api.md` - API 设计规范
- `standards-db.md` - 数据库规范
- `standards-security.md` - 安全规范
- `standards-naming.md` - 命名规范

**designs/ 目录模板**（6 个文件）：
- `designs-README.md` - 现状目录说明
- `designs-api.yaml` - API 现状（OpenAPI/Swagger）
- `designs-db.md` - 数据库现状
- `designs-others-README.md` - 其他现状说明
- `designs-others-businessrule.md` - 业务规则现状
- `designs-others-data-dict.md` - 数据字典现状

### 修改

#### 1. SKILL.md

- 更新目录创建逻辑：Standard 模式增加 `standards/` 和 `designs/` 目录
- 更新目录对照表：增加 `standards` 和 `designs` 列
- 增加模板映射：12 个新模板文件
- 增加 Step 10：文档同步检查步骤
- 更新执行报告模板：增加文档同步状态显示

#### 2. AGENTS.md 模板

- 增加 PR / Change Checklist 段落
- 增加文档所有权表格：新增 `standards/` 和 `designs/` 目录

#### 3. docs-index.md 模板

- 增加目录职责表格：新增 `standards/` 和 `designs/` 目录
- 增加核心原则：说明文档同步规则

#### 4. README.md

- 增加参考项目链接：ddd-harness-microservices
- 增加核心目录表格：新增 `standards/` 和 `designs/` 目录

#### 5. USAGE.md

- 增加场景 6：代码变更后文档同步
- 更新文档决策树：增加文档同步分支
- 增加关键区别：`standards/` vs `designs/`、`design/` vs `designs/`

---

## 核心改进点

### 1. 文档同步机制

每次代码变更后，强制检查以下文档是否需要更新：

| 变更类型 | 需要更新的文档 |
|----------|---------------|
| 新增/修改 API | `docs/designs/api.yaml` |
| 新增/修改数据表 | `docs/designs/db.md` |
| 新增/修改业务规则 | `docs/designs/others/businessrule.md` |
| 新增/修改数据字典 | `docs/designs/others/data-dict.md` |
| 修改分层架构 | `docs/standards/layers.md` |
| 修改 API 规范 | `docs/standards/api.md` |
| 修改数据库规范 | `docs/standards/db.md` |
| 修改安全规范 | `docs/standards/security.md` |

### 2. PR Checklist 集成

在 AGENTS.md 中增加 PR Checklist，包含：
- 文档同步检查（强制）
- 代码质量检查
- 测试覆盖检查

### 3. 三层文档体系

- **规范层**（standards/）：开发规范，相对稳定
- **现状层**（designs/）：系统现状，高频更新
- **流程层**（现有目录）：文档管理流程

---

## 预期效果

- ✅ **文档完整性**：规范层 + 现状层 + 流程层
- ✅ **同步机制**：强制文档同步检查
- ✅ **开发体验**：文档驱动开发，减少沟通成本
- ✅ **质量保障**：PR Checklist 确保变更质量

---

## 参考资料

- [ddd-harness-microservices 项目](https://github.com/domain-driven-design/ddd-harness-microservices)
- [学习成果文档](../docs/ddd-harness-microservices-study.md)
- [改进方案文档](../docs/docs-pipeline-enhancement-proposal.md)
