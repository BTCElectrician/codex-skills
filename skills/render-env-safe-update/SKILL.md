---
name: render-env-safe-update
description: Safely update Render service environment variables without wiping existing keys. Use when asked to add or change Render env vars in production/staging, especially when bulk overwrite risk is unacceptable. Run this for key-level updates, redacted backup creation, diff previews, apply-only-after-confirmation, post-update verification, and optional deploy trigger.
---

# Render Env Safe Update

Use `scripts/render_env_safe_update.py` for all Render env var mutations.

## Workflow

1. Identify target service ID.
2. Run dry-run update with proposed key/value pairs.
3. Review backup path and key-level diff.
4. Re-run with `--apply` only after approval.
5. Trigger deploy and wait for completion.
6. Verify behavior with live endpoint checks.

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

Apply changes:

```bash
python3 scripts/render_env_safe_update.py \
  --service-id <service_id> \
  --set KEY_ONE=value1 \
  --set KEY_TWO=value2 \
  --apply
```

Apply and deploy:

```bash
python3 scripts/render_env_safe_update.py \
  --service-id <service_id> \
  --set KEY_ONE=value1 \
  --set KEY_TWO=value2 \
  --apply \
  --deploy-after
```

## Safety Rules

- Never use collection replace endpoints for env vars.
  - Do not use `PUT /services/{id}/env-vars`.
- Always create a backup before apply.
  - Redacted backup is always written.
- Keep secret values out of logs.
  - Default output is key-level only.
- Use single-key updates only.
  - Script updates keys via `PUT /services/{id}/env-vars/{key}`.
- Verify after mutation.
  - Script re-fetches envs and confirms changed keys.

## Backups

- Redacted backup: always created.
- Optional full restore file:

```bash
python3 scripts/render_env_safe_update.py \
  --service-id <service_id> \
  --set KEY=value \
  --write-full-backup \
  --full-backup-file /secure/path/render-env-restore.env
```

Default full backup target (if `--write-full-backup` used without file path):
- `render-env-restore-<timestamp>.env` in backup directory.

Use secure storage for full restore files.

## Troubleshooting

- If auth fails, run `render login` and re-run.
- If key update succeeds but behavior is unchanged, deploy/restart service.
- If CORS fails, verify exact `Origin` values and protocol (`https://`).
- For endpoint-specific checks, use explicit `OPTIONS` probes with `Origin` headers.

## Reference

Read `references/safety-checklist.md` for preflight/apply/postflight checklist.
