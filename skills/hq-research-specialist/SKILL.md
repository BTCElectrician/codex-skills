---
name: hq-research-specialist
description: Run bounded web, GitHub, and repo research for Ohmni HQ, optionally using up to two explorer sub-agents for evidence gathering, then synthesize the result into a standard research packet with sources, confidence, landing targets, and queue-ready next steps.
metadata:
  short-description: HQ research and synthesis
---

# HQ Research Specialist

Use this skill when the task needs:
- current web or vendor research
- GitHub or local-repo reconnaissance
- client or discovery research for HQ
- cross-source verification before HQ docs or packets are updated

Do not use this skill for:
- routine HQ health checks already covered by `hq-status`, `hq-audit`, or `hq-doctor`
- code changes in product repos
- deployment, environment mutation, or other write-heavy operational tasks

## Workflow

1. Ground locally first
- If the current repo is `ohmni-hq`, read `docs/HQ_DOC_VERSION.md` before deeper work.
- If the task touches a client, read `docs/clients/README.md` and the client folder if it already exists.
- If the task touches routing or portfolio questions, read `hq.yaml`, `docs/REPO_INVENTORY.md`, `docs/PORTFOLIO_CANON.md`, and `docs/NAMING_CANON.md`.
- Resolve what can be learned from local files before browsing or asking questions.

2. Split the research lanes
- Web or vendor lane: official docs, pricing pages, product pages, standards, and current external sources.
- GitHub or repo lane: repo inventory, issues, PRs, releases, local status, ownership, and drift signals.
- Use at most 2 explorer sub-agents in parallel when that materially reduces time.
- Keep delegated asks bounded and source-driven.
- Do not delegate the final synthesis.

3. Hold a strict source policy
- Prefer primary sources: official docs, vendor pages, GitHub repos, and repo-local docs.
- For time-sensitive facts, verify with live sources and include exact dates.
- Distinguish sourced facts from inference.
- Keep a link or repo path for every material claim.

4. Produce one research packet
- Follow `references/research-packet.md`.
- Default to returning the packet in the response unless the user asked for a file update.
- Keep the packet concise, but do not skip sources, confidence, or landing targets.

5. Land durable HQ state only where it belongs
- For market or industry intelligence, land in `docs/clients/<slug>/VERTICAL_RESEARCH.md`.
- For durable discovery capture, land in `docs/clients/<slug>/DISCOVERY_NOTES.md`.
- For stable client facts or commercial status, land in `docs/clients/<slug>/CLIENT_BRIEF.md`.
- Use `RAW_AI_NOTES.md` only when raw external output is useful for future reference.
- For durable HQ state or next actions, use `docs/STATUS.md` and `docs/WORK_QUEUE.md`.
- For life-admin tasks, use `docs/life/` redacted docs only.

## Guardrails

- No secrets in git.
- No cross-repo writes without explicit `go`.
- HQ remains the control plane; product behavior belongs in product repos.
- Treat generated packets and exports as artifacts, not canonical truth.
- If the user only wants a fast answer, keep the same packet structure and compress it.
