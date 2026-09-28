---
name: vast-test-audit
description: "在编写、修改、审查或清扫测试时调用。新测试的编写闸门，加上对低价值、与实现耦合或冗余测试以及它们所要求的“测试专用产线缝”的审计工作流。三种模式：authoring（编写）、audit（审计）、campaign（子系统清扫）。"
metadata:
  author: ported from openclaw/openclaw .agents/skills/test-audit
  source: https://github.com/openclaw/openclaw/blob/main/.agents/skills/test-audit/SKILL.md
  version: "1.0.0"
---

# vast-test-audit

三种模式，一个价值标尺。

- **Authoring（编写闸门）**：写新测试或改测试时，必须先答出四个问题（保护什么、能捕获什么失败、为什么现有覆盖抓不住、是否引入了产线缝）。
- **Audit（审计扫描）**：找出“复述源码”“重复更强证明”“与实现耦合”“只为测试留的生产缝”之类的测试；按 owner boundary 分批清理；广审计作为独立连贯的 follow-up PR，目标是信心不是删除数量。
- **Campaign（子系统清扫）**：一次性修剪某个插件或核心区域的整套测试面；启动前先读 [CAMPAIGN.md](CAMPAIGN.md)。

---

## Authoring gate

加任何测试前，先答四个问题；缺一个就不要加：

1. 它保护什么可观察行为、不变量或独立契约？
2. 什么可信的回归会让它失败？
3. 现有覆盖为什么抓不住这个失败？每个契约在最强边界有一个主测试 owner；另一层只有存在独立风险时才有意义（如 owner 触及不到的 transport/lifecycle 失败）。优先扩展表驱动用例或共享 fixture，而非复制新测试；同一变更内合并重复 setup。
4. 是否需要产线缝（export、flag、wrapper、注入钩子），而生产调用方根本不需要？如果需要，把测试搬到真实边界。

然后对照 [junk patterns](#junk-patterns) 全量检查；命中任何一个 = 闸门 fail，除非 [retention bar](#retention-bar) 明确点出它独立守护的契约。在“保持行为的重构”下会破的测试，是在断言实现而非行为；合入前搬到 owner 边界重写。

Bug 回归测试必须：
- 在修复前代码上以**预期原因**失败
- 在 owner boundary 修复后通过

一个从未可验证失败的回归测试，证明的是 mock 而不是 fix。一个 owner boundary 上的回归测试就够覆盖这个 bug，不要在它穿越的每一层重放。

---

## Junk patterns

authoring 和 audit 共用清单：新测试命中即拒绝；已有测试命中即审计目标。

- 只跑覆盖率但不写断言的探测
- 自我比较、恒等拷贝
- 复制的 fixture、清单、manifest 或导出列表
- 源码、import 或字符串的精确 grep
- 在真实边界重复断言的私有谓词或调用形态测试
- 同一契约的重复调用
- 在 provider 内部重放共享 helper
- 唯一目的就是保留“测试专用 export、全局变量、wrapper”
- 唯一调用方是测试的死产线代码
- 由被测 helper/renderer 自己生成的期望值
- 实现被断言行为的 mock，或一个相同 mock 充当不同 API 的替身
- fixture 自己提供 owner 应该产生的 receipt、admission、callback 顺序；或在路径根本不写入的存储上断言持久化
- 重述已声明 flag 而非演练 flag 承诺的传递/确认的能力测试
- 出于无关原因通过的负控制（不同 guard 的拒绝、或生产路径根本不触达的拒绝）
- 名字或 fixture 承诺超出实际演练（如“retires the window”测试却断言窗口未被清空）

---

## Value bar

测试用维护成本换取：守护行为、可信回归、或独立有意义的契约。审计里，一个“行为保持的源码重组”就会被迫改的测试是可疑的，但不自动可删——authoring 闸门同样会拒绝新写的。

判定前读完整测试和产线 owner、入口、调用方、被调方、兄弟实现、覆盖重叠的测试、CI 路由和相关历史。先读 root 和范围内的 `AGENTS.md`。当测试声称依赖某库行为时，直接看依赖源码或类型。

---

## Discovery

保持只读，先报证据再编辑。广范围下，有条件就跑并行的 discovery lane：

- 核心与 packages（`src/`、`packages/`）
- 插件（`extensions/`）
- UI、apps、scripts、tooling
- 跨切面 pattern 扫描

非 campaign 模式下，宁可少而精，不要大而猜。重点找 [junk patterns](#junk-patterns)。

---

## Retention bar

满足下列之一就保留：独立守护公开 API、插件 SDK、协议、config、migration、存储、安全、平台、默认、prompt-byte、跨语言生成产物、package、release、架构契约。

也保留：

- 调用顺序——当顺序是可观察行为
- 有可信失败模式的回归测试
- 源码巡检——当它是最便宜的独立守门：契约（用户可见 key、字节或路径）变化就失败，仅改标识符的重构能活下来
- 在 baseline 上失败的保留测试：当可能的产线 bug 处理，复现并修复 owner，不要直接删

慢或静态分析不是删除理由。看起来像实现的仍可能是独立契约，先证明不是再删。

---

## Candidate evidence

每个候选在编辑前都要记录全部字段。缺一个就还没准备好被删：

- 精确测试名和位置
- 它能实际检测到什么失败
- 被覆盖产线/支持缝的非测试调用方
- 更强的剩余 owner-boundary 证明，或为什么不需要证明
- 相关历史，以及这个测试或缝为什么存在
- 删除产线/测试支持能解锁什么
- 风险和聚焦的验证命令

---

## Edit shape

每次选一个连贯的 owner-boundary 批次。删掉过时的“测试专用 export、全局变量、wrapper、死产线路径”，不要用别名保留。保留的回归搬到它的规范 owner。重复的 package/依赖断言合并成一条通用契约。

优先让产线 LOC 净减少。不要加“复述同一实现”的替代测试，不要把不确定的候选包装成 cleanup 来刷删除数。

---

## Validation

不要在 Vitest/测试 runner 还在跑的时候改源码或测试。重型证明走项目自身的“重型隔离验证”规则（沙箱或专用 runner）。

1. 用项目自身的测试运行脚本跑最小 owner 和兄弟测试，例如 `node scripts/run-vitest.mjs <path-or-filter>`（按实际工具替换）。
2. 删掉的源码 grep/plan 断言，跑拥有真实契约的可执行脚本或 dry-run。
3. 跑聚焦的格式化检查，再 `git diff --check`。
4. 用项目自身的变更分类检查走 dry-run，例如 `node scripts/check-changed.mjs --dry-run -- <changed-paths>`，再按仓库策略跑实际分类门。
5. 检查 `git diff --numstat`，把产线/tooling 和测试/测试支持分开报。
6. 审计最终编辑后，跑项目强制要求的自动代码评审。

---

## Landing and continuation

只在被授权时 commit、push、开 PR 或合并。用项目自身的 PR 维护流程（如仓库 `scripts/pr`）。一次一个连贯 PR；合入后从当前 `main` 刷新，并对下一批高置信候选再跑一遍只读 discovery。

---

## Handoff

汇报：

- 根因和已删除的低价值类别
- 产线 owner 的简化
- 保留的误报以及它们为什么仍值钱
- 实际跑过的聚焦和完整证明
- 产线 vs 测试 LOC
- PR 和合并状态
- 命名的 follow-up