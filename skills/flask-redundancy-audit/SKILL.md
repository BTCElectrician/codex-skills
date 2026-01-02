---
name: flask-redundancy-audit
description: Audit a Flask backend for redundant logic and write redundancy-audit.md with clusters and a P0 P1 P2 plan.
---

# Flask Redundancy Audit

## Goal
Produce a repo wide redundancy report for a Flask backend. Do not change code. Write a file named redundancy-audit.md in the repo root.

## Workflow

1. Map entry points and structure
   1. Locate the app factory, create_app, or main Flask app file.
   2. Identify blueprints, route modules, service layers, and data access helpers.
   3. Note any shared utilities or middleware that appear in multiple modules.

2. Scan for redundancy clusters
   1. Look for duplicated route handlers, request validation, DB queries, or business rules.
   2. Group similar patterns into clusters with clear evidence.
   3. Each cluster must include file path, symbol, and line range evidence.

3. Classify severity
   1. P0 is correctness risk, inconsistent behavior, or security risk.
   2. P1 is high maintenance cost or common bug surface.
   3. P2 is low risk duplication or style level repetition.

4. Write redundancy-audit.md with the required sections

## Required output format

Create redundancy-audit.md with the following sections and headings.

Progress
Describe what was scanned and any blockers.

Coverage
List all directories, key files, and patterns reviewed. Include commands used if helpful.

Clusters
For each cluster, include
1. Cluster ID
2. Summary
3. Evidence list with file path, symbol, and 1 based line range
4. Severity
5. Notes

Plan
List P0, P1, and P2 items with a short fix approach for each.

## Evidence format example

Cluster R1
Summary: duplicate input validation for user profile updates
Evidence:
1. app/routes/profile.py update_profile lines 44 to 98
2. app/services/user_service.py validate_profile lines 12 to 63
Severity: P1
Notes: use shared validator to avoid drift
