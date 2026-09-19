---
name: example_server
host: 192.168.1.100
user: ubuntu
os: Ubuntu 22.04 (jammy)
role: home-dev-server
tags: [home, dev, self-hosted]
sudo: passwordless
cwd_default: ~
updated: 2026-09-20
---

# 家用开发机，跑 docker compose 部署私人服务

默认用户 ubuntu，sudo 免密。这台机器主要跑个人项目 + Docker 容器。

# 角色与用途

- 私人代码托管（gitea）
- 跑 AI 实验（jupyter、stable diffusion）
- 个人网盘（nextcloud）

# 用户与权限

- 默认登录用户: **ubuntu**（uid 1000，sudo 组成员）
- 提权方式: `sudo` 即可（不用 sudo -i）
- /opt/、/srv/、/home/ubuntu/ 用户可写
- /etc/ 需要 sudo

# 关键路径

- docker compose 项目: /opt/stacks/{gitea,jupyter,nextcloud}/
- 数据卷: /var/lib/docker/volumes/
- 个人 dotfiles: /home/ubuntu/dotfiles/
- 备份: /mnt/backup/（外接 USB 盘）

# 已安装的关键工具

- python3: ✓
- docker: ✓ v24 + compose v2
- systemd: ✓
- nvidia-smi: ✓（RTX 3060 12G）

# 已知坑（必须看）

- **GPU 容器要装 nvidia-container-toolkit**：否则容器看不到显卡
- **外接 USB 盘**偶尔掉线，systemd automount 配过了，看 `/etc/systemd/system/mnt-backup.automount`
- **Nextcloud 上传限速**：fpm pm.max_children 调到 20 才行

# 关键诊断命令（速查）

```bash
# docker 状态
docker ps
docker compose -f /opt/stacks/gitea/docker-compose.yml ps

# GPU
nvidia-smi

# USB 盘
ls -la /mnt/backup/
sudo systemctl status mnt-backup.automount

# 看系统负载
htop
iostat -xm 2

# 网络
ip a
ss -tlnp
```

# 最近的故障 / 经验

- 2026-09-15 docker compose 升级 v2 失败：原因是 docker-compose-plugin 没装。`apt install docker-compose-plugin` 后正常。