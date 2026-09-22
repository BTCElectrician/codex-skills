# Safety Checklist

## Preflight

1. Prepare locally without authentication; API access is needed for remote preview/apply.
2. Verify CLI identity/workspace only for CLI discovery or an authorized deploy.
3. Confirm exact target service id.
4. Confirm exact key/value pairs to change.
5. Decide whether a canonical local env file is available.
6. Run dry-run first.
7. Confirm redacted backup file exists.
8. Missing remote keys remain unknown even with a local canonical file. Only remote evidence establishes unchanged values.

## Apply

1. Run same command with `--apply`.
2. Use single-key update flow only.
3. Verify changed keys immediately after apply.
4. If `--canonical-env-file` was used, run with `--update-canonical-after-apply`.

## Postflight

1. Trigger deploy if runtime config must reload and authorization covers it.
2. Verify endpoint behavior from real origin(s).
3. Record change summary (service, keys changed, timestamp in CT).

## Important Notes

- Never use `PUT /services/{id}/env-vars` to replace the collection.
- The skill script uses `PUT /services/{id}/env-vars/{key}` one key at a time.
- Render `GET /services/{id}/env-vars` may return a partial snapshot.
- A full backup written without `--canonical-env-file` is only a snapshot, not a guaranteed full restore source.

## CORS Verification Command

```bash
curl -sS -D - -o /dev/null -X OPTIONS 'https://<backend>/api/public/access-requests' \
  -H 'Origin: https://<frontend-domain>' \
  -H 'Access-Control-Request-Method: POST' \
  -H 'Access-Control-Request-Headers: content-type,x-tenant-id'
```

Expected:
- `access-control-allow-origin: https://<frontend-domain>`
- `access-control-allow-methods` includes `POST`
