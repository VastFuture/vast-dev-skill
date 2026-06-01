# AGENTS.md

This document describes project-specific agent instructions and conventions.

## Working Directory (`.working`)

The `.working` directory is a temporary workspace for experimental or exploratory work. It is gitignored and should not be committed to the repository.

### Purpose

- Sandboxing: Clone or extract external repositories, templates, or proof-of-concept code without polluting the main codebase
- Experimentation: Test ideas, evaluate third-party tools, or prototype features in isolation
- Temporary artifacts: Store intermediate build artifacts, generated files, or cached content that doesn't need to be persisted

### Usage Guidelines

1. **Always clean up** when done — remove contents once the work is no longer needed
2. **Never commit** — ensure `.working` remains in `.gitignore`
3. **Document here** any special tools, scripts, or workflows specific to `.working` if needed

### Current Contents

Currently contains a clone of `attractor-guided-engineering-template` — a template repository used for evaluation or experimentation purposes.