# Adding New Templates

适用场景：发现某份通用文档（如 `MISTAKES.md`、`KNOWLEDGE.md`、某种代码规范）值得在每个新项目都自动落地，需要新增到 skill 的模板清单。

## 5 步流程

**Step 1：放模板进 assets/templates/**

```bash
cp <源文件路径> .claude/skills/docs-pipeline/assets/templates/<目标文件名>
```

模板文件名建议与目标落地路径同名，避免映射混淆。

**Step 2：改 SKILL.md（3 处）**

1. **frontmatter 的 `description`**：在括号里加上新模板名（影响 skill 触发匹配）
2. **「核心结构」目录树**：加入新文件位置
3. **「写入项目根 AI 代理模板」表格**（如果是根级模板）或「写入 docs/ 模板」表格（如果是 docs/ 内）：增加一行映射
4. **「不要做」清单**：在"不覆盖已有的 X / Y / Z"那一条加上新文件名

**Step 3：改 README.md（2 处）**

1. **「行为契约」表格**：加一行 `项目根 X 不存在 → 写入模板`
2. **「目录结构」**：在 `assets/templates/` 列表中加入新文件 + 一句话用途

**Step 4：升版本号**

SKILL.md 的 `metadata.version` 升级（语义版本：加新模板属于 minor，如 0.3.0 → 0.4.0）。

**Step 5：Dogfood 验证**

```bash
TARGET=/tmp/docs-pipeline-dogfood-$$
SKILL=<本 skill 绝对路径>

# Round 1: 全新初始化
mkdir -p $TARGET
mkdir -p $TARGET/docs/{research,prd,plans,plans/completed,handover,lessons,logs}
# 对每个模板: cp $SKILL/assets/templates/X $TARGET/X

# Round 2: 幂等性测试 (重跑应该全部跳过)

# 字节级 diff 验证
diff -q <源文件> $TARGET/<目标文件>

rm -rf $TARGET
```

通过标准：
- ✅ 全新模式：所有文件全部写入
- ✅ 二次模式：所有文件跳过（幂等）
- ✅ 字节级 diff：模板与源文件完全一致

## 反例：什么不该加

- ❌ 项目特有的业务文档（如某个公司的 PRD 模板、某个产品的接口文档）
- ❌ 与现有模板职责重叠的文档（如又一个"代码规范"）
- ❌ 频繁变化的内容（每月更新一次的清单）
- ❌ 体积巨大（>50KB）的文档（影响 skill 加载性能）

## 模板的两种类型

| 类型 | 例子 | 实现 |
|------|------|------|
| **静态模板** | AGENTS.md / karpathy-guidelines.md | `cp` 即可 |
| **探索型模板** | ARCHITECTURE.md | 需要调用 Explore 子代理读项目代码后生成 |

探索型模板的额外要求：
- 在 SKILL.md 里明确给 Claude 的"探索指令"（章节结构、字数预算、工具预算）
- **必须有降级骨架** `<name>.template`：探索失败时落地，不让流程卡住
- `allowed-tools` 必须包含 `Agent`

## 加模板前自问

1. 这份文档在 **3+ 个项目** 都需要吗？
2. 它在未来 6 个月内 **不会频繁修改** 吗？
3. 它和现有模板 **职责不重叠** 吗？

三个 yes 才加。否则放在原项目里就够。
