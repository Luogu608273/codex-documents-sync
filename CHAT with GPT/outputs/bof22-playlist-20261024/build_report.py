from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime,timezone,timedelta
from hashlib import sha256
import json,re,html,sys

sys.stdout.reconfigure(encoding='utf-8')
P=Path(__file__).resolve().parent
artists=json.loads((P/'artists.json').read_text(encoding='utf-8'))
songs=json.loads((P/'songs.json').read_text(encoding='utf-8'))
entries={e['id']:e for e in json.loads((P/'entries.json').read_text(encoding='utf-8'))}
teams={t['id']:t for t in json.loads((P/'teams.json').read_text(encoding='utf-8'))}
validation=json.loads((P/'validation.json').read_text(encoding='utf-8'))
by_name={}
for a in artists:
    r=by_name.setdefault(a['name'],{'name':a['name'],'records':[],'song_ids':set()})
    r['records'].append(a)
    r['song_ids'].update(a['song_ids'])
song_index={s['id']:s for s in songs}

# Each positive decision is reviewed against actual entry credits or a current
# team profile, rather than accepted from a substring-search result.
confirmed={
    'NoKANY': {'entries':[276,290], 'role':'作曲、编曲、BMS', 'note':'两首作品均在作者提供的 Credits 中列有作曲署名。'},
    'Kankitsu': {'entries':[289,465], 'role':'作曲、编曲、BMS', 'note':'网易云该艺人页的 alias 包含 Lime；本届署名为 Lime + ああああ、Lime / Kankitsu。', 'extra_sources':['https://music.163.com/artist?id=1098070','https://osu.ppy.sh/beatmaps/artists/116']},
    'ARForest': {'entries':[463], 'role':'音乐／BMS', 'note':'官方作品作者栏直接署名。'},
    'Cranky': {'entries':[364], 'role':'音乐、BMS', 'note':'与 ARMYTOM 合作；作者提供的 Credits 列明 Music: Cranky。'},
    'OfficialAz3': {'entries':[62,152,274], 'role':'音乐／BMS', 'note':'三首作品的作者栏均明确署名；另有多个团队的 BMS 制作登记。'},
    'ああああ': {'entries':[289], 'role':'作曲、编曲', 'note':'与 Lime 合作；作者说明主要作曲部分由ああああ担当。'},
    '庭師': {'entries':[384], 'role':'作曲、BMS', 'note':'作者提供的 Credits 列明 Music: 庭師。'},
    'ARMYTOM': {'entries':[364], 'role':'作曲、编曲、BMS', 'note':'与 Cranky 合作；Credits 列明 Compose & Arrangement: ARMYTOM。'},
    'BITPLANE': {'entries':[300,301], 'role':'音乐／BMS', 'note':'会场署名 Bitplane；仅大小写不同。'},
    'kanoryo': {'entries':[105], 'role':'音乐／BMS', 'note':'官方作品作者栏直接署名。'},
    'LYRi "Cyanblue" WHiTE': {'entries':[459,460], 'role':'作曲／编曲、BMS', 'note':'No.459 的作曲署名为 LYRi_WHiTE；No.460 的编曲署名为 LYRi "Cyanblue" WHiTE；同队成员登记并列这些名义。'},
    'nm-y': {'entries':[381], 'role':'音乐', 'note':'与 takehirotei 合作；作品作者栏为 nm-y。'},
    '米虾Fomiki': {'entries':[88], 'role':'作曲', 'note':'与 Chikanya 合作，Credits 明确列出两人为作曲。'},
    'Sennzai': {'entries':[390], 'role':'演唱', 'note':'作者提供的 Credits 明确标注 Vocals。'},
    'はぁち': {'entries':[352], 'role':'演唱', 'note':'ShrimpCats. 的演唱成员；Credits 明确标注 Vocal。'},
    'Eili': {'entries':[390,397], 'role':'作词／演唱', 'note':'会场署名 eili；No.390 为 Lyrics，No.397 为 Vocals。网易云同名的 ID 0 记录保留在来源信息中。'},
    '花見くくる': {'entries':[290], 'role':'演唱', 'note':'作品 Credits 与团队成员表均明确标注演唱。'},
}
support={
    'rN': {'teams':[141], 'role':'Graphics（美术）', 'note':'Stone Arch Project 当前成员表列为 Graphics；未找到以其名义署名的本届音乐作品。'},
}
registered={
    '初云CLoudie': {'teams':[165], 'role':'BMS 团队登记线索', 'note':'TwoTaker 成员表有 CLoudie（bms），但当前两首已提交作品均未以 CLoudie 署名；成员页没有个人链接，不计为已确认的作品参赛。过往官方作品页可见初雲CLoudie与CLoudie的对应署名。', 'extra_sources':['https://manbow.nothing.sh/event/event.cgi?action=More_def&event=146&num=249']},
}
ambiguous={
    'つぐ': {'entries':[61], 'teams':[10], 'role':'同名／转写待核实', 'note':'歌单为 TAKIO《多次元宇宙融合論》的演唱者つぐ；本届 No.61 的 Tsugu 被介绍为元祖焼きまんじゅう的歌手，缺少同一身份的可靠对应，不计入确认名单。', 'extra_sources':['https://linkco.re/uYgDq4h9/songs/4266560/lyrics?lang=ja']},
    'Plum - Melodic Artist': {'teams':[12,19], 'role':'同名待核实', 'note':'本届团队有谱师 plum，其中一队链接至 @plum_812；不能据此认定为歌单中的 Plum - Melodic Artist，未计入确认名单。'},
}
virtual={
    '初音ミク': {'entries':[211,366,415], 'role':'虚拟歌手／声库使用', 'note':'会场同时使用初音ミク、Hatsune Miku两种写法；不是现实作曲者本人参赛。'},
    '重音テト': {'entries':[227,312], 'role':'虚拟歌手／声库使用', 'note':'No.312 使用重音テトSV署名；不作为现实作曲者参赛计数。'},
    '洛天依Official': {'entries':[260], 'role':'虚拟歌手／声库使用', 'note':'与另一署名洛天依指向同一虚拟歌手；保留歌单原始显示名。'},
    '洛天依': {'entries':[260], 'role':'虚拟歌手／声库使用', 'note':'网易云为 ID 0 的原始记录；与洛天依Official不重复计作两位真人。'},
    '闇音レンリ': {'entries':[296], 'role':'虚拟歌手／声库使用', 'note':'本届作品列 ft. 闇音レンリ；不作为现实作曲者参赛计数。'},
}
groups=[('已确认作品署名',confirmed),('已确认其他制作参与',support),('团队登记线索、未确认作品',registered),('同名／转写待确认',ambiguous),('虚拟歌手／声库署名',virtual)]
decisions={}
for category,mapping in groups:
    for name,d in mapping.items():
        assert name in by_name,name
        assert name not in decisions,name
        for i in d.get('entries',[]):
            assert i in entries and not entries[i]['disqualified'] and not entries[i].get('full_card_disqualified'),(name,i)
        decisions[name]=dict(d,status=category)
for name in by_name:
    if name not in decisions:
        decisions[name]={'status':'未查到对应公开参赛署名','role':'—','note':'已对照全部作品作者栏、完整作品卡片附加署名与全部团队成员表；未找到可确认的对应。'}
assert len(decisions)==len(by_name)==270
assert len(songs)==validation['declared_tracks']==373
assert len(entries)==475 and len(teams)==175
counts=Counter(d['status'] for d in decisions.values())
assert sum(counts.values())==270

def esc(s):
    return html.escape(str(s),quote=False).replace('|','&#124;').replace('[','&#91;').replace(']','&#93;').replace('\n',' ')
def link(label,url):
    return '['+esc(label)+']('+url.replace(' ','%20')+')'
def worklinks(d):
    return '；'.join(link(entries[i]['title'],entries[i]['url']) for i in d.get('entries',[]))
def teamlinks(d):
    return '；'.join(link(teams[i]['name'],teams[i]['url']) for i in d.get('teams',[]))
def examples(name,limit=2):
    ss=sorted((song_index[i] for i in by_name[name]['song_ids']),key=lambda s:s['position'])
    return '；'.join(link(s['title'],s['url']) for s in ss[:limit])
def artistlinks(name):
    out=[]
    for a in by_name[name]['records']:
        if a['id']:
            out.append(link(str(a['id']),'https://music.163.com/artist?id='+str(a['id'])))
        else:
            out.append('ID 0（无独立艺人页）')
    return '；'.join(out)

stamp=validation['checked_at_china']
lines=[
    '# 网易云歌单全部艺人 × BOF22 核查', '',
    '- 歌单：'+link(validation['playlist_name'],'https://music.163.com/playlist?id=8483155610')+'。',
    '- 数据抓取时间：'+stamp+'（北京时间）。',
    '- 完整性：歌单声明 373 首，已取得 373 个不同歌曲编号的完整曲目资料；无缺失编号、无额外编号。',
    '- 提取范围：歌曲详情中的全部艺人字段，包含合作作者、演唱者、团体和虚拟歌手；不等同每首歌曲完整的作词、作曲、编曲及幕后人员名单。',
    '- 原始数据有 275 条不同艺人记录、270 个不同的显示署名。显示署名相同不自动证明是同一人，例如两个 SHIKI 艺人编号分别出现在 wotaku 的演唱作品与《Lapis》中。',
    '- 对照范围：BOF22 官方会场 475 条作品记录（简表与完整作品卡片编号完全一致）、175 个团队的成员表；命中项进一步核对作品介绍、Credits 与团队个人资料。',
    '- 本文是参赛署名核查，不是评分榜单。合作、演唱、美术、声库使用、仅团队登记分别列出。',
    '- “未查到”只表示目前公开署名与已核实别名没有匹配，不推断未公开身份或匿名马甲。只在评论区出现、仅是原曲作者或被致谢，不作为本届作品作者参赛证据。',
    '', '## 结果统计', '', '| 类别 | 不同显示署名数 |', '|---|---:|',
]
for category in [g[0] for g in groups]+['未查到对应公开参赛署名']:
    lines.append('| '+category+' | '+str(counts[category])+' |')
lines.extend(['', '已确认作品署名 17 个中，13 个涉及音乐／BMS 制作，另外 4 个在已提交作品中负责演唱或作词。rN 的美术参与另列，不计作音乐作者参赛。', '', '## 已确认：音乐／BMS 制作', '', '| 歌单原署名 | 歌单曲目数 | 歌单里的例子 | 本届作品 | 已核实参与方式 |', '|---|---:|---|---|---|'])
for name,d in confirmed.items():
    if d['role'] in ['演唱','作词／演唱']:
        continue
    lines.append('| '+esc(name)+' | '+str(len(by_name[name]['song_ids']))+' | '+examples(name)+' | '+worklinks(d)+' | '+esc(d['role'])+' |')
lines.extend(['', '## 已确认：演唱／作词', '', '| 歌单原署名 | 歌单曲目数 | 本届作品 | 参与方式 |', '|---|---:|---|---|'])
for name,d in confirmed.items():
    if d['role'] in ['演唱','作词／演唱']:
        lines.append('| '+esc(name)+' | '+str(len(by_name[name]['song_ids']))+' | '+worklinks(d)+' | '+esc(d['role'])+' |')
for category,mapping in groups[1:]:
    lines.extend(['', '## '+category, '', '| 歌单原署名 | 本届作品／团队线索 | 核查说明 |', '|---|---|---|'])
    for name,d in mapping.items():
        refs='；'.join(v for v in [worklinks(d),teamlinks(d)] if v)
        lines.append('| '+esc(name)+' | '+refs+' | '+esc(d['note'])+' |')
lines.extend(['', '## 署名与身份的特别处理', '',
    '- Kankitsu → Lime：网易云艺人资料直接列出 alias=Lime；本届 No.465 同时署名 Lime / Kankitsu。'+link('osu! 官方合作艺人介绍','https://osu.ppy.sh/beatmaps/artists/116')+'也将两者并列。',
    '- LYRi "Cyanblue" WHiTE → LYRi_WHiTE：同队成员登记及相邻作品的作者 Credits 交叉核对；不据此将该队所有其他成员名义也合并为同一个人。',
    '- Eili／eili、BITPLANE／Bitplane：仅大小写变化；保留网易云 ID 0 记录和有 ID 的记录，不丢弃对应歌曲。',
    '- 排除短字符串误匹配：xi 不等于 Yi Xi、AprilXI、Xiba；uma 不等于 JURUMA；LeaF 不等于 leafisly；rN 不等于 RNY、Rner；とあ不等于“とある歌い手”。',
    '- 同名不直接合并身份：つぐ与Tsugu、Plum - Melodic Artist与plum均未强行对应。',
    '', '## 全部 270 个显示署名的逐项结果', '',
    '按它们出现在歌单中的歌曲数降序排列；同名艺人资料以多个编号保留。', '',
    '| 序号 | 歌单原署名 | 网易云艺人编号／资料页 | 歌曲数 | 核查结果 | 本届作品或线索 | 歌单曲目示例 |',
    '|---:|---|---|---:|---|---|---|',
])
ordered=sorted(by_name,key=lambda name:(-len(by_name[name]['song_ids']),name.casefold()))
for i,name in enumerate(ordered,1):
    d=decisions[name]
    refs='；'.join(v for v in [worklinks(d),teamlinks(d)] if v) or '—'
    lines.append('| '+str(i)+' | '+esc(name)+' | '+artistlinks(name)+' | '+str(len(by_name[name]['song_ids']))+' | '+esc(d['status'])+' | '+refs+' | '+examples(name,1)+' |')
lines.extend(['', '## 来源与完整曲目表', '',
    '- '+link('原歌单','https://music.163.com/playlist?id=8483155610'),
    '- '+link('网易云歌单详情接口','https://music.163.com/api/v6/playlist/detail?id=8483155610&n=100000&s=0')+'：提供373个完整歌曲编号；接口内直接返回的歌曲详情只有6首，因此另按歌曲编号补齐详情。',
    '- 网易云歌曲详情接口 `/api/song/detail?ids=[...]`：分5批取得全部373首的歌曲名、艺人名与艺人编号；原始响应保存在同目录 sources/ 下。',
    '- '+link('BOF22 官方作品简表','https://manbow.nothing.sh/event/event.cgi?action=sp&event=152'),
    '- '+link('BOF22 官方完整作品列表','https://manbow.nothing.sh/event/event.cgi?action=List_def&event=152'),
    '- '+link('BOF22 官方团队成员列表','https://manbow.nothing.sh/event/event_teamprofile.cgi?event=152'),
    '- '+link('完整373首曲目与署名明细',(P/'歌单373首_曲目与全部署名.md').as_posix()),
])
(P/'网易云歌单作者_BOF22全量核查.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
song_lines=['# 歌单373首：曲目与全部艺人署名', '', '来源：'+link(validation['playlist_name'],'https://music.163.com/playlist?id=8483155610')+'。', '', '抓取时间：'+stamp+'。顺序与歌单编号列表一致，合作署名全部保留。', '', '| 序号 | 歌曲 | 全部艺人署名 |', '|---:|---|---|']
for s in songs:
    aa=[]
    for a in s['artists']:
        aa.append(link(a['name'],'https://music.163.com/artist?id='+str(a['id'])) if a['id'] else esc(a['name'])+'（ID 0）')
    song_lines.append('| '+str(s['position'])+' | '+link(s['title'],s['url'])+' | '+' / '.join(aa)+' |')
(P/'歌单373首_曲目与全部署名.md').write_text('\n'.join(song_lines)+'\n',encoding='utf-8')

recorded=[]
for name in ordered:
    r=by_name[name]
    recorded.append({'name':name,'netease_artist_ids':[a['id'] for a in r['records']], 'song_ids':sorted(r['song_ids']), **decisions[name]})
(P/'reviewed-results.json').write_text(json.dumps(recorded,ensure_ascii=False,indent=2),encoding='utf-8')
validation.update({'unique_display_names':len(by_name),'raw_artist_records':len(artists),'reviewed_display_names':len(recorded),'full_card_id_coverage':len(entries),'decision_counts':dict(counts),'report_built_at_china':datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds')})
validation['source_sha256']={f.name:sha256(f.read_bytes()).hexdigest() for f in sorted((P/'sources').iterdir()) if f.is_file()}
(P/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in validation.items() if k!='source_sha256'},ensure_ascii=False,indent=2))
print('Confirmed creators:',', '.join(n for n,d in confirmed.items() if d['role'] not in ['演唱','作词／演唱']))
print('Reports:',[f.name for f in P.glob('*.md')])
