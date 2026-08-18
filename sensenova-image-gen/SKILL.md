---
name: sensenova-image-gen
description: Use when users ask to generate or create images with SenseNova, SenseNova U1 Fast, or 商汤. Triggers include 生成图片, 画图, 做图, AI 绘图, AI 作画, 文生图, 图片生成, 海报, 封面, 插画, 信息图, infographic, and image generation.
---

# SenseNova Image Gen - AI 信息图生成 Skill

基于商汤 SenseNova U1 Fast 的专业信息图生成能力，快速将复杂文字描述转化为高质量信息图。

## 触发条件

当用户提到以下关键词时使用此 skill：
- "生成信息图" / "infographic" / "信息可视化"
- "SenseNova" / "商汤" / "U1 Fast"
- "数据可视化" / "图表生成" / "视觉呈现"
- "画个信息图" / "做个信息图" / "设计信息图"

## 核心能力

- 🎨 **多尺寸支持**: 11 种 aspect ratio（16:9, 1:1, 2:3, 3:2 等）
- ⚡ **极速生成**: 每张图片 6-8 秒
- 📊 **专业信息图**: 专为 Infographics 优化的视觉呈现
- 💾 **自动保存**: 自动下载图片避免 1 小时 URL 失效
- ⚙️ **用户配置**: 持久化配置文件，敏感信息统一管理

## 配置管理

### 配置优先级

```
环境变量 SENSENOVA_API_KEY  >  ~/.sensenova/config.yml
```

### 配置文件路径

```
~/.sensenova/config.yml
```

### 配置文件内容

```yaml
api_key: "your-api-key-here"     # 必填
default_size: "2752x1536"         # 默认尺寸
output_dir: "~/Pictures/sensenova" # 图片保存目录
```

## 使用流程

### 1. 首次使用 - 初始化配置

首次运行脚本时，若未检测到配置文件，**自动创建**并引导用户填写：

```bash
python scripts/generate_infographic.py --prompt "测试"

# 输出：
# [INFO] 首次使用，正在初始化配置文件...
# [OK] 配置文件已创建: ~/.sensenova/config.yml
#
# 请编辑配置文件填写你的 API Key:
#   获取免费 API Key: https://platform.sensenova.cn/console
#
# 请使用文本编辑器打开该文件。
```

获取 API Key：👉 **https://platform.sensenova.cn/console**

填写完成后重新运行即可，无需再次配置。

### 2. 理解用户需求

询问用户以下信息：
- 信息图的主题和内容
- 目标尺寸比例（默认 16:9）
- 视觉风格偏好
- 色彩方案

### 3. 构建详细 Prompt

根据用户需求，构建结构化的信息图描述：

```python
# 参考模板
prompt = """
这张信息图展示了"{主题}"。采用{视觉风格}设计风格，以{色彩方案}为主色调。

整体布局分为{N}个部分：

1. {区域1名称}：
   - {要点1}
   - {要点2}
   - {要点3}

2. {区域2名称}：
   - {步骤1}
   - {步骤2}
   - {步骤3}

3. {区域3名称}：
   - {特点1}
   - {特点2}
   - {特点3}
"""
```

### 4. 调用生成脚本

使用 `scripts/generate_infographic.py` 生成图片：

```bash
python scripts/generate_infographic.py \
  --prompt "详细描述..." \
  --size "2752x1536" \
  --output "output.png"
```

### 5. 验证结果

- 检查生成的图片质量
- 确认尺寸和内容符合预期
- 提供本地文件路径给用户

## 支持的尺寸

| 尺寸 | 比例 | 适用场景 |
|------|------|---------|
| 2752×1536 | 16:9 | 横屏演示、网页横幅 |
| 1536×2752 | 9:16 | 竖屏手机、社交媒体 Story |
| 2048×2048 | 1:1 | 社交媒体方形帖子 |
| 2496×1664 | 3:2 | 标准横屏 |
| 1664×2496 | 2:3 | 标准竖屏 |
| 2272×1824 | 5:4 | 经典横屏 |
| 1824×2272 | 4:5 | 经典竖屏 |
| 2368×1760 | 4:3 | 传统横屏 |
| 1760×2368 | 3:4 | 传统竖屏 |
| 3072×1376 | 21:9 | 超宽屏 |
| 1344×3136 | 9:21 | 超长竖屏 |

## 最佳实践

### Prompt 撰写技巧

1. **结构化描述**: 使用明确的层级和区块划分
2. **具体化内容**: 列出所有文字内容，不要省略
3. **视觉细节**: 描述色彩、风格、图标等视觉元素
4. **布局说明**: 明确左右/上下区域的安排

### 示例 Prompt

查看 `references/prompt-examples.md` 获取更多示例。

## 注意事项

⚠️ **重要限制**：
- 接口返回的图片 URL **有效期仅 1 小时**
- 不支持图像输入（仅文本 prompt）
- 最大 token 数：4096
- 使用独立接口，不是 Chat Completions

⚠️ **成本考虑**：
- 需要查看官方定价策略
- 建议先用小批量测试

## 故障排查

### API Key 无效
```bash
# 检查环境变量
echo $SENSENOVA_API_KEY

# 重新设置
export SENSENOVA_API_KEY='your-key'
```

### 请求超时
- 检查网络连接
- 增加超时时间（默认 60 秒）

### 图片下载失败
- URL 可能已过期（1 小时限制）
- 检查本地存储空间

## 参考资源

- 📖 [官方 API 文档](references/api-documentation.md)
- 🎨 [Prompt 示例库](references/prompt-examples.md)
- 🔧 [脚本使用说明](references/script-usage.md)
- ❓ [FAQ 常见问题](references/faq.md)

## 版本信息

- **Skill 版本**: 1.0.0
- **API 版本**: v1
- **模型**: sensenova-u1-fast
- **最后更新**: 2026-07-29
