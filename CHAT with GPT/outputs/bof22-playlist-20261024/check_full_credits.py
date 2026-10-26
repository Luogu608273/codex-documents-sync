from pathlib import Path
from urllib.request import Request,urlopen
from bs4 import BeautifulSoup
from urllib.parse import parse_qs,urlparse
import json,re,sys,unicodedata
sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).resolve().parent
url='https://manbow.nothing.sh/event/event.cgi?action=List_def&event=152'
with urlopen(Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as f:
    data=f.read()
(P/'sources/entries-full.html').write_bytes(data)
soup=BeautifulSoup(data,'html.parser')
entries={x['id']:x for x in json.loads((P/'entries.json').read_text(encoding='utf-8'))}
ids=[]
for a in soup.select('.pricing-title h4 a'):
    i=int(parse_qs(urlparse(a['href']).query)['num'][0])
    ids.append(i)
    card=a.find_parent(class_='pricing-box')
    hs=card.select('.pricing-title .center h5')
    entries[i]['full_artist_display']=hs[-1].get_text(' ',strip=True)
    entries[i]['full_card_disqualified']=bool(re.search('disqualification',card.get_text(' ',strip=True),re.I))
assert set(ids)==set(entries), (set(ids)^set(entries))
assert len(ids)==len(set(ids))
(P/'entries.json').write_text(json.dumps(list(entries.values()),ensure_ascii=False,indent=2),encoding='utf-8')
artists=json.loads((P/'artists.json').read_text(encoding='utf-8'))
def hit(n,s):
    n=unicodedata.normalize('NFKC',n).casefold()
    s=unicodedata.normalize('NFKC',s).casefold()
    return bool(re.search(r'(?<![a-z0-9])'+re.escape(n)+r'(?![a-z0-9])',s))
for a in artists:
    found=[(e['id'],e['full_artist_display']) for e in entries.values() if hit(a['name'],e['full_artist_display']) and not hit(a['name'],e['artist'])]
    if found:
        print(a['name'],found)
print('Validated full/simple entry ID coverage:',len(ids))
