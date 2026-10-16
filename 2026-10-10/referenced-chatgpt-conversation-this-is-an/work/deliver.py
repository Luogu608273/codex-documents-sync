import csv
import hashlib
import json
import shutil
from pathlib import Path

out=Path('outputs')
cfg=json.loads(Path('work/config.json').read_text(encoding='utf8'))
shutil.copyfile('work/config.json',out/'live-config.json')
shutil.copyfile('work/aha.decoded.js',out/'aha-decoded.js')
shutil.copyfile('work/observations.json',out/'wasm-observations.json')
rows=[]
for rarity in ['UR','SSR','SR','R']:
    p=cfg['pools'][rarity]
    for field,label in [('cards','普通'),('featuredCards','精选')]:
        for c in p.get(field,[]):
            rows.append((rarity,label,c['title'],c['url']))
assert len(rows)==51 and len({r[3] for r in rows})==51
with (out/'candidates.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(['档位','子池','配置中的标题（不代表身份核验）','候选URL']);w.writerows(rows)
sha='0cf9782acf0c31ac4b21c7a47171ff8c6f9b1a37'
repo=f'https://github.com/kaitoulapin/xn--qvrw50dh7j.com/blob/{sha}'
report=f'''# 米哈游.com 公开跳转逻辑检查

检查日期：2026-10-10，约 17:05—17:11（北京时间）。目标为 https://www.米哈游.com/，ASCII 域名为 www.xn--qvrw50dh7j.com。

## 结论与证据范围

当前版本是客户端“抽卡式”随机跳转：入口 HTML → 混淆 aha.js → aha.wasm → 抽取候选卡片 → JavaScript 执行 location.replace。

共提取出 51 个不同候选地址。候选集合及参数来自本次实际下载的线上 WASM 运行内存，不只是仓库配置，也不是通过少量刷新猜测。线上还原加载脚本与公开仓库 scripts/load.js 文本一致；线上配置除构建自动加入的 media.videoBytes 外与仓库 wasm/config.json 完全一致。

公开仓库固定版本：{sha}。

- [加载脚本]({repo}/scripts/load.js)
- [抽取算法]({repo}/wasm/src/engine.rs)
- [事件与跳转调度]({repo}/wasm/src/runtime.rs)
- [候选配置]({repo}/wasm/config.json)

## HTTP 跳转链

本次使用真实 GET 请求，保存响应头；HTTP 客户端不执行网页 JavaScript。

| 请求 | 实测链 |
|---|---|
| https://www.米哈游.com/ | 200 OK，无 HTTP 重定向 |
| http://www.米哈游.com/ | 301 → https://www.米哈游.com/ → 200 |
| https://米哈游.com/ | 200 OK，无 HTTP 重定向 |
| /search.html?gacha=ssr-0 | 307 → /search?gacha=ssr-0 → 200 |

三个入口请求取得的 HTML SHA-256 相同：1a1485c937e811e6938650bae540776c64dcc50a6406528fd930802c878cf56e。
入口正文为空，head 中直接引用 `<script src="aha.js"></script>`；没有观察到 meta refresh。aha.js 和 aha.wasm 本次均为 200，大小分别为 14,107 和 178,753 字节。响应含 Cloudflare 标记；不能据此确定实际源站架构或后端源码。

随机目标跳转由浏览器脚本发起，不是入口服务器随机返回 Location。未逐个访问 50 个外部候选网站，因此本报告不声称列出了各目标网站后续的全部 HTTP 跳转。

## 随机算法与概率

加载脚本默认向 WASM 传入 32 位种子：

```js
(Date.now() ^ Math.floor(Math.random() * 0xffffffff)) >>> 0
```

WASM 使用与 Mulberry32 相同的整数状态更新和输出算法，产生 [0,1) 伪随机数；URL 的 seed 参数可覆盖种子。相同种子、相同已保存状态和相同参数能重现结果。仅相同 seed、但保底状态不同，并不能保证相同结果。

默认每次访问抽一次。先抽稀有度，再抽该池的子池和具体 URL；不是对全部 51 条 URL 等概率抽样。

| 档位 | 候选数 | 全新状态第一抽的档位概率 | 池内选择 |
|---|---:|---:|---|
| UR，限定五星 | 1 | 2% | 原神官网 |
| SSR，常驻五星 | 2 | 2% | 初始各 1%；再次抽到常驻时，上一次常驻 URL 的权重减半 |
| SR，四星 | 22 | 30% | 当前池内等概率，每条约 1.3636% |
| R，三星 | 23 普通 + 3 精选 | 66% | 先以 50% 选择普通/精选；普通每条约 1.4348%，精选每条 11% |

以上是全新状态的单次访问概率，不是长期频率。全部卡片当前默认权重为 1，配置 weightCurve=0，所以列表位置本身不影响概率。SSR 的 repeatDamping=0.5，使上一次常驻 URL 在下次抽常驻时占 1/3，另一条占 2/3。

令 p 为自上次五星之后已抽取的非五星次数，五星概率为：

- p=0…10：4%；
- p=11…18：4% + (p−10)×8%，即第12抽12%、第13抽20%，直到第19抽68%；
- p≥19：100%，即第20抽硬保底。

五星结果再决定 UR/SSR：通常 UR 占 50%；若上一次五星是 SSR，则下一次五星必为 UR。每次非保底五星歪到 SSR 会增加 lossStreak；保底得到的 UR 保留该计数，非保底自然抽中 UR 才清零。当计数达到3时，非保底五星的 UR 概率提升到80%。因此不宜把它描述成“连续三个五星都歪”，因为保底 UR 会插在其中。

四星基础分配为 min(30%, 1−五星概率)。如果此前已连续9次未出四星及以上，本抽未中五星时必出 SR；五星会同时清空五星和四星保底计数。

状态保存在 localStorage 的 buwanyuanshen.gacha.v2 下，包含 totalPulls、pity5、pity4、guaranteeUp、lossStreak、lastStandardUrl 等。持久化失效时，保底无法跨访问保持；www 与裸域属于不同 origin，各自保存状态。

## 触发位置与执行顺序

1. head 中 aha.js 执行，解出加载脚本，调用 start()；如处于浏览器预渲染状态，则等待 prerenderingchange。
2. 下载并实例化 aha.wasm，读取 metadata.storageKey 和 localStorage，然后发送 init 事件。
3. WASM 选定结果并先返回 save 指令。普通 R/SR/SSR 随后立即返回 redirect；JS 的 execute() 在 redirect 分支调用 location.replace(c.url)。
4. UR 当前指向原神官网并配有 video/startup-01.mp4，因此先返回 guide。引导元素就绪后，document 上的一次 click 监听发送 start，并不限于点击按钮。
5. start 创建视频并播放，同时设置30秒加载兜底。视频 playing 后另设25秒定时器；较早触发的结束条件生效，且 playing 不会取消加载计时器。
6. skip、ended、媒体/source error、timeout 都会生成 cleanup 和 redirect，最终跳到原神官网。普通的 video.play() Promise 拒绝会走 play_error 分支；自动播放被拦截时静音重试，其余播放拒绝等待计时器兜底，不能一概说所有播放失败都会立即跳转。

跳转目标会附加抽取标记：外站为 #gacha-档位-pity，站内相对链接为 ?gacha=档位-pity。例如 #gacha-r-0 中的0表示此前未出五星次数，不是候选数组下标。

## 可用于自行复核的参数

| 参数 | 当前行为 |
|---|---|
| ?seed=42&probe=1 | 控制台打印抽取结果，不跳转、不保存新状态 |
| ?seed=42&probe=1&reset=1 | 先清空旧状态，再观察可复现的一抽；reset 确实会删除旧进度 |
| ?probe=1&sim=20000&seed=42 | 模拟抽取并打印统计，不保存模拟进度、不跳转 |
| ?pull=10 | 连抽10次，取 UR > SSR > SR > R 的最高档；同档取最先抽到的一条 |
| ?force=ur | 强制限定 UR，进入原神动画流程 |
| ?force=5 | 强制五星，但仍按限定/常驻规则决定结果 |

## 已完成的运行验证与限制

本次在无浏览器、无系统导入接口的隔离调用环境中实例化线上下载的 WASM；该模块 imports 为空。通过其真实 alloc/dispatch 接口复核输出指令，不执行外部候选网站内容。

- 20个 pity5 边界值的 rate5 输出与上述公式一致。
- 43组、共23,000抽，与历史 JS 对照算法在替换为本次线上候选配置并应用已公开的规则修正后完全一致；比较包含卡片、目标 URL、保底状态和随机数状态。
- 验证了状态读取、强制 UR、guide/start/playing/ended，以及 skip/error/timeout、probe、reset、连抽行为。
- 仓库自带旧对照脚本最初因旧候选集合而不通过；更新测试夹具为线上候选配置后通过。这不是直接宣称仓库所有测试原样通过。
- 全新状态、seed=42 的线上 WASM 返回 https://live.bilibili.com/1854314111#gacha-r-0；这是抽到 R 精选卡，不是直播优先规则。

加载脚本虽然保留 readLiveStatus() 函数，当前实际使用 Promise.resolve(null)，不调用该函数；Rust 直播优先分支也已被注释。没有证据表明当前版本会因直播状态强制去往另一个直播间。

上述“已证实”限于本次取得的线上资源和运行输出。公开仓库与线上脚本、配置相符且抽样行为一致，但没有重建并逐字节验证 Rust 编译产物，不能据此保证整个仓库与部署版本完全相同。未在真实浏览器中人工点击验证媒体播放，也未审查不可公开访问的服务端实现。未来部署、地区差异或动态规则变更不在本次结论范围内。

线上 aha.wasm SHA-256：{hashlib.sha256(Path('work/aha.wasm').read_bytes()).hexdigest()}。

## 完整候选集合

下表标题原样来自站点配置，仅用于辨认候选，不代表对账号主体、官网身份或标题事实的独立核验。相对地址 ./search.html 对应当前站点的搜索页。

| 档位 | 子池 | 配置标题 | URL |
|---|---|---|---|
'''
for rarity,group,title,url in rows:
    report+=f'| {rarity} | {group} | {title.replace("|","&#124;")} | [{url}]({url}) |\n'
(out/'analysis.md').write_text(report,encoding='utf8')
headers=[]
for fn in ['https-headers.txt','aha-headers.txt','wasm-headers.txt','http-chain.txt','bare-chain.txt','search-chain.txt']:
    headers.append(f'=== {fn} ===\n'+Path('work',fn).read_text(encoding='utf8'))
(out/'http-evidence.txt').write_text('\n'.join(headers),encoding='utf8')
print('Deliverables:', ', '.join(p.name for p in out.iterdir()))
print('Candidate count:',len(rows))
