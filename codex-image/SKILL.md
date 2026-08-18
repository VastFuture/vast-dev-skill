---
name: codex-image
description: "AI image generation via Codex CLI (ChatGPT Plus). Requires Codex.app (or codex.exe) installed and logged into a ChatGPT Plus account. Features: accurate text rendering, photorealistic quality."
allowed-tools: Bash(python3 *)
---

# Codex Image (via Codex CLI)

Image generation through Codex CLI + ChatGPT Plus subscription. **No API billing.**

> Prerequisite: Codex CLI installed and logged into ChatGPT Plus (`npm install -g @openai/codex` or `npx @openai/codex`).
> - macOS: Codex.app from codex.so
> - Windows: Codex.exe from codex.so
> - Linux: `npm install -g @openai/codex`, then `CODEX_BIN=$(which codex)` or `CODEX_BIN=$(npx which codex)`
> Note: Uses your existing ChatGPT Plus subscription limits (DALL-E 3 / GPT-4 message quotas apply).

## Usage

```bash
# Default (macOS)
python3 ~/.claude/skills/codex-image/generate.py "<prompt>" [size] [output_dir]

# Linux (override codex binary path)
CODEX_BIN=$(which codex) python3 ~/.claude/skills/codex-image/generate.py "<prompt>" [size] [output_dir]
```

| Argument | Description | Default |
|----------|-------------|---------|
| prompt | Image generation prompt | required |
| size | Dimensions | `1024x1024` |
| output_dir | Save location | current directory |

## Examples

```bash
# Square
python3 ~/.claude/skills/codex-image/generate.py "a orange cat sleeping on a sofa, sunlight streaming in"

# Landscape
python3 ~/.claude/skills/codex-image/generate.py "a futuristic city skyline at dusk" 1536x1024

# Portrait with output dir
python3 ~/.claude/skills/codex-image/generate.py "a japanese zen garden" 1024x1536 ~/Desktop
```

## How it works

Codex CLI routes through your ChatGPT subscription — no extra API costs, but it will consume your ChatGPT Plus message quota.

## Notes

- Large images (1536x1024 and above) may take 3-5 minutes to generate. When calling via Bash tool, set `timeout=300000` or higher to avoid premature termination.
- Linux: set `CODEX_BIN` environment variable if codex is not at the default `/Applications/Codex.app/Contents/Resources/codex` path. Verify with `which codex` first.
