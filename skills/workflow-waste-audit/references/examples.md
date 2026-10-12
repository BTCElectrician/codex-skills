# Synthetic audit examples

These illustrate decisions, not benchmarks. Figures and repositories are invented.

## 1. The same command is not always the same protection

A fork pull-request run and a trusted push run both test source revision A
with `npm test`. The fork receives a read-only token and no deployment secrets;
the push checks a protected environment. A merge-queue run tests generated
revision M against the current target branch and supplies a required check.

**Keep:** each run has a distinct trust, environment, or merge purpose. Source
revision A and the same command do not establish interchangeable coverage.
Removing the queue check would also break required-check attribution.

Separately, two optional lint jobs on the same trusted push use the same tested
revision, runner image, dependencies, cache, permissions, and generated inputs.
Their logs and outputs match; neither is a required check or downstream input.

**Change candidate:** remove one optional lint job after verifying the consumers.
Two sampled successful attempts each spend 70 runner-seconds on it. That supports
an anticipated reduction in runner execution. It does not prove lower elapsed
wait or billed cost; invoice usage and applicable allowance are unavailable.

## 2. A safe narrative skip needs more than a file extension

A complete comparison against the target branch changes only `notes/meeting.md`.
The build graph and application callers show that this path is never consumed.
A proposal could keep the required reporting job while skipping expensive tests
for that narrowly verified narrative set, subject to boundary and hosted proof.

**Change candidate:** the narrative-only case, with those safeguards. Also test
that the ordinary code case still runs checks and reports their true failures.

Other comparisons change `notes/meeting.md` and `src/auth.ts`, rename a note into
`prompts/system.md`, delete a build input, or lack their base revision in a
shallow checkout. The application loads `prompts/system.md` at runtime.

**Keep full checks:** mixed changes, runtime Markdown, renames, deletions, and
unavailable history. New branches and changes to the proposed skip logic,
workflow, build, or dependencies also take the full path. A green local fixture
does not establish correct reporting for actual hosted merge-queue events.

## 3. Faster on success can be slower overall

A serial baseline passes a matched workload in 8 minutes of elapsed wait and
8 runner-minutes. A proposed four-shard experiment fails after 3 minutes because
all shards share a database schema. Its shards consume 12 runner-minutes.
The operator reruns the safe serial baseline, which passes in 8 minutes.

**Keep the serial baseline; reject the experiment as tested.** The experiment
and recovery consume 20 runner-minutes, and at least 11 minutes of sequential
wait before queue delays. Count both attempts. The 3-minute failed result is
not a shipped speedup, and the provider's billable usage remains unknown.

The failure supports a shared-state diagnosis. It does not authorize database
changes, more paid trials, or blind retries. An explicitly approved repair would
need isolation proof, failure and valid cases, and comparable hosted evidence.
