# Codex Skills Vault Agent Rules

This repo is a personal vault for reusable Codex skills and agent templates.
It is not a product runtime, deploy target, or data corpus.

First read after `AGENTS.md`: `README.md`.

## Boundaries

- Treat each `skills/<skill>/SKILL.md` as the contract for that skill.
- Skills may cause writes in target repos or provider mutations when used
  elsewhere. Do not run a skill's scripts unless the current task explicitly
  calls for that workflow.
- Do not inspect or copy credentials, `.env` files, Render tokens, full env
  backups, private repo data, or target-repo secrets into this vault.
- Templates under `templates/` can shape future agent behavior; keep them
  conservative and clear.

Keep this repo lightweight. Do not add product-style project docs, model
registries, or heavy status machinery unless the operator explicitly asks.
