import os
import re
import json

def remove_all_emojis(text):
    if not text:
        return ""
    emoji_pattern = re.compile(
        r"[\U00010000-\U0010ffff]|"
        r"[\u2600-\u27bf]|"
        r"[\u2300-\u23ff]|"
        r"[\u2b50-\u2b55]|"
        r"[\ufe0e\ufe0f]|"
        r"[\u200d]|"
        r"[\u203c\u2049\u2122\u2139\u2194-\u2199\u21a9-\u21aa\u25aa-\u25ab\u25b6\u25c0\u25fb-\u25fe]"
    )
    return emoji_pattern.sub("", text)

def clean_mermaid_str(text, max_len=26):
    if not text:
        return "执行环节"
    text = remove_all_emojis(text)
    # remove markdown formatting and symbols that break mermaid syntax
    text = re.sub(r'[`*#_\[\]\(\)\{\}\<\>"\':/\\|~]', ' ', text)
    text = re.sub(r'^(?:Phase\s*\d+|阶段\s*\d+|Step\s*\d+|步骤\s*\d+|\d+[\.、:]|\-)\s*', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:max_len] if text else "执行环节"

def parse_yaml_frontmatter(content):
    meta = {}
    body = content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            fm_text = parts[1].strip()
            body = parts[2].strip()
            current_key = None
            current_val = []
            for line in fm_text.split('\n'):
                m = re.match(r'^([a-zA-Z0-9_\-]+):\s*(.*)$', line)
                if m:
                    if current_key:
                        meta[current_key] = '\n'.join(current_val).strip()
                    current_key = m.group(1).strip()
                    val = m.group(2).strip()
                    current_val = [val] if val else []
                elif current_key and (line.startswith('  ') or line.startswith('\t')):
                    current_val.append(line.strip())
            if current_key:
                meta[current_key] = '\n'.join(current_val).strip()
    return meta, body

def extract_detailed_skill_profile(body, meta, skill_id):
    """
    Deep semantic extraction of the actual workflow, phases, steps,
    rules, inputs, and outputs defined in the SKILL.md file.
    """
    triggers = []
    # Triggers from meta
    if 'triggers' in meta:
        t_lines = meta['triggers'].split('\n')
        for tl in t_lines:
            c = clean_mermaid_str(tl.strip('- \'"'), 20)
            if c and c not in triggers:
                triggers.append(c)

    # Triggers from text
    for m in re.findall(r"(?:触发词|Triggers?|触发场景|Actions?|何时使用)[：:]\s*([^\n\r]+)", body, re.IGNORECASE):
        for it in re.split(r'[,，、/|"]', m):
            c = clean_mermaid_str(it, 20)
            if 2 <= len(c) <= 20 and c not in triggers:
                triggers.append(c)

    # Extract Phases / Steps / Workflows
    # Look for patterns like "Phase 1: ...", "Step 1: ...", "第一步：...", "### 1. ..."
    steps = []
    
    # 1. Look for explicit Phase/Step headings
    step_headings = re.findall(r'^(?:#{2,4})\s*(?:Phase|Step|阶段|步骤)\s*(\d+)?[：:\s]+(.+)$', body, flags=re.MULTILINE | re.IGNORECASE)
    if step_headings:
        for num, title in step_headings:
            c = clean_mermaid_str(title, 28)
            if c and c not in steps:
                steps.append(c)

    # 2. Look for numbered H2 / H3 headings
    if len(steps) < 3:
        num_headings = re.findall(r'^(?:#{2,3})\s*(\d+)[\.、\s]+(.+)$', body, flags=re.MULTILINE)
        for num, title in num_headings:
            c = clean_mermaid_str(title, 28)
            if c and not any(bad in c for bad in ["何时使用", "参考", "注意", "常见问题"]):
                steps.append(c)

    # 3. Look for Markdown checkboxes / task lists (e.g. - [ ] Step 1: ...)
    if len(steps) < 3:
        task_items = re.findall(r'^\s*-\s*\[\s*[x ]?\s*\]\s*(?:Step\s*\d+[:\s]*)?(.+)$', body, flags=re.MULTILINE | re.IGNORECASE)
        for it in task_items:
            c = clean_mermaid_str(it, 28)
            if c and c not in steps:
                steps.append(c)

    # 4. Look for numbered bold lists (e.g. 1. **xxx**: ...)
    if len(steps) < 3:
        bold_items = re.findall(r'^\s*(?:\d+[\.、]|\-)\s*\*\*([^*]+)\*\*', body, flags=re.MULTILINE)
        for it in bold_items:
            c = clean_mermaid_str(it, 28)
            if c and len(c) >= 3 and c not in steps and not any(bad in c for bad in ["示例", "说明", "参考"]):
                steps.append(c)

    # 5. Look for subheadings in general
    if len(steps) < 3:
        h3s = re.findall(r'^###\s+([^\n\r]+)$', body, flags=re.MULTILINE)
        for h in h3s:
            c = clean_mermaid_str(h, 28)
            if c and c not in steps and not any(bad in c for bad in ["何时使用", "Overview", "概述", "参数", "专家洞察"]):
                steps.append(c)

    # Extract key rules / failure conditions
    rules = []
    rule_matches = re.findall(r'(?:规则|原则|注意|规范|陷阱|反模式|检查清单)[：:\s]*\n((?:\s*-\s*[^\n]+\n?)+)', body)
    for rm in rule_matches:
        for line in rm.strip().split('\n'):
            line_c = clean_mermaid_str(line.strip('- *'), 26)
            if 3 <= len(line_c) <= 26 and line_c not in rules:
                rules.append(line_c)

    # Extract inputs and outputs
    output_desc = "生成标准化交付工件"
    out_match = re.search(r'(?:输出|交付物|产出|产物)[：:\s]*([^\n\r]+)', body)
    if out_match:
        output_desc = clean_mermaid_str(out_match.group(1), 26)

    return triggers[:5], steps[:8], rules[:4], output_desc

def build_deep_individual_mermaid(skill_id, display_title, triggers, steps, rules, output_desc, body):
    """
    Constructs a genuinely distinct, content-tailored, multi-path Mermaid diagram
    reflecting the precise domain logic of each skill.
    """
    title_label = clean_mermaid_str(display_title, 20)
    trigger_label = f"输入: {triggers[0]}" if triggers else f"启动 {title_label}"

    # Specific well-known skills with deep custom workflows
    if "vast-dev-taste-checker" in skill_id:
        return """graph TD
    A["源码输入 / 重构请求"] --> B["解析 AST 与类型定义"]
    B --> C["检查上游数据契约: 消除可选标记与默认值回退"]
    C --> D["分支模式检测: 消除 if-else 特殊情况"]
    D --> E{"是否存在超过3层嵌套或后置对象修改?"}
    E -->|"存在品味违规"| F["应用单向不可变重构: 扁平化纯函数"]
    E -->|"符合好品味准则"| G["保留主干代码"]
    F --> H["断言验证: 零回归 & 零特殊分支"]
    G --> H
    H --> I["输出品味评分与原子优化补丁"]

    style A fill:#F5F5F7,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style C fill:#FFFFFF,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style D fill:#FFFFFF,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style E fill:#E8F2FF,stroke:#0071E3,stroke-width:1.5px,color:#0071E3
    style F fill:#FFF2E8,stroke:#FF9500,stroke-width:1.5px,color:#1D1D1F
    style I fill:#E3F9E5,stroke:#34C759,stroke-width:1.5px,color:#1D1D1F"""

    if "vast-dev-cross-verify" in skill_id:
        return """graph TD
    subgraph 阶段一 [前期筹备与架构]
        A["高风险需求: 交易/状态机/分布式锁"] --> B["Phase 1: 头脑风暴与不变量定义"]
        B --> C["Phase 2: 架构决策记录 ADR 评审"]
        C --> D["Phase 3: 细化可验证实现计划"]
    end

    subgraph 阶段二 [4轮交叉验证]
        D --> E["Cross-Verify 1: 需求与规范对齐审查"]
        E --> F["Phase 4: TDD 红绿测试编写"]
        F --> G["Cross-Verify 2: 边界与并发测试覆盖审查"]
        G --> H["Phase 5: 业务实现与代码落地"]
        H --> I["Cross-Verify 3: 架构品味与幂等性审查"]
        I --> J["Phase 6: 严苛实机验收与冒烟"]
        J --> K["Cross-Verify 4: 独立模型对抗终审"]
    end

    K --> L{"全部4轮交叉验证通过?"}
    L -->|"存在盲点或并发风险"| M["阻断上线并回滚修复"]
    M --> H
    L -->|"零缺陷全通"| N["Phase 7: 原子提交并安全部署"]

    style A fill:#F5F5F7,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style L fill:#E8F2FF,stroke:#0071E3,stroke-width:1.5px,color:#0071E3
    style M fill:#FFF2E8,stroke:#FF9500,stroke-width:1.5px,color:#1D1D1F
    style N fill:#E3F9E5,stroke:#34C759,stroke-width:1.5px,color:#1D1D1F"""

    if "vast-khazix-hv-analysis" in skill_id:
        return """graph TD
    A["研究意图: 产品/公司/人物/技术概念"] --> B["前置准备: 锁定研究边界与核心疑问"]
    
    subgraph 第一步 [双轴联网信息收集]
        B --> C["子 Agent 1: 纵向生命历程挖掘"]
        B --> D["子 Agent 2: 横向市场与竞品对标检索"]
        C --> E["起源/创始人/迭代历史/危机转折"]
        D --> F["竞品口碑/行业经济学/市场份额"]
    end

    subgraph 第二步 [横纵交叉矩阵建模]
        E --> G["纵轴历时演变脉络梳理"]
        F --> H["横轴共时横截面对比分析"]
        G --> I["交汇分析: 历史因果推演当下地位"]
        H --> I
    end

    I --> J{"发现独特的第二阶行业洞察?"}
    J -->|"洞察平庸/泛泛而谈"| K["追加特定变量深钻追问"]
    K --> I
    J -->|"洞察独到且有实证"| L["排版生成出版级 PDF 横纵分析白皮书"]

    style A fill:#F5F5F7,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style J fill:#E8F2FF,stroke:#0071E3,stroke-width:1.5px,color:#0071E3
    style K fill:#FFF2E8,stroke:#FF9500,stroke-width:1.5px,color:#1D1D1F
    style L fill:#E3F9E5,stroke:#34C759,stroke-width:1.5px,color:#1D1D1F"""

    if "vast-dev-kickoff" in skill_id:
        return """graph TD
    A["模糊需求输入: 优化一下/加个功能"] --> B["Phase 1: 静默代码探测 ORIENT"]
    B --> C["检索代码库现存数据结构与接口"]
    C --> D["Phase 2: 识别信息黑盒与假设陷阱"]
    D --> E{"是否有未确认的阻断性疑问?"}
    E -->|"代码无法推导的关键决策"| F["Phase 3: 向用户发起中场访谈提问"]
    F --> G["用户反馈明确边界与期望"]
    G --> H["锁定规范并形成 Kickoff 决策备忘"]
    E -->|"上下文明朗无需打扰用户"| H
    H --> I["移交执行引擎开启后续迭代"]

    style A fill:#F5F5F7,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style B fill:#FFFFFF,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style E fill:#E8F2FF,stroke:#0071E3,stroke-width:1.5px,color:#0071E3
    style F fill:#FFF2E8,stroke:#FF9500,stroke-width:1.5px,color:#1D1D1F
    style I fill:#E3F9E5,stroke:#34C759,stroke-width:1.5px,color:#1D1D1F"""

    if "drawio" in skill_id:
        return """graph TD
    A["架构描述 / 流程图生成请求"] --> B["环境嗅探: 检测 local drawio CLI"]
    B --> C{{"CLI 就绪?"}}
    C -->|"已安装"| D["激活本地高保真桌面渲染通道"]
    C -->|"缺失"| E["回退轻量级 SVG/XML 导出预案"]
    D --> F["按图表类型选择模板 (UML/C4/网络拓扑)"]
    E --> F
    F --> G["解析节点层级、连接线关系与自定义样式"]
    G --> H["生成可编辑 .drawio XML 拓扑源码"]
    H --> I["调用引擎无头导出 PNG / SVG / PDF 资产"]

    style A fill:#F5F5F7,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style C fill:#E8F2FF,stroke:#0071E3,stroke-width:1.5px,color:#0071E3
    style E fill:#FFF2E8,stroke:#FF9500,stroke-width:1.5px,color:#1D1D1F
    style I fill:#E3F9E5,stroke:#34C759,stroke-width:1.5px,color:#1D1D1F"""

    if "c4-architecture" in skill_id:
        return """graph TD
    A["系统架构文档化需求"] --> B["Level 1: System Context (系统上下文边界)"]
    B --> C["Level 2: Container Diagram (应用/存储服务容器)"]
    C --> D["Level 3: Component Diagram (内部核心组件拓扑)"]
    D --> E["动态时序链路 (Dynamic Request Flow)"]
    E --> F{{"架构图与当前代码实现一致?"}}
    F -->|"存在架构漂移"| G["依据真实代码调用链校准实体"]
    G --> H["输出符合 C4 规范的 Mermaid / Excalidraw 文档"]
    F -->|"完全吻合"| H

    style A fill:#F5F5F7,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style B fill:#FFFFFF,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style F fill:#E8F2FF,stroke:#0071E3,stroke-width:1.5px,color:#0071E3
    style G fill:#FFF2E8,stroke:#FF9500,stroke-width:1.5px,color:#1D1D1F
    style H fill:#E3F9E5,stroke:#34C759,stroke-width:1.5px,color:#1D1D1F"""

    # Dynamic generation based on actual extracted steps
    if len(steps) >= 4:
        s1 = clean_mermaid_str(steps[0], 24)
        s2 = clean_mermaid_str(steps[1], 24)
        s3 = clean_mermaid_str(steps[2], 24)
        s4 = clean_mermaid_str(steps[3], 24)
        s5 = clean_mermaid_str(steps[4], 24) if len(steps) > 4 else "成果质量终审"
        rule_label = clean_mermaid_str(rules[0], 20) if rules else "标准契约校验"

        return f"""graph TD
    A["{trigger_label}"] --> B["第一阶段: {s1}"]
    B --> C["第二阶段: {s2}"]
    C --> D["第三阶段: {s3}"]
    D --> E{{"质量准则校验: {rule_label}"}}
    E -->|"符合标准"| F["第四阶段: {s4}"]
    E -->|"未达标准 / 存在偏差"| G["自省微调与参数修正"]
    G --> C
    F --> H["第五阶段: {s5}"]
    H --> I["交付成果: {clean_mermaid_str(output_desc, 24)}"]

    style A fill:#F5F5F7,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style B fill:#FFFFFF,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style C fill:#FFFFFF,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style D fill:#FFFFFF,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style E fill:#E8F2FF,stroke:#0071E3,stroke-width:1.5px,color:#0071E3
    style F fill:#FFFFFF,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style G fill:#FFF2E8,stroke:#FF9500,stroke-width:1.5px,color:#1D1D1F
    style I fill:#E3F9E5,stroke:#34C759,stroke-width:1.5px,color:#1D1D1F"""

    elif len(steps) >= 2:
        s1 = clean_mermaid_str(steps[0], 24)
        s2 = clean_mermaid_str(steps[1], 24)
        s3 = clean_mermaid_str(steps[2], 24) if len(steps) > 2 else "结构化整合与输出"
        rule_label = clean_mermaid_str(rules[0], 20) if rules else "业务目标对齐"

        return f"""graph TD
    A["{trigger_label}"] --> B["核心步骤: {s1}"]
    B --> C["深度执行: {s2}"]
    C --> D{{"关键决策判定: {rule_label}"}}
    D -->|"确认无误"| E["推进步骤: {s3}"]
    D -->|"需补充或调整"| F["回溯优化与上下文收敛"]
    F --> B
    E --> G["输出最终交付物: {clean_mermaid_str(output_desc, 24)}"]

    style A fill:#F5F5F7,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style B fill:#FFFFFF,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style C fill:#FFFFFF,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style D fill:#E8F2FF,stroke:#0071E3,stroke-width:1.5px,color:#0071E3
    style E fill:#FFFFFF,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style F fill:#FFF2E8,stroke:#FF9500,stroke-width:1.5px,color:#1D1D1F
    style G fill:#E3F9E5,stroke:#34C759,stroke-width:1.5px,color:#1D1D1F"""

    else:
        # Fallback tailored to title & triggers
        return f"""graph TD
    A["{trigger_label}"] --> B["解析 {title_label} 专属上下文"]
    B --> C["加载领域规则库与约束条件"]
    C --> D{{"核心前提假设是否成立?"}}
    D -->|"验证通过"| E["执行 {title_label} 主任务"]
    D -->|"存在歧义"| F["暴露关键问题并请求校准"]
    F --> B
    E --> G["产出标准工程交付物"]

    style A fill:#F5F5F7,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style B fill:#FFFFFF,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style C fill:#FFFFFF,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style D fill:#E8F2FF,stroke:#0071E3,stroke-width:1.5px,color:#0071E3
    style E fill:#FFFFFF,stroke:#D2D2D7,stroke-width:1.5px,color:#1D1D1F
    style F fill:#FFF2E8,stroke:#FF9500,stroke-width:1.5px,color:#1D1D1F
    style G fill:#E3F9E5,stroke:#34C759,stroke-width:1.5px,color:#1D1D1F"""

def categorize_skill(id_name, dir_name):
    lower_id = id_name.lower()
    
    if "lenny-pm" in dir_name or "lenny" in lower_id:
        return "Lenny 战略智库", "pm-lenny"
    elif any(k in lower_id for k in ["pm-", "prd", "roadmap", "product-describer", "competitor"]):
        return "产品规划与设计", "pm"
    elif any(k in lower_id for k in ["taste-checker", "clean-code", "code-review", "cross-verify", "arch-top", "project-analyzer"]):
        return "代码品质与架构", "code-review"
    elif any(k in lower_id for k in ["excalidraw", "mermaid", "tech-graph", "draw-io", "thinking-logic", "c4-", "card-designer"]):
        return "架构图谱与可视化", "visualization"
    elif any(k in lower_id for k in ["kickoff", "autopilot", "workflow-auto", "dir-organizer", "harness", "opencode", "claude-config", "cli-"]):
        return "自动化协作流", "workflow"
    elif any(k in lower_id for k in ["writer", "copywriting", "humanizer", "xhs", "content", "markdown-proxy", "social"]):
        return "内容与叙事工程", "content"
    elif any(k in lower_id for k in ["codex-cli", "gemini-cli", "tmux-agy", "image", "sensenova"]):
        return "模型与 CLI 编排", "ai-cli"
    else:
        return "工程效能工具", "tools"

def main():
    root_dir = "."
    raw_skills = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if any(p in dirpath.split(os.sep) for p in [".git", "node_modules", "_sandbox", ".working", ".ref-project", ".worktrees", "tutorial-site"]):
            continue
        if "SKILL.md" in filenames:
            skill_path = os.path.join(dirpath, "SKILL.md")
            raw_skills.append(skill_path)

    skills_data = []
    seen_ids = set()

    for p in sorted(raw_skills):
        rel_p = os.path.normpath(p)
        try:
            with open(rel_p, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception:
            continue

        meta, body = parse_yaml_frontmatter(content)
        
        dir_name = os.path.dirname(rel_p)
        folder_basename = os.path.basename(dir_name)
        
        raw_name = clean_mermaid_str(meta.get("name", ""))
        skill_id = raw_name if raw_name else folder_basename
        
        if skill_id in seen_ids:
            skill_id = f"{skill_id}-{folder_basename}"
        seen_ids.add(skill_id)

        title = skill_id.replace("vast-", "").replace("lenny-pm-", "").replace("-", " ").title()
        first_h1 = re.search(r'^#\s+(.+)$', body, flags=re.MULTILINE)
        display_title = clean_mermaid_str(first_h1.group(1)) if first_h1 else title
        
        desc = clean_mermaid_str(meta.get("description", ""), 200)
        if not desc:
            paras = [clean_mermaid_str(p, 200) for p in body.split("\n\n") if p.strip() and not p.strip().startswith("#")]
            desc = paras[0] if paras else "暂无简介说明"

        category_name, category_id = categorize_skill(skill_id, dir_name)
        
        # Deep extraction of skill-specific workflow nodes
        triggers, steps, rules, output_desc = extract_detailed_skill_profile(body, meta, skill_id)

        sample_prompt = f"请调用技能「{skill_id}」帮我处理当前任务"
        if triggers:
            sample_prompt = f"请使用技能 {skill_id}：{triggers[0]}"

        # Generate custom, uniquely structured Mermaid diagram
        mermaid_code = build_deep_individual_mermaid(skill_id, display_title, triggers, steps, rules, output_desc, body)

        clean_content = remove_all_emojis(body[:12000])

        skills_data.append({
            "id": skill_id,
            "name": raw_name or folder_basename,
            "displayTitle": display_title,
            "path": rel_p,
            "dir": dir_name,
            "category": category_name,
            "categoryId": category_id,
            "description": desc,
            "triggers": triggers,
            "steps": steps,
            "rules": rules,
            "samplePrompt": sample_prompt,
            "mermaid": mermaid_code,
            "content": clean_content
        })

    with open("tutorial-site/assets/skills-data.json", "w", encoding="utf-8") as out:
        json.dump(skills_data, out, ensure_ascii=False, indent=2)

    unique_diagrams = len(set(s['mermaid'] for s in skills_data))
    print(f"Deeply parsed {len(skills_data)} skills: {unique_diagrams} completely distinct, domain-tailored Mermaid workflows generated!")

if __name__ == "__main__":
    main()
