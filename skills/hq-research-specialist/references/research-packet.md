# Research Packet

Use this shape for any substantial HQ research output.

## Question

State the question being answered in one sentence.

## Scope

Name the covered lanes and exclusions.

Examples:
- web or vendor research only
- GitHub plus local repo review
- client discovery plus competitor verification

## Sources

List the exact sources used.

Examples:
- official vendor page links
- GitHub repo, issue, PR, or release links
- absolute HQ file paths when citing local repo material

## Findings

List the highest-signal findings first.

Rules:
- facts first
- separate inference from direct evidence
- include exact dates when freshness matters

## Confidence

State one of:
- high
- medium
- low

Add one short sentence explaining the confidence level.

## Open Questions

List only the unresolved questions that materially affect the next move.

## Landing Targets

Name where the durable output should go.

Common HQ targets:
- `artifacts/research/` for immutable raw evidence and scout ingests
- `docs/research/topics/` for accepted technology, vendor, model, strategy, or general research
- `docs/clients/<slug>/VERTICAL_RESEARCH.md`
- `docs/clients/<slug>/DISCOVERY_NOTES.md`
- `docs/clients/<slug>/CLIENT_BRIEF.md`
- `docs/clients/<slug>/RAW_AI_NOTES.md` only if useful
- `ohmni-finance` for canonical finance research and analysis
- `ohmni-writing` for canonical drafts and content systems
- private operator storage outside the active repository portfolio for personal
  reflection and private context; archived REWIRE is deliberate historical
  provenance only
- `docs/STATUS.md`
- `docs/WORK_QUEUE.md`
- `docs/life/*.md`

Product behavior and implementation truth belong in the owning repo. Sensitive
life-admin source records stay outside git. If no durable update is needed, say
so directly.

## Suggested Queue Items

List queue-ready next steps in HQ format when useful.

Example:
- [ ] [HQ-BIZ-###] (parent: ROOT) (owner: hq-agent) Distill lender workflow findings into `docs/clients/<slug>/VERTICAL_RESEARCH.md`.
