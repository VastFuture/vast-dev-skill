# Vast Codex Image

通过 Codex CLI 生成 AI 图片,使用 ChatGPT Plus 订阅,零 API 成本。

## 简介

Vast Codex Image 是对 [codex-image](https://github.com/Leon-llb/codex-image) 的归档和封装,让任何 CLI 工具或 AI Agent 都能通过 Codex CLI 生成图片。

**原项目**: https://github.com/Leon-llb/codex-image  
**作者**: [Leon](https://github.com/Leon-llb)  
**License**: MIT

## 核心优势

| 特性 | Vast Codex Image | API方案 |
|------|------------------|---------|
| 成本 | 无额外费用(使用Plus配额) | 按图片收费 |
| 模型 | ChatGPT原生图片模型(DALL-E 3) | 取决于API |
| 文字渲染 | 准确 | 参差不齐 |
| 设置 | 一条命令安装 | 注册、充值、配置 |
| 依赖 | Codex CLI | 无 |

## 前置要求

| 要求 | 说明 |
|------|------|
| 操作系统 | macOS 或 Windows |
| [Codex](https://codex.chat) | 桌面客户端,提供 `codex` CLI |
| ChatGPT Plus | 图片生成使用 Plus 配额(DALL-E 3消息限制适用) |

> 没有 Plus? 访问 [chatgpt.com/upgrade](https://chatgpt.com/upgrade) 升级

## 快速开始

### 安装

技能已包含在仓库中:
```bash
# 位置
~/.claude/skills/vast-codex-image/
```

### 使用

```bash
# 基础用法
python3 ~/.claude/skills/vast-codex-image/generate.py "a cat sleeping on a sofa, warm sunlight"

# 指定尺寸
python3 ~/.claude/skills/vast-codex-image/generate.py "cyberpunk city at night" 1536x1024

# 指定保存位置
python3 ~/.claude/skills/vast-codex-image/generate.py "zen garden" 1024x1536 ~/Desktop
```

## 支持的尺寸

| 尺寸 | 用途 | 示例 |
|------|------|------|
| 1024x1024 | 正方形(默认) | 头像、图标、通用图片 |
| 1536x1024 | 横向 | 壁纸、Banner、横版海报 |
| 1024x1536 | 纵向 | 手机壁纸、竖版海报 |

## 使用示例

### 示例1: 生成插画
```bash
python3 ~/.claude/skills/vast-codex-image/generate.py "a fluffy orange cat sleeping on a cream-colored sofa, warm afternoon sunlight streaming through the window, photorealistic, 8k quality"
```

### 示例2: 产品海报(纵向)
```bash
python3 ~/.claude/skills/vast-codex-image/generate.py "minimalist product poster, iPhone 15 Pro, centered composition, gradient background from deep blue to purple" 1024x1536 ~/Downloads
```

### 示例3: 桌面壁纸(横向)
```bash
python3 ~/.claude/skills/vast-codex-image/generate.py "mountain landscape at sunset, golden hour lighting, ultra wide angle" 1536x1024 ~/Desktop
```

## 集成方式

### Claude Code

技能已自动可用,直接对话即可:
```
你: "帅哥,生成一张赛博朋克风格的城市夜景图"
Claude: [调用 vast-codex-image 生成]
```

触发词:
- "生成图片"、"画一张图"、"制作图片"
- "generate an image"、"create image"
- "帮我画"、"AI画图"

### Hermes / OpenClaw Agent

让你的 Telegram 或 WeChat Agent 也能生成图片。

**安装插件** (原项目提供):
```bash
# 复制插件文件
mkdir -p ~/.hermes/hermes-agent/plugins/image_gen/codex-image
cp hermes-plugin/* ~/.hermes/hermes-agent/plugins/image_gen/codex-image/
```

**配置** `~/.hermes/config.yaml`:
```yaml
plugins:
  enabled:
    - image_gen/codex-image

image_gen:
  provider: codex-image
```

**重启**:
```bash
hermes gateway restart
```

## 工作原理

```
用户 → Hermes/Claude → image_generate 工具调用
                           ↓
                  codex-image provider
                           ↓
                    generate.py 脚本
                           ↓
                 codex exec (ChatGPT Plus)
                           ↓
                    图片 → ~/Downloads
```

无 OpenAI API 调用,无额外费用,只使用你的 Plus 订阅(会消耗 DALL-E 3 消息配额)。

## 技能结构

```
vast-codex-image/
├── SKILL.md           # 完整的工作流程和使用指南
├── generate.py        # 核心生成脚本
├── LICENSE            # MIT License
└── README.md          # 本文档
```

## 提示词建议

### 好的提示词
```
✓ "a fluffy orange cat sleeping on a sofa, warm sunlight, photorealistic"
✓ "minimalist product poster, iPhone, gradient background, apple-style"
✓ "cyberpunk city skyline at night, neon lights, cinematic lighting"
✓ "vintage concert poster, rock band silhouette, grunge texture"
```

### 需要改进的提示词
```
✗ "cat" (太简单)
✗ "一只猫" (可以用,但英文效果更好)
✗ "nice picture" (没有具体描述)
```

### 提示词优化技巧
1. **描述主体**: 具体说明要画什么
2. **指定风格**: photorealistic / illustration / minimalist / vintage
3. **说明细节**: 光线、颜色、构图、情绪
4. **质量要求**: 8k / high quality / detailed
5. **使用英文**: DALL-E 3 对英文提示词优化更好

## 注意事项

### 配额消耗
- 每生成一张图片,会消耗 1 条 ChatGPT Plus 的 DALL-E 3 消息配额
- Plus 用户每 3 小时有 50 条消息限制
- 如果配额用完,需要等待重置

### 内容政策
- 遵守 OpenAI 的内容政策
- 不要生成暴力、色情、政治敏感内容
- 不要生成真人肖像(名人、公众人物)

### 生成时间
- 通常需要 1-2 分钟
- 复杂图片可能需要更长时间
- 网络不稳定时可能超时

## 故障排查

### 问题1: 找不到 codex 命令
```
解决: 
1. 确认已安装 Codex 桌面客户端
2. macOS: 检查 /Applications/Codex.app 是否存在
3. Windows: 检查 %LOCALAPPDATA%\Programs\codex\ 是否存在
```

### 问题2: 生成失败
```
可能原因:
- 未登录 ChatGPT Plus
- 配额已用完
- 提示词违反内容政策
- 网络连接问题

解决:
1. 打开 Codex 桌面应用,确认已登录
2. 检查 Plus 订阅状态
3. 修改提示词,避免敏感内容
4. 检查网络连接
```

### 问题3: 图片未找到
```
解决:
1. 检查输出目录是否可写
2. 查看 ~/.codex/generated_images/ 目录
3. 确认命令执行成功(SUCCESS:路径)
```

## 对比原项目的改进

1. **命名规范**: `codex-image` → `vast-codex-image`,统一 vast 系列命名
2. **完整文档**: 提供中文使用文档和详细的工作流程
3. **技能封装**: 提供 SKILL.md,方便 Claude Code 集成
4. **归档管理**: 纳入 vast-dev-skill 统一管理

## 原项目信息

- **项目**: codex-image
- **地址**: https://github.com/Leon-llb/codex-image
- **作者**: Leon (https://github.com/Leon-llb)
- **License**: MIT
- **归档时间**: 2026-07-27

感谢原作者 Leon 的贡献!

## 相关资源

- [Codex 官网](https://codex.chat)
- [ChatGPT Plus](https://chatgpt.com/upgrade)
- [OpenAI 内容政策](https://openai.com/policies/usage-policies)

## License

MIT (继承自原项目)

---

归档整理: Vast Future  
归档时间: 2026-07-27  
原项目: https://github.com/Leon-llb/codex-image
