import json
import pathlib
import subprocess
from verify import ROOT, check_a, check_d

result = []
for pid, name in [(3721, 'utopia'), (3722, 'road'), (3723, 'moment'), (3724, 'passerby')]:
    path = ROOT / f'sample-{pid}' / f'ex_{name}1.in'
    data = path.read_text()
    expected = path.with_suffix('.out').read_text()
    for ver in ('std', 'partial'):
        outdir = ROOT / f'io-{name}-{ver}'
        outdir.mkdir(exist_ok=True)
        (outdir / (name + '.in')).write_text(data)
        p = subprocess.run([str(ROOT / f'{name}_{ver}_file.exe')], cwd=str(outdir),
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=8)
        assert p.returncode == 0 and not p.stdout, (name, ver, p.returncode)
        output = (outdir / (name + '.out')).read_text()
        ok = check_a(data, output) if name == 'utopia' else check_d(data, output, expected) if name == 'passerby' else output.split() == expected.split()
        assert ok, (name, ver, output)
        result.append(name + '/' + ver)
(ROOT / 'file-io.json').write_text(json.dumps(result, indent=2))
print('FILE IO PASS', len(result))
