# pm-product-describer

> https://github.com/zephyrwang6/pm-product-describer.git

六维产品描述法 —— 从六个维度帮助用户生成完整的产品描述，让 AI 能一次性输出高质量原型或代码。

## 六个维度

| 维度 | 核心问题 | 作用 |
|------|----------|------|
| 用户流程与场景 | 谁、在什么情况下、完成什么任务 | 决定功能优先级和页面结构 |
| 视觉设计 | 产品的整体观感和调性 | 一句话参照比百字描述更高效 |
| 界面设计 | 每个页面放什么、怎么排 | 从信息架构到组件选型 |
| 交互设计 | 动起来之后会发生什么 | 覆盖按钮五状态、列表五状态 |
| 数据逻辑 | 界面背后的数据从哪来、往哪去 | 决定 demo 能不能变成可交付产品 |
| 运营设计 | 上线后怎么转起来 | 增长引擎和变现路径 |

## 六个切入角度

| 角度 | 适合场景 |
|------|----------|
| 框架驱动（Top-Down） | 仪表盘、数据看板 |
| 组件驱动（Bottom-Up） | 效率工具、编辑器 |
| 用户旅程驱动（Journey-Driven） | 电商下单、注册引导、审批流 |
| 状态机驱动（State-Driven） | 工单、订单、审核后台 |
| 数据模型驱动（Data-Model-Driven） | CRM、ERP、后台管理系统 |
| 角色权限驱动（Role-Based） | 多角色 SaaS 平台 |

## 安装

将 `pm-product-describer` 文件夹复制到 `~/.claude/skills/` 目录下即可。

```bash
cp -r pm-product-describer ~/.claude/skills/
```

## 使用

在 Claude Code 中说"我想做一个产品"、"帮我描述一下这个产品"等即可触发。

## 文件结构

```
pm-product-describer/
├── SKILL.md                    # 主文件：四步工作流 + 六维提问模板 + 输出格式
└── references/
    └── approach-guide.md       # 六个切入角度参考 + 选择速查表
```

## License

MIT
