import contextlib
import copy
import importlib.util
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('prefs', Path(__file__).with_name('codex-preferences.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
P = '11111111-1111-1111-1111-111111111111'
S = '22222222-2222-2222-2222-222222222222'
A = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'
B = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'
C = 'cccccccc-cccc-cccc-cccc-cccccccccccc'


class PreferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.root = Path(self.temp.name).resolve()
        (self.root / '.git').mkdir()
        self.dbpath = self.root / 'state_5.sqlite'
        with contextlib.closing(sqlite3.connect(self.dbpath)) as db:
            db.executescript('''
                CREATE TABLE projects(id TEXT PRIMARY KEY,name TEXT,metadata TEXT,position INTEGER,created_at_ms INTEGER,updated_at_ms INTEGER);
                CREATE TABLE project_roots(project_id TEXT,position INTEGER,path TEXT);
                CREATE TABLE thread_sections(id TEXT PRIMARY KEY,name TEXT,appearance TEXT);
                CREATE TABLE threads(id TEXT PRIMARY KEY,cwd TEXT,project_id TEXT,is_pinned INTEGER,
                    thread_section_id TEXT,section_position REAL,section_entered_at_ms INTEGER);
            ''')
            db.execute('INSERT INTO projects VALUES(?,?,?,0,0,0)', (P, 'Project', '{}'))
            db.execute('INSERT INTO project_roots VALUES(?,0,?)', (P, str(self.root / 'project')))
            db.execute('INSERT INTO threads VALUES(?,?,NULL,0,NULL,NULL,NULL)', (A, str(self.root / 'project')))
            db.commit()
        (self.root / 'config.toml').write_text('model = "old"\n', encoding='utf-8')
        (self.root / '.codex-global-state.json').write_text('{"unrelated":"preserve"}', encoding='utf-8')
        self.data = m.capture(self.root)
        self.data['config']['model'] = 'restored'
        self.data['threads'][A]['is_pinned'] = True
        self.data['sections'] = [{'id': S, 'name': 'Group', 'appearance': None}]
        self.data['threads'][B] = dict(self.data['threads'][A], project_id=P, thread_section_id=S)
        self.save()

    def tearDown(self):
        self.temp.cleanup()

    def save(self):
        (self.root / m.SNAPSHOT).write_bytes(m.encode(m.validate(self.data)))

    def insert_b(self):
        with contextlib.closing(sqlite3.connect(self.dbpath)) as db:
            db.execute('INSERT INTO threads VALUES(?,?,NULL,0,NULL,NULL,NULL)', (B, str(self.root / 'elsewhere')))
            db.commit()

    def files(self):
        return {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}

    def test_check_only_has_no_writes(self):
        before = self.files()
        report = m.restore(self.root, check_only=True)
        self.assertEqual(report['threads'], 1)
        self.assertEqual(report['pending_thread_ids'], [B])
        self.assertEqual(before, self.files())

    def test_restore_available_preserves_pending_and_unrelated(self):
        snapshot = (self.root / m.SNAPSHOT).read_bytes()
        report = m.restore(self.root)
        self.assertEqual(report['pending_threads'], 1)
        actual = m.capture(self.root)
        self.assertTrue(actual['threads'][A]['is_pinned'])
        self.assertNotIn(B, actual['threads'])
        self.assertEqual(actual['config']['model'], 'restored')
        state = m.read_json(self.root / '.codex-global-state.json')
        self.assertEqual(state['unrelated'], 'preserve')
        self.assertNotIn(B, state['pinned-thread-ids'])
        self.assertEqual(snapshot, (self.root / m.SNAPSHOT).read_bytes())
        self.assertEqual(m.read_json(m.baseline_path(self.root))['pending_thread_ids'], [B])

    def test_export_retains_absent_preferences(self):
        m.restore(self.root)
        self.assertEqual(m.export(self.root)['pending_threads'], 1)
        self.assertEqual(m.read_json(self.root / m.SNAPSHOT)['threads'][B], self.data['threads'][B])

    def test_export_after_import_does_not_erase_pending_preferences(self):
        m.restore(self.root)
        self.insert_b()
        self.assertEqual(m.export(self.root)['pending_threads'], 1)
        self.assertEqual(m.read_json(self.root / m.SNAPSHOT)['threads'][B], self.data['threads'][B])
        self.assertIsNone(m.capture(self.root)['threads'][B]['project_id'])

    def test_later_restore_applies_pending(self):
        m.restore(self.root)
        self.insert_b()
        m.export(self.root)
        report = m.restore(self.root)
        self.assertEqual(report['pending_threads'], 0)
        self.assertEqual(m.capture(self.root)['threads'][B], self.data['threads'][B])

    def test_menu_11_12_11_keeps_inferred_project_and_pending(self):
        m.restore(self.root)
        report = m.infer_projects(self.root)
        self.assertEqual(report['inferred_project_links'], 1)
        self.assertEqual(report['pending_threads'], 1)
        m.restore(self.root)
        self.assertEqual(m.capture(self.root)['threads'][A]['project_id'], P)
        self.assertEqual(m.read_json(self.root / m.SNAPSHOT)['threads'][B], self.data['threads'][B])

    def test_infer_applies_newly_imported_pending_before_export(self):
        m.restore(self.root)
        self.insert_b()
        report = m.infer_projects(self.root)
        self.assertEqual(report['pending_threads'], 0)
        self.assertEqual(m.capture(self.root)['threads'][B], self.data['threads'][B])

    def test_unacknowledged_snapshot_still_blocks_export_and_infer(self):
        before = self.files()
        for operation in (m.export, m.infer_projects):
            with self.assertRaisesRegex(RuntimeError, '尚未恢复'):
                operation(self.root)
        self.assertEqual(before, self.files())

    def test_infer_check_only_has_no_writes(self):
        m.restore(self.root)
        before = self.files()
        self.assertEqual(m.infer_projects(self.root, check_only=True)['pending_threads'], 1)
        self.assertEqual(before, self.files())

    def test_project_mapping_for_pending(self):
        current = m.capture(self.root)
        current['projects'][0]['id'] = C
        current['projects'][0]['legacy_id'] = C
        merged = m.retain_pending(current, self.data)
        self.assertEqual(merged['threads'][B]['project_id'], C)

    def test_project_collision_stops(self):
        current = m.capture(self.root)
        current['projects'][0]['roots'] = ['C:/different']
        with self.assertRaisesRegex(RuntimeError, '冲突'):
            m.retain_pending(current, self.data)

    def test_source_changes_prevent_apply(self):
        plan = m.plan_restore(self.root, self.data)
        plan['input_hashes'][m.SNAPSHOT] = m.digest((self.root / m.SNAPSHOT).read_bytes())
        self.data['config']['model'] = 'changed'
        self.save()
        before = self.files()
        with self.assertRaisesRegex(RuntimeError, '状态已变化'):
            m.apply_plan(self.root, plan)
        self.assertEqual(before, self.files())


if __name__ == '__main__':
    unittest.main()
