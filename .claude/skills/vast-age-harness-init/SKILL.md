---
name: vast-age-harness-init
description: Use when initializing, repairing, or completing an Attractor-Guided Engineering (AGE) harness or AGE-style docs system in an existing project. Triggers include init AGE, setup AGE harness, apply AGE template, initialize harness, 初始化 harness, 建立文档体系, and 给项目加 harness.
allowed-tools: Read, Bash, Glob, Grep
---

# Vast AGE Harness Init

Install the complete AGE consumer scaffold from the reference template. The template installer and `install-age.manifest` are the only source of truth; this skill is a safe orchestration layer, not a second template implementation.

## Invariants

- Never hand-write substitutes for files owned by `install-age.manifest`.
- Never move, rename, delete, or reorganize existing project documents.
- Never install unrelated skill collections such as `mattpocock/skills`.
- Never overwrite an existing manifest destination. The upstream installer skips it and fills only missing files.
- Do not stop merely because `AGENTS.md` or `docs/context/` exists. A partial harness must be repaired incrementally.
- State the two non-manifest mutations before installation: `.env` may gain `MISSION_DRIVER_HOME`; `.gitignore` may gain `.env`, `_tmp/`, and `tmp/`.
- Do not claim that onboarding or project-specific verification is complete just because scaffold installation succeeded.

## Inputs

Resolve these values before running:

| Input | Rule |
|---|---|
| Target | Existing project root; ask only when it cannot be inferred; current upstream orchestration accepts only paths made of letters, numbers, `/`, `\`, `:`, `.`, `_`, and `-` |
| Project name | Explicit user value, otherwise target directory basename; allow only letters, numbers, spaces, `.`, `_`, `@`, `+`, `,`, and `-` |
| Template root | Trusted persistent checkout under the current workspace's `.ref-project/`; apply the same safe path character restriction as Target |
| Pi support | Off by default; enable only when the user asks for pi support |
| Smoke executor | `opencode` by default; `pi` only when explicitly selected, independent of whether pi skill files are installed |
| Pi model | Required when the smoke executor is `pi`; allow only letters, numbers, `/`, `:`, `.`, `_`, `@`, `+`, and `-` in the verified Pi-compatible ID |

Do not require a README. The installer can scaffold an empty existing directory.

The installed shim keeps using `<template-root>/tools/mission-driver/` through `MISSION_DRIVER_HOME`. The checkout is a runtime dependency, not disposable installation media. Do not default to `.working/`, `_sandbox/`, `/tmp`, or another path that cleanup will remove. If the user explicitly selects an ephemeral checkout, explain that dependency and require a persistent location before installation.

Do not execute an installer from an arbitrary user-provided checkout. A checkout outside the workspace's trusted `.ref-project/` boundary requires the user to establish its source and approve it explicitly; otherwise stop. Path character checks prevent shell injection but do not make code trustworthy.

## Workflow

### 1. Preflight

Read the template's `install-age.manifest` and verify:

- target exists and is a directory
- Node.js 18 or newer is available
- Bash is available for the installed `tools/mission-driver.sh`; native Windows without Git Bash, WSL, or equivalent is unsupported by the current upstream scaffold
- `<template-root>/install-age.manifest` exists
- `<template-root>/tools/install-age.mjs` exists
- `<template-root>/tools/mission-driver/src/main.js` exists
- every enabled manifest source exists; `pi-only` entries are enabled only for a pi install
- every manifest source and installer file resolves inside the trusted template root
- no existing manifest destination, destination parent component, `.env`, or `.gitignore` is a symbolic link; every resolved write path remains inside the target root
- target and template paths, project name, and Pi model match the safe character sets above; reject rather than interpolate shell metacharacters into commands
- project name is non-empty; the restricted character set also avoids JavaScript replacement tokens that the upstream installer does not preserve safely
- the computed relative `MISSION_DRIVER_HOME` contains only letters, numbers, `.`, `_`, `/`, and `-`; the upstream installer writes it unquoted into `.env`, so spaces or shell metacharacters are unsafe
- an existing `.env` is safe for the installer to append to: allow only blank lines, comments, and simple `NAME=value` lines whose values use letters, numbers, `.`, `_`, `/`, `:`, `@`, `%`, `+`, `,`, or `-`; reject command substitution, backticks, shell operators, whitespace-bearing values, quotes, expansions, or other shell syntax
- before smoke testing, `.env` contains no environment-control names such as `PATH`, `BASH_ENV`, `ENV`, `SHELLOPTS`, `NODE_OPTIONS`, `NODE_PATH`, `LD_PRELOAD`, or language/runtime loader variables; if it does, scaffold installation may proceed but smoke testing is blocked because the upstream shim sources the whole file
- an existing non-empty `.env` ends with a newline when it lacks `MISSION_DRIVER_HOME`; otherwise stop and ask the user to add the newline because the upstream installer would concatenate the new assignment onto the last value
- the chosen smoke executor is installed and configured; installing pi skill files does not automatically select pi as the executor
- when the executor is pi, a Pi-compatible model ID is known; do not reuse the scaffold's default OpenCode model ID because the engine does not translate model formats

The `.env` restriction is deliberate. The installed upstream shim uses Bash `source` on the whole file. If the target needs richer dotenv syntax, stop before smoke testing and report that upstream incompatibility rather than executing the file or rewriting user configuration.

Parse manifest destinations only to report conflicts and validate the result. Do not reproduce its copy logic. Report existing destinations as `will skip`, not as a reason to abort the whole install.

Before mutation, summarize:

- target and project name
- persistent template path and the fact that the target depends on it at runtime
- enabled manifest entry count
- existing destinations that the installer will preserve
- `.env` and `.gitignore` append behavior
- runtime prerequisites and selected executor
- guarantee that no existing docs will be moved or deleted

If the target contains an existing `AGENTS.md` or AGE owner docs, preserve them. The installer will add the missing scaffold around them.

### 2. Install From The Reference Template

Prefer the Node installer entry point so manifest copying behaves consistently across platforms that also provide Bash for the installed runtime shim:

```bash
node "<template-root>/tools/install-age.mjs" "<target>" "<project-name>"
```

For requested pi skill-file support:

```bash
node "<template-root>/tools/install-age.mjs" "<target>" "<project-name>" --pi
```

Run from any working directory. Quote every path. Do not clone another repository when a local reference checkout is available.

Treat all values as data, not shell fragments. Never accept embedded quotes, backticks, `$`, command substitutions, newlines, or shell operators and then interpolate them into these commands.

The installer is intentionally incremental:

- missing manifest files are copied
- existing manifest files are skipped without content comparison
- `.env` and `.gitignore` receive idempotent line additions
- runtime directories `docs/plans/{demo,onboarding}/` and `docs/logs/<year>/` are created

Re-running repairs missing files; it does not upgrade customized files. Template upgrades to existing files require a later manual diff and merge.

### 3. Validate The Installed Contract

After installation, fail the task if any enabled manifest destination is absent. Also verify:

- `AGENTS.md` and `docs/index.md` exist
- all six `docs/context/` files exist
- `docs/architecture/` exists
- `tools/mission-driver.sh` exists and is executable on Unix
- `.env.example` and `.env` contain `MISSION_DRIVER_HOME=`
- `missions/base.json`, `missions/demo.json`, and `missions/onboarding.json` parse as JSON
- `missions/onboarding.json` points to `docs/backlog/onboarding-roadmap.md` and `docs/plans/onboarding`
- `.opencode/skills/mission-driver/SKILL.md` exists
- pi destinations exist when pi support was requested
- `docs/plans/demo/`, `docs/plans/onboarding/`, and `docs/logs/<current-year>/` exist
- `.gitignore` contains at least one exact line for each of `.env`, `_tmp/`, and `tmp/`; report duplicates as optional cleanup, not installation failure
- newly copied fill-in Markdown has no `<project-name>` placeholder

Validate manifest destinations rather than hard-coding a second 88-file list. The manifest may evolve.

Before executing the installed shim, compare it byte-for-byte with the trusted manifest source `template/install/tools/mission-driver.sh`. If the target already contained a different shim, preserve it but do not run it; report `Scaffold installed` at most and require explicit human review. Apply the same trust rule to any executable that the smoke path would load.

Resolve the effective `MISSION_DRIVER_HOME` exactly as the shim will: a process environment value overrides the target `.env`. Its canonical path must equal `<template-root>/tools/mission-driver/` from this installation. If an exported or existing value points elsewhere, do not smoke test until the user resolves the conflict; otherwise the test would validate a different engine than the installed manifest.

### 4. Smoke Test The Harness

Run from the target project:

```bash
./tools/mission-driver.sh list
./tools/mission-driver.sh run demo
```

When the selected smoke executor is pi, run the equivalent explicit selection instead of the default demo command:

```bash
MISSION_DRIVER_EXEC=pi OPENCODE_MODEL="<pi-provider>/<pi-model>" ./tools/mission-driver.sh run demo
```

If the environment cannot run the external engine, report the exact failure and stop. Do not claim a working harness from file checks alone.

`list` validates the shim and persistent engine path. `run demo` additionally validates the explicitly selected external executor and may require credentials or model configuration; keep these as separate reported gates.

Do not automatically run onboarding unless the user requested full project personalization. Onboarding can invoke AI tools, inspect the whole codebase, take significant time, and modify owner docs.

When full personalization is requested:

1. Inspect `missions/base.json` and replace placeholder verification commands with commands proven from the target repository.
2. Run `./tools/mission-driver.sh run onboarding`.
3. Review the onboarding diff against the actual codebase before accepting it.
4. Run the real target-project verification commands.

Blank or placeholder verification commands block any `full green` claim.

### 5. Report Truthfully

Separate the result into:

- copied manifest files
- preserved existing files
- runtime files/directories added
- smoke-test result
- personalization status
- remaining manual work

Use one of these outcomes:

| Outcome | Meaning |
|---|---|
| Scaffold installed | Manifest contract and runtime directories validate |
| Harness smoke-tested | Installation validates and mission-driver demo passes |
| Project personalized | Onboarding reviewed and real project verification passes |
| Partial/blocked | State exactly which gate failed; never collapse this into success |

## Common Mistakes

| Mistake | Correct behavior |
|---|---|
| Treat six context files as a complete harness | Compare every enabled manifest destination and fill missing files |
| Create `docs/articles/` but omit `docs/architecture/` | Trust the manifest; consumer installs architecture and excludes template methodology articles |
| Generate shortened `AGENTS.md` or source-of-truth rules | Install the curated upstream files unchanged unless a destination already exists |
| Copy a third-party skill library into `.agents/skills/` and `docs/skills/` | Install only the AGE operator skill and AGE methodology files listed by the manifest |
| Reorganize changelogs, architecture docs, or user guides | Preserve all existing paths; migration is a separate, explicit task |
| Call file existence “full success” | Validate the manifest, then run `list` and `demo` |
| Say `template/START-HERE-after-copy.md` was installed | Do not assume it; the current manifest is authoritative |

## Reference

- AGE template: `https://github.com/entropy-cloud/attractor-guided-engineering-template`
- Consumer file contract: `<template-root>/install-age.manifest`
- Cross-platform installer: `<template-root>/tools/install-age.mjs`
- Installed maintenance guide: `<target>/docs/references/age-files-guide.md`
