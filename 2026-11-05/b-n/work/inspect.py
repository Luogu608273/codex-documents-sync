import json,re,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
D=json.loads(Path('work/scan.json').read_text(encoding='utf-8'))
C=json.loads(Path('work/comments.json').read_text(encoding='utf-8'))
if sys.argv[1]=='comments':
 for i in range(int(sys.argv[2]),min(int(sys.argv[3]),len(C))):
  c=C[i];t=c['text']
  lines=[x.strip() for x in t.splitlines() if re.search(r'[\u4e00-\u9fff]|ccf|afo|love|rp\+|akioi|fuck|please|give me|miku|nahida|genshin',x,re.I)]
  if lines:print(f"[{i}] {c['path']}:{c['line']} ({len(t)} chars) "+' | '.join(lines)[:500])
elif sys.argv[1]=='getcomments':
 for i in map(int,sys.argv[2:]):
  c=C[i];print(f"[{i}] {c['path']}:{c['line']}\n{c['text'][:6000]}\n")
elif sys.argv[1]=='files':
 for pat in sys.argv[2:]:
  for d in D:
   if pat in d['path']:
    print('\n=== '+d['path']+' ===')
    for i,l in enumerate(d['text'].splitlines(),1):print(f'{i}: {l}')
elif sys.argv[1]=='flag':
 for d in D:
  if sys.argv[2] in d['flags']:
   print(d['path'],d['flags'])
   ls=d['text'].splitlines()
   for i,l in enumerate(ls):
    if re.search(r'fre|include|define int|main\(',l):print(f'{i+1}: {l[:200]}')
