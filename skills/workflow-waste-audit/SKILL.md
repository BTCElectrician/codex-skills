---
name: workflow-waste-audit
description: Audit repeated CI, test, build, deployment, or artifact work in one repository and propose evidence-backed reductions without weakening required protections. Use when investigating wasted workflow effort or cost; defaults to read-only recommendations.
---

# Workflow Waste Audit

Find work that can safely stop, run less often, or run differently. A result
that finds no safe cut is successful. Do not promise a savings target.

## Bound the question

Default to one repository and one suspected pattern: duplicate runs, overly
broad checks, slow test execution, repeated builds, or retained artifacts.
Read the repository's operating instructions and inspect its current revision,
dirty state, workflow definitions, and relevant build/test callers. Preserve
unrelated work. Use existing tools before proposing a custom subsystem.

Choose a bounded recent sample that includes successes, failures, and reruns.
Record the period and omissions. Respect an explicitly requested broader audit; do not expand the default into
a portfolio inventory, recurring monitor, automatic cleanup, or reusable
change classifier on your own.

Default to read-only. Existing permission to inspect is not permission to
cancel runs, change rules, dispatch paid work, delete artifacts or deployments,
change secrets, or publish. Honor task-specific authorization and limits.
Never expose credentials or private data in evidence or a public report.

## Follow purpose before calling work redundant

Trace each candidate to the user outcome and protection it provides. Compare:

- Event and purpose: pull request, push, manual run, release, or merge queue.
- Source and tested revisions: branch head versus generated merge revision.
- Trust and access: fork versus trusted branch, permissions, secret availability,
  environment approvals, and security or privacy boundaries.
- Execution inputs: platform, runner, dependencies, generated inputs, caches,
  matrix entries, artifacts, and build configuration.
- Consumers: required checks, check attribution, downstream jobs, publication,
  deployment, native checks, regression coverage, and migration validation.

Matching a commit hash and command is insufficient. Keep independently required
trust, merge, or environment checks. A duplicate is a change candidate only
when inputs, execution boundaries, outputs, and consumers are equivalent and
removing it preserves the required protection and its attribution.

## Assess a narrower trigger conservatively

Trace actual served and build inputs before labeling files narrative-only.
Markdown, prompts, configuration, and generated source may affect runtime.
An extension or directory name does not establish that a file is harmless.

A narrative-only skip proposal needs a complete, understood comparison against
the right base and a verified allowlist of non-runtime narrative paths. Keep
full checks for mixed or unknown changes, unavailable/ambiguous history,
renames, deletions, new branches, changes to the classifier itself, workflows,
build inputs, dependencies, and security-sensitive inputs. Preserve required
check reporting and merge-queue behavior even when expensive work is skipped.
Do not create a general classifier as part of this audit.

## Measure the effect that the evidence supports

Count all attempts, including failed experiments and reruns; successful runs
alone hide the cost of an unreliable shortcut. Separate these measurements:

| Measurement | Meaning and limit |
| --- | --- |
| Developer wait | Elapsed time until the needed result; concurrent jobs overlap. |
| Runner execution | Sum of job execution time across all attempts; not elapsed wait. |
| Billable usage | Provider-metered usage after applicable rounding, allowances, and rates. |
| Storage | Source bytes, deployed bytes, and metered GB-month are different quantities. |

Use matched workloads and disclose cache, runner, platform, and concurrency
differences. Unknown billing, visibility, allowance, or rates stay unknown,
not zero. Verify current provider terms before making a dollar claim. Reduced
execution may improve wait without reducing the invoice. Label proposed
savings anticipated until comparable post-change evidence proves them.

## Review assets or retention only when relevant

For a build/deployment/artifact question, trace what is actually uploaded,
served, retained, and metered. Check ownership, aliases, preview consumers,
rollback requirements, and retention policy before recommending a cut.
Repository size alone does not establish deployment or billed storage.
Version 1 produces retention recommendations only; it does not delete assets,
branches, deployments, caches, or artifacts.

## Return a usable decision

Lead with the plain-English finding, why it matters, what was verified, what
remains uncertain, and any decision needed. Classify each candidate as:

- **Keep:** work supplies a necessary protection or distinct outcome.
- **Change:** evidence supports a narrowly scoped reduction and its safeguards.
- **Investigate:** missing evidence prevents a safe classification or cost claim.

For each material finding, link the relevant definitions and sampled runs,
explain the scoped proposal, and state the supported effect and uncertainty.
Use a compact table when useful; no mandatory receipt or dashboard. Reuse one
existing task, pull request, or completion record instead of creating paperwork.
Stop once the bounded question is answered.

If implementation is explicitly authorized, prove the changed safeguard at its
actual enforcement point with a relevant failure case and a valid case. Then
check a real hosted result, including required-check attribution and merge
behavior where applicable. Local simulation does not prove hosted enforcement.
Preserve real regression, security, privacy, migration, and native checks.
A faster experiment that fails is not an improvement: report it, keep the safe
baseline, and stop at the agreed cap instead of retrying or expanding authority.

## Conditional tools and examples

Use available read-only connectors or CLIs. For GitHub Actions, inspect run
attempts, jobs, events, and logs with existing `gh` commands; see the official
[run-view manual](https://cli.github.com/manual/gh_run_view). For Vercel evidence,
use its official CLI or connector; see
[deployment inspection](https://vercel.com/docs/cli/inspect). Neither tool is a
mandatory dependency. Read current primary provider documentation for the
specific billing or protection question rather than copying vendor manuals.

Read [examples](references/examples.md) when an ambiguous classification needs
an illustration. The figures are synthetic, not performance or savings claims.
