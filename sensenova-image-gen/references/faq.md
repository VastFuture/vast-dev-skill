# FAQ - 常见问题

## 一般问题

### Q1: 如何获取 API Key？

**A**: 访问商汤 SenseNova 平台注册获取免费 API Key。

1. 访问：https://platform.sensenova.cn/console
2. 注册账号并登录
3. 进入控制台创建 API Key
4. 复制并保存你的 API Key

### Q2: API Key 是否免费？

**A**: 商汤 SenseNova 提供免费额度，具体额度和定价请查看官方平台。建议先用小批量测试，了解成本后再大规模使用。

### Q3: 生成一张图片需要多长时间？

**A**: 通常 6-8 秒，具体取决于：
- 网络状况
- Prompt 复杂度
- 图片尺寸
- API 服务负载

### Q4: 支持哪些图片格式？

**A**: 目前只支持 PNG 格式，8-bit RGB，无损压缩。

---

## API 使用问题

### Q5: 图片 URL 为什么会失效？

**A**: SenseNova U1 Fast 接口返回的是临时访问链接，**固定有效期 1 小时**。超时后链接直接失效，无法再次访问。

**解决方法**：
- 立即下载保存到本地
- 使用我们提供的脚本会自动下载

### Q6: Prompt 最大长度是多少？

**A**: 最大 4096 tokens（约 3000-4000 个中文字符）。

**如果超长怎么办**：
- 精简描述，保留核心要点
- 移除冗余的修饰词
- 分解成多张信息图

### Q7: 可以生成多张图片吗？

**A**: 可以，通过设置 `n` 参数：

```json
{
  "model": "sensenova-u1-fast",
  "prompt": "...",
  "n": 3
}
```

但建议 `n=1`，因为：
- 每次生成的图片会有差异
- 成本更可控
- 可以针对性调整 prompt

### Q8: 支持哪些尺寸？

**A**: 支持 11 种 aspect ratio，所有尺寸都是 2K 分辨率：

| 比例 | 尺寸 | 适用场景 |
|------|------|---------|
| 16:9 | 2752×1536 | 横屏演示 |
| 9:16 | 1536×2752 | 竖屏手机 |
| 1:1 | 2048×2048 | 社交媒体 |
| 3:2 | 2496×1664 | 标准横屏 |
| 2:3 | 1664×2496 | 标准竖屏 |
| 其他 | ... | 查看完整列表 |

### Q9: 生成的图片可以商用吗？

**A**: 请查阅商汤 SenseNova 的服务条款和版权协议。建议在商用前：
1. 仔细阅读平台用户协议
2. 咨询官方客服
3. 保留使用记录

---

## Prompt 编写问题

### Q10: 如何写出好的 Prompt？

**A**: 遵循以下原则：

1. **结构化描述**：使用明确的层级和区块划分
   ```
   整体布局分为三个部分：
   1. 左侧区域：...
   2. 中间区域：...
   3. 右侧区域：...
   ```

2. **具体化内容**：列出所有文字内容
   ```
   标题："AI 技术发展史"
   副标题："从1950年代到2020年代"
   ```

3. **视觉细节**：描述色彩、风格、图标
   ```
   采用扁平设计风格，以蓝色和绿色为主色调
   ```

4. **布局说明**：明确空间安排
   ```
   左栏占30%，中栏40%，右栏30%
   ```

### Q11: 生成的图片效果不理想怎么办？

**A**: 逐步优化 Prompt：

1. **增加细节**：补充更多视觉描述
2. **调整结构**：重新组织内容层次
3. **明确风格**：指定具体的设计风格
4. **参考示例**：查看 `references/prompt-examples.md`

### Q12: 可以参考现有图片生成吗？

**A**: 不可以。U1 Fast 不支持图像输入，只能通过文字 prompt 描述。

**替代方案**：
- 详细描述参考图片的布局、色彩、风格
- 使用文字精确表达视觉元素

---

## 技术问题

### Q13: 为什么总是请求超时？

**A**: 可能原因：
- 网络连接不稳定
- API 服务负载高
- Prompt 过于复杂

**解决方法**：
```python
# 增加超时时间
response = requests.post(url, headers=headers, json=payload, timeout=120)

# 添加重试逻辑
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3, backoff_factor=1)
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)
```

### Q14: 如何批量生成？

**A**: 使用循环或并发：

```python
# 串行（安全）
for prompt in prompts:
    result = generate_infographic(prompt=prompt)

# 并发（注意频率限制）
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=2) as executor:
    results = list(executor.map(generate_infographic, prompts))
```

⚠️ 注意遵守 API 频率限制！

### Q15: 可以集成到 Web 应用吗？

**A**: 可以，示例代码：

```python
from flask import Flask, request, jsonify
from generate_infographic import generate_infographic

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    prompt = data.get('prompt')
    size = data.get('size', '2752x1536')
    
    result = generate_infographic(prompt=prompt, size=size)
    
    if result['success']:
        return jsonify({
            'success': True,
            'file': result['file'],
            'url': f"/static/outputs/{result['file']}"
        })
    else:
        return jsonify({
            'success': False,
            'error': result['error']
        }), 400

if __name__ == '__main__':
    app.run()
```

### Q16: 如何处理并发请求？

**A**: 使用队列系统：

```python
from queue import Queue
from threading import Thread

task_queue = Queue()

def worker():
    while True:
        task = task_queue.get()
        if task is None:
            break
        generate_infographic(**task)
        task_queue.task_done()

# 启动工作线程
threads = [Thread(target=worker) for _ in range(2)]
for t in threads:
    t.start()

# 添加任务
for prompt in prompts:
    task_queue.put({'prompt': prompt})

# 等待完成
task_queue.join()
```

---

## 成本与限制问题

### Q17: 如何控制成本？

**A**: 建议措施：
1. 先用小批量测试
2. 缓存已生成的图片
3. 合并相似的 prompt
4. 监控 API 使用量
5. 设置每日配额上限

### Q18: 有频率限制吗？

**A**: 具体限制请查看官方文档。一般建议：
- 单次请求间隔 ≥ 1 秒
- 使用队列控制并发
- 实现指数退避重试

### Q19: 生成失败会扣费吗？

**A**: 这取决于商汤的计费策略。建议：
1. 查看官方计费说明
2. 监控账户余额
3. 实现完善的错误处理

---

## 错误处理问题

### Q20: 常见错误码及解决方法？

**A**: 

| 错误码 | 说明 | 解决方法 |
|-------|------|---------|
| 400 | 请求参数错误 | 检查 prompt、size、model 参数 |
| 401 | 认证失败 | 检查 API Key 是否正确 |
| 429 | 请求频率超限 | 降低请求频率，增加间隔 |
| 500 | 服务器错误 | 稍后重试，或联系技术支持 |

### Q21: 如何实现错误重试？

**A**: 示例代码：

```python
import time

def generate_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = generate_infographic(prompt=prompt)
            if result['success']:
                return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # 指数退避
            time.sleep(wait_time)
    
    return {'success': False, 'error': 'Max retries reached'}
```

---

## 其他问题

### Q22: 如何联系技术支持？

**A**: 
- 官方平台：https://platform.sensenova.cn/console
- 官方文档：https://platform.sensenova.cn/docs
- 工单系统：通过控制台提交工单

### Q23: 这个 Skill 是官方提供的吗？

**A**: 不是。这是基于商汤 SenseNova U1 Fast API 的第三方封装工具。

官方资源：
- API 接口：商汤提供
- 文档参考：官方文档
- Skill 封装：社区贡献

### Q24: 可以贡献代码或反馈问题吗？

**A**: 欢迎！你可以：
1. 提交 Issue 报告问题
2. 提交 PR 改进代码
3. 分享优秀的 Prompt 示例
4. 完善文档

### Q25: 未来会支持更多功能吗？

**A**: 计划中的功能：
- [ ] 模板库管理
- [ ] Prompt 优化建议
- [ ] 批量生成工作流
- [ ] Web UI 界面
- [ ] 图片质量评估

---

## 快速参考

### 获取帮助

```bash
# 查看脚本帮助
python scripts/generate_infographic.py --help

# 查看 API 文档
cat references/api-documentation.md

# 查看 Prompt 示例
cat references/prompt-examples.md
```

### 常用命令

```bash
# 生成单张图片
python scripts/generate_infographic.py --prompt "..." --size "2752x1536"

# 批量测试
python scripts/test_all_sizes.py

# 从文件读取
python scripts/generate_infographic.py --prompt-file prompt.txt
```

### 环境变量

```bash
# 设置 API Key
export SENSENOVA_API_KEY='your-key'

# 检查环境变量
echo $SENSENOVA_API_KEY
```

---

如果你的问题没有在这里找到答案，请：
1. 查看官方文档
2. 提交 Issue
3. 联系技术支持
