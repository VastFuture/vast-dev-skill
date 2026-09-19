# SSH Context 系统（模板）

每个 server 一个 `<server-name>.md` 文件。AI 在操作这台 server 前**必须先 Read 这个文件**获取上下文。

## 路径

```
~/.ssh-manager-skill/ssh-context/
├── README.md              # 本文件
├── <server-name>.md       # 每台 server 一个，机器特定
└── lessons/<topic>.md     # 跨机器通用经验
```

`<server-name>` 必须和 `data/servers.json` 里的 `name` 字段完全一致。

## 文件格式

`<server-name>.md`：

```markdown
---
name: <server-name>          # 必须与 servers.json 的 name 一致
host: 1.2.3.4                 # 可选，冗余存方便 grep
user: ubuntu                  # 当前默认登录用户
os: ubuntu 22.04              # 操作系统 + 版本
role: clash-server            # 一句话角色（人类可读）
tags: [aliyun, mihomo, clash] # 自由标签，方便检索
sudo: passwordless            # sudo 模式：passwordless | needs-password | none
cwd_default: ~                # 默认工作目录
updated: 2026-09-20           # 最后一次更新日期
---

# <一句话说明这台机器干嘛的>

# 角色与用途
... 自由文本 ...

# 用户与权限
- 默认用户: installer
- 提权方式: sudo -i（启动一个 root login shell）
- /etc/clash/ 需要 sudo 写
- 普通用户可以读 /etc/clash/

# 关键路径
- clash 配置: /etc/clash/
- clash 二进制: /usr/local/bin/clash
- clash systemd: clash.service

# 已安装的关键工具
- python3: 是
- systemd: 是（service 管理走 systemctl）
- curl: 是

# 已知坑（必须看）
- **坑 1**: ...
- **坑 2**: ...

# 关键诊断命令（速查）
- 看 clash 状态: systemctl status clash
- 看 clash 节点: curl -s http://127.0.0.1:9090/proxies | python3 -m json.tool
- 看 clash 日志: journalctl -u clash --no-pager -n 50

# 最近的故障 / 经验
- 2026-09-20 xxx 故障：根因 YYY。详见 ~/.claude/ai-dev-log/...
```

`<topic>.md` (lesson)：

```markdown
---
topic: <kebab-case-id>          # 文件名同名
severity: critical | warning | tip
tags: [<category>, ...]
related: [<other-topic-id>, ...]
updated: YYYY-MM-DD
---

# <一句话标题：什么场景 + 什么坑>

## 症状
看到 X / 报 Y → 说明踩坑了。

## 根因
一句话技术原因。

## 错的写法
... 反例 + 为什么失败 ...

## 对的写法
... 正例 + 为什么成功 ...

## 适用范围
- 适用: ...
- 不适用: ...
```

## 必填字段（server context）

| 字段 | 必填 | 含义 |
|---|---|---|
| `name` | 是 | 与 servers.json 的 name 一致 |
| `user` | 是 | 默认登录用户 |
| `os` | 是 | 操作系统 + 版本 |
| `sudo` | 是 | `passwordless` / `needs-password` / `none` |
| `updated` | 是 | 最后更新日期 YYYY-MM-DD |
| `host` | 否 | IP/域名（方便 grep） |
| `role` | 否 | 一句话角色 |
| `tags` | 否 | 自由标签 |
| `cwd_default` | 否 | 默认工作目录 |

## 必填字段（lesson）

| 字段 | 必填 | 含义 |
|---|---|---|
| `topic` | 是 | 文件名同名（kebab-case） |
| `severity` | 是 | `critical` / `warning` / `tip` |
| `updated` | 是 | 最后更新日期 |

## AI 工作流

```
用户说 "在 xx 服务器上做 yyy"
  ↓
AI Read ~/.ssh-manager-skill/ssh-context/<name>.md   ← 机器特定
  ↓
AI 按当前任务挑 lesson(s)，Read lessons/<topic>.md  ← 跨机器通用
  ↓
AI 综合判断 → 设计命令（参考 context 里的路径、权限、坑）
  ↓
AI 用 ssh-manager exec 执行
```

## 创建 / 更新 context

**AI 自己写**——用户说"加台服务器"、"这台机器要记一下 XXXX"，AI 就创建或更新对应的 `.md` 文件。

不需要任何额外的脚本/命令，AI 直接 Read/Write markdown。

## 删除 context

```bash
rm ~/.ssh-manager-skill/ssh-context/<name>.md
```

## 列出所有有 context 的 server

```bash
ls ~/.ssh-manager-skill/ssh-context/*.md | sed 's|.*/||;s|\.md$||'
```

## 示例

- `server-context.example.md` — 完整 server context 示例
- `lessons/lesson.example.md` — 完整 lesson 示例