# Portable Agent Skills

Reusable skills and agent templates for Codex, Claude Code, Cursor, and other
tools that support the open `SKILL.md` Agent Skills format.

Agent startup: read `AGENTS.md`, then this `README.md`.

Do not copy secrets, full env backups, private repo data, or target-repo
credentials into this vault. Skills that mutate target repos or providers
should only be run when the current task explicitly calls for that workflow.

## Canonical homes (avoid drift)

Each retained shared skill has one authoritative source. HQ owns the registry
at `/Users/collin/Desktop/ohmni-hq/ops/skill_sources.json`; consult it before
editing or installing a skill. HQ-owned sources live in `ohmni-hq/skills/`,
a maintained directory outside agent discovery. This vault remains the owner
of `skills/repo-housekeeping/`, `skills/render-env-safe-update/`,
`skills/construction-etl-hardening-loop/`, and
`skills/oracle-v3-review-workbook-hardening/`. Edit these sources here.

Purchased/private upstream skills and private overrides stay in their registered
private location outside public Git. Vendor-managed packages retain vendor
ownership. Do not copy that content into this public vault or HQ. Historical
source records are provenance; the current HQ registry governs maintained paths.

## Maintained shared installations on this workstation

Claude Code and Codex reach shared skills through direct per-skill global
symlinks: `~/.claude/skills/<name>` and `~/.codex/skills/<name>` both point to the
registered authoritative source. These links provide access without independent
copies. Do not copy shared skills into user or repository discovery directories.
Global availability preserves the owning workspace's execution and approval rules.

Locate a maintained source from any workspace with the read-only HQ resolver:

```bash
python3 /Users/collin/Desktop/ohmni-hq/ops/skill_sync.py --resolve <name>
```

After editing a registered source, use the targeted HQ guard from HQ:

```bash
cd /Users/collin/Desktop/ohmni-hq
bash ops/skills_guard.sh --check --skill <name>
bash ops/skills_guard.sh --apply --skill <name>
```

Use `--apply` only for the intended skill. The maintained registry and
`/Users/collin/Desktop/ohmni-hq/docs/AVAILABLE_AGENT_SKILLS.md` describe source
ownership, discovery modes, updates, and restoration. Reload or start a fresh
agent task after changing instructions already loaded in memory. Historical and
secondary worktree discovery entries are outside this migration; global links
do not override or deduplicate their repository definitions.

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

Use the registered global link for your agent; both Claude Code and Codex
resolve `repo-housekeeping` directly to this vault's authoritative folder.
Consult the HQ registry for maintained access paths rather than creating
project copies. Other agents' installations are outside this migration.
