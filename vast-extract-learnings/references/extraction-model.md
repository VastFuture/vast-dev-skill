# Extraction Model

## Core Rule

Extract only claims explicitly supported by the collected artifacts. Every item must name one source file; include a section anchor when it is reliable.

## Decision

Use for a technical, architectural, product, workflow, or trade-off choice.

Required shape:

```markdown
### Title
What was decided.

**Rationale:** Why the team made this choice.
**Source:** `relative/path.md#section`
```

Evidence signals: "decided", "selected", "will use", "trade-off", "because", "rationale", architecture decision records.

Do not classify an implementation fact as a decision unless the artifact records a choice or rationale.

## Lesson

Use for knowledge gained during execution, verification, UAT, debugging, or a failed approach.

Required shape:

```markdown
### Title
What was learned.

**Context:** The execution situation that exposed the lesson.
**Source:** `relative/path.md#section`
```

Evidence signals: unexpected complexity, failed approach, verification gap, UAT feedback, corrected assumption.

Do not restate a decision as a lesson unless execution produced new information beyond the original rationale.

## Pattern

Use only for an approach that can plausibly apply again beyond the exact work item.

Required shape:

```markdown
### Pattern name
Description of the reusable approach.

**When to use:** Concrete applicability conditions.
**Source:** `relative/path.md#section`
```

Evidence signals: repeated successful technique, reusable testing strategy, stable module organization, workflow that reduced failures.

Reject one-off implementation details and generic advice such as "write tests" or "communicate clearly".

## Surprise

Use for an outcome that differed from planning or reasonable expectation.

Required shape:

```markdown
### Title
What was surprising.

**Impact:** Schedule, behavior, performance, scope, or design impact.
**Source:** `relative/path.md#section`
```

Evidence signals: estimate variance, hidden dependency, unanticipated edge case, performance mismatch, environment behavior difference.

## Classification Rules

1. Put an item in exactly one category.
2. Prefer the category matching the artifact's meaning, not its filename.
3. Merge duplicate claims from multiple artifacts; use the strongest source and mention additional sources only when useful.
4. Preserve uncertainty stated by the source. Do not strengthen "may" into "will".
5. Use concise, durable titles. Avoid dates in item titles.
6. If a category has no supported items, write `无（本轮未发现）`.

## Source Rules

- Prefer paths relative to the code project root.
- Absolute paths are allowed only for explicit external evidence.
- Use an anchor only when the heading is identifiable; do not invent anchors.
- A Git commit, current conversation, or source-code inference is not a valid standalone Source.
- Do not cite the generated learnings file itself.
