# docs-pipeline 使用指南

初始化完成后，常见的使用场景、陷阱和最佳实践。

---

## 使用场景

### 场景 1：添加新功能（标准四步）

> 灵感来源：[neat-freak 四处都补原则](https://github.com/VastFuture/khazix-skills/tree/main/neat-freak)

**标准四步（新增能力时四处都补）**：

1. **docs/prd/**：创建 `feature-name.md`（使用 `prd/TEMPLATE.md`）
   - 需求：要解决什么问题
   - 验收标准：如何验证完成
   - 技术方案：如何实现

2. **docs/design/**：更新架构文档
   - 数据流：数据如何流转
   - 设计取舍：为什么这样设计
   - 模块边界：影响哪些模块

3. **docs/exec-plans/active/**：创建执行计划（如触发计划触发器）
   - 触发条件：> 5 文件或 > 200 行
   - 分阶段：将大特性拆分为多个阶段
   - 风险与依赖：记录已知风险

4. **docs/handover/**：完成后更新已完成清单
   - 已完成功能：新增了什么
   - 已知问题：还有什么问题
   - 注意事项：运维要注意什么

**实施并验证**：
- 运行 `docs/context/project-context.md` 中的验证命令
- 在 `docs/lessons/` 记录教训（如有）

**⚠️ 防膨胀检查**：
如果需要更新 CLAUDE.md/AGENTS.md：
- 判断标准：下次 AI 写代码时如果没看到这条，会不会犯错？
- ✅ 该进：硬边界规则、禁止事项、踩坑警示
- ❌ 不该进：历史叙事（"X 时刻起 Y 上线"）、详细机制
- 红灯线：净涨幅 ≤ 30 行

### 场景 2：修复 Bug

1. 在 `docs/issues/` 创建 `bug-name.md`（使用 `issues/TEMPLATE.md`）
2. 记录问题描述、复现步骤、根因分析
3. 实施修复并验证
4. 更新 issue 状态为"已解决"

### 场景 3：AI 不知道做什么

1. 检查 `docs/backlog/README.md`
2. 确保至少有一个 `status=ready`、`AI 自主级别=implement` 的任务
3. AI 会自动选择优先级最高的任务
4. 如果所有任务都是 `blocked`，在阻塞项中说明原因

### 场景 4：项目交接

1. 在 `docs/handover/` 创建 `handover-YYYY-MM-DD.md`（使用 `handover/TEMPLATE.md`）
2. 填写项目概述、技术架构、关键决策、待办事项、已知问题
3. 提供给接手人阅读

---

## 场景 5：会话结束后同步文档

**重要**：开发过程中会产生大量文档修改，但很容易漏掉关键更新或让 CLAUDE.md 膨胀。

**建议流程**：
1. 完成一个开发阶段（新功能、重构、修复）
2. 运行 `/neat-freak`（需要安装 [vast-khazix-neat-freak](../vast-khazix-neat-freak)）
3. neat-freak 会自动：
   - 审查 3 层知识：agent memory + CLAUDE.md + docs/
   - 同步本次会话的文档变更
   - 检查并防止 CLAUDE.md 膨胀（软上限 ~300 行）
   - 清理过期内容和重复记录

**触发时机**：
- 阶段性收尾（"这个阶段做完了"）
- 准备交接（"新人能直接上手"）
- 文档不同步（"整理一下文档"）

详见 [neat-freak SKILL.md](../vast-khazix-neat-freak/SKILL.md) 了解完整工作流。

---

## Gotchas（常见陷阱）

- **ARCHITECTURE.md 生成降级策略**：Explore 失败后，先尝试基于项目配置文件（package.json/setup.py/go.mod/Cargo.toml）生成基本结构，再尝试通用骨架，最后才完全跳过
- **项目根 CLAUDE.md 已有大量自定义内容**：只追加"## 文档"段落到末尾，绝不修改或删除已有内容。用 `grep -q "^## 文档"` 检测，存在就跳过
- **重复调用后误报"已建"**：幂等检测必须用 `Read` 确认文件实际存在，不能靠 `mkdir -p` 的返回值推断
- **Pensieve 不是必需的**：`.pensieve/` 不存在时完全跳过 Step 7，不询问、不提示。只有当 `ENABLE_PENSIEVE=true` 或 `.pensieve/` 已存在时才激活
- **模板里的 TODO 占位被自动填充**：`<!-- TODO(docs-pipeline): ... -->` 是留给用户的，不要替换
- **模式 B 路径引用错误**：独立文档仓库模式下，项目根 CLAUDE.md/AGENTS.md 中的文档引用必须是正确的相对路径。用 `realpath --relative-to=project_root docs_root` 计算
- **docs/ 目录既是独立 git 仓库又是项目子目录**：检测优先级 `DOCS_ROOT` > `docs/.git` 存在 > 默认 inline
- **用户修改路径后路径不存在**：用户输入的路径不存在时，询问是否创建，不自动创建
- **context/ 目录的 4 个文件是整体**：project-context.md、ai-autonomy-policy.md、codebase-map.md、source-of-truth-and-precedence.md 必须一起存在，才能保证 AI 上下文完整

---

## 不要做

- ❌ 不要在模板里塞业务示例（保持骨架空白）
- ❌ 不要自动填充索引（让用户用着用着自己填）
- ❌ 不要做 `--reset` / `--uninstall`（用户手动决定）
- ❌ 不要假设项目用 Python/Node/Rust
- ❌ 不要修改项目根 CLAUDE.md 已有内容（只追加"## 文档"段落，不改其他）
- ❌ 不要覆盖已有的 CLAUDE.md / AGENTS.md / MBTI_DEV_TRAPS.md / karpathy-guidelines.md / .mcp.json / ARCHITECTURE.md（用户可能已有定制版本）
- ❌ 不要让 Explore 子代理偏离 5 章节固定结构（保持跨项目一致）
- ❌ 模式 B 不要往项目根写 docs/ 目录（文档完全在独立仓库）
- ❌ 模式 B 不要硬编码文档仓库路径（用 `DOCS_ROOT` 环境变量或自动检测）
- ❌ 不要跳过交互询问（除非用户明确要求）
- ❌ 不要强制用户接受自动检测结果（始终提供修改选项）
