# 脚本使用说明

## 脚本列表

### 1. generate_infographic.py

单张信息图生成脚本。

**功能**：
- 生成单张指定尺寸的信息图
- 支持从命令行或文件读取 prompt
- 自动下载并保存图片
- 可选生成详细报告

**使用方法**：

```bash
# 基础用法
python scripts/generate_infographic.py \
  --prompt "AI技术发展历程信息图" \
  --size "2752x1536"

# 从文件读取 prompt
python scripts/generate_infographic.py \
  --prompt-file my_prompt.txt \
  --output my_infographic.png

# 保存详细报告
python scripts/generate_infographic.py \
  --prompt "数据分析流程图" \
  --save-report
```

**参数说明**：

| 参数 | 必填 | 说明 | 默认值 |
|------|------|------|--------|
| --prompt | ❌ | 图像描述文本 | - |
| --prompt-file | ❌ | 从文件读取 prompt | - |
| --size | ❌ | 图像尺寸 | 2752x1536 |
| --output | ❌ | 输出文件路径 | 自动生成 |
| --save-report | ❌ | 保存 JSON 报告 | False |

**注意**：`--prompt` 和 `--prompt-file` 必须提供其中一个。

**输出**：
- 图片文件：`infographic_{size}_{timestamp}.png`
- 报告文件（可选）：`infographic_{size}_{timestamp}.json`

---

### 2. test_all_sizes.py

批量测试所有支持的尺寸。

**功能**：
- 测试 4 种常见尺寸比例
- 自动下载所有生成的图片
- 生成详细的测试报告
- 统计成功率和失败原因

**使用方法**：

```bash
python scripts/test_all_sizes.py
```

**输出目录**：`test_outputs/`
- 图片文件：`sensenova_u1_fast_{size}_{timestamp}.png`
- 测试报告：`test_report_{timestamp}.json`

**报告内容**：
```json
{
  "test_time": "2026-07-29T13:35:33",
  "total": 4,
  "success": 4,
  "failed": 0,
  "results": [
    {
      "size": "2752x1536",
      "ratio": "16:9",
      "success": true,
      "url": "https://...",
      "created": "2026-07-29 13:36:14",
      "local_file": "test_outputs/..."
    }
  ]
}
```

---

## 环境配置

### 方式 1: 环境变量

```bash
export SENSENOVA_API_KEY='your-api-key-here'
python scripts/generate_infographic.py --prompt "..."
```

### 方式 2: .env 文件

创建 `.env` 文件：

```bash
SENSENOVA_API_KEY=your-api-key-here
```

然后直接运行脚本：

```bash
python scripts/generate_infographic.py --prompt "..."
```

### 方式 3: 内联方式

```bash
SENSENOVA_API_KEY='your-key' python scripts/generate_infographic.py --prompt "..."
```

---

## 完整示例

### 示例 1: 生成单张信息图

```bash
# 1. 创建 prompt 文件
cat > my_prompt.txt << 'EOF'
这张信息图展示了"Python学习路线"。采用现代扁平设计风格，以蓝紫渐变为主色调。

整体布局分为三个阶段：

1. 初级阶段：
   - 基础语法
   - 数据类型
   - 控制流程

2. 中级阶段：
   - 面向对象
   - 常用库
   - 数据库操作

3. 高级阶段：
   - 框架开发
   - 性能优化
   - 项目实战
EOF

# 2. 生成信息图
python scripts/generate_infographic.py \
  --prompt-file my_prompt.txt \
  --size "2752x1536" \
  --output python_learning_path.png \
  --save-report

# 3. 查看结果
ls -lh python_learning_path.png
cat python_learning_path.json
```

### 示例 2: 批量测试

```bash
# 1. 运行批量测试
python scripts/test_all_sizes.py

# 2. 查看测试结果
ls -lh test_outputs/

# 3. 查看测试报告
cat test_outputs/test_report_*.json | jq '.results[] | {size, success}'
```

### 示例 3: 不同尺寸对比

```bash
# 生成多个尺寸进行对比
for size in "2752x1536" "2048x2048" "1664x2496"; do
  python scripts/generate_infographic.py \
    --prompt "AI技术栈对比图" \
    --size "$size" \
    --output "comparison_${size}.png"
done

# 查看所有生成的图片
ls -lh comparison_*.png
```

---

## 故障排查

### 问题 1: API Key 无效

**症状**：
```
❌ 错误: 未找到 SENSENOVA_API_KEY 环境变量
```

**解决方法**：
```bash
# 检查环境变量
echo $SENSENOVA_API_KEY

# 重新设置
export SENSENOVA_API_KEY='your-actual-key'

# 或创建 .env 文件
echo 'SENSENOVA_API_KEY=your-actual-key' > .env
```

### 问题 2: 请求超时

**症状**：
```
❌ 请求超时
```

**解决方法**：
- 检查网络连接
- 增加超时时间（修改脚本中的 `timeout=60` 参数）
- 稍后重试

### 问题 3: 图片下载失败

**症状**：
```
⚠️ 下载图片失败
```

**解决方法**：
- URL 可能已过期（1 小时限制）
- 检查本地磁盘空间
- 检查写入权限

### 问题 4: Prompt 过长

**症状**：
```
❌ 请求失败 (HTTP 400)
错误信息: prompt too long
```

**解决方法**：
- Prompt 最大 4096 tokens
- 精简描述内容
- 移除冗余文字

---

## 高级用法

### 1. 批量生成（多个 Prompt）

```bash
# 创建多个 prompt 文件
cat > prompts/prompt1.txt << EOF
第一张信息图的描述...
EOF

cat > prompts/prompt2.txt << EOF
第二张信息图的描述...
EOF

# 批量生成
for file in prompts/*.txt; do
  name=$(basename "$file" .txt)
  python scripts/generate_infographic.py \
    --prompt-file "$file" \
    --output "output/${name}.png"
done
```

### 2. 集成到 Python 项目

```python
import sys
sys.path.append('scripts')
from generate_infographic import generate_infographic

result = generate_infographic(
    prompt="AI技术发展历程",
    size="2752x1536",
    output="my_infographic.png",
    save_report=True
)

if result["success"]:
    print(f"生成成功: {result['file']}")
else:
    print(f"生成失败: {result['error']}")
```

### 3. 自动化工作流

```bash
#!/bin/bash
# auto_generate.sh

# 配置
PROMPT_DIR="prompts"
OUTPUT_DIR="outputs"
SIZE="2752x1536"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 批量生成
for prompt_file in "$PROMPT_DIR"/*.txt; do
  filename=$(basename "$prompt_file" .txt)
  echo "处理: $filename"
  
  python scripts/generate_infographic.py \
    --prompt-file "$prompt_file" \
    --size "$SIZE" \
    --output "$OUTPUT_DIR/${filename}.png" \
    --save-report
  
  if [ $? -eq 0 ]; then
    echo "✅ $filename 生成成功"
  else
    echo "❌ $filename 生成失败"
  fi
done

echo "全部完成！"
```

---

## 性能优化

### 1. 并发生成（谨慎使用）

```python
from concurrent.futures import ThreadPoolExecutor
import sys
sys.path.append('scripts')
from generate_infographic import generate_infographic

prompts = [
    "Prompt 1...",
    "Prompt 2...",
    "Prompt 3..."
]

def generate(prompt):
    return generate_infographic(prompt=prompt)

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(generate, prompts))
```

⚠️ 注意：请遵守 API 频率限制！

### 2. 缓存机制

```python
import hashlib
import os

def cached_generate(prompt, size="2752x1536"):
    # 生成缓存 key
    cache_key = hashlib.md5(f"{prompt}{size}".encode()).hexdigest()
    cache_file = f"cache/{cache_key}.png"
    
    # 检查缓存
    if os.path.exists(cache_file):
        return {"success": True, "file": cache_file, "cached": True}
    
    # 生成新图片
    result = generate_infographic(prompt=prompt, size=size, output=cache_file)
    return result
```

---

## 依赖要求

```bash
pip install requests
```

或使用 requirements.txt：

```txt
requests>=2.31.0
```

安装：
```bash
pip install -r requirements.txt
```
