#!/usr/bin/env python3
"""Safely patch Render env vars one key at a time.

Design goals:
- Never replace whole env var collections
- Always produce a redacted backup before apply
- Default to dry-run preview
- Keep secrets out of stdout by default
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, Tuple
from zoneinfo import ZoneInfo

import requests

CT = ZoneInfo("America/Chicago")
API_BASE = "https://api.render.com/v1"
KEY_PATTERN = re.compile(r"^[A-Z][A-Z0-9_]*$")


class RenderEnvError(RuntimeError):
    """Raised for recoverable workflow failures."""


@dataclass
class BackupPaths:
    redacted_json: Path
    full_env: Path | None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Safely update Render env vars with backups and verification")
    parser.add_argument("--service-id", required=True, help="Render service id (e.g., srv-xxxx)")
    parser.add_argument(
        "--set",
        dest="updates",
        action="append",
        default=[],
        help="Key/value assignment in KEY=VALUE format. Repeat for multiple keys.",
    )
    parser.add_argument(
        "--backup-dir",
        default="docs/ops",
        help="Directory for backup artifacts (default: docs/ops)",
    )
    parser.add_argument(
        "--write-full-backup",
        action="store_true",
        help="Write full restore .env backup (contains secrets; store securely)",
    )
    parser.add_argument(
        "--full-backup-file",
        default="",
        help="Explicit full backup file path (used with --write-full-backup)",
    )
    parser.add_argument(
        "--api-key",
        default="",
        help="Render API key override (default: RENDER_API_KEY or ~/.render/cli.yaml)",
    )
    parser.add_argument(
        "--canonical-env-file",
        default="",
        help="Optional local canonical .env restore file used for accurate diff classification",
    )
    parser.add_argument("--apply", action="store_true", help="Apply updates (default is dry-run)")
    parser.add_argument(
        "--deploy-after",
        action="store_true",
        help="Trigger 'render deploys create <service-id> --wait' after successful apply",
    )
    parser.add_argument(
        "--show-values",
        action="store_true",
        help="Print old/new values in diff output (avoid for secrets)",
    )
    parser.add_argument(
        "--update-canonical-after-apply",
        action="store_true",
        help="Merge applied keys into --canonical-env-file after successful verification",
    )
    args = parser.parse_args()

    if not args.updates:
        parser.error("At least one --set KEY=VALUE is required")

    if args.deploy_after and not args.apply:
        parser.error("--deploy-after requires --apply")

    if args.full_backup_file and not args.write_full_backup:
        parser.error("--full-backup-file requires --write-full-backup")

    if args.update_canonical_after_apply and not args.canonical_env_file:
        parser.error("--update-canonical-after-apply requires --canonical-env-file")

    return args


def now_ts() -> str:
    return datetime.now(CT).strftime("%Y%m%d-%H%M%S")


def load_render_api_key(explicit_key: str = "") -> str:
    if explicit_key:
        return explicit_key.strip()

    env_key = (os.getenv("RENDER_API_KEY") or "").strip()
    if env_key:
        return env_key

    cfg_path = Path.home() / ".render" / "cli.yaml"
    if not cfg_path.exists():
        raise RenderEnvError("No API key found (set RENDER_API_KEY or login via Render CLI)")

    text = cfg_path.read_text(encoding="utf-8", errors="ignore")
    for line in text.splitlines():
        m = re.match(r"^\s*(?:key|token):\s*(\S+)\s*$", line)
        if m:
            return m.group(1).strip()

    raise RenderEnvError("Could not parse API key from ~/.render/cli.yaml")


def parse_updates(raw_updates: Iterable[str]) -> Dict[str, str]:
    parsed: Dict[str, str] = {}
    for item in raw_updates:
        if "=" not in item:
            raise RenderEnvError("Invalid --set (expected KEY=VALUE; input redacted)")
        key, value = item.split("=", 1)
        key = key.strip()
        if not KEY_PATTERN.match(key):
            raise RenderEnvError(
                f"Invalid env key '{key}'. Use upper snake case like FRONTEND_ORIGIN"
            )
        parsed[key] = value
    return parsed


def parse_env_file(path_str: str) -> Dict[str, str]:
    path = Path(path_str).expanduser().resolve()
    if not path.exists():
        raise RenderEnvError(f"Canonical env file not found: {path}")

    env_map: Dict[str, str] = {}
    for idx, raw_line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise RenderEnvError(f"Invalid env line in {path} at line {idx} (content redacted)")
        key, value = line.split("=", 1)
        key = key.strip()
        if not KEY_PATTERN.match(key):
            raise RenderEnvError(f"Invalid env key {key!r} in {path} at line {idx}")
        value = value.strip()
        if value.startswith(("\"", "[")) or value in {"true", "false", "null"}:
            try:
                parsed_value = json.loads(value)  # ubs:ignore -- JSONDecodeError handled immediately below
                value = "" if parsed_value is None else str(parsed_value)
            except json.JSONDecodeError:
                pass
        env_map[key] = value
    return env_map


def api_get_env_vars(api_key: str, service_id: str) -> Dict[str, str]:
    url = f"{API_BASE}/services/{service_id}/env-vars"
    resp = requests.get(url, headers={"Authorization": f"Bearer {api_key}"}, timeout=30)
    if resp.status_code >= 400:
        raise RenderEnvError(f"GET env vars failed ({resp.status_code})")

    rows = resp.json()
    env_map: Dict[str, str] = {}
    for row in rows:
        env_var = row.get("envVar") or {}
        key = env_var.get("key")
        if not key:
            continue
        env_map[key] = str(env_var.get("value", ""))
    return env_map


def write_backups(
    backup_dir: Path,
    service_id: str,
    service_name: str,
    current_env: Dict[str, str],
    write_full_backup: bool,
    full_backup_file: str,
) -> BackupPaths:
    backup_dir.mkdir(parents=True, exist_ok=True)
    ts = now_ts()

    redacted_path = backup_dir / f"render-env-backup-{ts}-redacted.json"
    redacted = {
        "generated_at_ct": datetime.now(CT).isoformat(),
        "service_id": service_id,
        "service_name": service_name,
        "count": len(current_env),
        "env_vars": [{"key": k, "value_redacted": True} for k in sorted(current_env)],
    }
    redacted_path.write_text(json.dumps(redacted, indent=2) + "\n", encoding="utf-8")

    full_path: Path | None = None
    if write_full_backup:
        full_path = Path(full_backup_file).expanduser().resolve() if full_backup_file else backup_dir / f"render-env-restore-{ts}.env"
        lines = [f"{k}={json.dumps(v)}" for k, v in sorted(current_env.items())]
        full_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        os.chmod(full_path, 0o600)

    return BackupPaths(redacted_json=redacted_path, full_env=full_path)


def compute_diff(current_env: Dict[str, str], updates: Dict[str, str]) -> Tuple[Dict[str, str], Dict[str, str], Dict[str, str]]:
    unchanged: Dict[str, str] = {}
    changed_existing: Dict[str, str] = {}
    missing_from_baseline: Dict[str, str] = {}

    for key, new_value in updates.items():
        if key not in current_env:
            missing_from_baseline[key] = new_value
        elif current_env[key] == new_value:
            unchanged[key] = new_value
        else:
            changed_existing[key] = new_value

    return unchanged, changed_existing, missing_from_baseline


def apply_updates(api_key: str, service_id: str, updates: Dict[str, str]) -> None:
    for key, value in updates.items():
        url = f"{API_BASE}/services/{service_id}/env-vars/{key}"
        resp = requests.put(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={"value": value},
            timeout=30,
        )
        if resp.status_code >= 400:
            raise RenderEnvError(f"PUT {key} failed ({resp.status_code})")


def verify_updates(current_env: Dict[str, str], updates: Dict[str, str]) -> None:
    bad = [k for k, v in updates.items() if current_env.get(k) != v]
    if bad:
        raise RenderEnvError(f"Verification failed for keys: {', '.join(bad)}")


def run_deploy(service_id: str) -> None:
    cmd = [
        "render",
        "deploys",
        "create",
        service_id,
        "--wait",
        "--confirm",
        "-o",
        "text",
    ]
    proc = subprocess.run(cmd, check=False)
    if proc.returncode != 0:
        raise RenderEnvError("Deploy command failed")


def write_env_file(path: Path, env_map: Dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"{k}={json.dumps(v)}" for k, v in sorted(env_map.items())]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    os.chmod(path, 0o600)


def print_plan(
    service_id: str,
    backups: BackupPaths,
    unchanged: Dict[str, str],
    changed_existing: Dict[str, str],
    missing_from_baseline: Dict[str, str],
    baseline_env: Dict[str, str],
    current_env: Dict[str, str],
    updates: Dict[str, str],
    show_values: bool,
    baseline_label: str,
    baseline_path: Path | None,
    baseline_warning: str | None,
) -> None:
    print(f"service_id: {service_id}")
    print(f"backup_redacted: {backups.redacted_json}")
    if backups.full_env:
        print(f"backup_full: {backups.full_env} (chmod 600)")
        if baseline_path is None:
            print("warning: full backup file was written from the Render API snapshot and may be partial")

    print(f"remote_snapshot_count: {len(current_env)}")
    print(f"diff_baseline: {baseline_label}")
    if baseline_path:
        print(f"diff_baseline_path: {baseline_path}")
    if baseline_warning:
        print(f"warning: {baseline_warning}")
    print(f"update_count_requested: {len(updates)}")
    print(f"update_count_effective: {len(changed_existing) + len(missing_from_baseline)}")
    print(f"unchanged_count: {len(unchanged)}")

    if unchanged:
        print("unchanged_keys:")
        for key in sorted(unchanged):
            print(f"  - {key}")

    if changed_existing:
        print("changed_existing_keys:")
        for key in sorted(changed_existing):
            if show_values:
                print(f"  - {key}: {baseline_env.get(key)!r} -> {changed_existing[key]!r}")
            else:
                print(f"  - {key}")

    if missing_from_baseline:
        bucket_name = "keys_missing_from_render_snapshot"
        print(f"{bucket_name}:")
        for key in sorted(missing_from_baseline):
            if show_values:
                before = "<not-returned-by-render>"
                print(f"  - {key}: {before} -> {missing_from_baseline[key]!r}")
            else:
                print(f"  - {key}")


def main() -> int:
    args = parse_args()

    try:
        updates = parse_updates(args.updates)
        api_key = load_render_api_key(args.api_key)

        current_env = api_get_env_vars(api_key, args.service_id)
        canonical_env = parse_env_file(args.canonical_env_file) if args.canonical_env_file else None
        baseline_env = current_env  # Only remote evidence can establish a no-op.
        baseline_path = (
            Path(args.canonical_env_file).expanduser().resolve()
            if args.canonical_env_file
            else None
        )
        baseline_label = "Render API snapshot (canonical file is restore context only)"
        baseline_warning = "Render GET /env-vars can be partial. Missing keys are unknown; a local canonical file cannot prove current remote values."
        backups = write_backups(
            backup_dir=Path(args.backup_dir).expanduser().resolve(),
            service_id=args.service_id,
            service_name="unknown",
            current_env=canonical_env if canonical_env is not None else current_env,
            write_full_backup=args.write_full_backup,
            full_backup_file=args.full_backup_file,
        )

        unchanged, changed_existing, missing_from_baseline = compute_diff(baseline_env, updates)
        effective_updates = {**changed_existing, **missing_from_baseline}

        print_plan(
            service_id=args.service_id,
            backups=backups,
            unchanged=unchanged,
            changed_existing=changed_existing,
            missing_from_baseline=missing_from_baseline,
            baseline_env=baseline_env,
            current_env=current_env,
            updates=updates,
            show_values=args.show_values,
            baseline_label=baseline_label,
            baseline_path=baseline_path,
            baseline_warning=baseline_warning,
        )

        if not effective_updates:
            print("no_changes: all requested key values already match")
            return 0

        if not args.apply:
            print("mode: dry-run (no mutations applied)")
            print("next: re-run with --apply to perform key-level updates")
            return 0

        apply_updates(api_key, args.service_id, effective_updates)
        refreshed = api_get_env_vars(api_key, args.service_id)
        verify_updates(refreshed, effective_updates)
        if canonical_env is not None and args.update_canonical_after_apply:
            canonical_env.update(effective_updates)
            write_env_file(baseline_path, canonical_env)
            print(f"canonical_update: wrote merged keys to {baseline_path}")
        print("apply_status: success")
        print(f"verified_keys: {', '.join(sorted(effective_updates))}")

        if args.deploy_after:
            run_deploy(args.service_id)
            print("deploy_status: success")
        else:
            print("deploy_status: skipped (use --deploy-after or run render deploys create manually)")

        return 0
    except RenderEnvError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except requests.RequestException as exc:
        print("error: network request failed (details redacted)", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
