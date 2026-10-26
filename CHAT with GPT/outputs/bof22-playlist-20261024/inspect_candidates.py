from pathlib import Path
from collections import Counter
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
P = Path(__file__).resolve().parent
artists = json.loads((P/'artists.json').read_text(encoding='utf-8'))
songs = {s['id']: s for s in json.loads((P/'songs.json').read_text(encoding='utf-8'))}
names = Counter(a['name'] for a in artists)
print('Unique display names:', len(names))
print('Repeated names:', {k: v for k, v in names.items() if v > 1})
selected = {'Kankitsu', 'SHIKI', 'Plum - Melodic Artist', '初云CLoudie', 'つぐ', 'LYRi "Cyanblue" WHiTE', 'Eili', 'ARMYTOM', 'BITPLANE', 'NoKANY', 'OfficialAz3', 'nm-y', '米虾Fomiki'}
for a in artists:
    if a['name'] in selected:
        print(a['key'], a['name'], [(songs[i]['title'], [n['name'] for n in songs[i]['artists']]) for i in a['song_ids']])

# Boundaries intentionally remain conservative: a short alias is not a
# participant merely because it occurs inside another, unrelated name.
def hit(name, value):
    import re, unicodedata
    name = unicodedata.normalize('NFKC', name).casefold()
    value = unicodedata.normalize('NFKC', value).casefold()
    return bool(re.search(r'(?<![a-z0-9])' + re.escape(name) + r'(?![a-z0-9])', value))

alias_tests = {
    '削除': ['Sakuzyo', '削除'],
    'かめりあ': ['Camellia', 'かめりあ', "z'5"],
    'void': ['void', 'Mournfinale'],
    'Silentroom': ['Silentroom', 'polycube'],
    'モリモリあつし': ['モリモリあつし', 'Morimori Atsushi'],
    'Kankitsu': ['Kankitsu', 'Lime'],
    'DELA': ['DELA', 'DETRO', 'ルゼ'],
    'Se-U-Ra': ['Se-U-Ra', 'Se_IRA', 'Se_ira'],
    '初云CLoudie': ['CLoudie', '初云', 'Cloudie'],
    'つぐ': ['Tsugu', 'つぐ'],
    '洛天依Official': ['洛天依'],
    '初音ミク': ['初音ミク', 'Hatsune Miku'],
    '重音テト': ['重音テト', 'Kasane Teto'],
    'LYRi "Cyanblue" WHiTE': ['LYRi "Cyanblue" WHiTE', 'LYRi_WHiTE'],
    'Plum - Melodic Artist': ['Plum'],
    'Gram': ['Gram', 'Team Grimoire'],
}
entries = json.loads((P/'entries.json').read_text(encoding='utf-8'))
teams = json.loads((P/'teams.json').read_text(encoding='utf-8'))
print('\nCONSERVATIVE MATCHES AND ALIAS CANDIDATES')
for name in names:
    aliases = alias_tests.get(name, [name])
    es = [e for e in entries if any(hit(n, e['artist']) for n in aliases)]
    ts = [t for t in teams if any(hit(n, t['members']) for n in aliases)]
    if es or ts:
        print(name, '|', [(e['id'],e['title'],e['artist']) for e in es], '|', [(t['id'],t['name']) for t in ts])
