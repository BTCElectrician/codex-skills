---
name: doc-rot-scrub
description: Audit and scrub stale AI-era markdown so it stops misleading coding agents — hand-maintained "workflow"/context docs full of extracted functions and file maps, old PRDs and plans, cross-repo "mirror docs", duplicate doc trees, and stale editor rules (.cursor/rules, .cursorrules, copilot-instructions). Use whenever the user mentions old docs or markdown misleading agents or polluting context, an agent going off course from a stale doc, documentation debt, doc cleanup/audit/scrub, mirror docs, old PRDs/context files they used to keep updated by hand, or a repo full of markdown from the early vibe-coding era — even if they never say the word "scrub".
---

# Doc-Rot Scrub

## Why this skill exists

Between 2023 and 2025, people wrote piles of markdown to work around small
context windows and weak models: hand-maintained "workflow docs" with
extracted functions and file attributions (updated every few days so the
agent never had to read the whole codebase), architecture narratives,
duplicated "how the other repo works" docs, PRDs, pasted AI diagnoses,
implementation plans. These served the human as much as the agent — external
working memory, so the operator didn't have to hold the codebase in their
head either. That habit was correct then; pre-digested context was
load-bearing. Modern agents read code directly, but they still treat
repo-local markdown as pre-verified context. Code fails loudly when it
drifts; markdown never does. The harm is double: outright wrong claims send
agents off course, and even accurate-but-obsolete docs pollute the context
window with noise that anchors the agent's plan on a stale map of the
codebase. The scaffolding outlived the construction phase and became a
hazard.

This skill finds that rot, proposes dispositions, and executes them safely.

## The two axes (the core doctrine)

Classify every doc on two independent axes. Do not collapse them.

1. **Ownership** — does this repo own the behavior the doc describes?
   A doc whose primary subject is another repo/service's internals is a
   **mirror doc**. Mirrors cannot stay true: nothing breaks here when the
   other repo changes.
2. **Freshness** — is this doc live-and-promoted, or a superseded snapshot?
   A doc can be fully repo-own and still be stale ("repo-own ≠ live").

Dispositions by quadrant:

| | Fresh | Stale |
|---|---|---|
| **Repo-own** | KEEP (promote/maintain) | DEMOTE (archive dir, out of default search) or DELETE |
| **Mirror** | RETIRE → replace with a link to the owning repo or a thin, dated boundary contract | DELETE (`git rm` — git history is the archive) |

Archive-with-banner only when a doc holds unique rationale captured nowhere
else. Banner format: date, "ARCHIVED SNAPSHOT — do not treat as current",
pointer to the owning source of truth.

## Operating rules (non-negotiable safety)

- **Audit and execution are separate passes.** The audit is read-only and
  produces a manifest. A human approves the manifest before anything is
  deleted. Never audit-and-delete in one pass: dispositions are judgment
  calls, and on auto-deploy branches a merge is a release.
- **Never touch a working tree another agent (or the user) is actively
  using.** Signs of life: dirty files, fresh mtimes, HEAD advancing between
  your looks. If active, do all writes in a `git worktree` cut from
  `origin/<default>` on a new branch, merge remote-side via PR, and state the
  expected conflicts in the PR body.
- **Never destroy a possibly-only copy.** Before deleting bulk-copied content
  (research dumps, corpora), verify it exists at its origin (`diff -r`). If
  origin is missing or ambiguous, leave it and report.
- **Code wins.** When a doc contradicts the code, the doc is wrong. Verify
  claims against code before calling a doc stale, and before writing
  replacement text.

## Phase 0 — Trip-wire recon (before anything else)

Answer these for each target repo; they decide execution mechanics later:

1. Does pushing the default branch deploy? Check workflows AND prose —
   platform-native integrations (Render, Vercel, Netlify) are invisible in
   `.github/workflows/`; READMEs and agent files usually state them.
2. Do workflows/scripts read or publish docs? Look for: Pages/site builds fed
   from files under `docs/`, guardrail scripts with hardcoded doc-path
   allowlists, build scripts that regenerate doc files, CI path filters on
   `docs/**`.
3. Do deploy-exclude files (`.funcignore`, `.vercelignore`, package globs)
   already exclude docs? If yes, doc changes carry zero runtime risk there.
4. Is there a search-hygiene contract (`.rgignore`, archive policy in a docs
   README)? You must preserve it — see pattern 10 in the reference.
5. Does automation consume specific docs (autofix workflows reading a prompt
   file, skills reading an asset map)? Those files are load-bearing.
6. Is another agent active in the checkout (rule above)?

## Phase 1 — Audit (read-only)

Work in this order; the order is the method:

1. **Agent surfaces first.** Enumerate every file that instructs agents:
   `AGENTS.md`, `CLAUDE.md`, `README` "start here" sections, docs-index
   READMEs, `.cursor/rules/*` and `.cursorrules`,
   `.github/copilot-instructions.md`, `.codex/` prompts/skills. Extract each
   surface's mandated reading list. **The danger is not a stale doc existing;
   it is a stale doc being cited from a startup surface.** Priority =
   referenced-from-surface × stale.
2. **Inventory.** `git ls-files '*.md'` (plus `.mdc` editor rules), count by
   directory, capture last-commit date per candidate
   (`git log -1 --format=%cs -- <path>`).
3. **Classify** against the two axes using the pattern catalog — read
   `references/rot-patterns.md` for the 10 field patterns with detection
   commands, dispositions, and real-world field notes.
4. **Spot-check verification.** For the docs that surfaces DO mandate, verify
   2–3 concrete claims each against code: routes, file paths, commands, make
   targets, framework/model names. Report only failures. This is cheap and
   high-signal — it separates "old but true" from "confidently wrong".
5. For multi-repo scrubs: detect replicated bundles — the same
   directory/filenames appearing in several repos at different freshness
   levels is the classic mirror signature (compare `git ls-files` basenames
   across repos).

### Required audit output: the disposition manifest

Write one manifest file (do not scatter findings). Use exactly this shape:

```
# Doc-Rot Audit — <date>
## <repo> (deploy-on-push: yes/no; execution mechanics: direct|branch+PR|worktree+PR)
State: <branch, dirty count, active-agent signs>
Trip-wires: <pages builds, guardrail scripts, regen scripts, rgignore contract, automation-consumed docs>
- RETIRE (mirror, delete): path — 1-line why — last commit — referenced-from
- ARCHIVE (unique rationale): path — why unique — target archive path
- MOVE/DEMOTE (repo-own, stale): path — target
- FIX (surface citations, wrong claims): file — exact claim — verified truth
- REGENERATE: path — regen command — coupling (build scripts)
- KEEP (load-bearing, verified): path — why
- DO-NOT-TOUCH: paths with runtime/CI coupling
Counts: total md / stale % / lines to remove (estimate)
```

## Phase 2 — Approval gate

Present the manifest with per-repo mechanics and stop. Ask one clear
question: execute as proposed, execute PRs-only, or hold. Do not proceed on
silence.

## Phase 3 — Execution (only after approval)

Pick mechanics per repo from Phase 0 answers:

| Situation | Mechanics |
|---|---|
| No deploy on push, no active agent | direct commit to default branch |
| Deploy on push (main = production) | branch + PR; merging is a release — operator merges |
| Active agent / dirty checkout | worktree from `origin/<default>` + PR; sequencing note for expected delete/modify conflicts ("resolve by keeping deletions") |

Execution rules, learned the hard way:

- Fix pointer surfaces **in the same change** as the deletions. Deleting a
  mirror while `AGENTS.md` still says "trust the local mirror" leaves agents
  chasing dead links — worse than before. Grep every removed path across the
  repo (`rg -uu` to bypass ignore files) and fix danglers; replace citations
  with owning-repo links.
- `diff -r` duplicate directories against their archive twins immediately
  before `git rm`; if any file differs, move it instead.
- Do not hand-edit or delete generated docs with build coupling — rerun the
  generator, or flag as known-stale if it needs live infrastructure.
- Update guardrail allowlists / ignore files in the same change; when
  deciding search visibility, judge on **freshness**, not ownership
  (keeping a repo-own doc in the tree ≠ surfacing it in default search).
- Run the repo's own checks (its doc-guardrail scripts, linters, test suite)
  before commit; after opening PRs, read bot-review comments before merging —
  in field use a review bot caught a real regression a human missed.
- Never print anything that looks like a credential; if a file slated for
  deletion appears to contain a live secret, skip it and report.

## Phase 4 — Prevention (so it doesn't regrow)

1. Add a short rule to each repo's `AGENTS.md`: "Do not create or maintain
   docs describing sibling repos'/services' internals. Link to the owning
   repo or write a thin, dated boundary contract."
2. If the org has a control-plane/meta repo, land the two-axes doctrine there
   as policy; the control plane may keep cross-repo *maps* only as dated
   routing aids, never implementation truth.
3. Gold standard seen in the field: a docs-guardrail CI script that fails any
   tracked doc outside an approved location allowlist, plus a dated-archive
   directory convention. Offer it; do not force it.

## Calibration (what to expect)

Field data from a four-repo portfolio audit (~950 tracked markdown files):
75–81% of markdown was stale in the worst repos; ~108,000 lines deleted with
zero functional risk; actively-maintained startup surfaces were mostly
accurate (~70 claims verified, 2 false) while the rot concentrated in old
strata and editor-rule files. Expect the scrub to be mostly deletion, not
rewriting — and expect the sneakiest findings in `.cursor/rules/`, not in
`docs/`.
