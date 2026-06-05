# Darwin-Skill 对 Docs-Pipeline 的改进帮助分析

> 创建时间: 2026-06-05
> 分析目标: 评估 darwin-skill (达尔文.skill 2.0) 对本项目 docs-pipeline 改进的真实价值与可执行路径

## 1. 一句话结论

**darwin-skill 是 SKILL.md 质量审计器 + 自动改进器,docs-pipeline 本身就是一个被审计对象。** 用 darwin 的 9 维度 rubric(SkillLens 论文)可以从用户视角给 docs-pipeline 评分,识别短板并提出改进建议。

## 2. Darwin-Skill 能力概览

来源: <https://github.com/alchaincyf/darwin-skill> (3.4k stars, **无 license ⚠️**)

| 能力 | 说明 |
|------|------|
| 9 维度 Rubric 评分 | 静态分析 + 实测验证,满分 100 |
| 棘轮机制 | 只保留改进,自动回滚退步 |
| 独立评分 | 子 agent 盲评,避免"自己改自己评"的偏差 |
| 人在回路 | 每个改进完后暂停,用户确认再继续 |
| 实测对比 | 跑 2-3 个测试 prompt,对比有/无 skill 的输出差异 |
| 结果卡片 | 生成可视化改进报告 |

### 9 维度 Rubric 权重

| # | 维度 | 权重 | 类型 |
|---|------|------|------|
| 1 | Frontmatter 质量 | 7 | 结构 |
| 2 | 工作流清晰度 | 12 | 结构 |
| 3 | 失败模式编码 | 12 | 结构 |
| 4 | 检查点设计 | 6 | 结构 |
| 5 | 可执行具体性 | 17 | 结构 |
| 6 | 资源整合度 | 4 | 结构 |
| 7 | 整体架构 | 12 | 效果 |
| 8 | 实测表现 | 23 | 效果 |
| 9 | 反例与黑名单 | 6 | Meta-skill |

**关键评分规则**: 改进后总分必须**严格高于**改进前才保留。

## 3. 怎么使用(2 步)

### 步骤 1: 安装到全局

**当前问题**: 本项目 `darwin-skill/` 已存在(116K, 在 `upgrade/docs-pipeline-enhanced` 分支),但**全局 `~/.claude/skills/` 和 `~/.agents/skills/` 都没有 darwin-skill**——这意味着其他项目用不了。

```bash
ln -sf "$(pwd)/darwin-skill" ~/.claude/skills/darwin-skill
ln -sf "$(pwd)/darwin-skill" ~/.agents/skills/darwin-skill
```

### 步骤 2: 触发 darwin 评估 docs-pipeline

在 Claude Code 里说:

> "用 darwin 评估 docs-pipeline 这个 skill,跑完整 9 维度评分 + 2 个测试 prompt"

darwin 会自动:
1. 静态分析 `docs-pipeline/SKILL.md` 9 维度
2. 跑 2-3 个典型用户 prompt,对比有/无 docs-pipeline 的输出差异
3. 生成结果卡片(总分 + 维度分 + 改进建议)
4. **人在回路**: 不自动改,等你确认才动手

## 4. Docs-Pipeline 现状粗判(预估非实测)

| 维度 | 预估 | 关键问题 |
|------|------|---------|
| dim1 Frontmatter | 🟢 高 | description 长但完整,触发词丰富 |
| dim2 工作流清晰度 | 🟡 中 | 步骤清晰但偏多,新手需读 30 秒 |
| dim3 失败模式 | 🔴 **低** | **没显式"如果 X 失败 → Y"分支** |
| dim4 检查点 | 🟡 中 | 有"打开/添加/运行"3 步,但无显式 🔴 标记 |
| dim5 可执行具体性 | 🟡 中 | 有"环境变量"和"模式选择",但有"灵活选择"等软化措辞 |
| dim6 资源整合度 | 🟢 高 | references/scripts/assets 完整 |
| dim7 整体架构 | 🟢 高 | 层次清晰,无花叔禁用词 |
| dim8 实测表现 | ⚪ 待测 | 需 darwin 跑测试 |
| dim9 反例黑名单 | 🔴 **低** | **没"不要做什么"清单** |

**预估总分**: 70-75/100
**主要短板**: dim3(失败模式) + dim9(反例黑名单)

## 5. 3 个真实风险

| 风险 | 详情 | 应对 |
|------|------|------|
| **license 缺失** | darwin-skill 仓库 `license: None`,集成前要补 MIT/Apache-2.0 | 联系作者加 license,或 fork 时补 |
| **darwin 对脚手架类 skill 不友好** | docs-pipeline 是"初始化器"(一次性输出 47 文件),不是"功能 skill",实测对比难设计(初始化没"baseline") | dim8 可能需要手动设计测试 prompt,跳过 baseline 对比 |
| **dim3 失败模式对 docs-pipeline 杀伤大** | 当前 SKILL.md 没显式写"目录冲突时怎么办"、"用户拒绝确认时怎么办"——darwin 会扣 ≥3 分 | 改进时优先补这块 |

## 6. 改进优先级建议

按 darwin 9 维度,对 docs-pipeline 改进的优先级:

1. **🔴 P0 - dim3 失败模式** (预计 +8~12 分)
   - 显式写"如果 X 失败 → Y"分支
   - 至少 3 个失败模式: 目录已存在、模式选择错误、模板拷贝失败
   - 示例:
     ```markdown
     ### 失败处理
     - **目录已存在**: docs-pipeline 默认幂等,跳过已存在文件;如需强制覆盖,使用 `--force` 参数
     - **模式选择错误**: 检测到模式不匹配时,提示用户重新选择;不会自动切换
     - **模板拷贝失败**: 列出失败文件清单,保留部分初始化结果,提示用户重试
     ```

2. **🔴 P0 - dim9 反例黑名单** (预计 +4~6 分)
   - 加"## ⚠️ 不要做什么"章节
   - 内容建议:
     ```markdown
     ## ⚠️ 不要做什么
     - ❌ 不要修改 docs/ 下的现有文件——docs-pipeline 只初始化,不更新
     - ❌ 不要在 standard 模式下用 minimal 模板——会丢失目录
     - ❌ 不要跳过用户确认——初始化是不可逆的(删除文件需要手动)
     - ❌ 不要把 `assets/templates/` 当成可执行脚本——是模板,不是工具
     ```

3. **🟡 P1 - dim4 检查点显式化** (预计 +2~3 分)
   - 关键步骤前加 `🔴 CHECKPOINT` 标记
   - 例: `🔴 CHECKPOINT: 用户确认初始化模式(minimal/standard)后再继续`

4. **🟡 P1 - dim5 软化措辞清理** (预计 +2~3 分)
   - 删除"灵活选择"、"根据情况"、"建议考虑"等措辞
   - 改为具体决策表

5. **🟢 P2 - dim1 description 精简** (预计 +1~2 分)
   - 当前 description 长 ~150 字符,可考虑分拆触发词与功能描述

## 7. 建议执行路径

```
[现在]    装全局 darwin-skill
   ↓
[Day 1]   跑 darwin 评分(确认预估 70-75 是否准确)
   ↓
[Day 2]   根据真实评分针对改进 dim3 + dim9 (P0)
   ↓
[Day 3]   跑 darwin 二次评分,确认总分上升
   ↓
[Day 4]   棘轮锁定,提交 SKILL.md 改进
```

## 8. 与现有 docs-pipeline 改进提案的关系

`docs/docs-pipeline-enhancement-proposal.md` (2026-06-05) 关注的是**目录结构扩展**(增加 standards/ + designs/ 两层 + 同步机制)。

**本文档关注的是 SKILL.md 本身质量审计**(9 维度评分 + 失败模式/反例清单)。

两者**不冲突,正交**:
- 那个提案 = 扩展 docs-pipeline **输出什么**
- 这个分析 = 改进 docs-pipeline **自己本身**

建议:先跑 darwin 评分摸清 SKILL.md 真实短板 → 再决定是否合并到 enhancement proposal 的执行计划里。

## 9. 后续行动项(Backlog)

- [ ] 全局安装 darwin-skill(`ln -sf` 软链)
- [ ] 跑 darwin 评估 docs-pipeline,生成第一次结果卡片
- [ ] 基于结果卡片改进 SKILL.md(dim3 + dim9 优先)
- [ ] 跑 darwin 二次评分验证
- [ ] 决定是否合并到 enhancement proposal 的 Phase 1
- [ ] 联系 darwin-skill 作者补 license(MIT 或 Apache-2.0)
