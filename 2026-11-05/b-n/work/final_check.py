import json,re,subprocess,concurrent.futures,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
W=Path(__file__).parent;D=json.loads((W/'scan.json').read_text(encoding='utf-8'))
TOK=re.compile(r'"(?:\\[\s\S]|[^"\\])*"|\'(?:\\[\s\S]|[^\'\\])*\'|//(?:\\\n|[^\n])*|/\*[\s\S]*?(?:\*/|$)')
TYPO=re.compile(r'\b(?:fropen|freeopen|froepen|freopne|frepoen|feropen|freoper|frozpen|feopen|freout|freclose)\s*\(')
candidates=[]
for d in D:
 code=TOK.sub(lambda m:re.sub(r'[^\n]',' ',m[0]),d['text'])
 if (set(d['flags']) & {'header','freopen_typo','int_main_macro','file_stream'} or TYPO.search(code) or d['path'] in ['GD-S02756/hub/hub.cpp','GD-S02722/crystal/crystal.cpp','GD-S03359/migrate.cpp','GD-S00196/subway/subway.cpp','GD-S01451/crystal/crystal.cpp']) and d['path'].endswith('.cpp'):candidates.append(d)
def check(d):
 dst=W/'compile'/d['path'].replace('/','_');dst.write_text(d['text'],encoding='utf-8')
 cmd=[r'C:\TDM-GCC-64\bin\g++.exe','-std=c++14','-fsyntax-only','-fmax-errors=4',str(dst)]
 try:
  r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
  return {'path':d['path'],'returncode':r.returncode,'diagnostics':r.stderr.decode('utf-8',errors='replace')[:6000]}
 except subprocess.TimeoutExpired:return {'path':d['path'],'returncode':None,'diagnostics':'timeout'}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:R=list(ex.map(check,candidates))
(W/'final_compilation.json').write_text(json.dumps(R,ensure_ascii=False,indent=2),encoding='utf-8')
print('checked',len(R),'failed',sum(r['returncode'] not in [0,None] for r in R),'timeout',sum(r['returncode'] is None for r in R))
# Confirm the line splice by inspecting only the preprocessed main function.
d=next(d for d in D if d['path']=='GD-S02722/crystal/crystal.cpp');src=W/'compile'/d['path'].replace('/','_')
r=subprocess.run([r'C:\TDM-GCC-64\bin\g++.exe','-std=c++14','-E','-P',str(src)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
s=r.stdout.decode('utf-8',errors='replace');body=s[s.rfind('int main()'):]
print('02722 preprocessed main contains freopen:', 'freopen(' in body)
(W/'line_splice_check.txt').write_text(body,encoding='utf-8')
