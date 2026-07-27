---
name: vast-codex-image
description: "通过Codex CLI生成AI图片,使用ChatGPT Plus订阅,无需API密钥和额外费用。Actions: 生成图片、画图、create image、generate image、draw、制作图片、AI绘图、图片生成。支持场景: 信息图表、海报设计、产品图、概念图、插画、壁纸。当用户说'生成图片'、'画一张图'、'create an image'、'生成XX图片'、'帮我画'、'制作图片'、'AI画图'时使用。需要Codex CLI已安装并登录ChatGPT Plus账号。支持正方形(1024x1024)、横向(1536x1024)、纵向(1024x1536)尺寸。使用ChatGPT Plus的DALL-E 3配额,文字渲染准确,图片质量高。Triggers: generate image, create image, 生成图片, 画图, 绘图, AI画图, make image, draw image, 制作图片, 图片生成, image generation。"
---

# Vast Codex Image

通过 Codex CLI 生成 AI 图片,使用你的 ChatGPT Plus 订阅,零 API 成本。

IRON LAW: 必须先确认 Codex CLI 已安装并登录 ChatGPT Plus 账号,否则无法生成图片。生成图片会消耗 ChatGPT Plus 的 DALL-E 3 消息配额。

## Workflow

```
Vast Codex Image Progress:

- [ ] Step 1: 检查环境 ⛔ BLOCKING
  - [ ] 1.1 确认 Codex CLI 已安装
  - [ ] 1.2 确认已登录 ChatGPT Plus
- [ ] Step 2: 理解需求 ⚠️ REQUIRED
  - [ ] 2.1 明确图片内容和风格
  - [ ] 2.2 确定图片尺寸
  - [ ] 2.3 确定保存位置
- [ ] Step 3: 生成图片
  - [ ] 3.1 构建详细的提示词
  - [ ] 3.2 执行生成命令
  - [ ] 3.3 等待生成完成(可能需要1-2分钟)
- [ ] Step 4: 验证结果 ⚠️ REQUIRED
  - [ ] 4.1 确认图片已生成
  - [ ] 4.2 检查图片路径
  - [ ] 4.3 向用户展示结果
```

## Step 1: 检查环境 ⛔ BLOCKING

### 1.1 确认 Codex CLI 已安装

**macOS**: Codex CLI 位于 `/Applications/Codex.app/Contents/Resources/codex`
**Windows**: Codex CLI 位于 `%LOCALAPPDATA%\Programs\codex\codex.exe`

如果未安装,告知用户:
```
需要先安装 Codex CLI:
1. 访问 https://codex.chat 下载 Codex 桌面客户端
2. 安装后会自动包含 codex 命令行工具
```

### 1.2 确认已登录 ChatGPT Plus

Ask yourself:
- 用户是否有 ChatGPT Plus 订阅?
- Codex 是否已登录?

如果未确认,提醒用户:
```
这个工具需要:
✓ ChatGPT Plus 订阅 (访问 chatgpt.com/upgrade 升级)
✓ Codex 已登录到 Plus 账号

生成图片会消耗你的 ChatGPT Plus 消息配额(DALL-E 3)
```

## Step 2: 理解需求 ⚠️ REQUIRED

### 2.1 明确图片内容和风格

Ask user (if not clear):
- 图片的主题是什么?
- 希望什么风格? (写实/插画/概念图/海报/信息图表)
- 有特殊要求吗? (颜色/构图/情绪/细节)

**提示词优化原则**:
- 具体描述主体
- 说明风格和质量要求
- 指定光线、色彩、构图
- 英文提示词效果更好

### 2.2 确定图片尺寸

| 尺寸 | 用途 | 命令格式 |
|------|------|----------|
| 1024x1024 | 正方形,通用 | (默认,不需要指定) |
| 1536x1024 | 横向,壁纸/banner | `1536x1024` |
| 1024x1536 | 纵向,海报/手机壁纸 | `1024x1536` |

### 2.3 确定保存位置

默认: 当前工作目录
可选: `~/Downloads`, `~/Desktop`, 或用户指定路径

## Step 3: 生成图片

### 3.1 构建详细的提示词

**好的提示词示例**:
```
✓ "a fluffy orange cat sleeping on a cream-colored sofa, warm afternoon sunlight streaming through the window, photorealistic, 8k quality"

✓ "minimalist product poster, iPhone 15 Pro, centered composition, gradient background from deep blue to purple, soft shadows, apple-style design"

✓ "cyberpunk city skyline at night, neon lights reflecting on wet streets, flying cars in the distance, cinematic lighting, ultra wide angle"
```

**不好的提示词**:
```
✗ "cat" (太简单,缺少细节)
✗ "一只猫在沙发上" (中文可以用,但英文效果更好)
```

### 3.2 执行生成命令

```bash
python3 ~/.claude/skills/vast-codex-image/generate.py "<prompt>" [size] [output_dir]
```

**示例**:
```bash
# 正方形,默认尺寸
python3 ~/.claude/skills/vast-codex-image/generate.py "a shiba inu wearing sunglasses, beach background, summer vibes"

# 横向壁纸
python3 ~/.claude/skills/vast-codex-image/generate.py "mountain landscape at sunset, golden hour lighting" 1536x1024

# 纵向海报,保存到桌面
python3 ~/.claude/skills/vast-codex-image/generate.py "vintage concert poster, rock band silhouette" 1024x1536 ~/Desktop
```

### 3.3 等待生成完成

生成过程需要 **1-2 分钟**,这是正常的:
1. 命令发送到 Codex CLI
2. Codex 通过 ChatGPT Plus 调用 DALL-E 3
3. 图片生成并保存到本地

告知用户: "正在生成图片,请稍等 1-2 分钟..."

## Step 4: 验证结果 ⚠️ REQUIRED

### 4.1 确认图片已生成

检查命令输出:
- 成功: `SUCCESS:/path/to/codex-image-20260727-150230.png`
- 失败: `ERROR:...`

如果失败,可能的原因:
- Codex CLI 未安装或未登录
- ChatGPT Plus 配额用完
- 提示词违反内容政策
- 网络问题

### 4.2 检查图片路径

生成的图片文件名格式: `codex-image-YYYYMMDD-HHMMSS.png`

### 4.3 向用户展示结果

**成功时**:
```
✅ 图片已生成!

保存位置: /path/to/codex-image-20260727-150230.png
尺寸: 1024x1024
提示词: [用户的提示词]

[如果可以,展示图片预览]
```

**失败时**:
```
❌ 图片生成失败

错误: [具体错误信息]
可能原因:
- 检查 Codex CLI 是否已安装
- 确认已登录 ChatGPT Plus
- 检查配额是否充足
- 尝试修改提示词
```

## Advanced: 参考图片编辑

如果用户提供了一张参考图片,想基于它重新生成:

```bash
python3 ~/.claude/skills/vast-codex-image/generate.py "product info: [描述]" 1024x1024 ~/Desktop --image /path/to/reference.png
```

这会:
1. 参考原图的设计风格和布局
2. 根据新的产品信息重新生成
3. 保持视觉风格一致

## Anti-Patterns

Do NOT:
- ❌ 提示词过于简单(少于5个词)
- ❌ 不检查环境就直接生成
- ❌ 忽略错误信息
- ❌ 在生成过程中断(需要等待1-2分钟)
- ❌ 使用违反内容政策的提示词
- ❌ 假设用户有无限配额(提醒会消耗配额)

## Common Use Cases

### 用例1: 概念图/插画
```
提示词: "a futuristic AI assistant robot, friendly appearance, holographic interface, soft blue lighting, digital art style"
尺寸: 1024x1024
```

### 用例2: 产品海报
```
提示词: "product poster for wireless earbuds, minimalist design, white background, dramatic lighting, apple-style photography"
尺寸: 1024x1536 (纵向)
```

### 用例3: 社交媒体 Banner
```
提示词: "tech conference banner, abstract geometric shapes, gradient from blue to purple, modern and professional"
尺寸: 1536x1024 (横向)
```

### 用例4: 信息图表
```
提示词: "infographic showing project timeline, modern flat design, colorful icons, clean layout, corporate style"
尺寸: 1024x1536
```

## 工作原理

```
用户请求
    ↓
Vast Codex Image Skill
    ↓
generate.py 脚本
    ↓
Codex CLI (本地)
    ↓
ChatGPT Plus (DALL-E 3)
    ↓
图片 → 保存到本地
```

- 不调用 OpenAI API
- 不产生额外费用
- 使用你已有的 ChatGPT Plus 订阅
- 消耗 Plus 的 DALL-E 3 消息配额

## Pre-Delivery Checklist

### 环境检查
- [ ] 已确认 Codex CLI 已安装
- [ ] 已确认用户有 ChatGPT Plus
- [ ] 已提醒会消耗配额

### 提示词质量
- [ ] 提示词足够详细(10+个词)
- [ ] 指定了风格和质量要求
- [ ] 使用英文或优化过的描述

### 执行验证
- [ ] 命令格式正确
- [ ] 路径存在且可写
- [ ] 等待足够时间(1-2分钟)

### 结果反馈
- [ ] 向用户报告成功/失败状态
- [ ] 提供图片保存路径
- [ ] 如果失败,提供排查建议
