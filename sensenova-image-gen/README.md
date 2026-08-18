# SenseNova U1 Fast - AI 信息图生成工具

基于商汤 SenseNova U1 Fast API 的专业信息图生成 Skill。

## 特性

- 🎨 **多尺寸支持**: 11 种 aspect ratio（16:9, 1:1, 2:3, 3:2 等）
- ⚡ **极速生成**: 每张图片 6-8 秒
- 📊 **专业信息图**: 专为 Infographics 优化
- 💾 **自动保存**: 自动下载避免 1 小时 URL 失效
- 📋 **详细报告**: JSON 格式完整测试报告

## 快速开始

### 1. 获取 API Key

访问商汤 SenseNova 平台注册：
👉 https://platform.sensenova.cn/console

### 2. 设置环境变量

```bash
export SENSENOVA_API_KEY='your-api-key-here'
```

或创建 `.env` 文件：
```bash
echo 'SENSENOVA_API_KEY=your-api-key-here' > .env
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 生成信息图

```bash
python scripts/generate_infographic.py \
  --prompt "AI技术发展历程信息图" \
  --size "2752x1536"
```

## 使用示例

### 单张生成

```bash
python scripts/generate_infographic.py \
  --prompt "这张信息图展示Python学习路线..." \
  --size "2752x1536" \
  --output my_infographic.png \
  --save-report
```

### 批量测试

```bash
python scripts/test_all_sizes.py
```

## 支持的尺寸

| 尺寸 | 比例 | 适用场景 |
|------|------|---------|
| 2752×1536 | 16:9 | 横屏演示、网页横幅 |
| 1536×2752 | 9:16 | 竖屏手机、社交媒体 |
| 2048×2048 | 1:1 | 社交媒体方形帖子 |
| 2496×1664 | 3:2 | 标准横屏 |
| 1664×2496 | 2:3 | 标准竖屏 |
| 更多... | ... | 查看文档 |

## 文档

- 📖 [API 文档](references/api-documentation.md)
- 🎨 [Prompt 示例](references/prompt-examples.md)
- 🔧 [脚本使用](references/script-usage.md)
- ❓ [常见问题](references/faq.md)

## 注意事项

⚠️ **重要限制**：
- 图片 URL 有效期仅 **1 小时**
- 不支持图像输入（仅文本 prompt）
- 最大 token 数：4096

## 版本

- **Skill 版本**: 1.0.0
- **API 版本**: v1
- **模型**: sensenova-u1-fast
- **最后更新**: 2026-07-29

## 许可

本 Skill 使用 MIT 许可证。API 服务由商汤 SenseNova 提供。
