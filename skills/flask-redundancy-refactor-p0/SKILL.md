---
name: flask-redundancy-refactor-p0
description: Implement exactly one P0 item from redundancy-audit.md in a Flask backend with contract snapshots and a single commit.
---

# Flask Redundancy Refactor P0

## Goal
Read redundancy-audit.md, implement exactly one P0 item, and make one commit. Preserve behavior. Do not add dependencies.

## Workflow

1. Read redundancy-audit.md
   1. Select exactly one P0 cluster.
   2. If no P0 exists, stop and report that no P0 items are available.

2. Create a contract snapshot before changes
   1. Create docs/contract_snapshots if it does not exist.
   2. Create a file named docs/contract_snapshots/<P0-ID>.md.
   3. Add a Before section that captures public contracts
      1. Routes and HTTP methods
      2. Request and response shapes
      3. Background jobs or CLI commands if relevant
      4. Config or environment variables touched
      5. Tests that cover the behavior

3. Implement the refactor
   1. Remove redundancy using a single shared helper or service.
   2. Keep changes minimal and localized.
   3. Preserve external behavior and existing APIs.

4. Update the contract snapshot
   1. Add an After section with the same structure as Before.
   2. Note any behavior that is intentionally unchanged.

5. Tests
   1. Run existing tests if they are fast and available.
   2. If a regression test is feasible without new dependencies, add one minimal test.

6. Commit
   1. Make exactly one commit.
   2. Suggested message: refactor: resolve redundancy <P0-ID>

## Guardrails

1. Do not touch auth, billing, or security logic.
2. Do not refactor more than one P0 cluster.
3. Do not change dependencies or deployment configuration.
