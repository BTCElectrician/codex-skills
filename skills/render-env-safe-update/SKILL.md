---
name: render-env-safe-update
description: Safely update Render service environment variables without wiping existing keys. Use when asked to add or change Render env vars in production/staging, especially when bulk overwrite risk is unacceptable. Run this for key-level updates, redacted backup creation, diff previews, apply-only-after-confirmation, post-update verification, and optional deploy trigger.
---

# Render Env Safe Update

Use `scripts/render_env_safe_update.py` relative to this skill directory for
Render env var mutations. Its dry run is a read-only remote preview, not an
offline check. Local command preparation and offline tests need no credentials.
Never pass `--show-values` for secret-bearing updates. A local canonical file
is restore context; only the remote snapshot establishes unchanged values.

## Workflow

1. Inspect the requested scope and helper locally. Verify API access before
   a remote preview/update; verify CLI identity and workspace only when using
   the CLI for service discovery or an authorized deployment.
2. Identify target service ID.
3. Prefer an existing local canonical env file when one exists.
4. Run dry-run update with proposed key/value pairs.
5. Review the redacted backup path and key-level diff.
6. Re-run with `--apply` only within approval for the exact service and key changes.
7. Trigger deploy and wait only when required and covered by authorization.
8. Verify behavior with live endpoint checks.

## Commands

List services:

```bash
render -o json services
```

Dry run (no mutation):

```bash
python3 scripts/render_env_safe_update.py \
  --service-id <service_id> \
  --set KEY_ONE=value1 \
  --set KEY_TWO=value2
```

Dry run with a canonical local env file as restore context:

```bash
python3 scripts/render_env_safe_update.py \
  --service-id <service_id> \
  --canonical-env-file docs/ops/render-env-canonical.env \
  --set KEY_ONE=value1 \
  --set KEY_TWO=value2
```

Apply changes:

```bash
python3 scripts/render_env_safe_update.py \
  --service-id <service_id> \
  --canonical-env-file docs/ops/render-env-canonical.env \
  --set KEY_ONE=value1 \
  --set KEY_TWO=value2 \
  --apply \
  --update-canonical-after-apply
```

Apply and deploy:

```bash
python3 scripts/render_env_safe_update.py \
  --service-id <service_id> \
  --canonical-env-file docs/ops/render-env-canonical.env \
  --set KEY_ONE=value1 \
  --set KEY_TWO=value2 \
  --apply \
  --update-canonical-after-apply \
  --deploy-after
```

## Safety Rules

- Missing authentication blocks only dependent remote operations. Continue
  local inspection, command preparation, and offline validation. Use existing
  credential routing; do not initiate login or expose secrets during unrelated work.
- Never use collection replace endpoints for env vars.
  - Do not use `PUT /services/{id}/env-vars`.
- Always create a backup before apply.
  - Redacted backup is always written.
- Treat Render env snapshots as potentially partial; local restore files may also be stale.
  - `GET /services/{id}/env-vars` may not return every key.
  - Without `--canonical-env-file`, keys reported as missing from the snapshot are not proven to be new.
- Keep secret values out of logs.
  - Default output is key-level only.
- Use single-key updates only.
  - Script updates keys via `PUT /services/{id}/env-vars/{key}`.
- Keep a canonical env restore file outside git when you have one.
  - Prefer `docs/ops/render-env-canonical.env` or another local-only secure path.
- Verify after mutation.
  - Script re-fetches envs and confirms changed keys.

## Backups

- Redacted backup: always created.
- Optional full backup file:

```bash
python3 scripts/render_env_safe_update.py \
  --service-id <service_id> \
  --canonical-env-file docs/ops/render-env-canonical.env \
  --set KEY=value \
  --write-full-backup \
  --full-backup-file /secure/path/render-env-restore.env
```

Default full backup target:
- `render-env-restore-<timestamp>.env` in backup directory.

Important:
- If you provide `--canonical-env-file`, the full backup is based on that canonical file.
- If you do not provide `--canonical-env-file`, the full backup is only a Render API snapshot and may be partial.
- Use secure storage for any full backup file.

## Troubleshooting

- If auth fails, report the dependent operation and follow the authorized
  credential workflow. Do not initiate login or credential changes automatically.
- If the dry-run shows `keys_missing_from_render_snapshot`, the snapshot is incomplete for those keys.
  - Re-run with `--canonical-env-file` to retain restore context; it does not prove remote values.
- If behavior is unchanged, inspect whether a reload is required; deploy/restart
  only within applicable authorization.
- If CORS fails, verify exact `Origin` values and protocol (`https://`).
- For endpoint-specific checks, use explicit `OPTIONS` probes with `Origin` headers.

## Reference

Read `references/safety-checklist.md` for preflight/apply/postflight checklist.
