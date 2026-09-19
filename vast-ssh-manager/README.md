# vast-ssh-manager

> Vast 系列的 SSH 服务器管理技能。两层架构：**连接层**（bash 脚本）+ **上下文层**（外部 markdown）。

## 特性

- **免密登录**：自动生成 ed25519 密钥、推送公钥、验证免密、写入 `~/.ssh/config`
- **幂等设计**：`add` 检测到密钥已存在会复用，多次执行安全
- **外部 context 系统**：每台服务器一个 markdown，跨机器 lessons 库
- **AI 友好**：SKILL.md 引导 AI 在 exec/ssh 前先读 context，避开已知坑
- **零脚本膨胀**：核心脚本 < 350 行，所有"机器特定信息" 在 markdown

## 架构

```
vast-ssh-manager/
├── SKILL.md                      # AI 入口（vast 风格）
├── README.md                     # 本文件
├── scripts/
│   └── ssh-manager.sh            # 核心脚本（add/list/show/exec/ssh/remove）
├── data/
│   └── servers.json.example      # 数据格式示例
├── references/                   # 按需加载的详细文档
│   ├── scenarios.md
│   ├── sudo-workflow.md
│   ├── troubleshooting.md
│   └── examples.md
└── context-template/             # context 系统模板（用户首次用时复制）
    ├── README.md
    ├── server-context.example.md
    └── lessons/
        └── lesson.example.md
```

## 安装

### 方式 A：拷贝到 skills 目录

```bash
cp -r vast-ssh-manager ~/.claude/skills/
```

### 方式 B：符号链接（开发模式）

```bash
ln -s "$(pwd)/vast-ssh-manager" ~/.claude/skills/vast-ssh-manager
```

### 方式 C：在另一个 skill 里复用

```bash
ln -s /path/to/vast-dev-skill/vast-ssh-manager/scripts/ssh-manager.sh \
      ~/.claude/skills/your-skill/scripts/ssh-manager.sh
```

## 快速开始

```bash
# 1. 安装 skill（一次性）
cp -r vast-ssh-manager ~/.claude/skills/

# 2. 创建 context 目录（一次性）
mkdir -p ~/.ssh-manager-skill/ssh-context/lessons

# 3. 添加服务器（脚本自动生成密钥 + 推送公钥 + 验证免密）
bash ~/.claude/skills/vast-ssh-manager/scripts/ssh-manager.sh add user@1.2.3.4
#    ↑ 这次执行后得到 server name（默认 user_1_2_3_4 这种格式）
```

**之后所有步骤都是 AI 做：**

| 步骤 | 谁做 | 做什么 |
|---|---|---|
| 4. 写 context 文件 | **AI**（问你问题） | 第一次 exec 前，AI 会问你这台机器的 OS、用户、关键路径、坑。AI 自动写 `~/.ssh-manager-skill/ssh-context/<name>.md`（frontmatter + 骨架），你审核/补充正文 |
| 5. exec 前 Read context | **AI**（强制） | SKILL.md 规则 3 强制要求，每次 exec/ssh 前**无条件** Read `<name>.md` |
| 6. exec 前 Read lessons | **AI**（按需） | 当前任务涉及已知坑时，按 `<topic>.md` 路径 Read |
| 7. 写新 lesson | **AI**（你提示"记一下"） | 你说"踩了个坑记一下"，AI 写到 `~/.ssh-manager-skill/ssh-context/lessons/<topic>.md` |

**核心理念**：用户只回答"这台机器 XXXX" 和 "记一下 YYYY"，剩下的全是 AI 自动做。

## Context 系统（核心理念）

参考宝玉的"外部化配置"思想：把容易变、需要人维护的信息从脚本里剥离到外部 markdown。

**两个层级**：

| 层级 | 文件 | 内容 |
|---|---|---|
| 机器特定 | `ssh-context/<server-name>.md` | OS、用户、权限、关键路径、坑、诊断命令 |
| 跨机器 | `ssh-context/lessons/<topic>.md` | 通用经验（任何机器做 X 都会踩 Y 的坑） |

**AI 工作流**：

```
exec / ssh 前
  ↓
Read ssh-context/<name>.md      ← 机器特定
  ↓
按需 Read ssh-context/lessons/   ← 跨机器通用
  ↓
综合判断 → 设计命令
  ↓
ssh-manager exec
```

详见 `context-template/README.md`。

## 与原 ssh-manager 技能的关系

`vast-ssh-manager` 是 `~/.claude/skills/ssh-manager` 的**升级版 / 分发版**：

| 项目 | 原 ssh-manager | vast-ssh-manager |
|---|---|---|
| 核心脚本 | 同 | 同（复制，未修改）|
| Context 系统 | ✅（后期加） | ✅（默认包含在模板里）|
| SKILL.md 描述 | 中文 | vast 风格 + 双向引用 lessons |
| 可独立分发 | ❌（依赖用户实例） | ✅（含 templates 和 examples）|
| 在 vast-dev-skill 仓库 | ❌ | ✅ |

## 贡献

发现新坑？写 lesson：

1. 复制 `context-template/lessons/lesson.example.md` → `~/.ssh-manager-skill/ssh-context/lessons/<your-topic>.md`
2. 填 frontmatter、症状、根因、错/对写法
3. 在相关 server context 的"已知坑"里加引用

发现 skill 设计问题？提 issue 或 PR 到本仓库。

## 许可

参考原 ssh-manager 技能作者约定。