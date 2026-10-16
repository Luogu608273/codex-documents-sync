import base64
import json
import re
from pathlib import Path

source = Path('work/aha.js').read_text(encoding='utf-8')
chunks = json.loads(re.search(r'const \w+=(\[\[.*?\]\]),', source).group(1))
size = int(re.search(r'new Uint8Array\((\d+)\)', source).group(1))
decoded = bytearray(size)
written = set()
for offset, state, encoded in chunks:
    data = base64.b64decode(encoded)
    for i, value in enumerate(reversed(data)):
        state ^= (state << 13) & 0xffffffff
        state ^= state >> 17
        state ^= (state << 5) & 0xffffffff
        decoded[offset+i] = ((value ^ (state & 255))-i) & 255
        written.add(offset+i)
assert len(written) == size
text = decoded.decode('utf-8')
Path('work/aha.decoded.js').write_text(text, encoding='utf-8')
print(text)
