import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('repair', Path(__file__).with_name('repair-chat-index.py'))
repair = importlib.util.module_from_spec(spec)
spec.loader.exec_module(repair)


class EngineTests(unittest.TestCase):
    def discover(self, available, env=None, explicit=None, legacy=(), which=None, replies=None):
        paths = {str(Path(p)) for p in available}
        replies = replies or {}
        def run(args, **kwargs):
            answer = replies.get(args[0], b'codex-cli 0.166.0-alpha.5.1\n')
            if isinstance(answer, Exception):
                raise answer
            return SimpleNamespace(returncode=0, stdout=answer)
        with patch.dict(os.environ, env or {}, clear=True), \
             patch.object(Path, 'is_file', lambda p: str(p) in paths), \
             patch.object(Path, 'glob', return_value=[Path(p) for p in legacy]), \
             patch.object(Path, 'stat', return_value=SimpleNamespace(st_mtime=1)), \
             patch.object(repair.shutil, 'which', return_value=which), \
             patch.object(repair.subprocess, 'run', side_effect=run) as probe:
            result = repair.find_codex(explicit)
            return result, probe.call_count

    def test_current_desktop(self):
        target = Path('C:/Local/Programs/Codex/app/resources/codex.exe')
        self.assertEqual(self.discover([target], {'LOCALAPPDATA': 'C:/Local'})[0], target)

    def test_desktop_without_app(self):
        target = Path('C:/Local/Programs/Codex/resources/codex.exe')
        self.assertEqual(self.discover([target], {'LOCALAPPDATA': 'C:/Local'})[0], target)

    def test_legacy(self):
        target = Path('C:/Local/OpenAI/Codex/bin/old/codex.exe')
        self.assertEqual(self.discover([target], {'LOCALAPPDATA': 'C:/Local'}, legacy=[target])[0], target)

    def test_program_files(self):
        target = Path('C:/Program Files/Codex/app/resources/codex.exe')
        self.assertEqual(self.discover([target], {'ProgramFiles': 'C:/Program Files'})[0], target)

    def test_path_fallback(self):
        target = Path('C:/cli/codex.exe')
        self.assertEqual(self.discover([target], which=str(target))[0], target)

    def test_explicit(self):
        target = Path('C:/custom/codex.exe')
        self.assertEqual(self.discover([target], explicit=str(target))[0], target)

    def test_invalid_explicit_does_not_fallback(self):
        with self.assertRaisesRegex(RuntimeError, '--codex-exe'):
            self.discover(['C:/cli/codex.exe'], explicit='C:/missing/codex.exe', which='C:/cli/codex.exe')

    def test_reject_non_cli_version(self):
        target = str(Path('C:/cli/codex.exe'))
        with self.assertRaises(RuntimeError):
            self.discover([target], which=target, replies={target: b'Codex desktop application'})

    def test_timeout_falls_back(self):
        desktop = str(Path('C:/Local/Programs/Codex/app/resources/codex.exe'))
        fallback = str(Path('C:/cli/codex.exe'))
        result, count = self.discover([desktop, fallback], {'LOCALAPPDATA': 'C:/Local'}, which=fallback,
                                     replies={desktop: subprocess.TimeoutExpired('codex', 8)})
        self.assertEqual(result, Path(fallback))
        self.assertEqual(count, 2)

    def test_duplicate_path_probed_once(self):
        target = str(Path('C:/Program Files/Codex/app/resources/codex.exe'))
        fallback = str(Path('C:/cli/codex.exe'))
        result, count = self.discover([target, fallback],
                                     {'ProgramFiles': 'C:/Program Files', 'ProgramW6432': 'C:/Program Files'},
                                     which=fallback, replies={target: b'wrong version'})
        self.assertEqual(result, Path(fallback))
        self.assertEqual(count, 2)

    def test_no_installation(self):
        with self.assertRaisesRegex(RuntimeError, '未找到'):
            self.discover([])


if __name__ == '__main__':
    unittest.main()
