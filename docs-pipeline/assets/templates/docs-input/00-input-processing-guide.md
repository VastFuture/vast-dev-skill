# 原始输入处理指南

## 用途

本指南说明如何在原始素材变成需求之前处理它。

## 规则

当源材料仍然混合以下内容时，不要让 AI 直接从大型原始输入转编码：

- 业务目标
- UI 示例
- 实现猜测
- 缺失假设
- 半确定的范围

## 推荐流程

1. 将原始素材存入 `docs/input/`
2. 标记来源类型：PM 笔记、卡片集文档、原型、文章或混合来源
3. 将未解决的问题写入 `docs/discussions/`
4. 将综合结果写入 `docs/prd/`

## 来源分类

- `source-pm-*.md` — 产品经理笔记
- `source-prototype-*.md` — 原型解读
- `source-cardset-*.md` — 卡片集或结构化需求文档
- `source-article-*.md` — 外部文章或参考

## 文件头约定

放入此目录的每个输入文件**应该**以如下头部开头：

    status: new | supplement | supersedes <filename>
    processed: pending | partial | done

- `status` 描述文件与其他输入的关系：`new`（新）、`supplement`（补充）、`supersedes`（取代）
- `processed` 跟踪此输入是否已被消费：`pending`（未处理）、`partial`（部分）、`done`（完成）
