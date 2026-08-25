# Portable Agent Skills

Reusable skills and agent templates for Codex, Claude Code, Cursor, and other
tools that support the open `SKILL.md` Agent Skills format.

Agent startup: read `AGENTS.md`, then this `README.md`.

Do not copy secrets, full env backups, private repo data, or target-repo
credentials into this vault. Skills that mutate target repos or providers
should only be run when the current task explicitly calls for that workflow.

## Canonical homes (avoid drift)

Copy-based installs fork silently, so every skill has exactly one canonical
home, named in its `SOURCE.md`. Skills owned by a repo (e.g.
`hq-research-specialist` → `ohmni-hq/.codex/skills/`) are only *distributed*
from this vault: edit the canonical copy, then re-copy it here. Skills with
no other home (`flask-redundancy-audit`, `flask-redundancy-refactor-p0`,
`render-env-safe-update`) are canonical in this vault. When installing into a
repo, keep the skill's `SOURCE.md` so the next agent knows where edits belong.

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

## Repository housekeeping

`repo-housekeeping` performs a bounded closeout after meaningful work. It
updates operating instructions only when durable rules changed, brings the
repository's declared status or resume handoff to verified current truth, and
leaves unrelated dirty work alone.

Invoke it naturally:

```text
Do the repo housekeeping and bring the agent docs current.
```

Install the same folder at the project or user skill location supported by
your agent:

- Codex: `.codex/skills/repo-housekeeping/`
- Claude Code: `.claude/skills/repo-housekeeping/`
- Cursor: `.cursor/skills/repo-housekeeping/`; Cursor also discovers Codex and
  Claude skill directories.
