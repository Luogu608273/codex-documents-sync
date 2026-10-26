from pathlib import Path
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import json, re, sys

sys.stdout.reconfigure(encoding='utf-8')
P = Path(__file__).resolve().parent
RAW = P/'sources'
BASE = 'https://manbow.nothing.sh/event/'
jobs = []
for i in [10,12,19,64,76,82,125,131,139,141,143,165]:
    jobs.append(('team-%s.html'%i, BASE+'event_teamprofile.cgi?event=152&team=%s'%i, 'team'))
for i in [61,88,276,289,290,352,364,381,384,390,397,434,459,460,465]:
    jobs.append(('entry-%s.html'%i, BASE+'event.cgi?action=More_def&num=%s&event=152'%i, 'entry'))
for i in [46278925,49726260,50609651,1098070,60364651,31464433,29786464]:
    jobs.append(('artist-%s.json'%i, 'https://music.163.com/api/artist/%s'%i, 'artist'))

def get(job):
    name,url,kind = job
    req = Request(url, headers={'User-Agent':'Mozilla/5.0','Referer':'https://music.163.com/' if kind=='artist' else BASE})
    with urlopen(req, timeout=25) as f:
        data = f.read()
    (RAW/name).write_bytes(data)
    if kind=='artist':
        j = json.loads(data)
        a = j.get('artist',{})
        return name, {'code':j.get('code'), 'artist':{k:a.get(k) for k in ['id','name','alias','trans','transNames','briefDesc']}}
    soup = BeautifulSoup(data, 'html.parser')
    if kind=='team':
        values = []
        for tr in soup.select('tr'):
            cs = tr.find_all(['th','td'],recursive=False)
            if cs:
                values.append(' | '.join(c.get_text(' ',strip=True) for c in cs))
        links = [{'text':a.get_text(' ',strip=True),'url':a['href']} for a in soup.find_all('a',href=True) if any(v in a['href'] for v in ['twitter.com','x.com','youtube.com','bilibili.com','music.163.com','More_def'])]
        return name, {'title':soup.title.get_text() if soup.title else '', 'rows':values,'links':links}
    # Only author-controlled description and metadata; exclude public reviews.
    for node in soup.select('script,style'):
        node.decompose()
    s = soup.get_text(' ',strip=True)
    cutoff = re.search(r'(?:Short Impression|Post Short Impression)',s)
    s = s[:cutoff.start()] if cutoff else s
    return name, {'title':soup.title.get_text() if soup.title else '', 'description':s}

with ThreadPoolExecutor(max_workers=3) as pool:
    results = dict(pool.map(get,jobs))
(P/'source-audit.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
for name,v in results.items():
    print('\n'+name)
    if name.startswith('artist-') or name in ['team-10.html','team-12.html','team-19.html','team-165.html']:
        print(json.dumps(v,ensure_ascii=False))
    elif name in ['entry-61.html','entry-384.html','entry-397.html','entry-434.html','entry-459.html','entry-460.html']:
        print(json.dumps(v,ensure_ascii=False)[:10000])
    else:
        print(v['title'])
