# SenseNova U1 Fast API 官方文档

## 接口概述

SenseNova U1 Fast 是基于 SenseNova U1 的加速版本，专供信息图（Infographics）生成。

- **模型 ID**: `sensenova-u1-fast`
- **接口类型**: 图像生成（非 Chat Completions）
- **图片有效期**: 1 小时

## 接口地址

```
POST https://token.sensenova.cn/v1/images/generations
```

## 认证方式

使用 Bearer Token 认证：

```bash
Authorization: Bearer YOUR_API_KEY
```

## 请求参数

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| model | string | ✅ | - | 固定为 `sensenova-u1-fast` |
| prompt | string | ✅ | - | 图像描述文本，最大 token 数为 4096 |
| size | string | ❌ | `"2752x1536"` | 图像尺寸，见下方支持列表 |
| n | integer | ❌ | 1 | 生成图片数量 |

### 支持的尺寸

2K 分辨率常量 - 11 种 aspect ratio：

| 尺寸 | 比例 |
|------|------|
| 1664x2496 | 2:3 |
| 2496x1664 | 3:2 |
| 1760x2368 | 3:4 |
| 2368x1760 | 4:3 |
| 1824x2272 | 4:5 |
| 2272x1824 | 5:4 |
| 2048x2048 | 1:1 |
| 2752x1536 | 16:9 |
| 1536x2752 | 9:16 |
| 3072x1376 | 21:9 |
| 1344x3136 | 9:21 |

## 请求示例

### cURL

```bash
curl https://token.sensenova.cn/v1/images/generations \
  -H "Authorization: Bearer $SENSENOVA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sensenova-u1-fast",
    "prompt": "这张信息图展示了AI技术发展历程...",
    "size": "2752x1536",
    "n": 1
  }'
```

### Python

```python
import requests

url = "https://token.sensenova.cn/v1/images/generations"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": "sensenova-u1-fast",
    "prompt": "详细的信息图描述...",
    "size": "2752x1536",
    "n": 1
}

response = requests.post(url, headers=headers, json=payload)
data = response.json()
```

## 响应结构

```json
{
  "created": 1713167890,
  "data": [
    {
      "url": "https://cdn.sensenova.dev/gen/..."
    }
  ]
}
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| created | integer | Unix 时间戳 |
| data | array | 图片数据数组 |
| data[].url | string | 图片临时访问 URL（1 小时有效期） |

## 重要限制

⚠️ **关键注意事项**：

1. **URL 有效期**: 接口返回的图片 URL 为临时访问链接，**固定有效期 1 小时**，超时后链接直接失效，无法再次访问图片。
2. **不支持图像输入**: U1 Fast 使用独立的图像生成接口，不是 Chat Completions 接口，不支持图像输入。
3. **Token 限制**: prompt 最大 token 数为 4096。

## 错误码

| HTTP 状态码 | 说明 |
|------------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 认证失败 |
| 429 | 请求频率超限 |
| 500 | 服务器错误 |

## 最佳实践

1. **立即下载图片**: 由于 URL 仅 1 小时有效期，建议立即下载保存到本地
2. **结构化 Prompt**: 使用明确的层级结构描述信息图内容
3. **错误处理**: 实现完整的超时和重试机制
4. **成本控制**: 合理控制生成频率和数量

## 相关链接

- 官方平台: https://platform.sensenova.cn/console
- API 文档: https://platform.sensenova.cn/docs
