# MageByte Power Skills

A Claude Code Superpowers extension library offering a **7-phase workflow** with **4 rounds of independent AI cross-verification** for high-risk features like payments, state machines, and distributed systems.

**Core insight**: Traditional code review suffers from "context pollution" — all reviewers share the same assumptions. This workflow counteracts it through cold-context reviews where AI reviewers see only code, no design docs.

**Key features**:
- Native support for Claude Code, Codex CLI, OpenClaw (symlink to `~/.agents/skills/`)
- Phase 4.2 "cold context review" (no design doc access) is highest value step
- Exit criteria per phase; fallback modes without Superpowers MCP

**Cost vs benefit**: +40–50% time, but critical bug detection jumps from ~40% to ~95%.

Quote (124 chars): "你给的信息越多，reviewer 就越难发现你信念系统里的漏洞。"