# Artifact Discovery

## Evidence Priority

1. User-supplied `--source` files or directories.
2. Files whose names, directories, or frontmatter clearly match the inferred work topic.
3. PLAN, SUMMARY, VERIFICATION, and UAT artifacts in the relevant phase or execution-plan directory.
4. REVIEW, RETROSPECTIVE, POSTMORTEM, testing, and handover artifacts.
5. Project-level STATE and CHANGELOG files for context.

Read high-priority candidates first. Stop adding broad project files once the work boundary and evidence are sufficient.

## Default Candidates

```text
*-PLAN.md
*-SUMMARY.md
*-VERIFICATION.md
*-UAT.md
*-REVIEW.md
*-RETROSPECTIVE.md
*-POSTMORTEM.md
STATE.md
CHANGELOG.md
docs/exec-plans/**/*.md
docs/testing/**/*.md
docs/handover/**/*.md
docs/retrospectives/**/*.md
.planning/**/*.md
```

## Exclusions

Always exclude:

```text
.git/
.ref-project/
.worktrees/
node_modules/
vendor/
dist/
build/
coverage/
.working/
_sandbox/
<docs_root>/<learnings_dir>/
```

The target learnings directory is excluded to prevent recursive summarization and gradual distortion.

## Work-Boundary Inference

Use evidence in this order:

1. The business object named by the user.
2. Active or recently completed plans.
3. Matching summary, verification, UAT, handover, or postmortem artifacts.
4. Branch, tag, and recent commit messages as discovery clues.
5. The current session's completed work.

Do not expose scope taxonomy to the user. If two work boundaries are equally plausible, present their business names and ask which one to extract, or offer to generate separate documents.

## Minimum Evidence Gate

Proceed only when at least one artifact is explicitly associated with the inferred work boundary. A generic README, repository code, or unrelated CHANGELOG is insufficient by itself.

When evidence is insufficient:

1. State which topic was inferred.
2. List the files examined.
3. Ask for a plan, summary, verification, UAT, retrospective, or explicit `--source` path.
4. Do not generate a partial speculative document.
