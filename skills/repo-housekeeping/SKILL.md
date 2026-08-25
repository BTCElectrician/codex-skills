---
name: repo-housekeeping
description: Refresh repository agent instructions and the canonical current-state handoff after meaningful work. Use when the user asks to do repo or project housekeeping, update agent docs, bring status current, refresh a resume manifest, clean up the documents agents use, or close work out properly. Do not use for a broad documentation rewrite or doc-rot audit.
---

# Repository Housekeeping

Make the smallest evidence-backed documentation update that lets the next agent
resume correctly. Follow the owning repository's instructions; do not impose a
universal filename or duplicate repository doctrine.

## Scope

- Work in the named repository. If none is named, use the current workspace;
  do not fan out across repositories by inference.
- Treat unrelated dirty changes as user or agent work. Preserve them and edit
  only the files this closeout owns.
- Housekeeping does not authorize implementation, release, deployment,
  destructive cleanup, or another repository's writes.

## Closeout

1. Read the applicable repository-local `AGENTS.md` files when present,
   `git status --short`, and the relevant diff, code, tests, or artifacts from
   the work being closed out.
2. Use the repository's declared instruction precedence and path scope to
   identify the canonical current-truth surface. It may be `STATUS.md`,
   `docs/STATUS.md`, `RESUME_MANIFEST.md`, or an equivalent. If `AGENTS.md`
   is missing or names no such surface, inspect existing repository
   instruction entry points and their first-read links; select an existing
   handoff only when its canonical role is unambiguous. Never choose by
   filename alone or create a new status document merely to finish closeout.
   When several surfaces exist, preserve their declared roles and avoid
   repeating the same state across them.
3. If instructions conflict, a declared handoff is missing, or canonical
   ownership remains ambiguous after applying declared precedence, do not
   guess or rewrite the disputed surfaces. Report the conflict as the
   remaining blocker and ask the user to identify the authority.
4. Update an existing `AGENTS.md` only when a durable operating rule,
   boundary, canonical command, first-read path, or ownership fact actually
   changed. Do not create one solely to complete housekeeping.
5. Bring the canonical current-truth surface up to verified live state:
   outcome, decisive evidence, unresolved blocker or residual risk, approval
   gates still closed, and the smallest next action. Include branch or commit
   identity when it matters to resumption or release truth.
6. Remove completed work from active context. Keep status concise and current,
   not chronological; link to existing evidence or immutable artifacts rather
   than copying their history.
7. Reconcile an active plan only when live evidence invalidated its assumptions,
   scope, sequencing, or acceptance check. Do not create or polish a plan merely
   to complete housekeeping.
8. If the repository declares an upstream coordination or portfolio handoff,
   leave its compact return record only when the outcome changed information
   that surface owns. Do not write upstream or into another repository unless
   that write is explicitly in scope.
9. Run the repository's documented focused checks for changed agent surfaces,
   plus `git diff --check` when available.

If evidence is incomplete, write `unknown` or name the unverified boundary.
Never manufacture a clean closeout from stale prose.

## Return

Report the files changed, the current truth established, validation performed,
and any remaining blocker. If no durable documentation fact changed, say so and
leave the files untouched.

