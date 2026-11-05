import json,re,sys
from pathlib import Path
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')
W=Path(__file__).parent
D=json.loads((W/'scan.json').read_text(encoding='utf-8'))
# Comments consume escaped newlines, as C/C++ line splicing requires.
TOK=re.compile(r'"(?:\\[\s\S]|[^"\\])*"|\'(?:\\[\s\S]|[^\'\\])*\'|//(?:\\\n|[^\n])*|/\*[\s\S]*?(?:\*/|$)')
def strip(s,strings=False):
 return TOK.sub(lambda m:re.sub(r'[^\n]',' ',m[0]) if strings or m[0].startswith(('//','/*')) else m[0],s)
def preprocess(s):
 macros={'__cplusplus':'201402','__GNUC__':'10','__linux__':'1','__unix__':'1'};stack=[];on=True;out=[];unknown=[]
 def ev(expr):
  expr=re.sub(r'defined\s*(?:\(\s*(\w+)\s*\)|(\w+))',lambda m:str(int((m[1] or m[2]) in macros)),expr)
  for _ in range(6):
   nex=re.sub(r'\b[A-Za-z_]\w*\b',lambda m:macros.get(m[0],'0'),expr)
   if nex==expr:break
   expr=nex
  expr=re.sub(r'(?<=\d)[uUlL]+\b','',expr).replace('&&',' and ').replace('||',' or ')
  expr=re.sub(r'!(?!=)',' not ',expr)
  if re.search(r'[^\d\s()<>!=+*/%&|.^~\-a-z]',expr):raise ValueError(expr)
  return bool(eval(expr,{'__builtins__':{}},{}))
 for num,line in enumerate(s.splitlines(keepends=True),1):
  m=re.match(r'\s*#\s*(\w+)\s*(.*)',line)
  if m:
   op,arg=m.groups()
   if op in ['if','ifdef','ifndef']:
    try:yes=(arg.strip() in macros) if op=='ifdef' else (arg.strip() not in macros) if op=='ifndef' else ev(arg)
    except Exception:yes=False;unknown.append((num,arg))
    stack.append([on,yes]);on=on and yes
   elif op=='else' and stack:
    parent,taken=stack[-1];on=parent and not taken;stack[-1][1]=True
   elif op=='elif' and stack:
    parent,taken=stack[-1]
    try:yes=ev(arg)
    except Exception:yes=False;unknown.append((num,arg))
    on=parent and not taken and yes;stack[-1][1]=taken or yes
   elif op=='endif' and stack:on=stack.pop()[0]
   elif op=='define' and on:
    mm=re.match(r'(\w+)(.*)',arg)
    if mm:macros[mm[1]]=mm[2].strip() or '1'
   elif op=='undef' and on:macros.pop(arg.strip(),None)
   out.append(re.sub(r'[^\n]',' ',line))
  else:out.append(line if on else re.sub(r'[^\n]',' ',line))
 return ''.join(out),macros,unknown
IO=re.compile(r'\b(?:freopen(?:64|_s)?|fopen(?:64|_s)?|[io]?fstream|[io]?filebuf|open(?:64)?|openat|creat|dup2)\b')
R=[]
for d in D:
 if not d['path'].endswith(('.cpp','.c','.pas')):continue
 s=d['text'];clean=strip(s);active,mac,unknown=preprocess(clean)
 code=strip(active,True)
 macroio={k for k,v in mac.items() if IO.search(v)}
 for _ in range(5):
  for k,v in mac.items():
   if set(re.findall(r'\b\w+\b',v))&macroio:macroio.add(k)
 hasio=bool(IO.search(code) or set(re.findall(r'\b\w+\b',code))&macroio)
 if d['path'].endswith('.pas'):hasio=hasio or bool(re.search(r'\b(?:assign|reset|rewrite)\s*\(',s,re.I))
 commented=any(c['text'].startswith('//') and re.match(r'//\s*freopen\s*\(',c['text']) for c in d['comments'])
 calls=[]
 for c in d['calls']:
  ls=active.splitlines()
  if c['line']<=len(ls) and re.search(r'\b(?:freopen|fopen)\b',ls[c['line']-1]):calls.append(c)
 task=d['path'].split('/')[-2]
 gin=any(c['name'] in [task+'.in','./'+task+'.in'] and c['mode']=='r' and c['stream']=='stdin' for c in calls)
 gout=any(c['name'] in [task+'.out','./'+task+'.out'] and c['mode']=='w' and c['stream']=='stdout' for c in calls)
 R.append({'path':d['path'],'empty':not s.strip(),'hasio':hasio,'commented':commented,'literal_good_pair':gin and gout,'calls':calls,'unknown':unknown})
(W/'io_audit.json').write_text(json.dumps(R,ensure_ascii=False,indent=2),encoding='utf-8')
print(Counter(('empty' if r['empty'] else 'comment_noio' if r['commented'] and not r['hasio'] else 'never_io' if not r['hasio'] else 'comment_with_io' if r['commented'] else 'io') for r in R))
print('unknown',[(r['path'],r['unknown']) for r in R if r['unknown']])
print('pascal',[(r['path'],r['hasio']) for r in R if r['path'].endswith('.pas')])
