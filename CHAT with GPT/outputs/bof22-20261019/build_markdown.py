from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
from datetime import datetime, timezone, timedelta
from collections import Counter
import json, re, html, hashlib

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / 'sources'
BASE = 'https://manbow.nothing.sh/event/'
URLS = {
    'homepage': 'https://bmsoffighters.net/bof22/',
    'songs_simple': BASE + 'event.cgi?action=sp&event=152',
    'songs_full': BASE + 'event.cgi?action=List_def&event=152',
    'teams': BASE + 'event_teamprofile.cgi?event=152',
    'downloads_all': BASE + 'event.cgi?action=URLList&event=152&end=999',
}

def soup(name):
    return BeautifulSoup((SOURCES / (name + '.html')).read_bytes(), 'html.parser')

def text(node):
    return re.sub(r'\s+', ' ', node.get_text(' ', strip=True)).strip() if node else ''

def number(value):
    if not re.fullmatch(r'-?\d+(?:\.\d+)?', value):
        return None
    return float(value) if '.' in value else int(value)

def md(value):
    return html.escape(str(value or ''), quote=False).replace('|', '&#124;').replace('[', '&#91;').replace(']', '&#93;').replace('`', '&#96;').replace('\n', '<br>')

def link(label, url):
    safe = str(url).replace(' ', '%20').replace('(', '%28').replace(')', '%29').replace('<', '%3C').replace('>', '%3E')
    return '[' + md(label) + '](' + safe + ')'

def entry_id(a):
    return int(parse_qs(urlparse(a['href']).query)['num'][0])

simple = soup('songs_simple')
full = soup('songs_full')
teams_page = soup('teams')
download_page = soup('downloads_all')
team_urls = {}
for tr in teams_page.select('table tr')[1:]:
    c = tr.find_all('td', recursive=False)
    if len(c) == 10 and c[3].find('a'):
        a = c[3].find('a')
        team_urls[text(a)] = urljoin(BASE, a['href'])
records = {}
for row in simple.select('table tr')[1:]:
    cells = row.find_all('td', recursive=False)
    if not cells:
        continue
    assert len(cells) == 12, ('unexpected song columns', len(cells))
    values = [text(c) for c in cells]
    num = int(values[0])
    assert num not in records, ('duplicate ID', num)
    records[num] = {
        'id': num, 'title': values[4], 'artist': values[2], 'team': values[1], 'genre': values[3],
        'impressions': number(values[5]), 'total_adjusted': number(values[6]),
        'total_native': number(values[7]), 'median': number(values[8]), 'average': number(values[9]),
        'registered_at_jst': values[10], 'updated_at_jst': values[11],
        'entry_url': urljoin(BASE, cells[4].find('a')['href']),
    }

cards = {}
field_differences = []
expected_display_differences = []
layout_recoveries = []
for a in full.select('.pricing-title h4 a'):
    num = entry_id(a)
    card = a.find_parent(class_='pricing-box')
    block = a.find_parent(class_='team_information')
    assert card is not None
    assert num not in cards, ('duplicate card', num)
    row = records[num]
    headings = card.select('.pricing-title .center h5')
    artist_credit = text(headings[-1])
    mov_match = re.search(r'[（(]\s*mov\s*[:：](.*)[)）]\s*$', artist_credit, re.I)
    labels = [text(x) for x in card.select('.bmsinfo strong.label')]
    action = text(card.select_one('.pricing-action'))
    type_match = re.search(r'No\.\d+\s*/\s*(.*?)\s*/\s*update', action, re.I)
    team_anchor = block.select_one('.fancy-title h3 a') if block else None
    if block is None:
        layout_recoveries.append({'id':num,'note':'Card has no team container in HTML; team URL matched by exact simple-list team name against team profiles.'})
    card_text = text(card)
    row.update({
        'artist_full_display': artist_credit,
        'visual_extra_credit': mov_match.group(1).strip() if mov_match else '',
        'key_modes': [v for v in labels if re.fullmatch(r'\d+K|Other', v)],
        'format_tags': [v for v in labels if v in ('62-bms', 'bmson')],
        'display_tags': labels,
        'final_striker': card.get('id') == 'ace_mus',
        'status': '失格（官网 Disqualification）' if re.search('disqualification', card_text, re.I) else '未标示失格',
        'entry_type': type_match.group(1) if type_match else '',
        'team_url': urljoin(BASE, team_anchor['href']) if team_anchor else team_urls.get(row['team'], ''),
    })
    for key, card_value in [('title', text(a)), ('genre', text(headings[0]))] + ([('team', text(team_anchor))] if team_anchor else []):
        if row[key] != card_value:
            difference = {'id': num, 'field': key, 'simple': row[key], 'full': card_value}
            if key == 'team' and card_value.endswith('...') and row[key].startswith(card_value[:-3]):
                difference['reason'] = 'Full card truncates long team heading; keep full name from simple list.'
                expected_display_differences.append(difference)
            elif key == 'title' and row['status'].startswith('失格') and row[key] == card_value + ' (Disq)':
                difference['reason'] = 'Simple list appends status to title; keep title and status in separate fields.'
                expected_display_differences.append(difference)
                row['title_list_display'] = row[key]
                row['title'] = card_value
            else:
                field_differences.append(difference)
    cards[num] = row
assert set(cards) == set(records), ('simple/full ID mismatch', sorted(set(cards) ^ set(records)))

downloads = {}
for tr in download_page.select('table tr')[1:]:
    c = tr.find_all('td', recursive=False)
    if not c:
        continue
    assert len(c) == 6
    num = int(text(c[0]))
    assert num not in downloads
    artist_link = c[1].find('a')
    raw_artist_url = artist_link.get('href', '') if artist_link else ''
    urls = []
    for a in c[5].find_all('a', href=True):
        href = a['href'].strip()
        if href.startswith(('https://', 'http://')) and href not in urls:
            urls.append(href)
    downloads[num] = {
        'size_kb': number(re.sub(r'\s*KB\s*$', '', text(c[4]), flags=re.I)),
        'download_urls': urls,
        'download_description': c[5].get_text('\n', strip=True),
        'artist_url': raw_artist_url if raw_artist_url.startswith(('https://', 'http://')) else '',
    }
for num, row in records.items():
    row.update(downloads.get(num, {'size_kb': None, 'download_urls': [], 'download_description': '', 'artist_url': ''}))

teams = []
for tr in teams_page.select('table tr')[1:]:
    c = tr.find_all('td', recursive=False)
    if not c:
        continue
    assert len(c) == 10
    a = c[3].find('a')
    teams.append({
        'id': int(text(c[0])), 'name': text(a), 'leader': text(c[4]),
        'members': text(c[7]), 'works_display': text(c[6]),
        'status_display': text(c[3])[len(text(a)):].strip() if text(c[3]).startswith(text(a)) else text(c[3]),
        'team_url': urljoin(BASE, a['href']),
    })

full_plain = text(full)
reported_match = re.search(r'EntryBMS\s*:\s*(\d+)', full_plain)
reported = int(reported_match.group(1)) if reported_match else None
rows = sorted(records.values(), key=lambda r:r['id'])
stamp = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds')
checks = {
    'scraped_at_china': stamp,
    'song_count': len(rows), 'unique_song_ids': len(records), 'full_card_count': len(cards),
    'site_reported_entrybms': reported,
    'download_rows': len(downloads), 'download_rows_without_song': sorted(set(downloads) - set(records)),
    'song_rows_without_download_metadata': sorted(set(records) - set(downloads)),
    'team_profile_count': len(teams), 'teams_with_song_records': len(set(r['team'] for r in rows)),
    'final_striker_count_from_card_marker': sum(r['final_striker'] for r in rows),
    'disqualified_ids': [r['id'] for r in rows if r['status'].startswith('失格')],
    'missing_required_fields': [{'id': r['id'], 'fields': [k for k in ('title','artist','team','genre','entry_url') if not r[k]]} for r in rows if any(not r[k] for k in ('title','artist','team','genre','entry_url'))],
    'replacement_characters': [r['id'] for r in rows if '\ufffd' in json.dumps(r,ensure_ascii=False)],
    'source_field_differences': field_differences,
    'expected_display_differences': expected_display_differences,
    'layout_recoveries': layout_recoveries,
    'sources': {name: {'url':url, 'bytes':(SOURCES/(name+'.html')).stat().st_size, 'sha256':hashlib.sha256((SOURCES/(name+'.html')).read_bytes()).hexdigest()} for name,url in URLS.items()},
}
assert not checks['missing_required_fields'], checks['missing_required_fields']
assert not checks['replacement_characters'], checks['replacement_characters']
assert not checks['source_field_differences'], checks['source_field_differences']
assert not checks['download_rows_without_song'], checks['download_rows_without_song']
assert not checks['song_rows_without_download_metadata'], checks['song_rows_without_download_metadata']

lines = [
    '# BOF22 全曲目资料', '',
    '赛事：THE BMS OF FIGHTERS 22 — GO 2 YOUR EVOLUTION —。', '',
    f'- 抓取时间：{stamp}（北京时间）。',
    f'- 抓取范围：官网所链接会场的全部公开列表记录，共 **{len(rows)} 条**，编号不重复。',
    '- 顺序：作品登记编号升序，不代表排名。',
    f'- 数量差异：会场页头显示 EntryBMS={reported}，但简表与完整作品卡片均可解析出 {len(rows)} 个相同的作品编号。本文保留全部公开记录，不将页头数字解释为已核实的有效参赛作品数。',
    f'- 完整列表中明确出现 Disqualification 的编号：{", ".join(str(x) for x in checks["disqualified_ids"])}；其余“未标示失格”不等于已完成全部参赛资格审核。',
    '- 曲名、作者、曲风及团队保留官网原文；没有按艺名推断真实身份，也没有将合作作者随意拆分。',
    '- “影像／附加署名”取自完整列表作者栏的 mov 字段；可能混含插画等署名，未列出不代表没有影像。',
    '- FS 标记来自官网完整列表的 FS 卡片标识；评分是抓取时快照，不是最终成绩。',
    '- 登记与更新时间沿用官网日本时间 JST（UTC+9）；与北京时间相差 1 小时。',
    '- 仅抓取网页元数据及公开链接，没有下载音乐包、谱面文件或视频。',
    '', '## 来源', '',
]
for name,label in [('homepage','赛事官网'),('songs_simple','官方曲目简表'),('songs_full','官方完整会场'),('teams','官方团队名单'),('downloads_all','官方全曲下载链接表')]:
    lines.append('- '+link(label, URLS[name]))
lines += ['', '## 曲目索引', '', '| 编号 | 曲名／作品页 | 作者（官网原文） | 团队 | 曲风 | 键型／格式 | FS | 状态 |', '| ---: | --- | --- | --- | --- | --- | :---: | --- |']
for r in rows:
    mode=' / '.join(r['key_modes']+r['format_tags']) or '未标示'
    lines.append('| '+' | '.join([str(r['id']),link(r['title'],r['entry_url']),md(r['artist']),link(r['team'],r['team_url']),md(r['genre']),md(mode),'是' if r['final_striker'] else '否',md(r['status'])])+' |')
lines += ['', '## 逐曲补充信息与下载入口', '', '下列下载入口由作者在会场登记；不同入口可能是格式版本、镜像、补丁或附加文件，请结合原始说明选择。链接仅被收集，未逐一验证文件是否可下载。', '']
for r in rows:
    lines += [f'### No.{r["id"]} · {md(r["title"])}', '', '- 作品页：'+link('官网详情',r['entry_url']), '- 作者完整显示：'+md(r['artist_full_display'])]
    if r['visual_extra_credit']:lines.append('- 影像／附加署名（mov 原文）：'+md(r['visual_extra_credit']))
    if r['artist_url']:lines.append('- 作者所填主页：'+link('主页',r['artist_url']))
    lines += ['- 官网类型：'+md(r['entry_type']), '- 登记时间（JST）：'+md(r['registered_at_jst'])+'；更新（JST）：'+md(r['updated_at_jst'])]
    def n(v):return '未提供' if v is None else str(v)
    lines.append('- 评价快照：'+f'评价数 {n(r["impressions"])}；加成总分 {n(r["total_adjusted"])}；原始总分 {n(r["total_native"])}；中位数 {n(r["median"])}；均分 {n(r["average"])}。')
    if r['size_kb'] is not None:lines.append('- 官网标注大小：'+str(r['size_kb'])+' KB（原始标注，非本地下载测量）。')
    if r['download_urls']:
        lines.append('- 下载入口：'+'；'.join(link(str(i+1)+' · '+urlparse(u).hostname,u) for i,u in enumerate(r['download_urls'])))
    else:lines.append('- 下载入口：公开下载表未列出 HTTP(S) 链接。')
    # Preserve label/version context as readable text, without copying entire URLs twice.
    desc = r['download_description']
    for u in sorted(r['download_urls'], key=len, reverse=True):desc=desc.replace(u,'〔链接见上〕')
    desc=re.sub(r'(?:〔链接见上〕\s*)+', '〔链接见上〕\n', desc).strip()
    labels=[x.strip() for x in desc.splitlines() if x.strip() and x.strip()!='〔链接见上〕']
    if labels:lines.append('- 下载版本说明（官网原文）：'+md(' / '.join(labels)))
    lines.append('')
lines += ['## 团队成员登记表', '', '包括官网仍公开展示的已退出、失格或尚未提交作品的团队；以原始状态栏为准。', '', '| 团队编号 | 团队／主页 | 队长 | 成员及职责（原文） | 作品提交显示 | 团队状态（原文） |', '| ---: | --- | --- | --- | --- | --- |']
for t in sorted(teams,key=lambda x:x['id']):
    lines.append('| '+' | '.join([str(t['id']),link(t['name'],t['team_url']),md(t['leader']),md(t['members']),md(t['works_display']),md(t['status_display']) or '未注明'])+' |')

document=ROOT/'BOF22_全曲目资料_2026-10-19.md'
document.write_text('\n'.join(lines)+'\n',encoding='utf-8')
(ROOT/'catalogue.json').write_text(json.dumps({'metadata':checks,'songs':rows,'teams':teams},ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'validation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
content=document.read_text(encoding='utf-8')
assert len(re.findall(r'^### No\.\d+ ·',content,re.M))==len(rows)
index_section = content.split('## 曲目索引\n',1)[1].split('## 逐曲补充信息与下载入口\n',1)[0]
assert len(re.findall(r'^\| \d+ \| ',index_section,re.M))==len(rows)
print(json.dumps({'markdown':str(document),'bytes':document.stat().st_size,'songs':len(rows),'teams':len(teams),'reported_entrybms':reported,'fs':checks['final_striker_count_from_card_marker'],'disqualified':checks['disqualified_ids'],'checks':'passed','sample':[{'id':records[i]['id'],'title':records[i]['title'],'artist':records[i]['artist'],'visual_credit':records[i]['visual_extra_credit'],'downloads':len(records[i]['download_urls'])} for i in [1,36,64,253,289,385]]},ensure_ascii=False,indent=2))
