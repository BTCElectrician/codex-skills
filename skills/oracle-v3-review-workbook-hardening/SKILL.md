---
name: oracle-v3-review-workbook-hardening
description: Repair Oracle V3 construction review packets when source PDFs, extracted CSVs, ground-truth fields, Excel workbooks, or emitted production facts disagree. Use only for explicit Oracle V3 review and synchronization work; do not use as Anvil compiler architecture guidance.
metadata:
  short-description: Oracle V3 review and workbook synchronization
  version: "1.0.0"
  owner: "BTCElectrician/codex-skills"
  last-verified: "2026-08-29"
  applies-to: "ohmni-oracle-v3 review packets and workbooks"
---

# Oracle V3 Review Workbook Hardening

Use this skill only when the live task targets Oracle V3 review packets, ground truth, CSVs, Excel workbooks, or emitted facts. Read Oracle V3's current `AGENTS.md`, status, code, and tests first; those sources outrank this skill.

## Boundary

- This is an incumbent review-and-synchronization procedure, not a generic Anvil extraction design.
- Do not copy Oracle-specific paths, overlays, mappers, or workbook mechanics into a successor unless a measured compatibility requirement justifies them.
- Do not run indexing, provider calls, broad reprocessing, production writes, or reviewed-truth mutation without the authority required by the live Oracle repository.

## Review loop

1. Open the exact source PDF visually when layout determines meaning.
2. Compare the affected extracted CSV or packet record with the source.
3. Preserve raw extracted values; put approved human truth only in the repository's current ground-truth or review fields.
4. Classify the issue as extraction, normalization, post-processing, packet/workbook, stale artifact, false positive, or unresolved ambiguity.
5. Repair the earliest reusable Oracle path and add a focused regression, or preserve the unresolved condition with evidence.
6. Regenerate the affected candidate or review surfaces without overwriting immutable runs or reviewed files outside the authorized scope.
7. When Excel is the active reviewer surface, synchronize its affected sheet with the backing CSV and verify entry count, review status, and key values before calling it complete.
8. When a review correction exposes a production-fact mismatch, verify the current Oracle transform/fact-emission path receives the same reusable repair before calling the pipeline hardened.

## Schedule-entry evidence

Judge a schedule entry using its identifying cell, the complete horizontal entry, the governing headings, and any explicitly linked notes. Name the actual failure: entire entry omitted, identifying cell missed, individual value missing, values under wrong headings, entry split, adjacent entries merged, or summary/footer omitted.

Do not add a one-off extractor automatically. First inspect Oracle's current detection, normalization, fallback, and schedule post-processing seams. Prefer an existing generic extension seam; use a specialized fallback only when source evidence and a focused regression justify it.

## Safety and completion

- Back up reviewed truth before an authorized mutation; never overwrite immutable artifacts.
- Keep literal source values separate from canonical or human-reviewed projections.
- Fail closed on ambiguous table structure instead of guessing.
- Run the focused tests and Oracle's current repository verification gate.
- A packet correction alone is not pipeline hardening when production facts would still reproduce the defect.

Finish with the exact source, affected review artifact, root cause, reusable code or tooling change, regression result, synchronized workbook/fact status when applicable, and remaining uncertainty.
