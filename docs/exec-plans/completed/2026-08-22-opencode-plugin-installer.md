# OpenCode Plugin Installer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a user-confirmed, configuration-driven installer to `vast-opencode-plugin-recommender` while preserving existing OpenCode configuration.

**Architecture:** `SKILL.md` owns conversation flow and confirmation. A dependency-free Node.js script owns deterministic discovery, secret-safe preview, stale-plan detection, atomic replacement, duplicate detection, runtime validation, and concurrency-aware rollback. OpenCode remains responsible for downloading npm plugins after restart.

**Tech Stack:** Node.js ESM, `node:test`, JSON, OpenCode CLI.

---

### Task 1: Lock the installer contract with tests

**Files:**
- Create: `vast-opencode-plugin-recommender/scripts/install-plugin.test.mjs`
- Create: `vast-opencode-plugin-recommender/scripts/install-plugin.mjs`

- [x] Write failing tests that use cleaned temporary HOME and Git repositories for preview, new global config, existing project config, idempotency, JSONC refusal, cross-scope duplicate warning, tuple conflict, stale digest, secret-safe output, and validation rollback.
- [x] Add the minimal module exports and CLI JSON envelope so the tests run and fail on behavior rather than imports.
- [x] Run `node --test vast-opencode-plugin-recommender/scripts/install-plugin.test.mjs` and confirm the behavioral tests fail.

### Task 2: Implement safe preview and application

**Files:**
- Modify: `vast-opencode-plugin-recommender/scripts/install-plugin.mjs`
- Test: `vast-opencode-plugin-recommender/scripts/install-plugin.test.mjs`

- [x] Implement built-in-first plugin lookup from built-in and user recommendation files without executing `installCommand`.
- [x] Implement root-only global/project config discovery and reject JSONC or ambiguous root candidates.
- [x] Parse string and tuple plugin entries, detect exact matches and incompatible versions/options, and block similarly named local plugin files.
- [x] Emit secret-safe preview JSON with `schemaVersion`, `status`, `changed`, `targetPath`, `beforeSha256`, `expectedChange`, `warnings`, and `conflicts`.
- [x] Require `--expect-sha256` for `--apply`, reject stale plans, replace atomically, and use the written digest for concurrency-aware rollback.
- [x] Validate exact `packageSpec` with an injectable `OPENCODE_PURE=1 opencode debug config` while never exposing captured output.
- [x] Run the Node test suite until all cases pass.

### Task 3: Make recommendation records installable

**Files:**
- Modify: `vast-opencode-plugin-recommender/plugin-builtin.json`
- Modify: `vast-opencode-plugin-recommender/scripts/install-plugin.test.mjs`

- [x] Add `packageSpec`, `installStrategy`, and `supportedScopes` to the auto-installable `cc-adapter-v2` and `opencode-wecom-ping` records; keep `ralph-loop` manual-only while npm `latest` is stale.
- [x] Keep `https://github.com/VastFuture/opencode-cc-adapter` as the canonical URL for `cc-adapter-v2`.
- [x] Replace legacy global npm commands; point `ralph-loop` to repository manual instructions.
- [x] Add tests proving all auto-installable built-ins pass metadata validation and `cc-adapter-v2` resolves by ID and name.

### Task 4: Update the skill workflow and human documentation

**Files:**
- Modify: `vast-opencode-plugin-recommender/SKILL.md`
- Modify: `vast-opencode-plugin-recommender/README.md`

- [x] Add OpenCode-specific install triggers, the every-time scope question, preview/confirmation/apply protocol, cancellation rules, restart requirement, and safe handling of environment variable names.
- [x] Extend add/update flows with optional validated installation metadata and duplicate-name rejection; never infer metadata from a Shell command.
- [x] Show installation availability and `/opencode-plugin install <id>` in list/detail output.
- [x] Correct README structure and explain configuration-driven installation for the two automatic built-ins and manual-only `ralph-loop`.

### Task 5: Verify and review

**Files:**
- Review all changed files under `vast-opencode-plugin-recommender/`
- Review: `docs/design/opencode-plugin-installer.md`

- [x] Run `node --test vast-opencode-plugin-recommender/scripts/install-plugin.test.mjs`.
- [x] Run dry-run previews for all three built-ins against an isolated temporary HOME and project.
- [x] Run the repository's skill review or equivalent structure checks.
- [x] Request an independent review focused on config safety, secret leakage, idempotency, and requirement coverage.
- [x] Fix findings and rerun verification.
