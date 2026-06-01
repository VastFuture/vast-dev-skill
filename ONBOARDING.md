# vast-dev-skill Onboarding Guide

> A skill library for AI agents (Claude Code / Gemini CLI) covering the full development lifecycle.

---

## What Is This?

vast-dev-skill is a collection of AI agent skills for software development and office automation. Each skill is a self-contained prompt + instruction package that agents can invoke to handle specific tasks — from requirements analysis and architecture design to code review and visual generation.

The project targets developers who want to extend their AI coding assistant's capabilities. Skills are installed by copying their directory into the agent's skills folder.

---

## Developer Experience

Install a skill by copying its directory:

```bash
# Example: install the kickoff skill
cp -r ~/vast-dev-skill/vast-dev-kickoff ~/.claude/skills/
```

Invoke skills during a session using the agent's skill invocation command (e.g., `/kickoff` in Claude Code). The skill system then loads the skill's `SKILL.md` and executes its workflow.

Common usage patterns:

```
1. Clarify intent:  /brainstorming  ->  /arch-top
2. Define scope:    /kickoff  ->  /office-hours  ->  /pm-prd-writer
3. Execute:        /kickoff-pua  (plan, execute, review, commit loop)
4. Visualize:      /draw-tech-graph  (generate architecture diagrams)
```

---

## How Is It Organized?

```
vast-dev-skill/
├── AGENTS.md               # Agent conventions (this file augments README)
├── README.md               # Project overview and skill catalog
├── vast-dev-kickoff/       # Requirement gathering before coding
├── vast-dev-kickoff-pua/   # Full development loop with pressure escalation
├── vast-dev-brainstorming/ # Pre-creative exploration of intent
├── vast-dev-arch-top/      # Five-layer project constitution
├── vast-pm-prd-writer/     # PRD generation from raw requirements
├── vast-draw-tech-graph/   # SVG architecture diagram generation
├── vast-code-review-expert/ # SOLID/security code review
├── vast-agent-skill-reviewer/ # Skill implementation review
├── ... (40+ more skills)
```

| Category | Skills | What They Do |
|----------|--------|--------------|
| **Development Workflow** | `vast-dev-kickoff*`, `vast-dev-brainstorming`, `vast-dev-arch-top` | Plan and structure projects before and during coding |
| **Product Management** | `vast-pm-prd-writer`, `vast-pm-roadmap-planner` | Convert requirements into structured documents |
| **Visualization** | `vast-draw-tech-graph`, `vast-draw-mermaid` | Generate diagrams and visual content |
| **Code Quality** | `vast-code-review-expert`, `vast-pragmatic-clean-code-reviewer` | Review code for issues and style violations |
| **Content Processing** | `vast-markdown-proxy`, `vast-md-translator` | Fetch, translate, and summarize content |

Each skill directory contains a `SKILL.md` file that defines the skill's instructions, execution flow, and entry conditions.

---

## Key Concepts and Abstractions

| Concept | What It Means Here |
|---------|---------------------|
| **Skill** | A directory with `SKILL.md` + optional scripts/tools. Invoked by the agent to handle a specific task type |
| **SKILL.md** | The skill's definition file — instructions, workflow steps, and entry conditions |
| **vast-dev-kickoff** | Interview-based requirement gathering to avoid blind coding |
| **vast-dev-kickoff-pua** | Full development loop: plan → execute → review → verify → commit, with failure escalation |
| **vast-pm-prd-writer** | Converts fragmented raw requirements into评审-ready PRD documents |
| **vast-draw-tech-graph** | Generates production-ready SVG architecture diagrams in 7 professional styles |

---

## Primary Flows

```
User identifies a gap or need
  |
  v
Selects or installs a skill
  (copies skill directory to agent's skill folder)
  |
  v
Invokes skill during agent session
  (e.g., /kickoff, /draw-tech-graph)
  |
  v
Skill loads its SKILL.md
  and guides the agent through the workflow
  |
  v
Agent produces output
  (document, diagram, code, review, etc.)
```

For code review:

```
Code change submitted
  |
  v
vast-code-review-expert or vast-pragmatic-clean-code-reviewer invoked
  |
  v
Skill scans diff for SOLID violations, security risks, style issues
  |
  v
Returns structured findings with file:line references
```

---

## Developer Guide

### Setup

Skills are framework-agnostic — they work with any agent that supports external skills. Installation is copy-based:

```bash
git clone https://github.com/0x43f96f/vast-dev-skill.git ~/vast-dev-skill
cp -r ~/vast-dev-skill/vast-dev-kickoff ~/.claude/skills/
```

Some skills require environment variables or local tools. Check each skill's `SKILL.md` before use.

### Adding a New Skill

1. Create a directory under the project root: `vast-my-new-skill/`
2. Add `SKILL.md` — the skill definition with instructions and entry conditions
3. Add the skill to the appropriate category table in `README.md`

### Reference

- **AGENTS.md** — Project conventions for agents (you are reading its companion now)
- **README.md** — Full skill catalog with descriptions
- Individual skill `SKILL.md` files — Detailed usage instructions per skill