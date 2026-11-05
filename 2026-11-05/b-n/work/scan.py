from pathlib import Path
from collections import Counter
import re,json
ROOT=Path(r'C:\Users\605\Downloads\answers')
WORK=Path(__file__).parent
token=re.compile(r'R"([^ ()\\\t\r\n]{0,16})\([\s\S]*?\)\1"|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?(?:\*/|$)')
def read(p):
 b=p.read_bytes()
 for enc in ['utf-8-sig','gb18030']:
  try:s=b.decode(enc);break
  except UnicodeDecodeError:pass
 else:s=b.decode('utf-8',errors='replace');enc='replacement'
 return re.sub(r'\r+\n','\n',s).replace('\r','\n'),enc
def parse(s):
 comments=[]
 def sub(m):
  t=m.group()
  if t.startswith(('//','/*')):
   comments.append({'line':s.count('\n',0,m.start())+1,'text':t})
   return re.sub(r'[^\n]',' ',t)
  return t
 return token.sub(sub,s),comments
data=[]
for p in sorted(ROOT.rglob('*')):
 if not p.is_file():continue
 s,enc=read(p);code,comments=parse(s)
 rel=p.relative_to(ROOT).as_posix(); task=p.parent.name
 calls=[]
 for m in re.finditer(r'\b(freopen|fopen)\s*\(\s*"([^"\n]*)"\s*,\s*"([^"\n]*)"\s*(?:,\s*([^);]*))?',code):
  calls.append({'line':code.count('\n',0,m.start())+1,'fn':m[1],'name':m[2],'mode':m[3],'stream':(m[4] or '').strip()})
 flags=[]
 if p.suffix in ['.cpp','.c']:
  if p.stem!=task:flags.append('source_name')
  if not re.search(r'\bmain\s*\(',code):flags.append('no_main')
  if re.search(r'\b(?:froepen|freopne|frepoen|freopon|fropen|frepopen)\b',code):flags.append('freopen_typo')
  if re.search(r'#\s*define\s+int\s+(?:long|unsigned)',code) and re.search(r'\bint\s+main\s*\(',code):flags.append('int_main_macro')
  for c in calls:
   if c['fn']=='freopen':
    n=c['name'];st=c['stream'];mode=c['mode']
    expected=task+('.in' if st=='stdin' else '.out')
    if n.removeprefix('./')!=expected if hasattr(n,'removeprefix') else (n[2:] if n.startswith('./') else n)!=expected: flags.append('file_name')
    if (st=='stdin' and not mode.startswith('r')) or (st=='stdout' and not mode.startswith('w')):flags.append('file_mode')
    if st not in ['stdin','stdout']:flags.append('file_stream')
  for inc in re.findall(r'#\s*include\s*[<"]([^>"\n]+)',code):
   if ('bits' in inc and inc!='bits/stdc++.h') or inc in ['iostrem','iostream.h','studio.h']:flags.append('header')
 data.append({'path':rel,'encoding':enc,'text':s,'comments':comments,'calls':calls,'flags':sorted(set(flags))})
(WORK/'scan.json').write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
print('files',len(data),'ids',len(set(d['path'].split('/')[0] for d in data)))
print('enc',Counter(d['encoding'] for d in data));print('flags',Counter(f for d in data for f in d['flags']))
interesting=[]
kw=re.compile(r'ccf|akioi|afo|rp\+|保佑|神|佛|迷惑|我是|不会|不会|原神|崩|星穹|明日|鸡|爱|退役|评测|考场|奶龙|牢|作弊|骗|人生|再见|救|sb|fuck|114514|love|give me|please|pls|waifu|miku|nahida|moyu|yuanshen|woc|qwq|喵|草|orz',re.I)
for d in data:
 for c in d['comments']:
  t=c['text']
  if re.search(r'如果.{0,15}(?:AI|LLM)|if you are (?:an? )?(?:ai|llm)',t,re.I):continue
  if kw.search(t) or (len(t)>180 and re.search(r'[a-zA-Z]{3,}\s+[a-zA-Z]{3,}\s+[a-zA-Z]{3,}',t)):
   interesting.append({'path':d['path'],**c})
(WORK/'comments.json').write_text(json.dumps(interesting,ensure_ascii=False),encoding='utf-8')
with (WORK/'comments.txt').open('w',encoding='utf-8') as f:
 for i,c in enumerate(interesting):f.write(f"[{i}] {c['path']}:{c['line']}\n{c['text'][:2800]}\n\n")
print('comments',len(interesting))
with (WORK/'flags.txt').open('w',encoding='utf-8') as f:
 for d in data:
  if d['flags']:f.write(d['path']+' '+','.join(d['flags'])+' '+json.dumps(d['calls'],ensure_ascii=False)+'\n')
