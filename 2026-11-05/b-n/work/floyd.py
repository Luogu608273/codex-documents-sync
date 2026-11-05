import re,json,sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
W=Path(__file__).parent
D=json.loads((W/'scan.json').read_text(encoding='utf-8'))
TOK=re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|//[^\n]*|/\*[\s\S]*?(?:\*/|$)')
def mask(s):return TOK.sub(lambda m:re.sub(r'[^\n]',' ',m[0]),s)
def scopes(code):
 stack=[];pair={}
 for i,ch in enumerate(code):
  if ch in '({[':stack.append((ch,i))
  elif ch in ')}]' and stack and stack[-1][0]=={')':'(','}':'{',']':'['}[ch]:
   _,a=stack.pop();pair[a]=i
 def ws(p):
  while p<len(code) and code[p].isspace():p+=1
  return p
 def end(p):
  p=ws(p)
  if p>=len(code):return p
  if code[p]=='{':return pair.get(p,p)+1
  m=re.match(r'(for|if|while|switch)\s*\(',code[p:])
  if m:
   a=p+m.end()-1;b=pair.get(a,a);e=end(b+1)
   e2=ws(e)
   if m[1]=='if' and code[e2:e2+4]=='else':e=end(e2+4)
   return e
  while p<len(code):
   if code[p]==';':return p+1
   if code[p]=='}':return p
   if p in pair:p=pair[p]+1
   else:p+=1
  return p
 out=[]
 for m in re.finditer(r'\bfor\s*\(',code):
  a=m.end()-1;b=pair.get(a)
  if b is None:continue
  header=code[a+1:b];v=re.search(r'\b(\w+)\s*=(?!=)',header)
  if not v:continue
  out.append({'start':m.start(),'body':b+1,'end':end(b+1),'var':v[1],'header':header})
 return out
F=[]
for d in D:
 if '/subway/' not in d['path']:continue
 code=mask(d['text']);loops=scopes(code)
 for m in re.finditer(r'(\w+)\s*\[\s*i\s*\]\s*\[\s*k\s*\]\s*\+\s*\1\s*\[\s*k\s*\]\s*\[\s*j\s*\]',code):
  enc=[x for x in loops if x['body']<=m.start()<x['end']]
  if len(enc)<3:continue
  nest=enc[-3:];order=''.join(x['var'] for x in nest)
  if order not in ['ijk','ikj']:continue
  line=code.count('\n',0,nest[0]['start'])+1;el=code.count('\n',0,m.end())+1
  item={'path':d['path'],'order':order,'line':line,'end':el,'outer':[x['header'] for x in enc[:-3]],'snippet':'\n'.join(d['text'].splitlines()[line-1:el+1])}
  if not any(f['path']==item['path'] and f['line']==line for f in F):F.append(item)
(W/'floyd_verified.json').write_text(json.dumps(F,ensure_ascii=False,indent=2),encoding='utf-8')
from collections import Counter
print('Floyd',len(F),'files',len(set(f['path'] for f in F)),Counter(f['order'] for f in F))
for f in F:print(f['path'],f['line'],f['order'],'outer',f['outer'],'\n'+f['snippet']+'\n')
