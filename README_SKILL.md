# Chinese Copywriting Guidelines Skill

中文文案排版规范检查与修复技能,基于 [sparanoid/chinese-copywriting-guidelines](https://github.com/sparanoid/chinese-copywriting-guidelines) 制作。

## 功能特性

- ✅ 检查中英文之间的空格问题
- ✅ 检查中文与数字之间的空格问题
- ✅ 检查数字与单位之间的空格问题
- ✅ 检查标点符号使用规范(全角/半角)
- ✅ 检查专有名词大小写(GitHub, JavaScript, macOS 等)
- ✅ 支持单个文案片段检查
- ✅ 支持 Markdown 文档修复
- ✅ 支持项目文档批量审查
- ✅ 按优先级(P0-P3)分类问题
- ✅ 提供详细的修复建议

## 安装

```bash
# 复制到全局技能目录
cp chinese-copywriting-guidelines.skill ~/.agents/skills/

# 解压
cd ~/.agents/skills
unzip chinese-copywriting-guidelines.skill
```

## 使用方式

### 1. 检查单个文案片段

```
帅哥,帮我检查这段文案的排版:
在GitHub上使用LLM进行开发,效率提升了50%!
```

### 2. 检查并修复文档

```
帅哥,检查并修复 test_copywriting.md 的中文排版问题
```

### 3. 批量审查项目文档

```
帅哥,审查 docs/ 目录下所有 markdown 文件的排版规范
```

## 检查规则

### 空格规则
- 中英文之间需要增加空格: `在 GitHub 上` ✅
- 中文与数字之间需要增加空格: `花了 5000 元` ✅
- 数字与单位之间需要增加空格: `10 Gbps` ✅
- 全角标点与其他字符之间不加空格: `好开心!` ✅

### 标点符号规则
- 不重复使用标点符号: `巴西队!` ✅ (不是 `!!!`)
- 中文使用全角标点: `,。!?` ✅
- 数字使用半角字符: `1000` ✅ (不是 `１０００`)
- 英文整句使用半角标点: `Stay hungry, stay foolish.` ✅

### 专有名词规则
- GitHub (不是 github/Github)
- JavaScript (不是 javascript/Javascript)
- macOS (不是 macos/MacOS)
- iPhone (不是 iphone/Iphone)
- Node.js (不是 nodejs/NodeJS)

## 输出格式

技能会按优先级分类问题:

```
## 排版问题报告

### P0 - 严重问题 (2处)
1. [第3行] 中英文之间缺少空格
   原文: `在GitHub上使用LLM`
   修复: `在 GitHub 上使用 LLM`

### P1 - 高优先级问题 (5处)
...

### 统计
- 总问题数: 12
- P0: 2, P1: 5, P2: 3, P3: 2
```

## 技能结构

```
chinese-copywriting-guidelines/
├── SKILL.md                        # 主工作流程
└── references/
    ├── spacing-rules.md           # 空格规则详解
    ├── punctuation-rules.md       # 标点符号规则详解
    └── proper-nouns.md            # 专有名词规则详解
```

## 例外情况

- inline code 与中文之间的空格是可选的
- 度数/百分比与数字之间不加空格: `90°`, `15%`
- 产品名称按官方格式: 豆瓣FM, 小米MIX
- 代码块、命令、URL 中不应用空格规则

## 参考资料

- [中文文案排版指北](https://github.com/sparanoid/chinese-copywriting-guidelines)
- [Guidelines for Using Capital Letters](https://www.thoughtco.com/guidelines-for-using-capital-letters-1691724)
- [全形和半形 - 维基百科](https://zh.wikipedia.org/wiki/%E5%85%A8%E5%BD%A2%E5%92%8C%E5%8D%8A%E5%BD%A2)

## 相关工具

- [pangu.js](https://github.com/vinta/pangu.js) - JavaScript
- [autocorrect](https://github.com/huacnlee/autocorrect) - Rust/CLI
- [autocorrect-vscode](https://marketplace.visualstudio.com/items?itemName=huacnlee.autocorrect) - VS Code 扩展

## License

MIT

---

制作时间: 2026-07-27
基于: sparanoid/chinese-copywriting-guidelines
制作工具: Skill Forge
