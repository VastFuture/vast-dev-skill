# Docs-Pipeline 融合改进方案

> 基于 ddd-harness-microservices 项目的启发
> 创建时间: 2026-06-05

## 1. 改进目标

将 ddd-harness-microservices 的**文档驱动开发**和**文档同步机制**融入 docs-pipeline，形成更完整的文档管理体系。

### 核心改进点

1. **增加规范层**（standards/）
2. **增加现状层**（designs/）
3. **增强同步机制**（强制文档同步检查）
4. **集成 PR 流程**（PR Checklist）

---

## 2. 目录结构改进

### 2.1 现有结构

```text
docs/
├── context/          # AI 上下文
├── backlog/          # 工作队列
├── prd/              # 需求文档
├── design/           # 应用层设计
├── exec-plans/       # 执行计划
├── ideas/            # 灵感池
├── research/         # 调研文档
├── handover/         # 项目交接
├── issues/           # Bug 追踪
├── lessons/          # 经验教训
└── agent-guides/     # AI 行为指南
```

### 2.2 改进后结构

```text
docs/
├── context/          # AI 上下文（现有）
├── backlog/          # 工作队列（现有）
├── prd/              # 需求文档（现有）
├── design/           # 应用层设计（现有）
├── exec-plans/       # 执行计划（现有）
├── ideas/            # 灵感池（现有）
├── research/         # 调研文档（现有）
├── handover/         # 项目交接（现有）
├── issues/           # Bug 追踪（现有）
├── lessons/          # 经验教训（现有）
├── agent-guides/     # AI 行为指南（现有）
├── standards/        # 【新增】开发规范
│   ├── README.md     # 规范目录说明
│   ├── layers.md     # 分层架构规范
│   ├── api.md        # API 设计规范
│   ├── db.md         # 数据库规范
│   ├── security.md   # 安全规范
│   └── naming.md     # 命名规范
└── designs/          # 【新增】系统现状
    ├── README.md     # 现状目录说明
    ├── api.yaml      # API 现状（OpenAPI/Swagger）
    ├── db.md         # 数据库现状（表结构）
    └── others/       # 其他设计现状
        ├── businessrule.md  # 业务规则现状
        └── data-dict.md     # 数据字典现状
```

---

## 3. 文档同步机制

### 3.1 同步检查规则

在每轮任务完成后，强制检查以下文档是否需要更新：

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

### 3.2 同步检查流程

在 SKILL.md 中增加同步检查步骤：

```markdown
### 10. 文档同步检查

**Step 10.1：检测代码变更**

分析代码变更涉及的层：
- adapter 层变更 → 可能影响 API 设计
- application 层变更 → 可能影响用例流程
- domain 层变更 → 可能影响业务规则
- infrastructure 层变更 → 可能影响数据库或外部 API

**Step 10.2：提示同步更新**

根据变更类型提示需要更新的文档：

```
📋 文档同步检查

🔍 检测到以下变更：
  - 新增 API: POST /users
  - 修改数据表: user 表增加字段

📝 建议更新以下文档：
  - docs/designs/api.yaml（API 现状）
  - docs/designs/db.md（数据库现状）

⏭️ 是否现在更新？
  1. 是，立即更新
  2. 否，稍后手动更新
  3. 跳过（本次变更不涉及）
```

**Step 10.3：生成同步报告**

在执行报告中显示同步状态：

```
📋 docs-pipeline 执行报告

...

🔄 文档同步状态：
  - docs/designs/api.yaml: 需要更新（新增 2 个 API）
  - docs/designs/db.md: 需要更新（修改 1 个表）
  - docs/standards/layers.md: 无需更新

⏭️ 下一步：
  1. 更新 docs/designs/api.yaml
  2. 更新 docs/designs/db.md
```

---

## 4. PR Checklist 集成

### 4.1 AGENTS.md 模板增强

在 AGENTS.md 模板中增加 PR Checklist：

```markdown
## PR / Change Checklist

### 文档同步（强制）

- [ ] `docs/designs/` 同步检查（已更新 / 不涉及）
  - 新增/修改 API → 更新 `docs/designs/api.yaml`
  - 新增/修改数据表 → 更新 `docs/designs/db.md`
  - 新增/修改业务规则 → 更新 `docs/designs/others/businessrule.md`
  - 新增/修改数据字典 → 更新 `docs/designs/others/data-dict.md`

### 代码质量

- [ ] 分层检查：adapter 不含业务逻辑；domain 不依赖 infrastructure；事务边界在 application
- [ ] 错误处理：业务校验使用 `BusinessException`，避免裸 `RuntimeException`
- [ ] DTO/映射：新增字段同步更新 Assembler/Converter，并保证向后兼容
- [ ] 安全：不记录 token/敏感信息；对外接口做鉴权/越权检查
- [ ] 验证：本地至少运行相关模块的测试（`mvn test` 或按模块 `-pl`）

### 测试覆盖

- [ ] 新增 API 有集成测试
- [ ] 至少覆盖 1 个 Happy Path + 关键失败分支
- [ ] DB 相关用例可重复执行
```

### 4.2 PR Checklist 模板文件

新增模板文件：`assets/templates/agent-guides/pr-checklist.md`

```markdown
# PR / Change Checklist

## 文档同步（强制）

- [ ] `docs/designs/` 同步检查（已更新 / 不涉及）

## 代码质量

- [ ] 分层检查通过
- [ ] 错误处理规范
- [ ] DTO/映射同步
- [ ] 安全检查通过
- [ ] 测试验证通过

## 测试覆盖

- [ ] 新增 API 有集成测试
- [ ] 覆盖 Happy Path + 关键失败分支
- [ ] DB 用例可重复执行
```

---

## 5. 模板文件新增

### 5.1 standards/ 目录模板

新增以下模板文件：

| 模板 | 目标路径 | 用途 |
|------|---------|------|
| `assets/templates/standards-README.md` | `$docs_root/standards/README.md` | 规范目录说明 |
| `assets/templates/standards-layers.md` | `$docs_root/standards/layers.md` | 分层架构规范 |
| `assets/templates/standards-api.md` | `$docs_root/standards/api.md` | API 设计规范 |
| `assets/templates/standards-db.md` | `$docs_root/standards/db.md` | 数据库规范 |
| `assets/templates/standards-security.md` | `$docs_root/standards/security.md` | 安全规范 |
| `assets/templates/standards-naming.md` | `$docs_root/standards/naming.md` | 命名规范 |

### 5.2 designs/ 目录模板

新增以下模板文件：

| 模板 | 目标路径 | 用途 |
|------|---------|------|
| `assets/templates/designs-README.md` | `$docs_root/designs/README.md` | 现状目录说明 |
| `assets/templates/designs-api.yaml` | `$docs_root/designs/api.yaml` | API 现状 |
| `assets/templates/designs-db.md` | `$docs_root/designs/db.md` | 数据库现状 |
| `assets/templates/designs-others-README.md` | `$docs_root/designs/others/README.md` | 其他现状说明 |
| `assets/templates/designs-others-businessrule.md` | `$docs_root/designs/others/businessrule.md` | 业务规则现状 |
| `assets/templates/designs-others-data-dict.md` | `$docs_root/designs/others/data-dict.md` | 数据字典现状 |

---

## 6. SKILL.md 修改

### 6.1 增加目录创建

在 Step 2 中增加 standards/ 和 designs/ 目录：

```bash
# Standard 模式（12 个核心目录，默认）
elif [ "$MODE" = "standard" ]; then
  mkdir -p "$docs_root/context" "$docs_root/backlog" "$docs_root/prd" "$docs_root/design" "$docs_root/exec-plans/active" "$docs_root/exec-plans/completed" "$docs_root/research" "$docs_root/issues" "$docs_root/handover" "$docs_root/ideas" "$docs_root/lessons" "$docs_root/agent-guides" "$docs_root/standards" "$docs_root/designs" "$docs_root/designs/others"
fi
```

### 6.2 增加模板映射

在 Step 3 中增加模板映射：

```markdown
| 模板 | 目标路径 |
|------|---------|
| ...（现有模板）|
| `assets/templates/standards-README.md` | `$docs_root/standards/README.md` |
| `assets/templates/standards-layers.md` | `$docs_root/standards/layers.md` |
| `assets/templates/standards-api.md` | `$docs_root/standards/api.md` |
| `assets/templates/standards-db.md` | `$docs_root/standards/db.md` |
| `assets/templates/standards-security.md` | `$docs_root/standards/security.md` |
| `assets/templates/standards-naming.md` | `$docs_root/standards/naming.md` |
| `assets/templates/designs-README.md` | `$docs_root/designs/README.md` |
| `assets/templates/designs-api.yaml` | `$docs_root/designs/api.yaml` |
| `assets/templates/designs-db.md` | `$docs_root/designs/db.md` |
| `assets/templates/designs-others-README.md` | `$docs_root/designs/others/README.md` |
| `assets/templates/designs-others-businessrule.md` | `$docs_root/designs/others/businessrule.md` |
| `assets/templates/designs-others-data-dict.md` | `$docs_root/designs/others/data-dict.md` |
```

### 6.3 增加同步检查步骤

在 Step 9 之后增加 Step 10：

```markdown
### 10. 文档同步检查

**Step 10.1：检测代码变更**

使用 Git 或文件系统检测最近的代码变更：

```bash
# 检测最近的代码变更
git diff --name-only HEAD~1 2>/dev/null || echo "NO_GIT"
```

**Step 10.2：分析变更类型**

根据变更文件路径判断变更类型：

```bash
# 分析变更类型
if echo "$CHANGED_FILES" | grep -q "Controller"; then
  echo "API 变更"
fi
if echo "$CHANGED_FILES" | grep -q "Mapper\|PO\|entity"; then
  echo "数据库变更"
fi
if echo "$CHANGED_FILES" | grep -q "BusinessRule\|Rule"; then
  echo "业务规则变更"
fi
```

**Step 10.3：提示同步更新**

根据变更类型提示需要更新的文档。

**Step 10.4：生成同步报告**

在执行报告中显示同步状态。
```

---

## 7. 目录对照表更新

更新目录对照表，增加 standards/ 和 designs/：

| 模式 | context | backlog | prd | exec-plans | lessons | research | design | issues | handover | ideas | agent-guides | standards | designs |
|------|---------|---------|-----|------------|---------|----------|--------|--------|----------|-------|--------------|-----------|---------|
| minimal | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| standard | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 8. 执行计划

### Phase 1：模板文件创建

1. 创建 standards/ 目录模板
2. 创建 designs/ 目录模板
3. 创建 PR Checklist 模板

### Phase 2：SKILL.md 修改

1. 增加目录创建逻辑
2. 增加模板映射
3. 增加同步检查步骤

### Phase 3：AGENTS.md 模板增强

1. 增加 PR Checklist 段落
2. 增加文档同步规则

### Phase 4：测试验证

1. 测试标准模式初始化
2. 测试最小化模式初始化
3. 测试同步检查功能
4. 验证 PR Checklist

---

## 9. 预期效果

### 9.1 文档完整性

- ✅ 规范层（standards/）：开发规范，相对稳定
- ✅ 现状层（designs/）：系统现状，高频更新
- ✅ 流程层（现有目录）：文档管理流程

### 9.2 同步机制

- ✅ 强制文档同步检查
- ✅ PR Checklist 集成
- ✅ 同步状态报告

### 9.3 开发体验

- ✅ 文档驱动开发
- ✅ 减少沟通成本
- ✅ 提高变更质量

---

## 10. 总结

通过融合 ddd-harness-microservices 的文档同步机制，docs-pipeline 将形成：

1. **三层文档体系**：规范层 + 现状层 + 流程层
2. **强制同步机制**：每次变更后强制检查文档同步
3. **PR 流程集成**：将文档同步纳入 PR Checklist
4. **质量保障**：文档与代码强关联，减少沟通成本

这样既保持了 docs-pipeline 的通用性，又吸收了 ddd-harness-microservices 的文档驱动开发优势。
