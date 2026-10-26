from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode, urljoin
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import json, re, time, unicodedata, sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parent
RAW = ROOT / 'sources'
RAW.mkdir(exist_ok=True)
BASE = 'https://manbow.nothing.sh/event/'

def fetch(url, name):
    for attempt in range(3):
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://music.163.com/' if '163.com' in url else BASE})
            with urlopen(req, timeout=25) as response:
                data = response.read()
            (RAW / name).write_bytes(data)
            return data
        except Exception:
            if attempt == 2:
                raise
            time.sleep(0.5 * (attempt + 1))

def save(name, obj):
    (ROOT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')

def txt(node):
    return re.sub(r'\s+', ' ', node.get_text(' ', strip=True)).strip()

def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFKC', s).casefold() if c.isalnum())

playlist_url = 'https://music.163.com/api/v6/playlist/detail?id=8483155610&n=100000&s=0'
playlist_response = json.loads(fetch(playlist_url, 'playlist.json'))
assert playlist_response['code'] == 200
playlist = playlist_response['playlist']
ids = [t['id'] for t in playlist['trackIds']]
assert len(ids) == playlist['trackCount'], (len(ids), playlist['trackCount'])

def get_batch(pair):
    i, batch = pair
    url = 'https://music.163.com/api/song/detail?' + urlencode({'ids': json.dumps(batch, separators=(',', ':'))})
    data = json.loads(fetch(url, 'songs-%02d.json' % i))
    assert data['code'] == 200
    return data['songs']

with ThreadPoolExecutor(max_workers=3) as pool:
    batches = list(pool.map(get_batch, enumerate([ids[i:i+80] for i in range(0, len(ids), 80)])))
song_map = {s['id']: s for batch in batches for s in batch}
missing = sorted(set(ids) - set(song_map))
extra = sorted(set(song_map) - set(ids))
assert not missing and not extra, {'missing': missing, 'extra': extra}
songs = []
artist_map = {}
for i, song_id in enumerate(ids, 1):
    s = song_map[song_id]
    artists = s.get('artists', s.get('ar', []))
    songs.append({'position': i, 'id': song_id, 'title': s['name'], 'artists': [{'id': a['id'], 'name': a['name']} for a in artists], 'url': 'https://music.163.com/song?id=%s' % song_id})
    for a in artists:
        # ID 0 is used by the service for multiple unrelated unregistered artists.
        key = str(a['id']) if a['id'] else 'name:' + a['name']
        row = artist_map.setdefault(key, {'key': key, 'id': a['id'], 'name': a['name'], 'name_variants': [], 'song_ids': [], 'aliases': []})
        if a['name'] not in row['name_variants']:
            row['name_variants'].append(a['name'])
        for alias in a.get('alias', []):
            if alias not in row['aliases']:
                row['aliases'].append(alias)
        row['song_ids'].append(song_id)

urls = [('entries', BASE + 'event.cgi?action=sp&event=152'), ('teams', BASE + 'event_teamprofile.cgi?event=152')]
with ThreadPoolExecutor(max_workers=2) as pool:
    pages = dict(pool.map(lambda p: (p[0], fetch(p[1], p[0] + '.html')), urls))
entries = []
for tr in BeautifulSoup(pages['entries'], 'html.parser').select('table tr'):
    c = tr.find_all('td', recursive=False)
    if not c:
        continue
    assert len(c) == 12, len(c)
    v = [txt(x) for x in c]
    entries.append({'id': int(v[0]), 'team': v[1], 'artist': v[2], 'title': v[4], 'disqualified': '(Disq)' in v[4], 'url': urljoin(BASE, c[4].find('a')['href'])})
teams = []
for tr in BeautifulSoup(pages['teams'], 'html.parser').select('table tr'):
    c = tr.find_all('td', recursive=False)
    if not c:
        continue
    assert len(c) == 10, len(c)
    a = c[3].find('a')
    teams.append({'id': int(txt(c[0])), 'name': txt(a), 'leader': txt(c[4]), 'members': txt(c[7]), 'works': txt(c[6]), 'url': urljoin(BASE, a['href'])})

artists = sorted(artist_map.values(), key=lambda a: (-len(a['song_ids']), a['name'].casefold()))
for a in artists:
    keys = [norm(n) for n in a['name_variants'] + a['aliases'] if len(norm(n)) >= 2]
    a['entry_candidates'] = [e['id'] for e in entries if any(k in norm(e['artist']) for k in keys)]
    a['team_candidates'] = [t['id'] for t in teams if any(k in norm(t['members']) for k in keys)]
save('songs.json', songs)
save('artists.json', artists)
save('entries.json', entries)
save('teams.json', teams)
summary = {'checked_at_china': datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds'), 'playlist_id': playlist['id'], 'playlist_name': playlist['name'], 'declared_tracks': playlist['trackCount'], 'retrieved_tracks': len(songs), 'unique_song_ids': len(song_map), 'missing_track_ids': missing, 'extra_track_ids': extra, 'artists': len(artists), 'entries': len(entries), 'teams': len(teams), 'candidate_artists': sum(bool(a['entry_candidates'] or a['team_candidates']) for a in artists)}
save('validation.json', summary)
print(json.dumps(summary, ensure_ascii=False))
for a in artists:
    print('%s | %s | songs=%s | entries=%s | teams=%s' % (a['key'], a['name'], len(a['song_ids']), a['entry_candidates'], a['team_candidates']))
