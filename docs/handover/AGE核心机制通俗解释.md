# AGE 核心机制通俗解释

## AGE 是什么？

**AGE = Attractor-Guided Engineering（引力导向工程）**

解决的问题：AI 辅助开发中"迭代快但方向容易跑偏"的问题。

它的核心思想：给项目建一个"引力中心"，让 AI 每次工作时都回归稳定结构，而不是跟着 chat 跑偏。

---

## AGE 是怎么工作的？

### 入口拦截机制

`AGENTS.md` 里有明确要求，AI 每次启动时自动读取：

```
Before writing non-trivial code, agents must first understand:
- docs/context/project-context.md
- docs/context/ai-autonomy-policy.md
- docs/context/codebase-map.md
- the active requirement listed in project context
```

**AI 不读这些文件就不能开始写代码**——这是强制性的入口检查。

### Task Routing（任务路由）

不是 AI 自己决定做什么，而是先问"这是什么类型的任务"：

```
Before writing code, agents MUST classify the task first:
1. Determine the task type:
   - requirement clarification     (需求澄清)
   - app-layer design change      (设计变更)
   - architecture change         (架构变更)
   - implementation-only change  (纯实现)
   - bug investigation           (Bug调查)
   - verification or audit work (验证/审计)
2. Use docs/index.md to read the owner docs for that task type before acting.
```

**不是想写就写，是先分类再决定走什么流程**。

### Planning Rule（规划触发）

`AGENTS.md` 规定了什么时候必须先做计划：

```
Create a plan when the task has any of these traits:
- changes API, database/model, auth, integration, deployment...
- touches multiple modules and changes shared behavior...
- is expected to take more than one AI session...
- modifies more than 5 total files...
- has unresolved product or technical risk that must not be hidden...
```

**不是想写就写，是条件触发**。

### 文件作为唯一真相源

所有结论必须写到文件里，chat 只是临时表面：

```
1. Prefer file-in, file-out collaboration.
2. Do not treat chat summaries as durable project memory.
```

---

## 三个核心机制对比

| 机制 | 作用 | 实现方式 |
|------|------|---------|
| **强制上下文** | AI 写代码前必须了解项目背景 | `docs/context/` + AGENTS.md 入口约定 |
| **Task Routing** | 不同任务类型走不同流程 | AGENTS.md 决策树 |
| **Planning Triggers** | 复杂任务必须先做计划 | AGENTS.md 触发条件列表 |

---

## 一个具体的例子

**传统方式**：
```
用户: 帮我加个用户管理模块
AI: 好!(直接开始写代码)
结果: 可能跟项目已有设计冲突，API 不一致，没有记录
```

**AGE 方式**：
```
用户: 帮我加个用户管理模块
AI: 先分类 -> 这是 app-layer design change
  然后问: 这个需求跟 docs/requirements/ 里的描述一致吗？
  要不要先出个 plan？
  涉及哪些模块的 owner docs？
结果: 有计划、有 review、有记录、可追溯
```

---

## 本质

AGE 不是什么魔法，而是一套 **约定 + 文件入口 + 触发条件**：

- 用 `AGENTS.md` 里的规则约束 AI
- 用 `docs/context/` 里的文件提供背景知识
- 用 Task Routing 决策树强制 AI 先思考再行动
- 用 Planning Triggers 强制复杂任务走计划流程

**本质上**：AGE 是"项目宪法"，AI 每次行动前都得确认自己符合宪法。