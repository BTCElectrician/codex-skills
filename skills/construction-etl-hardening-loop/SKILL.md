---
name: construction-etl-hardening-loop
description: Harden construction-document extraction when source content is missing, misassigned, or silently omitted. Use for cross-trade drawing, schedule, table, and final-query failures. Preserve model-native semantics and generic evidence capture; do not use this skill as authority for Oracle V3 workbook procedures or as a reason to add trade-specific parsers.
metadata:
  short-description: Evidence-bound model-native construction extraction
  version: "2.1.0"
  owner: "BTCElectrician/codex-skills"
  last-verified: "2026-10-12"
  applies-to: "Cross-trade construction extraction and compiler hardening"
---

# Construction Evidence Hardening

Use this skill to prevent the same construction-document information loss on future projects. It supplies portable integrity rules, not product architecture or permission to mutate reviewed truth.

## Authority and freshness

- The user's current request and the target repository's live `AGENTS.md`, status, contracts, runtime code, and tests outrank this skill.
- Inspect the live repository before choosing an implementation. Do not import Oracle V3, workbook, Azure, or historical packet procedures unless the current task and repository actually use them.
- If this skill conflicts with current product evidence, keep the evidence and stop applying the conflicting instruction. Report the mismatch instead of treating an installed skill as current authority.

## Required outcome

Require complete accounting, not a dishonest promise of perfect semantic extraction:

- every registered source and meaningful work unit reaches the repository's existing terminal contract;
- `empty` is earned by source evidence, not accepted because an extractor returned nothing;
- visible but unresolved material remains explicit `incomplete`, unclassified, or the repository's equivalent;
- literal content and source locators survive before normalization and typed projection; and
- a correction is not closed until the reusable path is fixed and tested, the issue is proven false or stale, or the unresolved ambiguity is preserved with evidence.

Do not add a new public state merely to satisfy this skill.
Complete accounting does not require every possible fact to become a typed
record before a user can ask a question. Keep authorized source access usable
when semantic compilation is incomplete; make the answer's evidence and limits
explicit. This is not permission to bypass publication or write gates.

## Model-native boundary

Model-native does not mean logic-free. Keep the split outcome-based:

- deterministic machinery accounts for sources, representations, work units, hashes, geometry, cache validity, schema validity, conservation, and terminal states;
- qualified models may perform the cross-trade semantic reading and structured extraction;
- validators test completeness and support; they do not invent missing source meaning; and
- typed trade projections follow lossless generic capture rather than replacing it.

Literal transcription and supported interpretation are different outputs.
Preserve the printed cells unchanged, while allowing a qualified model to
propose relationships or calculations separately, with source references,
assumptions and unresolved alternatives. A no-inference transcription prompt
must not become a blanket ban on semantic extraction. Do not invent geometry
or silently promote an interpretation into printed truth.

Deterministic output is a candidate, not independent ground truth. Require
field-local source support before an override; record both candidates and the
reason. A partial native read must not erase a populated field it did not
observe. Plausibility, familiar values, majority agreement and a parser's empty
cell do not by themselves prove what a source prints. Keep unsupported or
disputed values available as review evidence without serving them as settled.

Before adding parser logic, test whether the model received the complete, legible source region with its headings, entries, notes, and geometry. A stronger model cannot recover evidence that routing, cropping, truncation, or candidate selection withheld.

Default to one generic table/schedule path. Do not add project, customer, drawing, or trade literals. Add a specialized deterministic path only after a measured generic failure proves it necessary, keep it narrow, and retain a generic fallback. A mature incumbent implementation may serve as a conformance baseline or temporary fallback; it is not automatically the successor architecture.

## Earliest-fault repair order

Run enough of the complete compiler to keep downstream failures visible, then repair the earliest demonstrated loss:

1. frozen source inventory and readable representation;
2. region or work-unit construction, including the exact evidence supplied to a model;
3. literal and semantic extraction;
4. table structure and deterministic normalization;
5. occurrence grouping, relationships, authority, and conflict handling;
6. retrieval, projection, and final presentation.

Trace the actual request and every representation serving the affected fact:
source region -> untouched provider response -> adapted/normalized data ->
final consumer records. A pre-normalizer sidecar may already contain repairs;
label it honestly if the original provider response is unavailable. Check
parallel record types for inconsistent values and lost units, relationships or
review conditions; a correct primary record does not certify its duplicates.

The repair mechanism remains open. The correct fix may be a generic model input, profile, prompt, region builder, validator, normalizer, or projection change. "Fix upstream" does not mean "write another parser."

## Cross-trade schedule contract

For a schedule or table-like region, preserve an equivalent of:

- source title and table identity;
- every header row and merged or hierarchical heading;
- every entry's identifying cell plus all cells governed by those headings;
- continuation lines and repeated designations without accidental merging;
- notes explicitly referenced by an entry;
- sparse summaries, totals, capacities, and footer values;
- literal cell text, units, and evidence geometry; and
- diagnostics for illegible, ambiguous, truncated, or structurally unmatched content.

When typed semantics are not supportable, retain the literal cell grid or bounded source observation. Do not discard the region merely because it cannot yet become an electrical, mechanical, plumbing, architectural, structural, controls, or other typed record.

## Proof proportional to the claim

- Reproduce the demonstrated failure on source-authorized evidence or an honest focused fixture.
- For a changed behavioral boundary, add a relevant positive and failure/suppression/abstention control; documentation-only clarification does not require a new extraction experiment.
- Name what each validator observes and show that it rejects a relevant failure. A row count, plausible value, arithmetic agreement or valid JSON cannot certify descriptions, notes or complete semantics. Escalation gated on those checks inherits their blind spots.
- For a generic or cross-trade claim, exercise materially different schedule shapes and trades; one project or one selected answer set is not universal proof.
- Compare with any proven incumbent capability that the successor promises to preserve.
- Run representative operator questions through the final delivered surface, with the correct source/page/region and an honest abstention when unsupported.
- Use an unseen project only after the generic repair is frozen. Preserve failed holdouts as failed evidence; do not tune their validator or hidden key into a pass.

Prefer the smallest focused test and repository-required gate that falsify the changed boundary. Do not create packets, councils, or review artifacts that do not improve the working capability.

Treat image sizing, token/reasoning limits, model allowlists and escalation
thresholds as replaceable, evidence-backed policies. Inspect the actual input,
provider completion status and reasoning/output usage before blaming a model
or raising a budget. Reconsider a restriction when current evidence falsifies
its rationale; a newer model name alone is insufficient. Saved-output replay
can prove processing changes, not the accuracy of a new prompt or image crop.
This skill grants no spending, fresh holdout use or production-data authority.

## Residual recovery

When most frozen work units remain valid, rerun only failed, changed, or invalidated units. Rebuild the complete artifact from validated cached units only when the output contract requires it. Broaden reprocessing only when source revision, schema, runtime, provenance, or cache validation proves the broader set invalid.

## Oracle V3 review workflows

When the task specifically concerns Oracle V3 ground-truth CSVs, review workbooks, or production fact synchronization, use `$oracle-v3-review-workbook-hardening` for that repository-specific procedure. Do not apply those manual review mechanics to Anvil by default.
