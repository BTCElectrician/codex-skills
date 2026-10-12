# Workflow Waste Audit

A portable agent skill for finding unnecessary CI, test, build, deployment,
or artifact work without cutting the checks that make releases safe.
It defaults to one repository and one suspected pattern, then recommends **keep**,
**change**, or **investigate**, with evidence and honest measurement limits.

## Install and use

Download this folder, or clone [Portable Agent Skills](https://github.com/BTCElectrician/codex-skills)
and select `skills/workflow-waste-audit`. Put the complete folder in your agent's
supported skills directory, keeping `SKILL.md`, `agents/`, and `references/`
together. For Codex, the usual per-user location is
`~/.codex/skills/workflow-waste-audit`. Use your agent's installation guidance
if its discovery path differs. Start a fresh session if needed.

Example request:

```text
Use $workflow-waste-audit to audit duplicate CI in this repository.
Inspect the last 12 completed runs, including failures and reruns.
Stay read-only. Give me keep/change/investigate recommendations.
Distinguish developer wait, runner execution, and actual billed usage.
```

GitHub CLI and Vercel CLI are optional evidence sources, not dependencies.
The agent needs read access to the relevant definitions and run history; it
should identify gaps when that access is unavailable.

## Public scope

This is an original instructional recipe, not an automatic optimizer or cleanup
tool. It does not guarantee savings, create a workflow classifier, dispatch
runs, or delete retained data. Authorized implementation needs focused boundary
checks and a real hosted result. Format validation and synthetic read-only
examples do not prove a production change is safe or a bill is lower.

The three [examples](references/examples.md) use synthetic facts and figures.
They cover misleading duplicate runs, conservative narrative-only skips,
and a faster experiment that fails. No private project evidence is included.

Licensed under the repository's [MIT license](LICENSE). Keep that license
with redistributed copies or substantial portions of this skill.
