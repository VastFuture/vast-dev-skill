---
name: vast-ssh-manager
description: 管理免密 SSH 服务器 + 外部 context 系统（每台机器特定信息 + 跨机器通用 lessons）。触发场景："添加服务器 ssh xxx"、"列出服务器"、"在 xx 上跑 xxx"、"登录"、"删除"、"这台机器记一下"、"踩了个坑记一下"。触发词：ssh、服务器、远程、添加、列出、执行、登录、删除、ssh-keygen、免密、context、坑、经验、lesson。不要触发：通用 shell、git、本地文件编辑。
---

# Vast SSH Manager

Two-layer SSH management: **connection** (script) + **context** (external markdown).

## Why split

| Layer | What | Storage |
|---|---|---|
| Connection | host / port / user / key | `scripts/ssh-manager.sh` + `data/servers.json` |
| Context | role / paths / gotchas / lessons | `~/.ssh-manager-skill/ssh-context/` (external markdown) |

Script stays simple and reliable. Per-server "what is this box for" and "what gotchas" live in human-maintainable markdown that AI reads before each operation.

## Standard Workflow

```
1. User: "do yyy on server xx"
2. AI: Read ~/.ssh-manager-skill/ssh-context/<name>.md     ← machine-specific
3. AI: Read relevant lesson(s) from ssh-context/lessons/  ← cross-machine
4. AI: design command (paths, sudo, gotchas)
5. AI: ssh-manager exec <name> "<cmd>"
```

## Critical Rules

1. **Read context BEFORE exec/ssh** (see Context section below).
2. **Idempotent key**: `add` is idempotent — don't bypass with raw ssh-keygen.
3. **Check duplicates** before add (read `data/servers.json`).
4. **Ask before destructive commands**: `rm -rf`, `mkfs`, `dd`, `shutdown`, `chmod 777`, modifications to `/etc/passwd`, `/etc/sudoers`, `/etc/ssh/sshd_config`.
5. **Ambiguous match → ask user**.
6. **Output visible**: never hide exec output.
7. **Fail honestly**: don't fake success.

## Context System (exec/ssh 前必读)

External markdown at `~/.ssh-manager-skill/ssh-context/`:

```
ssh-context/
├── README.md
├── <server-name>.md      ← machine-specific (per server)
├── lessons/<topic>.md    ← cross-machine, by topic
└── logs/                  ← operational logs (event-driven)
    └── YYYY-MM-DD-<topic>.md
```

### When to read / write

| Situation | Action | File |
|---|---|---|
| Before any `exec` / `ssh` | **Read** | `<server-name>.md` (full) |
| Task touches a known pitfall | **Read** | `lessons/<topic>.md` (relevant) |
| After a major incident / fix / day-end | **Write** | `logs/YYYY-MM-DD-<topic>.md` |
| User says "记一下 / add server / add lesson" | **Write** | `<server-name>.md` or `lessons/<topic>.md` |

### When user says "记一下 / add server / add lesson"

AI directly Read / Write the corresponding markdown file. **No CLI tool needed.**

## Operation Logs (重要事件后写)

事件驱动的 markdown 工作日志，存在 `~/.ssh-manager-skill/ssh-context/logs/`。

### When to write a log

| Trigger | Example |
|---|---|
| **重大故障修复** | "代理全死 → 2 节点复活"，类似 `2026-09-20-clash-proxy-recovery.md` |
| **跨多步的复杂操作** | "诊断 + 改配置 + 重启 + 验证" 整套 |
| **用户明确要求** | "记一下今天的工作" / "总结这次会话" |
| **周期工作结束** | 一周 / 一天的运维总结 |

**不要**为每个小 exec 都写日志——会刷屏且无信息量。

### Log format

```markdown
---
date: YYYY-MM-DD
topic: <一句话>
servers: [<server-name>]      # 涉及的服务器
tags: [<category>]
status: success | partial | failed
duration: ~<minutes>
---

# <标题>

## TL;DR
一两句话讲清发生了什么。

## 时间线
| 时间 | 事件 |
|---|---|
| HH:MM | ... |

## 关键发现
每条带"教训 / 正确做法"。

## 当前状态
表格列出关键指标。

## 后续行动
按优先级排列。

## 经验沉淀建议
哪些 lesson 应该新增 / 升级。

## 相关文件
其他 markdown 的相对路径。
```

### Logs vs Lessons — 何时用哪个

| 场景 | 用 logs | 用 lessons |
|---|---|---|
| 一次性事件记录 | ✓ | — |
| 跨机器通用的踩坑教训 | — | ✓ |
| 包含时间线 / 状态变化 | ✓ | — |
| 长期稳定可复用 | — | ✓ |

**经验**："这次会话学到 X" → 先写 logs，**末尾建议** 哪些可以升级为 lesson。AI 自己评估要不要升级。

## Common Patterns

### sudo write to `/etc/`

```bash
# ✗ redirect permission denied (shell `>` uses installer permission)
sudo base64 -d > /etc/clash/x

# ✓ A: write to /tmp then sudo mv
echo "$DATA" | base64 -d > /tmp/x && sudo mv /tmp/x /etc/clash/x

# ✓ B: sudo -i bash -s (redirect inside root shell)
ssh-manager exec server 'sudo -i bash -s' <<'EOF'
echo "$DATA" | base64 -d > /etc/clash/x
EOF
```

### heredoc with local variable to remote

```bash
# ✗ <<EOF expands $VAR locally before ssh
ssh-manager exec server 'bash -s' <<EOF
echo "got: $LOCAL_VAR"   # remote sees literal value, not var name
EOF

# ✓ <<'EOF' + pass var via cmd string
ssh-manager exec server "VAR=$LOCAL_VAR bash -s" <<'EOF'
echo "got: $VAR"          # remote sees $VAR as a var to expand
EOF
```

### exec failed — debugging flow

```
1. Re-read ssh-context/<name>.md "已知坑"
2. Read relevant lessons
3. ssh -i ~/.ssh/<name>_key -o BatchMode=yes <user>@<host> 'whoami'
4. bash -c "</dev/tcp/<host>/22"
5. Read references/troubleshooting.md
```

## Subcommands

| Command | Purpose |
|---|---|
| `add <user@host> [port] [name]` | generate key + push pubkey + verify + write config + json |
| `list` | table view |
| `show <name>` | JSON detail |
| `exec <name> "<cmd>"` | run on server |
| `ssh <name>` | interactive login |
| `remove <name>` | remove from list (keeps key file) |

## Files

- `scripts/ssh-manager.sh` — main script (bash, depends on `python3`)
- `data/servers.json` — connection list (created by `add`)
- `data/servers.json.example` — template
- `references/scenarios.md` — detailed flows
- `references/sudo-workflow.md` — sudo patterns
- `references/troubleshooting.md` — debugging
- `references/examples.md` — conversation templates
- `context-template/` — context system templates

## Installation

1. Copy this directory to `~/.claude/skills/vast-ssh-manager/` (or symlink)
2. Run `add <user@host>` to register your first server
3. AI reads this `SKILL.md` on first call to `ssh-manager`
4. AI asks you to populate `~/.ssh-manager-skill/ssh-context/<name>.md` after first exec

## Why External Context?

- **Decoupled**: context can be edited without touching the script.
- **Version-controllable**: each server's context is a small markdown file.
- **AI-friendly**: AI scans frontmatter first, then dives into the body.
- **Lesson accumulation**: `lessons/` grows with team experience.
- **Zero coupling**: bash script stays under 350 lines; everything else is docs.