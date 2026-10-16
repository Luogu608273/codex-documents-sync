# 米哈游.com 公开跳转逻辑检查

检查日期：2026-10-10，约 17:05—17:11（北京时间）。目标为 https://www.米哈游.com/，ASCII 域名为 www.xn--qvrw50dh7j.com。

## 结论与证据范围

当前版本是客户端“抽卡式”随机跳转：入口 HTML → 混淆 aha.js → aha.wasm → 抽取候选卡片 → JavaScript 执行 location.replace。

共提取出 51 个不同候选地址。候选集合及参数来自本次实际下载的线上 WASM 运行内存，不只是仓库配置，也不是通过少量刷新猜测。线上还原加载脚本与公开仓库 scripts/load.js 文本一致；线上配置除构建自动加入的 media.videoBytes 外与仓库 wasm/config.json 完全一致。

公开仓库固定版本：0cf9782acf0c31ac4b21c7a47171ff8c6f9b1a37。

- [加载脚本](https://github.com/kaitoulapin/xn--qvrw50dh7j.com/blob/0cf9782acf0c31ac4b21c7a47171ff8c6f9b1a37/scripts/load.js)
- [抽取算法](https://github.com/kaitoulapin/xn--qvrw50dh7j.com/blob/0cf9782acf0c31ac4b21c7a47171ff8c6f9b1a37/wasm/src/engine.rs)
- [事件与跳转调度](https://github.com/kaitoulapin/xn--qvrw50dh7j.com/blob/0cf9782acf0c31ac4b21c7a47171ff8c6f9b1a37/wasm/src/runtime.rs)
- [候选配置](https://github.com/kaitoulapin/xn--qvrw50dh7j.com/blob/0cf9782acf0c31ac4b21c7a47171ff8c6f9b1a37/wasm/config.json)

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

线上 aha.wasm SHA-256：0c7a3163b6d6547acf2bbd4b9a33d56027971029c6b851b7dc9a3ee3ba1f69df。

## 完整候选集合

下表标题原样来自站点配置，仅用于辨认候选，不代表对账号主体、官网身份或标题事实的独立核验。相对地址 ./search.html 对应当前站点的搜索页。

| 档位 | 子池 | 配置标题 | URL |
|---|---|---|---|
| UR | 普通 | 原神国服官网（限定5★，出货播启动动画） | [https://ys.mihoyo.com/](https://ys.mihoyo.com/) |
| SSR | 普通 | FGO 国服官网（常驻5★） | [https://game.bilibili.com/fgo/](https://game.bilibili.com/fgo/) |
| SSR | 普通 | 纯静态搜索页（常驻池） | [./search.html](https://www.xn--qvrw50dh7j.com/search.html) |
| SR | 普通 | 《明日方舟》夏日嘉年华限时活动宣传PV | [https://www.bilibili.com/video/BV1fy4y1L7Rq/](https://www.bilibili.com/video/BV1fy4y1L7Rq/) |
| SR | 普通 | 《原神》纳塔交响音乐现场 | [https://www.bilibili.com/video/BV18E4m1d7b7/](https://www.bilibili.com/video/BV18E4m1d7b7/) |
| SR | 普通 | 《崩坏：星穹铁道》白厄角色PV——「日冕」 | [https://www.bilibili.com/video/BV1HfKiz3Ezf/](https://www.bilibili.com/video/BV1HfKiz3Ezf/) |
| SR | 普通 | 《明日方舟》EP - 铁花飞 | [https://www.bilibili.com/video/BV1EBcFznE2H/](https://www.bilibili.com/video/BV1EBcFznE2H/) |
| SR | 普通 | 千恋＊万花OP动画 | [https://www.bilibili.com/video/BV1L4421S7Kr/](https://www.bilibili.com/video/BV1L4421S7Kr/) |
| SR | 普通 | 烂苹果 | [https://www.bilibili.com/video/BV1x5411o7Kn/](https://www.bilibili.com/video/BV1x5411o7Kn/) |
| SR | 普通 | 【原创曲】ウィマーマ・サーガ（羽衣妈妈·物语） | [https://www.bilibili.com/video/BV1n8iEBGEYJ/](https://www.bilibili.com/video/BV1n8iEBGEYJ/) |
| SR | 普通 | Mili - Hero（英雄）【边狱巴士公司】 | [https://www.bilibili.com/video/BV1osSEYGEMd/](https://www.bilibili.com/video/BV1osSEYGEMd/) |
| SR | 普通 | 《崩坏：星穹铁道》EP：「拂晓」 | [https://www.bilibili.com/video/BV12HJBzHERG/](https://www.bilibili.com/video/BV12HJBzHERG/) |
| SR | 普通 | 春日影 | [https://www.bilibili.com/bangumi/play/ep1185679](https://www.bilibili.com/bangumi/play/ep1185679) |
| SR | 普通 | 「Moon Halo」——《崩坏3》印象曲（演唱者：茶理理/TetraCalyx/Hanser） | [https://www.bilibili.com/video/BV1Cg411u7Xr/](https://www.bilibili.com/video/BV1Cg411u7Xr/) |
| SR | 普通 | 【崩坏学园2】德丽莎角色歌《星与你消失之日》PV | [https://www.bilibili.com/video/BV1ds411y7Qc/](https://www.bilibili.com/video/BV1ds411y7Qc/) |
| SR | 普通 | 【60FPS补帧】Poppin'Party/キズナミュージック♪ Full Size MV(1080p+) | [https://www.bilibili.com/video/BV1q7411T7Eh/](https://www.bilibili.com/video/BV1q7411T7Eh/) |
| SR | 普通 | 《鸣潮 3.7 OST》心月狐主题曲 &#124; 月声尽，心灯明 | [https://www.bilibili.com/video/BV19Pad6fEhG/](https://www.bilibili.com/video/BV19Pad6fEhG/) |
| SR | 普通 | 愛♡スクリ～ム!-AiScReam——LoveLive! | [https://www.bilibili.com/video/BV1NdFCesESc/](https://www.bilibili.com/video/BV1NdFCesESc/) |
| SR | 普通 | 斯科特单曲《不许踏上旅途》Don't take the Journey | [https://www.bilibili.com/video/BV11FpeenE6D/](https://www.bilibili.com/video/BV11FpeenE6D/) |
| SR | 普通 | 绝区零周年庆同人节目｜艾莲・乔印象曲｜モエチャッカファイア / エレン・ジョー （CV：若山詩音）｜HoYoFair | [https://www.bilibili.com/video/BV13mGFzeECS/](https://www.bilibili.com/video/BV13mGFzeECS/) |
| SR | 普通 | 【原神拜年纪】让风告诉你 | [https://www.bilibili.com/video/BV18X4y1N7Yh/](https://www.bilibili.com/video/BV18X4y1N7Yh/) |
| SR | 普通 | 【中文CC字幕】【25時、ナイトコードで。 × 鏡音レン】バグ（故障） | [https://www.bilibili.com/video/BV1rY4y1g7qF/](https://www.bilibili.com/video/BV1rY4y1g7qF/) |
| SR | 普通 | HIMEHINA『Mr.VIRTUALIZER』MV | [https://www.bilibili.com/video/BV12K411K7cp/](https://www.bilibili.com/video/BV12K411K7cp/) |
| SR | 普通 | 【歌ってみた】ティアドロップス covered by 燈 | [https://www.bilibili.com/video/BV1Z34y157D7](https://www.bilibili.com/video/BV1Z34y157D7) |
| SR | 普通 | 【本家投稿】 TAK - 'numb numb' feat. Hatsune Miku, Kasane Teto | [https://www.bilibili.com/video/BV1SKLD6NEdC](https://www.bilibili.com/video/BV1SKLD6NEdC) |
| R | 普通 | 腾讯网 | [https://www.qq.com/](https://www.qq.com/) |
| R | 普通 | 鸣潮官方下载网页 | [https://mc.kurogames.com/download/](https://mc.kurogames.com/download/) |
| R | 普通 | 明日方舟终末地 | [https://endfield.hypergryph.com/](https://endfield.hypergryph.com/) |
| R | 普通 | 鹰角网络招聘 | [https://career.hypergryph.com/](https://career.hypergryph.com/) |
| R | 普通 | 异环官网 | [https://yh.wanmei.com/index.html](https://yh.wanmei.com/index.html) |
| R | 普通 | 少前二追放 | [https://gf2.sunborngame.com/](https://gf2.sunborngame.com/) |
| R | 普通 | 卡拉彼丘官网 | [https://klbq.idreamsky.com/](https://klbq.idreamsky.com/) |
| R | 普通 | our notes官网 | [https://bdon.biligames.com/](https://bdon.biligames.com/) |
| R | 普通 | 吉星派对官网 | [https://se.feimogames.com/home](https://se.feimogames.com/home) |
| R | 普通 | 中国反邪教B站主页 | [https://space.bilibili.com/75806856/](https://space.bilibili.com/75806856/) |
| R | 普通 | 米哈游法务部 | [https://space.bilibili.com/3546861952567358/](https://space.bilibili.com/3546861952567358/) |
| R | 普通 | 库洛游戏法务部 | [https://space.bilibili.com/3546379781671377/](https://space.bilibili.com/3546379781671377/) |
| R | 普通 | 鹰角网络法务部（高仿） | [https://space.bilibili.com/3546893747489397/](https://space.bilibili.com/3546893747489397/) |
| R | 普通 | Never Gonna Give You Up - Rick Astley | [https://www.bilibili.com/video/BV1GJ411x7h7/](https://www.bilibili.com/video/BV1GJ411x7h7/) |
| R | 普通 | 碧蓝幻想官网 | [https://game.granbluefantasy.jp/](https://game.granbluefantasy.jp/) |
| R | 普通 | 魔兽世界无限国服 | [https://wow.blizzard.cn/h5/20260913/resads/?channel=ua_bzsz&project_id=8c0da45f60a49f9656c466ca5a8a5ae4](https://wow.blizzard.cn/h5/20260913/resads/?channel=ua_bzsz&project_id=8c0da45f60a49f9656c466ca5a8a5ae4) |
| R | 普通 | 边狱巴士公司 | [https://limbuscompany.com/](https://limbuscompany.com/) |
| R | 普通 | 碧蓝航线官网 | [https://game.bilibili.com/blhx/](https://game.bilibili.com/blhx/) |
| R | 普通 | 碧蓝航线 交汇的航迹 | [https://store.steampowered.com/app/1150080/](https://store.steampowered.com/app/1150080/) |
| R | 普通 | 蔚蓝档案 | [https://bluearchive-cn.com/](https://bluearchive-cn.com/) |
| R | 普通 | 黑暗剑22 | [https://www.bilibili.com/video/BV1Ks421P7ZF/](https://www.bilibili.com/video/BV1Ks421P7ZF/) |
| R | 普通 | 千恋万花中文官网 | [https://hikarifield.co.jp/senren/](https://hikarifield.co.jp/senren/) |
| R | 普通 | 富婆妹官网 | [https://madosoft.net/hamidashi/](https://madosoft.net/hamidashi/) |
| R | 精选 | 瓶子君152 | [https://space.bilibili.com/730732](https://space.bilibili.com/730732) |
| R | 精选 | 买量网址？抹黑游戏？最近掀起二游社区风浪的米哈游.com的注册人到底是谁？本期视频带你了解！ | [https://www.bilibili.com/video/BV1S8pK6xEci/](https://www.bilibili.com/video/BV1S8pK6xEci/) |
| R | 精选 | 哔哩哔哩直播间 1854314111 | [https://live.bilibili.com/1854314111](https://live.bilibili.com/1854314111) |
