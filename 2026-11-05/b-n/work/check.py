import json,re,sys,subprocess,concurrent.futures
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
W=Path(__file__).parent
D=json.loads((W/'scan.json').read_text(encoding='utf-8'))
TOK=re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?(?:\*/|$)')
def strip(s):return TOK.sub(lambda m:re.sub(r'[^\n]',' ',m[0]) if m[0].startswith(('//','/*')) else m[0],s)
F=[]
loop=re.compile(r'for\s*\([^;\n]*?\b([ijk])\s*=[^;]*;[^;]*;[^)]*\)')
for d in D:
 if '/subway/' not in d['path']:continue
 code=strip(d['text']);loops=list(loop.finditer(code))
 for a,b,c in zip(loops,loops[1:],loops[2:]):
  order=a[1]+b[1]+c[1]
  if order not in ['ijk','ikj']:continue
  if c.end()-a.start()>420:continue
  tail=code[c.end():c.end()+550]
  pat=r'(\w+)\s*\[\s*i\s*\]\s*\[\s*k\s*\]\s*\+\s*\1\s*\[\s*k\s*\]\s*\[\s*j\s*\]'
  m=re.search(pat,tail)
  if not m:continue
  end=c.end()+m.end();line=code.count('\n',0,a.start())+1
  el=code.count('\n',0,end)+1
  F.append({'path':d['path'],'order':order,'line':line,'end':el,'snippet':'\n'.join(d['text'].splitlines()[line-1:el+2])})
(W/'floyd.json').write_text(json.dumps(F,ensure_ascii=False,indent=2),encoding='utf-8')
print('Floyd candidates',len(F),flush=True)
if '--compile' in sys.argv:
 candidates=[d for d in D if set(d['flags']) & {'header','freopen_typo','int_main_macro','file_stream'}]
 (W/'compile').mkdir(exist_ok=True)
 def check(d):
  dst=W/'compile'/d['path'].replace('/','_');dst.write_text(d['text'],encoding='utf-8')
  cmd=[r'C:\TDM-GCC-64\bin\g++.exe','-std=c++14','-fsyntax-only','-fmax-errors=3','-DONLINE_JUDGE',str(dst)]
  try:
   r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
   result={'path':d['path'],'returncode':r.returncode,'diagnostics':r.stderr.decode('utf-8',errors='replace')[:5000]}
  except subprocess.TimeoutExpired:result={'path':d['path'],'returncode':None,'diagnostics':'timeout'}
  return result
 R=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
  for r in ex.map(check,candidates):R.append(r)
 (W/'compilation.json').write_text(json.dumps(R,ensure_ascii=False,indent=2),encoding='utf-8')
 print('compiled',len(R),'failed',sum(r['returncode'] not in [0,None] for r in R),'timeout',sum(r['returncode'] is None for r in R),flush=True)
