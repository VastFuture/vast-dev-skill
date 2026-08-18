# SenseNova U1 Fast Skill 安装记录

## 安装信息

- **安装时间**: 2026-07-29
- **Skill 版本**: 1.0.0
- **API 版本**: v1
- **模型**: sensenova-u1-fast

## 安装位置

### 1. 源代码仓库
```
/home/fenghaolin/workspace/prj/opensource/vast-dev-skill/sensenova-u1-fast/
```

### 2. 全局 Skills 目录
```
~/.agents/skills/sensenova-u1-fast/
```

### 3. 项目文档目录
```
/home/fenghaolin/workspace/prj/develop/openai/human-resources/ai-dev-log/human-resources/docs/skills/sensenova-u1-fast/
```

## 目录结构

```
sensenova-u1-fast/
├── SKILL.md                          # 主 Skill 文档
├── README.md                         # 项目说明
├── requirements.txt                  # Python 依赖
├── scripts/                          # 脚本目录
│   ├── generate_infographic.py      # 单张生成脚本
│   └── test_all_sizes.py            # 批量测试脚本
└── references/                       # 参考文档
    ├── api-documentation.md          # API 官方文档
    ├── prompt-examples.md            # Prompt 示例库
    ├── script-usage.md               # 脚本使用说明
    └── faq.md                        # 常见问题
```

## 快速验证

```bash
# 1. 进入 skill 目录
cd ~/.agents/skills/sensenova-u1-fast

# 2. 查看帮助
python scripts/generate_infographic.py --help

# 3. 测试生成（需要先设置 API Key）
export SENSENOVA_API_KEY='your-key'
python scripts/generate_infographic.py --prompt "测试信息图"
```

## 使用说明

### 触发关键词

当 AI 助手检测到以下关键词时会自动使用此 Skill：
- "生成信息图" / "infographic" / "信息可视化"
- "SenseNova" / "商汤" / "U1 Fast"
- "数据可视化" / "图表生成" / "视觉呈现"
- "画个信息图" / "做个信息图" / "设计信息图"

### 首次使用

1. 访问 https://platform.sensenova.cn/console 注册账号
2. 获取免费 API Key
3. 设置环境变量：`export SENSENOVA_API_KEY='your-key'`
4. 调用生成脚本

## 更新日志

### v1.0.0 (2026-07-29)
- ✅ 初始版本发布
- ✅ 支持 11 种尺寸比例
- ✅ 完整的 API 封装
- ✅ 详细的参考文档
- ✅ Prompt 示例库
- ✅ 批量测试功能
