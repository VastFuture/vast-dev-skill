# MageByte Power Skills — CLAUDE.md

This CLAUDE.md file serves as guidance for Claude Code in this repository. The repo contains reusable "Claude Code Superpowers" skills—battle-tested development workflows and methodologies.

**Key points:**
- Skills are stored in `skills/<skill-name>/` directories with a required SKILL.md entry point
- The distribution format uses `.skill` files (zip archives) in the `dist/` folder
- Skills can be installed via symlink to `~/.claude/skills/` for local development
- The repo currently includes one skill: `cross-verified-feature-development`, designed for high-risk feature development with 4-round cross-verification
- Creating new skills requires adding frontmatter (name and description) to a SKILL.md file