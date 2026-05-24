# Codex Skills Vault

This folder is a personal vault of Codex skills and agent templates.

Agent startup: read `AGENTS.md`, then this `README.md`.

Do not copy secrets, full env backups, private repo data, or target-repo
credentials into this vault. Skills that mutate target repos or providers
should only be run when the current task explicitly calls for that workflow.

## Install a skill in a repo (.codex/skills)

1. Create the folder .codex/skills at the root of the target repo.
2. Copy a skill folder into it. Example:

   cp -R /path/to/codex-skills/skills/flask-redundancy-audit /path/to/repo/.codex/skills/

3. If the skill does not appear, restart Codex CLI or the VS Code extension.

## Install skills globally (~/.codex/skills)

1. Create ~/.codex/skills if it does not exist.
2. Copy any skill folder into ~/.codex/skills.
3. Restart Codex CLI and the VS Code extension if the skill is not detected.

## Use a skill

Codex CLI example:

  codex exec --full-auto "Use $flask-redundancy-audit on this repo"

VS Code extension example:

  Use $flask-redundancy-audit on this repo and write redundancy-audit.md

Note: a restart may be required for new skills to load.
