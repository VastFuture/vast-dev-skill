---
topic: example-lesson
severity: warning
tags: [docker, systemd, example]
related: []
updated: 2026-09-20
---

# docker service 启动后容器没起来，90% 是 compose 文件路径错了

## 症状

```bash
$ systemctl status my-app.service
● my-app.service - My App
   Active: active (exited)  ← service 起来了，但
$ docker ps
                              ← 容器没在跑！
```

`service` 状态显示 `active (exited)` 而不是 `active (running)`——说明 systemd 进程跑完了，但 docker 没启动容器。

## 根因

`docker-compose@<name>.service` 的 `WorkingDirectory` 配置错误，或者 `docker-compose.yml` 文件不存在。

或者 compose 文件存在但**路径用了相对路径**（systemd 启动时 cwd 不是 home）。

## 错的写法

```ini
# /etc/systemd/system/my-app.service
[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/user                    ← 用相对路径在 ~/myapp/ 找
ExecStart=/usr/bin/docker compose up -d        ← 找不到 docker-compose.yml
```

```yaml
# /home/user/myapp/docker-compose.yml  ← 实际在 ~/myapp/ 里
# 但 WorkingDirectory 没设对
```

## 对的写法

**方案 A：用绝对路径**

```ini
[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/user/myapp              ← 绝对路径
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
```

**方案 B：用 `-f` 指定 compose 文件**

```ini
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/bin/docker compose -f /home/user/myapp/docker-compose.yml up -d
ExecStop=/usr/bin/docker compose -f /home/user/myapp/docker-compose.yml down
```

**方案 C：用官方 systemd unit 生成器**

```bash
# 在 compose 项目目录下
docker compose --ansi never convert > docker-compose.service

# 或用社区工具
/usr/local/bin/compose-systemd-unit /home/user/myapp/docker-compose.yml \
    > /etc/systemd/system/my-app.service
```

## 验证方法

```bash
# 1. service 状态
sudo systemctl status my-app.service
# 应该显示 active (running)，不是 active (exited)

# 2. 容器在跑
docker ps | grep myapp

# 3. 手动跑 ExecStart 看输出
sudo systemctl start my-app.service
journalctl -u my-app.service -n 30 --no-pager

# 4. 看 service 文件实际生效的配置
sudo systemctl show my-app.service | grep WorkingDirectory
```

## 适用范围

- 适用: 用 systemd 托管 docker compose 项目
- 适用: `Type=oneshot` + `RemainAfterExit=yes` 的 compose service
- 不适用: docker compose 本身（不是 systemd 的锅）
- 不适用: k8s / nomad / 其他编排器

## 相关

- docker 官方文档: https://docs.docker.com/compose/compose-file/compose-file-v3/
- systemd compose unit 模板: https://github.com/mjuen/docker-compose-systemd-unit