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
└── lessons/<topic>.md    ← cross-machine, by topic
```

### When to read

| Situation | Must read |
|---|---|
| Before any `exec` / `ssh` | `<server-name>.md` (full) |
| Task touches a known pitfall | `lessons/<topic>.md` (relevant) |

### When user says "记一下 / add server / add lesson"

AI directly Read / Write the corresponding markdown file. **No CLI tool needed.**

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