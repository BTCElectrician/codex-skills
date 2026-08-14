---
name: hq-research-specialist
description: Research and synthesize evidence for Ohmni HQ across technology, software, finance, business, clients, writing, ideas, life administration, and general knowledge. Use for current external research, Perplexity or scout-report review, GitHub or repo reconnaissance, market or vendor questions, source verification, and research that must be routed into the correct HQ or owning-repo surface.
---

# HQ Research Specialist

Do not use this skill for:
- routine HQ health checks already covered by `hq-status`, `hq-audit`, or `hq-doctor`
- code changes in product repos
- deployment, environment mutation, or other write-heavy operational tasks

## Workflow

1. Ground locally and classify the question
- If the current repo is `ohmni-hq`, read `docs/HQ_DOC_VERSION.md` before deeper work.
- Search prior captures with `python3 ops/knowledge_ledger.py search <terms>` before starting fresh research when the task concerns research, markets, vendors, models, or tooling.
- If the task touches a client, read `docs/clients/README.md` and the client folder if it already exists.
- If the task touches routing or portfolio questions, read `hq.yaml`, `docs/REPO_INVENTORY.md`, `docs/PORTFOLIO_CANON.md`, and `docs/NAMING_CANON.md`.
- Resolve what can be learned from local files before browsing or asking questions.
- Classify the primary domain before choosing sources: technology/software, finance, client/business, writing/content, ideas/strategy, life administration, personal reflection, or general knowledge.

2. Choose sources for the domain
- Technology/software: source code, official docs, stable releases, standards, issues, PRs, benchmarks, and repo-local evidence.
- Finance: regulatory filings, company investor materials, primary market data, and dated source documents; keep research distinct from financial advice.
- Client/business: client-provided evidence, official records, industry sources, and current commercial context.
- Writing/content: original sources, interviews, the operator's corpus, and verified factual support; preserve source material separately from drafted prose.
- Ideas/strategy: existing canon, market evidence, counterarguments, analogs, and clearly labeled inference.
- Life administration: official agencies, providers, and operator-supplied records; keep sensitive sources outside git and use redacted HQ state.
- Personal reflection: use operator-provided material and private operator
  storage outside the active repository portfolio; archived REWIRE may be
  consulted only for an explicitly requested historical-provenance lookup. Do
  not force external research.
- General knowledge: use the strongest primary sources appropriate to the question.
- Do not browse merely to make a creative, reflective, or local-evidence task look more researched.

3. Compose specialist skills only when earned
- Use a narrower installed skill when it adds a distinct source system, tool, artifact, or validation method; keep this skill as the research router and synthesis layer.
- Examples: `openai-docs` for current OpenAI product claims, `research-software` for implementation-level software archaeology, `video-intelligence` for video ingestion, and an owning-repo finance workflow for securities research.
- Do not invoke a specialist merely because its topic is mentioned, and do not create a new skill for a one-off subject.

4. Split independent evidence lanes when useful
- Web or vendor lane: official docs, pricing pages, product pages, standards, and current external sources.
- GitHub or repo lane: source, issues, PRs, releases, local status, ownership, and drift signals.
- Use at most 2 explorer sub-agents in parallel when that materially reduces time.
- Keep delegated asks bounded and source-driven.
- Do not delegate the final synthesis.

5. Hold a strict source policy
- Prefer primary sources appropriate to the domain rather than one universal source hierarchy.
- For time-sensitive facts, verify with live sources and include exact dates.
- Distinguish sourced facts from inference.
- Keep a link or repo path for every material claim.
- Treat scout reports and generated research as leads until their material claims are verified.

6. Produce one research packet
- Follow `references/research-packet.md`.
- Default to returning the packet in the response unless the user asked for a file update.
- Keep the packet concise, but do not skip sources, confidence, or landing targets.

7. Land durable state only where it belongs
- Technology, vendor, model, and general research: keep raw evidence under `artifacts/research/`; promote accepted findings to a dated `docs/research/topics/` note. Product behavior still belongs in the owning repo.
- Finance: use `ohmni-finance` for canonical research and analysis; keep only redacted portfolio/admin state or a concise pointer in HQ.
- Client/business: use `docs/clients/<slug>/` and choose `VERTICAL_RESEARCH.md`, `DISCOVERY_NOTES.md`, or `CLIENT_BRIEF.md` according to the finding.
- Writing/content: use `ohmni-writing` for canonical drafts and content systems; HQ may retain research evidence or a strategy pointer.
- Ideas/strategy: use a research topic note or decision memo only when the conclusion is durable.
- Life administration: use redacted `docs/life/` state; keep sensitive source records outside git.
- Personal reflection: keep source material in private operator storage outside
  the active repository portfolio; promote only durable shared decisions or
  next actions to HQ.
- If the answer does not deserve durable state, say so instead of creating a file.
- Update `docs/STATUS.md` or `docs/WORK_QUEUE.md` only when current HQ state, ownership, priority, blocker, or next action materially changes.

## Guardrails

- No secrets in git.
- No cross-repo writes without explicit `go`.
- HQ remains the control plane; product behavior belongs in product repos.
- Treat generated packets and exports as artifacts, not canonical truth.
- Do not turn research into implementation authority, investment advice, published writing, or external communication without the applicable approval and owning workflow.
- If the user only wants a fast answer, keep the same packet structure and compress it.
