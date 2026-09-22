"""Offline contracts; all remote access and credential loading are replaced."""
import contextlib
import importlib.util  # ubs:ignore -- modern importlib, not deprecated imp
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch, Mock

path = Path(__file__).parents[1] / 'scripts/render_env_safe_update.py'
spec = importlib.util.spec_from_file_location('render_safe', path)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class SafeUpdateTest(unittest.TestCase):
    def test_only_key_endpoint(self):
        with patch.object(mod.requests, 'put', return_value=Mock(status_code=200)) as put:
            mod.apply_updates('fake', 'srv-test', {'EXAMPLE': 'synthetic'})
        self.assertEqual(put.call_args.args[0], 'https://api.render.com/v1/services/srv-test/env-vars/EXAMPLE')
        self.assertEqual(put.call_args.kwargs['json'], {'value': 'synthetic'})

    def test_provider_error_does_not_echo_body(self):
        with patch.object(mod.requests, 'put', return_value=Mock(status_code=400, text='synthetic-secret')):
            with self.assertRaises(mod.RenderEnvError) as exc:
                mod.apply_updates('fake', 'srv-test', {'EXAMPLE': 'synthetic'})
        self.assertNotIn('synthetic-secret', str(exc.exception))

    def test_invalid_local_line_redacted(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'fixture'; p.write_text('synthetic-secret-without-equals')
            with self.assertRaises(mod.RenderEnvError) as exc:
                mod.parse_env_file(str(p))
            self.assertNotIn('synthetic-secret', str(exc.exception))

    def test_backup_redacts_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = mod.write_backups(Path(tmp), 'srv-test', 'test', {'EXAMPLE': 'synthetic-secret'}, False, '')
            self.assertNotIn('synthetic-secret', result.redacted_json.read_text())
            self.assertIsNone(result.full_env)

    def test_verify_fails_closed(self):
        with self.assertRaises(mod.RenderEnvError):
            mod.verify_updates({}, {'EXAMPLE': 'synthetic'})

    def exercise(self, apply):
        with tempfile.TemporaryDirectory() as tmp:
            canonical = Path(tmp) / 'canonical'; canonical.write_text('EXAMPLE="requested"\n')
            argv = ['runner', '--service-id', 'srv-test', '--set', 'EXAMPLE=requested',
                    '--canonical-env-file', str(canonical), '--backup-dir', tmp]
            if apply: argv.append('--apply')
            reads = [{'EXAMPLE': 'remote-old'}, {'EXAMPLE': 'requested'}]
            with patch.object(sys, 'argv', argv), patch.object(mod, 'load_render_api_key', return_value='fake'), \
                 patch.object(mod, 'api_get_env_vars', side_effect=reads), \
                 patch.object(mod, 'apply_updates') as update, patch.object(mod, 'run_deploy') as deploy, \
                 contextlib.redirect_stdout(io.StringIO()) as output:
                result = mod.main()
            self.assertEqual(result, 0)
            deploy.assert_not_called()
            self.assertNotIn('remote-old', output.getvalue())
            if apply: update.assert_called_once_with('fake', 'srv-test', {'EXAMPLE': 'requested'})
            else: update.assert_not_called()

    def test_stale_canonical_cannot_suppress_remote_update(self):
        self.exercise(True)

    def test_dry_run_never_applies_or_deploys(self):
        self.exercise(False)


if __name__ == '__main__':
    unittest.main()
