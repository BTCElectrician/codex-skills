# Safety Checklist

## Preflight

1. Confirm exact target service id.
2. Confirm exact key/value pairs to change.
3. Run dry-run first.
4. Confirm redacted backup file exists.
5. Decide whether full backup file is needed.

## Apply

1. Run same command with `--apply`.
2. Use single-key update flow only.
3. Verify changed keys immediately after apply.

## Postflight

1. Trigger deploy if runtime config must reload.
2. Verify endpoint behavior from real origin(s).
3. Record change summary (service, keys changed, timestamp in CT).

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
