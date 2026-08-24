# Fix Docs Pipeline Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Repair the source `docs-pipeline` skill so its documented template contract, template assets, and tests agree.

**Architecture:** Treat `docs-pipeline/SKILL.md` as the public contract, `docs-pipeline/assets/templates/` as the asset set, and `docs-pipeline/scripts/` as the verification layer. The fix adds the missing assets, removes template-directory pollution, tightens documentation wording, and adds an automated reference checker so this class of drift fails loudly next time.

**Tech Stack:** Markdown skill documentation, shell scripts, Python 3 standard library, Git.

---

## Current Baseline

Source skill directory:

```text
/home/fenghaolin/workspace/prj/opensource/vast-dev-skill/docs-pipeline
```

Fresh audit evidence collected on 2026-08-24:

```text
template_refs_count 47
missing_refs_count 7
existing_refs_count 40
```

Missing source templates referenced by `docs-pipeline/SKILL.md`:

```text
assets/templates/architecture-README.md
assets/templates/logs-README.md
assets/templates/arch-nodejs.md
assets/templates/arch-python.md
assets/templates/arch-go.md
assets/templates/arch-rust.md
assets/templates/arch-generic.md
```

Pollution under `assets/templates/`:

```text
assets/templates/.omc/state/agent-replay-bc5a6a0f-eca4-4717-8a21-026666556874.jsonl
assets/templates/.omc/state/idle-notif-cooldown.json
assets/templates/.omc/state/last-tool-error.json
assets/templates/.omc/state/mission-state.json
assets/templates/.omc/state/subagent-tracking.json
```

Known documentation/test drift:

- `SKILL.md` says `docs/architecture/README.md` and `docs/logs/README.md` are generated, but the corresponding templates are absent.
- `SKILL.md` describes architecture fallback templates, but all five fallback templates are absent.
- `scripts/test-pipeline.sh` does not exercise the full standard contract.
- `scripts/test-pipeline.sh` copies `docs-agent-guides/*` into the test project root instead of `docs/agent-guides/`.
- `SKILL.md` has contradictory `docs/CLAUDE.md` guidance after saying the skill does not generate `docs/CLAUDE.md`.
- `SKILL.md` and `scripts/test-modes.sh` mix top-level directory counts with directory-node counts.
- `USAGE.md` uses both `docs/exec-plans/` and `plans/` for execution plans.

## Scope

### In Scope

- Add the seven missing template files under `docs-pipeline/assets/templates/`.
- Remove `docs-pipeline/assets/templates/.omc/` from the template asset tree.
- Add `docs-pipeline/scripts/check-template-refs.py` to verify template references and template hygiene.
- Update `docs-pipeline/scripts/test-pipeline.sh` to test the current standard `exec-plans` contract and `docs/agent-guides/` location.
- Update `docs-pipeline/scripts/test-modes.sh` wording and counts to use one directory-count convention.
- Update `docs-pipeline/SKILL.md` for clear directory counts, complete mkdir commands, no duplicate `design-README.md` mapping, and no `docs/CLAUDE.md` quick-start contradiction.
- Update `docs-pipeline/USAGE.md` to consistently use `docs/exec-plans/`.

### Out of Scope

- Do not change the canonical execution-plan directory from `docs/exec-plans/` to `docs/plans/`.
- Do not remove legacy `exec-plans-README.md` or `exec-plans-TEMPLATE.md` templates.
- Do not edit installed skill copies under `~/.claude/skills/` in this plan.
- Do not change unrelated skills in `vast-dev-skill/`.
- Do not commit unless the user explicitly asks for a commit after verification.

## File Structure

| Path | Responsibility |
|------|----------------|
| `docs-pipeline/assets/templates/architecture-README.md` | Template for generated `docs/architecture/README.md`. |
| `docs-pipeline/assets/templates/logs-README.md` | Template for generated `docs/logs/README.md`. |
| `docs-pipeline/assets/templates/arch-nodejs.md` | Fallback `ARCHITECTURE.md` template for Node.js projects. |
| `docs-pipeline/assets/templates/arch-python.md` | Fallback `ARCHITECTURE.md` template for Python projects. |
| `docs-pipeline/assets/templates/arch-go.md` | Fallback `ARCHITECTURE.md` template for Go projects. |
| `docs-pipeline/assets/templates/arch-rust.md` | Fallback `ARCHITECTURE.md` template for Rust projects. |
| `docs-pipeline/assets/templates/arch-generic.md` | Fallback `ARCHITECTURE.md` template when project type is unknown. |
| `docs-pipeline/assets/templates/.omc/` | Remove; runtime state does not belong in templates. |
| `docs-pipeline/scripts/check-template-refs.py` | Parse Markdown docs for `assets/templates/...` references and fail if referenced files are missing or `.omc/state` is present under templates. |
| `docs-pipeline/scripts/test-pipeline.sh` | Exercise a standard install with current directories and template destinations. |
| `docs-pipeline/scripts/test-modes.sh` | Verify minimal/standard directory modes and report counts consistently. |
| `docs-pipeline/SKILL.md` | Public skill contract; align wording, mappings, and counts with actual assets. |
| `docs-pipeline/USAGE.md` | User-facing examples; align plan path wording with `docs/exec-plans/`. |

## Task Route

| Item | Value |
|------|-------|
| Task type | Bug investigation + documentation/tooling fix |
| Owner docs read | `docs/index.md`, `docs/exec-plans/README.md` |
| Primary owner area | `docs-pipeline/` skill source |
| User-visible behavior | Future `/docs-pipeline` runs stop missing templates and reports cleaner structure |
| Risk level | Low to medium; changes are confined to one skill source directory |

## Task 1: Add template-reference consistency checker

**Files:**

- Create: `docs-pipeline/scripts/check-template-refs.py`

- [ ] **Step 1: Create the checker script**

Write this exact file:

```python
#!/usr/bin/env python3
"""Validate docs-pipeline template references and template tree hygiene."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = SKILL_DIR / "assets" / "templates"
DOC_FILES = [
    SKILL_DIR / "SKILL.md",
    SKILL_DIR / "README.md",
    SKILL_DIR / "USAGE.md",
    SKILL_DIR / "ADVANCED.md",
]
TEMPLATE_REF_RE = re.compile(r"`assets/templates/([^`]+)`")


def collect_refs() -> list[tuple[Path, str]]:
    refs: list[tuple[Path, str]] = []
    for doc in DOC_FILES:
        if not doc.exists():
            continue
        text = doc.read_text(encoding="utf-8")
        for ref in sorted(set(TEMPLATE_REF_RE.findall(text))):
            refs.append((doc, ref))
    return refs


def main() -> int:
    missing: list[tuple[Path, str]] = []
    for doc, ref in collect_refs():
        if not (TEMPLATES_DIR / ref).is_file():
            missing.append((doc, ref))

    polluted = sorted(TEMPLATES_DIR.glob(".omc/state/*"))

    if missing:
        print("Missing template references:")
        for doc, ref in missing:
            print(f"  {doc.relative_to(SKILL_DIR)} -> assets/templates/{ref}")

    if polluted:
        print("Runtime state files found under assets/templates:")
        for path in polluted:
            print(f"  {path.relative_to(SKILL_DIR)}")

    if missing or polluted:
        return 1

    print("Template reference check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run the checker before fixes to confirm it fails**

Run:

```bash
python3 docs-pipeline/scripts/check-template-refs.py
```

Expected: exit code `1`, listing the seven missing templates and `.omc/state` pollution.

## Task 2: Add missing docs directory templates

**Files:**

- Create: `docs-pipeline/assets/templates/architecture-README.md`
- Create: `docs-pipeline/assets/templates/logs-README.md`

- [ ] **Step 1: Create `architecture-README.md`**

Write this exact file:

```markdown
# Architecture / 架构基线

> 技术基线、模块边界、依赖方向和关键架构决策。

**AI 须知：**
- 架构变更前先读本目录
- 新增模块边界、跨服务调用、部署形态或核心数据流时更新本目录
- 不确定当前实现时，先从代码验证，不要凭印象补文档
- 检索本目录前先读此文件

---

## 当前状态

本目录用于沉淀稳定架构事实。初始化后如果还没有架构文档，先使用项目根 `ARCHITECTURE.md` 作为入口。

## 什么时候更新

- 新增或调整模块边界
- 新增外部集成或跨服务协议
- 修改部署方式、运行拓扑或关键配置
- 修改核心数据流、权限边界或持久化策略

## 索引

| 文件 | 主题 | 状态 |
|------|------|------|
| _（暂无）_ | | |
```

- [ ] **Step 2: Create `logs-README.md`**

Write this exact file:

```markdown
# Logs / 开发日志

> 开发过程中的事实记录、验证结果和阶段性上下文。

**AI 须知：**
- 记录事实，不写聊天摘要
- 重要验证结果、非显而易见的决策和阶段性交接写入本目录
- 时间敏感记录使用绝对日期
- 检索本目录前先读此文件

---

## 什么时候写日志

- 完成一个阶段性任务
- 验证结果会影响后续判断
- 发现非显而易见的问题
- 需要给后续 AI 或队友交接上下文

## 命名规范

使用 `YYYY-MM-DD-主题.md`。

## 索引

| 文件 | 主题 | 日期 |
|------|------|------|
| _（暂无）_ | | |
```

- [ ] **Step 3: Run the checker**

Run:

```bash
python3 docs-pipeline/scripts/check-template-refs.py
```

Expected: exit code `1`, with missing count reduced by two. The checker should still report the five `arch-*` files and `.omc/state` pollution.

## Task 3: Add architecture fallback templates

**Files:**

- Create: `docs-pipeline/assets/templates/arch-nodejs.md`
- Create: `docs-pipeline/assets/templates/arch-python.md`
- Create: `docs-pipeline/assets/templates/arch-go.md`
- Create: `docs-pipeline/assets/templates/arch-rust.md`
- Create: `docs-pipeline/assets/templates/arch-generic.md`

- [ ] **Step 1: Create `arch-nodejs.md`**

Write this exact file:

```markdown
# Architecture

> Generated from the Node.js fallback template because automated project exploration was skipped or unavailable.

## Project Type

Node.js / JavaScript / TypeScript project detected by `package.json`.

## Entry Points

- Application entry points should be confirmed from `package.json` scripts and source files.
- Common candidates include `src/index.*`, `src/main.*`, application framework entry files, or CLI binaries declared in `package.json`.

## Module Boundaries

Record each stable module here after reading the code:

| Module | Responsibility | Key Files |
|--------|----------------|-----------|
| _Unconfirmed_ | Confirm from source before relying on this architecture file. | |

## Build, Test, and Run

Confirm commands from `package.json` before use:

```bash
npm run build
npm test
npm start
```

## Update Rule

Replace this fallback with code-derived architecture notes before making non-trivial architecture changes.
```

- [ ] **Step 2: Create `arch-python.md`**

Write this exact file:

```markdown
# Architecture

> Generated from the Python fallback template because automated project exploration was skipped or unavailable.

## Project Type

Python project detected by `pyproject.toml` or `setup.py`.

## Entry Points

- Application entry points should be confirmed from packaging metadata, CLI definitions, or source files.
- Common candidates include `main.py`, package `__main__.py`, framework app objects, or console scripts.

## Module Boundaries

Record each stable module here after reading the code:

| Module | Responsibility | Key Files |
|--------|----------------|-----------|
| _Unconfirmed_ | Confirm from source before relying on this architecture file. | |

## Build, Test, and Run

Confirm commands from project metadata before use:

```bash
pytest
python main.py
```

## Update Rule

Replace this fallback with code-derived architecture notes before making non-trivial architecture changes.
```

- [ ] **Step 3: Create `arch-go.md`**

Write this exact file:

```markdown
# Architecture

> Generated from the Go fallback template because automated project exploration was skipped or unavailable.

## Project Type

Go project detected by `go.mod`.

## Entry Points

- Application entry points should be confirmed from `cmd/`, package `main`, and module layout.
- Common candidates include `cmd/<app>/main.go` or root `main.go`.

## Module Boundaries

Record each stable package here after reading the code:

| Package | Responsibility | Key Files |
|---------|----------------|-----------|
| _Unconfirmed_ | Confirm from source before relying on this architecture file. | |

## Build, Test, and Run

Confirm commands against the module before use:

```bash
go build ./...
go test ./...
go run .
```

## Update Rule

Replace this fallback with code-derived architecture notes before making non-trivial architecture changes.
```

- [ ] **Step 4: Create `arch-rust.md`**

Write this exact file:

```markdown
# Architecture

> Generated from the Rust fallback template because automated project exploration was skipped or unavailable.

## Project Type

Rust project detected by `Cargo.toml`.

## Entry Points

- Application entry points should be confirmed from Cargo targets and source files.
- Common candidates include `src/main.rs`, `src/lib.rs`, or binaries under `src/bin/`.

## Module Boundaries

Record each stable crate/module here after reading the code:

| Module | Responsibility | Key Files |
|--------|----------------|-----------|
| _Unconfirmed_ | Confirm from source before relying on this architecture file. | |

## Build, Test, and Run

Confirm commands against the crate/workspace before use:

```bash
cargo build
cargo test
cargo run
```

## Update Rule

Replace this fallback with code-derived architecture notes before making non-trivial architecture changes.
```

- [ ] **Step 5: Create `arch-generic.md`**

Write this exact file:

```markdown
# Architecture

> Generated from the generic fallback template because automated project exploration was skipped or unavailable and no known project marker was detected.

## Project Type

Unknown. Confirm the technology stack from repository files before relying on this architecture file.

## Entry Points

Record confirmed entry points after reading the code:

| Entry Point | Purpose | Evidence |
|-------------|---------|----------|
| _Unconfirmed_ | Confirm from source before relying on this architecture file. | |

## Module Boundaries

Record each stable module here after reading the code:

| Module | Responsibility | Key Files |
|--------|----------------|-----------|
| _Unconfirmed_ | Confirm from source before relying on this architecture file. | |

## Build, Test, and Run

No commands are assumed. Fill this section from project-owned docs or repository configuration.

## Update Rule

Replace this fallback with code-derived architecture notes before making non-trivial architecture changes.
```

- [ ] **Step 6: Run the checker**

Run:

```bash
python3 docs-pipeline/scripts/check-template-refs.py
```

Expected: exit code `1`, reporting only `.omc/state` pollution and no missing template references.

## Task 4: Remove template-directory pollution

**Files:**

- Delete: `docs-pipeline/assets/templates/.omc/`

- [ ] **Step 1: Confirm the polluted directory exists**

Run:

```bash
test -d docs-pipeline/assets/templates/.omc && find docs-pipeline/assets/templates/.omc -type f | sort
```

Expected output includes files under `docs-pipeline/assets/templates/.omc/state/`.

- [ ] **Step 2: Remove the polluted runtime-state directory**

Run:

```bash
rm -rf docs-pipeline/assets/templates/.omc
```

- [ ] **Step 3: Run the checker**

Run:

```bash
python3 docs-pipeline/scripts/check-template-refs.py
```

Expected:

```text
Template reference check passed.
```

## Task 5: Fix `SKILL.md` contract wording and mapping drift

**Files:**

- Modify: `docs-pipeline/SKILL.md`

- [ ] **Step 1: Update minimal and standard count wording**

Change the quick-start and mode table wording to this convention:

```markdown
# 标准模式（默认，14 个顶层目录 + 2 个 exec-plans 子目录）
/docs-pipeline

# 最小化模式（6 个顶层目录 + 2 个 exec-plans 子目录，适合小项目）
DOCS_PIPELINE_MODE=minimal /docs-pipeline
```

And update the table rows to:

```markdown
| **minimal**（最小化） | 个人项目、快速原型、初学者 | 6 个顶层目录 + 2 个 exec-plans 子目录 | 最低 |
| **standard**（标准，默认） | 大多数团队项目 | 14 个顶层目录 + 2 个 exec-plans 子目录 + 模板 | 中等 |
```

- [ ] **Step 2: Fix the mode directory comments**

Replace the comments above the mkdir commands with:

```bash
# Minimal 模式（6 个顶层目录 + 2 个 exec-plans 子目录）
```

and:

```bash
# Standard 模式（14 个顶层目录 + 2 个 exec-plans 子目录，默认）
```

- [ ] **Step 3: Make mkdir commands complete**

The minimal command must include exactly:

```bash
mkdir -p "$docs_root/context" "$docs_root/backlog" "$docs_root/prd" "$docs_root/exec-plans/active" "$docs_root/exec-plans/completed" "$docs_root/lessons" "$docs_root/agent-guides"
```

The standard command must include exactly:

```bash
mkdir -p "$docs_root/context" "$docs_root/backlog" "$docs_root/prd" "$docs_root/design" "$docs_root/exec-plans/active" "$docs_root/exec-plans/completed" "$docs_root/research" "$docs_root/issues" "$docs_root/handover" "$docs_root/ideas" "$docs_root/lessons" "$docs_root/agent-guides" "$docs_root/standards" "$docs_root/logs" "$docs_root/architecture"
```

- [ ] **Step 4: Fix design file count**

Replace:

```markdown
- docs/design/ (4 个文件：README + api + db + data-dict)
```

with:

```markdown
- docs/design/ (5 个文件：README + api + db + business-rule + data-dict)
```

- [ ] **Step 5: Remove duplicate `design-README.md` mapping**

Keep only this later grouped mapping:

```markdown
| `assets/templates/design-README.md` | `$docs_root/design/README.md` |
```

The earlier duplicate line near the first `prd-TEMPLATE.md` mapping should be removed.

- [ ] **Step 6: Fix `docs/CLAUDE.md` contradiction**

In the Mode B example, replace the documentation repository line:

```text
├── CLAUDE.md             # docs-pipeline 模板
```

with:

```text
├── docs/index.md         # docs-pipeline 路由中枢
```

In the final report, replace:

```markdown
💡 快速入门指南：docs/CLAUDE.md
```

with:

```markdown
💡 快速入门指南：docs/index.md
```

- [ ] **Step 7: Run the checker**

Run:

```bash
python3 docs-pipeline/scripts/check-template-refs.py
```

Expected:

```text
Template reference check passed.
```

## Task 6: Fix `USAGE.md` plan path wording

**Files:**

- Modify: `docs-pipeline/USAGE.md`

- [ ] **Step 1: Replace the stray `plans/` path**

Replace this line:

```text
  ├─ 执行计划 → plans/（>5文件或>200行触发）
```

with:

```text
  ├─ 执行计划 → exec-plans/（>5文件或>200行触发）
```

- [ ] **Step 2: Clarify root auxiliary-doc protection wording**

Replace this line:

```markdown
- ❌ 不要覆盖已有的 CLAUDE.md / AGENTS.md / MBTI_DEV_TRAPS.md / karpathy-guidelines.md / .mcp.json / ARCHITECTURE.md（用户可能已有定制版本）
```

with:

```markdown
- ❌ 不要覆盖已有的 CLAUDE.md / AGENTS.md / .mcp.json / ARCHITECTURE.md；辅助文档位于 docs/agent-guides/，如检测到项目根旧版辅助文档，仅提示迁移，不覆盖
```

- [ ] **Step 3: Verify no stray `plans/` execution-plan wording remains**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
text = Path('docs-pipeline/USAGE.md').read_text(encoding='utf-8')
for i, line in enumerate(text.splitlines(), 1):
    if '执行计划' in line and 'plans/' in line and 'exec-plans/' not in line:
        raise SystemExit(f'stray plans reference at line {i}: {line}')
print('USAGE execution-plan paths are consistent.')
PY
```

Expected:

```text
USAGE execution-plan paths are consistent.
```

## Task 7: Update pipeline test to exercise current standard contract

**Files:**

- Modify: `docs-pipeline/scripts/test-pipeline.sh`

- [ ] **Step 1: Update standard directory creation**

The test setup must create these directories:

```bash
mkdir -p "$DOCS_ROOT/context"
mkdir -p "$DOCS_ROOT/backlog"
mkdir -p "$DOCS_ROOT/prd"
mkdir -p "$DOCS_ROOT/design"
mkdir -p "$DOCS_ROOT/exec-plans/active"
mkdir -p "$DOCS_ROOT/exec-plans/completed"
mkdir -p "$DOCS_ROOT/ideas"
mkdir -p "$DOCS_ROOT/research"
mkdir -p "$DOCS_ROOT/handover"
mkdir -p "$DOCS_ROOT/issues"
mkdir -p "$DOCS_ROOT/lessons"
mkdir -p "$DOCS_ROOT/agent-guides"
mkdir -p "$DOCS_ROOT/standards"
mkdir -p "$DOCS_ROOT/logs"
mkdir -p "$DOCS_ROOT/architecture"
```

- [ ] **Step 2: Copy all standard docs templates**

The template copy block must include:

```bash
cp "$TEMPLATES_DIR/backlog-README.md" "$DOCS_ROOT/backlog/README.md"
cp "$TEMPLATES_DIR/prd-README.md" "$DOCS_ROOT/prd/README.md"
cp "$TEMPLATES_DIR/prd-TEMPLATE.md" "$DOCS_ROOT/prd/TEMPLATE.md"
cp "$TEMPLATES_DIR/design-README.md" "$DOCS_ROOT/design/README.md"
cp "$TEMPLATES_DIR/design-api.yaml" "$DOCS_ROOT/design/api.yaml"
cp "$TEMPLATES_DIR/design-db.md" "$DOCS_ROOT/design/db.md"
cp "$TEMPLATES_DIR/design-business-rule.md" "$DOCS_ROOT/design/business-rule.md"
cp "$TEMPLATES_DIR/design-data-dict.md" "$DOCS_ROOT/design/data-dict.md"
cp "$TEMPLATES_DIR/exec-plans-README.md" "$DOCS_ROOT/exec-plans/README.md"
cp "$TEMPLATES_DIR/exec-plans-TEMPLATE.md" "$DOCS_ROOT/exec-plans/TEMPLATE.md"
cp "$TEMPLATES_DIR/ideas-README.md" "$DOCS_ROOT/ideas/README.md"
cp "$TEMPLATES_DIR/research-README.md" "$DOCS_ROOT/research/README.md"
cp "$TEMPLATES_DIR/handover-README.md" "$DOCS_ROOT/handover/README.md"
cp "$TEMPLATES_DIR/handover-TEMPLATE.md" "$DOCS_ROOT/handover/TEMPLATE.md"
cp "$TEMPLATES_DIR/issues-README.md" "$DOCS_ROOT/issues/README.md"
cp "$TEMPLATES_DIR/issues-TEMPLATE.md" "$DOCS_ROOT/issues/TEMPLATE.md"
cp "$TEMPLATES_DIR/lessons-README.md" "$DOCS_ROOT/lessons/README.md"
cp "$TEMPLATES_DIR/logs-README.md" "$DOCS_ROOT/logs/README.md"
cp "$TEMPLATES_DIR/architecture-README.md" "$DOCS_ROOT/architecture/README.md"
cp "$TEMPLATES_DIR/standards-README.md" "$DOCS_ROOT/standards/README.md"
cp "$TEMPLATES_DIR/standards-layers.md" "$DOCS_ROOT/standards/layers.md"
cp "$TEMPLATES_DIR/standards-api.md" "$DOCS_ROOT/standards/api.md"
cp "$TEMPLATES_DIR/standards-db.md" "$DOCS_ROOT/standards/db.md"
cp "$TEMPLATES_DIR/standards-security.md" "$DOCS_ROOT/standards/security.md"
cp "$TEMPLATES_DIR/standards-naming.md" "$DOCS_ROOT/standards/naming.md"
```

- [ ] **Step 3: Copy agent guides to `docs/agent-guides/`**

Replace root-level guide copies with:

```bash
cp "$TEMPLATES_DIR/docs-agent-guides/MBTI_DEV_TRAPS.md" "$DOCS_ROOT/agent-guides/MBTI_DEV_TRAPS.md"
cp "$TEMPLATES_DIR/docs-agent-guides/karpathy-guidelines.md" "$DOCS_ROOT/agent-guides/karpathy-guidelines.md"
cp "$TEMPLATES_DIR/docs-agent-guides/output-modes.md" "$DOCS_ROOT/agent-guides/output-modes.md"
cp "$TEMPLATES_DIR/docs-agent-guides/engineering-rules.md" "$DOCS_ROOT/agent-guides/engineering-rules.md"
cp "$TEMPLATES_DIR/docs-agent-guides/plan-mode.md" "$DOCS_ROOT/agent-guides/plan-mode.md"
cp "$TEMPLATES_DIR/docs-agent-guides/requirement-confirmation.md" "$DOCS_ROOT/agent-guides/requirement-confirmation.md"
cp "$TEMPLATES_DIR/docs-agent-guides/content-organization.md" "$DOCS_ROOT/agent-guides/content-organization.md"
```

- [ ] **Step 4: Add explicit file existence checks**

Add this verification block after template copy:

```bash
REQUIRED_FILES=(
  "$DOCS_ROOT/index.md"
  "$DOCS_ROOT/context/project-context.md"
  "$DOCS_ROOT/context/ai-autonomy-policy.md"
  "$DOCS_ROOT/context/codebase-map.md"
  "$DOCS_ROOT/context/source-of-truth-and-precedence.md"
  "$DOCS_ROOT/backlog/README.md"
  "$DOCS_ROOT/prd/README.md"
  "$DOCS_ROOT/prd/TEMPLATE.md"
  "$DOCS_ROOT/design/README.md"
  "$DOCS_ROOT/design/api.yaml"
  "$DOCS_ROOT/design/db.md"
  "$DOCS_ROOT/design/business-rule.md"
  "$DOCS_ROOT/design/data-dict.md"
  "$DOCS_ROOT/exec-plans/README.md"
  "$DOCS_ROOT/exec-plans/TEMPLATE.md"
  "$DOCS_ROOT/ideas/README.md"
  "$DOCS_ROOT/research/README.md"
  "$DOCS_ROOT/handover/README.md"
  "$DOCS_ROOT/handover/TEMPLATE.md"
  "$DOCS_ROOT/issues/README.md"
  "$DOCS_ROOT/issues/TEMPLATE.md"
  "$DOCS_ROOT/lessons/README.md"
  "$DOCS_ROOT/logs/README.md"
  "$DOCS_ROOT/architecture/README.md"
  "$DOCS_ROOT/standards/README.md"
  "$DOCS_ROOT/standards/layers.md"
  "$DOCS_ROOT/standards/api.md"
  "$DOCS_ROOT/standards/db.md"
  "$DOCS_ROOT/standards/security.md"
  "$DOCS_ROOT/standards/naming.md"
  "$DOCS_ROOT/agent-guides/MBTI_DEV_TRAPS.md"
  "$DOCS_ROOT/agent-guides/karpathy-guidelines.md"
  "$DOCS_ROOT/agent-guides/output-modes.md"
  "$DOCS_ROOT/agent-guides/engineering-rules.md"
  "$DOCS_ROOT/agent-guides/plan-mode.md"
  "$DOCS_ROOT/agent-guides/requirement-confirmation.md"
  "$DOCS_ROOT/agent-guides/content-organization.md"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$file" ]; then
    echo "❌ 缺失文件: $file"
    exit 1
  fi
done
```

- [ ] **Step 5: Run the pipeline test**

Run:

```bash
bash docs-pipeline/scripts/test-pipeline.sh
```

Expected: exit code `0`, and output includes all required files.

## Task 8: Update mode test wording and expected counts

**Files:**

- Modify: `docs-pipeline/scripts/test-modes.sh`

- [ ] **Step 1: Keep the expected node counts**

Current expected counts are correct as directory nodes:

```bash
test_mode "minimal" 7
test_mode "standard" 16
```

If current `standard` is `15`, update it to `16` because standard includes 14 top-level docs directories plus `exec-plans/active` and `exec-plans/completed`.

- [ ] **Step 2: Fix the output wording**

Replace the summary with:

```bash
echo "目录数量对照:"
echo "  - minimal:  6 个顶层目录 + 2 个 exec-plans 子目录 = 7 个目录节点（exec-plans 本身也是顶层目录）"
echo "  - standard: 14 个顶层目录 + 2 个 exec-plans 子目录 = 16 个目录节点"
```

- [ ] **Step 3: Run mode test**

Run:

```bash
bash docs-pipeline/scripts/test-modes.sh
```

Expected:

```text
✅ 所有模式测试通过!
```

## Task 9: Final verification

**Files:**

- Verify: `docs-pipeline/`

- [ ] **Step 1: Run template reference check**

Run:

```bash
python3 docs-pipeline/scripts/check-template-refs.py
```

Expected:

```text
Template reference check passed.
```

- [ ] **Step 2: Run mode test**

Run:

```bash
bash docs-pipeline/scripts/test-modes.sh
```

Expected output includes:

```text
✅ 所有模式测试通过!
```

- [ ] **Step 3: Run pipeline test**

Run:

```bash
bash docs-pipeline/scripts/test-pipeline.sh
```

Expected output includes:

```text
✅ 测试完成!
```

- [ ] **Step 4: Verify no polluted template state remains**

Run:

```bash
test ! -e docs-pipeline/assets/templates/.omc && echo "template tree clean"
```

Expected:

```text
template tree clean
```

- [ ] **Step 5: Review Git diff**

Run:

```bash
git diff -- docs-pipeline
```

Expected: diff only touches the files listed in this plan.

## Implementation Notes

- Run all commands from repository root: `/home/fenghaolin/workspace/prj/opensource/vast-dev-skill`.
- Prefer exact file writes for new templates; avoid copying from the installed skill cache.
- Do not use `~/.claude/skills/docs-pipeline` as the source of truth.
- If `tree` is unavailable during `test-pipeline.sh`, the script already falls back to `find`; keep that behavior.
- If verification fails after three separate fix attempts, stop and re-check whether `SKILL.md` or the test scripts should be the contract. The intended contract for this plan is `SKILL.md` with `docs/exec-plans/`.

## Completion Gates

- [ ] All seven missing template files exist.
- [ ] `docs-pipeline/assets/templates/.omc/` is absent.
- [ ] `python3 docs-pipeline/scripts/check-template-refs.py` exits `0`.
- [ ] `bash docs-pipeline/scripts/test-modes.sh` exits `0`.
- [ ] `bash docs-pipeline/scripts/test-pipeline.sh` exits `0`.
- [ ] `SKILL.md`, `USAGE.md`, and scripts consistently refer to `docs/exec-plans/` as the execution-plan directory.
- [ ] No installed skill cache under `~/.claude/skills/` is modified by this source fix.
