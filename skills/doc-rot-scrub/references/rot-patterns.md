# Doc-Rot Pattern Catalog

Ten patterns observed in a real four-repo portfolio scrub (2026), ordered
roughly by danger. Each entry: what it is, why it misleads agents, how to
detect it, disposition. "Field note" lines are real (anonymized) findings —
use them to calibrate how bad things can actually be.

## 1. Mirror docs (sibling-repo internals)

Docs whose primary subject is another repo/service: "how the frontend flow
works" living in the backend repo, function-app internals documented in the
ETL repo. They cannot stay true — nothing in this repo breaks when the
sibling changes.

Detect:
```
git ls-files '*.md' | grep -iE 'frontend|backend|azure|flow|interplay|<sibling-names>'
rg -il '<sibling repo/service names>' docs/
```
Then read candidates: is the *primary subject* the sibling? (Mentioning a
sibling is fine; narrating its internals is the offense.)

Disposition: RETIRE. Delete; replace citations with a link to the owning
repo, or a thin dated boundary contract (interface only, "last verified
<date>"). Boundary contracts that draw the ownership line WITHOUT narrating
sibling internals are the healthy replacement — keep those.

Field note: 1,500-line "azure function flow" mirrors existed in three repos
at three different freshness levels; one was still labeled "Current Contract".

## 2. Replicated bundles across repos

The same doc bundle copy-pasted into several repos, each copy aging
differently. Four copies of "the truth" and no way to tell which lies.

Detect (multi-repo scrubs):
```
comm -12 <(git -C repoA ls-files '*.md' | xargs -n1 basename | sort -u) \
         <(git -C repoB ls-files '*.md' | xargs -n1 basename | sort -u)
```
Same distinctive directory names (`*-interplay/`, `*-flow/`) in ≥2 repos is
the signature.

Disposition: keep at most the copy in the owning repo (if fresh); delete the
rest per pattern 1.

## 3. Stale editor-agent rules (.cursor/rules, .cursorrules, copilot-instructions)

The sneakiest surface in the field. These files are auto-loaded by editors,
never listed in docs indexes, and nobody maintains them. They are read by
agents on every session.

Detect: `ls .cursor/rules/ .cursorrules .github/copilot-instructions.md`
then verify EVERY factual claim against the codebase: framework and version
(check the real package/dependency file), endpoints, model IDs, index/service
names, file paths.

Disposition: DELETE when generic-2024-era or wrong (the canonical agent
surface is `AGENTS.md`); FIX in place only when the file is genuinely used
and mostly right.

Field note: one repo's rules claimed it was a Next.js app — it was Flask.
Another cited an endpoint renamed months earlier, dead model IDs, and paths
from a different machine (`/mnt/project/...`). Three of four repos had stale
rules; zero had accurate ones.

## 4. Byte-identical duplicate doc trees

A directory duplicated wholesale (usually live copy + `legacy/` copy) so
"current" and "archive" contain the same bytes and both rot together.

Detect:
```
diff -rq docs/<dir>/ docs/legacy/<dir>/
```

Disposition: DELETE the live copy, keep the archived one — but re-run
`diff -r` immediately before `git rm`; if any file diverged, `git mv` the
divergent file into the archive instead of deleting it.

Field note: three full directories (37 files) were byte-identical duplicates
of their already-archived twins.

## 5. Weak-model-era briefing artifacts

Old implementation plans, "context for the AI" files, pasted chat diagnoses,
dated week-folders, one-off patch snippets. Correct habit for 2023-24 models;
pure hazard now.

Detect: filename patterns `*PLAN*`, `*CONTEXT*`, `*GUIDE*`, `*PROMPT*`,
`*IMPLEMENTATION*`, `*HANDOFF*`, `week-*/`, month-named dirs; cross-check
age (`git log -1 --format=%cs -- <path>`) and whether any agent surface
references them (`rg -uu -l "$(basename <path>)"`).
Rule of thumb: >6 months untouched AND unreferenced from any surface.

Disposition: DELETE (or MOVE into the archive dir if the repo has one and
the doc records a decision not captured elsewhere).

Field note: 75–81% of tracked markdown in two repos fell in this bucket,
including a 749-line pasted AI diagnosis.

## 6. Off-topic squatter content

Bulk-copied corpora that have nothing to do with the repo (research dumps,
training material) — usually one giant import commit, often with " copy" in
folder names.

Detect: directory md-counts wildly out of proportion to the repo's purpose;
`git log --diff-filter=A --format='%cs %s'` on the directory shows one bulk
commit.

Disposition: verify the content exists at its true origin
(`diff -r` against the origin repo/folder); if confirmed, `git rm` here; if
origin is missing or contents diverge, relocate first or leave and report.
Never delete a possibly-only copy.

Field note: a 140-file electrician-research corpus was squatting in a
serverless-functions repo; 139/140 files were byte-identical to their real
home, so deletion was safe — but only provably so after the diff.

## 7. Half-finished retirements

A previous cleanup added "do not trust this" banners or dropped docs from one
reading list, but other startup surfaces still cite the same files as
authoritative. Agents follow the mandated read order and hit the permissive
framing first.

Detect: for every doc with a banner or "historical" label, grep which
surfaces still cite it: `rg -uu -l "$(basename <doc>)" AGENTS.md CLAUDE.md README.md docs/`

Disposition: finish the job — delete the doc AND fix every citing surface in
the same change.

Field note: a repo's STATUS.md said "do not read the local mirrors" while its
AGENTS.md — read first — still said "the local mirror is <file>; trust it".

## 8. Stale generated docs with weak regeneration

Generated reference docs (schema snapshots, API dumps) where the regen step
only warns on drift instead of failing, so the file silently falls behind.

Detect: find the generator (`rg -l '<filename>' scripts/ Makefile *.sh`);
check whether CI/build fails or merely warns on diff; spot-check the file
against present-day reality.

Disposition: REGENERATE via the real generator — never hand-edit, never
delete (build coupling). If regen needs live infrastructure you lack, flag as
known-stale in the PR body and move on.

Field note: a "current database schema snapshot" was missing the repo's
dominant feature of the previous five months because the build step only
warned on drift.

## 9. Search-hygiene drift (the repo-own ≠ live trap)

Repos with an archive policy (".rgignore keeps archival docs out of default
search") accumulate drift in both directions: stale docs outside the ignore
set, and — worse — cleanups that un-ignore archival docs because they are
"repo-owned". Ownership and freshness are different axes; visibility follows
freshness.

Detect: read the docs README for a stated archive policy; then compare
`rg --files docs/` (honors ignores) against `git ls-files docs/` and check
each exposed doc's age/promotion status.

Disposition: FIX the ignore file so unpromoted/stale docs stay hidden by
default while explicitly-promoted live docs stay visible (negation entries).
Verify from the repo root with no path argument — explicit paths bypass
ignores by design, which is the sanctioned escape hatch.

Field note: a scrub agent un-ignored an entire conceptual-flow directory
because the docs were "repo-own"; a PR review bot caught it. The fix restored
the blanket ignore plus one `!live-map.md` negation.

## 10. Orphaned self-referencing bundles

Doc clusters that only cite each other — zero inbound links from any agent
surface or index. Harmless-looking, but they surface in content greps and
read as authoritative once found.

Detect: for each cluster member, `rg -uu -l "$(basename <file>)"` — if all
hits are inside the cluster, it is orphaned.

Disposition: DELETE (lowest risk in the whole catalog — nothing points at
them). Check the docs index actually never listed them, and clean the index
if it did.

Field note: an eight-file mirror bundle sat quarantined in a legacy folder,
referenced by nothing but itself, for five months after everyone forgot it.

---

## Keep-list heuristics (what NOT to touch)

- Startup surfaces that pass spot-checks (`AGENTS.md`, `STATUS.md`,
  `docs/current/**`-style trees) — in the field these were ~97% accurate;
  the rot lives in the old strata, not the maintained handoff path.
- Boundary/ownership contracts between services (dated, interface-only).
- Archive gate READMEs and any archived file that a live surface explicitly
  points into ("see <archive>/incident-X.md").
- Decision records / ADRs — dated by genre; they claim to be history, not
  current truth, so they do not mislead.
- Anything a workflow, build script, generator, dashboard, or skill reads —
  the Phase 0 trip-wire list exists to find these.
- Prompt/template assets that are runtime inputs (not documentation at all).
