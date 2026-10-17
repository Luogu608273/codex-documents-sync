"""Select the requested AMD inference device without rewriting unrelated settings."""
import argparse
import copy
import csv
import hashlib
import io
import json
import re
import subprocess
from datetime import datetime
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--dry-run', action='store_true')
args = parser.parse_args()
target = Path(r'D:\MAA-Arknights-Assistant\config\gui.new.json')
changes = {
    'UseGpu': True,
    'GpuDescription': 'Radeon RX550/550 Series',
    # Official selection code falls back to the unique adapter description.
    'GpuInstancePath': '',
}
if not args.dry_run:
    processes = subprocess.run(
        ['tasklist.exe', '/FI', 'IMAGENAME eq MAA.exe', '/FO', 'CSV', '/NH'],
        check=True, capture_output=True, text=True, encoding='mbcs',
    )
    if any(row and row[0].casefold() == 'maa.exe' for row in csv.reader(io.StringIO(processes.stdout))):
        raise SystemExit('MAA is still running. No configuration was written.')

raw = target.read_bytes()
text = raw.decode('utf-8-sig')
before = json.loads(text)
expected = copy.deepcopy(before)
expected['Gui']['Performance'].update(changes)
updated = text
for key, value in changes.items():
    value_pattern = r'(?:true|false)' if isinstance(value, bool) else r'"(?:\\.|[^"\\])*"'
    pattern = r'("' + re.escape(key) + r'"\s*:\s*)' + value_pattern
    updated, count = re.subn(
        pattern, lambda m: m.group(1) + json.dumps(value, ensure_ascii=False), updated,
    )
    if count != 1:
        raise SystemExit(f'Expected one {key} field, found {count}. No write.')
if json.loads(updated) != expected:
    raise SystemExit('Unrelated JSON data would change. No write.')

if args.dry_run:
    print(json.dumps({'dry_run': True, 'requested_performance': changes}, ensure_ascii=False))
else:
    output = (b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'') + updated.encode('utf-8')
    record = {
        'time': datetime.now().astimezone().isoformat(),
        'before_performance': {k: before['Gui']['Performance'][k] for k in changes},
        'after_performance': changes,
        'original_sha256': hashlib.sha256(raw).hexdigest(),
        'written_sha256': hashlib.sha256(output).hexdigest(),
        'other_configuration_preserved': True,
    }
    target.write_bytes(output)
    if target.read_bytes() != output:
        raise SystemExit('Write verification failed.')
    Path(__file__).with_name('applied.json').write_text(
        json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8',
    )
    print(json.dumps({'verified': True, 'performance': changes}, ensure_ascii=False))
